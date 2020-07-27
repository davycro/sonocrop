"""
Data visualization library
"""

import numpy as np
import numpy as np
import cv2
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import gridspec
from mpl_toolkits.mplot3d import Axes3D

def showVideoProperties(filename: str):
  capture = cv2.VideoCapture(str(filename))

  frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
  frame_width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
  frame_height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
  frame_rate = int(capture.get(cv2.CAP_PROP_FPS))

  print(f'Video file: {str(filename)}')
  print(f'Frame count: {frame_count}, fps: {frame_rate}, width x height: {frame_width}x{frame_height}')

  return True


def showFrame(filename: str, frame_number= 0, grid= True):
  """
  Display frame number from video
  """

  from sonocrop import vid
  vid, fps, f, height, width = vid.loadvideo(filename)

  plt.figure(figsize=(8,8))
  plt.imshow(vid[frame_number,:,:], cmap='gray')
  plt.grid(grid)
  plt.ylabel('Y')
  plt.xlabel('X')
  plt.show()


def plotPixel(filename: str, x, y, frame_number= 0):
  """
  Display how a pixel's grayscale value changes over time
  """

  from sonocrop import vid as scvid
  vid, fps, f, height, width = scvid.loadvideo(filename)

  plt.figure(figsize=(6,6))

  plt.subplot(211)
  plt.title(f'X:{x} Y:{y}')
  plt.imshow(vid[frame_number,:,:], cmap='gray')
  plt.plot(x,y, 'ro')
  plt.ylabel('Y')
  plt.xlabel('X')


  plt.subplot(212)
  plt.plot(vid[:, y, x], 'b.')
  plt.ylabel('Grayscale value')
  plt.xlabel('Frame number (t)')

  plt.show()


def plotColorVariation3D(filename: str):
  """
  3D chart of how pixel color changes over time
  """

  from sonocrop import vid as scvid
  vid, fps, f, height, width = scvid.loadvideo(filename)

  u = scvid.countUniquePixelsAlongFrames(vid)
  u = u/f
  xx,yy = np.mgrid[0:u.shape[0], 0:u.shape[1]]
  fig = plt.figure(figsize=(10,10))
  ax = fig.add_subplot(111, projection='3d')
  ax.plot_surface(xx, yy, u , rstride=5, cstride=5, cmap='viridis', linewidth=0)
  plt.show()


def plotColorVariation(filename: str):
  """
  2D heatmap of how pixel color changes over time
  """
  from sonocrop import vid as scvid
  vid, fps, f, height, width = scvid.loadvideo(filename)

  u = scvid.countUniquePixelsAlongFrames(vid)
  u_avg = u/f

  # Display heatmap of unique pixels
  plt.figure(figsize=(8,8))
  plt.imshow(u_avg, cmap='hot')
  plt.title('Heat map of unique pixels over time')
  plt.show()


def plotEdgeDetection(filename: str, thresh=0.05):
  """
  Graph of how edges are detected
  """
  from sonocrop import vid as scvid
  vid, fps, f, height, width = scvid.loadvideo(filename)

  scvid.validateVideo(filename)

  u = scvid.countUniquePixelsAlongFrames(vid)
  u_avg = u/f

  # Edge detection
  maxW = np.max(u_avg, axis=0)
  left,right = scvid.findEdges(maxW, thresh=thresh)
  maxH = np.max(u_avg, axis=1)
  top,bottom = scvid.findEdges(maxH, thresh=thresh)

  plt.figure(figsize=(8,4))
  plt.subplot(121)
  plt.plot(maxW)
  plt.plot([left,left], [np.min(maxW), np.max(maxW)], 'r-')
  plt.plot([right,right], [np.min(maxW), np.max(maxW)], 'r-')
  plt.title('Maxiumum value from left to right')

  plt.subplot(122)
  plt.plot(maxH)
  plt.plot([top,top], [np.min(maxH), np.max(maxH)], 'r-')
  plt.plot([bottom,bottom], [np.min(maxH), np.max(maxH)], 'r-')
  plt.title('Maxiumum value from top to bottom')

  plt.tight_layout()
  plt.show()


def showEdges(filename: str, thresh=0.05):
  """
  Display edges of ultrasound
  """
  from sonocrop import vid as scvid
  vid, fps, f, height, width = scvid.loadvideo(filename)

  scvid.validateVideo(filename)

  u = scvid.countUniquePixelsAlongFrames(vid)
  u_avg = u/f

  # Edge detection
  maxW = np.max(u_avg, axis=0)
  left,right = scvid.findEdges(maxW, thresh=thresh)
  maxH = np.max(u_avg, axis=1)
  top,bottom = scvid.findEdges(maxH, thresh=thresh)

  firstFrame = np.array(vid[0,:,:])
  plt.figure(figsize=(8,8))
  plt.imshow(firstFrame, cmap='gray')
  plt.plot([0,width],[top,top],'r-')
  plt.plot([0,width],[bottom,bottom],'r-')
  plt.plot([left,left],[0,height],'r-')
  plt.plot([right,right],[0,height],'r-')
  plt.title('Crop borders')
  plt.show()

  plt.figure(figsize=(8,8))
  plt.imshow(u_avg, cmap='hot')
  plt.plot([0,width],[top,top],'r-')
  plt.plot([0,width],[bottom,bottom],'r-')
  plt.plot([left,left],[0,height],'r-')
  plt.plot([right,right],[0,height],'r-')
  plt.title('Crop borders (heatmap)')
  plt.show()



