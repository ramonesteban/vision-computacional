from Tkinter import *
import random, math, Image, ImageTk, ImageDraw
from filters_methods import *
SIZE = 300

class Corners:
    def __init__(self):
        image = Image.new('RGB', (SIZE, SIZE), (255, 255, 255))

        self.root = Tk()
        self.root.title('Corners')
        self.root.resizable(width=False, height=False)

        self.imagetk = self.convert_to_imagetk(image)

        self.label1 = Label(self.root, image=self.imagetk)
        self.label1.pack(side=LEFT)

        self.button1 = Button(text='Corners', width=10,
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

    def draw_some_polygons(self, polygons, image):
        draw = ImageDraw.Draw(image)
        max_w, max_h = get_image_size(image)

        for points in polygons:
            draw.polygon(points, fill=(50, 100, 150))
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
        polygons = []

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
                    polygons.append(copy)
        return polygons, image

    def median_filter(self, image):
        width, height = get_image_size(image)
        image = grayscale(image)
        pixels = image.load()
        newimage = image
        result = newimage.load()

        for x in range(width):
            for y in range(height):
                neighborhood = list()
                for pos_x in [-1, 0, 1]:
                    for pos_y in [-1, 0, 1]:
                        if pos_x != 0 or pos_y != 0:
                            pixel_x = x + pos_x
                            pixel_y = y + pos_y
                            if pixel_x >= 0 and pixel_x < width and pixel_y >= 0 and pixel_y < height:
                                neighborhood.append(pixels[pixel_x, pixel_y][0])
                n = int(len(neighborhood)/2)
                neighborhood.sort()
                median = (neighborhood[n] + neighborhood[n-1])/2
                result[x, y] = (median, median, median)
        return newimage

    def find_corners(self, original_image, image):
        corners = Image.new('RGB', (SIZE, SIZE), (255, 255, 255))
        width, height = get_image_size(corners)
        pixels = corners.load()
        oim = original_image.load()
        im = image.load()

        for i in range(width):
            for j in range(height):
                color = abs(oim[i, j][0] - im[i, j][0])
                pixels[i, j] = (color, color, color)
        corners = binarization(corners, 100)
        return corners

    def search_wires_frames(self, polygons, corners_points):
        wires_frames = []
        single_wire = []

        for polygon in polygons:
            for each_pixel in polygon:
                for pixels_in_corner in corners_points:
                    for cp in pixels_in_corner:
                        if cp[0] == each_pixel[0] and cp[1] == each_pixel[1]:
                            single_wire.append(cp)
                            break

            wires_frames.append(single_wire)
        return wires_frames

    def draw_wires_detected(self, image, wires_frames):
        draw = ImageDraw.Draw(image)
        counter = 1

        for wire_frame in wires_frames:
            print 'Polygon', counter
            r = random.randint(100, 255)
            g = random.randint(100, 255)
            b = random.randint(100, 255)
            for corner in wire_frame:
                x, y = corner
                draw.ellipse((x-3, y-3, x+3, y+3), fill=(r, g, b))
            counter += 1
        return image

    def action(self):
        original_image = Image.new('RGB', (SIZE, SIZE), (255, 255, 255))
        image = Image.new('RGB', (SIZE, SIZE), (255, 255, 255))

        #create_polygons = [(20,20,20,100,100,100,100,20), (120,120,120,180,180,180,180,120)]
        #create_polygons = [(20,20,20,100,100,100,100,20), (120,120,120,180,180,180,180,120), (160,20,190,20,190,50,160,50)]
        #create_polygons = [(70, 20, 40, 90, 80, 160, 160, 120, 180, 40)]
        #create_polygons = [(100, 30, 160, 70, 160, 120, 100, 160, 40, 120, 40, 70)]
        create_polygons = [(20,20,20,100,100,100,100,20), (120,120,120,180,180,180,180,120), (200, 200, 280, 250, 150, 290)]

        original_image = self.draw_some_polygons(create_polygons, original_image)
        original_image = grayscale(original_image)

        image = self.draw_some_polygons(create_polygons, image)
        image = grayscale(image)
        image = self.median_filter(image)

        corners_image = self.find_corners(original_image, image)
        corners_points, trash = self.detect_forms(corners_image)

        h = [[0, 1, 0], [1, -4, 1], [0, 1, 0]]
        original_image = average_allneighbors(original_image)
        original_image = binarization(original_image, 210)
        edges = self.convolution(h, original_image)
        polygons, image_bfs = self.detect_forms(edges)

        wires_frames = self.search_wires_frames(polygons, corners_points)
        output_image = self.draw_wires_detected(image_bfs, wires_frames)
        self.update_image(output_image)

def main():
    Corners()

if __name__ == '__main__':
    main()

