import cv2
import numpy as np
import HandTrackingModule as htm
import autopy
import time

wCam=640
hCam=480
pTime=0
frameR=100
smoothening=7
pTime=0
plocX, plocY=0,0
clocX, clocY=0,0
#General approch- 1) Find hand landmarks 2)Get the tip of index and middle finger 3)Check which fingers are up
#4) Only index finger: Moving mode 5)Convert coordinates 6)Smoothen values 7)Move Mouse
#8)Both middle and index fingers up--->clicking mode  9)Find distance between fingers
#10) Click mouse if distance is short 11)FPS

cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
detector=htm.handDetector(maxHands=1)
wSrc,hSrc = autopy.screen.size()
while True:
    #1)
    success, img=cap.read()
    img=detector.findHands(img)
    lmList, bbox = detector.findPosition(img)  #bbox-->Boundary box

    #2)
    if len(lmList)!=0:
        x1,y1=lmList[8][1:]
        x2,y2=lmList[12][1:]
        #print(x1,y1,x2,y2)
        #3)
        fingers=detector.fingersUp()
        print(fingers)
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)
        #4
        if fingers[1]==1 and fingers[2]==0:

            x3=np.interp(x1,(frameR,wCam-frameR),(0,wSrc)) #Bounding the cursor to the screen using frameR
            y3=np.interp(y1,(frameR,hCam-frameR),(0,hSrc))
            clocX=plocX+(x3-plocX)/smoothening
            clocY=plocY+(y3-plocY)/smoothening
            autopy.mouse.move(wSrc-x3,hSrc-y3)

            cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
            plocX,plocY = clocX,clocY

        if fingers[1]==1 and fingers[2]==1:
            length,img,lineInfo = detector.findDistance(8,12,img)
            print(length)     #40 is threshold
            if length<40:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)

                autopy.mouse.click()  #10th move




    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 4)
    cv2.imshow("Image",img)
    if cv2.waitKey(1) & 0xff==ord("a"):
        break

