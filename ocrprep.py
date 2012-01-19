#!/usr/bin/python

'''
Created on Jan 10, 2012

@author: jsnavely
'''

import cv
import sys
from math import sin, cos, sqrt, pi, degrees
from  numpy import median

def findLines(src):
    dst = cv.CreateImage(cv.GetSize(src), 8, 1)
    color_dst = cv.CreateImage(cv.GetSize(src), 8, 3)
    storage = cv.CreateMemStorage(0)
    lines = 0
    cv.Canny(src, dst, 50, 200, 3)
    cv.CvtColor(dst, color_dst, cv.CV_GRAY2BGR)
    lines = cv.HoughLines2(dst, storage, cv.CV_HOUGH_STANDARD, 1, pi / 180, 100, 0, 0)
    return lines

def snd((a,b)):
    return b

def avgAngle(lines):
    angles = [(snd (a)) for a in lines[:10] ]
    return median(angles)
    
def drawLines(lines,img):
    for (rho, theta) in lines[:5]:
        print "line: ", rho, theta, "\n"
        a = cos(theta)
        b = sin(theta)
        x0 = a * rho
        y0 = b * rho
        pt1 = (cv.Round(x0 + 1000*(-b)), cv.Round(y0 + 1000*(a)))
        pt2 = (cv.Round(x0 - 1000*(-b)), cv.Round(y0 - 1000*(a)))
        cv.Line(img, pt1, pt2, cv.RGB(255, 0, 0), 3, 8)

def rotate(img, angle):
    center = (img.width/2.0, img.height/2.0)
    rot_mat = cv.CreateMat(2, 3, cv.CV_32FC1)
    cv.GetRotationMatrix2D(center, angle, 1.0,rot_mat)
    dst = cv.CreateImage( cv.GetSize(img), cv.IPL_DEPTH_8U, 1)
    cv.WarpAffine(img, dst, rot_mat, fillval=255)
    return dst

def threshhold(img):
    bwsrc = cv.CreateImage( cv.GetSize(img), cv.IPL_DEPTH_8U, 1)
    bwdst = cv.CreateImage( cv.GetSize(img), cv.IPL_DEPTH_8U, 1)

    cv.CvtColor(img, bwsrc, cv.CV_BGR2GRAY)
    cv.AdaptiveThreshold(bwsrc, bwdst, 255.0, cv.CV_THRESH_BINARY, cv.CV_ADAPTIVE_THRESH_MEAN_C,11)
    cv.Smooth(bwdst, bwdst, cv.CV_MEDIAN, 1, 1)
    cv.Dilate(bwdst,bwdst)
    cv.Erode(bwdst,bwdst)
    return bwdst

def wait():
    while True:
        k = cv.WaitKey(0) % 0x100
        if k == 27:
            break

fname =  sys.argv[1]
img = cv.LoadImage(fname)
thresh = threshhold(img)

lines = findLines(thresh)
ang = degrees ( avgAngle(lines) ) - 90.0
fix_rotation= rotate(thresh, ang )

#we need to convert back to greyscale because ocrfeeder doesn't expect a plain B&W image
cv.ShowImage("rotation fixed", fix_rotation)
color_dst = cv.CreateImage(cv.GetSize(fix_rotation), 8, 3)
cv.CvtColor(fix_rotation, color_dst, cv.CV_GRAY2BGR)

cv.SaveImage("skew_fix.jpg",color_dst)
wait()
