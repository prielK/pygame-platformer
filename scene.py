import pygame
import draw
import globalVars
import engine
import ui
import level
import util


class Scene:
    def __init__(self):
        pass

    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def input(self, s_manager, input_stream):
        pass

    def update(self, s_manager, input_stream):
        pass

    def draw(self, s_manager, screen):
        pass


class MainMenuScene(Scene):
    def __init__(self):
        self.enter = ui.Button(pygame.K_RETURN, "Start Game", 200, 200)
        self.esc = ui.Button(pygame.K_ESCAPE, "Exit", 200, 250)

    def on_enter(self):
        globalVars.sound_manager.play_music("menu")

    def input(self, s_manager, input_stream):
        if input_stream.keyboard.key_pressed(pygame.K_ESCAPE):
            s_manager.pop()
        if input_stream.keyboard.key_pressed(pygame.K_RETURN):
            s_manager.push(FadeTransition([self], [PlayerSelectScene()]))

    def update(self, s_manager, input_stream):
        self.enter.update(input_stream)
        self.esc.update(input_stream)

    def draw(self, s_manager, screen):
        screen.fill(globalVars.BLACK)
        self.enter.draw(screen)
        self.esc.draw(screen)


class PlayerSelectScene(Scene):
    def __init__(self):
        self.esc = ui.Button(pygame.K_ESCAPE, "Main Menu", 300, 300)
        self.player_ptr = 1
        globalVars.player1 = util.make_player(1)
        globalVars.player2 = util.make_player(2)

    def on_enter(self):
        globalVars.sound_manager.play_music("menu")

    def input(self, s_manager, input_stream):
        if input_stream.keyboard.key_pressed(pygame.K_ESCAPE):
            s_manager.pop()
            s_manager.push(FadeTransition([self], []))

        for player in [globalVars.player1, globalVars.player2]:
            # Add player
            if (
                input_stream.keyboard.key_pressed(player.input.up)
                and player not in globalVars.players
            ):
                globalVars.players.append(player)
            # Remove player
            if (
                input_stream.keyboard.key_pressed(player.input.down)
                and player in globalVars.players
            ):
                globalVars.players.remove(player)

        if (
            input_stream.keyboard.key_pressed(pygame.K_RETURN)
            and len(globalVars.players) > 0
        ):
            s_manager.push(FadeTransition([self], [LevelSelectScene()]))

    def update(self, s_manager, input_stream):
        self.esc.update(input_stream)

    def draw(self, s_manager, screen):
        screen.fill(globalVars.BLACK)
        self.esc.draw(screen)
        draw.draw_text(
            screen,
            "Player Select: " + str(len(globalVars.players)),
            globalVars.WHITE,
            100,
            100,
        )
        for ind, player in enumerate([globalVars.player1, globalVars.player2]):
            if player.player_index == 1:
                if player in globalVars.players:
                    globalVars.PLAYER_SELECT_IMAGE.set_alpha(255)
                else:
                    globalVars.PLAYER_SELECT_IMAGE.set_alpha(100)
                screen.blit(globalVars.PLAYER_SELECT_IMAGE, (70, 225))
            else:
                if player in globalVars.players:
                    globalVars.player2_idle_changed[0].set_alpha(255)
                else:
                    globalVars.player2_idle_changed[0].set_alpha(100)
                screen.blit(globalVars.player2_idle_changed[0], (140, 225))


class LevelSelectScene(Scene):
    def __init__(self):
        self.esc = ui.Button(pygame.K_ESCAPE, "Main Menu", 275, 250)
        self.level_ptr = 1

    def on_enter(self):
        globalVars.sound_manager.play_music("menu")

    def input(self, s_manager, input_stream):
        if input_stream.keyboard.key_pressed(pygame.K_ESCAPE):
            s_manager.pop()
            s_manager.push(FadeTransition([self], []))

        if input_stream.keyboard.key_pressed(
            pygame.K_LEFT
        ) or input_stream.keyboard.key_pressed(pygame.K_a):
            self.level_ptr = max(self.level_ptr - 1, 1)

        if input_stream.keyboard.key_pressed(
            pygame.K_RIGHT
        ) or input_stream.keyboard.key_pressed(pygame.K_d):
            self.level_ptr = min(self.level_ptr + 1, globalVars.LAST_LEVEL_INDEX)

        if input_stream.keyboard.key_pressed(pygame.K_RETURN):
            globalVars.level_index = self.level_ptr
            globalVars.sound_manager.fade_music()
            level.load_level(globalVars.level_index)
            # Update camera position and size for each player (depending on the amount of players)
            if len(globalVars.players) < 2:
                globalVars.players[0].camera.rect.x = 0
                globalVars.players[0].camera.rect.y = 0
                globalVars.players[0].camera.rect.w = globalVars.WINDOW_SIZE[0]
                globalVars.players[0].camera.rect.h = globalVars.WINDOW_SIZE[1]
            else:
                for player in globalVars.players:
                    if player.player_index == 1:
                        player.camera.rect.x = 0
                        player.camera.rect.y = 0
                        player.camera.rect.w = globalVars.CAMERA_SIZE[0]
                        player.camera.rect.h = globalVars.CAMERA_SIZE[1]
                    elif player.player_index == 2:
                        player.camera.rect.x = (
                            globalVars.WINDOW_SIZE[0] - globalVars.CAMERA_SIZE[0]
                        )
                        player.camera.rect.y = 0
                        player.camera.rect.w = globalVars.CAMERA_SIZE[0]
                        player.camera.rect.h = globalVars.CAMERA_SIZE[1]

            s_manager.push(FadeTransition([self], [GameScene()]))

    def update(self, s_manager, input_stream):
        self.esc.update(input_stream)

    def draw(self, s_manager, screen):
        screen.fill(globalVars.BLACK)
        self.esc.draw(screen)

        for level in range(1, globalVars.LAST_LEVEL_INDEX + 1):
            color = globalVars.WHITE
            if level == self.level_ptr:
                color = globalVars.GREEN
            draw.draw_text(screen, "Level " + str(level), color, level * 100, 200)


