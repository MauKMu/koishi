# koishi.py

Python 3 script for generating an SVG file with paths that resemble Koishi's "Genetics of the Subconscious" spell card from Touhou 11.

## Dependencies

`svgwrite`

## Instructions

Make any modifications to the parameters as desired, then simply run `koishi.py` with Python 3.

## Overview

The script uses two classes, `EllipticTrajectory` and `InterpolatedTrajectory` to output the points that should be on our desired path. The spell card's pattern is modelled as two ellipses that follow a "parent" point, which itself follows an arbitrary trajectory defined by the user.

The "speeds" of each trajectory can be adjusted, as well as how much of the arbitrary trajectory should be followed by the parent point. Changing these parameters is key to getting the final the output you want.

In the future, I might implement having these parameters being read from a YAML file. Right now, they should be editted from within the script (`ELLIPSE_SCALE`, `PARENT_SCALE`, `nodes` in `main`).

The size and rotation of the ellipses can also be changed, if you feel adventurous.

An older version where the "time" parameter behaves differently has been included for completion's sake, since it generates slightly different output.

# Example output

An example of an output where the parent point follows a heart-shaped trajectory is included in `img/example_output.svg`. Below are two rasterized versions, one of which is rotated to its "correct" orientation.

These images were generated with `ELLIPSE_SCALE = 2 * PI`, `PARENT_SCALE = 2` and `nodes = 200 * 15`.

![Rasterized](img/example_raster.png)

![Rasterized and rotated](img/example_raster_rotated.png)

## After running the script

The resulting SVG file can be opened in Inkscape for further editing. You may, for example, choose to use a smaller number of nodes and use Inkscape to transform the straight-line segments into smooth Bezier curves automatically.

I pasted a bullet pattern (actually just a circle) using the `Scatter` extension (Extensions > Generate from Path > Scatter). This is what I used instead of `Pattern along Path` because `Scatter` actually lays down the patterns in an overlapping way, which the other extensions/effects do not. Instead, they place the pattern down as if they were all on the same z-height.

### Manually fixing Z-order

At points where the bullet paths overlap, I chose to manually alter the z-order of clusters of bullets to give the impression than the paths are twisting and coiling (like DNA strands). Unfortunately, just doing this gets rid of the order in which the bullets are overlapped in their individual paths.

In particular, doing this creates a bullet that either covers or is covered by its two neighbors, which shouldn't happen. In other words, we have a pair of bullets in the opposite z-order.

![Before changing z-order](img/ks_0_before.png)

*Before changing z-order*

![After changing z-order](img/ks_1_after.png)

*After changing z-order; note the bullet covering both its neighbors, and how it creates an "offending pair"*

I fixed this manually by creating a clipping path from the bullets in the offending pair to restore the apparent z-order between those two bullets without actually changing their z-orders.

The idea is to create a clipping path that covers only the part of the bullet that should be visible. To accomplish this, we begin with a circular path corresponding to the bullet that will be clipped (this places the path on the "bottom"). Since the bullets have a stroke width, we need to:

* 1) Unclone the bullet clone

* 2) Ungroup the bullet group into its two constituent circular paths

* 3) Delete the innermost path

* 4) Select the remaining path and add a fill color (so it has both a fill and a stroke; this should not change its shape)

![After step 4](img/ks_2_bottom_path.png)

* 5) Duplicate the path and, on one of the duplicates (one should be automatically selected), remove the stroke by clicking on the X

![After step 5](img/ks_3_remove_stroke.png)

* 6) Select the other path, which should contain a stroke color, and do Path > Stroke to Path

* 7) Union the two paths into a big circular path

![After step 7](img/ks_4_path_done.png)

This procedure is necessary because Stroke to Path would not normally retain the size of the original path.

Repeat this for the other bullet in the offending pair, creating a circular path on top of the previous one. Select both paths and perform a boolean subtraction. This should give you a circular path with a concave hole in it. Use this as a clip (Object > Clip > Set).

Below are some additional images illustrating this process:

![Both circular paths](img/ks_5_top_path.png)

*Both circular paths created*

![Ready to clip](img/ks_6_clip_ready.png)

*After performing subtraction, we have a clipping path ready*

![All done](img/ks_7_all_done.png)

*All done -- the offending pair is gone!*

## Special thanks

Thanks to [http://verysimpledesigns.com/vectors/inkscape-tutorial-fancy-borders.html](this page) for showing me the light of the `Scatter` extension.
