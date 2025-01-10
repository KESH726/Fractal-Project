import pygame

from .assetloader import load_image

from .road_network import RoadNetwork

# Grass tile map
grass_image = load_image("city/ground_grass.png")

def tile_grass(map_surface, map_width, map_height):
    # Get the dimensions of the grass image
    grass_width, grass_height = grass_image.get_size()
    
    # Tile the grass texture over the entire surface
    for x in range(0, map_width, grass_width):
        for y in range(0, map_height, grass_height):
            map_surface.blit(grass_image, (x, y))

    
def init_city(width, height, segments, cars, stoplights, coordinates):
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
