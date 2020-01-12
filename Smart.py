# Created by Shikher Pant
# https://github.com/shikherpant

import cv2
import numpy as np
import math
import os

# function for counting fingers
def countFingers(cnt):

    hull1 = cv2.convexHull(cnt, returnPoints=False)
    defects = cv2.convexityDefects(cnt, hull1)
    try:
        num = 0
        for i in range(defects.shape[0]):
            s, e, f, d = defects[i, 0]
            start = tuple(cnt[s][0])
            end = tuple(cnt[e][0])
            far = tuple(cnt[f][0])

            a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
            b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
            c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)

            angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))

            if angle <= math.pi / 2:
                num = num + 1
    except AttributeError:
        print("Unable to detect hand")
        num=False
    return(num)


# function for difference between 1 finger and no finger
def forMute(cnt):

    hull1 = cv2.convexHull(cnt, returnPoints=False)
    defects = cv2.convexityDefects(cnt, hull1)
    try:
        num2=0
        for i in range(defects.shape[0]):
            s, e, f, d = defects[i, 0]
            start = tuple(cnt[s][0])
            end = tuple(cnt[e][0])
            far = tuple(cnt[f][0])

            a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
            b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
            c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)

            angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))

            if angle <= 2*(math.pi) / 3:
                num2 = num2 + 1
    except AttributeError:
        print("Unable to detect hand")
        num2=False
    return(num2)


# capture video from webcam
cap = cv2.VideoCapture(0)

# change width of cap
cap.set(3, 640)
# change height of cap
cap.set(4, 480)


while 1:
    # ret stores boolean value and frame store the img from video
    ret, frame = cap.read()
    if ret == True:
        # show the frame in window "original"
        cv2.imshow("Original", frame)

        # convert color from bgr to gray
        grayframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # to reduce noise from frame
        blur = cv2.medianBlur(grayframe, 5)

        # thresholding
        _, th = cv2.threshold(blur, 90, 255, cv2.THRESH_BINARY_INV)
        cv2.imshow("Thresholding", th)

        # to find boundries(edges) in frame
        contours, hiearchy = cv2.findContours(th, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        # to find and draw the boundries of largest contour
        maxarea=0
        i=0
        for x in range(len(contours)):
            area=cv2.contourArea(contours[x])
            if area>maxarea:
                maxarea=area
                i=x

        # using try/except to remove index error when the frame is empty
        try:
            lar_contour=contours[i]
            cnt=[]
            cnt.append(lar_contour)

            # create a new black image
            img=np.zeros((480,640,3),np.uint8)

            cv2.drawContours(img, cnt, -1, (0, 255, 0), 2)
            # cv2.imshow("Contours",img)

            # to draw convexhull
            for m in cnt:
                hull = cv2.convexHull(m)
                cv2.drawContours(img, [hull], -1, (0, 0, 255), 2)
                #cv2.imshow("Contour & ConvexHull", img)

            cnt.clear()

            # function call to count fingers
            num=countFingers(lar_contour)
            if num != False:
                print(num+1)

            # function call to check for mute
            if num+1==1:
                num2=forMute(lar_contour)
                print("num2 : "+str(num2))

            # to change volume in macos
            if (num+1)>=5:
                os.system('osascript -e "set Volume 10"')
                cv2.putText(img, "Volume is set to 100 %", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

            elif (num+1)==4:
                os.system('osascript -e "set Volume 8"')
                cv2.putText(img, "Volume is set to 80 %", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

            elif (num+1)==3:
                os.system('osascript -e "set Volume 6"')
                cv2.putText(img, "Volume is set to 60 %", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

            elif (num+1)==2:
                os.system('osascript -e "set Volume 4"')
                cv2.putText(img, "Volume is set to 40 %", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

            elif (num+1)==1 and num2!=0:
                os.system('osascript -e "set Volume 2"')
                cv2.putText(img, "Volume is set to 20 %", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

            elif (num+1)==1 and num2==0:
                os.system('osascript -e "set Volume 0"')
                cv2.putText(img, "Volume is set to 0 %", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

            cv2.imshow("Contour & ConvexHull", img)

            # video stops on pressing "q"
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        except IndexError:
            print("Unable to detect hand")

    else:
        break

# to release memory of cap
cap.release()
# to destroy all windows
cv2.destroyAllWindows()
