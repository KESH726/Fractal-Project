from src.services.DendriteFractal import DendriteFractal


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
    def __init__(self,x = -1.188, i = 0.305,max_iteration = 500,recursion_limit = 5,fractal_coord = None):
        self.recursion_limit = recursion_limit
        self.fractal_generator = DendriteFractal(x,i, max_iteration)
        self.left = None
        self.right = None
        self.fractal_coord = fractal_coord

    def set_max_iteration(self, max_iteration):
        self.max_iteration = max_iteration

    def _add_new_fractal_coord(self, fractal_coord):
        self.fractal_coord = fractal_coord

    def generate_fractal_tree(self,fractal_coord):
        if self.left == None and self.right == None and self.fract_coord == None:
            self.fractal_coord = self.generate_fractal_tree(self.fractal_generator.generate_julia_set())







    def get_fractal_coord_tree_as_json(self):
        pass

    def get_fractal_coord_tree_as_obj(self):
        pass

    '''
    Since the recursion has limit we need to make sure that there are a specific amount of recursion happening based on the limit. 
    So each time we need more recursion we could always generate further that would further append more node to the existing binary tree
    '''
    def generate_further(self):
        pass