##
#dependencies


#json_up function is a method for unpacking jsonified data from a index location in a pandas dataframe.
def json_up(inp):
  if inp != '{}':
      j = json.loads(inp)
      return pd.Series({'x': j.get('x', 0), 'y': j.get('y', 0), 'width': j.get('width', 0), 'height': j.get('height', 0)})
  else:
      return pd.Series({'x': 0, 'y': 0, 'width': 0, 'height': 0})

#getmeta function takes an image path from the training data store & pulls some metadata on it,
# returning, a tuple 
def getmeta(image_path):
  with Image.open(image_path) as img:
    width, height = img.size
    
    creation_timestamp = os.path.getctime(image_path)
    creation_date = datetime.datetime.fromtimestamp(creation_timestamp)
    
  return creation_date, width, height

#this operates on a single row o
def imagerescale(row, path, target_size):

  image_path = os.path.join(path,row['filename'])
  
  with Image.open(image_path) as img:
    #actual resizing
    resized_img = img.resize(target_size)
    resized_img.save(image_path)

    #obtaining scale factors
    width_factor = target_size[0] / img.size[0]
    height_factor = target_size[1] / img.size[1]

    #new params for new image log
    x = int(row['x'] * width_factor)
    y = int(row['y'] * height_factor)
    w = int(row['width'] * width_factor)
    h = int(row['height'] * height_factor)

    #rescaling any associated bounding boxes with image
    if x != 0 and y != 0 and w != 0 and h !=0:
      row['region_shape_attributes'] = f'{'name':'rect','x': {x},'y': {y},'width': {w},'height': {h}}'
      row['x'] = x
      row['y'] = y
      row['width'] = w
      row['height'] = h
      row['imwidth'] = target_size[0]
      row['imheight'] = target_size[1]
    
    
  return row
    

  
