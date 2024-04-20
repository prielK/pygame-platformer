import pygame
import draw
import globalVars


class System:
    def __init__(self):
        pass

    def check(self, entity):
        return True

    def update(self, screen=None, input_stream=None):
        for entity in globalVars.world.entities:
            if self.check(entity):
                self.update_entity(screen, entity, input_stream)

    def update_entity(self, screen, entity, input_stream):
        pass


class PhysicsSystem(System):
    def check(self, entity):
        return entity.position is not None

    def update_entity(self, screen, entity, input_stream):
        next_x = entity.position.rect.x
        next_y = entity.position.rect.y
        x_collide = False
        y_collide = False

        # Apply entity control
        if entity.control is not None and entity.state != "dead":
            if entity.control.move_left and not entity.hurt:
                next_x -= entity.speed
                entity.direction = "left"
                entity.state = "running"
                # Steps SFX
                if entity.walked > 0 or entity.walked < -24:
                    entity.walked = 0
                if entity.grounded:
                    if entity.walked == -1:
                        globalVars.sound_manager.play_sfx("walk")
                    entity.walked -= 1

            if entity.control.move_right and not entity.hurt:
                next_x += entity.speed
                entity.direction = "right"
                entity.state = "running"
                # Steps SFX
                if entity.walked < 0 or entity.walked > 24:
                    entity.walked = 0
                if entity.grounded:
                    if entity.walked == 1:
                        globalVars.sound_manager.play_sfx("walk")
                    entity.walked += 1
            # Check player state
            if not entity.control.move_left and not entity.control.move_right:
                entity.state = "idle"
            # Jump
            if entity.control.jump and entity.grounded and not entity.hurt:
                entity.fall_vel -= globalVars.JUMP_FORCE

        # Check for horizontal collisions
        next_rect = pygame.Rect(
            int(next_x),
            int(entity.position.rect.y),
            entity.position.rect.w,
            entity.position.rect.h,
        )

        for p in globalVars.world.platforms:
            if p.colliderect(next_rect):
                x_collide = True
                break
        if not x_collide:
            entity.position.rect.x = next_x

        # Check for vertical collision and jump/fall
        entity.grounded = False
        entity.fall_vel += globalVars.GRAVITY
        next_y += entity.fall_vel + 1
        next_rect = pygame.Rect(
            int(entity.position.rect.x),
            int(next_y),
            entity.position.rect.w,
            entity.position.rect.h,
        )
        for p in globalVars.world.platforms:
            if p.colliderect(next_rect):
                entity.fall_vel = 0
                y_collide = True
                if p.y >= next_rect.y:
                    entity.grounded = True
                    entity.hurt = False
                if p[1] >= next_y:
                    entity.position.rect.y = p[1] - entity.position.rect.h
                break

        # If in the air
        if not entity.grounded:
            entity.landed = False

        # If no platform under the player
        if not y_collide:
            entity.position.rect.y = next_y

        # If was in the air and landing sound wasnt played yet
        elif not entity.landed and entity.grounded:
            globalVars.sound_manager.play_sfx("land")
            entity.landed = True

        # If player falls off map set health to 0
        if entity.position.rect.y > globalVars.WINDOW_SIZE[1]:
            entity.health.health = 0
            entity.state = "dead"


class InputSystem(System):
    def check(self, entity):
        return entity.input is not None and entity.control is not None

    def update_entity(self, screen, entity, input_stream):
        if input_stream.keyboard.key_down(entity.input.up):
            entity.control.jump = True
        else:
            entity.control.jump = False
        if input_stream.keyboard.key_down(entity.input.down):
            entity.control.crouch = True
        else:
            entity.control.crouch = False
        if input_stream.keyboard.key_down(entity.input.left):
            entity.control.move_left = True
        else:
            entity.control.move_left = False
        if input_stream.keyboard.key_down(entity.input.right):
            entity.control.move_right = True
        else:
            entity.control.move_right = False
        if input_stream.keyboard.key_down(entity.input.z_in):
            entity.control.zoom_in = True
        else:
            entity.control.zoom_in = False
        if input_stream.keyboard.key_down(entity.input.z_out):
            entity.control.zoom_out = True
        else:
            entity.control.zoom_out = False


class CameraSystem(System):
    def check(self, entity):
        return entity.camera is not None

    def update_entity(self, screen, entity, input_stream):
        # Camera clipping
        screen_rect = pygame.Rect(
            entity.camera.rect.x,
            entity.camera.rect.y,
            entity.camera.rect.w,
            entity.camera.rect.h,
        )
        screen.set_clip(screen_rect)

        # If camera tracking entity
        if entity.camera.tracked is not None:
            if entity.control.zoom_in and entity.camera.zoom < 1.5:
                entity.camera.zoom += 0.01
            if entity.control.zoom_out and entity.camera.zoom > 0.5:
                entity.camera.zoom -= 0.01
            tracked_entity = entity.camera.tracked
            # Current camera position
            current_x = entity.camera.world_x
            current_y = entity.camera.world_y
            # Target camera position
            target_x = (
                tracked_entity.position.rect.x + tracked_entity.position.rect.w / 2
            )
            target_y = (
                tracked_entity.position.rect.y + tracked_entity.position.rect.h / 2
            )
            # Update camera position
            entity.camera.world_x = (current_x * 0.96) + (target_x * 0.04)
            entity.camera.world_y = (current_y * 0.96) + (target_y * 0.04)

        # Calculate camera offset
        offset_x = (
            screen_rect.x
            + screen_rect.w / 2
            - entity.camera.world_x * entity.camera.zoom
        )
        offset_y = (
            screen_rect.y
            + screen_rect.h / 2
            - entity.camera.world_y * entity.camera.zoom
        )

        # Render platforms
        for p in globalVars.world.platforms:
            next_pos_rect = pygame.Rect(
                p.x * entity.camera.zoom + offset_x,
                p.y * entity.camera.zoom + offset_y,
                p.w * entity.camera.zoom,
                p.h * entity.camera.zoom,
            )
            draw.draw_platform(screen, next_pos_rect)

        # Render entities
        for e in globalVars.world.entities:
            s = e.state
            anim = e.animations.animations_list[s]
            anim.draw(
                screen,
                e.position.rect.x * entity.camera.zoom + offset_x,
                e.position.rect.y * entity.camera.zoom + offset_y,
                e.direction == "left",
                entity.camera.zoom,
                e.animations.alpha,
            )  # If direction of entity is left than flip animation

        if entity.type == "player":
            if entity.camera.rect.x > 0:
                index = 2
            else:
                index = 1
            # Draw HUD
            draw.draw_HUD(screen, entity.health.health, entity.coins.coins, index)

        # Camera unclipping
        screen.set_clip(None)


