import pygame
import sys
import os

pygame.init()

# Configurer l'affichage
ecran = pygame.display.set_mode((700, 700))
pygame.display.set_caption("School Fighter")

horloge = pygame.time.Clock()

class AnimationLoop:
    def __init__(self, dossier, taille, x, y):
        self.images = self.charger_images(dossier, taille)
        self.sprite_actuel = 0
        self.vitesse_sprite = 0.2
        self.x = x
        self.y = y

    def charger_images(self, dossier, taille):
        images = []
        for fichier in sorted(os.listdir(dossier)):
            if fichier.endswith('.png'):
                image = pygame.image.load(os.path.join(dossier, fichier))
                image = pygame.transform.scale(image, taille)
                images.append(image)
        return images

    def mettre_a_jour(self):
        self.sprite_actuel += self.vitesse_sprite
        if self.sprite_actuel >= len(self.images):
            self.sprite_actuel = 0  # Boucle l'animation

    def dessiner(self, surface):
        surface.blit(self.images[int(self.sprite_actuel)], (self.x, self.y))

class EcranMenu:
    def __init__(self):
        self.font = pygame.font.Font(None, 74)
        self.text = self.font.render('Menu Principal', True, (255, 255, 255))
        # Positionner le logo au centre de la fenêtre
        logo_x = (700 - 640) // 2
        logo_y = (700 - 426) // 2
        self.logo_animation = AnimationLoop('img/IPI_logo', (640, 426), logo_x, logo_y)  # Chemin, taille et position du logo

    def gerer_evenements(self, evenement):
        if evenement.type == pygame.KEYDOWN:
            if evenement.key == pygame.K_RETURN:
                return 'jeu'  # Passer à l'écran de jeu
        return 'menu'

    def mettre_a_jour(self):
        self.logo_animation.mettre_a_jour()

    def dessiner(self, surface):
        surface.fill((0, 0, 0))
        surface.blit(self.text, (150, 300))
        self.logo_animation.dessiner(surface)

class EcranJeu:
    def __init__(self):
        self.animations = [
            AnimationSprite('img/IPI_fight', (700, 700)),
            AnimationSprite('img/IPI_Shrauder', (700, 700)),
            AnimationSprite('img/IPI_Basic', (700, 700)),
            AnimationSprite('img/IPI_attaque', (700, 700)),
        ]
        self.index_animation_actuelle = 0
        self.toutes_animations_finies = False

    def gerer_evenements(self, evenement):
        if evenement.type == pygame.KEYDOWN:
            if evenement.key == pygame.K_ESCAPE:
                return 'menu'  # Retourner au menu
        return 'jeu'

    def mettre_a_jour(self):
        if not self.toutes_animations_finies:
            animation_actuelle = self.animations[self.index_animation_actuelle]
            animation_actuelle.mettre_a_jour()
            if animation_actuelle.animation_finie:
                self.index_animation_actuelle += 1
                if self.index_animation_actuelle >= len(self.animations):
                    self.toutes_animations_finies = True

    def dessiner(self, surface):
        surface.fill((0, 0, 0))
        if not self.toutes_animations_finies:
            animation_actuelle = self.animations[self.index_animation_actuelle]
            animation_actuelle.dessiner(surface, 0, 0)

class AnimationSprite:
    def __init__(self, dossier, taille):
        self.images = self.charger_images(dossier, taille)
        self.sprite_actuel = 0
        self.vitesse_sprite = 0.2
        self.animation_finie = False

    def charger_images(self, dossier, taille):
        images = []
        for fichier in sorted(os.listdir(dossier)):
            if fichier.endswith('.png'):
                image = pygame.image.load(os.path.join(dossier, fichier))
                image = pygame.transform.scale(image, taille)
                images.append(image)
        return images

    def mettre_a_jour(self):
        if not self.animation_finie:
            self.sprite_actuel += self.vitesse_sprite
            if self.sprite_actuel >= len(self.images):
                self.sprite_actuel = len(self.images) - 1
                self.animation_finie = True

    def dessiner(self, surface, x, y):
        surface.blit(self.images[int(self.sprite_actuel)], (x, y))

# Initialiser les écrans
ecrans = {
    'menu': EcranMenu(),
    'jeu': EcranJeu()
}
ecran_actuel = 'menu'

# Boucle principale du jeu
en_cours = True
while en_cours:
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Gérer les événements de l'écran actuel
        nouvel_ecran = ecrans[ecran_actuel].gerer_evenements(evenement)
        if nouvel_ecran != ecran_actuel:
            ecran_actuel = nouvel_ecran

    # Mettre à jour l'écran actuel
    ecrans[ecran_actuel].mettre_a_jour()

    # Dessiner l'écran actuel
    ecrans[ecran_actuel].dessiner(ecran)

    # Mettre à jour l'affichage
    pygame.display.flip()

    # Limiter la fréquence d'images par seconde
    horloge.tick(60)