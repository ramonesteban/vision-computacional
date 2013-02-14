import sys, os, random, Image

def open_image(image_file_path):
    image = Image.open(image_file_path)
    image.thumbnail((600, 450), Image.ANTIALIAS)
    return image

def get_image_size(image):
    width, height = image.size
    return (width, height)

def grayscale(image):
    width, height = get_image_size(image)
    for w in range(width):
        for h in range(height):
            r, g, b = image.getpixel((w, h))
            gray = (r+g+b)/3
            image.putpixel((w, h), (gray, gray, gray))
    return image

def put_salt_and_pepper(image_file_path, intensity):
    image = open_image(image_file_path)
    width, height = get_image_size(image)
    image = grayscale(image)

    for w in range(width):
        for h in range(height):
            if random.random() < intensity:
                if random.random() < 0.5:
                    image.putpixel((w, h), (0, 0, 0))
                else:
                    image.putpixel((w, h), (255, 255, 255))
    image.show()
    return image

def remove_salt_and_pepper(image):
    image_copy = image
    width, height = get_image_size(image)

    for w in range(width):
        for h in range(height):
            pixel = image_copy.getpixel((w, h))[0]
            if pixel == 0 or pixel == 255:
                pixel_list = []
                try: pixel_list.append(image_copy.getpixel((w, h-1))[0])
                except: pass
                try: pixel_list.append(image_copy.getpixel((w, h+1))[0])
                except: pass
                try: pixel_list.append(image_copy.getpixel((w-1, h))[0])
                except: pass
                try: pixel_list.append(image_copy.getpixel((w+1, h))[0])
                except: pass
                try: pixel_list.append(image_copy.getpixel((w-1, h-1))[0])
                except: pass
                try: pixel_list.append(image_copy.getpixel((w-1, h+1))[0])
                except: pass
                try: pixel_list.append(image_copy.getpixel((w+1, h-1))[0])
                except: pass
                try: pixel_list.append(image_copy.getpixel((w+1, h+1))[0])
                except: pass
                pixel = sum(pixel_list)/len(pixel_list)
                image.putpixel((w, h), (pixel, pixel, pixel))
    image.show()

def main():
    if len(sys.argv) > 2:
        image_file_path = str(sys.argv[1])
        intensity = float(sys.argv[2])
        if os.path.isfile(image_file_path):
            image = put_salt_and_pepper(image_file_path, intensity)
            remove_salt_and_pepper(image)
        else:
            print 'Image file does not exist'
    else:
        print 'Missing parameters'

if __name__ == '__main__':
    main()

