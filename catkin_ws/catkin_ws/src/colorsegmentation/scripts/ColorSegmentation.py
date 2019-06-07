import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    cv2.imshow('HSV Frame', hsv)
    lower_bound = np.array([0,90,70])
    upper_bound = np.array([20,130,120])
    mask = cv2.inRange(hsv,lower_bound, upper_bound)
    cv2.imshow('Binary', mask)
    kernel   = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(7,7))
    eroded   = cv2.erode(mask, kernel)
    openning = cv2.dilate(eroded, kernel)
    cv2.imshow('Eroded', eroded)
    cv2.imshow('Openning', openning)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
