lab 01 for CSCI 331 (Intro to Artificial Intelligence).

pre-requisite for running the program: all files exist. Map elevation file is the same size or larger than the
    terrain image file.


NOTES:
---
- Walking speed based on slope: https://en.wikipedia.org/wiki/Tobler%27s_hiking_function
- indexing the _map: map[x][y]_    will give you a map point where _point.x = x_ and _point.y = y_.

- x = latitude
- y = longitude
- z = elevation