#!/usr/bin/env python3
"""
Draws Genetics of the Subconscious as a straight-line path in an SVG file.
Can later be smoothed in Inkscape, for example.
"""
import svgwrite
from math import sin, cos, sqrt
from math import pi as PI

class EllipticTrajectory:

  def __init__(self, rotation, x_length, y_length):
    """
    rotation : (float) Rotation from canonical +axis in radians
    x_length : (float) Length of ellipse's x-axis
    y_length : (float) Length of ellipse's y-axis
    """
    self.rotation = rotation 
    self.x_length = x_length 
    self.y_length = y_length 
    self.t = 0.0 # parameter in parametric equations
    self.curr_pos = (0, 0)
    self.last_pos = self.get_next_position(0)
    self.curr_pos = self.last_pos
  
  def get_next_position(self, step):
    self.t += step
    # Combine parametric equation and 2D rotation
    x = (self.x_length * cos(self.t) * cos(self.rotation) - 
         self.y_length * sin(self.t) * sin(self.rotation))
    y = (self.x_length * cos(self.t) * sin(self.rotation) +
         self.y_length * sin(self.t) * cos(self.rotation))
    if self.t >= 1000 * PI:
      self.t -= 1000 * PI
    elif self.t <= -1000 * PI:
      self.t += 1000 * PI
    self.last_pos = self.curr_pos
    self.curr_pos = (x, y)
    return (x, y)

  def get_delta(self, step):
    """Steps to next position and returns delta of curr - last positions."""
    self.get_next_position(step)
    return (self.curr_pos[0] - self.last_pos[0],
            self.curr_pos[1] - self.last_pos[1])

class InterpolatedTrajectory:
  """
  Each trajectory is a list of nodes, which are visited sequentially.
  Each node is a tuple of three floats: (x, y, time).
  x is the node's x-coordinate.
  y is the node's y-coordinate.
  time is a scaling factor that represents how long it should take
  to reach the next node.
  Thus, time can be used to have varying speeds and to force
  a trajectory to stop for a while at a certain node;
  e.g. [(0, 0, 5), (0, 0, 1), (1, 1, 1)] stops at (0, 0) for a while.

  The list of nodes is treated as cyclic. In other words, if you
  provide a list of n nodes, the trajectory at the n-th node will
  move towards the 1st node.

  Note that there must exist at least one node with non-zero time.
  The constructor checks for this and will throw a ValueError if the list doesn't have at least one node with non-zero time.
  It also checks if each node has exactly three values, as it should.
  """

  def __init__(self, nodes):
    """
    nodes : (list) List of nodes.
    """
    found_nonzero_time = False
    for node in nodes:
      if len(node) != 3:
        raise ValueError('Expected 3 values in node {0}!'.format(node))
      if node[2] != 0.0:
        found_nonzero_time = True
    if not found_nonzero_time:
      raise ValueError('List of nodes must contain at least one node with non-zero time!')
    self.nodes = nodes
    self.index = 0
    self.next_index = self._get_next_index()
    self.time = 0.0
    self.last_pos = nodes[0][0:2]
    self.curr_pos = self.last_pos
    self.target_time = nodes[0][2]
  
  def _get_next_index(self):
    if self.index + 1  >= len(self.nodes):
      return 0
    else:
      return self.index + 1

  def _go_to_next_index(self):
    # Update indices
    self.index = self.next_index
    self.next_index = self._get_next_index()
    # Update target time
    self.target_time = self.nodes[self.index][2]

  def get_next_position(self, step):
    # Handle target time = 0
    # Shouldn't be infinite loop as long as nodes list isn't modified
    while self.target_time == 0.0:
      self._go_to_next_index()
    # if new self.time >= self.target_time, move on to next index, jumping over
    # multiple indices if needed, and make self.time < 1.0
    # also consider different time values for each node
    if self.time + step >= self.target_time:
      remaining_step = step - (self.target_time - self.time)

      self._go_to_next_index()

      while remaining_step >= self.target_time:
        # Find portion of step that contributed to movement 
        # and subtract it from remaining step
        remaining_step -= self.target_time

        if remaining_step < 0.0:
          remaining_step = 0.0

        # Note target time is updated here
        self._go_to_next_index()

      # Treat self.time as if it were 0.0 now, and "add" increment
      self.time = remaining_step
    else:
      self.time += step
    # Interpolate
    start_x = self.nodes[self.index][0]
    delta_x = self.nodes[self.next_index][0] - start_x
    start_y = self.nodes[self.index][1]
    delta_y = self.nodes[self.next_index][1] - start_y

    self.last_pos = self.curr_pos
    self.curr_pos = (start_x + delta_x * self.time / self.target_time, 
                     start_y + delta_y * self.time / self.target_time)

    return self.curr_pos

  def get_delta(self, step):
    self.get_next_position(step)
    return (self.curr_pos[0] - self.last_pos[0],
            self.curr_pos[1] - self.last_pos[1])

