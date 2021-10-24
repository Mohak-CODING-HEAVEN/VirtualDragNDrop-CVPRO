import cv2
from cvpro.HandTrackingModule import HandDetector
import cvpro
import numpy as np

cap = cv2.VideoCapture(2)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8)
colorR = (255, 0, 255)

cx, cy, w, h = 100, 100, 200, 200


class DragRect():
    def __init__(self, posCenter, size=&amp;#91;200, 200]):
        self.posCenter = posCenter
        self.size = size

    def update(self, cursor):
        cx, cy = self.posCenter
        w, h = self.size

        # If the index finger tip is in the rectangle region
        if cx - w // 2 &amp;lt; cursor&amp;#91;0] &amp;lt; cx + w // 2 and \
                cy - h // 2 &amp;lt; cursor&amp;#91;1] &amp;lt; cy + h // 2:
            self.posCenter = cursor


rectList = &amp;#91;]
for x in range(5):
    rectList.append(DragRect(&amp;#91;x * 250 + 150, 150]))

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList, _ = detector.findPosition(img)

    if lmList:

        l, _, _ = detector.findDistance(8, 12, img, draw=False)
        print(l)
        if l &amp;lt; 30:
            cursor = lmList&amp;#91;8]  # index finger tip landmark
            # call the update here
            for rect in rectList:
                rect.update(cursor)

    ## Draw solid
    # for rect in rectList:
    #     cx, cy = rect.posCenter
    #     w, h = rect.size
    #     cv2.rectangle(img, (cx - w // 2, cy - h // 2),
    #                   (cx + w // 2, cy + h // 2), colorR, cv2.FILLED)
    #     cvpro.cornerRect(img, (cx - w // 2, cy - h // 2, w, h), 20, rt=0)

    ## Draw Transperency
    imgNew = np.zeros_like(img, np.uint8)
    for rect in rectList:
        cx, cy = rect.posCenter
        w, h = rect.size
        cv2.rectangle(imgNew, (cx - w // 2, cy - h // 2),
                      (cx + w // 2, cy + h // 2), colorR, cv2.FILLED)
        cvpro.cornerRect(imgNew, (cx - w // 2, cy - h // 2, w, h), 20, rt=0)

    out = img.copy()
    alpha = 0.5
    mask = imgNew.astype(bool)
    out&amp;#91;mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)&amp;#91;mask]

    cv2.imshow("Image", out)
    cv2.waitKey(1)
