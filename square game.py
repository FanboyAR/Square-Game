import pygame
import sys
import random
import json
import os

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 40
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE
FPS = 60

# Colors
BG_COLOR = (30, 40, 70)
WALL_COLOR = (0, 0, 0)
PLAYER_COLOR = (220, 80, 120)
GOAL_COLOR = (80, 220, 120)
TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (100, 100, 150)
BUTTON_HOVER = (150, 150, 200)

# Fonts
font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 24)

# Save file
SAVE_FILE = 'progress.json'

def load_progress():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, 'r') as f:
            data = json.load(f)
            return data.get('level', 1)
    return 1

def save_progress(level):
    with open(SAVE_FILE, 'w') as f:
        json.dump({'level': level}, f)

class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[1 for _ in range(width)] for _ in range(height)]  # 1 = wall, 0 = path
        self.generate_maze()
        self.player_pos = [1, 1]
        self.goal_pos = [width - 2, height - 2]

    def generate_maze(self):
        # Simple maze generation using randomized DFS
        stack = []
        visited = set()
        start = (1, 1)
        self.grid[start[1]][start[0]] = 0
        stack.append(start)
        visited.add(start)

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while stack:
            current = stack[-1]
            neighbors = []
            for dx, dy in directions:
                nx, ny = current[0] + dx * 2, current[1] + dy * 2
                if 0 < nx < self.width - 1 and 0 < ny < self.height - 1 and (nx, ny) not in visited:
                    neighbors.append((nx, ny, current[0] + dx, current[1] + dy))

            if neighbors:
                nx, ny, wx, wy = random.choice(neighbors)
                self.grid[ny][nx] = 0
                self.grid[wy][wx] = 0
                stack.append((nx, ny))
                visited.add((nx, ny))
            else:
                stack.pop()

        # Ensure goal is reachable
        self.grid[self.goal_pos[1]][self.goal_pos[0]] = 0

    def draw(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == 1:
                    pygame.draw.rect(screen, WALL_COLOR, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Draw goal
        pygame.draw.rect(screen, GOAL_COLOR, (self.goal_pos[0] * CELL_SIZE, self.goal_pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Draw player
        pygame.draw.rect(screen, PLAYER_COLOR, (self.player_pos[0] * CELL_SIZE, self.player_pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def move_player(self, dx, dy):
        new_x = self.player_pos[0] + dx
        new_y = self.player_pos[1] + dy
        if 0 <= new_x < self.width and 0 <= new_y < self.height and self.grid[new_y][new_x] == 0:
            self.player_pos = [new_x, new_y]

    def check_win(self):
        return self.player_pos == self.goal_pos

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = BUTTON_COLOR

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surf = small_font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_hovered(self, pos):
        return self.rect.collidepoint(pos)

def draw_text(screen, text, x, y, font=font, color=TEXT_COLOR):
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=(x, y))
    screen.blit(surf, rect)

def main_menu(screen):
    start_button = Button(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50, "Start Game")
    quit_button = Button(WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 50, "Quit")

    while True:
        screen.fill(BG_COLOR)
        draw_text(screen, "Square Maze Game", WIDTH // 2, HEIGHT // 4)

        mouse_pos = pygame.mouse.get_pos()
        for button in [start_button, quit_button]:
            if button.is_hovered(mouse_pos):
                button.color = BUTTON_HOVER
            else:
                button.color = BUTTON_COLOR
            button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.is_hovered(mouse_pos):
                    return 'start'
                if quit_button.is_hovered(mouse_pos):
                    return 'quit'

        pygame.display.flip()

def game_loop(screen, start_level):
    level = start_level
    while True:
        maze = Maze(GRID_WIDTH, GRID_HEIGHT)
        clock = pygame.time.Clock()

        while True:
            screen.fill(BG_COLOR)
            maze.draw(screen)
            draw_text(screen, f"Level {level}", WIDTH // 2, 30, small_font)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save_progress(level)
                    return 'quit'

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                maze.move_player(-1, 0)
            if keys[pygame.K_RIGHT]:
                maze.move_player(1, 0)
            if keys[pygame.K_UP]:
                maze.move_player(0, -1)
            if keys[pygame.K_DOWN]:
                maze.move_player(0, 1)
            if keys[pygame.K_ESCAPE]:
                save_progress(level)
                return 'menu'

            if maze.check_win():
                level += 1
                save_progress(level)
                break

            pygame.display.flip()
            clock.tick(FPS)

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Square Maze Game")

    current_level = load_progress()

    state = 'menu'
    while state != 'quit':
        if state == 'menu':
            state = main_menu(screen)
        elif state == 'start':
            state = game_loop(screen, current_level)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()