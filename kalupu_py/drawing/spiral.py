def spiral(size):
    out = []
    for l in range(size):
        prev = -(l-1)
        for j in range(prev,l):
            # print(prev,j,end='\t')
            out.append((prev,j))
        for i in range(prev,l):
            # print(i,l,end='\t')
            out.append((i,l))
        for j in reversed(range(prev,l+1)):
            # print(l,j,end='\t')
            out.append((l,j))
        for i in reversed(range(prev,l+1)):
            # print(i,-l,end='\t')
            out.append((i,-l))
    return out

# 0,0

# 0,1 1,1
# 1,0 1,-1 
# 0,-1 -1,-1
# -1,0 -1,1

# -1,2 0,2 1,2
# 2,2 2,1 2