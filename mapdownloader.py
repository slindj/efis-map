import argparse
import requests
import os

import shutil
import sys
import math
from PIL import Image
#from PIL.Image import core as _imaging

parser = argparse.ArgumentParser(description='Download and Stitch WMS tiles')
parser.add_argument('maps', nargs='+',
                    help='eFIS map to process, ie: W118N50')
parser.add_argument('-d','--download',action='store_true')
parser.add_argument('--dryrun',action='store_true')
parser.add_argument('-c','--clone',action='store_true')

def downloadmap():
  print("downloading columns " + str(x_start) + " to " + str(x_end))
  for x in range(x_start,x_end+1):
    print("Column " + str(x),end=" ")
    for y in range(y_start,y_end+1):
      url = "https://cache.dciwx.com/basemaps/dci/vfr-canada/10/{}/{}.png".format(x,y)
      file = requests.get(url, stream=True)
      dump = file.raw
      location = os.path.abspath("./tiles/")
      print(".",end='')
      sys.stdout.flush()
      with open("./tiles/image-{}-{}.png".format(x,y), 'wb') as location:
        shutil.copyfileobj(dump, location)
      url = "https://cache.dciwx.com/basemaps/dci/sectionals/10/{}/{}.png".format(x,y)
      file = requests.get(url, stream=True)
      dump = file.raw
      location = os.path.abspath("./tiles-2/")
      print(".",end='')
      sys.stdout.flush()
      with open("./tiles-2/image-{}-{}.png".format(x,y), 'wb') as location:
        shutil.copyfileobj(dump, location)
    print(" ")

def downloadstructure():
  print("downloading columns " + str(x_start) + " to " + str(x_end))
  for x in range(x_start,x_end+1):
    print("Column " + str(x),end=" ")
    for y in range(y_start,y_end+1):
      url = "https://cache.dciwx.com/basemaps/dci/vfr-canada/10/{}/{}.png".format(x,y)
      file = requests.get(url, stream=True)
      dump = file.raw
      location = os.path.abspath("./tiles/")
      print(".",end='')
      sys.stdout.flush()
      try:
        with open("./10/{}/{}-fore.png".format(x,y), 'wb') as location:
          shutil.copyfileobj(dump, location)
      except FileNotFoundError:
        os.makedirs("10/"+str(x))
        with open("./10/{}/{}-fore.png".format(x,y), 'wb') as location:
          shutil.copyfileobj(dump, location)
      url = "https://cache.dciwx.com/basemaps/dci/sectionals/10/{}/{}.png".format(x,y)
      file = requests.get(url, stream=True)
      dump = file.raw
      location = os.path.abspath("./tiles-2/")
      print(".",end='')
      sys.stdout.flush()
      with open("./10/{}/{}-back.png".format(x,y), 'wb') as location:
        shutil.copyfileobj(dump, location)
      new_im = Image.new('RGB', (256, 256))
      try:
        im=Image.open("./10/{}/{}-back.png".format(x,y))
        new_im.paste(im, (0,0),im.convert('RGBA'))
      except Image.UnidentifiedImageError:
        pass
      try:
        im=Image.open("./10/{}/{}-fore.png".format(x,y))
        new_im.paste(im, (0,0),im.convert('RGBA'))
      except Image.UnidentifiedImageError:
        pass
      temp_im = new_im.convert("P", palette=Image.ADAPTIVE, colors=8)
      temp_im.save("./10/{}/{}.png".format(x,y),dpi=(94, 94))
      os.remove("./10/{}/{}-back.png".format(x,y))
      os.remove("./10/{}/{}-fore.png".format(x,y))
    print(" ")


def stitch():
  new_im = Image.new('RGB', (256 * (x_end+1-x_start), 256 * (y_end+1-y_start)))
  print("stiching columns " + str(x_start) + " to " + str(x_end))
  for x in range(x_start,x_end+1):
    print("Column " + str(x),end=" ")
    for y in range(y_start,y_end+1):
      image_file = "./tiles/image-{}-{}.png".format(x,y)
      image_file_us = "./tiles-2/image-{}-{}.png".format(x,y)
      #try to paste the US tile first, doesn't matter if it fails.
      try:
        im=Image.open(image_file_us)
        new_im.paste(im, (256 * (x-x_start),256 * (y_end-y)),im.convert('RGBA'))
      except Image.UnidentifiedImageError:
        print(" ",end='')
      except FileNotFoundError:
        print("/",end='')
      try:
        im=Image.open(image_file)
        new_im.paste(im, (256 * (x-x_start),256 * (y_end-y)),im.convert('RGBA'))
        print(".",end='')
        sys.stdout.flush()
      except Image.UnidentifiedImageError:
        print(" ", end='')
        sys.stdout.flush()
    print(" ")
  new_im.save(map+".jpg")
  print("Map file saved as " + map + ".jpg")

