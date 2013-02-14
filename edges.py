from Tkinter import *
import sys, os, time, Image, ImageTk
from filters_methods import *

class Edges:
    def __init__(self, image_file_path, w, h):
        self.image_file_path = image_file_path
        self.w = w
        self.h = h
        image = self.open_image(self.image_file_path)

        self.root = Tk()
        self.root.title('Edges')
        self.root.resizable(width=False, height=False)

        self.imagetk_original = self.convert_to_imagetk(image)
        self.imagetk_modified = self.imagetk_original

        self.label1 = Label(self.root, image=self.imagetk_original)
        self.label1.pack(side=LEFT)
        self.label2 = Label(self.root, image=self.imagetk_modified)
        self.label2.pack(side=LEFT)

        self.button1 = Button(text='Reset', width=10,
                              command=self.reset_image).pack()
        self.button2 = Button(text='Convolution', width=10,
                              command=self.action).pack()
        self.button_exit = Button(text='Exit', width=10,
                              command=self.root.destroy).pack()
        self.root.mainloop()

    def open_image(self, image_file_path):
        image = Image.open(image_file_path)
        image.thumbnail((self.w, self.h), Image.ANTIALIAS)
        return image

    def convert_to_imagetk(self, image):
        return ImageTk.PhotoImage(image)

    def reset_image(self):
        image = self.open_image(self.image_file_path)
        self.update_image(image)

    def update_image(self, image):
        self.imagetk_modified = self.convert_to_imagetk(image)
        self.label2.config(image=self.imagetk_modified)
        self.label2.pack()
        self.root.mainloop()

    def action(self):
        start = time.time()
        '''Abrimos la imagen en la cual vamos a buscar bordes
        y la convertimos a escala de grises.
        '''
        f = self.open_image(self.image_file_path)
        f = grayscale(f)

        '''Experimente con varias matrices para observar
        cuales daban mejor resultado y deje solo la que me
        parecio mas exacta.
        '''
        # bordes verticales
        #h = [[-1, -1, -1], [0, 0, 0], [1, 1, 1]]
        # bordes horizontales
        #h = [[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]]
        # resaltar bordes
        #h = [[0, 0, 0], [-1, 1, 0], [0, 0, 0]]
        # detectar bordes
        h = [[0, 1, 0], [1, -4, 1], [0, 1, 0]]

        '''Aqui mandamos llamar el metodo convolucion,
        del cual recibiremos la imagen con la mascara aplicada
        y luego aplicamos unos filtros mas para hacer los
        bordes mas notorios.
        '''
        image = self.convolution(h, f)
        image = average_allneighbors(image)
        image = black_and_white(image, 18)
        end = time.time()
        print end - start
        self.update_image(image)

    def convolution(self, h, f):
        '''Abrimos una imagen para aplicar en ella los cambios
        y no alterar la imagen de la cual se obtienen los datos.
        '''
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
                            #suma += f.getpixel((x+i, y+j))[0]*h[i][j]
                            suma += f.getpixel((x+z1, y+z2))[0]*h[i][j]
                        except:
                            pass
                suma = int(suma)
                F.putpixel((x, y), (suma, suma, suma))
        return F

def main():
    if len(sys.argv) > 3:
        image_file_path = sys.argv[1]
        w = int(sys.argv[2])
        h = int(sys.argv[3])
        if os.path.isfile(image_file_path):
            Edges(image_file_path, w, h)
        else:
            print 'Image file does not exist'
    else:
        print 'First parameter must be an image file name'

if __name__ == '__main__':
    main()

