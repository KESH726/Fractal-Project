import random

from .entities import Road, Car, Building, calculate_magnitude, nature_images

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