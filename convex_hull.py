from Tkinter import *
import sys, os, random, Image, ImageTk, ImageDraw
from filters_methods import *

class Convex:
    def __init__(self, image_file_path):
        self.image_file_path = image_file_path
        image = self.open_image(self.image_file_path)
        self.temp_image = image

        self.root = Tk()
        self.root.title('Convex')
        self.root.resizable(width=False, height=False)

        self.imagetk = self.convert_to_imagetk(image)

        self.label1 = Label(self.root, image=self.imagetk)
        self.label1.pack(side=LEFT)

        self.button1 = Button(text='Reset', width=10,
                              command=self.reset_image).pack()
        self.button2 = Button(text='Convex', width=10,
                              command=self.action).pack()
        self.button_exit = Button(text='Exit', width=10,
                              command=self.root.destroy).pack()
        self.root.mainloop()

    def open_image(self, image_file_path):
        image = Image.open(image_file_path)
        image.thumbnail((800, 800), Image.ANTIALIAS)
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

    def bfs(self, image, start_pixel_pos, color):
        pixels = image.load()
        width, height = get_image_size(image)
        queue = []
        queue_copy = []
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
                                image.putpixel((pixel_x, pixel_y), color)
                                queue.append((pixel_x, pixel_y))
                                queue_copy.append((pixel_x, pixel_y))
        return image, queue_copy

    def gift_wrapping(self, pixels):
        hull = [min(pixels)]
        for i in range(len(pixels)):
            end = pixels[0]
            for j in range(len(pixels) - 1):
                if 0 < (hull[i][0] - pixels[j][0])*(end[1] - pixels[j][1]) - (end[0] - pixels[j][0])*(hull[i][1] - pixels[j][1]):
                    side = -1
                else:
                    side = 1
                if end == hull[i] or side == -1:
                    end = pixels[j]
            hull.append(end)
            if end == hull[0]:
                break
        return hull

    def convex_hull(self, image):
        width, height = get_image_size(image)
        drawing = ImageDraw.Draw(image)
        pixels = image.load()
        hulls = []

        for i in range(width):
            for j in range(height):
                # Ahora detectamos los contornos por su color blanco
                if pixels[i, j] == (255, 255, 255):
                    # Obtenemos todos los pixeles dentro del contorno
                    # y usamos el metodo grift wrapping para obtener
                    # los puntos que estan mas al exterior del contorno actual
                    image, pixels_in = self.bfs(image, (i, j), (0, 0, 100))
                    hulls.append(self.gift_wrapping(pixels_in))
        for i in range(len(hulls)):
            for j in range(len(hulls[i]) - 1):
                linea = (hulls[i][j][0], hulls[i][j][1], hulls[i][j+1][0], hulls[i][j+1][1])
                drawing.line(linea)

    def action(self):
        f = self.open_image(self.image_file_path)
        f = grayscale(f)
        h = [[0, 1, 0], [1, -4, 1], [0, 1, 0]]

        image = self.convolution(h, f)
        image = average_allneighbors(image)
        image = average_allneighbors(image)
        image = binarization(image, 20)

        self.convex_hull(image)
        self.update_image(image)

def main():
    if len(sys.argv) > 0:
        image_file_path = sys.argv[1]
        if os.path.isfile(image_file_path):
            Convex(image_file_path)
        else:
            print 'Image file does not exist'
    else:
        print 'First parameter must be an image file name'

if __name__ == '__main__':
    main()