def main():
  X_NODES = [(0, 0, 1), (2000, 2000, 1), (2000, 0, 1), (0, 2000, 1)]

  # straight-line segments have lower speed
  HEART_NODES = [(1042.397, 0.0, 2),
                 (222.128, 798.490, 1),
                 (75.494, 1003.194, 1),
                 (0.0, 1286.295, 1),
                 (2.908, 1493.902, 1),
                 (76.948, 1740.708, 1),
                 (239.549, 1927.991, 1),
                 (371.661, 2007.840, 1),
                 (541.524, 2045.586, 1),
                 (707.029, 2013.647, 1),
                 (823.173, 1927.991, 1),
                 (904.474, 1881.533, 1),
                 (1042.397, 1871.370, 1),
                 (1180.316, 1881.533, 1),
                 (1261.617, 1927.991, 1),
                 (1377.761, 2013.647, 1),
                 (1543.266, 2045.586, 1),
                 (1713.124, 2007.840, 1),
                 (1845.240, 1927.991, 1),
                 (2007.842, 1740.708, 1),
                 (2081.886, 1493.902, 1),
                 (2084.785, 1286.295, 1),
                 (2009.291, 1003.194, 1),
                 (1862.662, 798.490, 2)]

  ELLIPSE_SCALE = 2 * PI
  PARENT_SCALE = 2
  et_1 = EllipticTrajectory(PI / 4, 200, 25)
  et_2 = EllipticTrajectory(3 * PI / 4, 200, 25)
  parent = InterpolatedTrajectory(HEART_NODES)

  dwg = svgwrite.drawing.Drawing('time-fixed.svg')
  path_1 = dwg.add(dwg.path(style='stroke:#00ff00;fill:none;stroke-width:5;stroke-miterlimit:4;stroke-dasharray:none'))
  path_2 = dwg.add(dwg.path(style='stroke:#0000ff;fill:none;stroke-width:5;stroke-miterlimit:4;stroke-dasharray:none'))
 
  path_1.push('M {0:.4} {1:.4}'.format(parent.curr_pos[0] + et_1.curr_pos[0], parent.curr_pos[1] + et_1.curr_pos[1]))
  path_2.push('M {0:.4} {1:.4}'.format(parent.curr_pos[0] + et_2.curr_pos[0], parent.curr_pos[1] + et_2.curr_pos[1]))

  step = 0.005

  nodes = int(200 * 15)
  threshold = nodes / 10

  for i in range(nodes):
    if not i % threshold:
      print("{:3.0%} done.".format(i / float(nodes)))
    parent_delta = parent.get_delta(step * PARENT_SCALE)
    et_1_delta = et_1.get_delta(step * ELLIPSE_SCALE)
    et_2_delta = et_2.get_delta(step * ELLIPSE_SCALE)

    path_1.push('l {0:.4} {1:.4}'.format(parent_delta[0] + et_1_delta[0], parent_delta[1] + et_1_delta[1]))
    path_2.push('l {0:.4} {1:.4}'.format(parent_delta[0] + et_2_delta[0], parent_delta[1] + et_2_delta[1]))

  print("Writing SVG file...")
  dwg.save()
  print("Done!")

if __name__ == '__main__':
  main()
