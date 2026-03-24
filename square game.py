import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 800, 600
windowed_size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Square Gaem")

# colors
bg_color = (30, 40, 70)       # background color
square_color = (220, 80, 120) # square color

# square
size = 50
x = WIDTH // 2 - size // 2
y = HEIGHT // 2 - size // 2
speed = 5

clock = pygame.time.Clock()

full_screen = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x -= speed
    if keys[pygame.K_RIGHT]:
        x += speed
    if keys[pygame.K_UP]:
        y -= speed
    if keys[pygame.K_DOWN]:
        y += speed
    if keys[pygame.K_F11]:
        full_screen = not full_screen
        if full_screen:
            screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            WIDTH, HEIGHT = screen.get_size()
        else:
            screen = pygame.display.set_mode(windowed_size)
            WIDTH, HEIGHT = windowed_size
        # Clamp square position to new screen size
        x = max(0, min(x, WIDTH - size))
        y = max(0, min(y, HEIGHT - size))
        pygame.time.wait(200)  # Prevent rapid toggling

    # keep square inside screen
    x = max(0, min(x, WIDTH - size))
    y = max(0, min(y, HEIGHT - size))

    screen.fill(bg_color)
    pygame.draw.rect(screen, square_color, (x, y, size, size))
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
sys.exit()