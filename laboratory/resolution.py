import sys
import math

def get_resolution(total_pixels):
    digits = len(str(total_pixels))
    if digits <= 5:
        size = total_pixels/10.0**3
        prefix = 'K'
    elif digits <= 8:
        size = total_pixels/10.0**6
        prefix = 'M'
    else:
        size = total_pixels/10.0**9
        prefix = 'G'
    return (size, prefix)

def get_factor(prefix):
    if prefix == 'k':
        return 10**3
    if prefix == 'm':
        return 10**6
    if prefix == 'g':
        return 10**9

def get_width_height(pixels, relation_x, relation_y):
    x = math.sqrt(pixels/(relation_x*relation_y))
    return (int(x*relation_x), int(x*relation_y))

def main():
    try:
        option = sys.argv[1]
    except:
	print 'Argument expected:'
	print '-r get image resolution'
	print '-p get image width and height in pixels'
        return

    if option == '-r':
        try:
            image_area = raw_input('Write the image width and height (e.g. 1024x769): ')
            image_area = image_area.split('x')
            width = int(image_area[0])
            height = int(image_area[1])
            total_pixels = width*height
            size, prefix = get_resolution(total_pixels)
            print '%.1f%spx' % (size, prefix)
        except:
            print 'Something is wrong'
    elif option == '-p':
        try:
            image_size = raw_input('Write the image size (e.g. 5Mpx): ')
            aspect_ratio = raw_input('Write the aspect ratio (e.g. 16:9): ')
            size = int(image_size[0])
            prefix = image_size[1].lower()
            factor = get_factor(prefix)
            pixels = size*factor
            relation = aspect_ratio.split(':')
            relation_x = int(relation[0])
            relation_y = int(relation[1])
            width, height = get_width_height(pixels, relation_x, relation_y)
            print 'The image has %d x %d pixels' % (width, height)
        except:
            print 'Something is wrong'
    else:
        print 'Invalid parameter'
        return

if __name__ == '__main__':
    main()
