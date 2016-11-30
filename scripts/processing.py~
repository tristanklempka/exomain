#!/usr/bin/env python
import cv2
import numpy as np

def remove_background(image, bckground_image):
    #rgb to hsv
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    bckground_image_hsv = cv2.cvtColor(bckground_image, cv2.COLOR_BGR2HSV)
    #split
    image_h = cv2.split(image_hsv)[0]
    bckground_image_h = cv2.split(bckground_image_hsv)[0]
    #diff of hue channel
    hand_image_diff_h = cv2.absdiff(image_h, bckground_image_h)
    #otsu threshold
    hand_image_diff_thresh = cv2.threshold(hand_image_diff_h,0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    bckground_image_thresh = cv2.threshold(bckground_image_h,0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    #dilate
    hand_image_diff_thresh_dilated = cv2.dilate(hand_image_diff_thresh, np.ones((3,3),np.uint8), iterations = 12)
    bckground_image_thresh_dilated = cv2.dilate(bckground_image_thresh, np.ones((3,3),np.uint8), iterations = 12)
    #bitwise op to remove background
    hand_withoutbackground_thresh = hand_image_diff_thresh_dilated - bckground_image_thresh_dilated
    #erode to filter some noise
    hand_withoutbackground_thresh_erode = cv2.erode(hand_withoutbackground_thresh, np.ones((3,3),np.uint8), iterations = 2)

    return hand_withoutbackground_thresh_erode

def skeletonize(image):
    #blog post http://felix.abecassis.me/2011/09/opencv-morphological-skeleton/

    skel = np.zeros(image.shape,np.uint8)
    element = cv2.getStructuringElement(cv2.MORPH_CROSS,(7,7))
    size = np.size(image)
    done = False
 
    while( not done):
        eroded = cv2.erode(image,element)
        temp = cv2.dilate(eroded,element)
        temp = cv2.subtract(image,temp)
        skel = cv2.bitwise_or(skel,temp)
        image = eroded.copy()
 
        zeros = size - cv2.countNonZero(image)
        if zeros==size:
            done = True

    return skel

def get_largest_contour(image):
	contours, hierarchy = cv2.findContours(image,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	#select only the largest countour
	areaArray = []
	for i, c in enumerate(contours):
    area = cv2.contourArea(c)
    areaArray.append(area)

	#sort the array by area
	sorted_countours = sorted(zip(areaArray, contours), key=lambda x: x[0], reverse=True)

	return sorted_countours[0][1] #largest countour

def detect_fingers(defects):
	FINGER_DEFECT_LENGHT = 25000
	fingers_detected = 0
	if defects.any() : 
		  for i in range(defects.shape[0]):
		      s,e,f,d = defects[i,0]
		      start = tuple(contour_selected[s][0])
		      end = tuple(contour_selected[e][0])
		      far = tuple(contour_selected[f][0])
		      if d > FINGER_DEFECT_LENGHT :
		          cv2.line(hand_image,end,far,[128,128,128],2)
		          cv2.circle(hand_image,far,5,[128,128,128],-1)
		          fingers_detected += 1
	
	return fingers_detected
		    










