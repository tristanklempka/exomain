#!/usr/bin/env python
import cv2
import numpy as np
import processing as process 
#creating window
cv2.namedWindow('Fingers segmentation', cv2.WINDOW_NORMAL)

#Cst
FINGER_DEFECT_LENGHT = 25000

#Inputs
input_folder = "images_main/"
#read
bckground_image = cv2.imread(input_folder+"ueye_background.png")
test_image = cv2.imread(input_folder+"ueye_00238_mono.png")

hand_image = process.preprocess_image(test_image, bckground_image)
skel_image = process.skeletonize(hand_image)

hand_image_contours = hand_image.copy()
contours, hierarchy = cv2.findContours(hand_image_contours,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

#select only the largest countour
areaArray = []
for i, c in enumerate(contours):
    area = cv2.contourArea(c)
    areaArray.append(area)

#sort the array by area
sorted_countours = sorted(zip(areaArray, contours), key=lambda x: x[0], reverse=True)
contour_selected = sorted_countours[0][1] #largest countour

hull = cv2.convexHull(contour_selected)
cv2.drawContours(hand_image, contour_selected, 0, (128,128,128), 3)
cv2.drawContours(hand_image, [hull], 0, (75,75,75), 5)

hull = cv2.convexHull(contour_selected, returnPoints = False)
defects = cv2.convexityDefects(contour_selected, hull) 

#defects exists ? if so try to detect defects that can match a finger
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
            print(d) # depth printing to debug

#display result on image
cv2.putText(hand_image,"Fingers detected: " + str(fingers_detected), (100, 100), cv2.FONT_HERSHEY_PLAIN, 2, 255)

#Events loop
while(1):
#########################################################     
   cv2.imshow('test_image', test_image)
   cv2.imshow('hand_image', hand_image)
   #cv2.imshow('skel image', skel_image)
   k = cv2.waitKey(5) & 0xFF
   if k == 27:
      break
#########################################################

