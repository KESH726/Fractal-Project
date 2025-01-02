import numpy as np

class DendriteFractal:
    def __init__(self, x, i, max_iteration=500, escape_radius=2, height=800, width=800):
        self.x = x
        self.i = i
        self.x_min, self.x_max = -1.5, 1.5
        self.y_min, self.y_max = -1.5, 1.5
        self.width, self.height = width, height
        self.max_iteration = max_iteration
        self.escape_radius = escape_radius

    def set_max_iteration(self, max_iteration):
        self.max_iteration = max_iteration

    def generate(self):
        x = np.linspace(self.x_min, self.x_max, self.width)
        y = np.linspace(self.y_min, self.y_max, self.height)
        zx, zy = np.meshgrid(x, y)

        c = complex(self.x, self.i)
        z = zx + 1j * zy
        fractal = np.zeros(z.shape, dtype=int)

        def recursive_calculate(z, fractal, iteration):
            if iteration >= self.max_iteration:
                return fractal

            mask = np.abs(z) < self.escape_radius
            fractal[mask] = iteration
            z[mask] = z[mask]**2 + c

            return recursive_calculate(z, fractal, iteration + 1)

        fractal = recursive_calculate(z, fractal, 0)
        return fractal

# def mapcolor(iterations, max_iteration):
#     colormap = (255 - iterations * 255 // max_iteration).astype(np.uint8)
#     return np.stack([colormap, colormap // 2, colormap // 4], axis=-1)

if __name__ == "__main__":
    dendrite = DendriteFractal(-0.334, .645)
    fract = dendrite.generate()

    # from PIL import Image
    #
    # colors = mapcolor(fract, 500)
    # img = Image.fromarray(colors, mode="RGB")
    # img.show(title="Test image")

    for x in fract:
        print(x)
