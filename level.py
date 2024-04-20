import pygame
import globalVars
import util


class Level:
    def __init__(self, platforms=None, entities=None, lose_func=None, win_func=None):
        self.platforms = platforms
        self.entities = entities
        self.lose_func = lose_func
        self.win_func = win_func

    def is_lost(self):
        if self.lose_func is None:
            return False
        return self.lose_func(self)

    def is_won(self):
        if self.win_func is None:
            return False
        return self.win_func(self)


# Lose if all players died or fell off the map
def lost_level(level):
    # Check if any player alive
    for entity in level.entities:
        if entity.type == "player" and entity.health.health > 0:
            return False
    # If all players died
    return True


# Win if collected all coins
def won_level(level):
    # Check if any coins still exist on the level
    for entity in level.entities:
        if entity.type == "collectable":
            return False
    # If no coins remaining
    return True


# Set player spawn point
def spawn_player(player, level_index):
    player.position.rect.x = globalVars.STARTING_POS[level_index - 1][0]
    player.position.rect.y = globalVars.STARTING_POS[level_index - 1][1]
    player.fall_vel = 0
    player.direction = "right"
    if player.player_index == 2:
        player.position.rect.x += 30
    player.camera.set_position(player.position.rect.x, player.position.rect.y)


# Loads a level
def load_level(index):
    # Create level list
    levels = {
        1: Level(
            platforms=[
                pygame.Rect(100, 300, 400, 50),
                pygame.Rect(100, 250, 50, 50),
                pygame.Rect(450, 250, 50, 50),
                pygame.Rect(500, 400, 250, 50),
                pygame.Rect(500, 350, 50, 50),
                pygame.Rect(700, 350, 50, 50),
                pygame.Rect(380, 200, 50, 50),
            ],
            entities=[
                util.make_coin(450, 200),
                util.make_coin(700, 320),
                util.make_enemy(100, 175, "right"),
                util.make_powerup("health", 400, 250),
            ],
            lose_func=lost_level,
            win_func=won_level,
        ),
        2: Level(
            platforms=[
                pygame.Rect(100, 300, 1000, 50),
            ],
            entities=[
                util.make_coin(450, 200),
            ],
            lose_func=lost_level,
            win_func=won_level,
        ),
        3: Level(
            platforms=[
                pygame.Rect(100, 300, 400, 50),
                pygame.Rect(400, 200, 1000, 50),
                pygame.Rect(500, 400, 400, 50),
            ],
            entities=[
                util.make_coin(650, 150),
                util.make_powerup("invinsibility", 500, 150),
                util.make_enemy(600, 300, "left"),
            ],
            lose_func=lost_level,
            win_func=won_level,
        ),
    }

    globalVars.world = levels[index]  # Set level

    # Add the players
    for player in globalVars.players:
        spawn_player(player, index)
        globalVars.world.entities.append(player)
