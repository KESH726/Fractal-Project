import numpy as np
from PIL import Image, ImageTk, ImageOps

class FractalToPyGameMapper:
    def __init__(self):
        pass

    def pixel_to_symbol(self,value,low, high,mid):
        if value < low:
            return '*'  # Darker pixels
        elif value < mid:
            return ' '  # Medium brightness
        else:
            return '.'  # Lighter pixels

    def convert_grey_scale_image_to_np_array(self,grayscale_image):
        pixel_arr = np.zeros(grayscale_image.size, dtype=int)
        height,weight = grayscale_image.size
        for x in range(0,height):
            for y in range(0,weight):
                pixel_arr[x][y] = grayscale_image.getpixel((x,y))

        return pixel_arr

    def get_l_system_from_pixels(self,gray_scale_image):
        pixels = self.convert_grey_scale_image_to_np_array(gray_scale_image)
        distinct_pixels_value_array = np.unique(pixels)
        first_quartile = np.percentile(distinct_pixels_value_array,25)
        median = np.median(distinct_pixels_value_array)
        third_quartile = np.percentile(distinct_pixels_value_array,75)
        pixel_map = {}
        for x in distinct_pixels_value_array:
            pixel_map.update({x:self.pixel_to_symbol(x,first_quartile,third_quartile,median)})

        new_pixels = np.zeros(pixels.shape, dtype = str)

        print(np.unique(pixels))
        for idx,x in enumerate(pixels):
            for idx2, y in enumerate(x):
                new_pixels[idx,idx2] = pixel_map[y]

        text_arr = []
        for x in new_pixels:
            text_arr.append(''.join(i for i in x))

        # print(new_pixels)
        # for x in text_arr:
        #     print(x)

        self._text_arr = text_arr

    def mapcolor(self,iterations, max_iteration):
        colormap = (255 - iterations * 255 // max_iteration).astype(np.uint8)
        return np.stack([colormap, colormap // 2, colormap // 4], axis=-1)

    def get_pygame_mapper_matrics_from_fractal(self, fractal,max_iteration = 500):
        colors = self.mapcolor(fractal, max_iteration)
        img = Image.fromarray(colors, mode="RGB")
        img = ImageOps.grayscale(img)
        pixels = self.convert_grey_scale_image_to_np_array(img)
        distinct_pixels_value_array = np.unique(pixels)

        first_quartile = np.percentile(distinct_pixels_value_array,25)
        median = np.median(distinct_pixels_value_array)
        third_quartile = np.percentile(distinct_pixels_value_array,75)
        pixel_map = {}
        for x in distinct_pixels_value_array:
            pixel_map.update({x:self.pixel_to_symbol(x,first_quartile,third_quartile,median)})

        new_pixels = np.zeros(pixels.shape, dtype = str)

        print(np.unique(pixels))
        for idx,x in enumerate(pixels):
            for idx2, y in enumerate(x):
                new_pixels[idx,idx2] = pixel_map[y]

        return new_pixels