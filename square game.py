import pygame
import sys
import random
import json
import os

pygame.init()

# Fixed screen size independent from external display resolution
CELL_SIZE = 40
WIDTH = 1920
HEIGHT = 1080
FPS = 60
windowed_size = (WIDTH, HEIGHT)
full_screen = False
display_mode = 'windowed'  # 'windowed', 'fullscreen', 'borderless'
resolution_setting = 'auto'  # 'auto' or (w, h)
RESOLUTION_OPTIONS = ['auto', (1280, 720), (1366, 768), (1600, 900), (1920, 1080), (2560, 1440)]

# Maze growth by level
BASE_GRID_WIDTH = 15
BASE_GRID_HEIGHT = 11
MAX_GRID_WIDTH = 47
MAX_GRID_HEIGHT = 25
GRID_STEP = 2
BASE_PLAYER_SPEED = 3
SPEED_UPGRADE_COSTS = [12, 24, 40, 60, 85]
BONUS_COIN_UPGRADE_COSTS = [15, 30, 50, 75, 105]
PRESTIGE_UPGRADE_COSTS = [5, 11, 18]

# Colors
BG_COLOR = (30, 40, 70)
WALL_COLOR = (0, 0, 0)
PLAYER_COLOR = (220, 80, 120)
GOAL_COLOR = (80, 220, 120)
COIN_COLOR = (255, 215, 0)  # Gold color
TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (100, 100, 150)
BUTTON_HOVER = (150, 150, 200)

PLAYER_SKINS = [
    {'id': 'base', 'name': 'Classic', 'color': (220, 80, 120), 'accent': (245, 225, 235), 'pattern': 'solid', 'cost': 0, 'currency': 'free', 'tier': 'Preset', 'unlock_type': 'default'},
    {'id': 'mint', 'name': 'Mint Lines', 'color': (95, 225, 175), 'accent': (230, 255, 245), 'pattern': 'stripe_h', 'cost': 80, 'currency': 'coins', 'tier': 'Preset', 'unlock_type': 'shop'},
    {'id': 'azure', 'name': 'Azure Bars', 'color': (80, 150, 235), 'accent': (220, 240, 255), 'pattern': 'stripe_v', 'cost': 140, 'currency': 'coins', 'tier': 'Preset', 'unlock_type': 'shop'},
    {'id': 'sunset', 'name': 'Sunset Check', 'color': (245, 145, 95), 'accent': (255, 215, 190), 'pattern': 'checker', 'cost': 220, 'currency': 'coins', 'tier': 'Preset', 'unlock_type': 'shop'},
    {'id': 'ember', 'name': 'Ember Frame', 'color': (225, 95, 70), 'accent': (255, 210, 190), 'pattern': 'frame', 'cost': 300, 'currency': 'coins', 'tier': 'Preset', 'unlock_type': 'shop'},
    {'id': 'signal', 'name': 'Signal Cross', 'color': (115, 185, 250), 'accent': (235, 245, 255), 'pattern': 'cross', 'cost': 380, 'currency': 'coins', 'tier': 'Preset', 'unlock_type': 'shop'},
    {'id': 'jade', 'name': 'Jade Lattice', 'color': (90, 210, 165), 'accent': (225, 255, 240), 'pattern': 'grid', 'cost': 10, 'currency': 'level', 'tier': 'Level', 'unlock_type': 'level'},
    {'id': 'inferno', 'name': 'Inferno Split', 'color': (235, 120, 70), 'accent': (255, 220, 195), 'pattern': 'diag', 'cost': 18, 'currency': 'level', 'tier': 'Level', 'unlock_type': 'level'},
    {'id': 'royal', 'name': 'Royal Dots', 'color': (230, 200, 70), 'accent': (255, 245, 185), 'pattern': 'dots', 'cost': 4, 'currency': 'prestige', 'tier': 'Premium', 'unlock_type': 'shop'},
    {'id': 'void', 'name': 'Void Diagonal', 'color': (170, 95, 240), 'accent': (235, 210, 255), 'pattern': 'diag', 'cost': 8, 'currency': 'prestige', 'tier': 'Premium', 'unlock_type': 'shop'},
    {'id': 'circuit', 'name': 'Circuit Grid', 'color': (70, 220, 210), 'accent': (210, 255, 250), 'pattern': 'grid', 'cost': 12, 'currency': 'prestige', 'tier': 'Premium', 'unlock_type': 'shop'},
    {'id': 'crown', 'name': 'Crown Core', 'color': (235, 180, 80), 'accent': (255, 235, 190), 'pattern': 'core', 'cost': 16, 'currency': 'prestige', 'tier': 'Premium', 'unlock_type': 'shop'},
    {'id': 'aurora', 'name': 'Aurora Fade', 'color': (95, 165, 255), 'accent': (185, 110, 255), 'pattern': 'gradient_v', 'cost': 20, 'currency': 'prestige', 'tier': 'Premium', 'unlock_type': 'shop'},
    {'id': 'horizon', 'name': 'Horizon Lines', 'color': (80, 145, 245), 'accent': (255, 170, 130), 'pattern': 'gradient_v_lines', 'cost': 260, 'currency': 'coins', 'tier': 'Preset', 'unlock_type': 'shop'},
    {'id': 'tilewave', 'name': 'Tilewave Fade', 'color': (85, 195, 230), 'accent': (245, 245, 255), 'pattern': 'gradient_checker', 'cost': 320, 'currency': 'coins', 'tier': 'Preset', 'unlock_type': 'shop'},
    {'id': 'flux', 'name': 'Spectrum Flux', 'color': (220, 80, 120), 'accent': (165, 225, 255), 'pattern': 'gradient_grid', 'cost': 430, 'currency': 'coins', 'tier': 'Preset', 'unlock_type': 'shop'},
    {'id': 'neon_steps', 'name': 'Neon Steps', 'color': (95, 220, 185), 'accent': (165, 120, 255), 'pattern': 'gradient_h_lines', 'cost': 14, 'currency': 'level', 'tier': 'Level', 'unlock_type': 'level'},
    {'id': 'lumen_blocks', 'name': 'Lumen Blocks', 'color': (240, 130, 90), 'accent': (120, 195, 255), 'pattern': 'gradient_checker', 'cost': 24, 'currency': 'level', 'tier': 'Level', 'unlock_type': 'level'},
]
SKIN_ID_SET = {skin['id'] for skin in PLAYER_SKINS}
DEFAULT_BASE_SKIN_COLOR = (220, 80, 120)

# Fonts
font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 24)

# Save files
SAVE_FILE = 'progress.json'
MID_SAVE_FILE = 'mid_save.json'
SETTINGS_FILE = 'settings.json'

def _is_valid_rgb_triplet(value):
    return (
        isinstance(value, (tuple, list))
        and len(value) == 3
        and all(isinstance(channel, int) and 0 <= channel <= 255 for channel in value)
    )

class ProgressRepository:
    def __init__(self, save_file):
        self.save_file = save_file

    def _read_data(self):
        if os.path.exists(self.save_file):
            with open(self.save_file, 'r') as f:
                return json.load(f)
        return {}

    def _write_data(self, data):
        with open(self.save_file, 'w') as f:
            json.dump(data, f)

    def load_progress(self):
        data = self._read_data()
        return data.get('level', 1), data.get('total_coins', 0)

    def load_speed_level(self):
        return self._read_data().get('speed_level', 0)

    def load_bonus_coin_level(self):
        return self._read_data().get('bonus_coin_level', 0)

    def load_reset_count(self):
        return self._read_data().get('reset_count', 0)

    def load_prestige_points(self):
        return self._read_data().get('prestige_points', 0)

    def load_prestige_upgrade_level(self):
        return self._read_data().get('prestige_upgrade_level', 0)

    def load_skin_state(self):
        selected_skin_id = 'base'
        unlocked_skin_ids = ['base']
        data = self._read_data()

        raw_selected = data.get('selected_skin_id', 'base')
        raw_unlocked = data.get('unlocked_skin_ids', ['base'])

        if raw_selected in SKIN_ID_SET:
            selected_skin_id = raw_selected

        if isinstance(raw_unlocked, list):
            filtered = [skin_id for skin_id in raw_unlocked if skin_id in SKIN_ID_SET]
            if 'base' not in filtered:
                filtered.insert(0, 'base')
            unlocked_skin_ids = list(dict.fromkeys(filtered))

        if selected_skin_id not in unlocked_skin_ids:
            selected_skin_id = 'base'

        return selected_skin_id, unlocked_skin_ids

    def load_custom_skin_colors(self):
        colors = {skin['id']: tuple(skin['color']) for skin in PLAYER_SKINS}
        data = self._read_data()

        raw_colors = data.get('custom_skin_colors')
        if isinstance(raw_colors, dict):
            for skin_id, raw_color in raw_colors.items():
                if skin_id in SKIN_ID_SET and _is_valid_rgb_triplet(raw_color):
                    colors[skin_id] = (int(raw_color[0]), int(raw_color[1]), int(raw_color[2]))
        else:
            raw_legacy_color = data.get('custom_base_skin_color', list(DEFAULT_BASE_SKIN_COLOR))
            if _is_valid_rgb_triplet(raw_legacy_color):
                legacy_color = (int(raw_legacy_color[0]), int(raw_legacy_color[1]), int(raw_legacy_color[2]))
                colors['base'] = legacy_color
                if 'flux' in colors:
                    colors['flux'] = legacy_color

        return colors

    def save_progress(
        self,
        level,
        total_coins,
        speed_level,
        bonus_coin_level,
        reset_count,
        prestige_points,
        prestige_upgrade_level,
        selected_skin_id,
        unlocked_skin_ids,
        custom_skin_colors,
    ):
        if selected_skin_id not in SKIN_ID_SET:
            selected_skin_id = 'base'

        filtered_unlocked = [skin_id for skin_id in unlocked_skin_ids if skin_id in SKIN_ID_SET]
        if 'base' not in filtered_unlocked:
            filtered_unlocked.insert(0, 'base')
        filtered_unlocked = list(dict.fromkeys(filtered_unlocked))

        if selected_skin_id not in filtered_unlocked:
            selected_skin_id = 'base'

        serialized_custom_skin_colors = {}
        if isinstance(custom_skin_colors, dict):
            for skin in PLAYER_SKINS:
                skin_id = skin['id']
                raw_color = custom_skin_colors.get(skin_id, skin['color'])
                if not _is_valid_rgb_triplet(raw_color):
                    raw_color = skin['color']
                serialized_custom_skin_colors[skin_id] = [int(raw_color[0]), int(raw_color[1]), int(raw_color[2])]

        legacy_base_color = serialized_custom_skin_colors.get('base', [
            int(DEFAULT_BASE_SKIN_COLOR[0]),
            int(DEFAULT_BASE_SKIN_COLOR[1]),
            int(DEFAULT_BASE_SKIN_COLOR[2]),
        ])

        self._write_data(
            {
                'level': level,
                'total_coins': total_coins,
                'speed_level': speed_level,
                'bonus_coin_level': bonus_coin_level,
                'reset_count': reset_count,
                'prestige_points': prestige_points,
                'prestige_upgrade_level': prestige_upgrade_level,
                'selected_skin_id': selected_skin_id,
                'unlocked_skin_ids': filtered_unlocked,
                'custom_skin_colors': serialized_custom_skin_colors,
                'custom_base_skin_color': legacy_base_color,
            }
        )


