import pygame
import engine
import globalVars


heart_img_set = [
    pygame.transform.scale(pygame.image.load("Assets/pickups/heart.png"), (30, 24))
]
invinsible_img_set = [
    pygame.transform.scale(pygame.image.load("Assets/pickups/invinsible.png"), (30, 30))
]


# Create coin entity
def make_coin(x, y):
    entity = engine.Entity()
    entity.position = engine.Position(
        x, y, globalVars.COIN_SIZE[0], globalVars.COIN_SIZE[1]
    )
    entity.animations.add("idle", globalVars.COIN_ANIMATION)
    entity.type = "collectable"
    return entity


# Health powerup trigger (check if player health is full)
def check_health(entity):
    if entity.health.health == globalVars.MAX_PLAYER_HEALTH:
        return False
    else:
        return True


# Health powerup apply
def regain_health(entity):
    entity.health.health = globalVars.MAX_PLAYER_HEALTH  # Refill health


def make_invinsible(entity):
    entity.health.health = globalVars.MAX_PLAYER_HEALTH  # Keep refilling health to max
    entity.animations.alpha = 120  # Make player transparent


# When invinsibility ends
def invinsible_end(entity):
    globalVars.sound_manager.play_sfx(entity.effect.sfx)
    entity.animations.alpha = 255  # Stop player transparancy


# Contains all powerup related info
powerup_dict = {
    "health": [regain_health, 0, "hp", None, check_health, heart_img_set],
    "invinsibility": [
        make_invinsible,
        500,
        "hp",
        invinsible_end,
        None,
        invinsible_img_set,
    ],
}

# Create a powerup
def make_powerup(type, x, y):
    entity = engine.Entity()
    entity.position = engine.Position(x, y, 30, 30)
    entity.animations.add("idle", engine.Animation(powerup_dict[type][5]))
    entity.effect = engine.Effect(
        powerup_dict[type][0],
        powerup_dict[type][1],
        powerup_dict[type][2],
        powerup_dict[type][3],
        powerup_dict[type][4],
    )
    return entity


# Create enemy entity
def make_enemy(x, y, direction):
    entity = engine.Entity()
    entity.position = engine.Position(
        x, y, globalVars.ENEMY_SIZE[0], globalVars.ENEMY_SIZE[1]
    )
    entity.animations.add("idle", globalVars.ENEMY_ANIMATION)
    entity.type = "enemy"
    entity.direction = direction
    return entity


# Set a player's spawn position and create his camera and attributes
def make_player(index):
    player = engine.Entity()
    player.position = engine.Position(
        0,
        0,
        globalVars.PLAYER_SIZE[0],
        globalVars.PLAYER_SIZE[1],
    )
    player.type = "player"
    player.direction = "right"
    player.speed = globalVars.PLAYER_SPEED
    player.player_index = index
    player.coins = engine.Coins()
    player.health = engine.Health()
    # Sets player1 parameters
    if index == 1:
        for a in globalVars.PLAYER_ANIMATION_1.keys():
            player.animations.add(a, globalVars.PLAYER_ANIMATION_1[a])
        player.camera = engine.Camera(
            0, 0, globalVars.CAMERA_SIZE[0], globalVars.CAMERA_SIZE[1]
        )
        player.input = engine.Input(
            pygame.K_SPACE,
            pygame.K_s,
            pygame.K_a,
            pygame.K_d,
            pygame.K_q,
            pygame.K_e,
        )
    # Sets player2 parameters
    elif index == 2:
        for a in globalVars.PLAYER_ANIMATION_2.keys():
            player.animations.add(a, globalVars.PLAYER_ANIMATION_2[a])
        player.camera = engine.Camera(
            globalVars.WINDOW_SIZE[0] - globalVars.CAMERA_SIZE[0],
            0,
            globalVars.CAMERA_SIZE[0],
            globalVars.CAMERA_SIZE[1],
        )
        player.input = engine.Input(
            pygame.K_UP,
            pygame.K_DOWN,
            pygame.K_LEFT,
            pygame.K_RIGHT,
            pygame.K_KP_PLUS,
            pygame.K_KP_MINUS,
        )
    player.camera.set_position(player.position.rect.x, player.position.rect.y)
    player.camera.track(player)
    player.control = engine.EntityControl()
    return player


def reset_player(player):
    player.health.health = globalVars.MAX_PLAYER_HEALTH
    player.coins.coins = 0
    player.state = "idle"
    player.animations.alpha = 255
    player.effect = None
