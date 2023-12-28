# 
# 
# Hill-Climb-Racing-Hand-Automation System Code By Varun Chopra.
# 
# Python libraries required/used : 1.) Opencv 2.) Mediapipe 3.) PyAutoGUI
# 
# 1.) Opencv installation command: "pip install opencv-python"
# 
# 2.) Mediapippe installation command: "pip install mediapipe"
# 
# 3.) PyAutoGUI installation command: "pip install PyAutoGUI"
#
#

import cv2
import mediapipe as mp
import time
import pyautogui

cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
tipIds = [4,8,12,16,20]
pTime= 0
cTime= 0
with mpHands.Hands(min_detection_confidence=0.5,
               min_tracking_confidence=0.5) as hands:
    while True:

        success, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)
        lmList=[]

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):

                    h,w,c = img.shape
                    cx , cy = int(lm.x*w), int(lm.y*h)
                    lmList.append([id,cx,cy])
                                                          #if id ==  0:
                                                          #cv2.circle(img, (cx, cy),15,(0,0,0),cv2.FILLED)
                                                          #These two comments is the syntax to use a feature that unables
                                                          # you to mark a circle on the point...

                mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
                fingers=[]
        if len(lmList)!=0:
            if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]:
                fingers.append(1)
            else:
                   fingers.append(0)
            for id in range(1,5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            total=fingers.count(1)
            if total==0:
                 pyautogui.keyDown('right')
                 pyautogui.keyUp('left')



            elif total==5:
                 pyautogui.keyDown('left')
                 pyautogui.keyUp('right')    



        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        img = cv2.flip(img, 1)
        cv2.putText(img,str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN,3,(0, 0 ,0),2)
        cv2.imshow("Image", img)
        cv2.waitKey(1)