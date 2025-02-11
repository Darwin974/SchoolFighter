import pygame
import sys
import os

pygame.init()

# Set up l'affichage
screen = pygame.display.set_mode((650, 650))
pygame.display.set_caption("Animation Shrauder Test")

clock = pygame.time.Clock()

# Charger les images du sprite
sprite_images = []
sprite_folder = 'img/IPI_Shrauder'
for file in sorted(os.listdir(sprite_folder)):
    if file.endswith('.png'):
        image = pygame.image.load(os.path.join(sprite_folder, file))
        image = pygame.transform.scale(image, (650, 650))  # Redimensionner l'image
        sprite_images.append(image)

# Variables d'animation
current_sprite = 0
sprite_x = 0
sprite_y = 0
sprite_speed = 0.2
animation_finie = False

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update le sprite actuel si l'animation n'est pas finie
    if not animation_finie:
        current_sprite += sprite_speed
        if current_sprite >= len(sprite_images):
            current_sprite = len(sprite_images) - 1
            animation_finie = True

    # Couleur de l'écran
    screen.fill((0, 0, 0))  # Noir

    # Dessine le sprite actuel
    screen.blit(sprite_images[int(current_sprite)], (sprite_x, sprite_y))

    # Update l'affichage
    pygame.display.flip()

    # FPS
    clock.tick(60)