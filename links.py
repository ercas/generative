#!/usr/bin/env python3

from PIL import Image, ImageDraw
from numpy import random
from optparse import OptionParser
import sys


parser = OptionParser(add_help_option = False)
parser.add_option("-n", "--individuals", dest = "num_individuals", type = "int",
                  default = 100)
parser.add_option("-o", "--output", dest = "filename", type = "string",
                  default = "links.png")
parser.add_option("-w", "--width", dest = "width", type = "int",
                  default = 4096)
parser.add_option("-h", "--height", dest = "height", type = "int",
                  default = 1024)
parser.add_option("--help", action = "help")
(options, args) = parser.parse_args()

FILENAME = options.filename

CANVAS_WIDTH = options.width
CANVAS_HEIGHT = options.height

NUM_INDIVIDUALS = options.num_individuals

DRAW_COLOR = [random.randint(90, 140), random.randint(90, 140),
              random.randint(90, 140)]
#DRAW_COLOR = [0, 0, 0]
DRAW_I_TRANSPARENCY = 0.2
DRAW_R_TRANSPARENCY = 0.2

I_MAX_VEL_Y = 0.8
I_MAX_LIFESPAN = CANVAS_WIDTH * 1.2
I_MIN_LIFESPAN = CANVAS_WIDTH / 2
I_BASIC_INTEREST_RANGE = 255

R_CONTACT_DISTANCE = 60
R_MIN_STRENGTH = 0
R_MAX_STRENGTH = 25

def similarity(value_1, value_2, max_value):
    return (max_value - abs(value_1 - value_2)) / float(max_value)

class Renderer(object):
    def __init__(self, filename):
        self.canvas = Image.new("RGB", (CANVAS_WIDTH, CANVAS_HEIGHT),
                                (255, 255, 255))
        self.draw = ImageDraw.Draw(self.canvas, "RGBA")
        self.filename = filename

    def write(self):
        output_file = open(self.filename, "wb")
        self.canvas.save(output_file)
        output_file.close()

class Handler(object):
    def __init__(self, renderer):
        self.renderer = renderer
        self.objects = {}
        self.current_id = 0

class Relationships(Handler):
    def __init__(self, renderer):
        Handler.__init__(self, renderer)

    def make_connections(self, i1, i2):
        dist = abs(i1["pos_y"] - i2["pos_y"])

        if (
            (dist < R_CONTACT_DISTANCE)
            and (similarity(i1["interests"], i2["interests"],
                            I_BASIC_INTEREST_RANGE) < 0.4)
            and (similarity(i1["lifespan"], i2["lifespan"],
                            I_MAX_LIFESPAN) < 0.7)
            ):
            self.new(i1, i2)

    def step(self):
        to_purge = []

        for key in self.objects:
            relationship = self.objects[key]

            i1 = relationship["i1"]
            i2 = relationship["i2"]

            if (i1["lifespan"] <= 0) or (i2["lifespan"] <= 0):
                to_purge.append(key)
                continue

            # relationship strength calculation
            dist = abs(i1["pos_y"] - i2["pos_y"])
            distance_similarity = similarity(i1["pos_y"], i2["pos_y"],
                                             R_CONTACT_DISTANCE)
            interest_similarity = similarity(i1["interests"], i2["interests"],
                                             I_BASIC_INTEREST_RANGE)

            age_similarity = (similarity(i1["lifespan"], i2["lifespan"],
                                         I_MAX_LIFESPAN)
                              * (i1["lifespan"] + i2["lifespan"])
                              / I_MAX_LIFESPAN / 2)
            relationship["strength"] += 0.6 * (distance_similarity
                                               + interest_similarity
                                               + 0.7 * age_similarity
                                               + random.randn() / 2) / 4

            # bounds checking
            relationship["strength"] = min(relationship["strength"],
                                           R_MAX_STRENGTH)
            if (relationship["strength"] <= R_MIN_STRENGTH):
                to_purge.append(key)
                continue

            # move individuals closer to each other
            dy = random.randn()
            if (dy > 1.4):
                change_vel = False
                if (dy > 2.5):
                    change_vel = True
                dy = dy * relationship["strength"] / R_MAX_STRENGTH
                if (i1["pos_y"] < i2["pos_y"]):
                    dy = -dy
                if (change_vel):
                    i1["vel_y"] -= dy / 30
                    i2["vel_y"] += dy / 30
                i1["pos_y"] -= dy / 4
                i2["pos_y"] += dy / 4
                i1["interests"] -= dy / 3
                i2["interests"] += dy / 3

            # drawing
            i1_transparency = (DRAW_I_TRANSPARENCY * i1["lifespan"]
                               / I_MAX_LIFESPAN)
            i2_transparency = (DRAW_I_TRANSPARENCY * i2["lifespan"]
                               / I_MAX_LIFESPAN)
            strength_transparency = (DRAW_R_TRANSPARENCY
                                     * relationship["strength"]
                                     / R_MAX_STRENGTH)
            relationship_transparency = min(i1_transparency, i2_transparency,
                                            strength_transparency)
            self.renderer.draw.line(
                (i1["pos_x"], i1["pos_y"], i2["pos_x"], i2["pos_y"]),
                tuple(DRAW_COLOR + [int(relationship_transparency * 255)]),
                1
            )

        for key in to_purge:
            self.objects.pop(key)

    def new(self, i1, i2):

        # don't create duplicates
        for key in self.objects:
            relationship = self.objects[key]
            if (relationship["i1"] == i1) and (relationship["i2"] == i2):
                return

        self.current_id += 1
        self.objects[self.current_id] = {
            "i1": i1,
            "i2": i2,
            "strength": 0
        }

