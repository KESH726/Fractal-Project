import pygame
class Water(pygame.sprite.Sprite):
    def __init__(self,size):
        super().__init__()
        self.image = pygame.image.load("../assets/water_class.png")
        pygame.transform.scale(self.image,size)
        self.rect = self.image.get_rect()