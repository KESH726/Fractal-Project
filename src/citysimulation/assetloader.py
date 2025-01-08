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