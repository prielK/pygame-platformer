import pygame
import os
import globalVars

pygame.init()


HEALTH_BAR_IMAGE = pygame.transform.scale(
    pygame.image.load(os.path.join("Assets", "UI", "health_bar.png")),
    globalVars.HEALTH_BAR_SIZE,
)
COIN_FONT = pygame.font.Font(os.path.join("Assets", "UI", "HighlandGothicFLF.ttf"), 20)
coin_image = pygame.transform.scale(
    pygame.image.load(os.path.join("Assets", "pickups", "coin.png")),
    globalVars.UI_COIN_SIZE,
)


def blit_alpha(target, source, location, opacity):
    x = location[0]
    y = location[1]
    temp = pygame.Surface((source.get_width(), source.get_height())).convert()
    temp.blit(target, (-x, -y))
    temp.blit(source, (0, 0))
    temp.set_alpha(opacity)
    target.blit(temp, location)


def draw_background(screen):
    screen.fill(globalVars.GREY)


def draw_platform(screen, platform_rect):
    pygame.draw.rect(screen, globalVars.GREEN, platform_rect)


def draw_HUD(screen, player_health, coin_count, index):
    # Draw UI (Health)
    if index == 1:  # player1 HUD
        full_health = pygame.Rect(
            globalVars.CAMERA_SIZE[0] // 16,
            globalVars.CAMERA_SIZE[1] // 31,
            globalVars.HEALTH_BAR_SIZE[0] - globalVars.HEALTH_BAR_SIZE[0] // 5,
            globalVars.HEALTH_BAR_SIZE[1] // 2,
        )
        health = pygame.Rect(
            globalVars.CAMERA_SIZE[0] // 15,
            globalVars.CAMERA_SIZE[1] // 48,
            (player_health + globalVars.HEALTH_BAR_SIZE[0] // 8),
            globalVars.HEALTH_BAR_SIZE[1] - globalVars.HEALTH_BAR_SIZE[1] // 6,
        )
    elif index == 2:  # player2 HUD
        full_health = pygame.Rect(
            globalVars.WINDOW_SIZE[0]
            - globalVars.CAMERA_SIZE[0]
            + globalVars.CAMERA_SIZE[0] // 22,
            globalVars.CAMERA_SIZE[1] // 31,
            globalVars.HEALTH_BAR_SIZE[0] - globalVars.HEALTH_BAR_SIZE[0] // 5,
            globalVars.HEALTH_BAR_SIZE[1] // 2,
        )
        health = pygame.Rect(
            globalVars.WINDOW_SIZE[0]
            - globalVars.CAMERA_SIZE[0]
            + globalVars.CAMERA_SIZE[0] // 20,
            globalVars.CAMERA_SIZE[1] // 48,
            (player_health + globalVars.HEALTH_BAR_SIZE[0] // 8),
            globalVars.HEALTH_BAR_SIZE[1] - globalVars.HEALTH_BAR_SIZE[1] // 6,
        )

    if player_health == globalVars.MAX_PLAYER_HEALTH:
        pygame.draw.rect(screen, globalVars.GREEN, health)
        pygame.draw.rect(screen, globalVars.GREEN, full_health)
    elif player_health >= 70:
        pygame.draw.rect(screen, globalVars.GREEN, health)
    elif player_health >= 40:
        pygame.draw.rect(screen, globalVars.YELLOW, health)
    elif player_health >= 10:
        pygame.draw.rect(screen, globalVars.RED, health)

    # Draw UI
    coins_text = COIN_FONT.render(str(coin_count), True, globalVars.COPPER)
    if index == 1:
        screen.blit(HEALTH_BAR_IMAGE, globalVars.HEALTH_BAR_POS1)
        screen.blit(
            coins_text,
            coins_text.get_rect(
                topleft=(
                    globalVars.UI_COIN_SIZE[0] * 3,
                    globalVars.HEALTH_BAR_SIZE[1] + globalVars.HEALTH_BAR_SIZE[1] // 5,
                )
            ),
        )
        screen.blit(
            coin_image,
            (globalVars.HEALTH_BAR_SIZE[0] // 4, globalVars.HEALTH_BAR_SIZE[1] + 10),
        )
    elif index == 2:
        screen.blit(HEALTH_BAR_IMAGE, globalVars.HEALTH_BAR_POS2)
        screen.blit(
            coins_text,
            coins_text.get_rect(
                topleft=(
                    globalVars.WINDOW_SIZE[0]
                    - globalVars.CAMERA_SIZE[0]
                    + globalVars.UI_COIN_SIZE[0] * 3,
                    globalVars.HEALTH_BAR_SIZE[1] + globalVars.HEALTH_BAR_SIZE[1] // 5,
                )
            ),
        )
        screen.blit(
            coin_image,
            (
                globalVars.WINDOW_SIZE[0]
                - globalVars.CAMERA_SIZE[0]
                + globalVars.HEALTH_BAR_SIZE[0] // 4,
                globalVars.HEALTH_BAR_SIZE[1] + 10,
            ),
        )


# Draw win/lose message
def draw_text(screen, msg, color, x, y, alpha=255):
    message = pygame.font.SysFont("arial", 30).render(msg, True, color)
    blit_alpha(screen, message, (x, y), alpha)
