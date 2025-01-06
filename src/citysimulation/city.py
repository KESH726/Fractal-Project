import pygame
from math import sqrt
import random

# Helper functions
def calculate_magnitude(point1, point2):
    # Calculate the Euclidean distance (magnitude)
    return sqrt((abs(point2[0] - point1[0]))**2 + (abs(point2[1] - point1[1]))**2)

""" road_coordinates = [
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
] """

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
    def __init__(self, network, current_road, speed=2):
        self.current_road = current_road
        self.speed = speed
        self.pos = current_road.start_pos
        self.progress = 0  # 0 to 1, representing position along current road
        self.color = (255, 0, 0)  # Red car
        self.network = network
    
    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, (self.pos[0]-10, self.pos[1]-5, 20, 10))

    def update(self):
        self.progress += self.speed / self.current_road.get_length()
        if self.progress >= 1:
            self.progress = 1  # handle road switching later in pathfinding
            self.switch_road()
            
        # Interpolate position
        start_x, start_y = self.current_road.start_pos
        end_x, end_y = self.current_road.end_pos
        self.pos = (
            start_x + (end_x - start_x) * self.progress,
            start_y + (end_y - start_y) * self.progress
        )
    
    def switch_road(self):
        roads = self.network.get_road_list(self.network)
        match_roads = []
        match_road_found = False

        for road in roads:
            if (road.start_pos == self.current_road.end_pos):
                match_roads.append(road)
                match_road_found = True
        
        if match_road_found:
            random_match_road = random.choice(match_roads)
            self.current_road = random_match_road
            self.pos = random_match_road.start_pos
            self.progress = 0
        
        if not match_road_found:
            pass

        # Find new ends

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

    def __init__(self, coordinates, segments, scale_factor, translation_vector):
        # Pairs of coordinates to create vector lines for roads
        coordinate_pairs = []

        # Coordinates that have been used up to make a vector already
        used_up_coords = []   

        for coord in coordinates:
            # Skip current coordinate if we've already used it
            if coord in used_up_coords:
                continue

            closest_coords = []
            #print("NEW COORDINATE:", closest_coords)

            # Fetch distance to all other coordinates
            for matching_coord in coordinates:
                # Skip this paired up coordinate if we've already used it
                if matching_coord in used_up_coords: 
                    continue

                # If these two coordinates have the same value, there's no point in making a road,
                # so put a really high magnitude that it basically gets ignored
                if (coord == matching_coord):
                    closest_coords.append(99999999)
                    continue
                
                magnitude = calculate_magnitude(coord, matching_coord)
                #print(coord, matching_coord, magnitude)

                closest_coords.append(calculate_magnitude(coord, matching_coord))

            # Join the seg
            # Create a list of tuples consisting of magnitude & index
            indexed_coords = list(enumerate(closest_coords))

            # Sort by magnitude, but keep original indices
            sorted_coords = sorted(indexed_coords, key=lambda x: x[1])

            # Get smallest magnitudes
            smallest_values = sorted_coords[:segments]

            # Get the smallest values in the order they appeared on the original list of coordinates
            smallest_coordinates = [coordinates[index] for index, _ in smallest_values]

            # Scale the coordinates to be bigger so it covers more of the map
            smallest_coordinates = [(x * scale_factor, y * scale_factor) for x, y in smallest_coordinates]

            # Translate the coordinates if needed
            smallest_coordinates = [
                (x + translation_vector[0], y + translation_vector[1]) for x, y in smallest_coordinates
            ]

            # Iterate through the smallest coordinates and pair them up, so we can form roads
            for i in range(len(smallest_coordinates) - 1):
                pair = (smallest_coordinates[i], smallest_coordinates[i + 1])
                coordinate_pairs.append(pair)      

                # Mark these coordinates as used
                used_up_coords.append(smallest_coordinates[i])
                used_up_coords.append(smallest_coordinates[i + 1])
    
        self.roads_coordinates = coordinate_pairs
    
    def create_roads(self):
        for road_coordinate in self.roads_coordinates:
            #print(road_coordinate)
            new_road = Road((road_coordinate[0]),(road_coordinate[1]))
            new_reverse_road = Road((road_coordinate[1]),(road_coordinate[0]))
            
            # Only add roads to the network with a valid length (not 0)
            if new_road.get_length() != 0:
                RoadNetwork._road_list.append(new_road)
                RoadNetwork._road_list.append(new_reverse_road)

    def create_cars(self):
        for road in self._road_list:
            new_car = Car(RoadNetwork, road, 0.5)
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
    
    def get_car_list(self):
        return self._car_list
    
    def get_road_list(self):
        return self._road_list
    
    def get_building_list(self):
        return self._building_list

    
def init_city(width, height, city_config):
    pygame.init()
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    clock = pygame.time.Clock()

    # Create a test surface that is larger than the screen (e.g., a large map)
    scale_factor = 6
    map_width, map_height = 1000*scale_factor, 720*scale_factor
    map_surface = pygame.Surface((map_width, map_height))

    map_surface.fill((40, 255, 100))

    # Camera variables
    camera_zoom = 0.5           # Zoom factor (1.0 means no zoom)
    # Camera offset
    camera_offset_quotient = (camera_zoom*10) + 1
    camera_x, camera_y = map_width/(camera_offset_quotient), map_width/(camera_offset_quotient) 
    

    dragging = False
    last_mouse_x, last_mouse_y = 0, 0

    # Set default cursor to system cursor
    pygame.mouse.set_cursor(*pygame.cursors.arrow)
    
    pygame.display.set_caption('Fractal City Simulation')

    my_city = RoadNetwork(coordinates, 5, 3, (map_width/4, map_height/4))
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
                    # Change cursor to grab hand when dragging
                    pygame.mouse.set_cursor(*pygame.cursors.broken_x)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Stop dragging
                    dragging = False
                    # Reset cursor back to normal when done
                    pygame.mouse.set_cursor(*pygame.cursors.arrow)
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
