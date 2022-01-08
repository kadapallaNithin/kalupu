import cv2
from imutils import paths
import imutils
image_paths = list(paths.list_images("groundnut/gr/"))
#print(len(image_paths))
images = list()
for img in image_paths:
    images.append(cv2.imread(img))
sticher = cv2.createSticher() if imutils.is_cv3() else cv2.Stitcher_create()
(status, stiched) = sticher.stitch(images)

if status == 0:
    cv2.imshow("Stiched",stiched)
    cv2.waitKey(0)
    write = input("Store Image? y/n")
    if write == 'y':
        cv2.imwrite("Stiched.jpg",stiched)
        print("saved")
    else:
        print("not saved")
else:
    print(status)
