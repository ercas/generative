inspired by the work of [anders hoff](http://inconvergent.net)

![links demo](links.png)
links (WIP)
=====
_links_ is an oversimplified visualization of how relationships form, develop,
and persist over time.

individuals
-----------
individuals are represented by jagged, wandering lines. their opacity is
indicative of the amount of time that they have left.
* individuals' lifespans are predetermined when they are created
* semi-random movement:
    * horizontal speed is constant
    * vertical speed is sampled from a normal distribution at each step
* there is a random chance to form relationships with nearby individuals
* individuals are more or less likely to form relationships based on:
    * [difference in age group][dlc2016]
    * similarities
    * time spent in close proximity
    * "friends of friends"

relationships
-----------
relationships are represented by the shaded areas between pairs of individuals.
their opacity is indicative of the strength of the individuals' relationship
with each other.
* strength is based on:
    * proximity
    * [difference in age group][dlc2016]
    * similarities
* strengthens/deteriorates based on distance and random chance
* influences the paths of individuals
* terminates when one of the participating individuals ceases to exist

[dlc2016]: https://arxiv.org/abs/1606.07556v1 "Do the Young Live in a 'Smaller
World' Than the Old? Age-Specific Degrees of Separation in a Large-Scale Mobile
Communication Network"
