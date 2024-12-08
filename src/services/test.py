import pygame
import sys

pygame.init()


screen = pygame.display.set_mode((850,850))
pygame.display.set_caption("Hello World")

class Water(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((25,25))
        img = pygame.image.load("../assets/water_class.png").convert_alpha()
        self.image.blit(img,(0,0),(407,510,140,140))
        self.image.set_colorkey((31,26,23))

        pygame.transform.scale(self.image,(25,25))

        self.rect = self.image.get_rect()

group = pygame.sprite.Group()

water = Water()
water.rect.x = 12
water.rect.y = 12
group.add(water)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            done = True
            sys.exit()

    screen.fill((235,156,0))
    group.draw(screen)
    pygame.display.update()