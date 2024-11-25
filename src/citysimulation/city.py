import pygame
from math import sqrt

coordinates = [
    # Horizontal Roads
    ((50, 100), (250, 100)),
    ((300, 200), (600, 200)),
    ((100, 300), (400, 300)),
    ((450, 400), (750, 400)),
    ((200, 500), (500, 500)),

    # Vertical Roads
    ((100, 50), (100, 250)),
    ((250, 150), (250, 450)),
    ((400, 100), (400, 350)),
    ((550, 200), (550, 500)),
    ((700, 50), (700, 250)),

    # Diagonal Roads
    ((50, 50), (200, 200)),
    ((250, 100), (400, 250)),
    ((150, 400), (300, 550)),
    ((500, 50), (650, 200)),
    ((350, 300), (500, 450)),
    ((600, 400), (750, 550)),
    ((100, 600), (250, 750)),
    ((400, 500), (550, 650)),
    ((200, 250), (350, 400)),
    ((650, 150), (800, 300))
]

class Road:
    def __init__(self, start_pos, end_pos, width=10):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.width = width
        self.color = (128,128,128)
    
    def draw(self, screen):
        pygame.draw.line(screen, self.color, self.start_pos, self.end_pos, self.width)
    
    def get_length(self):
        x1, y1 = self.start_pos
        x2, y2 = self.end_pos

        return sqrt((x2-x1)**2 + (y2-y1)**2)


class Car:
    def __init__(self, current_road, speed=2):
        self.current_road = current_road
        self.speed = speed
        self.pos = current_road.start_pos
        self.progress = 0  # 0 to 1, representing position along current road
        self.color = (255, 0, 0)  # Red car
    
    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, (self.pos[0]-10, self.pos[1]-5, 20, 10))

    def update(self):
        self.progress += self.speed / self.current_road.get_length()
        if self.progress >= 1:
            self.progress = 1  # You'll handle road switching in your pathfinding
            
        # Interpolate position
        start_x, start_y = self.current_road.start_pos
        end_x, end_y = self.current_road.end_pos
        self.pos = (
            start_x + (end_x - start_x) * self.progress,
            start_y + (end_y - start_y) * self.progress
        )


class RoadNetwork:
    _car_list = []
    _road_list = []

    def __init__(self, roads_coordinates):
        self.roads_coordinates = roads_coordinates
    
    def create_roads(self):
        for road_coordinate in self.roads_coordinates:
            RoadNetwork._road_list.append(Road((road_coordinate[0]),(road_coordinate[1])))

    def create_cars(self):
        for road in self._road_list:
            new_car = Car(road, 0.5)
            self._car_list.append(new_car)
    
    def draw_and_update(self, screen):
        for road in self._road_list:
            road.draw(screen)
        for car in self._car_list:
            car.update()
            car.draw(screen)

    
def init_city(width, height, city_config):
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    
    pygame.display.set_caption('Fractal City Simulation')

    my_city = RoadNetwork(coordinates)
    my_city.create_roads()
    my_city.create_cars()

    run = True
    while run:
        screen.fill((40, 255, 100))

        my_city.draw_and_update(screen)

        pygame.display.update()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        
    pygame.quit()

init_city(800, 800, 1)
