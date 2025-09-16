# Import OpenCV for image processing, Pandas for data storage/export, and NumPy as the background support for array operations
import cv2 as cv
import numpy as np
import pandas as pd

# Reference and target image paths with circle center coordinates and radius
REF_IMAGE_PATH = "IMAGES/d (1).jpg"
TGT_IMAGE_PATH = "IMAGES/d (1).jpg"
xc_ref, yc_ref, r_ref = 300, 166, 33
xc_backup, yc_backup, r_backup = 301, 166, 33
# Find good ORB feature matches between reference and target images
def get_orb_matches(img_ref, img_tgt, nfeatures=2000):
    orb = cv.ORB_create(nfeatures=nfeatures)
    kp1, des1 = orb.detectAndCompute(img_ref, None)
    kp2, des2 = orb.detectAndCompute(img_tgt, None)
    if des1 is None or des2 is None:
        return [], [], None, None
    bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=False)
    matches = bf.knnMatch(des1, des2, k=2)
    good = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good.append(m)
    return kp1, kp2, good, orb

# Compute homography matrix from matched keypoints using RANSAC
def compute_homography_from_matches(kp1, kp2, good, min_good=20):
    if good is None or len(good) < min_good:
        return None
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1,1,2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1,1,2)
    H, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC, 3.0)
    return H

# Apply homography matrix H to transform a list of (x,y) points
def transform_points(H, pts_xy):
    pts = np.float32([[x,y,1.0] for (x,y) in pts_xy]).T
    Hp = H @ pts
    Hp /= Hp[2,:]
    out = np.vstack([Hp[0,:], Hp[1,:]]).T
    return [tuple(p) for p in out]

# Estimate new circle center and radius after applying homography
def estimate_transformed_circle(H, xc, yc, r):
    center_ref = (xc, yc)
    A = (xc - r, yc); B = (xc + r, yc)
    C = (xc, yc - r); D = (xc, yc + r)
    xyc = transform_points(H, [center_ref, A, B, C, D])
    center_new = xyc[0]
    A2, B2, C2, D2 = xyc[1], xyc[2], xyc[3], xyc[4]
    d_h = np.hypot(B2[0]-A2[0], B2[1]-A2[1])
    d_v = np.hypot(D2[0]-C2[0], D2[1]-C2[1])
    r_new = 0.25*(d_h + d_v)
    return center_new[0], center_new[1], r_new

#Load reference/target images and Excel data, check errors, resize images
ref = cv.imread(REF_IMAGE_PATH)
img = cv.imread(TGT_IMAGE_PATH)
df = pd.read_excel("dryers.xlsx")
if ref is None or img is None:
    print("Error loading reference or target image")
    exit()
ref = cv.resize(ref, (500,375))
img = cv.resize(img, (500,375))

# Match ORB features and compute homography between reference and target
kp1, kp2, good, _ = get_orb_matches(ref, img, nfeatures=2000)
H = compute_homography_from_matches(kp1, kp2, good, min_good=20)

# If homography is valid, estimate new circle; otherwise use backup values
if H is not None:
    xc_new, yc_new, r_new = estimate_transformed_circle(H, xc_ref, yc_ref, r_ref)
    h_img, w_img = img.shape[:2]
    if 0 <= xc_new < w_img and 0 <= yc_new < h_img and r_new > 3:
        xc, yc, r = int(round(xc_new)), int(round(yc_new)), int(round(r_new))
    else:
        xc, yc, r = xc_backup, yc_backup, r_backup
else:
    xc, yc, r = xc_backup, yc_backup, r_backup

# Isolate circular region, enhance contrast, binarize, and detect contours
mask = np.zeros(img.shape[:2], dtype=np.uint8)
cv.circle(mask, (xc, yc), r, 255, -1)
crop = cv.bitwise_and(img, img, mask=mask)
gray = cv.cvtColor(crop, cv.COLOR_BGR2GRAY)
gray = cv.GaussianBlur(gray, (5,5), 0)
clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
gray= clahe.apply(gray)
_, threshold = cv.threshold(gray, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
contours, hier = cv.findContours(threshold, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

# Detect outer/inner contours, measure diameters, and draw them with labels


if hier is None or len(contours) == 0:
    print("no contours"); exit()
hier = hier[0]
h, w = threshold.shape
img_area = h * w
outer_idx = -1
outer_area_max = 0
for i, cnt in enumerate(contours):
    a = cv.contourArea(cnt)
    if a > outer_area_max and a > 0.002 * img_area:
        outer_area_max = a
        outer_idx = i
if outer_idx == -1:
    print("no outer found"); exit()

inner_idx = hier[outer_idx][2]
(xo, yo), ro = cv.minEnclosingCircle(contours[outer_idx])
do = 2 * ro
print(f"Outer diameter: {do:.1f}px")

if inner_idx != -1:
    (xi, yi), ri = cv.minEnclosingCircle(contours[inner_idx])
    di = 2 * ri
    print(f"Inner diameter: {di:.1f}px")
else:
    (xi, yi), ri, di = (xo, yo), 0, 0

cv.circle(img, (int(xo), int(yo)), int(ro), (0,255,0), 2)
cv.putText(img, f"out:{do:.0f}", (int(xo)-20, int(yo)), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)

if di > 0:
    cv.circle(img, (int(xi), int(yi)), int(ri), (0,255,0), 2)
    cv.putText(img, f"in:{di:.0f}", (int(xi)-20, int(yi)+15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)


# Save measured dryer diameters (OD/ID) into Excel
dryer_name = "DRYER"
OD = float(do)
ID = float(di)

df = pd.concat([df, pd.DataFrame([{"Dryer": dryer_name, "OD": OD, "ID": ID}])],
               ignore_index=True)
df.to_excel("dryers.xlsx", index=False)
cv.imshow("orignal", img)
cv.imshow("result_after crop",crop)
cv.waitKey(0)
cv.destroyAllWindows()

