import Image

def get_image_size(image):
    width, height = image.size
    return (width, height)

def binarization(image, gray_base):
    print 'Black and white'
    width, height = get_image_size(image)

    for w in range(width):
        for h in range(height):
            r, g, b = image.getpixel((w, h))
            gray = (r+g+b)/3
            if gray < gray_base:
                image.putpixel((w, h), (0, 0, 0))
            else:
                image.putpixel((w, h), (255, 255, 255))
    return image

def grayscale(image):
    print 'Grayscale'
    width, height = get_image_size(image)

    for w in range(width):
        for h in range(height):
            r, g, b = image.getpixel((w, h))
            gray = (r+g+b)/3
            image.putpixel((w, h), (gray, gray, gray))
    return image

def thresholds(image, level_min, level_max):
    print 'Thresholds'
    width, height = get_image_size(image)

    for w in range(width):
        for h in range(height):
            r, g, b = image.getpixel((w, h))
            gray = (r+g+b)/3
            if gray < level_min:
                image.putpixel((w, h), (0, 0, 0))
            if gray > level_max:
                image.putpixel((w, h), (255, 255, 255))
            image.putpixel((w, h), (gray, gray, gray))
    return image

def average(image):
    print 'Average'
    width, height = get_image_size(image)
    image_copy = image

    for w in range(width):
        for h in range(height):
            if w > 0 and w < width-1 and h > 0 and h < height-1:
                r1, g1, b1 = image_copy.getpixel((w, h))
                r2, g2, b2 = image_copy.getpixel((w, h-1))
                r3, g3, b3 = image_copy.getpixel((w-1, h))
                r4, g4, b4 = image_copy.getpixel((w, h+1))
                r5, g5, b5 = image_copy.getpixel((w+1, h))
                r, g, b = ((r1+r2+r3+r4+r5)/5,
                           (g1+g2+g3+g4+g5)/5,
                           (b1+b2+b3+b4+b5)/5)
                image.putpixel((w, h), (r, g, b))
    return image

def average_allneighbors(image):
    print 'Average With All Neighbors'
    width, height = get_image_size(image)
    image_copy = image

    for w in range(width):
        for h in range(height):
            if w > 0 and w < width-1 and h > 0 and h < height-1:
                r1, g1, b1 = image_copy.getpixel((w, h))
                r2, g2, b2 = image_copy.getpixel((w, h-1))
                r3, g3, b3 = image_copy.getpixel((w, h+1))
                r4, g4, b4 = image_copy.getpixel((w-1, h))
                r5, g5, b5 = image_copy.getpixel((w-1, h-1))
                r6, g6, b6 = image_copy.getpixel((w-1, h+1))
                r7, g7, b7 = image_copy.getpixel((w+1, h))
                r8, g8, b8 = image_copy.getpixel((w+1, h-1))
                r9, g9, b9 = image_copy.getpixel((w+1, h+1))
                r, g, b = ((r1+r2+r3+r4+r5+r6+r7+r8+r9)/9,
                           (g1+g2+g3+g4+g5+g6+g7+g8+g9)/9,
                           (b1+b2+b3+b4+b5+b6+b7+b8+b9)/9)
                image.putpixel((w, h), (r, g, b))
    return image

def negative(image):
    print 'Negative'
    width, height = get_image_size(image)

    for w in range(width):
        for h in range(height):
            r, g, b = image.getpixel((w, h))
            gray = (r+g+b)/3
            image.putpixel((w, h), (255-r, 255-g, 255-b))
    return image

def sepia(image, sepia_intensity=25):
    print 'Sepia'
    width, height = get_image_size(image)

    for w in range(width):
        for h in range(height):
            r, g, b = image.getpixel((w, h))
            gray = (r+g+b)/3
            r = gray + (sepia_intensity * 2)
            g = gray + sepia_intensity
            b = gray - sepia_intensity

            if r > 255:
                r = 255
            if g > 255:
                g = 255
            if b < 0:
                b = 0
            image.putpixel((w, h), (r, g, b))
    return image

