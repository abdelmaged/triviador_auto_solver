import cv2
import os
# 
for fname in os.listdir("./fix"):
	for i in range(1000):
	 
		image = cv2.imread("./fix/" + fname)

		gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) # grayscale
		# _, thresh = cv2.threshold(gray,150,255,cv2.THRESH_BINARY_INV) # threshold
		thresh = gray
		kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
		dilated = cv2.dilate(thresh,kernel,iterations = 13) # dilate
		contours, hierarchy = cv2.findContours(dilated,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) # get contours

		# for each contour found, draw a rectangle around it on original image
		a,b, c,d, q = 0,0,0,1000, 0
		for contour in contours:
			# get rectangle bounding contour
			[x,y,w,h] = cv2.boundingRect(contour)

			# discard areas that are too small
			if h<40 or w<40:
				continue

			if(h < d):
				a,b,c,d = x+q,y+q,w-q,h-q

		# write original image with added contours to disk
		# cv2.imshow(image)
		print a,b,c,d, fname
		if(d != 1000):
			cv2.imwrite('./fix/' + fname, thresh[b:b+d, a:a+c])
		else:
			break