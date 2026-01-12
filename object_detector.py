
import cv2

# seting up the web cam
cam = cv2.VideoCapture(0)

while True:
    ret, frame = cam.read()
    if not ret: break

    frame = cv2.flip(frame, 1)

    # conversion to HSV from BGR
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # range for red color
    mask1 = cv2.inRange(hsv, (0, 150, 100), (10, 255, 255))
    mask2 = cv2.inRange(hsv, (170, 150, 100), (180, 255, 255))

    mask = cv2.bitwise_or(mask1, mask2)

    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # finding contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # filtering the largest contour
    if len(contours) > 0:
        largest = max(contours, key = cv2.contourArea)
        box = cv2.boundingRect(largest)
        
        cv2.rectangle(frame, box, [255, 0, 0], 2)
        cv2.drawContours(frame, [largest], -1, [0, 0, 255], 1)

    # live tracking
    cv2.imshow("live", frame)
    if cv2.waitKey(1) & 0xff == ord('q'): break

cam.release()
cv2.destroyAllWindows()