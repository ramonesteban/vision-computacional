from Tkinter import *
import random, math, Image, ImageTk, ImageDraw
from filters_methods import *
SIZE = 200

class Ellipses:
    def __init__(self):
        image = Image.new('RGB', (SIZE, SIZE), (255, 255, 255))

        self.root = Tk()
        self.root.title('Ellipses')
        self.root.resizable(width=False, height=False)

        self.imagetk = self.convert_to_imagetk(image)

        self.label1 = Label(self.root, image=self.imagetk)
        self.label1.pack(side=LEFT)

        self.button1 = Button(text='Ellipses', width=10,
                              command=self.action).pack()
        self.button_exit = Button(text='Exit', width=10,
                              command=self.root.destroy).pack()
        self.action()
        self.root.mainloop()

    def convert_to_imagetk(self, image):
        return ImageTk.PhotoImage(image)

    def update_image(self, image):
        self.imagetk = self.convert_to_imagetk(image)
        self.label1.config(image=self.imagetk)
        self.label1.pack()
        self.root.mainloop()

    def draw_some_ellipses(self, ellipses, image):
        newdraw = ImageDraw.Draw(image)
        max_w, max_h = get_image_size(image)

        for ellipse in ellipses:
            xdim, ydim, x, y = ellipse
            newdraw.ellipse((x-xdim, y-ydim, x+xdim, y+ydim), outline=(0, 0, 0), fill=(0, 0, 0))
        return image

    def convolution(self, h, f):
        F = Image.new('RGB', (SIZE, SIZE), (255, 255, 255))
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
                                queue.append((pixel_x, pixel_y))
                                copy.append((pixel_x, pixel_y))
                                count += 1
        return image, count, copy

    def detect_forms(self, image):
        pixels = image.load()
        width, height = get_image_size(image)
        percentages = []
        all_colors = []
        can_be_ellipses = []

        for i in range(width):
            for j in range(height):
                if pixels[i, j] == (255, 255, 255):
                    r = random.randint(150, 255)
                    g = random.randint(150, 255)
                    b = random.randint(150, 255)
                    image, count, copy = self.bfs(image, (i, j), (r, g, b))
                    per = float(count)/float(width * height)
                    percentages.append(per)
                    all_colors.append((r, g, b))
                    pixels = image.load()
                    can_be_ellipses.append(copy)
        return can_be_ellipses, image

    def search_ellipse(self, can_be_ellipses, image, Gx, Gy):
        width, height = get_image_size(image)
        pixels_gx = Gx.load()
        pixels_gy = Gy.load()
        l = 80
        ellipses_found = []

        for ellipse in can_be_ellipses:
            pixels = image.load()
            votes = []

            for i in range(width):
                votes.append([0] * height)

            for i in range(100):
                P1 = random.choice(ellipse)
                P2 = random.choice(ellipse)
                px1 = P1[0]
                py1 = P1[1]
                px2 = P2[0]
                py2 = P2[1]

                Mx = (px1 + px2)/2
                My = (py1 + py2)/2

                gx1 = pixels_gx[px1, py1][0]
                gy1 = pixels_gy[px1, py1][0]
                gx2 = pixels_gx[px2, py2][0]
                gy2 = pixels_gy[px2, py2][0]

                if abs(gx1) + abs(gy1) <= 0:
                    theta = None
                else:
                    theta = math.atan2(gy1, gx1)
                    theta -= math.pi/2
                    x0 = px1 - l * math.cos(theta)
                    y0 = py1 - l * math.sin(theta)
                    x1 = px1 + l * math.cos(theta)
                    y1 = py1 + l * math.sin(theta)

                if abs(gx2) + abs(gy2) <= 0:
                    theta = None
                else:
                    theta = math.atan2(gy2, gx2)
                    theta -= math.pi/2
                    x2 = px2 - l * math.cos(theta)
                    y2 = py2 - l * math.sin(theta)
                    x3 = px2 + l * math.cos(theta)
                    y3 = py2 + l * math.sin(theta)

                try:
                    Tx = ((x0*y1-y0*x1)*(x2-x3)-(x0-x1)*(x2*y3-y2*x3))/((x0-x1)*(y2-y3)-(y0-y1)*(x2-x3))
                    Ty = ((x0*y1-y0*x1)*(y2-y3)-(y0-y1)*(x2*y3-y2*x3))/((x0-x1)*(y2-y3)-(y0-y1)*(x2-x3))
                    Kx = Tx - Mx
                    Ky = Ty - My
                    m = Ky/Kx
                    x0 = Mx
                    y0 = My
                    while True:
                        x = int(x0 + 1)
                        y = int(m*(x - x0) + y0)
                        if pixels[x, y] == (0, 0, 0):
                            votes[x][y] += 1
                            x0 = x
                            y0 = y
                        else:
                            break
                except:
                    pass

            morevotes = 0
            for x in range(width):
                for y in range(height):
                    v = votes[x][y]
                    if v > morevotes:
                        morevotes = v
                        center_x = x
                        center_y = y

            for coord in ellipse:
                x, y = coord
                if center_x == x:
                    ydiameter = abs(center_y - y)
                if center_y == y:
                    xdiameter = abs(center_x - x)

            ellipses_found.append((center_x, center_y, xdiameter, ydiameter))
        return ellipses_found

    def draw_ellipses_found(self, image, ellipses_found):
        draw = ImageDraw.Draw(image)
        max_w, max_h = get_image_size(image)
        counter_circle = 1
        counter_ellipse = 1

        for ellipse in ellipses_found:
            x, y, xd, yd = ellipse
            r = random.randint(100, 255)
            g = random.randint(100, 255)
            b = random.randint(100, 255)
            image, count, copy = self.bfs(image, (x, y), (r, g, b))
            percentage = (count * 100)/(SIZE**2)
            if abs(xd - yd) < 20:
                print '\nCircle %d detected at center (%d, %d)' % (counter_circle, x, y)
                print '> Radio', xd
                print '> %.1f%% of all the image' % percentage
                draw.ellipse((x-xd, y-xd, x+xd, y+xd), outline=(0, 150, 255), fill=None)
                draw.ellipse((x-1, y-1, x+1, y+1), fill=(255, 255, 0), outline=(255, 255, 0))
                draw.text((x-20, y-15), 'Circle '+str(counter_circle), fill=(255, 100, 0))
                counter_circle += 1
            else:
                print '\nEllipse %d detected at center (%d, %d)' % (counter_ellipse, x, y)
                print '> Semidiameters:', xd, yd
                print '> %.1f%% of all the image' % percentage
                draw.ellipse((x-xd, y-yd, x+xd, y+yd), outline=(0, 150, 255), fill=None)
                draw.ellipse((x-2, y-2, x+2, y+2), fill=(255, 255, 0), outline=(255, 255, 0))
                draw.text((x-20, y-15), 'Ellipse '+str(counter_ellipse), fill=(255, 100, 0))
                counter_ellipse += 1
        return image

    def action(self):
        original_image = Image.new('RGB', (SIZE, SIZE), (255, 255, 255))
        original_image = self.draw_some_ellipses([(70, 30, 80, 50), (40, 40, 150, 150)], original_image)
        original_image = grayscale(original_image)

        # detect all the edges
        h = [[0, 1, 0], [1, -4, 1], [0, 1, 0]]
        image = self.convolution(h, original_image)
        image.save('original.png', 'png')
        can_be_ellipses, image_bfs = self.detect_forms(image)

        # gradient
        sobely = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
        sobelx = [[1, 2, 1], [0, 0, 0], [-1, -2, -1]]
        Gx = self.convolution(sobelx, original_image)
        Gy = self.convolution(sobely, original_image)

        image_bfs = average_allneighbors(image_bfs)
        image_bfs.save('bfs.png', 'png')
        ellipses_found = self.search_ellipse(can_be_ellipses, image_bfs, Gx, Gy)
        image = self.draw_ellipses_found(original_image, ellipses_found)
        image.save('result.png', 'png')
        self.update_image(image)

def main():
    Ellipses()

if __name__ == '__main__':
    main()

