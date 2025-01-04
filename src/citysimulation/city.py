import pygame
from math import sqrt
import random

road_coordinates = [
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

coordinates = [
    (50, 100),
    (250, 100),
    (300, 200),
    (600, 200),
    (100, 300),
    (400, 300),
    (450, 400),
    (750, 400),
    (200, 500),
    (500, 500),

    (100, 50),
    (100, 250),
    (250, 150),
    (250, 450),
    (400, 100),
    (400, 350),
    (550, 200),
    (550, 500),
    (700, 50),
    (700, 250),

    (50, 50),
    (200, 200),
    (250, 100),
    (400, 250),
    (150, 400),
    (300, 550),
    (500, 50),
    (650, 200),
    (350, 300),
    (500, 450),
    (600, 400),
    (750, 550),
    (100, 600),
    (250, 750),
    (400, 500),
    (550, 650),
    (200, 250),
    (350, 400),
    (650, 150),
    (800, 300)
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
            self.progress = 1  # handle road switching later in pathfinding
            
        # Interpolate position
        start_x, start_y = self.current_road.start_pos
        end_x, end_y = self.current_road.end_pos
        self.pos = (
            start_x + (end_x - start_x) * self.progress,
            start_y + (end_y - start_y) * self.progress
        )
    
    def pathfinding(self):
        pass


class Building:
    def __init__(self, x, y, width, height):
        self.coord = pygame.Rect(x, y, width, height)
        self.color = (72, 73, 74)
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.coord)


class RoadNetwork:
    _car_list = []
    _road_list = []
    _building_list = []

    def __init__(self, coordinates):
        coordinate_pairs = []

        self.roads_coordinates = road_coordinates
    
    def create_roads(self):
        for road_coordinate in self.roads_coordinates:
            RoadNetwork._road_list.append(Road((road_coordinate[0]),(road_coordinate[1])))

    def create_cars(self):
        for road in self._road_list:
            new_car = Car(road, 0.5)
            RoadNetwork._car_list.append(new_car)
    
    def create_buildings(self, building_count):
        for i in range(building_count):
            boundary_px = 60
            random_x = random.randint(0+boundary_px,800-boundary_px)
            random_y = random.randint(0+boundary_px,800-boundary_px)
            random_width = random.randint(10,20)
            random_height = random.randint(10,20)
            new_building = Building(random_x, random_y, random_width, random_height)
            RoadNetwork._building_list.append(new_building)
    
    def draw_and_update(self, screen):
        for road in RoadNetwork._road_list:
            road.draw(screen)
        for car in RoadNetwork._car_list:
            car.update()
            car.draw(screen)
        for building in RoadNetwork._building_list:
            building.draw(screen)

    
def init_city(width, height, city_config):
    pygame.init()
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    clock = pygame.time.Clock()

    # Camera variables
    camera_x, camera_y = 0, 0  # Camera offset
    camera_zoom = 1.0           # Zoom factor (1.0 means no zoom)

    # Create a test surface that is larger than the screen (e.g., a large map)
    scale_factor = 3
    map_width, map_height = 1000*scale_factor, 720*scale_factor
    map_surface = pygame.Surface((map_width, map_height))

    map_surface.fill((40, 255, 100))

     # Start the camera at the center of the map
    camera_x = (map_width - width) // 2  # Center the camera horizontally
    camera_y = (map_height - height) // 2  # Center the camera vertically

    dragging = False
    last_mouse_x, last_mouse_y = 0, 0
    
    pygame.display.set_caption('Fractal City Simulation')

    my_city = RoadNetwork(coordinates)
    my_city.create_roads()
    my_city.create_cars()
    my_city.create_buildings(10)

    run = True
    while run:
        screen.fill((0, 0, 0))
        map_surface.fill((40, 255, 100))

        my_city.draw_and_update(map_surface)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.VIDEORESIZE:  # Handle resize events
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left-click to start dragging
                    dragging = True
                    last_mouse_x, last_mouse_y = event.pos
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Stop dragging
                    dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    mouse_x, mouse_y = event.pos
                    # Move the camera by the difference in mouse movement
                    camera_x -= mouse_x - last_mouse_x
                    camera_y -= mouse_y - last_mouse_y
                    last_mouse_x, last_mouse_y = mouse_x, mouse_y
            elif event.type == pygame.MOUSEWHEEL:
                zoom_factor = 1.1 if event.y > 0 else 1 / 1.1
                camera_zoom *= zoom_factor

        # Apply the camera transformations (panning + zooming)
        scaled_surface = pygame.transform.scale(map_surface, 
                                                (int(map_width * camera_zoom), int(map_height * camera_zoom)))

        # Compute the area of the map that should be visible based on camera position and zoom
        camera_rect = pygame.Rect(camera_x, camera_y, width, height)
        
        # Blit the visible portion of the map to the screen
        screen.blit(scaled_surface, (0, 0), camera_rect)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    init_city(800, 800, 1)
