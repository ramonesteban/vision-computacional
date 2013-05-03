from Tkinter import *
import random, math, Image, ImageTk, ImageDraw
from filters_methods import *
SIZE = 200

class Polygons:
    def __init__(self):
        image = Image.new('RGB', (SIZE, SIZE), (255, 255, 255))

        self.root = Tk()
        self.root.title('Polygons')
        self.root.resizable(width=False, height=False)

        self.imagetk = self.convert_to_imagetk(image)

        self.label1 = Label(self.root, image=self.imagetk)
        self.label1.pack(side=LEFT)

        self.button1 = Button(text='Polygons', width=10,
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

    def what_polygon(self, sides):
        if sides == 3:
            print 'It should be a Triangle'
        elif sides == 4:
            print 'It should be a Square'
        elif sides == 5:
            print 'It should be a Pentagon'
        elif side == 6:
            print 'It should be a Hexagon'
        else:
            print 'This polygon have more than 6 sides'

    def draw_some_polygons(self, polygons, image):
        draw = ImageDraw.Draw(image)
        max_w, max_h = get_image_size(image)

        for points in polygons:
            draw.polygon(points, outline=(0, 0, 0), fill=(100, 150, 200))
        return image

    def draw_polygons_detected(self, image, polygons_found):
        draw = ImageDraw.Draw(image)
        max_w, max_h = get_image_size(image)
        counter = 0

        for polygon in polygons_found:
            center, sides = polygon
            x, y = center
            r = random.randint(100, 255)
            g = random.randint(100, 255)
            b = random.randint(100, 255)
            image, count, copy = self.bfs(image, center, (r, g, b))
            percentage = (count * 100.0)/(max_w*max_h)
            print 'Whit the %0.2f%% of all the image' % percentage

            print 'Polygon %d detected at center (%d, %d)' % (counter, x, y)
            self.what_polygon(sides)
            draw.ellipse((x-2, y-2, x+2, y+2), fill=(255, 255, 0), outline=(255, 255, 0))
            draw.text((x+5, y), 'Poly '+str(counter), fill=(255, 0, 0))
            counter += 1
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
        can_be_polygons = []

        for i in range(width):
            for j in range(height):
                if pixels[i, j] == (255, 255, 255):
                    r = random.randint(100, 255)
                    g = random.randint(100, 255)
                    b = random.randint(100, 255)
                    image, count, copy = self.bfs(image, (i, j), (r, g, b))
                    per = float(count)/float(width * height)
                    percentages.append(per)
                    all_colors.append((r, g, b))
                    pixels = image.load()
                    can_be_polygons.append(copy)
        return can_be_polygons, image

    def search_polygon(self, can_be_polygons, image, Gx, Gy):
        width, height = get_image_size(image)
        pixels_gx = Gx.load()
        pixels_gy = Gy.load()
        points_orientation = []
        polygons_found = []

        for i in range(width):
            points_orientation.append([0] * height)

        for polygon in can_be_polygons:
            pixels = image.load()
            for point in polygon:
                px, py = point
                color_of_the_ploygon = pixels[px, py]
                gx = pixels_gx[px-1, py][0]
                gy = pixels_gy[px, py+1][0]

                if abs(gx) + abs(gy) <= 0:
                    theta = None
                else:
                    theta = math.atan2(gy, gx)
                    points_orientation[px][py] = theta

            lines, image = self.detect_lines(image, color_of_the_ploygon, points_orientation)

            filtered_lines = []
            for line in lines:
                if len(line) > 5:
                    # save true line segemnt
                    filtered_lines.append(line)
                else:
                    # delete false line segment
                    for point in line:
                        pixels[point] = (0, 0, 0)

            for line in filtered_lines:
                px1, py1 = line[0]
                px2, py2 = line[-1]
                px = (px1+px2)/2
                py = (py1+py2)/2
                dis = math.sqrt((px2-px1)**2+(py2-py1)**2)
                dis_to_move = dis/2

                theta = points_orientation[px][py]
                x0 = px - dis * math.cos(theta)
                y0 = py - dis * math.sin(theta)
                x1 = px + dis * math.cos(theta)
                y1 = py + dis * math.sin(theta)

                draw = ImageDraw.Draw(image)
                #draw.line((x0, y0, x1, y1), fill=(255, 255, 0))

                for point in line:
                    x, y = point
                    color = pixels[x, y]
                    pixels[x, y] = (0, 0, 0)
                    if theta > 0:
                        try: pixels[x, y+dis_to_move] = color
                        except: pass
                        try: pixels[x, y-dis_to_move] = color
                        except: pass
                    else:
                        try: pixels[x+dis_to_move, y] = color
                        except: pass
                        try: pixels[x-dis_to_move, y] = color
                        except: pass

                image.save('output.png', 'png')
            polygons_found.append(((px-dis_to_move, py), len(filtered_lines)))
        return image, polygons_found

    def detect_lines(self, image, color_of_the_ploygon, points_orientation):
        width, height = get_image_size(image)
        pixels = image.load()
        lines = []

        for i in range(width):
            for j in range(height):
                if pixels[i, j] == color_of_the_ploygon:
                    r = random.randint(100, 255)
                    g = random.randint(100, 255)
                    b = random.randint(100, 255)
                    image, line_points = self.line_segment(image, (i, j), (r, g, b), points_orientation)
                    lines.append(line_points)
                    pixels = image.load()
        return lines, image

    def line_segment(self, image, start_pixel_pos, color, points_orientation):
        width, height = get_image_size(image)
        pixels = image.load()
        queue = []
        copy = []
        queue.append(start_pixel_pos)
        original = pixels[start_pixel_pos]
        orientation_original = points_orientation[start_pixel_pos[0]][start_pixel_pos[1]]

        while 0 < len(queue):
            (x, y) = queue.pop(0)
            current = pixels[x, y]
            if current == original or current == color:
                for pos_x in [-1, 0, 1]:
                    for pos_y in [-1, 0, 1]:
                        pixel_x = x + pos_x
                        pixel_y = y + pos_y
                        if pixel_x >= 0 and pixel_x < width and pixel_y >= 0 and pixel_y < height:
                            if pixels[pixel_x, pixel_y] == original and orientation_original == points_orientation[pixel_x][pixel_y]:
                                pixels[pixel_x, pixel_y] = color
                                queue.append((pixel_x, pixel_y))
                                copy.append((pixel_x, pixel_y))
        return image, copy

    def action(self):
        original_image = Image.new('RGB', (SIZE, SIZE), (255, 255, 255))
        #create_polygons = [(40, 40, 40, 160, 160, 160, 160, 40)]
        #create_polygons = [(20,20,20,100,100,100,100,20), (120,120,120,180,180,180,180,120)]
        create_polygons = [(20,20,20,100,100,100,100,20), (120,120,120,180,180,180,180,120), (160,20,190,20,190,50,160,50)]
        original_image = self.draw_some_polygons(create_polygons, original_image)
        #original_image.save('original.png', 'png')
        original_image = grayscale(original_image)

        # detect all the edges
        h = [[0, 1, 0], [1, -4, 1], [0, 1, 0]]
        image = self.convolution(h, original_image)
        can_be_polygons, image_bfs = self.detect_forms(image)

        # gradient
        sobely = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
        sobelx = [[1, 2, 1], [0, 0, 0], [-1, -2, -1]]
        Gx = self.convolution(sobelx, original_image)
        Gy = self.convolution(sobely, original_image)
        #Gx.save('gx.png', 'png')
        #Gy.save('gy.png', 'png')

        image, polygons_found = self.search_polygon(can_be_polygons, image_bfs, Gx, Gy)
        image = self.draw_polygons_detected(original_image, polygons_found)
        #image.save('polygons.png', 'png')
        self.update_image(image)

def main():
    Polygons()

if __name__ == '__main__':
    main()

