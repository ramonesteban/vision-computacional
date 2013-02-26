from Tkinter import *
import sys, os, random, math, Image, ImageTk
from filters_methods import *

class Lines:
    def __init__(self, image_file_path):
        self.image_file_path = image_file_path
        image = self.open_image(self.image_file_path)
        self.temp_image = image

        self.root = Tk()
        self.root.title('Lines')
        self.root.resizable(width=False, height=False)

        self.imagetk = self.convert_to_imagetk(image)

        self.label1 = Label(self.root, image=self.imagetk)
        self.label1.pack(side=LEFT)

        self.button1 = Button(text='Reset', width=10,
                              command=self.reset_image).pack()
        self.button2 = Button(text='Lines', width=10,
                              command=self.action).pack()
        self.button_exit = Button(text='Exit', width=10,
                              command=self.root.destroy).pack()
        self.root.mainloop()

    def open_image(self, image_file_path):
        image = Image.open(image_file_path)
        image.thumbnail((500, 500), Image.ANTIALIAS)
        return image

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

    def detect_lines(self, image, imagenx, imageny):
        width, height = get_image_size(image)
        x_lines = imagenx.load()
        y_lines = imageny.load()

        dictionary = {}
        complete_list = []

        for i in range(width):
            temp_list = []
            for j in range(height):
                x = x_lines[i, j][0]
                y = y_lines[i, j][0]
                angle = 0.0
                if x + y <= 0.0:
                    angle = None
                elif x == 0 and y == 255:
                    angle = 90
                else:
                    angle = math.degrees(y/x)
                if angle == None:
                    temp_list.append((None, None))
                else:
                    rho = abs((i)*math.cos(angle) + (j)*math.sin(angle))
                    if i > 0 and j > 0 and i < width and j < height:
                        if (rho, angle) in dictionary:
                            dictionary[(rho, angle)] += 1
                        else:
                            dictionary[(rho, angle)] = 1
                    temp_list.append((rho, angle))
            complete_list.append(temp_list)

        frecuency = {}
        dictionary = sorted(dictionary.items(), key = lambda tupla: tupla[1], reverse = True)
        for i in range(len(dictionary)):
            (rho, angle) = dictionary[i][0]
            frecuency[(rho, angle)] = dictionary[1]

        x_counter = 0
        y_counter = 0
        for i in range(width):
            for j in range(height):
                if i > 0 and j > 0 and i < width and j < height:
                    rho, angle = complete_list[i][j]
                    if (rho, angle) in frecuency:
                        if angle == 0:
                            image.putpixel((i, j), (255, 0, 0))
                            x_counter += 1
                        if angle == 90:
                            image.putpixel((i, j), (120, 0, 0))
                            y_counter += 1

        print 'Vertical pixels:', x_counter
        print 'Horizontal pixels:', y_counter
        return image

    def action(self):
        f = self.open_image(self.image_file_path)
        f = grayscale(f)

        hx = [[-1, -1, -1], [2, 2, 2], [-1, -1, -1]]
        hy = [[-1, 2, -1], [-1, 2, -1], [-1, 2, -1]]
        imagex = self.convolution(hx, f)
        imagey = self.convolution(hy, f)
        imagex = binarization(imagex, 20)
        imagey = binarization(imagey, 20)

        image = self.detect_lines(f, imagex, imagey)
        self.update_image(image)

def main():
    if len(sys.argv) > 0:
        image_file_path = sys.argv[1]
        if os.path.isfile(image_file_path):
            Lines(image_file_path)
        else:
            print 'Image file does not exist'
    else:
        print 'First parameter must be an image file name'

if __name__ == '__main__':
    main()

