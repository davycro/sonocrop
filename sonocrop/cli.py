import numpy as np
import cv2
from pathlib import Path

import fire

import sonocrop.vid as vid



def crop(input_file, output_file):
  """
  Finds the center of an ultrasound and crops out the static borders
  """

  vid.crop(input_file, output_file)


def edges(input_file):
  thresh = 0.1
  v, fps, f, height, width = vid.loadvideo(input_file)

  u = vid.countUniquePixelsAlongFrames(v)
  u_avg = u/f

  maxW = np.max(u_avg, axis=0)
  left,right = vid.findEdges(maxW, thresh=0.1)
  maxH = np.max(u_avg, axis=1)
  top,bottom = vid.findEdges(maxH, thresh=0.1)

  return (f'{left},{right},{top},{bottom}')


def main():
  fire.Fire()

if __name__ == '__main__':
  main()
