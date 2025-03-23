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
        self.image_loader = image_loader
        self.dossier = dossier
        self.taille = taille
        self.images = image_loader.charger_images(dossier, taille)
        self.sprite_actuel = 0
        self.vitesse_sprite = 0.18
        self.x = x
        self.y = y
        self.vitesse_x = 0
        self.vitesse_y = 0
        self.en_air = False  # Indique si le joueur est en l'air
        self.sol = 100  # Position du sol ajustée (plus élevée)
        self.appliquer_gravite = appliquer_gravite
        self.direction = 'right'  # Direction initiale du joueur
        self.animation_temporaire = None
        self.animation_temporaire_duree = 0

    def changer_animation(self, dossier_temporaire, duree):
        self.animation_temporaire = self.image_loader.charger_images(dossier_temporaire, self.taille)
        self.animation_temporaire_duree = duree
        self.sprite_actuel = 0  # Réinitialiser l'index de l'animation

    def mettre_a_jour(self):
        self.sprite_actuel += self.vitesse_sprite
        if self.sprite_actuel >= len(self.images):
            self.sprite_actuel = 0  # Réinitialiser l'index si nécessaire
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

        # Gérer l'animation temporaire
        if self.animation_temporaire:
            self.animation_temporaire_duree -= 1
            if self.animation_temporaire_duree <= 0:
                self.animation_temporaire = None

        # Réapparaître de l'autre côté de l'écran
        if self.x < -self.taille[0]:
            self.x = 700 - self.taille[0] / 2
        elif self.x > 700:
            self.x = -self.taille[0] / 2

    def dessiner(self, surface):
        if self.animation_temporaire:
            # Vérifiez que l'index est valide
            if int(self.sprite_actuel) >= len(self.animation_temporaire):
                self.sprite_actuel = 0  # Réinitialiser l'index si nécessaire
            image = self.animation_temporaire[int(self.sprite_actuel)]
        else:
            # Vérifiez que l'index est valide pour l'animation normale
            if int(self.sprite_actuel) >= len(self.images):
                self.sprite_actuel = 0  # Réinitialiser l'index si nécessaire
            image = self.images[int(self.sprite_actuel)]
        if self.direction == 'left':
            image = pygame.transform.flip(image, True, False)
        surface.blit(image, (self.x, self.y))

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
        if self.file:  # Si un fichier est fourni
            self.animation = AnimationLoop(image_loader, self.file, (self.sx, self.sy), self.x, self.y)
        else:  # Si aucun fichier n'est fourni (bouton caché)
            self.animation = None

    # Dessiner le bouton sur l'écran
    def showButton(self, display):
        if self.animation:  # Ne dessine que si une animation est définie
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
        # Positionner le logo au centre de la fenêtre, mais remonter légèrement
        logo_x = (700 - 640) // 2
        logo_y = (700 - 426) // 2 - 50  # Remonter le logo de 50 pixels
        self.logo_animation = AnimationLoop(image_loader, 'data/img/IPI_logo', (640, 420), logo_x, logo_y)  # Chemin, taille et position du logo
        # Ajouter une animation de fond
        self.fond_animation = AnimationLoop(image_loader, 'data/img/IPI foret', (700, 700), 0, 0)  # Chemin, taille et position du fond
        self.buttons = [
            Button(250, 435, 200, 100, 'data/img/IPI start', 'jeu'),
            Button(250, 535, 200, 100, 'data/img/IPI quit', 'exit'),
            Button(0, 0, 50, 50, None, 'secret')  # Bouton caché en haut à gauche
        ]
        
        # Charger le son pour le bouton Start
        self.start_sound = pygame.mixer.Sound('data/sounds/8-bit-game-sfx-sound-21.mp3')
        # Charger le son pour la touche Échap
        self.escape_sound = pygame.mixer.Sound('data/sounds/powerup.mp3')

        # Jouer la musique de fond pour le menu
        pygame.mixer.music.load('data/music/8bit-era.mp3')  # Charger la musique "8bit-era.mp3"
        pygame.mixer.music.set_volume(0.3)  # Régler le volume à 30%
        pygame.mixer.music.play(-1)  # Jouer en boucle (-1 pour répéter indéfiniment)

    def gerer_evenements(self, evenement):
        if evenement.type == pygame.MOUSEBUTTONDOWN:
            mousepos = pygame.mouse.get_pos()
            mouseclick = pygame.mouse.get_pressed()
            for button in self.buttons:
                target_screen = button.focusCheck(mousepos, mouseclick)
                if target_screen:
                    if target_screen == 'jeu':  # Si le bouton "Start" est cliqué
                        self.start_sound.play()  # Jouer le son
                    elif target_screen == 'secret':  # Si le bouton caché est cliqué
                        return 'secret'  # Aller à l'écran secret
                    return target_screen
        elif evenement.type == pygame.KEYDOWN:
            if evenement.key == pygame.K_ESCAPE:
                self.escape_sound.play()  # Jouer le son "powerup.mp3"
                return 'exit'  # Quitter le jeu
        return 'menu'

    def mettre_a_jour(self):
        self.logo_animation.mettre_a_jour()
        self.fond_animation.mettre_a_jour()
        for button in self.buttons:
            if button.animation:  # Ne met à jour que si une animation est définie
                button.animation.mettre_a_jour()

    def dessiner(self, surface):
        surface.fill((0, 0, 0))
        self.fond_animation.dessiner(surface)  # Dessiner le fond animé
        self.logo_animation.dessiner(surface)
        for button in self.buttons:
            button.showButton(surface)

