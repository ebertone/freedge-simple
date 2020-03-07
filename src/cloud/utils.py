
import re
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def draw_boxes(img, bboxes, classes, scores, color='YellowGreen'):
  """Draw bounding boxes + class + probabilities on an image
  """
  if len(bboxes) == 0:
      return img
  im_height, im_width, _ = img.shape
  im_height, im_width, _ = img.shape
  bboxes = [box * np.array([im_height, im_width, im_height, im_width]) for box in bboxes]

  image = Image.fromarray(img)
  try:
      font = ImageFont.truetype('arial.ttf', 32)
  except IOError:
      font = ImageFont.load_default()
  thickness = (image.size[0] + image.size[1]) // 350
  draw = ImageDraw.Draw(image)
  for box, category, _ in zip(bboxes, classes, scores):
    ymin, xmin, ymax, xmax = [int(i) for i in box]
    (left, right, top, bottom) = (xmin, xmax, ymin, ymax)

    draw.line([(left, top), (left, bottom), (right, bottom),
               (right, top), (left, top)], width=thickness, fill=color)

    text_bottom = top
  # Reverse list and print from bottom to top.
    text_width, text_height = font.getsize(category)
    margin = np.ceil(0.05 * text_height)
    draw.rectangle(
        [(left, text_bottom - text_height - 2 * margin), (left + text_width,
                                                          text_bottom)],
        fill=color)
    draw.text(
        (left + margin, text_bottom - text_height - margin),
        category,
        fill='black',
        font=font)

  del draw
  return np.array(image)

def parse_label_map(label_map_path):
  """Parse label map file into a dictionary
  Args:
    label_map_path:

  Returns:
    a dictionary : key: obj_id value: obj-name
  """
  # Open image has different label maps:  {name: ... id: .... display_name: ...}
  # MSCOCO and PASCAL has: {id:... name: ...}
  is_oid = False
  if 'oid' in label_map_path.split('/')[-1]:
    is_oid = True
    parser = re.compile(r'name:\s+\"(?P<name>[/\w_-]+)\"\s+id:\s+(?P<id>[0-9]+)\s+display_name:\s+\"(?P<display_name>[\w_-]+)\"')
  else:
      parser = re.compile(r'id:[^\d]*(?P<id>[0-9]+)\s+name:[^\']*\'(?P<name>[\w_-]+)\'')
  # Read label_map file
  with open(label_map_path, 'r') as f:
    lines = f.read().splitlines()
    lines = ''.join(lines)

    # match group having the same language 
    result = parser.findall(lines)
    if is_oid:
      label_map_dict = {int(item[1]): item[2] for item in result}
    else:
      label_map_dict = {int(item[0]): item[1] for item in result}

    return label_map_dict

