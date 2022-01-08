import numpy as np
import cv2
import spiral
# def in_limit(i,j,rows,cols):
#     return i>=0 and j>=0 and i < rows and j < cols
# class Q:
#     def __init__(self):
#         self.array = list()
#         self.front_itr = 0
#     def __len__(self):
#         return len(self.array)
#     def __str__(self):
#         return self.array[self.front_itr:].__str__()
#     def is_empty(self):
#         return len(self.array) == self.front_itr
#     def deque(self):
#         value = self.array[self.front_itr]
#         self.front_itr += 1
#         return value
#     def enque(self,value):
#         self.array.append(value)
# # q = Q()
# # q.enque(10)
# # q.enque(12)
# # print(q)
# # q.deque()
# # print(q.deque())
# # q.enque(3)
# # q.enque(90)
# # q.enque(1)
# # print(q)
# # print(q.deque())
# # print(q.deque())
# # print(q)
# visited = None
# img = cv2.imread("edge/N.png")#"edge/nithin.png" #np.zeros((512,512),np.bool)
# reimg = cv2.resize(img,(img.shape[0]//3,img.shape[1]//2))
# img = reimg
# gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

# def is_selected(value,threshold = 60):
#     return value < threshold
# visited = np.zeros(gray.shape,np.uint8) # non of the pixels is visited initially

# binary_img = np.zeros(gray.shape,np.uint8)
# for i in range(gray.shape[0]):
#     for j in range(gray.shape[1]):
#         if is_selected(gray[i][j]):
#             binary_img[i][j] = 255
# cv2.imshow("img",gray)
# cv2.imshow("binary",binary_img)
# cv2.waitKey(1)
# #cv2.imshow("img",img)
# #cv2.imshow("reimg",reimg)

# def bfs():
#     for i in range(gray.shape[0]):
#         for j in range(gray.shape[1]):
#             if binary_img[i][j] == 255 and visited[i][j] == 0: # not visited
#                 print("In",i,j)
#                 input()
#                 children = [(1,0),(0,1)] #[(1,0),(1,1),(1,-1),(0,-1),(0,1),(0,-1),(-1,-1),(1,-1)]
#                 q = Q()
#                 q.enque((i,j))
#                 while not q.is_empty():
#                     ci,cj = q.deque()
#                     visited[ci][cj] = 1
#                     for ch in children:
#                         chi, chj = ci+ch[0], cj+ch[1]
#                         if in_limit(chi,chj,visited.shape[0],visited.shape[1]):
#                             if visited[chi][chj] == 0 and binary_img[chi][chj] == 255:
#                                 binary_img[chi][chj] = 0
#                                 cv2.imshow("resized binary",binary_img)#cv2.resize(binary_img,(binary_img.shape[0]*2,binary_img.shape[1]*2))
#                                 cv2.waitKey(100)
#                                 visited[chi][chj] = 1
#                                 q.enque((chi,chj))
#                                 #print(q)
#                 print("OUT")

