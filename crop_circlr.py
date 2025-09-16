import cv2 as cv
import numpy as np

points = []

def mouse_callback(event, x, y, flags, param):
    global points, img_copy
    if event == cv.EVENT_LBUTTONDOWN:
        points.append((x, y))
        cv.circle(img_copy, (x, y), 3, (0, 0, 255), -1)
        cv.imshow("Select circle", img_copy)

        # أول نقطة = المركز، تاني نقطة = على الحافة
        if len(points) == 2:
            (xc, yc), (xh, yh) = points
            r = int(((xc - xh)**2 + (yc - yh)**2)**0.5)
            print(f"Center: ({xc},{yc}), Radius: {r}")

            # نعمل ماسك ونقص الدائرة
            mask = np.zeros(img.shape[:2], dtype=np.uint8)
            cv.circle(mask, (xc, yc), r, 255, -1)
            crop = cv.bitwise_and(img, img, mask=mask)

            cv.imshow("Inner Circle Crop", crop)
# --- تشغيل ---
img = cv.imread("IMAGES/d1m.jpg")
img=cv.resize(img,(500,375))
if img is None:
    print("Error loading image"); exit()

img_copy = img.copy()
cv.imshow("Select circle", img_copy)
cv.setMouseCallback("Select circle", mouse_callback)

cv.waitKey(0)
cv.destroyAllWindows()
