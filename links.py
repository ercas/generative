#!/usr/bin/env python3

from PIL import Image, ImageDraw
from numpy import random
import sys

CANVAS_HEIGHT = 1024
CANVAS_WIDTH = 4096

INDIVIDUAL_MAX_LIFESPAN = CANVAS_WIDTH

class Renderer(object):
    def __init__(self, filename):
        self.canvas = Image.new("RGBA", (CANVAS_WIDTH, CANVAS_HEIGHT),
                                (255, 255, 255))
        self.draw = ImageDraw.Draw(self.canvas)
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
            i["vel_y"] += random.randn() / 100
            i["pos_x"] += 1
            i["pos_y"] += (random.randn() * 2) + i["vel_y"]
            i["lifespan"] -= 1

            i_transparency = 0.8 * i["lifespan"] / INDIVIDUAL_MAX_LIFESPAN

            # TODO: move into relationship class and add other factors
            for key2 in self.objects:
                i2 = self.objects[key2]
                dist = abs(i2["pos_y"] - i["pos_y"])
                if (dist < 200):

                    i2_transparency = 0.8 * i2["lifespan"] / INDIVIDUAL_MAX_LIFESPAN
                    dist_transparency = 0.5 * (200 - dist) / 200 / 2
                    relationship_transparency = min(i_transparency,
                                                    i2_transparency,
                                                    dist_transparency)
                    self.renderer.draw.line(
                        (i["pos_x"], i["pos_y"], i2["pos_x"], i2["pos_y"]),
                        (0, 0, 0, int(relationship_transparency * 255)),
                        1
                    )

            # Drawing
            self.renderer.draw.line(
                (original_pos_x, original_pos_y, i["pos_x"], i["pos_y"]),
                (0, 0, 0, int(i_transparency * 255)),
                3
            )

        for key in to_purge:
            self.objects.pop(key)

    def new(self):
        self.current_id += 1
        self.objects[self.current_id] = {
            "vel_y": 0,
            "pos_x": 0,
            "pos_y": random.rand() * CANVAS_HEIGHT,
            "angle": 0,
            "lifespan": random.randint(INDIVIDUAL_MAX_LIFESPAN / 2,
                                       INDIVIDUAL_MAX_LIFESPAN)
        }

class Relationships(Handler):
    def __init__(self, renderer):
        Handler.__init__(self, renderer)

    def step(self):
        pass

    def new(self, i1, i2):
        self.current_id += 1
        self.objects[self.current_id] = {
            "i1": i1,
            "i2": i2,
            "strength": 0
        }

if (__name__ == "__main__"):
    renderer = Renderer("links.png")
    relationships = Relationships(renderer)
    individuals = Individuals(renderer, relationships)

    for _ in range(100):
        individuals.new()

    for step in range(CANVAS_WIDTH):
        sys.stdout.write("%f (%d/%d)\r" % (step/CANVAS_WIDTH * 100,
                                           step, CANVAS_WIDTH))
        individuals.step()
    print()

    renderer.write()
