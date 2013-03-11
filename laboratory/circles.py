from Tkinter import *
import sys, os, random, math, Image, ImageTk, ImageDraw
from filters_methods import *

class Circles:
    def __init__(self):
        image = Image.new('RGB', (400, 400), (255, 255, 255))
        self.temp_image = image

        self.root = Tk()
        self.root.title('Circles')
        self.root.resizable(width=False, height=False)

        self.imagetk = self.convert_to_imagetk(image)

        self.label1 = Label(self.root, image=self.imagetk)
        self.label1.pack(side=LEFT)

        self.button1 = Button(text='Reset', width=10,
                              command=self.reset_image).pack()
        self.button2 = Button(text='Circles', width=10,
                              command=self.action).pack()
        self.button_exit = Button(text='Exit', width=10,
                              command=self.root.destroy).pack()
        self.action()
        self.root.mainloop()

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
        F = Image.new('RGB', (400, 400), (255, 255, 255))
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

    def draw_some_circles(self, radius_list, image):
        newdraw = ImageDraw.Draw(image)
        max_w, max_h = get_image_size(image)
        for radius in radius_list:
            x = random.randint(radius, max_w-radius)
            y = random.randint(radius, max_h-radius)
            newdraw.ellipse((x-radius, y-radius, x+radius, y+radius), fill=(0, 0, 255))
            print 'Drawed circle at center (%d, %d) and radius %d' % (x, y, radius)
        return image

    def draw_circles_found(self, image, circles_found):
        draw = ImageDraw.Draw(image)
        for i in range(len(circles_found)):
            x = circles_found[i][0]
            y = circles_found[i][1]
            r = circles_found[i][2]
            draw.ellipse((x-r, y-r, x+r, y+r), fill=None, outline=(255, 0, 0))
            draw.text((x, y), 'Circle '+str(i), fill='black')
        return image

    def search_circles(self, image, Gx, Gy):
        width, height = get_image_size(image)
        pixels_x = Gx.load()
        pixels_y = Gy.load()

        votes = list()
        for i in xrange(height):
            votes.append([0] * width)

        posible_radius = list()
        for i in xrange(height):
            posible_radius.append([0] * width)

        for radius in range(20, 70, 10):
            for ym in xrange(height):
                y = height / 2- ym
                for xm in xrange(width):
                    x = xm - width / 2
                    gx = pixels_x[ym, xm][0]
                    gy = pixels_y[ym, xm][0]
                    g = math.sqrt(gx ** 2 + gy ** 2)
                    if math.fabs(g) > 0:
                        cosTheta = gx / g
                        sinTheta = gy / g
                        xc = int(round(x - radius * cosTheta))
                        yc = int(round(y - radius * sinTheta))
                        xcm = xc + width / 2
                        ycm = height / 2 - yc
                        if xcm >= 0 and xcm < width and ycm >= 0 and ycm < height:
                            votes[ycm][xcm] += 1
                            posible_radius[xcm][ycm] = radius

        for try_range in xrange(1, 40):
            added = True
            while added:
                added = False
                for y in xrange(height):
                    for x in xrange(width):
                        v = votes[y][x]
                        if v > 0:
                            for dx in xrange(-20, 20):
                                for dy in xrange(-20, 20):
                                    if not (dx == 0 and dy == 0):
                                        if y + dy >= 0 and y + dy < height and x + dx >= 0 and x + dx < width:
                                            w = votes[y + dy][x + dx]
                                            if w > 0:
                                                if v - try_range >= w:
                                                    votes[y][x] = v + w
                                                    votes[y + dy][x + dx] = 0
                                                    added = True

        maximum = 0
        total = 0.0
        for x in xrange(width):
            for y in xrange(height):
                v = votes[y][x]
                total += v
                if v > maximum:
                    maximum = v

        average = total / (width * height)
        umbral = (maximum + average) / 2.0
        circles_found = list()
        for x in xrange(width):
            for y in xrange(height):
                v = votes[y][x]
                if v > umbral:
                    radius = posible_radius[x][y]
                    circles_found.append((y, x, radius))
                    print 'Center detected at (%d, %d)' % (y, x)
        return circles_found

    def action(self):
        image = Image.new('RGB', (400, 400), (255, 255, 255))
        image = self.draw_some_circles([20, 30, 25, 45, 50], image)
        image = grayscale(image)

        sobelx = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
        sobely = [[1, 2, 1], [0, 0, 0], [-1, -2, -1]]
        Gx = self.convolution(sobelx, image)
        Gy = self.convolution(sobely, image)

        circles_found = self.search_circles(image, Gx, Gy)
        image = self.draw_circles_found(image, circles_found)
        self.update_image(image)

def main():
    if len(sys.argv) > 0:
        Circles()
    else:
        print 'First parameter must be an image file name'

if __name__ == '__main__':
    main()

