inspired by the work of [anders hoff](http://inconvergent.net)

![links demo](img/links-175.jpg)
links (WIP)
=====
_links_ is an oversimplified visualization of how relationships form, develop,
and persist over time.

_links-old_ is an early version of _links_ without much functionality, but it
still produces nice images.

individuals
-----------
individuals are represented by jagged, wandering lines. their opacity is
indicative of the amount of time that they have left.
* individuals' lifespans are predetermined when they are created
* semi-random movement:
    * horizontal speed is constant
    * vertical speed is sampled from a normal distribution at each step and
      additional jitter is applied
* individuals' interests shift over time
* there is a chance to form relationships when close to other individuals
* individuals are more or less likely to form relationships based on:
    * proximity
    * [difference in age group][dlc2016]
    * similar interests

relationships
-------------
relationships are represented by the shaded areas between pairs of individuals.
their opacity is indicative of the strength of the participaing individuals'
relationship with each other.
* strength is based on:
    * proximity
    * [difference in age group][dlc2016]
    * similar interests
* strengthens/deteriorates based on distance and random chance
* influences the paths of individuals
* influences the interests of individuals
* terminates when one of the participating individuals ceases to exist

caveats
-------

observations
------------
* groups of like-minded individuals pull in more members more easily as they
  become larger, creating a positive feedback loop
* very few individuals who exist longer than average maintain relationships with
  other individuals

[dlc2016]: https://arxiv.org/abs/1606.07556v1 "Do the Young Live in a 'Smaller
World' Than the Old? Age-Specific Degrees of Separation in a Large-Scale Mobile
Communication Network"
