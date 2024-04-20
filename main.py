import pygame
import sys
import scene
import globalVars
import input


# main
def main():
    window = pygame.display.set_mode(globalVars.WINDOW_SIZE)
    pygame.display.set_caption("Platformer")
    clock = pygame.time.Clock()
    run = True
    fps = 60
    scene_manager = scene.SceneManager()
    scene_manager.push(scene.MainMenuScene())
    input_stream = input.InputStream()

    # Run loop
    while run:
        clock.tick(fps)

        # Check for quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        input_stream.process()
        if scene_manager.is_empty():
            run = False
        scene_manager.input(input_stream)
        scene_manager.update(input_stream)

        # Draw the scene
        scene_manager.draw(window)

        # Update the screen
        pygame.display.update()

        # End of run loop

    # End of main
    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
