import sys, time, Image, numpy, pywt

def load_image(image, effect, size=None):
    im = Image.open(image)
    if size is not None and im.size != size:
        im = im.resize(size, Image.ANTIALIAS)
    im = im.convert('RGB')
    if effect == 'sepia':
        im = sepia(im)
    return im

def sepia(image, sepia_intensity=25):
    width, height = image.size

    for w in range(width):
        for h in range(height):
            r, g, b = image.getpixel((w, h))
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
            image.putpixel((w, h), (r, g, b))
    return image

def image2array(image):
    assert image.mode in ('L', 'RGB', 'CMYK')
    arr = numpy.fromstring(image.tostring(), numpy.uint8)
    arr.shape = (image.size[1], image.size[0], len(image.getbands()))
    return arr.swapaxes(0, 2).swapaxes(1, 2).astype(numpy.float32)

def array2image(arr, mode):
    arr = arr.swapaxes(1, 2).swapaxes(0, 2)
    arr[arr < 0] = 0
    arr[arr > 255] = 255
    arr = numpy.fix(arr).astype(numpy.uint8)
    return Image.fromstring(mode, arr.shape[1::-1], arr.tostring())

def blend_images(base, texture, level=4, mode='sp1', base_gain=None, texture_gain=None):
    base_data = image2array(base)
    texture_data = image2array(texture)
    output_data = []

    for base_band, texture_band in zip(base_data, texture_data):
        base_band_coeffs = pywt.wavedec2(base_band, 'db2', mode, level)
        texture_band_coeffs = pywt.wavedec2(texture_band, 'db2', mode, level)

        output_band_coeffs = [base_band_coeffs[0]]
        del base_band_coeffs[0], texture_band_coeffs[0]

        for n, (base_band_details, texture_band_details) in enumerate(
            zip(base_band_coeffs, texture_band_coeffs)):
            blended_details = []
            for (base_detail, texture_detail) in zip(base_band_details, texture_band_details):
                if base_gain is not None:
                    base_detail *= base_gain
                if texture_gain is not None:
                    texture_detail *= texture_gain

                blended = numpy.where(abs(base_detail) > abs(texture_detail), base_detail, texture_detail)
                blended_details.append(blended)

            base_band_coeffs[n] = texture_band_coeffs[n] = None
            output_band_coeffs.append(blended_details)

        new_band = pywt.waverec2(output_band_coeffs, 'db2', mode)
        output_data.append(new_band)
        del new_band, base_band_coeffs, texture_band_coeffs

    del base_data, texture_data
    output_data = numpy.array(output_data)
    return array2image(output_data, base.mode)

def miximages(image, texture, output, effect):
    base = load_image(image, effect)
    texture = load_image(texture, effect, base.size)

    start_time = time.time()
    im = blend_images(base, texture)
    end_time = time.time()

    print end_time - start_time
    im.save(output)

def main():
    if len(sys.argv) > 3:
        image = str(sys.argv[1])
        texture = str(sys.argv[2])
        output = str(sys.argv[3])
        try:
            effect = str(sys.argv[4])
        except:
            effect = None
        miximages(image, texture, output, effect)
    else:
        print 'Missing arguments'

if __name__ == '__main__':
    main()

