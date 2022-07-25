from loguru import *

def line_topology(points):
  faces = []
  for p in range(len(points) - 1):
    faces.append((p, p+1, p))
  return faces

def to_ply(points, filename="debug.ply"):
  faces = line_topology(points)
  with open(filename, 'w') as f:
    header = f"""ply
format ascii 1.0
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

def end_sequence():
  return [
    'J3,0,0,1',
    'C7',
    'END',
    '\nUNIT_ERROR:',
    'CN, 97',
    'END'
  ]

def begin_sequence():
  return [
    'IF %(25)=1 THEN GOTO UNIT_ERROR',
    'SA',
    'CN, 90',
    'J3,0,0,1',
    'TR,17000',
    'C6',
    'PAUSE 2\n'
  ]

def make_multiple_passes(line, depth_per_pass=0.0625):
  max_depth = max([l[2] for l in line])
  if max_depth < depth_per_pass:
    max_depth = depth_per_pass

  n_passes = ceil(max_depth / depth_per_pass)
  passes = []
  for p in range(n_passes):
    depth_multiplier = (p + 1) * (depth_per_pass / max_depth)
    assert depth_multiplier <= 1
    plunge_pass = [[p[0], p[1], p[2] * depth_multiplier for p in line]]
    passes += plunge_pass

  return passes

def create_shopbot_file(path, filebase):
  lines = []
  lines += begin_sequence()
  lines += make_multiple_passes(path)
  lines += end_sequence()
  to_ply(lines, f'{filebase}.ply')

  with open(f'{filebase}.sbp', 'w') as f:
    f.write('\n'.join(lines))
