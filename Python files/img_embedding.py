import cv2
import numpy as n


def intToBinary(msg):
    binary = [format(i, "08b") for i in msg]
    return binary  # list


def binaryToInt(rgb):
    r, g, b = rgb
    rgb = (int(r, 2), int(g, 2), int(b, 2))
    rgb = n.asarray(rgb)
    return rgb


def mergeRGB(rgb1, rgb2):
    r1, g1, b1 = rgb1
    r2, g2, b2 = rgb2
    rgb = (r2[:6] + r1[:2],
           g2[:6] + g1[:2],
           b2[:6] + b1[:2])
    return rgb  # tuple


def merge(img1, img2):
    if img1.shape[0] > img2.shape[0] or img1.shape[1] > img2.shape[1]:
        print("Reduce the size of embedding image or increase the size of cover image")
        return
    merge = n.zeros((img2.shape[0], img2.shape[1], 3), dtype=n.uint8)
    row = -1
    col = -1
    for i in img2:  # gives rows
        row += 1
        col = -1
        for pixel in i:  # gives column
            col += 1
            rgb2 = intToBinary(pixel)
            if row < img1.shape[0] and col < img1.shape[1]:
                rgb1 = intToBinary(img1[row][col])
            else:
                rgb1 = intToBinary(n.array((0, 0, 0)))
            tup = mergeRGB(rgb1, rgb2)
            merge[row][col] = binaryToInt(tup)
    cv2.imwrite(r'Images\merged.png', merge)
    mergename = 'Images\merged.png'
    return mergename


def unmerge(img):
    unmerge = n.zeros((img.shape[0], img.shape[1], 3), dtype=n.uint8)
    size = [0, 0]  # list
    row = -1
    col = -1
    for i in img:
        row += 1
        col = -1
        for pixel in i:
            col += 1
            r, g, b = intToBinary(pixel)
            rgb = (r[6:] + "000000",
                   g[6:] + "000000",
                   b[6:] + "000000")
            unmerge[row][col] = binaryToInt(rgb)
            r, g, b = unmerge[row][col]
            if not (r == 0 and g == 0 and b == 0):
                size = [row+1, col+1]

    for i in range(unmerge.shape[1]-1, 0, -1):
        r, g, b = unmerge[0][i]
        if r == 0 and b == 0 and g == 0:
            size[1] = i
        else:
            break

    unmerge1 = unmerge[0:size[0], 0:size[1]]
    cv2.imwrite(r'Images\unmerged.png', unmerge1)


def main():
    # merge image1 to image2
    image1 = cv2.imread(r'Images\waterfall2.png', 1)
    image2 = cv2.imread(r'Images\sunset2.png', 1)
    # print(image1.shape) # 200,300,3
    mergename = merge(image1, image2)
    mergedImage = cv2.imread(mergename, 1)
    unmerge(mergedImage)


main()