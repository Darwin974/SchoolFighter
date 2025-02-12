import pygame
import sys
import os

pygame.init()

# Configurer l'affichage
ecran = pygame.display.set_mode((700, 700))
pygame.display.set_caption("Test d'Animation")

horloge = pygame.time.Clock()

class AnimationSprite:
    def __init__(self, dossier, taille):
        self.images = self.charger_images(dossier, taille)
        self.sprite_actuel = 0
        self.vitesse_sprite = 0.2
        self.animation_finie = False

    def charger_images(self, dossier, taille):
        """Charger et redimensionner les images des sprites depuis un dossier."""
        images = []
        for fichier in sorted(os.listdir(dossier)):
            if fichier.endswith('.png'):
                image = pygame.image.load(os.path.join(dossier, fichier))
                image = pygame.transform.scale(image, taille)  # Redimensionner l'image
                images.append(image)
        return images

    def mettre_a_jour(self):
        """Mettre à jour le sprite actuel si l'animation n'est pas finie."""
        if not self.animation_finie:
            self.sprite_actuel += self.vitesse_sprite
            if self.sprite_actuel >= len(self.images):
                self.sprite_actuel = len(self.images) - 1
                self.animation_finie = True

    def dessiner(self, surface, x, y):
        """Dessiner le sprite actuel sur la surface donnée."""
        surface.blit(self.images[int(self.sprite_actuel)], (x, y))

# Charger les animations des sprites
animations = [
    AnimationSprite('img/IPI_fight', (700, 700)),
    AnimationSprite('img/IPI_Shrauder', (700, 700)),
    AnimationSprite('img/IPI_Basic', (700, 700)),
    AnimationSprite('img/IPI_attaque', (700, 700)),
]

index_animation_actuelle = 0
toutes_animations_finies = False

# Boucle principale du jeu
en_cours = True
while en_cours:
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not toutes_animations_finies:
        # Mettre à jour l'animation actuelle
        animation_actuelle = animations[index_animation_actuelle]
        animation_actuelle.mettre_a_jour()

        # Vérifier si l'animation actuelle est finie et passer à la suivante
        if animation_actuelle.animation_finie:
            index_animation_actuelle += 1
            if index_animation_actuelle >= len(animations):
                toutes_animations_finies = True

        # Dessiner l'animation actuelle
        ecran.fill((0, 0, 0))  # Remplir l'écran de noir avant de dessiner
        animation_actuelle.dessiner(ecran, 0, 0)
    else:
        # Remplir l'écran de noir si toutes les animations sont finies
        ecran.fill((0, 0, 0))

    # Mettre à jour l'affichage
    pygame.display.flip()

    # Limiter la fréquence d'images par seconde
    horloge.tick(60)