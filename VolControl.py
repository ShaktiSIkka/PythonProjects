import cv2
import mediapipe as mp
import time
import pyautogui as pk

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volume.GetMute()
volume.GetMasterVolumeLevel()
# print(volume.GetVolumeRange()[0])
# exit()
# volume.SetMasterVolumeLevel(-20.0, None)

cap = cv2.VideoCapture(1)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 450)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)

mpHands = mp.solutions.hands
hands = mpHands.Hands(min_detection_confidence=0.8)
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

count = 0
cxSet = []
centerPos = []
size = 0
# cySet = []

while True:
    success, img = cap.read()

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    # print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        # print(size)
        print("Hand Found")
        for handLms in results.multi_hand_landmarks:
            cxSet = []

            for id, lm in enumerate(handLms.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id, cx, cy)
                # exit()
                if id == 4 or id == 8 or id == 12 or id == 16 or id == 20:
                    cxSet.append(cx)
###################### HandPosition #######################
                if id == 13:
                    cv2.circle(img, (cx, cy), 15, (255, 255, 0), cv2.FILLED)
                    # print(cx)
                    centerPos.append(cx)

                if id == 8:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 0), cv2.FILLED)

                    # -------HEADPHONE--------RANGE (-37.0, 0.0, 1.0)----------------
                    # -------SPEAKER--------RANGE (-96.0, 0.0, 0.125)----------------
                    rng = volume.GetVolumeRange()
                    # print(range[0], range[1], type(range[0]))
                    # exit()
############################ Volume Control ##############################
                    if 470 < cx < 530 and 30 < cy < 70:
                        pk.press('volumeup')

                    elif 470 < cx < 530 and 230 < cy < 270:
                        pk.press('volumedown')

            if len(cxSet) == 5:
                count += 1
                if count == 1:
                    size = max(cxSet) - min(cxSet)
                    pSize = (size*50)/100
                    # print(size, pSize)
                # print(cxSet)
                # for i in cxSet:
                #     print(i)
                if max(cxSet) - min(cxSet) <= pSize:
                    # print("play / pause")
                    pk.press('playpause')
                    time.sleep(0.5)
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
    else:
        # print("No Hand")
        cVal = 0
        Rcount = 0
        Lcount = 0
        # print(Rcount, Lcount)
        # print(centerPos)
        for val in centerPos:
            # print(cVal, val)
            # print(val)
            if cVal < val:
                Rcount += 1
                if Rcount == 25:
                    pk.press('left')
                    print("Left")
            elif cVal > val:
                Lcount += 1
                if Lcount == 25:
                    pk.press('right')
                    print("Right")
            cVal = val


                    # pk.keyDown('Ctrl')
                    # pk.keyDown('Shift')
                    # pk.press('s')
                    # pk.keyUp('Ctrl')
                    # pk.keyUp('Shift')
        centerPos = []



    cTime = time.time()
    fps = 1 / (cTime - pTime)

    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 3)
    cv2.putText(img, f'+', (500, 50), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 0), 3)
    cv2.putText(img, f'-', (500, 250), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 0), 3)

    cv2.imshow("Img", img)
    cv2.waitKey(1)

    # https://www.youtube.com/watch?v=NZde8Xt78Iw
