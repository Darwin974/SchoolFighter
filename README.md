# School Fighter

**School Fighter** est un jeu de combat où les professeurs s'affrontent dans des duels épiques. Ce projet est développé en Python avec la bibliothèque Pygame.

## Fonctionnalités

- **Menu principal** :
  - Fond animé avec le thème "IPI foret".
  - Musique de fond : "8bit-era.mp3".
  - Boutons pour démarrer le jeu, quitter ou accéder à un mode secret.

- **Mode de combat** :
  - Deux joueurs s'affrontent :
    - Joueur 1 (contrôlé avec les flèches).
    - Joueur 2 (contrôlé avec ZQSD).
  - Animations personnalisées pour chaque personnage.
  - Mode secret avec un personnage spécial (Schrauder) et une carte unique.

- **Effets sonores** :
  - Son "powerup.mp3" joué lors du retour au menu.
  - Musique de combat différente pour chaque mode :
    - Mode normal : "Spider Dance.mp3".
    - Mode secret : "FinalBoss.mp3".

- **Système de points de vie** :
  - Les joueurs commencent avec des points de vie différents selon le mode :
    - Mode normal : Joueur 1 (100 PV), Joueur 2 (100 PV).
    - Mode secret : Joueur 1 (175 PV), Joueur 2 (300 PV).

## Contrôles

- **Joueur 1** :
  - Flèche gauche/droite : Se déplacer.
  - Flèche haut : Sauter.
  - Touche `A` : Attaquer.

- **Joueur 2** :
  - Touche `Q`/`D` : Se déplacer.
  - Touche `Z` : Sauter.
  - Barre d'espace : Attaquer.

- **Général** :
  - Échap : Retourner au menu principal.

## Installation

1. Téléchargez ce dépôt

2. Installez les dépendances :
```shell
pip install -r requirements.txt
```

3. Lancez le jeu :
```shell
cd SchoolFighter
python sources/main.py
```

## Dépendances
- Python 3.x
- Pygame

## License
Ce projet est sous licence [GNU GPL v3](https://github.com/Darwin974/SchoolFighter/blob/main/license.txt). Vous êtes libre de l'utiliser, de le modifier et de le redistribuer sous les termes de cette licence.