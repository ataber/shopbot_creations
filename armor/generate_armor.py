from math import *

def line_topology(points):
  faces = []
  for p in range(len(points) - 1):
    faces.append((p, p+1, p))
  return faces

def to_ply(points, faces, filename="debug.ply"):
  with open(filename, 'w') as f:
    header = f"""ply
format ascii 1.0
comment https://github.com/mikedh/trimesh
element vertex {len(points)}
property float x
property float y
property float z
element face {len(faces)}
property list uchar int vertex_indices
end_header\n"""
    f.write(header)
    for point in points:
      f.write(f'{point[0]}, {point[1]}, {point[2]}\n')
    for face in faces:
      f.write(f'3 {face[0]}, {face[1]}, {face[2]}\n')

if __name__ == "__main__":
  lines = ['IF %(25)=1 THEN GOTO UNIT_ERROR', 'SA', 'CN, 90', 'J3,0,0,1', 'TR,17000', 'C6', 'PAUSE 2\n']
  y_lim = 8.5
  x_lim = 3.5
  bit_size = 0.52
  max_depth = 0.25
  material_top = 0.5
  safe_z = material_top + 0.5

  x_step_size = bit_size
  n_x = int(x_lim / x_step_size) + 1
  y_step_size = bit_size * 2
  n_y = int(y_lim / y_step_size) + 1
  gaussian_modifier = lambda p, center, lim: exp(-0.5 * (p - center)**2 / (lim / 2.)**2)
  for x_cur in range(n_x):
    current_line = []
    for y_cur in range(n_y):
      x = x_cur * x_step_size
      y = y_cur * y_step_size
      if x_cur % 2 == 0:
        y += y_step_size / 2
      center = (x_lim / 2., y_lim / 2.)
      x_modifier = gaussian_modifier(x, center[0], x_lim)
      y_modifier = gaussian_modifier(y, center[1], y_lim)
      modifier = x_modifier * y_modifier
      if modifier > 1:
        print(f'modifier {modifier} exceeded max depth {max_depth}')
        exit()
      plunge = material_top - max_depth * modifier

      y_next = y + y_step_size
      y_halfstep = y_step_size / 2

      plunge_steps = 50
      for n in range(plunge_steps):
        step_angle = -pi * (n / plunge_steps)
        y_step = cos(step_angle) * -y_halfstep
        next_y = y + y_step
        z_step = sin(step_angle) * (material_top - plunge)
        next_z = material_top + z_step
        current_line.append((x, next_y, next_z))
        lines.append(f'M3,{x},{next_y},{next_z}')

      if y_cur == n_y - 1:
        faces = line_topology(current_line)
        to_ply(current_line, faces, f'line_{x_cur}.ply')
        # move to next row
        lines.append(f'M3,{x},{next_y},{safe_z}')
        lines.append(f'J3,{x + x_step_size},0.0,{safe_z}')
  lines.append('J3,0,0,1')
  lines.append('C7')
  lines.append('END')

  lines.append('\nUNIT_ERROR:')
  lines.append('CN, 97')
  lines.append('END')

  with open('armor.sbp', 'w') as f:
    f.write('\n'.join(lines))
