import os, sys
from PIL import Image, ImageDraw

argv = sys.argv
if len(argv) != 3:
    print("usage: %s [left_img] [right_img]", argv[0])
left = argv[1]
right = argv[2]

im = Image.open(left)
cmp_im = Image.open(right)

resolution_ratio = 1
print "checking resolution ratio %d" % resolution_ratio
pixel_delta_range = 10
print "checking pixel delta range %d" % pixel_delta_range
limit = 1000

palette = im.getpalette()

def print_slice():
    print("===================================")

def right_bound(im):
    print "checking right bound"
    (weight, height) = im.size
    pix = im.load()
    for i in range(weight - 1, -1, -1):
        flag = False
        for j in range(height):
            if pix[i,j] != 0 and pix[i,j]!=1:
                flag = True
#                print "get at %d %d ,color %d" % (i,j,pix[i,j])
                break
        if flag:
            return i
    print("nothing detected for left bound")
    sys.exit(0)

def low_bound(im):
    print "checking low bound"
    (weight, height) = im.size
    pix = im.load()
    for j in range(height - 1,  -1, -1):
        flag = False
        for i in range(weight):
            if pix[i,j] != 0 and pix[i,j]!=1:
                flag = True
#                print "get at %d %d ,color %d" % (i,j,pix[i,j])
                break
        if flag:
            return j
    print("nothing detected for up bound")
    sys.exit(0)

def left_bound(im):
    print "checking left bound"
    (weight, height) = im.size
    pix = im.load()
    for i in range(weight):
        flag = False
        for j in range(height):
            if pix[i,j] != 0 and pix[i,j]!=1:
                flag = True
#                print "get at %d %d ,color %d" % (i,j,pix[i,j])
                break
        if flag:
            return i
    print("nothing detected for left bound")
    sys.exit(0)

def up_bound(im):
    print "checking up bound"
    (weight, height) = im.size
    pix = im.load()
    for j in range(height):
        flag = False
        for i in range(weight):
            if pix[i,j] != 0 and pix[i,j]!=1:
                flag = True
#                print "get at %d %d ,color %d" % (i,j,pix[i,j])
                break
        if flag:
            return j
    print("nothing detected for up bound")
    sys.exit(0)


left_bound_for_left_img = left_bound(im)
up_bound_for_left_img = up_bound(im)
right_bound_for_left_img = right_bound(im)
low_bound_for_left_img = low_bound(im)
print_slice()
print("get left bound %d" % left_bound_for_left_img)
print("get up bound %d" % up_bound_for_left_img)
print_slice()
left_bound_for_right_img = left_bound(cmp_im)
up_bound_for_right_img = up_bound(cmp_im)
print_slice()
print("get left bound %d" % left_bound_for_right_img)
print("get up bound %d" % up_bound_for_right_img)

print_slice()

def cmp(img1, img2):
    (w1,h1) = img1.size
    (w,h) = img2.size
    img2_palette = img2.getpalette()
    img2_palette[10] = 0
    img2_palette[11] = 245
    img2_palette[12] = 255
    print("palette setup done")
    print_slice()
    
    new_img = img2.copy()

    new_img.putpalette(img2_palette)
    complcate = (right_bound_for_left_img - left_bound_for_left_img - 1) * (low_bound_for_left_img - up_bound_for_left_img - 1)
    print("complcate is %d" % complcate)
    
    i_range = range(left_bound_for_left_img + 1, right_bound_for_left_img)
    j_range = range(up_bound_for_left_img + 1, low_bound_for_left_img)
    img1Data = img1.getdata()
    img2Data = img2.getdata()

    for i in i_range:
        for j in j_range:
            right_w = i - left_bound_for_left_img + left_bound_for_right_img
            right_h = j - up_bound_for_left_img + up_bound_for_right_img
            if right_w >= w:
                break
            if right_h >= h:
                break
            img2Pix = img2Data[right_w+right_h * w]
            delta = img1Data[i + j * w1] - img2Pix
            if abs(delta) > 0:
                new_img.putpixel((right_w, right_h), 3)
    new_img.save("output.png")

cmp(im, cmp_im)
print("done")