# From https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#Tile_numbers_to_lon./lat._2
def num2deg(xtile, ytile, zoom):
  n = 2.0 ** zoom
  lon_deg = xtile / n * 360.0 - 180.0
  lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
  lat_deg = math.degrees(lat_rad)
  return (lat_deg, lon_deg)
#from https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#Tile_numbers_to_lon./lat._2
def deg2num(lat_deg, lon_deg, zoom):
  lat_rad = math.radians(lat_deg)
  n = 2.0 ** zoom
  xtile = int((lon_deg + 180.0) / 360.0 * n)
  ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
  return (xtile, ytile)


args = parser.parse_args()
print(args.maps, args.download, args.dryrun, args.clone)

for map in args.maps:
  if map == "W076N50":
      lonstart=-42.0
      latend=-068.0
  elif map == "W084N50":
      lonstart=-42.0
      latend=-076.0
  elif map == "W092N50":
      lonstart=-42.0
      latend=-084.0
  elif map == "W100N50":
      lonstart=-42.0
      latend=-092.0
  elif map == "W108N50":
      lonstart=-42.0
      latend=-100.0
  elif map == "W076N58":
      lonstart=-50.0
      latend=-068.0
  elif map == "W084N58":
      lonstart=-50.0
      latend=-076.0
  elif map == "W092N58":
      lonstart=-50.0
      latend=-084.0
  elif map == "W100N58":
      lonstart=-50.0
      latend=-092.0
  elif map == "W108N58":
      lonstart=-50.0
      latend=-100.0
  elif map == "W116N58":
      lonstart=-50.0
      #latstart=-116.0
      #lonend=-58.0
      latend=-108.0
  elif map == "W124N58":
      lonstart=-50.0
      #latstart=-124.0
      #lonend=-58.0
      latend=-116.0
  elif map == "W132N58":
      lonstart=-50.0
      #latstart=-124.0
      #lonend=-58.0
      latend=-124.0
  elif map == "W132N50":
      lonstart=-42.0
      latend=-124.0
  elif map == "W124N50":
      lonstart=-42.0
      latend=-116.0
  elif map == "W116N50":
      lonstart=-42.0
      latend=-108.0
  else:
      print(map + " invalid map.")
      quit()

  latstart=latend-8.0
  lonend=lonstart-8.0

  x_start = 182
  x_end = 204

  y_start = 676
  y_end = 715

  zoom = 10

  #print(deg2num(lonstart,latstart,zoom))
  #print("should be " + str(x_start) + " to " + str(y_start))

  x_start, y_start = deg2num(lonstart,latstart,zoom)
  x_end, y_end = deg2num(lonend,latend,zoom)
  if (args.clone ==True):
    downloadstructure()
  if ((args.download == True) and (args.clone == False)):
    downloadmap()
  if ((args.dryrun == False) and (args.clone == False)):
    try:
      stitch()
    except FileNotFoundError:
      print()
      print()
      print("Could not find tile files.  Try running with -d to download")
  (lat_deg, lon_deg) = num2deg(x_start,y_end,zoom)
  lat_deg = abs(lat_deg)
  lon_deg = abs(lon_deg)
  lat_deg_floor = math.floor(lat_deg)
  lat_deg_min = (lat_deg - lat_deg_floor) * 60
  lon_deg_floor = math.floor(lon_deg)
  lon_deg_min = (lon_deg - lon_deg_floor) * 60
  #print("North West: ",lat_deg_floor, " ", lat_deg_min,",",lon_deg_floor," ",lon_deg_min, "(",lat_deg,",",lon_deg,")")
  (lat_deg, lon_deg) = num2deg(x_end,y_start,zoom)
  lat_deg = abs(lat_deg)
  lon_deg = abs(lon_deg)
  lat_deg_floor = math.floor(lat_deg)
  lat_deg_min = (lat_deg - lat_deg_floor) * 60
  lon_deg_floor = math.floor(lon_deg)
  lon_deg_min = (lon_deg - lon_deg_floor) * 60
  #print("South East: ",lat_deg_floor, " ", lat_deg_min,",",lon_deg_floor," ",lon_deg_min, "(",lat_deg,",",lon_deg,")")
