import numpy as np

class DendriteFractal:
    def __init__(self,x, i,max_iteration = 500, escape_radius = 2):
        self.x = x
        self.i = i
        self.x_min, self.x_max = -1.5, 1.5
        self.y_min, self.y_max = -1.5, 1.5
        self.width, self.height = 800, 800
        self.max_iteration = max_iteration
        self.escape_radius = escape_radius

    def set_max_iteration(self, max_iteration):
        self.max_iteration = max_iteration

    def generate_julia_set(self):
        x = np.linspace(self.x_min, self.x_max, self.width)
        y = np.linspace(self.y_min, self.y_max, self.height)
        zx, zy = np.meshgrid(x, y)

        c = complex(self.x, self.i)
        z = zx + 1j * zy
        fractal = np.zeros(z.shape, dtype=int)

        for i in range(self.max_iteration):
            mask = np.abs(z) < self.escape_radius
            z[mask] = z[mask]**2 + c
            fractal[mask] = i

        return fractal



if __name__ == "__main__":
    dendrite = DendriteFractal(0.334, .645)
    fract = dendrite.generate_julia_set()

    for x in fract:
        print(x)