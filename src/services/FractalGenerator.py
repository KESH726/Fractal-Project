
'''
<h1>FractalGenerator</h1>
This class is responsible to generate coordinates of fractals using recursion and fractal formulas.
@:param x : value of the real number
@:param i : value of the imaginary number
'''
class FractalGenerator:
    def __init__(self,x, i,max_iteration = 500):
        self.x = x
        self.i = i
        self.max_iteration = max_iteration

    def set_max_iteration(self, max_iteration):
        self.max_iteration = max_iteration

    def generate_julia_set(self,max_iteration, escape_radius):
        x = np.linspace(x_min, x_max, width)
        y = np.linspace(y_min, y_max, height)
        zx, zy = np.meshgrid(x, y)

        c = complex(self.x, self.i)
        z = zx + 1j * zy
        fractal = np.zeros(z.shape, dtype=int)

        for i in range(max_iteration):
            mask = np.abs(z) < escape_radius
            z[mask] = z[mask]**2 + c
            fractal[mask] = i

        return fractal



