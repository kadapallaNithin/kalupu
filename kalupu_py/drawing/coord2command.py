import cv2
import numpy as np

def split_coord(coord):
    coord = coord.split(' ')
    return int(coord[0]),int(coord[1])

def coord2command(img = np.zeros((512,512,3),np.uint8),
    file_name = "amma_a.txt",
    prev_pt = (0,0),
    plot_scale = [1,1],
    transparent = (0,255,0),
    ink = (255,0,0)
    ):
    px, py = prev_pt
    coords = open(file_name).read().splitlines()
    color = transparent
    command = ""
    for coord in coords:
        if coord[0] == "s":
            # color = transparent
            x,y = split_coord(coord[2:])
            # print("p 180")
        elif coord[0] == 'e':
            x,y = split_coord(coord[2:])
            # color = ink
            # print("p 160")
        else:
            # color = ink
            x,y = split_coord(coord)
        
        if px - x != 0 or py - y != 0:
            cv2.line(img,(px,py),(x,y),color)
            command += f"d {(px-x)*plot_scale[0]} {(py - y)*plot_scale[1]}\n"
        if coord[0] == 's':
            color = ink
            command += "p 180\n"
        elif coord[0] == 'e':
            color = transparent
            command += "p 160\n"
        
        # if draw:
        #     cv2.line(img,(px,py),(x,y),(255,0,0))
        # else:
        #     cv2.line(img,(px,py),(x,y),(0,0,0))
        cv2.imshow("img",img)
        cv2.waitKey(3)
        px,py = x,y
    x = input()
    if x == 'p':
        print(command)
    cv2.destroyWindow("img")

def coord2bytes(contours,save_dir):
    contour_index = 0
    for cnt in contours:
        contour_bytes = bytes(0)
        for i in cnt:
            contour_bytes += int(i[0][0]).to_bytes(2,'big') + int(512 - i[0][1]).to_bytes(2,'big')
        with open(save_dir+str(contour_index),'wb') as f:
            f.write(contour_bytes)
        contour_index += 1


#coord2command(plot_scale=[20,20])