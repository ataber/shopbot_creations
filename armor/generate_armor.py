from math import *

if __name__ == "__main__":
  lines = ['SA', 'J3 0, 0, 1']
  y_lim = 8.5
  x_lim = 3.5
  bit_size = 0.5
  max_depth = 0.25
  material_top = 0.6
  x_cur = 0
  y_cur = 0
  x_step_size = bit_size
  n_x = int(x_lim / x_step_size) + 1
  y_step_size = bit_size * 2
  n_y = int(y_lim / y_step_size) + 1
  for x_cur in range(0, n_x):
    for y_cur in range(0, n_y):
      x = x_cur * x_step_size
      y = y_cur * y_step_size
      if x_cur % 2 == 0:
        y -= bit_size * 0.5
      y_up = y + 0.5 * bit_size
      center = (x_lim / 2., y_lim / 2.)
      x_modifier = exp(-0.5 * (x - center[0])**2 / (x_lim / 4.)**2)
      y_modifier = exp(-0.5 * (y - center[1])**2 / (y_lim / 4.)**2)
      modifier = x_modifier * y_modifier
      plunge = material_top - max_depth * modifier
      lines.append(f'M3 {x} {y} {plunge}')
      lines.append(f'M3 {x} {y_up} {material_top}')
      if y_cur == n_y - 1:
        lines.append(f'M3 {x}, {y_up}, 1')
        lines.append(f'J3 {x + x_step_size}, 0.0, 1')
  lines.append('J3 0, 0, 1')

  with open('armor.gcode', 'w') as f:
    f.write('\n'.join(lines))
