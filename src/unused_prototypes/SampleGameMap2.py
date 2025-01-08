import pygame, sys
from random import randint

from DendriteFractal import DendriteFractal
from FractalToPyGameMapper import FractalToPyGameMapper


game_window_dimension = (800,800)

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

class Tree(pygame.sprite.Sprite):
    def __init__(self,pos,group):
        super().__init__(group)
        self.image = pygame.image.load('../assets/tree.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.image = pygame.image.load('../assets/player.png').convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        self.direction = pygame.math.Vector2()
        self.speed = 5
    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0



    def update(self):
        self.input()
        self.rect.center += self.direction * self.speed

def generate_pygame_landscape_from_map_matrix(map_matrix):
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



def get_ground_surface():
    fractal = DendriteFractal(-0.37,0.6,game_window_dimension[0],game_window_dimension[1])
    fract = fractal.generate_julia_set()
    fractal_pygame_mapper = FractalToPyGameMapper()
    fractal_pygame_map_matrix = fractal_pygame_mapper.get_pygame_mapper_matrics_from_fractal(fract)

    map_grp =generate_pygame_landscape_from_map_matrix(fractal_pygame_map_matrix)
    ground_surf = pygame.Surface((game_window_dimension))
    ground_surf.fill("#71ddee")

    map_grp.draw(ground_surf)

    return ground_surf

# makes it so that the tree appears behind the player
class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        #camera offset
        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

        #box setup
        self.camera_borders = {'left': 200, 'right': 200, 'top': 100, 'bottom': 100}
        l = self.camera_borders['left']
        t = self.camera_borders['top']
        w = self.display_surface.get_size()[0] - (self.camera_borders['left'] + self.camera_borders['right'])
        h = self.display_surface.get_size()[1] - (self.camera_borders['top'] + self.camera_borders['bottom'])
        self.camera_rect = pygame.Rect(l,t,w,h)

        # ground
        # self.ground_surf = pygame.image.load('ground.png').convert_alpha() # update
        # self.ground_rect = self.ground_surf.get_rect(topleft = (0,0)) # update
        self.ground_surf = get_ground_surface()
        self.ground_rect = self.ground_surf.get_rect(topleft = (0,0))

        #camera speed
        self.keyboard_speed = 5
        self.mouse_speed = 0.2

        # zoom
        self.zoom_scale = 1
        self.internal_surf_size = (800,800)
        self.internal_surf = pygame.Surface(self.internal_surf_size, pygame.SRCALPHA)
        self.internal_rect = self.internal_surf.get_rect(center = (self.half_w,self.half_h))
        self.internal_surface_size_vector = pygame.math.Vector2(self.internal_surf_size)
        self.internal_offset = pygame.math.Vector2()
        self.internal_offset.x = self.internal_surf_size[0] // 2 - self.half_w
        self.internal_offset.y = self.internal_surf_size[1] // 2 - self.half_h


    def center_target_camera(self,target):
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h

    def box_target_camera(self,target):
        if target.rect.left < self.camera_rect.left:
            self.camera_rect.left = target.rect.l
        if target.rect.right > self.camera_rect.right:
            self.camera_rect.right = target.rect.ri
        if target.rect.top < self.camera_rect.top:
            self.camera_rect.top = target.rect.top
        if target.rect.bottom > self.camera_rect.bottom:
            self.camera_rect.bottom = target.rect.bottom

        self.offset.x = self.camera_rect.left - self.camera_borders['left']
        self.offset.y = self.camera_rect.top - self.camera_borders['top']

    def keyboard_control(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]: self.camera_rect.x -= self.keyboard_speed
        if keys[pygame.K_d]: self.camera_rect.x += self.keyboard_speed
        if keys[pygame.K_w]: self.camera_rect.y -= self.keyboard_speed
        if keys[pygame.K_s]: self.camera_rect.y += self.keyboard_speed

        self.offset.x = self.camera_rect.left - self.camera_borders['left']
        self.offset.y = self.camera_rect.top - self.camera_borders['top']

    # the mouse borders and what the screen will do when it the mouse moves outside of the border
    def mouse_control(self):
        mouse = pygame.math.Vector2(pygame.mouse.get_pos())
        mouse_offset_vector = pygame.math.Vector2()

        left_border = self.camera_borders['left']
        top_border = self.camera_borders['top']
        right_border = self.display_surface.get_size()[0] - self.camera_borders['right']
        bottom_border = self.display_surface.get_size()[1] - self.camera_borders['bottom']

        if top_border < mouse.y < bottom_border:
            if mouse.x < left_border:
                mouse_offset_vector.x = mouse.x - left_border
                pygame.mouse.set_pos((left_border,mouse.y))
            if mouse.x > right_border:
                mouse_offset_vector.x = mouse.x - right_border
                pygame.mouse.set_pos((right_border,mouse.y))
        elif mouse.y < top_border:
            if mouse.x < left_border:
                mouse_offset_vector = mouse - pygame.math.Vector2(left_border,top_border)
                pygame.mouse.set_pos((left_border,top_border))
            if mouse.x > right_border:
                mouse_offset_vector = mouse - pygame.math.Vector2(right_border,top_border)
                pygame.mouse.set_pos((right_border,top_border))
        elif mouse.y > bottom_border:
            if mouse.x < left_border:
                mouse_offset_vector = mouse - pygame.math.Vector2(left_border,bottom_border)
                pygame.mouse.set_pos((left_border,bottom_border))
            if mouse.x > right_border:
                mouse_offset_vector = mouse - pygame.math.Vector2(right_border,bottom_border)
                pygame.mouse.set_pos((right_border,bottom_border))

        if left_border < mouse.x < right_border:
            if mouse.y < top_border:
                mouse_offset_vector.y = mouse.y - top_border
                pygame.mouse.set_pos((mouse.x,top_border))
            if mouse.y > bottom_border:
                mouse_offset_vector.y = mouse.y - bottom_border
                pygame.mouse.set_pos((mouse.x,bottom_border))

        self.offset += mouse_offset_vector * self.mouse_speed

    def zoom_keyboard_control(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            self.zoom_scale += 0.01
        if keys[pygame.K_e]:
            self.zoom_scale -= 0.01

    def custom_draw(self, player):
        self.mouse_control()
        self.zoom_keyboard_control()

        self.internal_surf.fill('#71ddee')

        # ground
        ground_offset = self.ground_rect.topleft - self.offset + self.internal_offset
        self.internal_surf.blit(self.ground_surf,ground_offset)

        # active elements
        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset + self.internal_offset
            self.internal_surf.blit(sprite.image,offset_pos)

        scaled_surf = pygame.transform.scale(self.internal_surf,self.internal_surface_size_vector * self.zoom_scale)
        scaled_rect = scaled_surf.get_rect(center = (self.half_w,self.half_h))

        self.display_surface.blit(scaled_surf,scaled_rect)

pygame.init()
screen = pygame.display.set_mode((500,500))
clock = pygame.time.Clock()

#setup for camera and trees

camera_group = CameraGroup()
player = Player((640,360),camera_group)

# amount of trees placed
for i in range(20):
    random_x = randint(0, 1000)
    random_y = randint(0, 1000)
    Tree((random_x, random_y),camera_group)


#update game events
#just to quit the application
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill('#71ddee')

    camera_group.update()
    camera_group.custom_draw(player)

    pygame.display.update()
    clock.tick(60)