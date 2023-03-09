import numpy as np
import time
import cv2

# input video untuk menyalakan kamera
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

# ambil input dari kamera
cap = cv2.VideoCapture(0)

time.sleep(3)
count = 0
background = 0

# menerima input gambar background
for i in range(60):
    ret, background = cap.read()
background = np.flip(background, axis=1)

# aktivasi "green screen"
while (cap.isOpened()):
    ret, img = cap.read()
    if not ret:
        break
    count += 1
    img = np.flip(img, axis=1)

    # BGR ke HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # # warna merah menjadi invisible
    # lower_color = np.array([0, 120, 50])
    # upper_color = np.array([10, 255,255])
    # mask1 = cv2.inRange(hsv, lower_red, upper_red)

    # lower_color = np.array([170, 120, 70])
    # upper_color = np.array([180, 255, 255])

    # warna kulit menjadi invisible
    lower_color = np.array([0, 0, 70])
    upper_color = np.array([100, 255,255])
    mask1 = cv2.inRange(hsv, lower_color, upper_color)

    lower_color = np.array([170, 120, 70])
    upper_color = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_color, upper_color)

    mask1 = mask1 + mask2

    # membuka dan memperbesar image
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8))

    # membuat mask invert
    mask2 = cv2.bitwise_not(mask1)

    # menggunakan bitwise untuk mengeluarkan warna
    res1 = cv2.bitwise_and(img, img, mask = mask2)

    # membuat background static
    res2 = cv2.bitwise_and(background, background, mask = mask1)

    # output
    hasil = cv2.addWeighted(res1, 1, res2, 1, 0)
    out.write(hasil)
    cv2.imshow("Hasil", hasil)
    cv2.waitKey(1)

cap.release()
out.release()
cv2.destroyAllWindows()