class GameScene(Scene):
    def __init__(self):
        self.camera_system = engine.CameraSystem()
        self.physics_system = engine.PhysicsSystem()
        self.input_system = engine.InputSystem()
        self.collection_system = engine.CollectionSystem()
        self.combat_system = engine.CombatSystem()
        self.animation_system = engine.AnimationSystem()
        self.powerup_system = engine.PowerupSystem()

    def on_enter(self):
        globalVars.sound_manager.play_music("level_1")

    def on_exit(self):
        globalVars.sound_manager.fade_music()

    def input(self, s_manager, input_stream):
        if input_stream.keyboard.key_pressed(pygame.K_ESCAPE):
            # Go back to level select scene
            s_manager.pop()
            s_manager.push(FadeTransition([self], []))
            # Remove the players from the world
            for player in globalVars.players:
                globalVars.world.entities.remove(player)
            # Reset the players
            for player in globalVars.players:
                util.reset_player(player)
        elif globalVars.world.is_lost():
            s_manager.push(LoseScene())
        elif globalVars.world.is_won():
            if globalVars.level_index == globalVars.LAST_LEVEL_INDEX:
                s_manager.push(WinScene())
            else:
                globalVars.level_index += 1
                level.load_level(globalVars.level_index)
        else:
            pass

    def update(self, s_manager, input_stream):
        self.physics_system.update()
        self.input_system.update(input_stream=input_stream)
        self.collection_system.update()
        self.combat_system.update()
        self.animation_system.update()
        self.powerup_system.update()

    def draw(self, s_manager, screen):
        draw.draw_background(screen)
        self.camera_system.update(screen)
        # Draw partition between player cameras
        if len(globalVars.players) > 1:
            pygame.draw.line(
                screen,
                globalVars.BLACK,
                (globalVars.CAMERA_SIZE[0], 0),
                (globalVars.CAMERA_SIZE[0], globalVars.CAMERA_SIZE[1]),
                globalVars.WINDOW_SIZE[0] - globalVars.CAMERA_SIZE[0] * 2,
            )


class LoseScene(Scene):
    def __init__(self):
        self.restart = ui.Button(pygame.K_r, "Restart", 450, 250)
        self.esc = ui.Button(pygame.K_ESCAPE, "Main Menu", 450, 300)
        self.alpha = 0

    def on_exit(self):
        for player in globalVars.players:
            globalVars.world.entities.remove(player)

    def update(self, s_manager, input_stream):
        self.restart.update(input_stream)
        self.esc.update(input_stream)
        self.alpha = min(255, self.alpha + 1)

    def input(self, s_manager, input_stream):
        if input_stream.keyboard.key_pressed(pygame.K_ESCAPE):
            s_manager.set(
                [
                    FadeTransition(
                        [GameScene(), self],
                        [MainMenuScene(), PlayerSelectScene(), LevelSelectScene()],
                    )
                ]
            )
            for player in globalVars.players:
                util.reset_player(player)

        if input_stream.keyboard.key_pressed(pygame.K_r):
            s_manager.pop()
            s_manager.push(FlashTransition([self], []))
            # Reset the players
            for player in globalVars.players:
                util.reset_player(player)
            level.load_level(globalVars.level_index)

    def draw(self, s_manager, screen):
        if len(s_manager.scenes) > 1:
            s_manager.scenes[-2].draw(s_manager, screen)

        # Draw transparent background
        bg_surface = pygame.Surface(globalVars.WINDOW_SIZE)
        bg_surface.fill(globalVars.BLACK)
        draw.blit_alpha(screen, bg_surface, (0, 0), self.alpha * 0.7)

        draw.draw_text(
            screen,
            "You Lost!",
            globalVars.RED,
            globalVars.WINDOW_SIZE[0] // 2,
            globalVars.WINDOW_SIZE[1] // 2 - 50,
            self.alpha,
        )
        self.restart.draw(screen, alpha=self.alpha)
        self.esc.draw(screen, alpha=self.alpha)


