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
      print(point)
      f.write(f'{point[0]}, {point[1]}, {point[2]}\n')
    for face in faces:
      f.write(f'3 {face[0]}, {face[1]}, {face[2]}\n')

if __name__ == "__main__":
  lines = ['SA', 'J3 0, 0, 1']
  y_lim = 8.5
  x_lim = 3.5
  bit_size = 0.5
  max_depth = 0.25
  material_top = 0.6

  x_step_size = bit_size
  n_x = int(x_lim / x_step_size) + 1
  y_step_size = bit_size * 2
  n_y = int(y_lim / y_step_size) + 1
  for x_cur in range(n_x):
    current_line = []
    for y_cur in range(n_y):
      x = x_cur * x_step_size
      y = y_cur * y_step_size
      if x_cur % 2 == 0:
        y += y_step_size / 2
      center = (x_lim / 2., y_lim / 2.)
      x_modifier = exp(-0.5 * (x - center[0])**2 / (x_lim / 4.)**2)
      y_modifier = exp(-0.5 * (y - center[1])**2 / (y_lim / 4.)**2)
      modifier = x_modifier * y_modifier
      # modifier = 1
      plunge = material_top - max_depth * modifier

      y_next = y + y_step_size
      y_halfstep = y_step_size / 2

      plunge_steps = 50
      for n in range(plunge_steps):
        step_angle = pi * (n / plunge_steps) + pi
        y_step = cos(step_angle) * -y_halfstep
        next_y = y + y_step
        z_step = sin(step_angle) * (material_top - plunge)
        next_z = material_top + z_step
        current_line.append((x, next_y, next_z))
        lines.append(f'M3 {x} {next_y} {next_z}')

      if y_cur == n_y - 1:
        faces = line_topology(current_line)
        to_ply(current_line, faces, f'line_{x_cur}.ply')
        lines.append(f'M3 {x}, {next_y}, 1')
        lines.append(f'J3 {x + x_step_size}, 0.0, 1')
  lines.append('J3 0, 0, 1')

  with open('armor.gcode', 'w') as f:
    f.write('\n'.join(lines))
