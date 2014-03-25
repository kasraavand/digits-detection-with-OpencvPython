import cv2
import numpy as np

##read distinced digit
img1 = cv2.imread('distinc digits/4.png')#for exapmle 4.ping
hh=img1.shape[0]
ww=img1.shape[1]
#gray1 = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
#blur1 = cv2.GaussianBlur(gray1,(5,5),0)
#ret1, thresh1 = cv2.threshold(blur1, 127, 255,0)

##read main image
img2 = cv2.imread('mainpic.png')
gray2 = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
blur2 = cv2.GaussianBlur(gray2,(5,5),0)
ret, thresh2 = cv2.threshold(blur2, 127, 255,0)
contours,hierarchy = cv2.findContours(thresh2,2,1)

for cnt in contours:
 [x,y,w,h] = cv2.boundingRect(cnt)
 if (h>27 and h<35):
  tempim = img2[y:y+h,x:x+w]
  new = cv2.resize(tempim,(ww,hh))
  #new = np.float32(new)
  res = cv2.matchTemplate(img1,new,1)
  if res<0.18 :
   cv2.rectangle(img2,(x,y),(x+w,y+h),(0,0,255),2)

cv2.imshow('norm',img2)
cv2.imwrite('result.png',img2)
key = cv2.waitKey(0)

