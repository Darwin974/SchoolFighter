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
    def __init__(self, image_loader, dossier, taille, x, y, appliquer_gravite=False):
        self.images = image_loader.charger_images(dossier, taille)
        self.sprite_actuel = 0
        self.vitesse_sprite = 0.2
        self.x = x
        self.y = y
        self.vitesse_x = 0
        self.vitesse_y = 0
        self.en_air = False  # Indique si le joueur est en l'air
        self.sol = 100  # Position du sol ajustée (plus élevée)

        self.appliquer_gravite = appliquer_gravite

    def mettre_a_jour(self):
        self.sprite_actuel += self.vitesse_sprite
        if self.sprite_actuel >= len(self.images):
            self.sprite_actuel = 0  # Boucle l'animation
        self.x += self.vitesse_x
        self.y += self.vitesse_y

        # Appliquer la gravité uniquement si nécessaire
        if self.appliquer_gravite:
            if self.y < self.sol:
                self.vitesse_y += 0.5  # Gravité
                self.en_air = True
            else:
                self.y = self.sol
                self.vitesse_y = 0
                self.en_air = False

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
    def __init__(self, x, y, sx, sy, file, target_screen):
        self.file = file
        self.x = x
        self.y = y
        self.sx = sx
        self.sy = sy
        self.CurrentState = False
        self.target_screen = target_screen
        self.animation = AnimationLoop(image_loader, self.file, (self.sx, self.sy), self.x, self.y)

    # DRAW THE BUTTON ON THE SCREEN
    def showButton(self, display):
        self.animation.dessiner(display)

    # THIS FUNCTION CAPTURE WHETHER ANY MOUSE EVENT OCCUR ON THE BUTTON
    def focusCheck(self, mousepos, mouseclick):
        if (self.x <= mousepos[0] <= self.x + self.sx and
            self.y <= mousepos[1] <= self.y + self.sy):
            self.CurrentState = True
            if mouseclick[0]:
                if self.target_screen == 'exit':
                    pygame.quit()
                    sys.exit()
                return self.target_screen
        else:
            self.CurrentState = False
        return None

class EcranMenu:
    def __init__(self):
        self.font = pygame.font.Font(None, 74)
        # Positionner le logo au centre de la fenêtre
        logo_x = (700 - 640) // 2
        logo_y = (700 - 426) // 2
        self.logo_animation = AnimationLoop(image_loader, 'img/IPI_logo', (640, 420), logo_x, logo_y)  # Chemin, taille et position du logo
        # Ajouter une animation de fond
        self.fond_animation = AnimationLoop(image_loader, 'img/IPI_TerrainSchrauder', (700, 700), 0, 0)  # Chemin, taille et position du fond
        self.buttons = [
            Button(250, 435, 200, 100, 'img/IPI start', 'jeu'),
            Button(250, 535, 200, 100, 'img/IPI quit', 'exit')
        ]

    def gerer_evenements(self, evenement):
        if evenement.type == pygame.MOUSEBUTTONDOWN:
            mousepos = pygame.mouse.get_pos()
            mouseclick = pygame.mouse.get_pressed()
            for button in self.buttons:
                target_screen = button.focusCheck(mousepos, mouseclick)
                if target_screen:
                    return target_screen
        return 'menu'

    def mettre_a_jour(self):
        self.logo_animation.mettre_a_jour()
        self.fond_animation.mettre_a_jour()
        for button in self.buttons:
            button.animation.mettre_a_jour()

    def dessiner(self, surface):
        surface.fill((0, 0, 0))
        self.fond_animation.dessiner(surface)  # Dessiner le fond animé
        self.logo_animation.dessiner(surface)
        for button in self.buttons:
            button.showButton(surface)

class CombatSystem:
    def __init__(self, joueur_animation):
        self.joueur_animation = joueur_animation
        self.joueur_vie = 100
        self.adversaire_vie = 100
        self.combat_termine = False

    def attaquer(self):
        # Logique d'attaque
        self.adversaire_vie -= 10
        if self.adversaire_vie <= 0:
            self.combat_termine = True

    def defendre(self):
        # Logique de défense
        self.joueur_vie -= 5
        if self.joueur_vie <= 0:
            self.combat_termine = True

    def mettre_a_jour(self):
        # Mettre à jour l'état du combat
        pass

    def dessiner(self, surface):
        # Dessiner les éléments du combat
        font = pygame.font.Font(None, 36)
        joueur_vie_text = font.render(f'Joueur Vie: {self.joueur_vie}', True, (255, 255, 255))
        adversaire_vie_text = font.render(f'Adversaire Vie: {self.adversaire_vie}', True, (255, 255, 255))
        surface.blit(joueur_vie_text, (10, 10))
        surface.blit(adversaire_vie_text, (10, 50))

class EcranJeu:
    def __init__(self):
        self.fond_animation = AnimationLoop(image_loader, 'img/IPI_fond_chill', (700, 700), 0, 0)
        self.debut_combat_animation = AnimationSprite(image_loader, 'img/IPI_fight', (700, 700))
        self.joueur_animation = AnimationLoop(image_loader, 'img/IPI_Basic', (500, 500), 100, 200, appliquer_gravite=True)  # Position initiale ajustée
        self.debut_combat_termine = False
        self.combat_system = CombatSystem(self.joueur_animation)

    def gerer_evenements(self, evenement):
        if evenement.type == pygame.KEYDOWN:
            if evenement.key == pygame.K_ESCAPE:
                return 'menu'  # Retourner au menu
            elif evenement.key == pygame.K_a:
                self.combat_system.attaquer()
            elif evenement.key == pygame.K_d:
                self.combat_system.defendre()
            elif evenement.key == pygame.K_LEFT:
                self.joueur_animation.vitesse_x = -5
            elif evenement.key == pygame.K_RIGHT:
                self.joueur_animation.vitesse_x = 5
            elif evenement.key == pygame.K_UP and not self.joueur_animation.en_air:
                self.joueur_animation.vitesse_y = -10  # Sauter
        elif evenement.type == pygame.KEYUP:
            if evenement.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                self.joueur_animation.vitesse_x = 0
        return 'jeu'

    def mettre_a_jour(self):
        self.fond_animation.mettre_a_jour()
        if not self.debut_combat_termine:
            self.debut_combat_animation.mettre_a_jour()
            if self.debut_combat_animation.animation_finie:
                self.debut_combat_termine = True
        else:
            self.joueur_animation.mettre_a_jour()
            self.combat_system.mettre_a_jour()

    def dessiner(self, surface):
        surface.fill((0, 0, 0))
        self.fond_animation.dessiner(surface)
        if not self.debut_combat_termine:
            self.debut_combat_animation.dessiner(surface, 0, 0)
        else:
            self.joueur_animation.dessiner(surface)
            self.combat_system.dessiner(surface)

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