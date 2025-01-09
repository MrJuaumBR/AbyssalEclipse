import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 768
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Infinite Floor')

# Load floor image
floor_img = pygame.image.load('./aseprite/floor.png')
floor_width, floor_height = floor_img.get_width(), floor_img.get_height()

# Create a surface for the entire floor
floor_surface = pygame.Surface((SCREEN_WIDTH + floor_width, SCREEN_HEIGHT + floor_height))

# Fill the floor surface with the floor image
for x in range(0, SCREEN_WIDTH + floor_width, floor_width):
    for y in range(0, SCREEN_HEIGHT + floor_height, floor_height):
        floor_surface.blit(floor_img, (x, y))

# Player settings
player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
player_speed = 5
player_img = pygame.Surface((50, 50))  # Temporary player representation
player_img.fill((0, 255, 0))  # Green player

# Font settings for FPS display
font = pygame.font.SysFont(None, 20)

clock = pygame.time.Clock()

def draw_floor(offset_x, offset_y):
    # Calculate modulo only once
    mod_x = offset_x % floor_width
    mod_y = offset_y % floor_height

    for x in range(-floor_width, SCREEN_WIDTH, floor_width):
        for y in range(-floor_height, SCREEN_HEIGHT, floor_height):
            screen.blit(floor_surface, (x - mod_x, y - mod_y))



def run():
    offset_x, offset_y = 0, 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            offset_y -= player_speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            offset_y += player_speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            offset_x -= player_speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            offset_x += player_speed

        # Draw the floor
        screen.fill((0, 0, 0))  # Clear screen with black
        draw_floor(offset_x, offset_y)

        # Draw the player
        screen.blit(player_img, player_pos)

        # Display FPS
        fps = int(clock.get_fps())
        fps_text = font.render(f'FPS: {fps}', True, (255, 255, 255))
        screen.blit(fps_text, (10, 10))

        pygame.display.update()
        clock.tick(60)  # Set to 60 FPS
