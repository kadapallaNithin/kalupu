incomplete
# import cv2
# import os
# img_dir = "../drawing/edge/"
# img_name = "drawing_nithin.jpg"
# down_z, up_z = -2, 3
# img = cv2.imread(os.path.join(img_dir,img_name))
# if type(img) == "None":
#     print("Could not read img")
# else:
#     img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#     contours, hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
#     # gcode_dir = os.path.join(img_dir,img_name[:-4]+"_gcode")
#     gcode_file_name = os.path.join(img_dir,img_name[:-4]+".gcode")
#     # os.mkdir(gcode_dir)
#     # os.system(f"cp {os.path.join(img_dir,img_name)} {gcode_dir}")
#     contour_index = 0
#     print(img.shape)
#     print(len(contours))
#     gcode = f"( img.shape : {img.shape}, Number of contours : {len(contours)})\n"
#     for cnt in contours:
#         # points = bytes(0)
#         gcode += f"(contour : {contour_index})\ng0 z{down_z}"
#         prev_point = [-1,-1]
#         for i in cnt:
#             if prev_point[0] != i[0][0] and prev_point[1] != i[0][1]:
#                 points += int(i[0][0]).to_bytes(2,'big')+int(i[0][1]).to_bytes(2,'big')
#             prev_point = i[0]
#         # with open(os.path.join(gcode_dir,str(contour_index)),'wb') as f:
#         #     f.write(points)
#         # contour_index += 1
