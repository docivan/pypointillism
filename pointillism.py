import random
import math
import cairo
import cv2

scale = 0.1
radius_max = 10
radius_min = 4
segment_cnt = 8
pos_jitter = 5
rad_scale = 1.5

src_img = cv2.imread("eye.jpg")
img = cv2.cvtColor(cv2.resize(src_img, (int(src_img.shape[1]*scale), int(src_img.shape[0]*scale))), cv2.COLOR_BGR2RGB)

img_w = img.shape[1]
img_h = img.shape[0]

#surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, img_w*radius_max*2, img_h*radius_max*2)
surface = cairo.PDFSurface("example.pdf", img_w*radius_max*2, img_h*radius_max*2)
ctx = cairo.Context(surface)

ctx.rectangle(0, 0, img_w*radius_max*2, img_h*radius_max*2)
ctx.set_source_rgba(0,0,0,1)
ctx.fill()

for y in range(img_h):
    for x in range(img_w):
        r, g, b = img[y][x][0], img[y][x][1], img[y][x][2]

        # https://stackoverflow.com/questions/596216/formula-to-determine-brightness-of-rgb-color
        lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
        local_rad_max = radius_min + (radius_max - radius_min) / 255 * lum

        center_x = x*radius_max*2 + radius_max + pos_jitter * random.random() - pos_jitter/2
        center_y = y*radius_max*2 + radius_max + pos_jitter * random.random() - pos_jitter/2

        for i in range(segment_cnt):
            radius = radius_min + (local_rad_max - radius_min) * random.random()
            radius *= rad_scale
            radians = 2 * math.pi / segment_cnt * i

            vertex_x = math.cos(radians) * radius + center_x
            vertex_y = math.sin(radians) * radius + center_y

            ctx.line_to(vertex_x, vertex_y)

        ctx.close_path()
        ctx.set_source_rgba(r/255., g/255., b/255., 1)
        ctx.fill()

surface.show_page()