class CombatSystem:
    def __init__(self, joueur_animation, adversaire_animation):
        self.joueur_animation = joueur_animation
        self.adversaire_animation = adversaire_animation
        self.joueur_vie = 100
        self.adversaire_vie = 100
        self.combat_termine = False

        # Charger le son de dégâts
        self.explosion_sound = pygame.mixer.Sound('data/sounds/explosion.mp3')

    def attaquer_joueur(self):
        # Vérifier si l'animation d'attaque précédente est terminée
        if self.joueur_animation.animation_temporaire is None:
            # Changer l'animation pour l'attaque pendant 80 frames
            self.joueur_animation.changer_animation('data/img/IPI_attaque', 80)

    def attaquer_adversaire(self):
        # Vérifier si l'animation d'attaque précédente est terminée
        if self.adversaire_animation.animation_temporaire is None:
            # Si le joueur 2 est Schrauder (mode secret), utiliser son animation d'attaque spécifique
            if self.adversaire_animation.dossier == 'data/img/IPI shrauder basic':
                self.adversaire_animation.changer_animation('data/img/IPIShrauderAttaque', 100)  # 100 frames pour le mode secret
            else:
                # Sinon, utiliser l'animation d'attaque par défaut
                self.adversaire_animation.changer_animation('data/img/IPI attaque katana', 120)  # 120 frames pour le mode normal

    def mettre_a_jour(self):
        # Vérifier si l'animation d'attaque du joueur est terminée
        if self.joueur_animation.animation_temporaire is not None:
            self.joueur_animation.animation_temporaire_duree -= 1
            if self.joueur_animation.animation_temporaire_duree <= 0:
                joueur_hitbox = pygame.Rect(
                    self.joueur_animation.x + self.joueur_animation.taille[0] * 0.35,
                    self.joueur_animation.y + self.joueur_animation.taille[1] * 0.1,
                    self.joueur_animation.taille[0] * 0.22,
                    self.joueur_animation.taille[1] * 0.62
                )
                # Calculer la hitbox de l'adversaire
                if self.adversaire_animation.dossier == 'data/img/IPI shrauder basic':  # Mode secret
                    adversaire_hitbox = pygame.Rect(
                        self.adversaire_animation.x + self.adversaire_animation.taille[0] * 0.2,
                        self.adversaire_animation.y + self.adversaire_animation.taille[1] * 0.1,
                        self.adversaire_animation.taille[0] * 0.4,  # Largeur doublée
                        self.adversaire_animation.taille[1] * 1.2   # Hauteur doublée
                    )
                else:  # Mode normal
                    adversaire_hitbox = pygame.Rect(
                        self.adversaire_animation.x + self.adversaire_animation.taille[0] * 0.4,
                        self.adversaire_animation.y + self.adversaire_animation.taille[1] * 0.2,
                        self.adversaire_animation.taille[0] * 0.2,
                        self.adversaire_animation.taille[1] * 0.6
                    )

                # Vérifier la collision entre les hitboxes
                if joueur_hitbox.colliderect(adversaire_hitbox):
                    self.adversaire_vie -= 10
                    self.explosion_sound.play()  # Jouer le son de dégâts
                    if self.adversaire_vie <= 0:
                        self.combat_termine = True
                self.joueur_animation.animation_temporaire = None

        # Vérifier si l'animation d'attaque de l'adversaire est terminée
        if self.adversaire_animation.animation_temporaire is not None:
            self.adversaire_animation.animation_temporaire_duree -= 1
            if self.adversaire_animation.animation_temporaire_duree <= 0:
                joueur_hitbox = pygame.Rect(
                    self.joueur_animation.x + self.joueur_animation.taille[0] * 0.35,
                    self.joueur_animation.y + self.joueur_animation.taille[1] * 0.1,
                    self.joueur_animation.taille[0] * 0.3,
                    self.joueur_animation.taille[1] * 0.8
                )
                # Calculer la hitbox de l'adversaire
                if self.adversaire_animation.dossier == 'data/img/IPI shrauder basic':  # Mode secret
                    adversaire_hitbox = pygame.Rect(
                        self.adversaire_animation.x + self.adversaire_animation.taille[0] * 0.2,
                        self.adversaire_animation.y + self.adversaire_animation.taille[1] * 0.1,
                        self.adversaire_animation.taille[0] * 0.4,  # Largeur doublée
                        self.adversaire_animation.taille[1] * 1.2   # Hauteur doublée
                    )
                else:  # Mode normal
                    adversaire_hitbox = pygame.Rect(
                        self.adversaire_animation.x + self.adversaire_animation.taille[0] * 0.4,
                        self.adversaire_animation.y + self.adversaire_animation.taille[1] * 0.2,
                        self.adversaire_animation.taille[0] * 0.2,
                        self.adversaire_animation.taille[1] * 0.6
                    )

                # Vérifier la collision entre les hitboxes
                if adversaire_hitbox.colliderect(joueur_hitbox):
                    self.joueur_vie -= 10
                    self.explosion_sound.play()  # Jouer le son de dégâts
                    if self.joueur_vie <= 0:
                        self.combat_termine = True
                self.adversaire_animation.animation_temporaire = None

    def defendre_joueur(self):
        # Logique de défense du joueur
        self.joueur_vie -= 5
        if self.joueur_vie <= 0:
            self.combat_termine = True

    def defendre_adversaire(self):
        # Logique de défense de l'adversaire
        self.adversaire_vie -= 5
        if self.adversaire_vie <= 0:
            self.combat_termine = True

    def dessiner(self, surface):
        # Dessiner les points de vie des joueurs
        font = pygame.font.Font(None, 36)
        
        # Texte pour le joueur 1 (à gauche)
        joueur_vie_text = font.render(f'J1 pv : {self.joueur_vie}', True, (255, 255, 255))
        surface.blit(joueur_vie_text, (10, 10))  # Position en haut à gauche
        
        # Texte pour le joueur 2 (à droite)
        adversaire_vie_text = font.render(f'J2 pv : {self.adversaire_vie}', True, (255, 255, 255))
        surface.blit(adversaire_vie_text, (700 - adversaire_vie_text.get_width() - 10, 10))  # Position en haut à droite

