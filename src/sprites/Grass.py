import pygame

class Grass(pygame.sprite.Sprite):
    def __init__(self,size):
        super().__init__()

        self.image = pygame.image.load("../assets/soil_grass_pack/grass1.png")
        pygame.transform.Scale(self.iamge,size)
        self.rect = self.image.get_rect()