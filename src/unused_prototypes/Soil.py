import pygame
class Soil(pygame.sprite.Sprite):
    def __init__(self,size):
        super().__init__()
        self.image = pygame.image.load("../assets/soil_grass_pack/soil1.png")
        pygame.transform.scale(self.image,size)
        self.rect = self.image.get_rect()