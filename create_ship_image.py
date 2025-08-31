import pygame
pygame.init()

# Create a simple ship shape (triangle)
size = (40, 40)
ship = pygame.Surface(size, pygame.SRCALPHA)
points = [(20, 0), (0, 39), (39, 39)]
pygame.draw.polygon(ship, (255, 255, 255), points)

pygame.image.save(ship, './data/ship.png')
print('ship.png created!')
