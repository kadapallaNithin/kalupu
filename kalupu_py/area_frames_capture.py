import cv2
import numpy as np
import requests
import time
import os
def capture_area(souce=0,dir_name = "area/1/",rows=4,cols=4,size=(500,500)):
    cap = cv2.VideoCapture(souce)
    for i in range(rows):
        for j in range(cols):
            if i%2 == 1:
                js = cols - j - 1
            else:
                js = j
            print(i*size[0],js*size[1])
            requests.post("http://192.168.43.80/pass_commands/",{"commands":f"m {i*size[0]} {js*size[1]} "})
            time.sleep(3)
            succ, img = cap.read()
            file_name = f"{i}-{js}.jpg"
            print(file_name)
            cv2.imwrite(dir_name+file_name,img)
def show_stacked(dir_name,rows=6,cols=5,save=False,show=True):
    img = cv2.imread(dir_name+"0-0.jpg")
    res = img.shape
    rotate = True
    if rotate:
        stacked = np.zeros((rows*res[1],cols*res[0],3),np.uint8)
    else:
        stacked = np.zeros((rows*res[0],cols*res[1],3),np.uint8)
        
    for i in range(rows):
        for j in range(cols):
            # if i%2 == 0:
            #     js = cols - j
            #     js1 = js - 1
            # else:
            #     js = j
            #     js1 = j - 1
            file_name = f"{i}-{j}.jpg"
            img = cv2.imread(dir_name+file_name)
            if not os.path.exists(dir_name+file_name):
                print("haa",end=' ')
            else:
                try:
                    if rotate:
                        img = cv2.rotate(img, cv2.cv2.ROTATE_90_CLOCKWISE)
                        stacked[i*res[1]:(i+1)*res[1],j*res[0]:(j+1)*res[0]] = img
                    else:
                        stacked[i*res[0]:(i+1)*res[0],j*res[1]:(j+1)*res[1]] = img
                # for pi in range(res[0]):
                #     for pj in range(res[1]):
                #         stacked[i*res[0]+pi][js*res[1]+pj] = img[pi][pj]
                except ValueError:
                    print("value error for ",file_name)
    if save:
        cv2.imwrite(dir_name+"stacked.jpg",stacked)
    if show:
        cv2.imshow("stacked",cv2.resize(stacked,(res[0],res[1])))
        cv2.waitKey(0)
def show_stiched(dir_name,rows=6,cols=5,save=False,show=True):
    img = cv2.imread(dir_name+"0-0.jpg")
    res = img.shape
    rotate = True
    if rotate:
        stacked = np.zeros((rows*res[1],cols*res[0],3),np.uint8)
    else:
        stacked = np.zeros((rows*res[0],cols*res[1],3),np.uint8)
    img1 = cv2.imread(dir_name+"0-1.jpg")
        
    # for i in range(rows):
    #     for j in range(cols):
    #         # if i%2 == 0:
    #         #     js = cols - j
    #         #     js1 = js - 1
    #         # else:
    #         #     js = j
    #         #     js1 = j - 1
    #         file_name = f"{i}-{j}.jpg"
    #         img = cv2.imread(dir_name+file_name)
    #         if not os.path.exists(dir_name+file_name):
    #             print("haa",end=' ')
    #         else:
    #             # try:
    #             #     if rotate:
    #             #         img = cv2.rotate(img, cv2.cv2.ROTATE_90_CLOCKWISE)
    #             #         stacked[i*res[1]:(i+1)*res[1],j*res[0]:(j+1)*res[0]] = img
    #             #     else:
    #             #         stacked[i*res[0]:(i+1)*res[0],j*res[1]:(j+1)*res[1]] = img
    #             # # for pi in range(res[0]):
    #             # #     for pj in range(res[1]):
    #             # #         stacked[i*res[0]+pi][js*res[1]+pj] = img[pi][pj]
    #             # except ValueError:
    #             #     print("value error for ",file_name)
    if save:
        cv2.imwrite(dir_name+"stacked.jpg",stacked)
    if show:
        cv2.imshow("stacked",cv2.resize(stacked,(res[0],res[1])))
        cv2.waitKey(0)

#capture_area(rows=4,cols=4,size=(500,500))
show_stacked("area/1/",rows=5,cols=5)
#show_stacked("area/1/",rows=2,cols=2)
#show_stiched("area/0/")