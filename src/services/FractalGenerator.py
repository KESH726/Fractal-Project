from src.services.DendriteFractal import DendriteFractal
from src.services.FractalType import FractalType

from PIL import Image, ImageOps
import numpy as np


'''
<h1>FractalGenerator</h1>
This class is responsible to generate coordinates of fractals using recursion and fractal formulas.
The data structure is binary tree

@:param x : value of the real number
@:param i : value of the imaginary number
@:param max_iteration iteration count for the fractal generation
@:param recursion_limit the limit of the fractal tree
@:param fractal_coord; it is the content of the generated fractal coord ; eatch fractal coord represents each node of
the binary tree also each fractal coord represents whole fractal
'''
class FractalGenerator:
    def __init__(self,x = -1.188, i = 0.305,max_iteration = 500,recursion_limit = 5, fractal_type = FractalType.DENDRITE):
        self.recursion_limit = recursion_limit
        self.x = x
        self.i = i
        self.max_iteration = max_iteration
        self.fractal_type = fractal_type

    def mapcolor(self,iterations, max_iteration):
        """Map the number of iterations to RGB values for coloring."""
        colormap = (255 - iterations * 255 // max_iteration).astype(np.uint8)
        return np.stack([colormap, colormap // 2, colormap // 4], axis=-1)


    def pixel_to_symbol(self,value,low, high,mid):
        if value < low:
            return '*'  # Darker pixels
        elif value < mid:
            return '_'  # Medium brightness
        else:
            return '.'  # Lighter pixels
    def convert_grey_scale_image_to_np_array(self,grayscale_image):
        pixel_arr = np.zeros(grayscale_image.size, dtype=int)
        height,weight = grayscale_image.size
        for x in range(0,height):
            for y in range(0,weight):
                pixel_arr[x][y] = grayscale_image.getpixel((x,y))

        return pixel_arr

    def convert_pixel_matrix_to_symbol_matrix(self,gray_scale_image):
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

        # text_arr = []
        # for x in new_pixels:
        #     text_arr.append(''.join(i for i in x))
        #
        # # print(new_pixels)
        # for x in text_arr:
        #     print(x)
        low_brightness_pixel_coord_list = list()
        mid_brightness_pixel_coord_list = list()
        high_brightness_pixel_coord_list = list()

        for idx, item1 in enumerate(new_pixels):
            for idx2, item2 in enumerate(item1):
                if new_pixels[idx,idx2] == "*":
                    low_brightness_pixel_coord_list.append((idx2,idx))
                elif new_pixels[idx,idx2] == "_":
                    mid_brightness_pixel_coord_list.append((idx2,idx))
                elif new_pixels[idx,idx2] == ".":
                    high_brightness_pixel_coord_list.append((idx2,idx))

        pixel_coord_mapper = {"*": low_brightness_pixel_coord_list,
                              "_": mid_brightness_pixel_coord_list,
                              ".": high_brightness_pixel_coord_list}
        return pixel_coord_mapper

    '''
    Gives pixel coord mapper like this structure:
    {
    "*": [(23,54)],
    "_": [(34,53)],
    ".": [(32,64)]
    }
    '''
    def generate_pixel_coord_mapper(self,height = 800, width = 800):
        fractal_generator_obj = None
        match(self.fractal_type):
            case FractalType.DENDRITE:
                fractal_generator_obj = DendriteFractal(x = self.x,i = self.i, max_iteration = self.max_iteration,height = height , width = width)

        fractal_pixels = fractal_generator_obj.generate()

        colors = self.mapcolor(fractal_pixels, self.max_iteration)
        img = Image.fromarray(colors, mode="RGB")
        img = ImageOps.grayscale(img)

        print(f"Printing teh the mapper : {self.convert_pixel_matrix_to_symbol_matrix(img)}")
        return self.convert_pixel_matrix_to_symbol_matrix(img)


if __name__ == "__main__":
    fractal_generator = FractalGenerator(x = -0.37, i = 0.6)
    fractal_generator.generate(height = 60, width = 60)