class ImageTraversal:
    def __init__(self,file_name=None,resize=None,waitKey_delay=None):
        self.img = cv2.imread(file_name)
        self.waitKey_delay = waitKey_delay
        if resize:
            self.img = cv2.resize(self.img,(resize[0],resize[1]))
        # reimg = cv2.resize(img,(img.shape[0]//3,img.shape[1]//2))
        # img = reimg
        self.gray = cv2.cvtColor(self.img,cv2.COLOR_BGR2GRAY)
        self.visited = np.zeros(self.gray.shape,np.uint8) # non of the pixels is visited initially
        self.binary_img = np.zeros(self.gray.shape,np.uint8)
        for i in range(self.gray.shape[0]):
            for j in range(self.gray.shape[1]):
                if self.is_selected(self.gray[i][j]):
                    self.binary_img[i][j] = 255
        cv2.waitKey(1)
    def in_limit(self,i,j):
        return i >= 0 and j >= 0 and i < self.gray.shape[0] and j < self.gray.shape[1]
    def is_selected(self,value,threshold = 60):
        return value > threshold
    def next_is_present(self,i,j,idir=1,jdir=1):
        if self.in_limit(i,j+jdir):
            return self.binary_img[i][j+jdir]
        return False
    # def up_is_present(self,i,j):
    #     if in_limit(i-1,j):
    #         return self.binary_img[i-1][j]
    #     return False
    def is_present(self,i,j):
        if self.in_limit(i,j):
            return self.binary_img[i][j]
        return False
    def clear(self,i,j):
        if self.in_limit(i,j):
            self.binary_img[i][j] = 0
    def line_by_line_comp(self,i,j,idir=1,jdir=1,lift_threshold=10): 
        # terms used assuming default setting i.e left_right, top_bottom
        print("Component")
        cv2.waitKey(300)
        polyline = []
        points_down = []
        next = (i,j+jdir)
        while True:
            if self.waitKey_delay:
                cv2.imshow("Traversal",self.binary_img)
                cv2.waitKey(self.waitKey_delay)
            points_up = []
            polyline.append((i,j))
            self.clear(i,j)
            while self.is_present(*next):
                self.clear(*next)
                up = (i-idir,j)
                if self.is_present(*up): # up
                    if self.is_present(i-idir,j-jdir): # previous to up
                        if len(points_up) > 0:
                            points_up[-1] = up # reset previous to up with up
                        else:
                            points_up.append(up)
                    else:
                        points_up.append(up)
                down = (i+idir,j)
                if self.is_present(*down): # down
                    print("pdown")
                    if self.is_present(i+idir,j-jdir): # previous to down
                        if len(points_down) > 0:
                            points_down[-1] = down
                        else:
                            points_down.append(down)
                    else:
                        points_down.append(down)
                next = (i,j+jdir)
            # for up_point in points_up:
            #     self.line_by_line_comp(*up_point,-1*idir,-1*jdir)
            # print(points_down)
            if len(points_down)>0:
                next = points_down[-1]
                print("Down",next)
                points_down = points_down[:-1]
                jdir *= -1
            else:
                # for p in spiral.spiral(10):
                #     pi, pj = p[0]+i, p[1]+j
                #     if self.is_present(pi,pj):
                #         self.line_by_line_comp(pi,pj)
                #         break
                break

            
# def not_cleared_and_not_visited(i,j):
#     return binary_img[i][j] == 255 and visited[i][j] == 0

    def line_by_line(self):
        # to do better than 2 approx tsp
        for i in range(self.gray.shape[0]):
            for j in range(self.gray.shape[1]):
                # if not_cleared_and_not_visited(i,j):
                #     print("In",i,j)
                #     input()
                #     print(i,j)
                #     next_i, next_j = i,j+1
                #     while :#not_cleared_and_not_visited(next_i,next_j)
                
                if self.is_present(i,j):
                    self.line_by_line_comp(i,j)
                    #print(i,j)
                    #input()
                    # children = [(1,0),(0,1)] #[(1,0),(1,1),(1,-1),(0,-1),(0,1),(0,-1),(-1,-1),(1,-1)]
                    # q = Q()
                    # q.enque((i,j))
                    # while not q.is_empty():
                    #     ci,cj = q.deque()
                    #     visited[ci][cj] = 1
                    #     for ch in children:
                    #         chi, chj = ci+ch[0], cj+ch[1]
                    #         if in_limit(chi,chj,visited.shape[0],visited.shape[1]):
                    #             if visited[chi][chj] == 0 and binary_img[chi][chj] == 255:
                    #                 binary_img[chi][chj] = 0
                    #                 cv2.imshow("resized binary",binary_img)#cv2.resize(binary_img,(binary_img.shape[0]*2,binary_img.shape[1]*2))
                    #                 cv2.waitKey(100)
                    #                 visited[chi][chj] = 1
                    #                 q.enque((chi,chj))
                    #                 print(q)
                    # print("OUT")
#bfs()
i = ImageTraversal("white50x50.jpg",waitKey_delay=200)#"edge/N.png"
i.line_by_line()

# h,w = 50,40
# img = np.zeros((h*10,w*10),np.uint8)
# l = []
# for i in range(h):
#     for j in range(w):
#         l.append((i,j))
# for p in spiral.spiral(25):
#     pi, pj = p[0]+25, p[1]+20
#     if pi >= 0 and pi < w and pj >= 0 and pj < h:
#         cv2.rectangle(img,(pj*10,pi*10),((pj+1)*10,(pi+1)*10),(255,255,255),cv2.FILLED)
#         cv2.imshow("a",img)
#         cv2.waitKey(10)
#     else:
#         print(pi,pj)
cv2.waitKey(0)
#-----------------------------------------
# w, h = 50,50
# binary_img = np.zeros((h,w),np.uint8)
# gray = binary_img
# for i in range(h):
#     for j in range(w):#(0,w,3):
#         for k in range(1):
#             binary_img[i][j+k] = 255
# cv2.imshow("a",binary_img)
# cv2.imwrite("",binary_img)
# input()
#------------------------------------------
