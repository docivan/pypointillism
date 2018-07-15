import random
import math
import cairo
import cv2
import numpy as np
import matplotlib.pyplot as plt

radius_max = 50
radius_min = 4
alpha_min = 0.1
points = 10000

src_img = cv2.imread("eye.jpg")
img_w = src_img.shape[1]
img_h = src_img.shape[0]

img = cv2.cvtColor(src_img, cv2.COLOR_BGR2RGB)

print("Computing luminosity channel...")
lum = [0.2126 * x[0] + 0.7152 * x[1] + 0.0722 * x[2] for y in img for x in y]

print("Normalizing...")
lum -= np.median(lum)
lum /= np.std(lum)
lum = np.abs(lum)

lum_max = max(lum)

lum_accum = []
sum = 0

print("Accumulating...")
for i in lum:
    sum += i
    lum_accum.append(sum)

lum_sum = lum_accum[len(lum_accum)-1]


def gen_random_xy():
    a = lum_sum*random.random()
    idx = -1

    for i in range(len(lum_accum)):
        if lum_accum[i] > a:
            idx = i - 1
            break

    if idx < 0:
        idx = 0

    y = idx // img_w
    x = idx - y*img_w
    lumval = lum[idx]

    return x, y, lumval


#prep for exporting pdf
surface = cairo.PDFSurface("example2.pdf", img_w, img_h)
ctx = cairo.Context(surface)

ctx.rectangle(0, 0, img_w, img_h)
ctx.set_source_rgba(0,0,0,1)
ctx.fill()

print("Painting...")
for i in range(points):
    if i % 100 == 0:
        print(i)

    x, y, lumval = gen_random_xy()

    r = radius_min + (radius_max-radius_min)*(1 - lumval/lum_max)
    a = alpha_min + (1 - alpha_min)*(lumval/lum_max)

    ctx.arc(x, y, r, 0, 2*math.pi)
    ctx.set_source_rgba(img[y][x][0]/255., img[y][x][1]/255., img[y][x][2]/255., a)
    ctx.fill()

surface.show_page()