class EcranJeu:
    def __init__(self):
        self.fond_animation = AnimationLoop(image_loader, 'data/img/IPI_fond_chill', (700, 700), 0, 0)
        self.debut_combat_animation = AnimationSprite(image_loader, 'data/img/IPI_fight', (700, 700))
        
        # Positionner le joueur contrôlé par les flèches à gauche
        self.joueur_animation = AnimationLoop(image_loader, 'data/img/IPI_Basic', (500, 500), -100, 300, appliquer_gravite=True)
        
        # Positionner le joueur contrôlé par zqsd à droite
        self.adversaire_animation = AnimationLoop(image_loader, 'data/img/IPI Basic Katana', (500, 500), 300, 200, appliquer_gravite=True)
        
        self.debut_combat_termine = False
        self.combat_system = CombatSystem(self.joueur_animation, self.adversaire_animation)
        
        # Animation de victoire
        self.victoire_animation = None

        # Charger les sons
        self.ready_fight_sound = pygame.mixer.Sound('data/sounds/ready-fight.mp3')
        self.victory_sound = pygame.mixer.Sound('data/sounds/victory.mp3')  # Charger le son de victoire

    def reinitialiser(self, secret_mode=False):
        # Réinitialiser les animations des joueurs
        self.joueur_animation = AnimationLoop(image_loader, 'data/img/IPI_Basic', (500, 500), -100, 300, appliquer_gravite=True)
        
        if secret_mode:
            # Mode secret : joueur 2 avec Schrauder
            self.adversaire_animation = AnimationLoop(image_loader, 'data/img/IPI shrauder basic', (500, 500), 300, 200, appliquer_gravite=True)
            self.combat_system = CombatSystem(self.joueur_animation, self.adversaire_animation)
            self.combat_system.adversaire_vie = 300  # Donner 300 PV au joueur 2
            self.fond_animation = AnimationLoop(image_loader, 'data/img/IPI_TerrainSchrauder', (700, 700), 0, 0)
            self.debut_combat_animation = AnimationSprite(image_loader, 'data/img/IPI_Shrauder', (700, 700))
            
            # Points de vie et musique pour le mode secret
            self.combat_system.joueur_vie = 175  # Joueur 1 à 175 PV
            pygame.mixer.music.load('data/music/FinalBoss.mp3')  # Musique "FinalBoss.mp3"
            pygame.mixer.music.set_volume(0.35)  # Augmenter le volume à 35% pour le mode secret
        else:
            # Mode normal
            self.adversaire_animation = AnimationLoop(image_loader, 'data/img/IPI Basic Katana', (500, 500), 300, 200, appliquer_gravite=True)
            self.combat_system = CombatSystem(self.joueur_animation, self.adversaire_animation)
            self.fond_animation = AnimationLoop(image_loader, 'data/img/IPI_fond_chill', (700, 700), 0, 0)
            self.debut_combat_animation = AnimationSprite(image_loader, 'data/img/IPI_fight', (700, 700))
            
            # Jouer le son "ready-fight.mp3" uniquement en mode normal
            self.ready_fight_sound.play()
            
            # Points de vie et musique pour le mode normal
            self.combat_system.joueur_vie = 100  # Joueur 1 à 100 PV
            self.combat_system.adversaire_vie = 100  # Joueur 2 à 100 PV
            pygame.mixer.music.load('data/music/Spider Dance.mp3')  # Musique "Spider Dance.mp3"
            pygame.mixer.music.set_volume(0.25)  # Volume à 25% pour le mode normal

        # Réinitialiser l'état du combat
        self.debut_combat_termine = False
        self.victoire_animation = None

        # Jouer la musique de combat
        pygame.mixer.music.play(-1)  # Jouer en boucle (-1 pour répéter indéfiniment)

    def gerer_evenements(self, evenement):
        # Permettre de retourner au menu même si le combat est terminé
        if evenement.type == pygame.KEYDOWN:
            if evenement.key == pygame.K_ESCAPE:
                ecrans['menu'].escape_sound.play()  # Jouer le son "powerup.mp3"
                return 'menu'  # Retourner au menu

            # Empêcher les personnages de bouger si le combat est terminé
            if self.victoire_animation is not None:
                return 'jeu'

            # Gestion des autres touches
            if evenement.key == pygame.K_a:  # Attaque pour le joueur contrôlé par les flèches
                self.combat_system.attaquer_joueur()
            elif evenement.key == pygame.K_q:
                self.joueur_animation.vitesse_x = -5
                self.joueur_animation.direction = 'left'
            elif evenement.key == pygame.K_d:
                self.joueur_animation.vitesse_x = 5
                self.joueur_animation.direction = 'right'
            elif evenement.key == pygame.K_z and not self.joueur_animation.en_air:
                self.joueur_animation.vitesse_y = -10  # Sauter
            elif evenement.key == pygame.K_SPACE:  # Attaque pour le joueur contrôlé par zqsd
                self.combat_system.attaquer_adversaire()
            elif evenement.key == pygame.K_LEFT:
                self.adversaire_animation.vitesse_x = -5
                self.adversaire_animation.direction = 'left'
                # Si Schrauder marche, changer l'animation
                if self.adversaire_animation.dossier == 'data/img/IPI shrauder basic':
                    self.adversaire_animation.changer_animation('data/img/IPI_shrauderMarche', 30)
            elif evenement.key == pygame.K_RIGHT:
                self.adversaire_animation.vitesse_x = 5
                self.adversaire_animation.direction = 'right'
                # Si Schrauder marche, changer l'animation
                if self.adversaire_animation.dossier == 'data/img/IPI shrauder basic':
                    self.adversaire_animation.changer_animation('data/img/IPI_shrauderMarche', 30)
            elif evenement.key == pygame.K_UP and not self.adversaire_animation.en_air:
                self.adversaire_animation.vitesse_y = -10  # Sauter
        elif evenement.type == pygame.KEYUP:
            if evenement.key in [pygame.K_q, pygame.K_d]:
                self.joueur_animation.vitesse_x = 0
            elif evenement.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                self.adversaire_animation.vitesse_x = 0
                # Réinitialiser l'animation de Schrauder lorsqu'il s'arrête
                if self.adversaire_animation.dossier == 'data/img/IPI shrauder basic':
                    self.adversaire_animation.changer_animation('data/img/IPI shrauder basic', 30)
        return 'jeu'

    def mettre_a_jour(self):
        # Vérifier si le combat est terminé
        if self.combat_system.joueur_vie <= 0 and self.victoire_animation is None:
            self.victoire_animation = AnimationSprite(image_loader, 'data/img/IPI2win', (700, 700))  # Adversaire gagne
            self.victory_sound.play()  # Jouer le son de victoire
            return
        elif self.combat_system.adversaire_vie <= 0 and self.victoire_animation is None:
            self.victoire_animation = AnimationSprite(image_loader, 'data/img/IPI1win', (700, 700))  # Joueur gagne
            self.victory_sound.play()  # Jouer le son de victoire
            return

        self.fond_animation.mettre_a_jour()
        if not self.debut_combat_termine:
            self.debut_combat_animation.mettre_a_jour()
            if self.debut_combat_animation.animation_finie:
                self.debut_combat_termine = True
        else:
            self.joueur_animation.mettre_a_jour()
            self.adversaire_animation.mettre_a_jour()
            self.combat_system.mettre_a_jour()

        # Mettre à jour l'animation de victoire si elle existe
        if self.victoire_animation is not None:
            self.victoire_animation.mettre_a_jour()

    def dessiner(self, surface):
        surface.fill((0, 0, 0))
        self.fond_animation.dessiner(surface)
        if not self.debut_combat_termine:
            self.debut_combat_animation.dessiner(surface, 0, 0)
        else:
            self.joueur_animation.dessiner(surface)
            self.adversaire_animation.dessiner(surface)
            self.combat_system.dessiner(surface)

        # Dessiner l'animation de victoire si le combat est terminé
        if self.victoire_animation is not None:
            self.victoire_animation.dessiner(surface, 0, 0)  # Afficher à (0, 0)

