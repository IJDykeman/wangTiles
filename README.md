# Wang Tiles
Experiments with wang-like tiles

For details on this project, see by blog post: http://ijdykeman.github.io/ml/2017/10/12/wang-tile-procedural-generation.html

This project allows interesting images to be created by defining a set of 'tiles' where each tile is a 3x3 grid of colors.  These tiles are arranged so that their colors match along abutting edges.  It is easy to create map-like images with this system by creating, for instance, all blue ocean tiles, all green grass tiles, and tiles with some blue and some green that define a shore.  To prevent the system from taking this set of tiles and creating a degenerate map solution (one where, for instance, all tiles are simply set to ocean), an element of randomness is used to select which tiles to place in a given location.  This introduces the hard problem of arranging tiles in a partly random way that still satisfies the edge matching criteria. This is the central challenge of this project.  It is necessary to employ some trickery to accomplish this, since no polynomial time algorithm exists for the tiling problem.  This trickery can cause obvious artifacts in the images the system produces, slow runtimes, partly degenerate solutions, or poor adherence to desired ratios between numbers of different types of tiles.  Indeed, the question of whether a given set of tiles can cover an infinite plane (as would be required to make an endless map) [is not decidable.](https://en.wikipedia.org/wiki/Wang_tile#Domino_problem)


True wang tiles are a type of formal system which can be visualized as squares with a color on each side.  A valid tiling of these tiles involves the squares being placed on a grid such that touching edges of adjacent tiles have the same color.
