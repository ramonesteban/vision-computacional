from Tkinter import *
import sys, os, Image, ImageTk

class Filters:
    def __init__(self, image_file_path):
        self.image_file_path = image_file_path
        self.image = self.open_image(self.image_file_path)

        self.root = Tk()
        self.root.title('Filters')
        self.root.resizable(width=False, height=False)

        self.imagetk_original = self.convert_to_imagetk(self.image)
        self.imagetk_modified = self.imagetk_original

        self.label1 = Label(self.root, image=self.imagetk_original)
        self.label1.pack(side=LEFT)
        self.label2 = Label(self.root, image=self.imagetk_modified)
        self.label2.pack(side=LEFT)

        self.button1 = Button(text='Reset', width=10,
                              command=self.reset_image).pack()
        self.button2 = Button(text='Black and White', width=10,
                              command=self.black_and_white).pack()
        self.button3 = Button(text='Grayscale', width=10,
                              command=self.grayscale).pack()
        self.button4 = Button(text='Thresholds', width=10,
                              command=self.thresholds).pack()
        self.button5 = Button(text='Average', width=10,
                              command=self.average).pack()
        self.button6 = Button(text='Average All', width=10,
                              command=self.average_allneighbors).pack()
        self.button7 = Button(text='Negative', width=10,
                              command=self.negative).pack()
        self.button8 = Button(text='Sepia', width=10,
                              command=self.sepia).pack()
        self.button_exit = Button(text='Exit', width=10,
                              command=self.root.destroy).pack()
        self.root.mainloop()

    def open_image(self, image_file_path):
        image = Image.open(image_file_path)
        image.thumbnail((400, 300), Image.ANTIALIAS)
        return image

    def convert_to_imagetk(self, image):
        return ImageTk.PhotoImage(image)

    def get_image_size(self, image):
        width, height = image.size
        return (width, height)

    def reset_window(self):
        self.imagetk_modified = self.convert_to_imagetk(self.image)
        self.label2.config(image=self.imagetk_modified)
        self.label2.pack()
        self.root.mainloop()

    def reset_image(self):
        print 'Reset image'
        self.image = self.open_image(self.image_file_path)
        self.reset_window()

    def black_and_white(self):
        print 'Black and white'
        width, height = self.get_image_size(self.image)
        gray_base = 180

        for w in range(width):
            for h in range(height):
                r, g, b = self.image.getpixel((w, h))
                gray = (r+g+b)/3
                if gray < gray_base:
                    self.image.putpixel((w, h), (0, 0, 0))
                else:
                    self.image.putpixel((w, h), (255, 255, 255))
        self.reset_window()

    def grayscale(self):
        print 'Grayscale'
        width, height = self.get_image_size(self.image)

        for w in range(width):
            for h in range(height):
                r, g, b = self.image.getpixel((w, h))
                gray = (r+g+b)/3
                self.image.putpixel((w, h), (gray, gray, gray))
        self.reset_window()

    def thresholds(self):
        print 'Thresholds'
        width, height = self.get_image_size(self.image)
        level_min = 100
        level_max = 200

        for w in range(width):
            for h in range(height):
                r, g, b = self.image.getpixel((w, h))
                gray = (r+g+b)/3
                if gray < level_min:
                    self.image.putpixel((w, h), (0, 0, 0))
                elif gray > level_max:
                    self.image.putpixel((w, h), (255, 255, 255))
                else:
                    self.image.putpixel((w, h), (gray, gray, gray))
        self.reset_window()

    def average(self):
        print 'Average'
        width, height = self.get_image_size(self.image)
        self.image_copy = self.image

        for w in range(width):
            for h in range(height):
                if w > 0 and w < width-1 and h > 0 and h < height-1:
                    r1, g1, b1 = self.image_copy.getpixel((w, h))
                    r2, g2, b2 = self.image_copy.getpixel((w, h-1))
                    r3, g3, b3 = self.image_copy.getpixel((w-1, h))
                    r4, g4, b4 = self.image_copy.getpixel((w, h+1))
                    r5, g5, b5 = self.image_copy.getpixel((w+1, h))
                    r, g, b = ((r1+r2+r3+r4+r5)/5,
                               (g1+g2+g3+g4+g5)/5,
                               (b1+b2+b3+b4+b5)/5)
                    self.image.putpixel((w, h), (r, g, b))
        self.reset_window()

    def average_allneighbors(self):
        print 'Average With All Neighbors'
        width, height = self.get_image_size(self.image)
        self.image_copy = self.image

        for w in range(width):
            for h in range(height):
                if w > 0 and w < width-1 and h > 0 and h < height-1:
                    r1, g1, b1 = self.image_copy.getpixel((w, h))
                    r2, g2, b2 = self.image_copy.getpixel((w, h-1))
                    r3, g3, b3 = self.image_copy.getpixel((w, h+1))
                    r4, g4, b4 = self.image_copy.getpixel((w-1, h))
                    r5, g5, b5 = self.image_copy.getpixel((w-1, h-1))
                    r6, g6, b6 = self.image_copy.getpixel((w-1, h+1))
                    r7, g7, b7 = self.image_copy.getpixel((w+1, h))
                    r8, g8, b8 = self.image_copy.getpixel((w+1, h-1))
                    r9, g9, b9 = self.image_copy.getpixel((w+1, h+1))
                    r, g, b = ((r1+r2+r3+r4+r5+r6+r7+r8+r9)/9,
                               (g1+g2+g3+g4+g5+g6+g7+g8+g9)/9,
                               (b1+b2+b3+b4+b5+b6+b7+b8+b9)/9)
                    self.image.putpixel((w, h), (r, g, b))
        self.reset_window()

    def negative(self):
        print 'Negative'
        width, height = self.get_image_size(self.image)

        for w in range(width):
            for h in range(height):
                r, g, b = self.image.getpixel((w, h))
                gray = (r+g+b)/3
                self.image.putpixel((w, h), (255-r, 255-g, 255-b))
        self.reset_window()

    def sepia(self):
        print 'Sepia'
        width, height = self.get_image_size(self.image)
        sepia_intensity = 25

        for w in range(width):
            for h in range(height):
                r, g, b = self.image.getpixel((w, h))
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
                self.image.putpixel((w, h), (r, g, b))
        self.reset_window()

def main():
    if len(sys.argv) > 1:
        image_file_path = sys.argv[1]
        if os.path.isfile(image_file_path):
            Filters(image_file_path)
        else:
            print 'Image file does not exist'
    else:
        print 'First parameter must be an image file name'

if __name__ == '__main__':
    main()