class SkinService:
    def __init__(self, skins):
        self.skins = skins

    def get_skin_definition(self, skin_id, custom_skin_colors=None):
        for skin in self.skins:
            if skin['id'] == skin_id:
                if isinstance(custom_skin_colors, dict) and skin_id in custom_skin_colors and _is_valid_rgb_triplet(custom_skin_colors[skin_id]):
                    overridden = dict(skin)
                    custom_color = (
                        int(custom_skin_colors[skin_id][0]),
                        int(custom_skin_colors[skin_id][1]),
                        int(custom_skin_colors[skin_id][2]),
                    )
                    overridden['color'] = custom_color
                    overridden['accent'] = (
                        max(40, min(255, 255 - custom_color[0] // 2)),
                        max(40, min(255, 255 - custom_color[1] // 2)),
                        max(40, min(255, 255 - custom_color[2] // 2)),
                    )
                    return overridden
                return skin
        return self.skins[0]

    def get_skin_color(self, skin_id, custom_skin_colors=None):
        return self.get_skin_definition(skin_id, custom_skin_colors)['color']


progress_repository = ProgressRepository(SAVE_FILE)
skin_service = SkinService(PLAYER_SKINS)


def load_progress():
    return progress_repository.load_progress()

def load_speed_level():
    return progress_repository.load_speed_level()

def load_bonus_coin_level():
    return progress_repository.load_bonus_coin_level()

def load_reset_count():
    return progress_repository.load_reset_count()

def load_prestige_points():
    return progress_repository.load_prestige_points()

def load_prestige_upgrade_level():
    return progress_repository.load_prestige_upgrade_level()

def load_skin_state():
    return progress_repository.load_skin_state()

def load_custom_skin_colors():
    return progress_repository.load_custom_skin_colors()

def load_custom_base_skin_color():
    return load_custom_skin_colors().get('base', DEFAULT_BASE_SKIN_COLOR)

def get_skin_definition(skin_id, custom_skin_colors=None):
    return skin_service.get_skin_definition(skin_id, custom_skin_colors)

def get_skin_color(skin_id, custom_skin_colors=None):
    return skin_service.get_skin_color(skin_id, custom_skin_colors)

def draw_skin_preview(screen, rect, skin_definition):
    if rect.width <= 0 or rect.height <= 0:
        return

    base_color = skin_definition['color']
    accent_color = skin_definition.get('accent', (235, 235, 245))
    pattern = skin_definition.get('pattern', 'solid')

    previous_clip = screen.get_clip()
    screen.set_clip(rect)

    pygame.draw.rect(screen, base_color, rect)

    inset = max(1, min(rect.width, rect.height) // 12)
    inner = rect.inflate(-inset * 2, -inset * 2)
    if inner.width <= 2 or inner.height <= 2:
        inner = rect.copy()

    def gradient_color_at(t):
        return (
            int(base_color[0] * (1 - t) + accent_color[0] * t),
            int(base_color[1] * (1 - t) + accent_color[1] * t),
            int(base_color[2] * (1 - t) + accent_color[2] * t),
        )

    def draw_vertical_gradient():
        span = max(1, rect.height - 1)
        for y in range(rect.top, rect.bottom):
            t = (y - rect.top) / span
            pygame.draw.line(screen, gradient_color_at(t), (rect.left, y), (rect.right - 1, y))

    def draw_horizontal_gradient():
        span = max(1, rect.width - 1)
        for x in range(rect.left, rect.right):
            t = (x - rect.left) / span
            pygame.draw.line(screen, gradient_color_at(t), (x, rect.top), (x, rect.bottom - 1))

    if pattern == 'stripe_h':
        spacing = max(4, rect.height // 4)
        for y in range(rect.top + inset, rect.bottom - inset, spacing):
            pygame.draw.line(screen, accent_color, (rect.left + inset, y), (rect.right - inset, y), max(1, inset // 2 + 1))
    elif pattern == 'gradient_v':
        draw_vertical_gradient()
    elif pattern == 'gradient_h':
        draw_horizontal_gradient()
    elif pattern == 'gradient_v_lines':
        draw_vertical_gradient()
        spacing = max(4, rect.height // 4)
        line_width = max(1, inset // 2 + 1)
        for y in range(rect.top + inset, rect.bottom - inset, spacing):
            pygame.draw.line(screen, accent_color, (rect.left + inset, y), (rect.right - inset, y), line_width)
    elif pattern == 'gradient_h_lines':
        draw_horizontal_gradient()
        spacing = max(4, rect.width // 4)
        line_width = max(1, inset // 2 + 1)
        for x in range(rect.left + inset, rect.right - inset, spacing):
            pygame.draw.line(screen, accent_color, (x, rect.top + inset), (x, rect.bottom - inset), line_width)
    elif pattern == 'gradient_checker':
        draw_vertical_gradient()
        cell = max(3, min(rect.width, rect.height) // 5)
        for y in range(rect.top + inset, rect.bottom - inset, cell):
            for x in range(rect.left + inset, rect.right - inset, cell):
                if ((x // cell) + (y // cell)) % 2 == 0:
                    pygame.draw.rect(screen, accent_color, (x, y, cell, cell), 1)
    elif pattern == 'gradient_grid':
        draw_vertical_gradient()
        spacing = max(5, min(rect.width, rect.height) // 4)
        for x in range(rect.left + inset, rect.right - inset, spacing):
            pygame.draw.line(screen, accent_color, (x, rect.top + inset), (x, rect.bottom - inset), 1)
        for y in range(rect.top + inset, rect.bottom - inset, spacing):
            pygame.draw.line(screen, accent_color, (rect.left + inset, y), (rect.right - inset, y), 1)
    elif pattern == 'stripe_v':
        spacing = max(4, rect.width // 4)
        for x in range(rect.left + inset, rect.right - inset, spacing):
            pygame.draw.line(screen, accent_color, (x, rect.top + inset), (x, rect.bottom - inset), max(1, inset // 2 + 1))
    elif pattern == 'checker':
        cell = max(3, min(rect.width, rect.height) // 5)
        for y in range(rect.top + inset, rect.bottom - inset, cell):
            for x in range(rect.left + inset, rect.right - inset, cell):
                if ((x // cell) + (y // cell)) % 2 == 0:
                    pygame.draw.rect(screen, accent_color, (x, y, cell, cell))
    elif pattern == 'frame':
        pygame.draw.rect(screen, accent_color, inner, max(2, inset // 2 + 1))
    elif pattern == 'cross':
        cx, cy = rect.center
        bar = max(2, inset // 2 + 1)
        pygame.draw.rect(screen, accent_color, (cx - bar, rect.top + inset, bar * 2, rect.height - inset * 2))
        pygame.draw.rect(screen, accent_color, (rect.left + inset, cy - bar, rect.width - inset * 2, bar * 2))
    elif pattern == 'dots':
        radius = max(1, min(rect.width, rect.height) // 10)
        for dy in range(1, 4):
            for dx in range(1, 4):
                px = rect.left + dx * rect.width // 4
                py = rect.top + dy * rect.height // 4
                pygame.draw.circle(screen, accent_color, (px, py), radius)
    elif pattern == 'diag':
        spacing = max(5, rect.width // 4)
        for d in range(-rect.height, rect.width, spacing):
            start = (rect.left + d, rect.bottom - inset)
            end = (rect.left + d + rect.height, rect.top + inset)
            pygame.draw.line(screen, accent_color, start, end, max(1, inset // 2 + 1))
    elif pattern == 'grid':
        spacing = max(5, min(rect.width, rect.height) // 4)
        for x in range(rect.left + inset, rect.right - inset, spacing):
            pygame.draw.line(screen, accent_color, (x, rect.top + inset), (x, rect.bottom - inset), 1)
        for y in range(rect.top + inset, rect.bottom - inset, spacing):
            pygame.draw.line(screen, accent_color, (rect.left + inset, y), (rect.right - inset, y), 1)
    elif pattern == 'core':
        core = inner.inflate(-inner.width // 3, -inner.height // 3)
        pygame.draw.rect(screen, accent_color, core)
        pygame.draw.rect(screen, accent_color, inner, max(1, inset // 2 + 1))

    screen.set_clip(previous_clip)

def save_progress(
    level,
    total_coins,
    speed_level=None,
    bonus_coin_level=None,
    reset_count=None,
    prestige_points=None,
    prestige_upgrade_level=None,
    selected_skin_id=None,
    unlocked_skin_ids=None,
    custom_skin_colors=None,
    custom_base_skin_color=None,
):
    if speed_level is None:
        speed_level = load_speed_level()
    if bonus_coin_level is None:
        bonus_coin_level = load_bonus_coin_level()
    if reset_count is None:
        reset_count = load_reset_count()
    if prestige_points is None:
        prestige_points = load_prestige_points()
    if prestige_upgrade_level is None:
        prestige_upgrade_level = load_prestige_upgrade_level()
    if selected_skin_id is None or unlocked_skin_ids is None:
        saved_selected_skin_id, saved_unlocked_skin_ids = load_skin_state()
        if selected_skin_id is None:
            selected_skin_id = saved_selected_skin_id
        if unlocked_skin_ids is None:
            unlocked_skin_ids = saved_unlocked_skin_ids
    if custom_skin_colors is None:
        custom_skin_colors = load_custom_skin_colors()

    if custom_base_skin_color is not None and _is_valid_rgb_triplet(custom_base_skin_color):
        base_override = (
            int(custom_base_skin_color[0]),
            int(custom_base_skin_color[1]),
            int(custom_base_skin_color[2]),
        )
        custom_skin_colors['base'] = base_override
        if 'flux' in custom_skin_colors:
            custom_skin_colors['flux'] = base_override

    progress_repository.save_progress(
        level,
        total_coins,
        speed_level,
        bonus_coin_level,
        reset_count,
        prestige_points,
        prestige_upgrade_level,
        selected_skin_id,
        unlocked_skin_ids,
        custom_skin_colors,
    )

def save_mid_game(maze, level, total_coins, speed_level, bonus_coin_level, prestige_points, prestige_upgrade_level):
    data = {
        'level': level,
        'total_coins': total_coins,
        'speed_level': speed_level,
        'bonus_coin_level': bonus_coin_level,
        'prestige_points': prestige_points,
        'prestige_upgrade_level': prestige_upgrade_level,
        'width': maze.width,
        'height': maze.height,
        'grid': maze.grid,
        'player_x': maze.player_x,
        'player_y': maze.player_y,
        'goal_pos': maze.goal_pos,
        'coins': [list(c) for c in maze.coins],
        'collected_coins': maze.collected_coins,
    }
    with open(MID_SAVE_FILE, 'w') as f:
        json.dump(data, f)

def load_mid_game(level):
    if os.path.exists(MID_SAVE_FILE):
        with open(MID_SAVE_FILE, 'r') as f:
            data = json.load(f)
        if data.get('level') == level:
            return data
    return None

def clear_mid_save():
    if os.path.exists(MID_SAVE_FILE):
        os.remove(MID_SAVE_FILE)

def calculate_prestige_reward(level, speed_level, bonus_coin_level):
    progress_score = max(0, (level - 1) + speed_level + bonus_coin_level)
    return max(1, progress_score // 3)

def load_settings():
    global windowed_size, full_screen, display_mode, resolution_setting
    default_mode = 'windowed'
    default_resolution = (WIDTH, HEIGHT)
    default_resolution_setting = 'auto'

    mode = default_mode
    resolution = default_resolution
    loaded_resolution_setting = default_resolution_setting

    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            data = json.load(f)
        loaded_mode = data.get('window_mode', default_mode)
        loaded_resolution = data.get('resolution', default_resolution_setting)

        if loaded_mode in ('windowed', 'fullscreen', 'borderless'):
            mode = loaded_mode
        if loaded_resolution == 'auto':
            loaded_resolution_setting = 'auto'
        elif (
            isinstance(loaded_resolution, list)
            and len(loaded_resolution) == 2
            and isinstance(loaded_resolution[0], int)
            and isinstance(loaded_resolution[1], int)
            and (loaded_resolution[0], loaded_resolution[1]) in RESOLUTION_OPTIONS
        ):
            resolution = (loaded_resolution[0], loaded_resolution[1])
            loaded_resolution_setting = resolution

    display_mode = mode
    resolution_setting = loaded_resolution_setting
    if resolution_setting == 'auto':
        windowed_size = default_resolution
    else:
        windowed_size = resolution_setting
    full_screen = display_mode != 'windowed'

def save_settings():
    saved_resolution = 'auto' if resolution_setting == 'auto' else [resolution_setting[0], resolution_setting[1]]
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(
            {
                'window_mode': display_mode,
                'resolution': saved_resolution,
            },
            f,
        )

def get_auto_resolution_for_mode(mode):
    desktop_sizes = pygame.display.get_desktop_sizes()
    if desktop_sizes:
        desktop_w, desktop_h = desktop_sizes[0]
    else:
        info = pygame.display.Info()
        desktop_w, desktop_h = info.current_w, info.current_h

    if mode == 'windowed':
        auto_w = int(desktop_w * 0.85)
        auto_h = int(desktop_h * 0.85)
        min_w, min_h = 1024, 576
        max_w = max(min_w, desktop_w - 120)
        max_h = max(min_h, desktop_h - 120)
        return max(min_w, min(auto_w, max_w)), max(min_h, min(auto_h, max_h))

    return desktop_w, desktop_h

def get_effective_resolution(mode):
    if resolution_setting == 'auto':
        return get_auto_resolution_for_mode(mode)
    return resolution_setting

def apply_display_mode():
    global full_screen, windowed_size, WIDTH, HEIGHT
    full_screen = display_mode != 'windowed'
    target_resolution = get_effective_resolution(display_mode)
    WIDTH, HEIGHT = target_resolution

    should_lock_cursor = display_mode == 'fullscreen'
    pygame.event.set_grab(should_lock_cursor)
    pygame.mouse.set_visible(True)

    if display_mode == 'fullscreen':
        windowed_size = target_resolution
        return pygame.display.set_mode(target_resolution, pygame.FULLSCREEN)
    if display_mode == 'borderless':
        windowed_size = get_auto_resolution_for_mode('borderless')
        WIDTH, HEIGHT = windowed_size
        return pygame.display.set_mode((0, 0), pygame.NOFRAME)

    windowed_size = target_resolution
    return pygame.display.set_mode(target_resolution)

class Maze:
    def __init__(self, width, height, level=1, speed_level=0, player_skin_id='base'):
        self.width = width
        self.height = height
        self.level = level
        self.grid = [[1 for _ in range(width)] for _ in range(height)]  # 1 = wall, 0 = path
        self.size = 30
        self.speed = BASE_PLAYER_SPEED + speed_level
        custom_skin_colors = load_custom_skin_colors()
        self.player_skin = get_skin_definition(player_skin_id, custom_skin_colors)
        self.player_x = 1 * CELL_SIZE + CELL_SIZE // 2
        self.player_y = 1 * CELL_SIZE + CELL_SIZE // 2
        self.goal_pos = [width - 2, height - 2]
        if self.goal_pos[0] % 2 == 0:
            self.goal_pos[0] = max(1, self.goal_pos[0] - 1)
        if self.goal_pos[1] % 2 == 0:
            self.goal_pos[1] = max(1, self.goal_pos[1] - 1)
        self.coins = []  # List of (x, y) coin positions
        self.collected_coins = 0
        self.generate_maze()

    def restore_from_save(self, data):
        self.grid = data['grid']
        self.player_x = data['player_x']
        self.player_y = data['player_y']
        self.goal_pos = data['goal_pos']
        self.coins = [tuple(c) for c in data['coins']]
        self.collected_coins = data['collected_coins']

    def find_path(self, start, goal):
        from collections import deque
        queue = deque([start])
        came_from = {start: None}

        while queue:
            current = queue.popleft()
            if current == goal:
                path = []
                while current:
                    path.append(current)
                    current = came_from[current]
                return path[::-1]

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = current[0] + dx, current[1] + dy
                if 0 <= nx < self.width and 0 <= ny < self.height and self.grid[ny][nx] == 0 and (nx, ny) not in came_from:
                    came_from[(nx, ny)] = current
                    queue.append((nx, ny))
        return None

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

        # Guarantee a live path; if DFS leaves goal disconnected, carve a direct route
        if self.find_path(start, (self.goal_pos[0], self.goal_pos[1])) is None:
            sx, sy = start
            gx, gy = self.goal_pos
            # carve straight corridor to goal, one axis then the other
            x, y = sx, sy
            while x != gx:
                x += 1 if gx > x else -1
                self.grid[y][x] = 0
                visited.add((x, y))
            while y != gy:
                y += 1 if gy > y else -1
                self.grid[y][x] = 0
                visited.add((x, y))

        # Add a secondary path that connects to existing maze structure
            secondary_candidates = [
                (x, y) for y in range(1, self.height - 1, 2) for x in range(1, self.width - 1, 2)
                if self.grid[y][x] == 0 and abs(x - 1) + abs(y - 1) >= 5 and (x, y) != self.goal_pos
            ]
            if secondary_candidates:
                secondary_start = random.choice(secondary_candidates)
                
                # Find intermediate connection points: open cells reachable from goal but not on main path
                main_path = self.find_path((1, 1), (self.goal_pos[0], self.goal_pos[1]))
                main_path_set = set(main_path) if main_path else set()
                
                # Find cells that are open, reachable from goal, not on main path, and at reasonable distance
                connection_candidates = []
                for y in range(1, self.height - 1):
                    for x in range(1, self.width - 1):
                        dist_from_goal = abs(x - self.goal_pos[0]) + abs(y - self.goal_pos[1])
                        if (self.grid[y][x] == 0 and (x, y) not in main_path_set and 
                            dist_from_goal >= 6 and dist_from_goal <= self.width // 2):  # At least 6 steps from goal, up to half maze width
                            connection_candidates.append((x, y))
                
                if connection_candidates:
                    # Choose a connection point not too close to secondary_start
                    valid_connections = [
                        (x, y) for x, y in connection_candidates 
                        if abs(x - secondary_start[0]) + abs(y - secondary_start[1]) >= 4
                    ]
                    if valid_connections:
                        connection_point = random.choice(valid_connections)
                        
                        # Carve path from secondary_start to connection_point
                        from collections import deque
                        queue = deque([secondary_start])
                        came_from = {secondary_start: None}
                        found = False

                        while queue and not found:
                            current = queue.popleft()
                            if current == connection_point:
                                found = True
                                break
                            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                                nx, ny = current[0] + dx, current[1] + dy
                                if 0 <= nx < self.width and 0 <= ny < self.height and (nx, ny) not in came_from:
                                    came_from[(nx, ny)] = current
                                    queue.append((nx, ny))

                        if found:
                            # Carve the secondary path
                            current = connection_point
                            path_cells = []
                            while current != secondary_start:
                                path_cells.append(current)
                                current = came_from[current]
                            path_cells.append(secondary_start)
                            
                            for cell in path_cells:
                                self.grid[cell[1]][cell[0]] = 0
                                visited.add(cell)
                            
                            # Add minimal obstacles near the secondary path
                            obstacles_added = 0
                            max_obstacles = min(2, len(path_cells) // 4)  # Fewer obstacles, more spaced out
                            random.shuffle(path_cells[1:-1])
                            for cell in path_cells[1:-1]:
                                if obstacles_added >= max_obstacles:
                                    break
                                adjacent_dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                                random.shuffle(adjacent_dirs)
                                for dx, dy in adjacent_dirs:
                                    nx, ny = cell[0] + dx, cell[1] + dy
                                    if (0 < nx < self.width - 1 and 0 < ny < self.height - 1 and 
                                        self.grid[ny][nx] == 0 and (nx, ny) not in path_cells and 
                                        (nx, ny) not in main_path_set and abs(nx - 1) + abs(ny - 1) > 3):
                                        self.grid[ny][nx] = 1
                                        obstacles_added += 1
                                        break

        # Fill isolated pockets that are completely surrounded by walls
        visited = [[False for _ in range(self.width)] for _ in range(self.height)]
        from collections import deque
        queue = deque([(1, 1)])  # Start from the player start position
        visited[1][1] = True
        
        # Flood fill to mark all reachable areas
        while queue:
            x, y = queue.popleft()
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if (0 <= nx < self.width and 0 <= ny < self.height and 
                    not visited[ny][nx] and self.grid[ny][nx] == 0):
                    visited[ny][nx] = True
                    queue.append((nx, ny))
        
        # Fill unreachable open spaces with walls
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == 0 and not visited[y][x]:
                    self.grid[y][x] = 1

        # Add accessible dead ends for more interesting navigation
        dead_end_candidates = []
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                if visited[y][x] and self.grid[y][x] == 0:  # Reachable open cell
                    # Check if it has at least 3 adjacent walls (potential dead end spot)
                    wall_count = 0
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nx, ny = x + dx, y + dy
                        if self.grid[ny][nx] == 1:
                            wall_count += 1
                    if wall_count >= 3:
                        dead_end_candidates.append((x, y))
        
        # Create dead ends by carving short branches
        random.shuffle(dead_end_candidates)
        dead_ends_added = 0
        max_dead_ends = min(5, len(dead_end_candidates) // 2)  # Up to 5 dead ends
        
        for x, y in dead_end_candidates:
            if dead_ends_added >= max_dead_ends:
                break
            # Try to extend in an open direction
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            random.shuffle(directions)
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if (1 <= nx < self.width - 1 and 1 <= ny < self.height - 1 and 
                    self.grid[ny][nx] == 1):  # Wall to carve through
                    # Carve 1-3 steps
                    steps = random.randint(1, 3)
                    for step in range(1, steps + 1):
                        cx, cy = x + dx * step, y + dy * step
                        if (1 <= cx < self.width - 1 and 1 <= cy < self.height - 1 and 
                            self.grid[cy][cx] == 1):
                            self.grid[cy][cx] = 0
                            visited[cy][cx] = True
                        else:
                            break
                    dead_ends_added += 1
                    break

        # Recompute reachability and clean any disconnected open cells
        visited = [[False for _ in range(self.width)] for _ in range(self.height)]
        from collections import deque
        queue = deque([start])
        visited[start[1]][start[0]] = True

        while queue:
            x, y = queue.popleft()
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if (0 <= nx < self.width and 0 <= ny < self.height and
                    not visited[ny][nx] and self.grid[ny][nx] == 0):
                    visited[ny][nx] = True
                    queue.append((nx, ny))

        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == 0 and not visited[y][x]:
                    self.grid[y][x] = 1

        # Coin reachability map: don't place coins on tiles that require stepping on goal first
        goal = (self.goal_pos[0], self.goal_pos[1])
        coin_reachable = [[False for _ in range(self.width)] for _ in range(self.height)]
        queue = deque([start])
        coin_reachable[start[1]][start[0]] = True

        while queue:
            x, y = queue.popleft()
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if (nx, ny) == goal:
                    continue
                if (0 <= nx < self.width and 0 <= ny < self.height and
                    not coin_reachable[ny][nx] and self.grid[ny][nx] == 0):
                    coin_reachable[ny][nx] = True
                    queue.append((nx, ny))

        # Place coins in the maze
        num_coins = min(self.level, 30)  # Level number of coins, max 30
        coin_candidates = [
            (x, y) for y in range(1, self.height - 1) for x in range(1, self.width - 1)
            if self.grid[y][x] == 0 and coin_reachable[y][x] and (x, y) != (1, 1) and (x, y) != tuple(self.goal_pos)
        ]
        random.shuffle(coin_candidates)
        self.coins = coin_candidates[:num_coins]

    def draw(self, screen, offset_x=0, offset_y=0, scale=1.0):
        # Center maze representation in the available render surface when needed
        maze_pixel_width = self.width * CELL_SIZE * scale
        maze_pixel_height = self.height * CELL_SIZE * scale

        if offset_x == 0 and offset_y == 0:
            # if caller doesn't provide offsets, center by default
            offset_x = max(0, (WIDTH - maze_pixel_width) // 2)
            offset_y = max(0, (HEIGHT - maze_pixel_height) // 2)

        scaled_cell_size = int(CELL_SIZE * scale)
        scaled_player_size = int(self.size * scale)

        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == 1:
                    pygame.draw.rect(
                        screen,
                        WALL_COLOR,
                        (offset_x + x * scaled_cell_size, offset_y + y * scaled_cell_size, scaled_cell_size, scaled_cell_size),
                    )

        # Draw goal
        pygame.draw.rect(
            screen,
            GOAL_COLOR,
            (offset_x + self.goal_pos[0] * scaled_cell_size, offset_y + self.goal_pos[1] * scaled_cell_size, scaled_cell_size, scaled_cell_size),
        )

        # Draw coins
        for x, y in self.coins:
            pygame.draw.circle(
                screen,
                COIN_COLOR,
                (offset_x + x * scaled_cell_size + scaled_cell_size // 2, offset_y + y * scaled_cell_size + scaled_cell_size // 2),
                max(1, scaled_cell_size // 3),
            )

        # Draw player
        player_rect = pygame.Rect(
            offset_x + int(self.player_x * scale) - scaled_player_size // 2,
            offset_y + int(self.player_y * scale) - scaled_player_size // 2,
            scaled_player_size,
            scaled_player_size,
        )
        draw_skin_preview(screen, player_rect, self.player_skin)

    def move_player(self, keys):
        # Handle horizontal movement (arrows + WASD)
        new_x = self.player_x
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            new_x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            new_x += self.speed
        
        player_rect = pygame.Rect(new_x - self.size // 2, self.player_y - self.size // 2, self.size, self.size)
        collision = False
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == 1:
                    wall_rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    if player_rect.colliderect(wall_rect):
                        collision = True
                        break
            if collision:
                break
        if not collision:
            self.player_x = new_x
        
        # Handle vertical movement (arrows + WASD)
        new_y = self.player_y
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            new_y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            new_y += self.speed
        
        player_rect = pygame.Rect(self.player_x - self.size // 2, new_y - self.size // 2, self.size, self.size)
        collision = False
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == 1:
                    wall_rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    if player_rect.colliderect(wall_rect):
                        collision = True
                        break
            if collision:
                break
        if not collision:
            self.player_y = new_y

        # Check for coin collection
        player_grid_x = int(self.player_x // CELL_SIZE)
        player_grid_y = int(self.player_y // CELL_SIZE)
        if (player_grid_x, player_grid_y) in self.coins:
            self.coins.remove((player_grid_x, player_grid_y))
            self.collected_coins += 1

    def check_win(self):
        goal_rect = pygame.Rect(self.goal_pos[0] * CELL_SIZE, self.goal_pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        player_rect = pygame.Rect(self.player_x - self.size // 2, self.player_y - self.size // 2, self.size, self.size)
        return player_rect.colliderect(goal_rect)

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = BUTTON_COLOR

    def draw(self, screen):
        shadow_rect = self.rect.move(0, 4)
        pygame.draw.rect(screen, (20, 25, 45), shadow_rect, border_radius=12)
        pygame.draw.rect(screen, self.color, self.rect, border_radius=12)
        pygame.draw.rect(screen, (210, 220, 245), self.rect, 2, border_radius=12)
        text_surf = small_font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_hovered(self, pos):
        return self.rect.collidepoint(pos)

def draw_text(screen, text, x, y, font=font, color=TEXT_COLOR):
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=(x, y))
    screen.blit(surf, rect)

def main_menu(screen, render_surface):
    global full_screen, display_mode
    menu_button_top = HEIGHT // 2 - 24
    start_button = Button(WIDTH // 2 - 140, menu_button_top, 280, 54, "Start Game")
    store_button = Button(WIDTH // 2 - 140, menu_button_top + 70, 280, 54, "Store")
    customization_button = Button(WIDTH // 2 - 140, menu_button_top + 140, 280, 54, "Customization")
    settings_button = Button(WIDTH // 2 - 140, menu_button_top + 210, 280, 54, "Settings")
    quit_button = Button(WIDTH // 2 - 140, menu_button_top + 280, 280, 54, "Quit")
    reset_button = Button(WIDTH // 2 - 140, menu_button_top + 350, 280, 54, "Reset Progress")
    reset_popup_width = max(520, min(680, WIDTH - 120))
    reset_popup_height = max(300, min(380, HEIGHT - 120))
    reset_popup_rect = pygame.Rect(
        WIDTH // 2 - reset_popup_width // 2,
        HEIGHT // 2 - reset_popup_height // 2,
        reset_popup_width,
        reset_popup_height,
    )
    yes_button = Button(WIDTH // 2 - 170, reset_popup_rect.bottom - 82, 140, 50, "Yes")
    no_button = Button(WIDTH // 2 + 30, reset_popup_rect.bottom - 82, 140, 50, "No")
    ok_button = Button(WIDTH // 2 - 70, reset_popup_rect.bottom - 82, 140, 50, "OK")

    gradient_surface = pygame.Surface((WIDTH, HEIGHT))
    top_color = (22, 32, 62)
    bottom_color = (12, 16, 30)
    for y in range(HEIGHT):
        t = y / max(1, HEIGHT - 1)
        color = (
            int(top_color[0] * (1 - t) + bottom_color[0] * t),
            int(top_color[1] * (1 - t) + bottom_color[1] * t),
            int(top_color[2] * (1 - t) + bottom_color[2] * t),
        )
        pygame.draw.line(gradient_surface, color, (0, y), (WIDTH, y))

    card_rect = pygame.Rect(WIDTH // 2 - 245, HEIGHT // 2 - 95, 490, 530)

    awaiting_reset_confirmation = False
    reset_feedback_waiting = False

    while True:
        render_surface.blit(gradient_surface, (0, 0))

        current_level, current_coins = load_progress()
        current_speed_level = load_speed_level()
        current_bonus_level = load_bonus_coin_level()
        current_resets = load_reset_count()
        current_prestige = load_prestige_points()
        reset_reward_preview = calculate_prestige_reward(current_level, current_speed_level, current_bonus_level)

        glow_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.circle(glow_surface, (120, 160, 255, 45), (WIDTH // 2, HEIGHT // 4), 190)
        render_surface.blit(glow_surface, (0, 0))

        draw_text(render_surface, "Square Game", WIDTH // 2 + 2, HEIGHT // 4 + 2, font, (20, 25, 40))
        draw_text(render_surface, "Square Game", WIDTH // 2, HEIGHT // 4, font, (245, 250, 255))
        draw_text(render_surface, "Escape the maze.", WIDTH // 2, HEIGHT // 4 + 46, small_font, (190, 205, 240))
        draw_text(render_surface, f"Saved Level: {current_level}   |   Wallet: {current_coins}", WIDTH // 2, HEIGHT // 4 + 80, small_font, (170, 185, 220))
        draw_text(render_surface, f"Resets: {current_resets}   |   Prestige: {current_prestige}", WIDTH // 2, HEIGHT // 4 + 106, small_font, (170, 185, 220))

        if not awaiting_reset_confirmation and not reset_feedback_waiting:
            panel_surface = pygame.Surface((card_rect.width, card_rect.height), pygame.SRCALPHA)
            panel_surface.fill((26, 36, 68, 195))
            render_surface.blit(panel_surface, card_rect.topleft)
            pygame.draw.rect(render_surface, (165, 180, 225), card_rect, 2, border_radius=16)

        mouse_pos = pygame.mouse.get_pos()
        screen_w, screen_h = screen.get_size()
        if full_screen:
            scale = min(screen_w / WIDTH, screen_h / HEIGHT)
            scaled_width = int(WIDTH * scale)
            scaled_height = int(HEIGHT * scale)
            offset_x = (screen_w - scaled_width) // 2
            offset_y = (screen_h - scaled_height) // 2
            if scale > 0:
                local_mouse_pos = ((mouse_pos[0] - offset_x) / scale, (mouse_pos[1] - offset_y) / scale)
            else:
                local_mouse_pos = (mouse_pos[0] - offset_x, mouse_pos[1] - offset_y)
        else:
            offset_x = (screen_w - WIDTH) // 2
            offset_y = (screen_h - HEIGHT) // 2
            local_mouse_pos = (mouse_pos[0] - offset_x, mouse_pos[1] - offset_y)

        if not awaiting_reset_confirmation and not reset_feedback_waiting:
            for button in [start_button, store_button, customization_button, settings_button, quit_button, reset_button]:
                if button.is_hovered(local_mouse_pos):
                    button.color = BUTTON_HOVER
                else:
                    button.color = BUTTON_COLOR
                button.draw(render_surface)
        elif awaiting_reset_confirmation:
            popup_surface = pygame.Surface((reset_popup_rect.width, reset_popup_rect.height), pygame.SRCALPHA)
            popup_surface.fill((26, 36, 68, 225))
            render_surface.blit(popup_surface, reset_popup_rect.topleft)
            pygame.draw.rect(render_surface, (170, 185, 225), reset_popup_rect, 2, border_radius=12)

            title_y = reset_popup_rect.top + 38
            body_panel = pygame.Rect(reset_popup_rect.left + 56, reset_popup_rect.top + 92, reset_popup_rect.width - 112, 128)
            detail_y = body_panel.bottom + 30

            inner_surface = pygame.Surface((body_panel.width, body_panel.height), pygame.SRCALPHA)
            inner_surface.fill((31, 45, 83, 165))
            render_surface.blit(inner_surface, body_panel.topleft)
            pygame.draw.rect(render_surface, (85, 110, 170), body_panel, 1, border_radius=10)

            draw_text(render_surface, "Reset Progress?", WIDTH // 2, title_y, font, (245, 250, 255))
            draw_text(render_surface, "This resets Level, Wallet, Speed, Coin Bonus,", WIDTH // 2, body_panel.top + 42, small_font, (200, 212, 240))
            draw_text(render_surface, "and Prestige Power upgrade back to 0.", WIDTH // 2, body_panel.top + 72, small_font, (200, 212, 240))
            draw_text(render_surface, f"Reward: +{reset_reward_preview} Prestige Points", WIDTH // 2, detail_y, small_font, (235, 215, 140))
            draw_text(render_surface, f"Prestige after reset: {current_prestige + reset_reward_preview}", WIDTH // 2, detail_y + 28, small_font, (235, 215, 140))
            yes_button.draw(render_surface)
            no_button.draw(render_surface)
        elif reset_feedback_waiting:
            popup_surface = pygame.Surface((reset_popup_rect.width, reset_popup_rect.height), pygame.SRCALPHA)
            popup_surface.fill((26, 36, 68, 225))
            render_surface.blit(popup_surface, reset_popup_rect.topleft)
            pygame.draw.rect(render_surface, (170, 185, 225), reset_popup_rect, 2, border_radius=12)
            draw_text(render_surface, "Progress was reset", WIDTH // 2, reset_popup_rect.top + 78, font, (245, 250, 255))
            ok_button.draw(render_surface)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit', screen
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not awaiting_reset_confirmation and not reset_feedback_waiting:
                    if start_button.is_hovered(local_mouse_pos):
                        return 'start', screen
                    if store_button.is_hovered(local_mouse_pos):
                        return 'store', screen
                    if customization_button.is_hovered(local_mouse_pos):
                        return 'customization', screen
                    if settings_button.is_hovered(local_mouse_pos):
                        return 'settings', screen
                    if quit_button.is_hovered(local_mouse_pos):
                        return 'quit', screen
                    if reset_button.is_hovered(local_mouse_pos):
                        awaiting_reset_confirmation = True
                elif awaiting_reset_confirmation:
                    if yes_button.is_hovered(local_mouse_pos):
                        awaiting_reset_confirmation = False
                        reset_feedback_waiting = True
                    if no_button.is_hovered(local_mouse_pos):
                        awaiting_reset_confirmation = False
                elif reset_feedback_waiting:
                    if ok_button.is_hovered(local_mouse_pos):
                        return 'reset', screen
            if event.type == pygame.KEYDOWN:
                if not awaiting_reset_confirmation and not reset_feedback_waiting:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        return 'start', screen
                    if event.key == pygame.K_ESCAPE:
                        return 'quit', screen
                    if event.key == pygame.K_r:
                        awaiting_reset_confirmation = True
                elif awaiting_reset_confirmation:
                    if event.key == pygame.K_y:
                        awaiting_reset_confirmation = False
                        reset_feedback_waiting = True
                    if event.key == pygame.K_n or event.key == pygame.K_ESCAPE:
                        awaiting_reset_confirmation = False
                elif reset_feedback_waiting:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                        return 'reset', screen
                if event.key == pygame.K_F11:
                    display_mode = 'windowed' if display_mode != 'windowed' else 'fullscreen'
                    screen = apply_display_mode()
                    save_settings()
                    pygame.time.wait(200)

        screen.fill(BG_COLOR)
        screen_w, screen_h = screen.get_size()
        if awaiting_reset_confirmation or reset_feedback_waiting:
            overlay = pygame.Surface((screen_w, screen_h), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0, 0))
        if full_screen:
            scale = min(screen_w / WIDTH, screen_h / HEIGHT)
            scaled_surface = pygame.transform.scale(render_surface, (int(WIDTH * scale), int(HEIGHT * scale)))
            scaled_width = scaled_surface.get_width()
            scaled_height = scaled_surface.get_height()
            offset_x = (screen_w - scaled_width) // 2
            offset_y = (screen_h - scaled_height) // 2
            screen.blit(scaled_surface, (offset_x, offset_y))
        else:
            offset_x = (screen_w - WIDTH) // 2
            offset_y = (screen_h - HEIGHT) // 2
            screen.blit(render_surface, (offset_x, offset_y))
        pygame.display.flip()

def settings_menu(screen, render_surface):
    global display_mode, windowed_size, resolution_setting

    mode_cycle = ['windowed', 'fullscreen', 'borderless']
    mode_names = {
        'windowed': 'Windowed',
        'fullscreen': 'Fullscreen',
        'borderless': 'Fullscreen Window',
    }

    try:
        resolution_index = RESOLUTION_OPTIONS.index(resolution_setting)
    except ValueError:
        resolution_index = RESOLUTION_OPTIONS.index('auto')
        resolution_setting = 'auto'

    mode_button = Button(WIDTH // 2 - 180, HEIGHT // 2 - 20, 360, 54, "")
    resolution_prev = Button(WIDTH // 2 - 210, HEIGHT // 2 + 130, 80, 54, "<")
    resolution_next = Button(WIDTH // 2 + 130, HEIGHT // 2 + 130, 80, 54, ">")
    back_button = Button(WIDTH // 2 - 140, HEIGHT // 2 + 225, 280, 54, "Back")
    clock = pygame.time.Clock()

    gradient_surface = pygame.Surface((WIDTH, HEIGHT))
    top_color = (22, 32, 62)
    bottom_color = (12, 16, 30)
    for y in range(HEIGHT):
        t = y / max(1, HEIGHT - 1)
        color = (
            int(top_color[0] * (1 - t) + bottom_color[0] * t),
            int(top_color[1] * (1 - t) + bottom_color[1] * t),
            int(top_color[2] * (1 - t) + bottom_color[2] * t),
        )
        pygame.draw.line(gradient_surface, color, (0, y), (WIDTH, y))

    card_rect = pygame.Rect(WIDTH // 2 - 320, HEIGHT // 2 - 150, 640, 500)

    while True:
        render_surface.blit(gradient_surface, (0, 0))
        draw_text(render_surface, "Settings", WIDTH // 2 + 2, HEIGHT // 4 + 2, font, (20, 25, 40))
        draw_text(render_surface, "Settings", WIDTH // 2, HEIGHT // 4, font, (245, 250, 255))

        panel_surface = pygame.Surface((card_rect.width, card_rect.height), pygame.SRCALPHA)
        panel_surface.fill((26, 36, 68, 195))
        render_surface.blit(panel_surface, card_rect.topleft)
        pygame.draw.rect(render_surface, (165, 180, 225), card_rect, 2, border_radius=16)

        draw_text(render_surface, "Window Type", WIDTH // 2, HEIGHT // 2 - 58, small_font, (190, 205, 240))
        mode_button.text = mode_names[display_mode]

        draw_text(render_surface, "Resolution", WIDTH // 2, HEIGHT // 2 + 72, small_font, (190, 205, 240))
        current_resolution = RESOLUTION_OPTIONS[resolution_index]
        if current_resolution == 'auto':
            preview_w, preview_h = get_auto_resolution_for_mode(display_mode)
            resolution_label = f"Auto ({preview_w} x {preview_h})"
        else:
            resolution_label = f"{current_resolution[0]} x {current_resolution[1]}"
        draw_text(render_surface, resolution_label, WIDTH // 2, HEIGHT // 2 + 108, small_font, (230, 235, 245))
        draw_text(render_surface, "(Auto follows selected Window Type)", WIDTH // 2, HEIGHT // 2 + 210, small_font, (165, 180, 215))

        mouse_pos = pygame.mouse.get_pos()
        screen_w, screen_h = screen.get_size()
        if full_screen:
            scale = min(screen_w / WIDTH, screen_h / HEIGHT)
            offset_x = (screen_w - int(WIDTH * scale)) // 2
            offset_y = (screen_h - int(HEIGHT * scale)) // 2
            local_mouse_pos = ((mouse_pos[0] - offset_x) / scale, (mouse_pos[1] - offset_y) / scale) if scale > 0 else mouse_pos
        else:
            offset_x = (screen_w - WIDTH) // 2
            offset_y = (screen_h - HEIGHT) // 2
            local_mouse_pos = (mouse_pos[0] - offset_x, mouse_pos[1] - offset_y)

        for button in [mode_button, resolution_prev, resolution_next, back_button]:
            button.color = BUTTON_HOVER if button.is_hovered(local_mouse_pos) else BUTTON_COLOR
            button.draw(render_surface)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit', screen
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mode_button.is_hovered(local_mouse_pos):
                    current_mode_index = mode_cycle.index(display_mode)
                    display_mode = mode_cycle[(current_mode_index + 1) % len(mode_cycle)]
                    screen = apply_display_mode()
                    save_settings()
                    return 'settings', screen
                if resolution_prev.is_hovered(local_mouse_pos):
                    resolution_index = (resolution_index - 1) % len(RESOLUTION_OPTIONS)
                    resolution_setting = RESOLUTION_OPTIONS[resolution_index]
                    if resolution_setting != 'auto':
                        windowed_size = resolution_setting
                    screen = apply_display_mode()
                    save_settings()
                    return 'settings', screen
                if resolution_next.is_hovered(local_mouse_pos):
                    resolution_index = (resolution_index + 1) % len(RESOLUTION_OPTIONS)
                    resolution_setting = RESOLUTION_OPTIONS[resolution_index]
                    if resolution_setting != 'auto':
                        windowed_size = resolution_setting
                    screen = apply_display_mode()
                    save_settings()
                    return 'settings', screen
                if back_button.is_hovered(local_mouse_pos):
                    return 'menu', screen
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'menu', screen

        screen.fill(BG_COLOR)
        if full_screen:
            scale = min(screen_w / WIDTH, screen_h / HEIGHT)
            scaled_surface = pygame.transform.scale(render_surface, (int(WIDTH * scale), int(HEIGHT * scale)))
            screen.blit(scaled_surface, ((screen_w - scaled_surface.get_width()) // 2, (screen_h - scaled_surface.get_height()) // 2))
        else:
            screen.blit(render_surface, ((screen_w - WIDTH) // 2, (screen_h - HEIGHT) // 2))
        pygame.display.flip()
        clock.tick(FPS)

def customization_menu(screen, render_surface, current_level, total_coins, prestige_points):
    clock = pygame.time.Clock()

    gradient_surface = pygame.Surface((WIDTH, HEIGHT))
    top_color = (22, 32, 62)
    bottom_color = (12, 16, 30)
    for y in range(HEIGHT):
        t = y / max(1, HEIGHT - 1)
        color = (
            int(top_color[0] * (1 - t) + bottom_color[0] * t),
            int(top_color[1] * (1 - t) + bottom_color[1] * t),
            int(top_color[2] * (1 - t) + bottom_color[2] * t),
        )
        pygame.draw.line(gradient_surface, color, (0, y), (WIDTH, y))

    selected_skin_id, unlocked_skin_ids = load_skin_state()
    custom_skin_colors = load_custom_skin_colors()
    active_slider = None
    page_index = 0

    purchase_message = ""
    purchase_color = (180, 185, 220)

    def persist_skin_progress():
        save_progress(
            current_level,
            total_coins,
            prestige_points=prestige_points,
            selected_skin_id=selected_skin_id,
            unlocked_skin_ids=unlocked_skin_ids,
            custom_skin_colors=custom_skin_colors,
        )

    def is_unlocked_by_level(skin):
        return skin.get('unlock_type') == 'level' and current_level >= skin['cost']

    def is_skin_unlocked(skin):
        if skin['id'] in unlocked_skin_ids:
            return True
        if skin.get('unlock_type') == 'default':
            return True
        return is_unlocked_by_level(skin)

    skin_index_map = {skin['id']: idx for idx, skin in enumerate(PLAYER_SKINS)}

    def skin_display_sort_key(skin):
        if skin.get('unlock_type') == 'default' or skin.get('currency') == 'free':
            group = 0
        elif skin.get('currency') == 'coins':
            group = 1
        elif skin.get('currency') == 'level':
            group = 2
        elif skin.get('currency') == 'prestige':
            group = 3
        else:
            group = 4
        return (group, skin_index_map.get(skin['id'], 999))

    while True:
        render_surface.blit(gradient_surface, (0, 0))

        ordered_skins = sorted(PLAYER_SKINS, key=skin_display_sort_key)

        draw_text(render_surface, "Customization", WIDTH // 2 + 2, HEIGHT // 4 + 2, font, (20, 25, 40))
        draw_text(render_surface, "Customization", WIDTH // 2, HEIGHT // 4, font, (245, 250, 255))

        panel_margin_x = 36
        panel_top = int(HEIGHT * 0.26)
        panel_bottom = HEIGHT - 24
        card_rect = pygame.Rect(panel_margin_x, panel_top, WIDTH - panel_margin_x * 2, panel_bottom - panel_top)

        col_gap = 14
        row_gap = 10
        top_controls_h = 274
        footer_h = 78
        grid_padding_x = 14
        grid_top = card_rect.top + top_controls_h
        available_grid_h = max(180, card_rect.height - top_controls_h - footer_h)

        cols = 4
        for candidate_cols in [4, 3, 2]:
            candidate_card_w = (card_rect.width - grid_padding_x * 2 - col_gap * (candidate_cols - 1)) // candidate_cols
            if candidate_card_w >= 200:
                cols = candidate_cols
                break

        max_rows_per_page = 3 if available_grid_h >= 300 else 2
        cards_per_page = max(1, cols * max_rows_per_page)
        total_pages = max(1, (len(ordered_skins) + cards_per_page - 1) // cards_per_page)
        page_index = max(0, min(page_index, total_pages - 1))

        start_index = page_index * cards_per_page
        end_index = min(len(ordered_skins), start_index + cards_per_page)
        page_skins = ordered_skins[start_index:end_index]
        rows = max(1, (len(page_skins) + cols - 1) // cols)

        card_w = (card_rect.width - grid_padding_x * 2 - col_gap * (cols - 1)) // cols
        card_h = (available_grid_h - row_gap * (rows - 1)) // rows
        card_w = min(320, max(200, card_w))
        card_h = min(132, max(92, card_h))
        total_grid_w = card_w * cols + col_gap * (cols - 1)
        grid_start_x = WIDTH // 2 - total_grid_w // 2

        slider_width = max(220, min(430, card_rect.width - 360))
        slider_start_x = WIDTH // 2 - slider_width // 2
        header_currency_y = card_rect.top + 84
        header_skin_y = header_currency_y + 30
        preview_size = 28
        preview_top = header_skin_y + 16
        header_rgb_y = preview_top + preview_size + 18

        slider_start_y = header_rgb_y + 16
        slider_step = 30
        slider_height = 10
        slider_labels = [('R', 0, (255, 110, 110)), ('G', 1, (120, 255, 150)), ('B', 2, (140, 170, 255))]
        slider_rects = {}
        for label, channel, color in slider_labels:
            slider_rects[channel] = pygame.Rect(slider_start_x, slider_start_y + channel * slider_step, slider_width, slider_height)

        skin_buttons = {}
        for index, skin in enumerate(page_skins):
            col = index % cols
            row = index // cols
            skin_x = grid_start_x + col * (card_w + col_gap)
            skin_y = grid_top + row * (card_h + row_gap)
            button_w = min(150, card_w - 28)
            button_x = skin_x + (card_w - button_w) // 2
            button_y = skin_y + card_h - 36
            skin_buttons[skin['id']] = {
                'rect': pygame.Rect(skin_x, skin_y, card_w, card_h),
                'button': Button(button_x, button_y, button_w, 30, ""),
            }

        back_button = Button(WIDTH // 2 - 140, card_rect.bottom - 50, 280, 38, "Back")
        prev_page_button = Button(card_rect.left + 16, card_rect.bottom - 50, 110, 38, "Prev")
        next_page_button = Button(card_rect.right - 126, card_rect.bottom - 50, 110, 38, "Next")
        purchase_y = back_button.rect.y - 16

        panel_surface = pygame.Surface((card_rect.width, card_rect.height), pygame.SRCALPHA)
        panel_surface.fill((26, 36, 68, 195))
        render_surface.blit(panel_surface, card_rect.topleft)
        pygame.draw.rect(render_surface, (165, 180, 225), card_rect, 2, border_radius=16)

        draw_text(render_surface, f"Coins: {total_coins}", WIDTH // 2 - 210, header_currency_y, small_font, (190, 205, 240))
        draw_text(render_surface, f"Prestige: {prestige_points}", WIDTH // 2, header_currency_y, small_font, (225, 205, 135))
        draw_text(render_surface, f"Level: {current_level}", WIDTH // 2 + 210, header_currency_y, small_font, (190, 205, 240))

        selected_skin = get_skin_definition(selected_skin_id, custom_skin_colors)
        selected_skin_rgb = list(custom_skin_colors.get(selected_skin_id, selected_skin['color']))
        draw_text(render_surface, f"Current Skin: {selected_skin['name']}", WIDTH // 2, header_skin_y, small_font, (230, 235, 245))
        preview_rect = pygame.Rect(WIDTH // 2 - preview_size // 2, preview_top, preview_size, preview_size)
        draw_skin_preview(render_surface, preview_rect, selected_skin)
        pygame.draw.rect(render_surface, (220, 225, 240), preview_rect, 2)

        draw_text(render_surface, "Custom RGB (Selected Skin)", WIDTH // 2, header_rgb_y, small_font, (210, 220, 245))
        for label, channel, color in slider_labels:
            rect = slider_rects[channel]
            pygame.draw.rect(render_surface, (46, 60, 98), rect, border_radius=4)
            fill_rect = pygame.Rect(rect.x, rect.y, int((selected_skin_rgb[channel] / 255) * rect.width), rect.height)
            pygame.draw.rect(render_surface, color, fill_rect, border_radius=4)
            knob_x = rect.x + int((selected_skin_rgb[channel] / 255) * rect.width)
            knob = pygame.Rect(knob_x - 6, rect.centery - 7, 12, 14)
            pygame.draw.rect(render_surface, (235, 240, 255), knob, border_radius=3)
            draw_text(render_surface, f"{label}: {selected_skin_rgb[channel]}", rect.right + 62, rect.centery, small_font, (210, 220, 245))

        mouse_pos = pygame.mouse.get_pos()
        screen_w, screen_h = screen.get_size()
        if full_screen:
            scale = min(screen_w / WIDTH, screen_h / HEIGHT)
            offset_x = (screen_w - int(WIDTH * scale)) // 2
            offset_y = (screen_h - int(HEIGHT * scale)) // 2
            local_mouse_pos = ((mouse_pos[0] - offset_x) / scale, (mouse_pos[1] - offset_y) / scale) if scale > 0 else mouse_pos
        else:
            offset_x = (screen_w - WIDTH) // 2
            offset_y = (screen_h - HEIGHT) // 2
            local_mouse_pos = (mouse_pos[0] - offset_x, mouse_pos[1] - offset_y)

        for skin in page_skins:
            skin_rect = skin_buttons[skin['id']]['rect']
            skin_x, skin_y = skin_rect.x, skin_rect.y
            display_skin = get_skin_definition(skin['id'], custom_skin_colors)

            if is_unlocked_by_level(skin) and skin['id'] not in unlocked_skin_ids:
                unlocked_skin_ids.append(skin['id'])

            is_selected = skin['id'] == selected_skin_id
            unlocked = is_skin_unlocked(skin)

            border_color = (220, 225, 245) if is_selected else (130, 150, 205)
            fill_color = (44, 60, 102) if is_selected else (34, 48, 84)
            pygame.draw.rect(render_surface, fill_color, skin_rect, border_radius=12)
            pygame.draw.rect(render_surface, border_color, skin_rect, 2, border_radius=12)

            color_box = pygame.Rect(skin_x + 12, skin_y + 12, 30, 30)
            draw_skin_preview(render_surface, color_box, display_skin)
            pygame.draw.rect(render_surface, (210, 220, 245), color_box, 2)

            label_center_x = skin_x + card_w // 2 + 10
            draw_text(render_surface, skin['name'], label_center_x, skin_y + 20, small_font, (245, 250, 255))
            tier_color = (225, 205, 135) if skin['tier'] == 'Premium' else ((175, 220, 255) if skin['tier'] == 'Level' else (190, 205, 240))
            draw_text(render_surface, skin['tier'], label_center_x, skin_y + 36, small_font, tier_color)

            if skin.get('unlock_type') == 'level' and not unlocked:
                status_text = f"Unlocks at Level {skin['cost']}"
                status_color = (205, 190, 170)
            elif skin['currency'] == 'free':
                status_text = "Free"
                status_color = (190, 205, 240)
            elif unlocked:
                status_text = "Owned"
                status_color = (140, 235, 170)
            elif skin['currency'] == 'coins':
                status_text = f"Cost: {skin['cost']} coins"
                status_color = (190, 205, 240)
            elif skin['currency'] == 'prestige':
                status_text = f"Cost: {skin['cost']} prestige"
                status_color = (225, 205, 135)
            else:
                status_text = "Locked"
                status_color = (205, 190, 170)
            draw_text(render_surface, status_text, label_center_x, skin_y + 52, small_font, status_color)

            button = skin_buttons[skin['id']]['button']
            if is_selected:
                button.text = "Selected"
            elif unlocked:
                button.text = "Select"
            elif skin.get('unlock_type') == 'level':
                button.text = "Locked"
            else:
                button.text = "Buy"
            button.color = BUTTON_HOVER if button.is_hovered(local_mouse_pos) else BUTTON_COLOR
            button.draw(render_surface)

        draw_text(render_surface, f"Page {page_index + 1}/{total_pages}", WIDTH // 2, back_button.rect.centery, small_font, (190, 205, 240))
        prev_page_button.color = BUTTON_HOVER if prev_page_button.is_hovered(local_mouse_pos) else BUTTON_COLOR
        next_page_button.color = BUTTON_HOVER if next_page_button.is_hovered(local_mouse_pos) else BUTTON_COLOR
        prev_page_button.draw(render_surface)
        next_page_button.draw(render_surface)
        back_button.color = BUTTON_HOVER if back_button.is_hovered(local_mouse_pos) else BUTTON_COLOR
        back_button.draw(render_surface)
        draw_text(render_surface, purchase_message, WIDTH // 2, purchase_y, small_font, purchase_color)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit', screen, total_coins, prestige_points

            if event.type == pygame.MOUSEBUTTONDOWN:
                slider_hit = False
                for _, channel, _ in slider_labels:
                    slider_rect = slider_rects[channel].inflate(0, 12)
                    if slider_rect.collidepoint(local_mouse_pos):
                        slider_hit = True
                        active_slider = channel
                        ratio = (local_mouse_pos[0] - slider_rects[channel].x) / max(1, slider_rects[channel].width)
                        selected_skin_rgb[channel] = max(0, min(255, int(ratio * 255)))
                        custom_skin_colors[selected_skin_id] = tuple(selected_skin_rgb)
                        purchase_message = f"{selected_skin['name']} RGB updated."
                        purchase_color = (140, 235, 170)
                        persist_skin_progress()
                        break
                if slider_hit:
                    continue

                handled_skin_action = False
                for skin in page_skins:
                    button = skin_buttons[skin['id']]['button']
                    if not button.is_hovered(local_mouse_pos):
                        continue

                    handled_skin_action = True
                    unlocked = is_skin_unlocked(skin)
                    is_selected = skin['id'] == selected_skin_id

                    if is_selected:
                        purchase_message = "That skin is already selected."
                        purchase_color = (180, 185, 220)
                        break

                    if unlocked:
                        if skin['id'] not in unlocked_skin_ids:
                            unlocked_skin_ids.append(skin['id'])
                        selected_skin_id = skin['id']
                        persist_skin_progress()
                        purchase_message = f"Selected {skin['name']}!"
                        purchase_color = (140, 235, 170)
                        break

                    if skin.get('unlock_type') == 'level':
                        purchase_message = f"Reach Level {skin['cost']} to unlock {skin['name']}."
                        purchase_color = (235, 170, 130)
                        break

                    if skin['currency'] == 'coins':
                        if total_coins >= skin['cost']:
                            total_coins -= skin['cost']
                            unlocked_skin_ids.append(skin['id'])
                            selected_skin_id = skin['id']
                            persist_skin_progress()
                            purchase_message = f"Bought {skin['name']} for {skin['cost']} coins!"
                            purchase_color = (140, 235, 170)
                        else:
                            purchase_message = f"Not enough coins (need {skin['cost']})."
                            purchase_color = (235, 150, 150)
                        break

                    if prestige_points >= skin['cost']:
                        prestige_points -= skin['cost']
                        unlocked_skin_ids.append(skin['id'])
                        selected_skin_id = skin['id']
                        persist_skin_progress()
                        purchase_message = f"Bought premium skin {skin['name']} for {skin['cost']} prestige!"
                        purchase_color = (235, 215, 140)
                    else:
                        purchase_message = f"Not enough prestige points (need {skin['cost']})."
                        purchase_color = (235, 150, 150)
                    break

                if handled_skin_action:
                    continue

                if prev_page_button.is_hovered(local_mouse_pos):
                    page_index = (page_index - 1) % total_pages
                    continue

                if next_page_button.is_hovered(local_mouse_pos):
                    page_index = (page_index + 1) % total_pages
                    continue

                if back_button.is_hovered(local_mouse_pos):
                    return 'menu', screen, total_coins, prestige_points

            if event.type == pygame.MOUSEMOTION and active_slider is not None and event.buttons[0]:
                rect = slider_rects[active_slider]
                ratio = (local_mouse_pos[0] - rect.x) / max(1, rect.width)
                selected_skin_rgb[active_slider] = max(0, min(255, int(ratio * 255)))
                custom_skin_colors[selected_skin_id] = tuple(selected_skin_rgb)
                purchase_message = f"{selected_skin['name']} RGB updated."
                purchase_color = (140, 235, 170)
                persist_skin_progress()

            if event.type == pygame.MOUSEBUTTONUP:
                active_slider = None

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return 'menu', screen, total_coins, prestige_points

        screen.fill(BG_COLOR)
        if full_screen:
            scale = min(screen_w / WIDTH, screen_h / HEIGHT)
            scaled_surface = pygame.transform.scale(render_surface, (int(WIDTH * scale), int(HEIGHT * scale)))
            screen.blit(scaled_surface, ((screen_w - scaled_surface.get_width()) // 2, (screen_h - scaled_surface.get_height()) // 2))
        else:
            screen.blit(render_surface, ((screen_w - WIDTH) // 2, (screen_h - HEIGHT) // 2))
        pygame.display.flip()
        clock.tick(FPS)

def store_menu(screen, render_surface, total_coins, speed_level, bonus_coin_level, prestige_points, prestige_upgrade_level, back_state='menu'):
    store_offset_y = -40
    left_col_x = WIDTH // 2 - 450
    right_col_x = WIDTH // 2 + 30

    back_button = Button(WIDTH // 2 - 140, HEIGHT // 2 + 340 + store_offset_y, 280, 54, "Back")
    buy_speed_button = Button(left_col_x + 20, HEIGHT // 2 + 10 + store_offset_y, 290, 54, "Upgrade Speed")
    info_speed_button = Button(left_col_x + 320, HEIGHT // 2 + 10 + store_offset_y, 80, 54, "Info")
    buy_bonus_button = Button(left_col_x + 20, HEIGHT // 2 + 220 + store_offset_y, 290, 54, "Upgrade Bonus Coins")
    info_bonus_button = Button(left_col_x + 320, HEIGHT // 2 + 220 + store_offset_y, 80, 54, "Info")
    buy_prestige_button = Button(right_col_x + 20, HEIGHT // 2 + 220 + store_offset_y, 290, 54, "Upgrade Prestige Power")
    info_prestige_button = Button(right_col_x + 320, HEIGHT // 2 + 220 + store_offset_y, 80, 54, "Info")
    clock = pygame.time.Clock()

    gradient_surface = pygame.Surface((WIDTH, HEIGHT))
    top_color = (22, 32, 62)
    bottom_color = (12, 16, 30)
    for y in range(HEIGHT):
        t = y / max(1, HEIGHT - 1)
        color = (
            int(top_color[0] * (1 - t) + bottom_color[0] * t),
            int(top_color[1] * (1 - t) + bottom_color[1] * t),
            int(top_color[2] * (1 - t) + bottom_color[2] * t),
        )
        pygame.draw.line(gradient_surface, color, (0, y), (WIDTH, y))

    card_rect = pygame.Rect(WIDTH // 2 - 500, HEIGHT // 2 - 170 + store_offset_y, 1000, 700)
    speed_section_rect = pygame.Rect(left_col_x, HEIGHT // 2 - 95 + store_offset_y, 420, 190)
    bonus_section_rect = pygame.Rect(left_col_x, HEIGHT // 2 + 115 + store_offset_y, 420, 190)
    prestige_section_rect = pygame.Rect(right_col_x, HEIGHT // 2 - 95 + store_offset_y, 420, 400)
    info_overlay_x = min(WIDTH - 340, card_rect.right + 20)
    info_overlay_rect = pygame.Rect(info_overlay_x, card_rect.top + 110, 320, 230)

    purchase_message = ""
    purchase_color = (180, 185, 220)
    info_color = (180, 205, 235)

    def wrap_text(text, max_width):
        words = text.split()
        lines = []
        current_line = ""
        for word in words:
            test_line = f"{current_line} {word}".strip()
            if small_font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        return lines

    while True:
        render_surface.blit(gradient_surface, (0, 0))

        draw_text(render_surface, "Store", WIDTH // 2 + 2, HEIGHT // 4 + 2, font, (20, 25, 40))
        draw_text(render_surface, "Store", WIDTH // 2, HEIGHT // 4, font, (245, 250, 255))
        draw_text(render_surface, f"Your coins: {total_coins}", WIDTH // 2 - 120, HEIGHT // 4 + 46, small_font, (190, 205, 240))
        draw_text(render_surface, f"Prestige points: {prestige_points}", WIDTH // 2 + 140, HEIGHT // 4 + 46, small_font, (225, 205, 135))

        panel_surface = pygame.Surface((card_rect.width, card_rect.height), pygame.SRCALPHA)
        panel_surface.fill((26, 36, 68, 195))
        render_surface.blit(panel_surface, card_rect.topleft)
        pygame.draw.rect(render_surface, (165, 180, 225), card_rect, 2, border_radius=16)

        pygame.draw.rect(render_surface, (34, 48, 84), speed_section_rect, border_radius=12)
        pygame.draw.rect(render_surface, (130, 150, 205), speed_section_rect, 1, border_radius=12)
        pygame.draw.rect(render_surface, (34, 48, 84), bonus_section_rect, border_radius=12)
        pygame.draw.rect(render_surface, (130, 150, 205), bonus_section_rect, 1, border_radius=12)
        pygame.draw.rect(render_surface, (34, 48, 84), prestige_section_rect, border_radius=12)
        pygame.draw.rect(render_surface, (170, 150, 95), prestige_section_rect, 1, border_radius=12)

        draw_text(render_surface, "Coin Upgrades", left_col_x + 210, HEIGHT // 2 - 130 + store_offset_y, small_font, (245, 250, 255))
        draw_text(render_surface, "Speed Upgrade", left_col_x + 210, HEIGHT // 2 - 70 + store_offset_y, small_font, (245, 250, 255))
        draw_text(
            render_surface,
            f"Level: {speed_level}/{len(SPEED_UPGRADE_COSTS)}   |   Move Speed: {BASE_PLAYER_SPEED + speed_level}",
            left_col_x + 210,
            HEIGHT // 2 - 45 + store_offset_y,
            small_font,
            (190, 205, 240),
        )

        if speed_level < len(SPEED_UPGRADE_COSTS):
            next_cost = SPEED_UPGRADE_COSTS[speed_level]
            buy_speed_button.text = f"Upgrade Speed ({next_cost} coins)"
            draw_text(render_surface, f"Next speed cost: {next_cost}", left_col_x + 210, HEIGHT // 2 - 20 + store_offset_y, small_font, (180, 185, 220))
        else:
            buy_speed_button.text = "Max Speed Reached"
            draw_text(render_surface, "You unlocked all speed upgrades.", left_col_x + 210, HEIGHT // 2 - 20 + store_offset_y, small_font, (180, 185, 220))

        draw_text(render_surface, "Bonus Coins Upgrade", left_col_x + 210, HEIGHT // 2 + 140 + store_offset_y, small_font, (245, 250, 255))
        draw_text(
            render_surface,
            f"Level: {bonus_coin_level}/{len(BONUS_COIN_UPGRADE_COSTS)}   |   Coins per pickup: {1 + bonus_coin_level}",
            left_col_x + 210,
            HEIGHT // 2 + 165 + store_offset_y,
            small_font,
            (190, 205, 240),
        )

        if bonus_coin_level < len(BONUS_COIN_UPGRADE_COSTS):
            next_bonus_cost = BONUS_COIN_UPGRADE_COSTS[bonus_coin_level]
            buy_bonus_button.text = f"Upgrade Bonus Coins ({next_bonus_cost} coins)"
            draw_text(render_surface, f"Next bonus cost: {next_bonus_cost}", left_col_x + 210, HEIGHT // 2 + 190 + store_offset_y, small_font, (180, 185, 220))
        else:
            buy_bonus_button.text = "Max Bonus Reached"
            draw_text(render_surface, "You unlocked all bonus upgrades.", left_col_x + 210, HEIGHT // 2 + 190 + store_offset_y, small_font, (180, 185, 220))

        draw_text(render_surface, "Prestige Upgrades", right_col_x + 210, HEIGHT // 2 - 130 + store_offset_y, small_font, (245, 235, 200))
        draw_text(render_surface, "Prestige Power", right_col_x + 210, HEIGHT // 2 - 70 + store_offset_y, small_font, (245, 235, 200))
        draw_text(
            render_surface,
            f"Level: {prestige_upgrade_level}/{len(PRESTIGE_UPGRADE_COSTS)}   |   End-level coin bonus: +{prestige_upgrade_level * 10}%",
            right_col_x + 210,
            HEIGHT // 2 - 45 + store_offset_y,
            small_font,
            (225, 210, 165),
        )
        if prestige_upgrade_level < len(PRESTIGE_UPGRADE_COSTS):
            next_prestige_cost = PRESTIGE_UPGRADE_COSTS[prestige_upgrade_level]
            buy_prestige_button.text = f"Upgrade Prestige Power ({next_prestige_cost} PP)"
            draw_text(render_surface, f"Next prestige cost: {next_prestige_cost} PP", right_col_x + 210, HEIGHT // 2 - 20 + store_offset_y, small_font, (210, 195, 150))
        else:
            buy_prestige_button.text = "Max Prestige Power"
            draw_text(render_surface, "You unlocked all prestige power levels.", right_col_x + 210, HEIGHT // 2 - 20 + store_offset_y, small_font, (210, 195, 150))

        draw_text(render_surface, purchase_message, WIDTH // 2, HEIGHT // 2 + 362 + store_offset_y, small_font, purchase_color)

        mouse_pos = pygame.mouse.get_pos()
        screen_w, screen_h = screen.get_size()
        if full_screen:
            scale = min(screen_w / WIDTH, screen_h / HEIGHT)
            offset_x = (screen_w - int(WIDTH * scale)) // 2
            offset_y = (screen_h - int(HEIGHT * scale)) // 2
            local_mouse_pos = ((mouse_pos[0] - offset_x) / scale, (mouse_pos[1] - offset_y) / scale) if scale > 0 else mouse_pos
        else:
            offset_x = (screen_w - WIDTH) // 2
            offset_y = (screen_h - HEIGHT) // 2
            local_mouse_pos = (mouse_pos[0] - offset_x, mouse_pos[1] - offset_y)

        buy_speed_button.color = BUTTON_HOVER if buy_speed_button.is_hovered(local_mouse_pos) else BUTTON_COLOR
        info_speed_button.color = BUTTON_HOVER if info_speed_button.is_hovered(local_mouse_pos) else BUTTON_COLOR
        buy_bonus_button.color = BUTTON_HOVER if buy_bonus_button.is_hovered(local_mouse_pos) else BUTTON_COLOR
        info_bonus_button.color = BUTTON_HOVER if info_bonus_button.is_hovered(local_mouse_pos) else BUTTON_COLOR
        buy_prestige_button.color = BUTTON_HOVER if buy_prestige_button.is_hovered(local_mouse_pos) else BUTTON_COLOR
        info_prestige_button.color = BUTTON_HOVER if info_prestige_button.is_hovered(local_mouse_pos) else BUTTON_COLOR
        back_button.color = BUTTON_HOVER if back_button.is_hovered(local_mouse_pos) else BUTTON_COLOR
        buy_speed_button.draw(render_surface)
        info_speed_button.draw(render_surface)
        buy_bonus_button.draw(render_surface)
        info_bonus_button.draw(render_surface)
        buy_prestige_button.draw(render_surface)
        info_prestige_button.draw(render_surface)
        back_button.draw(render_surface)

        # Hover info overlay (side panel)
        hover_info_title = None
        hover_info_text = None
        if info_speed_button.is_hovered(local_mouse_pos):
            hover_info_title = "Speed Upgrade"
            if speed_level < len(SPEED_UPGRADE_COSTS):
                next_speed = BASE_PLAYER_SPEED + speed_level + 1
                hover_info_text = f"Increases movement speed. Current speed is {BASE_PLAYER_SPEED + speed_level}. Next level raises it to {next_speed}."
            else:
                hover_info_text = "Increases movement speed. You are already at maximum level."
        elif info_bonus_button.is_hovered(local_mouse_pos):
            hover_info_title = "Bonus Coins Upgrade"
            if bonus_coin_level < len(BONUS_COIN_UPGRADE_COSTS):
                next_pickup = 1 + bonus_coin_level + 1
                hover_info_text = f"Each collected maze coin adds more wallet coins. Current value is {1 + bonus_coin_level} per coin. Next level gives {next_pickup} per coin."
            else:
                hover_info_text = "Each collected maze coin adds more wallet coins. You are already at maximum level."
        elif info_prestige_button.is_hovered(local_mouse_pos):
            hover_info_title = "Prestige Power"
            if prestige_upgrade_level < len(PRESTIGE_UPGRADE_COSTS):
                next_percent = (prestige_upgrade_level + 1) * 10
                hover_info_text = f"Prestige-only upgrade. Adds an end-level coin bonus multiplier. Current bonus is +{prestige_upgrade_level * 10}%. Next level raises it to +{next_percent}%."
            else:
                hover_info_text = "Prestige-only upgrade. Adds end-level coin bonus. You are already at maximum level."

        if hover_info_text:
            overlay_surface = pygame.Surface((info_overlay_rect.width, info_overlay_rect.height), pygame.SRCALPHA)
            overlay_surface.fill((20, 34, 62, 238))
            render_surface.blit(overlay_surface, info_overlay_rect.topleft)
            pygame.draw.rect(render_surface, (150, 175, 230), info_overlay_rect, 2, border_radius=10)

            draw_text(render_surface, hover_info_title, info_overlay_rect.centerx, info_overlay_rect.top + 24, small_font, (240, 245, 255))
            info_lines = wrap_text(hover_info_text, info_overlay_rect.width - 24)
            line_height = small_font.get_height() + 3
            y_line = info_overlay_rect.top + 56
            for line in info_lines[:6]:
                draw_text(render_surface, line, info_overlay_rect.centerx, y_line, small_font, info_color)
                y_line += line_height

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit', screen, total_coins, speed_level, bonus_coin_level, prestige_points, prestige_upgrade_level
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buy_speed_button.is_hovered(local_mouse_pos):
                    if speed_level >= len(SPEED_UPGRADE_COSTS):
                        purchase_message = "Speed is already maxed out."
                        purchase_color = (180, 185, 220)
                    else:
                        cost = SPEED_UPGRADE_COSTS[speed_level]
                        if total_coins >= cost:
                            total_coins -= cost
                            speed_level += 1
                            purchase_message = f"Speed upgraded to level {speed_level}!"
                            purchase_color = (140, 235, 170)
                        else:
                            purchase_message = f"Not enough coins (need {cost})."
                            purchase_color = (235, 150, 150)
                if buy_bonus_button.is_hovered(local_mouse_pos):
                    if bonus_coin_level >= len(BONUS_COIN_UPGRADE_COSTS):
                        purchase_message = "Bonus coins is already maxed out."
                        purchase_color = (180, 185, 220)
                    else:
                        cost = BONUS_COIN_UPGRADE_COSTS[bonus_coin_level]
                        if total_coins >= cost:
                            total_coins -= cost
                            bonus_coin_level += 1
                            purchase_message = f"Bonus coins upgraded to level {bonus_coin_level}!"
                            purchase_color = (140, 235, 170)
                        else:
                            purchase_message = f"Not enough coins (need {cost})."
                            purchase_color = (235, 150, 150)
                if buy_prestige_button.is_hovered(local_mouse_pos):
                    if prestige_upgrade_level >= len(PRESTIGE_UPGRADE_COSTS):
                        purchase_message = "Prestige power is already maxed out."
                        purchase_color = (180, 185, 220)
                    else:
                        prestige_cost = PRESTIGE_UPGRADE_COSTS[prestige_upgrade_level]
                        if prestige_points >= prestige_cost:
                            prestige_points -= prestige_cost
                            prestige_upgrade_level += 1
                            purchase_message = f"Prestige power upgraded to level {prestige_upgrade_level}!"
                            purchase_color = (235, 215, 140)
                        else:
                            purchase_message = f"Not enough prestige points (need {prestige_cost} PP)."
                            purchase_color = (235, 150, 150)
                if back_button.is_hovered(local_mouse_pos):
                    return back_state, screen, total_coins, speed_level, bonus_coin_level, prestige_points, prestige_upgrade_level
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return back_state, screen, total_coins, speed_level, bonus_coin_level, prestige_points, prestige_upgrade_level

        screen.fill(BG_COLOR)
        if full_screen:
            scale = min(screen_w / WIDTH, screen_h / HEIGHT)
            scaled_surface = pygame.transform.scale(render_surface, (int(WIDTH * scale), int(HEIGHT * scale)))
            screen.blit(scaled_surface, ((screen_w - scaled_surface.get_width()) // 2, (screen_h - scaled_surface.get_height()) // 2))
        else:
            screen.blit(render_surface, ((screen_w - WIDTH) // 2, (screen_h - HEIGHT) // 2))
        pygame.display.flip()
        clock.tick(FPS)

def level_complete_menu(screen, render_surface, level, total_coins, collected, speed_level, bonus_coin_level, prestige_points, prestige_upgrade_level):
    next_button = Button(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50, "Next Level")
    store_button = Button(WIDTH // 2 - 100, HEIGHT // 2, 200, 50, "Store")
    menu_button = Button(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50, "Main Menu")
    quit_button = Button(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 50, "Quit")
    clock = pygame.time.Clock()

    next_level = level + 1

    while True:
        render_surface.fill(BG_COLOR)
        draw_text(render_surface, f"Level {level} Complete!", WIDTH // 2, 50, font)
        draw_text(render_surface, f"Coins collected: {collected}", WIDTH // 2, 120, small_font)
        draw_text(render_surface, f"Total coins: {total_coins}", WIDTH // 2, 150, small_font)
        
        mouse_pos = pygame.mouse.get_pos()
        screen_w, screen_h = screen.get_size()
        if full_screen:
            scale = min(screen_w / WIDTH, screen_h / HEIGHT)
            offset_x = (screen_w - int(WIDTH * scale)) // 2
            offset_y = (screen_h - int(HEIGHT * scale)) // 2
            local_mouse_pos = ((mouse_pos[0] - offset_x) / scale, (mouse_pos[1] - offset_y) / scale) if scale > 0 else mouse_pos
        else:
            offset_x = (screen_w - WIDTH) // 2
            offset_y = (screen_h - HEIGHT) // 2
            local_mouse_pos = (mouse_pos[0] - offset_x, mouse_pos[1] - offset_y)

        for button in [next_button, store_button, menu_button, quit_button]:
            button.color = BUTTON_HOVER if button.is_hovered(local_mouse_pos) else BUTTON_COLOR
            button.draw(render_surface)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_progress(next_level, total_coins, speed_level, bonus_coin_level, prestige_points=prestige_points, prestige_upgrade_level=prestige_upgrade_level)
                return 'quit', screen, next_level, total_coins, speed_level, bonus_coin_level, prestige_points, prestige_upgrade_level
            if event.type == pygame.MOUSEBUTTONDOWN:
                if next_button.is_hovered(local_mouse_pos):
                    save_progress(next_level, total_coins, speed_level, bonus_coin_level, prestige_points=prestige_points, prestige_upgrade_level=prestige_upgrade_level)
                    return 'next_level', screen, next_level, total_coins, speed_level, bonus_coin_level, prestige_points, prestige_upgrade_level
                elif store_button.is_hovered(local_mouse_pos):
                    store_state, screen, total_coins, speed_level, bonus_coin_level, prestige_points, prestige_upgrade_level = store_menu(
                        screen,
                        render_surface,
                        total_coins,
                        speed_level,
                        bonus_coin_level,
                        prestige_points,
                        prestige_upgrade_level,
                        back_state='level_complete',
                    )
                    if store_state == 'quit':
                        save_progress(next_level, total_coins, speed_level, bonus_coin_level, prestige_points=prestige_points, prestige_upgrade_level=prestige_upgrade_level)
                        return 'quit', screen, next_level, total_coins, speed_level, bonus_coin_level, prestige_points, prestige_upgrade_level
                elif menu_button.is_hovered(local_mouse_pos):
                    save_progress(next_level, total_coins, speed_level, bonus_coin_level, prestige_points=prestige_points, prestige_upgrade_level=prestige_upgrade_level)
                    return 'menu', screen, next_level, total_coins, speed_level, bonus_coin_level, prestige_points, prestige_upgrade_level
                elif quit_button.is_hovered(local_mouse_pos):
                    save_progress(next_level, total_coins, speed_level, bonus_coin_level, prestige_points=prestige_points, prestige_upgrade_level=prestige_upgrade_level)
                    return 'quit', screen, next_level, total_coins, speed_level, bonus_coin_level, prestige_points, prestige_upgrade_level

        screen.fill(BG_COLOR)
        screen_w, screen_h = screen.get_size()
        if full_screen:
            scale = min(screen_w / WIDTH, screen_h / HEIGHT)
            scaled_surface = pygame.transform.scale(render_surface, (int(WIDTH * scale), int(HEIGHT * scale)))
            scaled_width = scaled_surface.get_width()
            scaled_height = scaled_surface.get_height()
            offset_x = (screen_w - scaled_width) // 2
            offset_y = (screen_h - scaled_height) // 2
            screen.blit(scaled_surface, (offset_x, offset_y))
        else:
            offset_x = (screen_w - WIDTH) // 2
            offset_y = (screen_h - HEIGHT) // 2
            screen.blit(render_surface, (offset_x, offset_y))
        pygame.display.flip()
        clock.tick(FPS)

def pause_menu(screen, render_surface, total_coins, speed_level, bonus_coin_level, prestige_points, prestige_upgrade_level):
    main_menu_button = Button(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50, "Main Menu")
    store_button = Button(WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 50, "Store")
    quit_button = Button(WIDTH // 2 - 100, HEIGHT // 2 + 90, 200, 50, "Quit")
    clock = pygame.time.Clock()
    paused_frame = render_surface.copy()
    popup_rect = pygame.Rect(WIDTH // 2 - 220, HEIGHT // 2 - 170, 440, 360)

    while True:
        render_surface.blit(paused_frame, (0, 0))
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        render_surface.blit(overlay, (0, 0))

        pygame.draw.rect(render_surface, (40, 55, 95), popup_rect)
        pygame.draw.rect(render_surface, (180, 190, 220), popup_rect, 2)
        draw_text(render_surface, "Paused", WIDTH // 2, HEIGHT // 2 - 120, font)

        mouse_pos = pygame.mouse.get_pos()
        screen_w, screen_h = screen.get_size()
        if full_screen:
            scale = min(screen_w / WIDTH, screen_h / HEIGHT)
            offset_x = (screen_w - int(WIDTH * scale)) // 2
            offset_y = (screen_h - int(HEIGHT * scale)) // 2
            local_mouse_pos = ((mouse_pos[0] - offset_x) / scale, (mouse_pos[1] - offset_y) / scale) if scale > 0 else mouse_pos
        else:
            offset_x = (screen_w - WIDTH) // 2
            offset_y = (screen_h - HEIGHT) // 2
            local_mouse_pos = (mouse_pos[0] - offset_x, mouse_pos[1] - offset_y)

        for button in [main_menu_button, store_button, quit_button]:
            button.color = BUTTON_HOVER if button.is_hovered(local_mouse_pos) else BUTTON_COLOR
            button.draw(render_surface)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit', screen, total_coins, speed_level, bonus_coin_level, prestige_points, prestige_upgrade_level
            if event.type == pygame.MOUSEBUTTONDOWN:
                if main_menu_button.is_hovered(local_mouse_pos):
                    return 'menu', screen, total_coins, speed_level, bonus_coin_level, prestige_points, prestige_upgrade_level
                if store_button.is_hovered(local_mouse_pos):
                    store_state, screen, total_coins, speed_level, bonus_coin_level, prestige_points, prestige_upgrade_level = store_menu(
                        screen,
                        render_surface,
                        total_coins,
                        speed_level,
                        bonus_coin_level,
                        prestige_points,
                        prestige_upgrade_level,
                        back_state='pause',
                    )
                    if store_state == 'quit':
                        return 'quit', screen, total_coins, speed_level, bonus_coin_level, prestige_points, prestige_upgrade_level
                if quit_button.is_hovered(local_mouse_pos):
                    return 'quit', screen, total_coins, speed_level, bonus_coin_level, prestige_points, prestige_upgrade_level
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'menu', screen, total_coins, speed_level, bonus_coin_level, prestige_points, prestige_upgrade_level

        screen.fill(BG_COLOR)
        if full_screen:
            scale = min(screen_w / WIDTH, screen_h / HEIGHT)
            scaled_surface = pygame.transform.scale(render_surface, (int(WIDTH * scale), int(HEIGHT * scale)))
            scaled_width = scaled_surface.get_width()
            scaled_height = scaled_surface.get_height()
            offset_x = (screen_w - scaled_width) // 2
            offset_y = (screen_h - scaled_height) // 2
            screen.blit(scaled_surface, (offset_x, offset_y))
        else:
            offset_x = (screen_w - WIDTH) // 2
            offset_y = (screen_h - HEIGHT) // 2
            screen.blit(render_surface, (offset_x, offset_y))
        pygame.display.flip()
        clock.tick(FPS)

def game_loop(screen, render_surface, start_level, total_coins, speed_level, bonus_coin_level, prestige_points, prestige_upgrade_level):
    level = start_level
    while True:
        grid_w = min(MAX_GRID_WIDTH, BASE_GRID_WIDTH + (level - 1) * GRID_STEP)
        grid_h = min(MAX_GRID_HEIGHT, BASE_GRID_HEIGHT + (level - 1) * GRID_STEP)
        # ensure odd sizes for maze DFS paths
        if grid_w % 2 == 0:
            grid_w -= 1
        if grid_h % 2 == 0:
            grid_h -= 1

        selected_skin_id, _ = load_skin_state()
        maze = Maze(grid_w, grid_h, level, speed_level, selected_skin_id)
        mid_save = load_mid_game(level)
        if mid_save:
            maze.restore_from_save(mid_save)
            total_coins = mid_save['total_coins']
            speed_level = mid_save.get('speed_level', speed_level)
            bonus_coin_level = mid_save.get('bonus_coin_level', bonus_coin_level)
            prestige_points = mid_save.get('prestige_points', prestige_points)
            prestige_upgrade_level = mid_save.get('prestige_upgrade_level', prestige_upgrade_level)
            maze.speed = BASE_PLAYER_SPEED + speed_level
        scale = min(WIDTH / (grid_w * CELL_SIZE), HEIGHT / (grid_h * CELL_SIZE))
        scale = min(scale, 1.0)  # don't scale up, only down
        clock = pygame.time.Clock()

        while True:
            render_surface.fill(BG_COLOR)
            maze.draw(render_surface, scale=scale)
            draw_text(render_surface, f"Level {level}", WIDTH // 2, 30, small_font)

            # HUD coin line: wallet + currently picked-up coins (highlighted)
            wallet_text = f"Coin Wallet: {total_coins} + "
            picked_text = f"{maze.collected_coins}"
            wallet_surf = small_font.render(wallet_text, True, TEXT_COLOR)
            picked_surf = small_font.render(picked_text, True, COIN_COLOR)
            total_width = wallet_surf.get_width() + picked_surf.get_width()
            start_x = WIDTH // 2 - total_width // 2
            y = 60
            render_surface.blit(wallet_surf, (start_x, y))
            render_surface.blit(picked_surf, (start_x + wallet_surf.get_width(), y))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save_progress(level, total_coins, speed_level, bonus_coin_level, prestige_points=prestige_points, prestige_upgrade_level=prestige_upgrade_level)
                    save_mid_game(maze, level, total_coins, speed_level, bonus_coin_level, prestige_points, prestige_upgrade_level)
                    return 'quit', screen, level, total_coins, 0, speed_level, bonus_coin_level, prestige_points, prestige_upgrade_level
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        global full_screen, display_mode
                        display_mode = 'windowed' if display_mode != 'windowed' else 'fullscreen'
                        screen = apply_display_mode()
                        save_settings()
                        pygame.time.wait(200)
                    elif event.key == pygame.K_ESCAPE:
                        action, screen, total_coins, speed_level, bonus_coin_level, prestige_points, prestige_upgrade_level = pause_menu(
                            screen,
                            render_surface,
                            total_coins,
                            speed_level,
                            bonus_coin_level,
                            prestige_points,
                            prestige_upgrade_level,
                        )
                        maze.speed = BASE_PLAYER_SPEED + speed_level
                        if action == 'menu':
                            save_progress(level, total_coins, speed_level, bonus_coin_level, prestige_points=prestige_points, prestige_upgrade_level=prestige_upgrade_level)
                            save_mid_game(maze, level, total_coins, speed_level, bonus_coin_level, prestige_points, prestige_upgrade_level)
                            return 'menu', screen, level, total_coins, 0, speed_level, bonus_coin_level, prestige_points, prestige_upgrade_level
                        if action == 'quit':
                            save_progress(level, total_coins, speed_level, bonus_coin_level, prestige_points=prestige_points, prestige_upgrade_level=prestige_upgrade_level)
                            save_mid_game(maze, level, total_coins, speed_level, bonus_coin_level, prestige_points, prestige_upgrade_level)
                            return 'quit', screen, level, total_coins, 0, speed_level, bonus_coin_level, prestige_points, prestige_upgrade_level

            keys = pygame.key.get_pressed()
            maze.move_player(keys)

            if maze.check_win():
                clear_mid_save()
                earned_coins = maze.collected_coins * (1 + bonus_coin_level)
                earned_coins = int(earned_coins * (1 + 0.10 * prestige_upgrade_level))
                total_coins += earned_coins
                return 'level_complete', screen, level, total_coins, maze.collected_coins, speed_level, bonus_coin_level, prestige_points, prestige_upgrade_level

            screen.fill(BG_COLOR)
            screen_w, screen_h = screen.get_size()
            if full_screen:
                scale = min(screen_w / WIDTH, screen_h / HEIGHT)
                scaled_surface = pygame.transform.scale(render_surface, (int(WIDTH * scale), int(HEIGHT * scale)))
                scaled_width = scaled_surface.get_width()
                scaled_height = scaled_surface.get_height()
                offset_x = (screen_w - scaled_width) // 2
                offset_y = (screen_h - scaled_height) // 2
                screen.blit(scaled_surface, (offset_x, offset_y))
            else:
                offset_x = (screen_w - WIDTH) // 2
                offset_y = (screen_h - HEIGHT) // 2
                screen.blit(render_surface, (offset_x, offset_y))
            pygame.display.flip()
            clock.tick(FPS)

def main():
    load_settings()
    screen = apply_display_mode()
    pygame.display.set_caption("Square Game")
    render_surface = pygame.Surface((WIDTH, HEIGHT))

    current_level, total_coins = load_progress()
    speed_level = load_speed_level()
    bonus_coin_level = load_bonus_coin_level()
    prestige_points = load_prestige_points()
    prestige_upgrade_level = load_prestige_upgrade_level()
    collected = 0

    state = 'menu'
    while state != 'quit':
        if render_surface.get_size() != (WIDTH, HEIGHT):
            render_surface = pygame.Surface((WIDTH, HEIGHT))

        if state == 'menu':
            state, screen = main_menu(screen, render_surface)
        elif state == 'settings':
            state, screen = settings_menu(screen, render_surface)
        elif state == 'start':
            state, screen, current_level, total_coins, collected, speed_level, bonus_coin_level, prestige_points, prestige_upgrade_level = game_loop(
                screen,
                render_surface,
                current_level,
                total_coins,
                speed_level,
                bonus_coin_level,
                prestige_points,
                prestige_upgrade_level,
            )
        elif state == 'level_complete':
            state, screen, current_level, total_coins, speed_level, bonus_coin_level, prestige_points, prestige_upgrade_level = level_complete_menu(
                screen,
                render_surface,
                current_level,
                total_coins,
                collected,
                speed_level,
                bonus_coin_level,
                prestige_points,
                prestige_upgrade_level,
            )
        elif state == 'next_level':
            state = 'start'
        elif state == 'store':
            state, screen, total_coins, speed_level, bonus_coin_level, prestige_points, prestige_upgrade_level = store_menu(
                screen,
                render_surface,
                total_coins,
                speed_level,
                bonus_coin_level,
                prestige_points,
                prestige_upgrade_level,
            )
        elif state == 'customization':
            state, screen, total_coins, prestige_points = customization_menu(
                screen,
                render_surface,
                current_level,
                total_coins,
                prestige_points,
            )
        elif state == 'reset':
            previous_level, _ = load_progress()
            previous_speed_level = load_speed_level()
            previous_bonus_level = load_bonus_coin_level()
            previous_reset_count = load_reset_count()
            previous_prestige_points = load_prestige_points()

            prestige_reward = calculate_prestige_reward(previous_level, previous_speed_level, previous_bonus_level)

            current_level = 1
            total_coins = 0
            speed_level = 0
            bonus_coin_level = 0
            prestige_upgrade_level = 0
            prestige_points = previous_prestige_points + prestige_reward
            save_progress(
                current_level,
                total_coins,
                speed_level,
                bonus_coin_level,
                previous_reset_count + 1,
                prestige_points,
                prestige_upgrade_level,
            )
            clear_mid_save()
            state = 'menu'

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()