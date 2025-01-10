import math
import pygame
import random
import time

from .assetloader import load_image, load_image_with_rounded_corners

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
    return math.sqrt((abs(point2[0] - point1[0]))**2 + (abs(point2[1] - point1[1]))**2)

def get_lane_offset(start, end, offset):
    # Calculate direction vector
    direction = (end[0] - start[0], end[1] - start[1])
    # Perpendicular vector
    perpendicular = (-direction[1], direction[0])
    # Normalize
    magnitude = math.sqrt(perpendicular[0]**2 + perpendicular[1]**2)
    normalized_perpendicular = (perpendicular[0] / magnitude, perpendicular[1] / magnitude)
    # Apply offset
    return (normalized_perpendicular[0] * offset, normalized_perpendicular[1] * offset)

class Road:
    def __init__(self, start_pos, end_pos, reverse=False, width=2):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.reverse = reverse
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
    def __init__(self, network, current_road, speed=2, reverse=False):
        self.current_road = current_road
        self.speed = speed

        self.pos = current_road.start_pos
        self.end_pos = current_road.end_pos

        self.translated_pos = current_road.start_pos
        self.translated_end_pos = current_road.end_pos

        self.swap_lane(reverse)

        self.progress = 0  # 0 to 1, representing position along current road
        self.color = (255, 0, 0)  # Red car
        self.network = network

        self.nearby_cars = []
        self.range = 70
        self.stop_counter = 0

        self.car_image = random.choice(car_images)
        self.angle = 0

        self.creation_time = time.time()
        self.traffic_time = 0
        self.stop_start_time = None

        self.cooldown_start_time = 3
    
    def draw(self, screen):
        #pygame.draw.ellipse(screen, self.color, (self.pos[0]-10, self.pos[1]-5, 20, 10))
         # Calculate the vector from the car's current position to the destination (end of the road)
        start_x, start_y = self.translated_pos
        end_x, end_y = self.translated_end_pos

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
        self.check_nearby_cars()
        self.check_for_traffic()

        self.progress += self.speed / self.current_road.get_length()
        if self.progress >= 1:
            self.progress = 1  # handle road switching later in pathfinding
            self.switch_road()
            
        # Interpolate position
        start_x, start_y = self.translated_pos
        end_x, end_y = self.translated_end_pos
        self.pos = (
            start_x + (end_x - start_x) * self.progress,
            start_y + (end_y - start_y) * self.progress
        )
    
    def swap_lane(self, reverse=False):
        self.lane_offset_multiplier = 20

        self.lane_offset = get_lane_offset(self.pos, self.end_pos, self.lane_offset_multiplier)

        self.translated_pos = (self.pos[0] + self.lane_offset[0], self.pos[1] + self.lane_offset[1])
        self.translated_end_pos = (self.end_pos[0] + self.lane_offset[0], self.end_pos[1] + self.lane_offset[1])
    
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
            self.end_pos = random_match_road.end_pos

            self.swap_lane(random_match_road.reverse)

            self.progress = 0
        
        if not match_road_found:
            pass
    
    def check_nearby_cars(self):
        cars = self.network.get_car_list(self.network)
        # roads = self.network.get_road_list(self.network)

        self.nearby_cars = []

        # Collect cars from current road
        for car in cars:
            if (self.current_road == car.current_road) and car != self:
               self.nearby_cars.append(car)

    def check_for_traffic(self):
        car_in_range = False

        for car in self.nearby_cars:
            if car == self:
                continue
            # Check if car is within range
            if calculate_magnitude(self.pos, car.pos) <= self.range:
                difference = (self.progress - car.progress)
                if difference < 0:  # A car is close enough
                    if self.speed != 0:  
                        self.stop_start_time = time.time()
                    self.stop_counter += 1
                    self.speed = 0
                    car_in_range = True
                    break

        if not car_in_range:
            if self.speed == 0 and self.stop_start_time is not None:
                elapsed_time = time.time() - self.stop_start_time
                self.traffic_time += elapsed_time  
                self.stop_start_time = None 
            self.speed = 2