class WinScene(Scene):
    def __init__(self):
        self.restart = ui.Button(pygame.K_r, "Restart", 450, 250)
        self.esc = ui.Button(pygame.K_ESCAPE, "Main Menu", 450, 300)
        self.alpha = 0

    def on_exit(self):
        for player in globalVars.players:
            globalVars.world.entities.remove(player)

    def update(self, s_manager, input_stream):
        self.restart.update(input_stream)
        self.esc.update(input_stream)
        self.alpha = min(255, self.alpha + 1)

    def input(self, s_manager, input_stream):
        if input_stream.keyboard.key_pressed(pygame.K_ESCAPE):
            s_manager.set(
                [
                    FadeTransition(
                        [GameScene(), self],
                        [MainMenuScene(), PlayerSelectScene(), LevelSelectScene()],
                    )
                ]
            )
            for player in globalVars.players:
                util.reset_player(player)

        if input_stream.keyboard.key_pressed(pygame.K_r):
            s_manager.pop()
            s_manager.push(FlashTransition([self], []))
            # Reset the players
            for player in globalVars.players:
                util.reset_player(player)
            level.load_level(globalVars.level_index)

    def draw(self, s_manager, screen):
        if len(s_manager.scenes) > 1:
            s_manager.scenes[-2].draw(s_manager, screen)

        # Draw transparent background
        bg_surface = pygame.Surface(globalVars.WINDOW_SIZE)
        bg_surface.fill(globalVars.BLACK)
        draw.blit_alpha(screen, bg_surface, (0, 0), self.alpha * 0.7)

        draw.draw_text(
            screen,
            "You Won!",
            globalVars.RED,
            globalVars.WINDOW_SIZE[0] // 2,
            globalVars.WINDOW_SIZE[1] // 2 - 50,
            self.alpha,
        )
        self.restart.draw(screen, alpha=self.alpha)
        self.esc.draw(screen, alpha=self.alpha)


class Transition(Scene):
    def __init__(self, source_scenes, destination_scenes):
        self.timer = 0
        self.source_scenes = source_scenes
        self.destination_scenes = destination_scenes

    def update(self, s_manager, input_stream):
        self.timer += 1  # Fade speed
        if self.timer >= 100:
            s_manager.pop()
            for s in self.destination_scenes:
                s_manager.push(s)
        for s in self.source_scenes:
            s.update(s_manager, input_stream)
        if len(self.destination_scenes) > 0:
            for s in self.destination_scenes:
                s.update(s_manager, input_stream)
        else:
            if len(s_manager.scenes) > 1:
                s_manager.scenes[-2].update(s_manager, input_stream)


class FadeTransition(Transition):
    def draw(self, s_manager, screen):
        if self.timer < 50:
            for s in self.source_scenes:
                s.draw(s_manager, screen)
        else:
            if len(self.destination_scenes) == 0:
                if len(s_manager.scenes) > 1:
                    s_manager.scenes[-2].draw(s_manager, screen)
            else:
                for s in self.destination_scenes:
                    s.draw(s_manager, screen)

        overlay = pygame.Surface((globalVars.WINDOW_SIZE[0], globalVars.WINDOW_SIZE[1]))
        alpha = 255 - int(abs(255 - (255 / 50) * self.timer))
        overlay.set_alpha(alpha)
        overlay.fill(globalVars.BLACK)
        screen.blit(overlay, (0, 0))


class FlashTransition(Transition):
    def draw(self, s_manager, screen):
        if self.timer < 50:
            screen.fill(globalVars.WHITE)
        else:
            if len(self.destination_scenes) == 0:
                if len(s_manager.scenes) > 1:
                    s_manager.scenes[-2].draw(s_manager, screen)
            else:
                for s in self.destination_scenes:
                    s.draw(s_manager, screen)

        overlay = pygame.Surface((globalVars.WINDOW_SIZE[0], globalVars.WINDOW_SIZE[1]))
        alpha = 255 - int(abs(255 - (255 / 50) * self.timer))
        overlay.set_alpha(alpha)
        overlay.fill(globalVars.BLACK)
        screen.blit(overlay, (0, 0))


class SceneManager:
    def __init__(self):
        self.scenes = []

    def is_empty(self):
        return len(self.scenes) == 0

    def enter_scene(self):
        if len(self.scenes) > 0:
            self.scenes[-1].on_enter()

    def exit_scene(self):
        if len(self.scenes) > 0:
            self.scenes[-1].on_exit()

    def input(self, input_stream):
        if len(self.scenes) > 0:
            self.scenes[-1].input(self, input_stream)

    def update(self, input_stream):
        if len(self.scenes) > 0:
            self.scenes[-1].update(self, input_stream)

    def draw(self, screen):
        if len(self.scenes) > 0:
            self.scenes[-1].draw(self, screen)

    def push(self, scene):
        self.exit_scene()
        self.scenes.append(scene)
        self.enter_scene()

    def pop(self):
        self.exit_scene()
        self.scenes.pop()
        self.enter_scene()

    def set(self, scenes):
        # Pop all scenes
        while len(self.scenes) > 0:
            self.pop()
        # Add new scenes
        for s in scenes:
            self.push(s)
