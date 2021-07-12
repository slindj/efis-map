import requests
import os
import shutil
import sys
import math
from PIL import Image


x_start = 186
x_end = 191

y_start = 691
y_end = 696

zoom = 10

def downloadmap():
  for x in range(x_start,x_end):
    for y in range(y_start,y_end):
      url = "https://cache.dciwx.com/basemaps/dci/vfr-canada/10/{}/{}.png".format(x,y)
      file = requests.get(url, stream=True)
      dump = file.raw
      location = os.path.abspath("/Users/justinslind/programming/efis-map")
      with open("image-{}-{}.png".format(x,y), 'wb') as location:
        shutil.copyfileobj(dump, location)

def stitch():
  new_im = Image.new('RGB', (256 * (x_end-x_start), 256 * (y_end-y_start)))
  for x in range(x_start,x_end):
    for y in range(y_start,y_end):
      image_file = "image-{}-{}.png".format(x,y)
      print(image_file)
      im=Image.open(image_file)
      new_im.paste(im, (256 * (x-x_start),256 * (y_end-y-1)))
  new_im.save('test.jpg')

def num2deg(xtile, ytile, zoom):
  n = 2.0 ** zoom
  lon_deg = xtile / n * 360.0 - 180.0
  lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
  lat_deg = math.degrees(lat_rad)
  return (lat_deg, lon_deg)

stitch()
(lat_deg, lon_deg) = num2deg(x_start,y_end,zoom)
lat_deg_floor = math.floor(lat_deg)
lat_deg_min = (lat_deg - lat_deg_floor) * 60
lon_deg_floor = math.floor(lon_deg)
lon_deg_min = (lon_deg - lon_deg_floor) * 60
print("North West: ",lat_deg_floor, " ", lat_deg_min,",",lon_deg_floor," ",lon_deg_min)
(lat_deg, lon_deg) = num2deg(x_end,y_start,zoom)
lat_deg_floor = math.floor(lat_deg)
lat_deg_min = (lat_deg - lat_deg_floor) * 60
lon_deg_floor = math.floor(lon_deg)
lon_deg_min = (lon_deg - lon_deg_floor) * 60
print("South East: ",lat_deg_floor, " ", lat_deg_min,",",lon_deg_floor," ",lon_deg_min)
