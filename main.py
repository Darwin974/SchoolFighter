import pygame
import sys
import os

pygame.init()

# Configurer l'affichage
ecran = pygame.display.set_mode((700, 700))
pygame.display.set_caption("School Fighter")

horloge = pygame.time.Clock()

class ImageLoader:
    def __init__(self):
        self.images_cache = {}

    def charger_images(self, dossier, taille):
        if dossier in self.images_cache:
            return self.images_cache[dossier]

        images = []
        for fichier in sorted(os.listdir(dossier)):
            if fichier.endswith('.png'):
                image = pygame.image.load(os.path.join(dossier, fichier))
                image = pygame.transform.scale(image, taille)
                images.append(image)
        self.images_cache[dossier] = images
        return images

# Initialiser le chargeur d'images
image_loader = ImageLoader()

class AnimationLoop:
    def __init__(self, image_loader, dossier, taille, x, y):
        self.images = image_loader.charger_images(dossier, taille)
        self.sprite_actuel = 0
        self.vitesse_sprite = 0.2
        self.x = x
        self.y = y

    def mettre_a_jour(self):
        self.sprite_actuel += self.vitesse_sprite
        if self.sprite_actuel >= len(self.images):
            self.sprite_actuel = 0  # Boucle l'animation

    def dessiner(self, surface):
        surface.blit(self.images[int(self.sprite_actuel)], (self.x, self.y))

class AnimationSprite:
    def __init__(self, image_loader, dossier, taille):
        self.images = image_loader.charger_images(dossier, taille)
        self.sprite_actuel = 0
        self.vitesse_sprite = 0.2
        self.animation_finie = False

    def mettre_a_jour(self):
        if not self.animation_finie:
            self.sprite_actuel += self.vitesse_sprite
            if self.sprite_actuel >= len(self.images):
                self.sprite_actuel = len(self.images) - 1
                self.animation_finie = True

    def dessiner(self, surface, x, y):
        surface.blit(self.images[int(self.sprite_actuel)], (x, y))

# NAVIGATION BUTTON CLASS
class Button():
    def __init__(self, x, y, sx, sy, file):
        self.f = file
		# ORIGIN_X COORDINATE OF BUTTON
        self.x = x
		# ORIGIN_Y COORDINATE OF BUTTON
        self.y = y
		# LAST_X COORDINATE OF BUTTON
        self.sx = sx
        # LAST_Y COORDINATE OF BUTTON
        self.sy = sy
		# CURRENT IS OFF
        self.CurrentState = False

	# DRAW THE BUTTON ON THE SCREEN
    def showButton(self, display):
        if(self.CurrentState):
            AnimationLoop(image_loader, self.file, (400, 400), self.x, self.y)

	# THIS FUNCTION CAPTURE WHETHER ANY MOUSE EVENT OCCUR ON THE BUTTON
    def focusCheck(self, mousepos, mouseclick):
    	if(mousepos[0] >= self.x and mousepos[0]
			<= self.x + self.sx and mousepos[1] >= self.y
				and mousepos[1] <= self.y + self.sy):
            self.CurrentState = True
			# IF MOUSE BUTTON CLICK THEN 
			# NAVIGATE TO THE NEXT OR PREVIOUS TABS
            return mouseclick[0]

        else:
			# ELSE LET THE CURRENT STATE TO BE OFF
            self.CurrentState = False
            return False

class EcranMenu:
    def __init__(self):
        self.font = pygame.font.Font(None, 74)
        # Positionner le logo au centre de la fenêtre
        logo_x = (700 - 640) // 2
        logo_y = (700 - 426) // 2
        self.logo_animation = AnimationLoop(image_loader, 'img/IPI_logo', (640, 426), logo_x, logo_y)  # Chemin, taille et position du logo
        # Ajouter une animation de fond
        self.fond_animation = AnimationLoop(image_loader, 'img/IPI_TerrainSchrauder', (700, 700), 0, 0)  # Chemin, taille et position du fond

    def gerer_evenements(self, evenement):
        if evenement.type == pygame.KEYDOWN:
            if evenement.key == pygame.K_RETURN:
                return 'jeu'  # Passer à l'écran de jeu
        return 'menu'

    def mettre_a_jour(self):
        self.logo_animation.mettre_a_jour()
        self.fond_animation.mettre_a_jour()

    def dessiner(self, surface):
        surface.fill((0, 0, 0))
        self.fond_animation.dessiner(surface)  # Dessiner le fond animé
        self.logo_animation.dessiner(surface)

class EcranJeu:
    def __init__(self):
        self.animations = [
            AnimationSprite(image_loader, 'img/IPI_fight', (700, 700)),
            AnimationSprite(image_loader, 'img/IPI_Shrauder', (700, 700)),
            AnimationSprite(image_loader, 'img/IPI_Basic', (700, 700)),
            AnimationSprite(image_loader, 'img/IPI_attaque', (700, 700)),
            AnimationSprite(image_loader, 'img/IPI Basic Katana', (700, 700)),
            AnimationSprite(image_loader, 'img/IPI attaque katana', (700, 700)),
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