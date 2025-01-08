import pygame
import math
from math import sqrt
import random
import time
import os
import pygame


def load_image(filename, scaled=False, width=100, height=100):
    # Get the absolute path to the assets folder
    assets_path = os.path.join(os.path.dirname(__file__), '../assets')

    # Construct the full path to the image
    image_path = os.path.join(assets_path, filename)

    # Normalize the path to use forward slashes
    image_path = image_path.replace("\\", "/")

    # Debugging: Print the path being used
    print(f"Attempting to load image from: {image_path}")
    
    image = pygame.image.load(image_path)
    
    if scaled:
        scaled_image = pygame.transform.scale(image, (width, height))
        return scaled_image

    return image

def load_image_with_rounded_corners(filename, width, height, radius):
    # Initialize Pygame if not already initialized
    if not pygame.get_init():
        pygame.init()

    # Create a dummy display surface (this prevents "No video mode has been set" error)
    pygame.display.set_mode((1, 1))

    # Get the absolute path to the assets folder
    assets_path = os.path.join(os.path.dirname(__file__), '../assets')

    # Construct the full path to the image
    image_path = os.path.join(assets_path, filename)

    # Normalize the path to use forward slashes
    image_path = image_path.replace("\\", "/")

    # Debugging: Print the path being used
    print(f"Attempting to load image from: {image_path}")
    
    # Load the image and convert it to have an alpha channel
    image = pygame.image.load(image_path).convert_alpha()

    # Scale the image to the desired size
    image = pygame.transform.scale(image, (width, height))

    # Create a mask with a rounded rectangle
    mask = pygame.Surface((width, height), pygame.SRCALPHA)  # Create a surface with alpha channel
    mask.fill((0, 0, 0, 0))  # Fill with transparency (fully alpha)
    
    # Draw a filled rounded rectangle onto the mask (white part will be visible)
    pygame.draw.rect(mask, (255, 255, 255), (0, 0, width, height), border_radius=radius)
    
    # Apply the mask to the image using BLEND_RGBA_MULT to preserve transparency
    image.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    return image


# Art assets
grass_image = load_image("city/ground_grass.png")
road_image = load_image_with_rounded_corners("city/road.png", 60, 60, 10)
car_images = [
    load_image("city/cars/van_black.png"),
    load_image("city/cars/pickup_olive.png"),
    load_image("city/cars/sedan_red.png"),
    load_image("city/cars/police_patrol_color.png"),
    load_image("city/cars/ambulance.png"),
    load_image("city/cars/seda_blue.png"),
    load_image("city/cars/van_red.png"),
    load_image("city/cars/pickup_gray.png"),
]
nature_images = [
    load_image("city/bush_01.png"),
    load_image("city/bush_02.png"),
    load_image("city/bush_03.png"),
    load_image("city/bush_04.png"),
    load_image("city/flowers_red.png"),
    load_image("city/flowers_yellow.png"),
    load_image("city/light_post.png"),
    load_image("city/tree_01.png"),
    load_image("city/tree_02.png"),
    load_image("city/tree_fall_01.png"),
    load_image("city/tree_fall_03.png"),
]


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
        self.road_image = road_image.convert_alpha()  # Ensure the image has alpha transparency

        # Calculate the road length (distance between start and end)
        self.length = self.get_length()

        # Calculate the angle to rotate the road image (from start to end)
        self.angle = self.calculate_angle()

    def calculate_angle(self):
        # Calculate the angle (in degrees) between the start and end points
        x1, y1 = self.start_pos
        x2, y2 = self.end_pos
        return math.degrees(math.atan2(y2 - y1, x2 - x1))

    def draw(self, screen):
        # Get the dimensions of the road image (keeping its original size)
        image_width, image_height = self.road_image.get_size()

        # Calculate the number of tiles needed to cover the road
        num_tiles = int(self.length / image_width)

        for i in range(num_tiles):
            # Position each image along the road
            # Calculate the x, y position for the tile
            tile_pos = (
                self.start_pos[0] + i * image_width * math.cos(math.radians(self.angle)),
                self.start_pos[1] + i * image_width * math.sin(math.radians(self.angle))
            )

            # Rotate the image to match the road angle
            rotated_image = pygame.transform.rotate(self.road_image, -self.angle)

            # Get the rotated image's rect to position it correctly
            rotated_rect = rotated_image.get_rect()
            rotated_rect.center = tile_pos

            # Draw the rotated image at the calculated position
            screen.blit(rotated_image, rotated_rect.topleft)

    def get_length(self):
        # Calculate the length of the road (distance between start and end points)
        x1, y1 = self.start_pos
        x2, y2 = self.end_pos
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