class Camera:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.world_x = 0
        self.world_y = 0
        self.zoom = 1
        self.tracked = None

    def set_position(self, x, y):
        self.world_x = x
        self.world_y = y

    def track(self, entity):
        self.tracked = entity


class Position:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)


class AnimationSystem(System):
    def check(self, entity):
        return entity.animations is not None

    def update_entity(self, screen, entity, input_stream):
        entity.animations.animations_list[entity.state].update()


class Animations:
    def __init__(self):
        self.animations_list = {}
        self.alpha = 255

    def add(self, state, animation):
        self.animations_list[state] = animation


class Animation:
    def __init__(self, image_list):
        self.image_list = image_list
        self.img_ind = 0
        self.animation_timer = 0
        self.animation_speed = 8

    def update(self):
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.img_ind += 1
            if self.img_ind > len(self.image_list) - 1:
                self.img_ind = 0

    def draw(self, window, x, y, flip, zoom, alpha):
        image = self.image_list[self.img_ind]
        image.set_alpha(alpha)
        window.blit(
            pygame.transform.scale(
                pygame.transform.flip(image, flip, False),
                (
                    int(self.image_list[self.img_ind].get_rect().w * zoom),
                    int(self.image_list[self.img_ind].get_rect().h * zoom),
                ),
            ),
            (x, y),
        )


class PowerupSystem(System):
    def check(self, entity):
        return entity.effect is not None

    def update_entity(self, screen, entity, input_stream):
        for ent in globalVars.world.entities:
            if ent is not entity and ent.type == "player" and entity.type != "player":
                # Check for collision between player and powerup and check if trigger is true
                if entity.position.rect.colliderect(ent.position.rect):
                    if entity.effect.trigger is None or entity.effect.trigger(ent):
                        # Set the player's effect and play a sound (consume powerup)
                        ent.effect = entity.effect
                        globalVars.sound_manager.play_sfx(entity.effect.sfx)
                        # Remove the powerup from the world
                        globalVars.world.entities.remove(entity)

        # Apply the player's effect
        if entity.type == "player":
            entity.effect.apply(entity)
            entity.effect.timer -= 1
            # When effect duration ends
            if entity.effect.timer <= 0:
                if entity.effect.end:
                    entity.effect.end(entity)
                entity.effect = None


class CollectionSystem(System):
    def check(self, entity):
        return entity.type == "player"

    def update_entity(self, screen, entity, input_stream):
        for ent in globalVars.world.entities:
            if ent is not entity and ent.type == "collectable":
                if entity.position.rect.colliderect(ent.position.rect):
                    globalVars.sound_manager.play_sfx("gold")
                    globalVars.world.entities.remove(ent)
                    entity.coins.coins += 1


class CombatSystem(System):
    def check(self, entity):
        return entity.type == "player"

    def update_entity(self, screen, entity, input_stream):
        for ent in globalVars.world.entities:
            if ent is not entity and ent.type == "enemy":
                if entity.position.rect.colliderect(ent.position.rect):
                    entity.health.health -= globalVars.ENEMY_DAMAGE
                    if entity.health.health > 0:
                        if entity.direction == "right":
                            entity.position.rect.x -= 20
                            entity.position.rect.y -= 8
                            entity.hurt = True
                        elif entity.direction == "left":
                            entity.position.rect.x += 20
                            entity.position.rect.y -= 8
                            entity.hurt = True
                    else:
                        entity.state = "dead"


class Coins:
    def __init__(self):
        self.coins = 0


class Health:
    def __init__(self):
        self.health = globalVars.MAX_PLAYER_HEALTH


class Effect:
    def __init__(self, apply, timer, sfx, end, trigger):
        self.apply = apply
        self.timer = timer
        self.sfx = sfx
        self.end = end
        self.trigger = trigger


class Input:
    def __init__(self, up, down, left, right, z_in, z_out):
        self.up = up
        self.down = down
        self.left = left
        self.right = right
        self.z_in = z_in
        self.z_out = z_out


class EntityControl:
    def __init__(self):
        self.jump = False
        self.crouch = False
        self.move_left = False
        self.move_right = False
        self.zoom_in = False
        self.zoom_out = False


class Entity:
    def __init__(self):
        self.position = None
        self.input = None
        self.control = None
        self.animations = Animations()
        self.state = "idle"
        self.type = "unknown"
        self.player_index = 0
        self.direction = "right"
        self.effect = None
        self.speed = 0
        self.fall_vel = 0
        self.camera = None
        self.coins = None
        self.health = None
        self.grounded = False
        self.hurt = False
        self.landed = True
        self.walked = 0
