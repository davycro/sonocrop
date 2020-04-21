import numpy as np
import cv2
from pathlib import Path

import fire

from sonocrop import vid

def crop(input_file, output_file, thresh=0.1):
  """
  Finds the center of an ultrasound and crops out the static borders
  """

  vid.crop(input_file, output_file, thresh=thresh)


def edges(input_file, thresh=0.1):
  v, fps, f, height, width = vid.loadvideo(input_file)

  u = vid.countUniquePixelsAlongFrames(v)
  u_avg = u/f

  maxW = np.max(u_avg, axis=0)
  left,right = vid.findEdges(maxW, thresh=thresh)
  maxH = np.max(u_avg, axis=1)
  top,bottom = vid.findEdges(maxH, thresh=thresh)

  return (f'{left},{right},{top},{bottom}')


def mask(input_file, output_file, thresh=0.05):
  v, fps, f, height, width = vid.loadvideo(input_file)
  u = vid.countUniquePixelsAlongFrames(v)
  u_avg = u/f
  mask = u_avg > thresh
  y = vid.applyMask(v, mask)
  vid.savevideo(output_file, y, fps)
  return ('Done')


def main():
  fire.Fire()

if __name__ == '__main__':
  main()
