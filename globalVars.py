import pygame
import os
import sound
import engine


# CONSTANTS:

# Main
WINDOW_SIZE = (1280, 720)

# Engine
GRAVITY = 0.3
ENEMY_DAMAGE = 15
PLAYER_SPEED = 4
JUMP_FORCE = 10
FIRST_LEVEL_INDEX = 1
LAST_LEVEL_INDEX = 3
MAX_PLAYER_HEALTH = 100

# Util
COIN_SIZE = (15, 15)
ENEMY_SIZE = (48, 76)
PLAYER_SIZE = (30, 45)
STARTING_POS = ((300, 10), (200, 200), (200, 200))
CAMERA_SIZE = (WINDOW_SIZE[0] // 2 - WINDOW_SIZE[0] // 80, WINDOW_SIZE[1])

# Colors
WHITE = (255, 255, 255)
GREY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (50, 205, 50)
YELLOW = (255, 255, 0)
COPPER = (204, 102, 0)
BLACK = (0, 0, 0)

# Draw
HEALTH_BAR_SIZE = (CAMERA_SIZE[0] // 4, CAMERA_SIZE[1] // 15)
UI_COIN_SIZE = (22, 22)
HEALTH_BAR_POS1 = (10, 10)
HEALTH_BAR_POS2 = (WINDOW_SIZE[0] - CAMERA_SIZE[0], 10)
MAX_OPACITY = 255
PLAYER_SELECT_IMAGE = pygame.transform.scale(
    pygame.image.load(os.path.join("Assets", "player", "idle-00.png")),
    PLAYER_SIZE,
)


# Animations
COIN_ANIMATION = engine.Animation(
    [
        pygame.transform.scale(
            pygame.image.load(os.path.join("Assets", "pickups", "coin_0.png")),
            COIN_SIZE,
        ),
        pygame.transform.scale(
            pygame.image.load(os.path.join("Assets", "pickups", "coin_1.png")),
            COIN_SIZE,
        ),
        pygame.transform.scale(
            pygame.image.load(os.path.join("Assets", "pickups", "coin_2.png")),
            COIN_SIZE,
        ),
        pygame.transform.scale(
            pygame.image.load(os.path.join("Assets", "pickups", "coin_3.png")),
            COIN_SIZE,
        ),
        pygame.transform.scale(
            pygame.image.load(os.path.join("Assets", "pickups", "coin_4.png")),
            COIN_SIZE,
        ),
        pygame.transform.scale(
            pygame.image.load(os.path.join("Assets", "pickups", "coin_5.png")),
            COIN_SIZE,
        ),
        pygame.transform.scale(
            pygame.image.load(os.path.join("Assets", "pickups", "coin_6.png")),
            COIN_SIZE,
        ),
        pygame.transform.scale(
            pygame.image.load(os.path.join("Assets", "pickups", "coin_7.png")),
            COIN_SIZE,
        ),
    ],
)
ENEMY_ANIMATION = engine.Animation(
    [
        pygame.transform.scale(
            pygame.image.load(os.path.join("Assets", "enemies", "enemy_ready_0.png")),
            ENEMY_SIZE,
        ),
        pygame.transform.scale(
            pygame.image.load(os.path.join("Assets", "enemies", "enemy_ready_1.png")),
            ENEMY_SIZE,
        ),
        pygame.transform.scale(
            pygame.image.load(os.path.join("Assets", "enemies", "enemy_ready_2.png")),
            ENEMY_SIZE,
        ),
        pygame.transform.scale(
            pygame.image.load(os.path.join("Assets", "enemies", "enemy_ready_3.png")),
            ENEMY_SIZE,
        ),
        pygame.transform.scale(
            pygame.image.load(os.path.join("Assets", "enemies", "enemy_ready_4.png")),
            ENEMY_SIZE,
        ),
        pygame.transform.scale(
            pygame.image.load(os.path.join("Assets", "enemies", "enemy_ready_5.png")),
            ENEMY_SIZE,
        ),
    ],
)
PLAYER_ANIMATION_1 = {
    "idle": engine.Animation(
        [
            pygame.transform.scale(
                pygame.image.load(os.path.join("Assets", "player", "idle-00.png")),
                PLAYER_SIZE,
            ),
            pygame.transform.scale(
                pygame.image.load(os.path.join("Assets", "player", "idle-01.png")),
                PLAYER_SIZE,
            ),
            pygame.transform.scale(
                pygame.image.load(os.path.join("Assets", "player", "idle-02.png")),
                PLAYER_SIZE,
            ),
            pygame.transform.scale(
                pygame.image.load(os.path.join("Assets", "player", "idle-03.png")),
                PLAYER_SIZE,
            ),
        ],
    ),
    "running": engine.Animation(
        [
            pygame.transform.scale(
                pygame.image.load(os.path.join("Assets", "player", "run-00.png")),
                PLAYER_SIZE,
            ),
            pygame.transform.scale(
                pygame.image.load(os.path.join("Assets", "player", "run-01.png")),
                PLAYER_SIZE,
            ),
            pygame.transform.scale(
                pygame.image.load(os.path.join("Assets", "player", "run-02.png")),
                PLAYER_SIZE,
            ),
            pygame.transform.scale(
                pygame.image.load(os.path.join("Assets", "player", "run-03.png")),
                PLAYER_SIZE,
            ),
            pygame.transform.scale(
                pygame.image.load(os.path.join("Assets", "player", "run-05.png")),
                PLAYER_SIZE,
            ),
            pygame.transform.scale(
                pygame.image.load(os.path.join("Assets", "player", "run-05.png")),
                PLAYER_SIZE,
            ),
        ],
    ),
    "dead": engine.Animation(
        [
            pygame.transform.scale(
                pygame.image.load(os.path.join("Assets", "player", "idle-00.png")),
                PLAYER_SIZE,
            ),
            pygame.transform.scale(
                pygame.image.load(os.path.join("Assets", "player", "idle-00.png")),
                PLAYER_SIZE,
            ),
        ],
    ),
}

# Player2 image list
player2_idle_changed = []
player2_running_changed = []
player2_idle_animation = [
    pygame.transform.scale(
        pygame.image.load(os.path.join("Assets", "player", "idle-00.png")),
        PLAYER_SIZE,
    ),
    pygame.transform.scale(
        pygame.image.load(os.path.join("Assets", "player", "idle-01.png")),
        PLAYER_SIZE,
    ),
    pygame.transform.scale(
        pygame.image.load(os.path.join("Assets", "player", "idle-02.png")),
        PLAYER_SIZE,
    ),
    pygame.transform.scale(
        pygame.image.load(os.path.join("Assets", "player", "idle-03.png")),
        PLAYER_SIZE,
    ),
]
player2_running_animation = [
    pygame.transform.scale(
        pygame.image.load(os.path.join("Assets", "player", "run-00.png")),
        PLAYER_SIZE,
    ),
    pygame.transform.scale(
        pygame.image.load(os.path.join("Assets", "player", "run-01.png")),
        PLAYER_SIZE,
    ),
    pygame.transform.scale(
        pygame.image.load(os.path.join("Assets", "player", "run-02.png")),
        PLAYER_SIZE,
    ),
    pygame.transform.scale(
        pygame.image.load(os.path.join("Assets", "player", "run-03.png")),
        PLAYER_SIZE,
    ),
    pygame.transform.scale(
        pygame.image.load(os.path.join("Assets", "player", "run-05.png")),
        PLAYER_SIZE,
    ),
    pygame.transform.scale(
        pygame.image.load(os.path.join("Assets", "player", "run-05.png")),
        PLAYER_SIZE,
    ),
]
for image in player2_idle_animation:
    threshold_test = pygame.transform.threshold(
        dest_surf=image,
        surf=image,
        search_color=(255, 0, 0, 255),
        threshold=(85, 110, 100, 255),
        set_color=BLUE,
        inverse_set=True,
    )
    player2_idle_changed.append(image)
for image in player2_running_animation:
    threshold_test = pygame.transform.threshold(
        dest_surf=image,
        surf=image,
        search_color=(255, 0, 0, 255),
        threshold=(85, 110, 100, 255),
        set_color=BLUE,
        inverse_set=True,
    )
    player2_running_changed.append(image)

PLAYER_ANIMATION_2 = {
    "idle": engine.Animation(player2_idle_changed),
    "running": engine.Animation(player2_running_changed),
    "dead": engine.Animation(
        [player2_idle_animation[0]],
    ),
}


# NON-CONSTANTS:

# Game
world = None
player1 = None
player2 = None
players = []
level_index = 1
player_index = 1

# Sound
sound_manager = sound.SoundManager()
