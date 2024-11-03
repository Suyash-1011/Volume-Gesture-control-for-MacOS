import os
import cv2 
import time 
import mediapipe
import numpy as np 
import hand_tracking_module as htm
import math 

#wCam, hCam=640, 480

cap=cv2.VideoCapture(1)
#cap.set(3,wCam)
#cap.set(4,hCam)
pTime=0
vol=0
detector=htm.handDetector(detectionCon=0.7)

while(True):
    success, img=cap.read()
    img=detector.findHands(img)
    
    lmlist=detector.findPosition(img,draw=False)
    if len(lmlist)!=0:
        x1,y1=lmlist[4][1],lmlist[4][2]
        x2,y2=lmlist[8][1],lmlist[8][2]
        length=math.hypot(x2-x1,y2-y1)
        

        temp_vol=np.interp(length, [19, 220], [0, 100])
        if abs(vol - temp_vol) > 5:  # Adjust the threshold as needed
            vol = temp_vol
            os.system(f"osascript -e 'set volume output volume {vol}'")
        cv2.circle(img,(x1,y1),10,(200,0,200),cv2.FILLED)
        cv2.circle(img,(x2,y2),10,(200,0,200),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)

       

    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime

    cv2.putText(img,f"FPS:{int(fps)}", (40,40),cv2.FONT_HERSHEY_PLAIN,2,(200,150,0),1)

    cv2.imshow("Img", img)
    if cv2.waitKey(1)  &0xFF == ord('q'):
        break
    
cap.release()

cv2.destroyAllWindowsq