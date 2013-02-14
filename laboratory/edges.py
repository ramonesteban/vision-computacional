from Tkinter import *
import sys, os, random, Image, ImageTk
from filters_methods import *

class Edges:
    def __init__(self, image_file_path):
        self.image_file_path = image_file_path
        image = self.open_image(self.image_file_path)
        self.temp_image = image

        self.root = Tk()
        self.root.title('Edges')
        self.root.resizable(width=False, height=False)

        self.imagetk = self.convert_to_imagetk(image)

        self.label1 = Label(self.root, image=self.imagetk)
        self.label1.pack(side=LEFT)

        self.button1 = Button(text='Reset', width=15,
                              command=self.reset_image).pack()
        self.button2 = Button(text='Convolution', width=15,
                              command=self.action).pack()
        self.button3 = Button(text='Difference', width=15,
                              command=self.difference).pack()
        self.button4 = Button(text='Put Salt & Pepper', width=15,
                              command=self.put_salt_and_pepper).pack()
        self.button5 = Button(text='Remove Salt & Pepper', width=15,
                              command=self.remove_salt_and_pepper).pack()
        self.button_exit = Button(text='Exit', width=15,
                              command=self.root.destroy).pack()
        self.root.mainloop()

    def open_image(self, image_file_path):
        image = Image.open(image_file_path)
        image.thumbnail((600, 450), Image.ANTIALIAS)
        return image

    def save_image(self, image, width, height):
        pixels = image.getdata()
        newimage = Image.new('RGB', (width, height))
        newimage.putdata(pixels)
        newimage.save('output.jpg')

    def convert_to_imagetk(self, image):
        return ImageTk.PhotoImage(image)

    def reset_image(self):
        image = self.open_image(self.image_file_path)
        self.update_image(image)

    def update_image(self, image):
        self.imagetk = self.convert_to_imagetk(image)
        self.label1.config(image=self.imagetk)
        self.label1.pack()
        self.root.mainloop()

    def action(self):
        f = self.open_image(self.image_file_path)
        f = grayscale(f)
        h = [[0, 1, 0], [1, -4, 1], [0, 1, 0]]

        image = self.convolution(h, f)
        image = average_allneighbors(image)
        image = binarization(image, 18)
        self.update_image(image)

    def convolution(self, h, f):
        F = self.open_image(self.image_file_path)
        width, height = get_image_size(F)
        k = len(h[1])

        for x in range(width):
            for y in range(height):
                suma = 0
                for i in range(k):
                    z1 = i - k/2
                    for j in range(k):
                        z2 = j - k/2
                        try:
                            suma += f.getpixel((x+z1, y+z2))[0]*h[i][j]
                        except:
                            pass
                suma = int(suma)
                F.putpixel((x, y), (suma, suma, suma))
        return F

    def difference(self):
        image = self.open_image(self.image_file_path)
        width, height = get_image_size(image)

        image_original = self.open_image(self.image_file_path)
        image_original = grayscale(image_original)

        image_filtrada = self.open_image(self.image_file_path)
        image_filtrada = grayscale(image_filtrada)
        image_filtrada = average_allneighbors(image_filtrada)

        for w in range(width):
            for h in range(height):
                r1, g1, b1 = image_filtrada.getpixel((w, h))
                r2, g2, b2 = image_original.getpixel((w, h))
                dif = int(abs(r2 - r1))
                image.putpixel((w, h), (dif, dif, dif))
        image = binarization(image, 18)
        self.update_image(image)

    def put_salt_and_pepper(self):
        intensity = 0.05
        image = self.open_image(self.image_file_path)
        width, height = get_image_size(image)
        image = grayscale(image)

        for w in range(width):
            for h in range(height):
                if random.random() < intensity:
                    if random.random() < 0.5:
                        image.putpixel((w, h), (0, 0, 0))
                    else:
                        image.putpixel((w, h), (255, 255, 255))
        self.save_image(image, width, height)
        self.temp_image = image
        self.update_image(image)

    def remove_salt_and_pepper(self):
        image_copy = self.temp_image
        width, height = get_image_size(image_copy)

        for w in range(width):
            for h in range(height):
                pixel = self.temp_image.getpixel((w, h))[0]
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
                    self.temp_image.putpixel((w, h), (pixel, pixel, pixel))
        self.update_image(self.temp_image)

def main():
    if len(sys.argv) > 0:
        image_file_path = sys.argv[1]
        if os.path.isfile(image_file_path):
            Edges(image_file_path)
        else:
            print 'Image file does not exist'
    else:
        print 'First parameter must be an image file name'

if __name__ == '__main__':
    main()

