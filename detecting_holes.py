from Tkinter import *
import sys, os, random, Image, ImageTk, ImageDraw
from filters_methods import *

class Holes:
    def __init__(self, image_file_path):
        self.image_file_path = image_file_path
        self.image = Image.open(image_file_path)

        self.root = Tk()
        self.root.title('Holes')
        self.root.resizable(width=False, height=False)

        self.imagetk = self.convert_to_imagetk(self.image)

        self.label1 = Label(self.root, image=self.imagetk)
        self.label1.pack(side=LEFT)

        self.button1 = Button(text='Holes', width=10,
                              command=self.action).pack()
        self.button_exit = Button(text='Exit', width=10,
                              command=self.root.destroy).pack()
        self.dark_color = 35
        self.action()
        self.root.mainloop()

    def convert_to_imagetk(self, image):
        return ImageTk.PhotoImage(image)

    def update_image(self, image):
        self.imagetk = self.convert_to_imagetk(image)
        self.label1.config(image=self.imagetk)
        self.label1.pack()
        self.root.mainloop()

    def bfs(self, image, start_pixel_pos, color):
        pixels = image.load()
        width, height = get_image_size(image)
        queue = []
        copy = []
        count = 0
        queue.append(start_pixel_pos)
        original = pixels[start_pixel_pos]

        while 0 < len(queue):
            (x, y) = queue.pop(0)
            current = pixels[x, y]
            if current == original or current == color:
                for pos_x in [-1, 0, 1]:
                    for pos_y in [-1, 0, 1]:
                        pixel_x = x + pos_x
                        pixel_y = y + pos_y
                        if pixel_x >= 0 and pixel_x < width and pixel_y >= 0 and pixel_y < height:
                            pixel_data = pixels[pixel_x, pixel_y]
                            if pixel_data == original:
                                pixels[pixel_x, pixel_y] = color
                                copy.append((pixel_x, pixel_y))
                                queue.append((pixel_x, pixel_y))
                                count += 1
        return image, count, copy

    def minimums_in_histogram(self, hist):
        minimums = list()
        for i, value in enumerate(hist):
            try:
                if hist[i-2] > value and hist[i-1] > value and value <= hist[i+1]:
                    minimums.append(i)
            except:
                pass
        return minimums

    def action(self):
        image = grayscale(self.image)
        image = binarization(self.image, 80)
        width, height = get_image_size(image)
        pixels = image.load()

        hist_verti = list()
        for x in range(width):
            pixels_sum = 0
            for y in range(height):
                pixels_sum += pixels[x, y][0]
            hist_verti.append(pixels_sum/255)

        hist_horiz = list()
        for y in range(height):
            pixels_sum = 0
            for x in range(width):
                pixels_sum += pixels[x, y][0]
            hist_horiz.append(pixels_sum/255)

        min_x = self.minimums_in_histogram(hist_verti)
        min_y = self.minimums_in_histogram(hist_horiz)

        holes = list()
        counter = 1
        for x in min_x:
            for y in min_y:
                this_pixel_color = pixels[x, y][0]
                if this_pixel_color < self.dark_color:
                    r = random.randint(60, 100)
                    g = random.randint(15, 55)
                    b = random.randint(80, 120)
                    image, count, pixels_with_color = self.bfs(image, (x, y), (r, g, b))
                    percentage = (count * 100.0)/(width*height)
                    holes.append((counter, percentage, (x, y), (r, g, b), pixels_with_color))
                    counter += 1

        image = Image.open(self.image_file_path)
        draw = ImageDraw.Draw(image)
        pixels = image.load()
        for hole in holes:
            counter, percentage, center, color, pixels_with_color = hole
            for x, y in pixels_with_color:
                pixels[x, y] = color
            x, y = center
            print 'Hole %d detected at (%d, %d)' % (counter, x, y)
            print '> %.4f%% of all the image' % percentage
            draw.ellipse((x-2, y-2, x+2, y+2), fill=(255, 255, 0), outline=(255, 255, 0))
            draw.text((x+4, y-4), 'Hole '+str(counter), fill=(255, 0, 0))

        self.update_image(image)

def main():
    if len(sys.argv) > 0:
        image_file_path = sys.argv[1]
        if os.path.isfile(image_file_path):
            Holes(image_file_path)
        else:
            print 'Image file does not exist'
    else:
        print 'First parameter must be an image file name'

if __name__ == '__main__':
    main()