def fondu_transition(ecran, couleur, duree):
    """
    Effectue un fondu de transition.
    :param ecran: Surface de l'écran.
    :param couleur: Couleur du fondu (ex. (0, 0, 0) pour noir).
    :param duree: Durée du fondu en millisecondes.
    """
    fondu_surface = pygame.Surface(ecran.get_size())
    fondu_surface.fill(couleur)
    for alpha in range(0, 255, 5):  # Augmente progressivement l'alpha
        fondu_surface.set_alpha(alpha)
        ecran.blit(fondu_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(duree // 51)  # Ajuste la vitesse du fondu

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
            # Ajouter un fondu lors du changement d'écran
            fondu_transition(ecran, (0, 0, 0), 500)  # Couleur noire, durée 500ms
            if nouvel_ecran == 'jeu':  # Si on retourne à l'écran de jeu
                ecrans['jeu'].reinitialiser()  # Réinitialiser l'écran de jeu
            elif nouvel_ecran == 'secret':  # Si on va à l'écran secret
                ecrans['jeu'].reinitialiser(secret_mode=True)  # Activer le mode secret
                nouvel_ecran = 'jeu'
            elif nouvel_ecran == 'menu':  # Si on retourne au menu
                pygame.mixer.music.load('data/music/8bit-era.mp3')  # Relancer la musique du menu
                pygame.mixer.music.set_volume(0.3)  # Régler le volume
                pygame.mixer.music.play(-1)  # Jouer en boucle
            elif ecran_actuel == 'jeu':  # Si on quitte l'écran de jeu
                pygame.mixer.music.stop()  # Arrêter la musique de combat
            ecran_actuel = nouvel_ecran

    # Mettre à jour l'écran actuel
    ecrans[ecran_actuel].mettre_a_jour()

    # Dessiner l'écran actuel
    ecrans[ecran_actuel].dessiner(ecran)

    # Mettre à jour l'affichage
    pygame.display.flip()

    # Limiter la fréquence d'images par seconde
    horloge.tick(60)