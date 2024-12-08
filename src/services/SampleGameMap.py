import pygame,sys
from random import randint
from concurrent.futures import ThreadPoolExecutor
from threading import Lock


from DendriteFractal import DendriteFractal
from FractalToPyGameMapper import  FractalToPyGameMapper
pygame.init()
game_window_dimension = (800,800)
screen = pygame.display.set_mode((850,850))
pygame.display.set_caption("Hello World")

img = pygame.image.load("Character.png")

done = False
bg = (127,127,35)

font = pygame.font.SysFont("Arial", 36)
text_surface = font.render("hello world ",True,(0,123,43))
# def draw_soil():
#
#     soil = pygame.image.load("533.jpg")
#
#     rect = soil.getrect()
#     rect.center = 500,300
#     screen.blit(soil_skin,rect)

class Soil(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("../assets/soil_grass_pack/dirt1.png")
        self.image = pygame.transform.scale(self.image,(2,2))
        self.rect = self.image.get_rect()
        # self.rect.topleft = (x,y)



class Grass(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("../assets/soil_grass_pack/grass1.png")
        self.image = pygame.transform.scale(self.image,(2,2))
        self.rect = self.image.get_rect()

    # def draw(self,x,y,screen_):
    #     screen_.blit(self.image,(x,y))

class Water(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((2,2))
        img = pygame.image.load("../assets/water_class.png").convert_alpha()
        self.image.blit(img,(0,0),(407,510,140,140))
        self.image.set_colorkey((31,26,23))

        pygame.transform.scale(self.image,(2,2))

        self.rect = self.image.get_rect()

fractal = DendriteFractal(-0.37,0.6,game_window_dimension[0],game_window_dimension[1])
fract = fractal.generate_julia_set()
fractal_pygame_mapper = FractalToPyGameMapper()
fractal_pygame_map_matrix = fractal_pygame_mapper.get_pygame_mapper_matrics_from_fractal(fract)

def generate_pygame_landscape_from_map_matrix(map_matrix,screen_):
    height,width = map_matrix.shape
    map_group = pygame.sprite.Group()
    height,width = game_window_dimension
    for y in range(0,height):
        for x in range(0,width):
            # print(f"Printing the value of mat {map_matrix[y,x]}")
            if map_matrix[y,x] == ".":
                # print("Brightness found ")
                # high brightness
                grass = Grass()
                grass.rect.x = x
                # print(f"printing coord : {x*100}, {y*100}")
                grass.rect.y = y
                # print(f"grass.rect : {grass.rect.x}, {grass.rect.y}")
                map_group.add(grass)

            elif map_matrix[y,x] == " ":
                # mid brightness

                water = Water()
                water.rect.x = x
                water.rect.y = y
                map_group.add(water)
            elif map_matrix[y,x] == "*":
                # low brightness
                # print("low Brightness found ")
                soil = Soil()
                soil.rect.x = x
                soil.rect.y = y
                soil_group = pygame.sprite.Group()
                map_group.add(soil)

    return map_group





clock = pygame.time.Clock()
map_grp =generate_pygame_landscape_from_map_matrix(fractal_pygame_map_matrix,screen)
while True:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            done = True

        if event.type == pygame.K_DOWN:
            rect.center = 350, 250

    screen.fill(bg)
    rect = img.get_rect()
    rect.center = 200, 150
    screen.blit(img, rect)
    screen.blit(text_surface,(200 - text_surface.get_width() // 2, 150 - text_surface.get_height() // 2))
    # soil = Soil(100,100)
    # soil.rect.x = 100
    # grass = Grass()
    # water = Water(300,150)

    # screen.blit(soil,soil.get_rect())
    # soil_group = pygame.sprite.Group()
    # soil_group.add(soil)
    # soil_group.draw(screen)
    #
    # grass_group = pygame.sprite.Group()
    # grass_group.add(grass)
    # grass_group.draw(screen)
    #
    # water_group = pygame.sprite.Group()
    # water_group.add(water)
    # water_group.draw(screen)
    # map_grp =generate_pygame_landscape_from_map_matrix(fractal_pygame_map_matrix,screen)

    # map_grp.draw(screen)

    # height,width = fractal_pygame_map_matrix.shape
    # grp = pygame.sprite.Group()
    # for y in range(0,randint(10,100)):
    #     for x in range(0,randint(10,100)):
    #
    #         grass = Grass()
    #         grass.rect.x = x
    #         grass.rect.y = y
    #         grp.add(grass)

    # grass = Grass()
    # grass.rect.x = 100
    # grass.rect.y = 100
    # grp.add(grass)
    # grp.draw(screen)

    map_grp.draw(screen)

    pygame.display.update()
    clock.tick(60)