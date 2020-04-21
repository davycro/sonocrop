import numpy as np
import cv2
from pathlib import Path


def loadvideo(filename: str):
    capture = cv2.VideoCapture(str(filename))

    frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_rate = int(capture.get(cv2.CAP_PROP_FPS))

    v = np.zeros((frame_count, frame_height, frame_width), np.uint8)

    for count in range(frame_count):
        ret, frame = capture.read()
        if not ret:
            raise ValueError("Failed to load frame #{} of {}.".format(count, filename))

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        v[count] = frame

    return (v, frame_rate, frame_count, frame_height, frame_width)


def savevideo(outFile, array, fps):
    f, height, width = array.shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(str(outFile), fourcc, fps, (width, height), False)
    for i in range(f):
        out.write(array[i, :,:])
    out.release()


def countUniquePixels(a):
    return len(np.unique(a))


def countUniquePixelsAlongFrames(vid):
    f, height, width = vid.shape
    u = np.zeros((height, width), np.uint8)
    for i in range(height):
        u[i] = np.apply_along_axis(countUniquePixels, 0, vid[:,i,:])

    return u


def findEdges(x, thresh=0.1):
    # find the right
    right = len(x)
    a = x[int(len(x)/2):-1]
    b, = np.where( a <= thresh )
    if len(b)>0:
        right = int(len(x)/2)+b[0]

    # find the left
    left = 0
    a = np.flip(x[0:int(len(x)/2)])
    b, = np.where( a <= thresh )
    if len(b)>0:
        left = int(len(x)/2)-b[0]

    return (left,right)


def crop(inputfile, outputfile, thresh=0.1):
  vid, fps, f, height, width = loadvideo(inputfile)

  u = countUniquePixelsAlongFrames(vid)
  u_avg = u/f

  maxW = np.max(u_avg, axis=0)
  left,right = findEdges(maxW, thresh=thresh)
  maxH = np.max(u_avg, axis=1)
  top,bottom = findEdges(maxH, thresh=thresh)

  cropped = vid[:,top:bottom,left:right]
  savevideo(outputfile, cropped, fps)



def applyMask(vid, mask):
    y = np.zeros_like(vid)
    f, height, width = vid.shape
    for i in range(f):
        y[i][mask] = vid[i][mask]

    return(y)






