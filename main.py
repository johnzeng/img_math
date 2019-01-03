import os, sys
from PIL import Image, ImageDraw

argv = sys.argv
if len(argv) != 2:
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

def print_slice():
    print("===================================")

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
    print "checking left bound"
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
print_slice();
print("get left bound %d" % left_bound_for_left_img)
print("get up bound %d" % up_bound_for_left_img)
print_slice();
left_bound_for_right_img = left_bound(cmp_im)
up_bound_for_right_img = up_bound(cmp_im)
print_slice();
print("get left bound %d" % left_bound_for_right_img)
print("get up bound %d" % up_bound_for_right_img)

def cmp(img1, img2):
    (maxw, maxh) = img1.size
    (w,h) = img2.size

    for i in range(left_bound_for_left_img, maxw):
        for j in range(up_bound_for_left_img, maxh):
            right_w = i - left_bound_for_left_img + left_bound_for_right_img
            right_h = j - up_bound_for_left_img + up_bound_for_right_img
            if right_w >= w :
                continue
            if right_h >= h:
                continue
            delta = img1.getpixel((i,j)) - img2.getpixel((right_w,right_h))
#            print("[%d,%d] %d, [%d, %d] %d"% (i,j, img1.getpixel((i,j)), right_w, right_h, img2.getpixel((right_w, right_h))))
            if abs(delta) >= 1:
                print("too much diff at : (%d,%d) %d (%d %d ) %d "%(i,j, img1.getpixel((i,j)), right_w, right_h, img2.getpixel((right_w, right_h))))

#cmp(shinked_im, shinked_im2)
#shinked_im.save("new_image.png")
#shinked_im2.save("new_image2.png")
cmp(im, cmp_im)
print("done")