class Car:
    def __init__(self, network, current_road, speed=2):
        self.current_road = current_road
        self.speed = speed
        self.pos = current_road.start_pos
        self.progress = 0  # 0 to 1, representing position along current road
        self.color = (255, 0, 0)  # Red car
        self.network = network

        self.nearby_cars = []
        self.range = 10
        self.stop_counter = 0

        self.car_image = random.choice(car_images)
        self.angle = 0
    
    def draw(self, screen):
        #pygame.draw.ellipse(screen, self.color, (self.pos[0]-10, self.pos[1]-5, 20, 10))
         # Calculate the vector from the car's current position to the destination (end of the road)
        start_x, start_y = self.pos
        end_x, end_y = self.current_road.end_pos

        # Calculate the angle using atan2 (returns angle in radians)
        delta_x = end_x - start_x
        delta_y = end_y - start_y
        self.angle = math.degrees(math.atan2(delta_y, delta_x))  # Convert radians to degrees for rotation

        self.angle += 180

        # Rotate the car image based on the calculated angle
        rotated_image = pygame.transform.rotate(self.car_image, -self.angle)  # Negative to rotate correctly

        # Get the new position for the rotated image (so it's centered around the car's position)
        new_rect = rotated_image.get_rect(center=(self.pos[0], self.pos[1]))

        # Draw the rotated car image
        screen.blit(rotated_image, new_rect.topleft)

    def update(self):
        self.check_for_traffic()

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
            self.check_nearby_cars()
        
        if not match_road_found:
            pass
    
    def check_nearby_cars(self):
        cars = self.network.get_car_list(self.network)
        roads = self.network.get_road_list(self.network)

        self.nearby_cars = []

        # Collect cars from current road
        for car in cars:
            if self.current_road == car.current_road:
               self. nearby_cars.append(car)

        # Collect cars from nearby roads
        for road in roads:
            if (road.start_pos) == self.current_road.end_pos:
                for car in cars:
                    if car.current_road == road:
                        self.nearby_cars.append(car)

    def check_for_traffic(self):
        # Track if a car is nearby and maintain a persistent timer
        if not hasattr(self, 'start_time'):  # Initialize start_time if it doesn't exist
            self.start_time = None

        car_in_range = False

        for car in self.nearby_cars:
            # Check if car is within range
            if calculate_magnitude(self.pos, car.pos) <= self.range:
                difference = (car.progress - self.progress)
                if 0 < difference <= 0.5:  # A car is close enough
                    #print("CAR IN RANGE")
                    self.stop_counter += 1
                    self.speed = 0
                    car_in_range = True

                    # Start the timer if it hasn't been started
                    if self.start_time is None:
                        self.start_time = time.time()
                    break  # Stop checking once a car is detected

        if not car_in_range:
            # Reset timer and resume movement if no cars are in range
            self.start_time = None
            self.speed = 2
        else:
            # Check if it's time to resume
            elapsed_time = time.time() - self.start_time
            if elapsed_time >= 2:
                self.speed = 2
                self.start_time = None  # Reset timer after resuming


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
    _nature_list = []
    _cars_left = 0

    def __init__(self, coordinates, segments, no_of_cars, scale_factor, translation_vector):
        self._cars_left = no_of_cars

        self.initial_coords = coordinates

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
            if self._cars_left <= 0:
                break

            new_car = Car(RoadNetwork, road, 2)
            RoadNetwork._car_list.append(new_car)
            self._cars_left -= 1
            print("ADDED ONE CAR")

    
    def create_buildings(self, building_count):
        for i in range(building_count):
            boundary_px = 60
            random_x = random.randint(0+boundary_px,800-boundary_px)
            random_y = random.randint(0+boundary_px,800-boundary_px)
            random_width = random.randint(10,20)
            random_height = random.randint(10,20)
            new_building = Building(random_x, random_y, random_width, random_height)
            RoadNetwork._building_list.append(new_building)
    
    def create_nature(self, nature_count, map_width, map_height):
        new_coordinates = []

        while len(new_coordinates) < nature_count:
            # Generate random coordinates within the map boundaries
            x = random.randint(0, map_width - 1)
            y = random.randint(0, map_height - 1)

            # Check if this coordinate is not already in the existing list or the new coordinates list
            if (x, y) not in self.initial_coords and (x, y) not in new_coordinates:
                new_coordinates.append((x, y))

        # For each generated coordinate, select a random nature image
        for coord in new_coordinates:
            # Select a random image from the nature_images list
            nature_image = random.choice(nature_images)
            
            # Add a dictionary or object to store the image and its position (for later drawing)
            nature_obj = {"image": nature_image, "position": coord}
            RoadNetwork._nature_list.append(nature_obj)
    
    def draw_and_update(self, screen):
        for road in RoadNetwork._road_list:
            road.draw(screen)
        for car in RoadNetwork._car_list:
            car.update()
            car.draw(screen)
        for building in RoadNetwork._building_list:
            building.draw(screen)
        for nature_obj in RoadNetwork._nature_list:
            # Draw the nature image at its position
            screen.blit(nature_obj["image"], nature_obj["position"])
    
    def get_car_list(self):
        return self._car_list
    
    def get_road_list(self):
        return self._road_list
    
    def get_building_list(self):
        return self._building_list



# Map
def tile_grass(map_surface, map_width, map_height):
    # Get the dimensions of the grass image
    grass_width, grass_height = grass_image.get_size()
    
    # Tile the grass texture over the entire surface
    for x in range(0, map_width, grass_width):
        for y in range(0, map_height, grass_height):
            map_surface.blit(grass_image, (x, y))

    
def init_city(width, height, segments, cars, stoplights):
    pygame.init()
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    clock = pygame.time.Clock()

    # Create a test surface that is larger than the screen (e.g., a large map)
    scale_factor = 6
    map_width, map_height = 1000*scale_factor, 720*scale_factor
    map_surface = pygame.Surface((map_width, map_height))

    #map_surface.fill((40, 255, 100))
    tile_grass(map_surface, map_width, map_height)

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

    my_city = RoadNetwork(coordinates, segments, cars, 3, (map_width/4, map_height/4))
    my_city.create_roads()
    my_city.create_cars()
    my_city.create_buildings(10)
    my_city.create_nature(500, map_width, map_height)

    run = True
    while run:
        screen.fill((0, 0, 0))
        #map_surface.fill((40, 255, 100))
        tile_grass(map_surface, map_width, map_height)

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
    init_city(800, 800, 5, 10, 3)