class Individuals(Handler):
    def __init__(self, renderer, relationships_handler):
        Handler.__init__(self, renderer)
        self.relationships = relationships_handler

    def step(self):
        to_purge = []

        for key in self.objects:
            i = self.objects[key]

            if (i["lifespan"] == 0):
                to_purge.append(key)
                continue

            original_pos_x = i["pos_x"]
            original_pos_y = i["pos_y"]
            i["vel_y"] += random.randn() / 50
            i["vel_y"] = min(max(i["vel_y"], -I_MAX_VEL_Y), I_MAX_VEL_Y)
            i["pos_x"] += 1
            i["pos_y"] += random.randn() + i["vel_y"]
            i["lifespan"] -= 1
            i["interests"] += random.randn() / 100

            for key2 in self.objects:
                i2 = self.objects[key2]
                if (i2 == i):
                    continue
                self.relationships.make_connections(i, i2)

            # Drawing
            i_transparency = (DRAW_I_TRANSPARENCY * i["lifespan"]
                              / I_MAX_LIFESPAN)
            self.renderer.draw.line(
                (original_pos_x, original_pos_y, i["pos_x"], i["pos_y"]),
                tuple(DRAW_COLOR + [int(i_transparency * 255)]),
                3
            )

        for key in to_purge:
            self.objects.pop(key)

    def new(self):
        self.current_id += 1
        self.objects[self.current_id] = {
            "vel_y": 0,
            "pos_x": 0,
            "pos_y": (random.rand() * CANVAS_HEIGHT * 1.25) - CANVAS_HEIGHT / 4,
            "angle": 0,
            "lifespan": random.randint(I_MIN_LIFESPAN, I_MAX_LIFESPAN),
            "interests": random.randint(0, I_BASIC_INTEREST_RANGE)
        }

if (__name__ == "__main__"):
    renderer = Renderer(FILENAME)
    relationships = Relationships(renderer)
    individuals = Individuals(renderer, relationships)

    for _ in range(NUM_INDIVIDUALS):
        individuals.new()

    for step in range(CANVAS_WIDTH):
        sys.stdout.write("%f%% (%d/%d)\r" % (float(step)/CANVAS_WIDTH * 100,
                                             step, CANVAS_WIDTH))
        sys.stdout.flush()
        relationships.step()
        individuals.step()
    print("")

    renderer.write()
