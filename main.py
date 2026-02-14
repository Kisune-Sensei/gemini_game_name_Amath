import ctypes
try:
    ctypes.windll.user32.SetProcessDPIAware()
except AttributeError:
    pass

import pygame
import sys
import random
import source.settings as settings
from source.settings import *
from source.sprites import Tile
from source.logic import validate_move
import source.sound_manager as audio
import source.ui_manager as ui
from source.ai_player import bot 

# --- Initialization ---
pygame.init()
audio.init_sounds()
ui.init_ui()
audio.play_music("MENU")

if settings.IS_FULLSCREEN:
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    w, h = screen.get_size()
    settings.set_resolution(w, h)
else:
    screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
    settings.set_resolution(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)

ui.init_ui()

pygame.display.set_caption("A-Math Simulator")
clock = pygame.time.Clock()

# --- Global Variables ---
grid_logic = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
board_tiles = []
p1_score = 0
p2_score = 0
turn = 1
message = "Place tiles to form an equation"
game_state = "MENU"
previous_state = "MENU"
has_rerolled = False
consecutive_skips = 0

IS_SINGLE_PLAYER = False 

tile_bag = settings.FULL_TILE_SET.copy()
random.shuffle(tile_bag)

resolutions = [(1000, 800), (1280, 720), (1600, 900), (1920, 1080)]
current_res_idx = 0

temp_music_volume = audio.current_music_volume
temp_sfx_volume = audio.current_sfx_volume
temp_res_idx = current_res_idx
temp_fullscreen = settings.IS_FULLSCREEN

dropdown_active = False    
fullscreen_active = False  
dragging_music_slider = False
dragging_sfx_slider = False

# --- Helper Functions ---

def reorganize_hand(current_hand):
    tile_spacing = settings.CELL_SIZE + int(5 * settings.UI_SCALE)
    total_width = len(current_hand) * tile_spacing
    start_x = (settings.SCREEN_WIDTH - total_width) // 2
    y_pos = settings.SCREEN_HEIGHT - (settings.CELL_SIZE + int(50 * settings.UI_SCALE))
    
    for i, t in enumerate(current_hand):
        t.rect.x = start_x + (i * tile_spacing)
        t.rect.y = y_pos
        t.orig_pos = (t.rect.x, t.rect.y)

def draw_tiles(current_hand):
    needed = 8 - len(current_hand)
    if needed <= 0 or not tile_bag:
        return

    num_count = sum(1 for t in current_hand if t.value.isdigit())
    op_count = sum(1 for t in current_hand if t.value in ['+', '-', '*', '/'])
    eq_count = sum(1 for t in current_hand if t.value == '=')

    need_num = max(0, 5 - num_count)
    need_op  = max(0, 2 - op_count)
    need_eq  = max(0, 1 - eq_count)

    new_vals = []

    def draw_specific(target_type):
        random.shuffle(tile_bag)
        for i, val in enumerate(tile_bag):
            is_num = val.isdigit()
            is_op = val in ['+', '-', '*', '/']
            is_eq = val == '='
            
            if (target_type == 'num' and is_num) or \
               (target_type == 'op' and is_op) or \
               (target_type == 'eq' and is_eq):
                return tile_bag.pop(i) 
        return None 

    for _ in range(need_num):
        if len(new_vals) < needed:
            val = draw_specific('num')
            if val: new_vals.append(val)

    for _ in range(need_op):
        if len(new_vals) < needed:
            val = draw_specific('op')
            if val: new_vals.append(val)

    for _ in range(need_eq):
        if len(new_vals) < needed:
            val = draw_specific('eq')
            if val: new_vals.append(val)

    while len(new_vals) < needed and tile_bag:
        random.shuffle(tile_bag)
        new_vals.append(tile_bag.pop())

    for val in new_vals:
        t = Tile(val, 0, 0)
        current_hand.append(t)
        
    reorganize_hand(current_hand)

def is_hand_playable(hand_tiles):
    values = [t.value for t in hand_tiles]
    num_count = sum(1 for v in values if v.isdigit())
    op_count = sum(1 for v in values if v in ['+', '-', '*', '/'])
    eq_count = sum(1 for v in values if v == '=')
    
    if len(hand_tiles) == 8:
        return num_count >= 5 and op_count >= 2 and eq_count >= 1
        
    return eq_count >= 1 and op_count >= 1 and num_count >= 3

def draw_initial_hand(current_hand):
    attempts = 0
    max_attempts = 100
    
    while True:
        draw_tiles(current_hand) 
        
        if len(current_hand) < 8 and not tile_bag: break 
        
        if is_hand_playable(current_hand):
            break
            
        attempts += 1
        if attempts > max_attempts:
            break
            
        for t in current_hand: tile_bag.append(t.value)
        current_hand.clear()
        random.shuffle(tile_bag)

player1_hand = []
player2_hand = []
draw_initial_hand(player1_hand)
draw_initial_hand(player2_hand)
selected_tile = None

def reset_game():
    global p1_score, p2_score, turn, message, grid_logic, board_tiles, player1_hand, player2_hand, selected_tile, tile_bag, has_rerolled, consecutive_skips
    p1_score = 0; p2_score = 0; turn = 1
    has_rerolled = False
    consecutive_skips = 0
    message = "Game Restarted!"
    grid_logic = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    board_tiles = []
    tile_bag = settings.FULL_TILE_SET.copy()
    random.shuffle(tile_bag)
    player1_hand = []; player2_hand = []
    draw_initial_hand(player1_hand)
    draw_initial_hand(player2_hand)
    selected_tile = None

def apply_settings():
    global current_res_idx, screen, player1_hand, player2_hand
    audio.set_music_volume(temp_music_volume)
    audio.set_sfx_volume(temp_sfx_volume)
    
    res_changed = (temp_res_idx != current_res_idx)
    mode_changed = (temp_fullscreen != settings.IS_FULLSCREEN)
    
    if res_changed or mode_changed:
        current_res_idx = temp_res_idx
        settings.IS_FULLSCREEN = temp_fullscreen 
        
        if settings.IS_FULLSCREEN:
            w, h = 0, 0
            flags = pygame.FULLSCREEN
        else:
            w, h = resolutions[current_res_idx]
            flags = 0
            
        screen = pygame.display.set_mode((w, h), flags)
        
        final_w, final_h = screen.get_size()
        settings.set_resolution(final_w, final_h)
        ui.init_ui()
        
        all_tiles = player1_hand + player2_hand + board_tiles
        for t in all_tiles:
            t.update_size() 
            if t.on_board and t.grid_pos:
                r, c = t.grid_pos
                t.rect.x = c * settings.CELL_SIZE + settings.BOARD_OFFSET_X + 1
                t.rect.y = r * settings.CELL_SIZE + settings.BOARD_OFFSET_Y + 1
        
        reorganize_hand(player1_hand)
        reorganize_hand(player2_hand)

def snap_to_grid(tile):
    rel_x = tile.rect.centerx - settings.BOARD_OFFSET_X
    rel_y = tile.rect.centery - settings.BOARD_OFFSET_Y
    gx, gy = rel_x // settings.CELL_SIZE, rel_y // settings.CELL_SIZE
    
    if 0 <= gx < GRID_SIZE and 0 <= gy < GRID_SIZE and grid_logic[gy][gx] is None:
        tile.rect.x = gx * settings.CELL_SIZE + settings.BOARD_OFFSET_X + 1
        tile.rect.y = gy * settings.CELL_SIZE + settings.BOARD_OFFSET_Y + 1
        tile.on_board = True; tile.grid_pos = (gy, gx)
    else:
        tile.rect.topleft = tile.orig_pos; tile.on_board = False; tile.grid_pos = None

def draw_board_background():
    board_rect = pygame.Rect(settings.BOARD_OFFSET_X, settings.BOARD_OFFSET_Y, settings.BOARD_PIXEL_SIZE, settings.BOARD_PIXEL_SIZE)
    pygame.draw.rect(screen, GREEN, board_rect)
    
    font_size = max(8, int(settings.CELL_SIZE * 0.25))
    cell_font = pygame.font.SysFont("arial", font_size, bold=True) 

    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            rect = pygame.Rect(settings.BOARD_OFFSET_X + c*settings.CELL_SIZE, settings.BOARD_OFFSET_Y + r*settings.CELL_SIZE, settings.CELL_SIZE, settings.CELL_SIZE)
            color = None; text = ""; text_color = BLACK
            if (r,c) in TRIPLE_EQ: color = RED; text = "3x EQ"; text_color = WHITE
            elif (r,c) in DOUBLE_EQ: color = YELLOW; text = "2x EQ"
            elif (r,c) in TRIPLE_PIECE: color = BLUE; text = "3x No"; text_color = WHITE
            elif (r,c) in DOUBLE_PIECE: color = ORANGE; text = "2x No"
            
            if color:
                pygame.draw.rect(screen, color, rect)
                t_s = cell_font.render(text, True, text_color)
                screen.blit(t_s, t_s.get_rect(center=rect.center))
            pygame.draw.rect(screen, (0,50,0), rect, 1)

    c_r = pygame.Rect(settings.BOARD_OFFSET_X + 7*settings.CELL_SIZE, settings.BOARD_OFFSET_Y + 7*settings.CELL_SIZE, settings.CELL_SIZE, settings.CELL_SIZE)
    pygame.draw.rect(screen, (255, 150, 150), c_r, 2)
    s_s = cell_font.render("STAR", True, BLACK)
    screen.blit(s_s, s_s.get_rect(center=c_r.center))

def check_game_over(current_hand):
    global game_state
    if len(tile_bag) == 0 and len(current_hand) == 0:
        game_state = "GAME_OVER"
        return True
    if consecutive_skips >= 6:
        game_state = "GAME_OVER"
        return True
    total_slots = GRID_SIZE * GRID_SIZE
    if len(board_tiles) >= total_slots:
        game_state = "GAME_OVER"
        return True
    return False

# --- Main Game Loop ---
running = True
while running:
    if game_state == "MENU":
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if ui.start_btn_rect.collidepoint(event.pos): 
                    audio.play_click(); game_state = "MODE_SELECT" 
                elif ui.setting_btn_rect.collidepoint(event.pos): 
                    audio.play_click(); previous_state="MENU"
                    temp_music_volume=audio.current_music_volume
                    temp_sfx_volume=audio.current_sfx_volume
                    temp_res_idx=current_res_idx
                    temp_fullscreen = settings.IS_FULLSCREEN
                    game_state="SETTINGS"
                elif ui.exit_btn_rect.collidepoint(event.pos): 
                    audio.play_click(); running = False
        ui.draw_menu(screen)

    elif game_state == "MODE_SELECT":
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if ui.single_player_btn_rect.collidepoint(event.pos):
                    audio.play_click(); IS_SINGLE_PLAYER = True; audio.play_music("GAME"); reset_game(); game_state = "GAME"
                elif ui.multi_player_btn_rect.collidepoint(event.pos):
                    audio.play_click(); IS_SINGLE_PLAYER = False; audio.play_music("GAME"); reset_game(); game_state = "GAME"
                elif ui.mode_back_btn_rect.collidepoint(event.pos):
                    audio.play_click(); game_state = "MENU"
        ui.draw_mode_select(screen)

    elif game_state == "SETTINGS":
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if ui.music_slider_rect.collidepoint(event.pos): dragging_music_slider = True
                    elif ui.sfx_slider_rect.collidepoint(event.pos): dragging_sfx_slider = True
                    
                    if dropdown_active:
                         for i, res in enumerate(resolutions):
                            opt = pygame.Rect(ui.dropdown_rect.x, ui.dropdown_rect.bottom+(i*int(30*settings.UI_SCALE)), ui.dropdown_rect.width, int(30*settings.UI_SCALE))
                            if opt.collidepoint(event.pos): audio.play_click(); temp_res_idx = i; dropdown_active = False; break
                         else: 
                             if not ui.dropdown_rect.collidepoint(event.pos): dropdown_active = False
                    else:
                        if ui.dropdown_rect.collidepoint(event.pos): audio.play_click(); dropdown_active = True
                        
                    if fullscreen_active:
                         modes = [False, True] 
                         for i, mode in enumerate(modes):
                             opt = pygame.Rect(ui.fullscreen_dd_rect.x, ui.fullscreen_dd_rect.bottom+(i*int(30*settings.UI_SCALE)), ui.fullscreen_dd_rect.width, int(30*settings.UI_SCALE))
                             if opt.collidepoint(event.pos): 
                                 audio.play_click()
                                 temp_fullscreen = mode 
                                 fullscreen_active = False
                                 break
                         else:
                             if not ui.fullscreen_dd_rect.collidepoint(event.pos): fullscreen_active = False
                    else:
                        if ui.fullscreen_dd_rect.collidepoint(event.pos): 
                            audio.play_click(); fullscreen_active = True
                            
                    if ui.apply_btn_rect.collidepoint(event.pos): audio.play_click(); apply_settings()
                    elif ui.ok_btn_rect.collidepoint(event.pos): audio.play_click(); apply_settings(); game_state = previous_state
                    elif ui.cancel_btn_rect.collidepoint(event.pos): audio.play_click(); game_state = previous_state
            
            elif event.type == pygame.MOUSEBUTTONUP: dragging_music_slider = False; dragging_sfx_slider = False
            elif event.type == pygame.MOUSEMOTION:
                if dragging_music_slider: temp_music_volume = max(0.0, min(1.0, (event.pos[0] - ui.music_slider_rect.x) / ui.music_slider_rect.width))
                if dragging_sfx_slider: temp_sfx_volume = max(0.0, min(1.0, (event.pos[0] - ui.sfx_slider_rect.x) / ui.sfx_slider_rect.width))
        
        ui.draw_settings(screen, temp_music_volume, temp_sfx_volume, resolutions, temp_res_idx, dropdown_active, fullscreen_active, temp_fullscreen)

    elif game_state == "PAUSED":
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: game_state = "GAME"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if ui.resume_btn_rect.collidepoint(event.pos): audio.play_click(); game_state = "GAME"
                elif ui.restart_btn_rect.collidepoint(event.pos): audio.play_click(); reset_game(); game_state = "GAME"
                elif ui.pause_setting_btn_rect.collidepoint(event.pos): 
                    audio.play_click(); previous_state="PAUSED"
                    temp_music_volume=audio.current_music_volume
                    temp_sfx_volume=audio.current_sfx_volume
                    temp_res_idx=current_res_idx
                    temp_fullscreen = settings.IS_FULLSCREEN
                    game_state="SETTINGS"
                elif ui.menu_return_btn_rect.collidepoint(event.pos): audio.play_click(); audio.play_music("MENU"); game_state = "MENU"
        ui.draw_pause_menu(screen)

    elif game_state == "GAME_OVER":
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if ui.game_over_home_btn_rect.collidepoint(event.pos):
                    audio.play_click(); audio.play_music("MENU"); reset_game(); game_state = "MENU"
        ui.draw_game_over(screen, p1_score, p2_score)

    elif game_state == "GAME":
        current_hand = player1_hand if turn == 1 else player2_hand
        
        # --- BOT TURN ---
        if IS_SINGLE_PLAYER and turn == 2:
            bot.start_turn()
            action, data, msg = bot.update(current_hand, grid_logic, tile_bag)
            
            if action == 'WAIT':
                if msg: message = msg
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: running = False
            
            elif action == 'SUBMIT_BOT':
                placed_tiles = data 
                score, valid_msg = validate_move(placed_tiles, grid_logic)
                if score > 0:
                    audio.play_place(); p2_score += score; message = f"Bot: {valid_msg}"
                    for t in placed_tiles:
                        board_tiles.append(t); grid_logic[t.grid_pos[0]][t.grid_pos[1]] = t.value
                        if t in current_hand: current_hand.remove(t)
                    
                    consecutive_skips = 0 # วางสำเร็จ ล้างค่าตัวนับ Skip
                    draw_initial_hand(current_hand)
                    check_game_over(current_hand)
                    
                    turn = 3 - turn; has_rerolled = False
                else:
                    for t in placed_tiles: t.rect.topleft = t.orig_pos; t.on_board = False; t.grid_pos = None
                    print(f"Bot Error: {valid_msg}"); turn = 3 - turn

            elif action == 'REROLL':
                if len(tile_bag) > 0:
                    audio.play_click()
                    for t in current_hand: tile_bag.append(t.value)
                    current_hand.clear(); random.shuffle(tile_bag)
                    draw_initial_hand(current_hand) 
                    
                    consecutive_skips += 1 # นับเป็น 1 Skip ตามกฎสากล
                    message = f"Bot swapped tiles. ({consecutive_skips}/6)"
                    turn = 3 - turn; has_rerolled = False
                    check_game_over(current_hand)
                else:
                    turn = 3 - turn; consecutive_skips += 1; message = f"Bot Skipped! ({consecutive_skips}/6)"; check_game_over(current_hand)

            elif action == 'SKIP':
                audio.play_click(); turn = 3 - turn; has_rerolled = False; consecutive_skips += 1
                message = f"Bot Skipped! ({consecutive_skips}/6)"
                check_game_over(current_hand)
                
        # --- PLAYER TURN ---
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: game_state = "PAUSED"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if ui.end_turn_btn.collidepoint(event.pos):
                            audio.play_click()
                            placed = [t for t in current_hand if t.on_board]
                            score, msg = validate_move(placed, grid_logic)
                            message = msg
                            if score > 0:
                                if turn == 1: p1_score += score
                                else: p2_score += score
                                for t in placed: board_tiles.append(t); grid_logic[t.grid_pos[0]][t.grid_pos[1]] = t.value; current_hand.remove(t)
                                
                                consecutive_skips = 0 # วางสำเร็จ ล้างค่าตัวนับ Skip
                                draw_initial_hand(current_hand)
                                if check_game_over(current_hand): break
                                turn = 3 - turn; has_rerolled = False
                            else:
                                for t in placed: t.rect.topleft = t.orig_pos; t.on_board = False; t.grid_pos = None
                        
                        elif ui.skip_btn_rect.collidepoint(event.pos):
                            audio.play_click()
                            for t in current_hand:
                                if t.on_board: t.rect.topleft = t.orig_pos; t.on_board = False; t.grid_pos = None
                            
                            consecutive_skips += 1 # นับเป็น 1 Skip
                            turn = 3 - turn; has_rerolled = False; message = f"Skipped! ({consecutive_skips}/6)"; check_game_over(current_hand)
                        
                        elif ui.reroll_btn_rect.collidepoint(event.pos):
                            if len(tile_bag) > 0:
                                audio.play_click()
                                for t in current_hand:
                                    if t.on_board: t.rect.topleft = t.orig_pos; t.on_board = False; t.grid_pos = None
                                
                                for t in current_hand: tile_bag.append(t.value)
                                current_hand.clear(); random.shuffle(tile_bag); draw_initial_hand(current_hand)
                                
                                consecutive_skips += 1 # นับเป็น 1 Skip ตามกฎสากล
                                message = f"Tiles exchanged! ({consecutive_skips}/6)"
                                turn = 3 - turn; has_rerolled = False 
                                if check_game_over(current_hand): break
                            else: 
                                message = "Bag is empty!"
                        
                        else:
                            for tile in reversed(current_hand):
                                if tile.rect.collidepoint(event.pos):
                                    selected_tile = tile; selected_tile.dragging = True
                                    mx, my = event.pos; off_x, off_y = tile.rect.x - mx, tile.rect.y - my
                                    break
                elif event.type == pygame.MOUSEBUTTONUP:
                    if selected_tile: audio.play_place(); selected_tile.dragging = False; snap_to_grid(selected_tile); selected_tile = None
                elif event.type == pygame.MOUSEMOTION:
                    if selected_tile and selected_tile.dragging: selected_tile.rect.x, selected_tile.rect.y = event.pos[0] + off_x, event.pos[1] + off_y

        screen.fill(GRAY)
        ui.draw_game_interface(screen, p1_score, p2_score, turn, message, has_rerolled, len(tile_bag))
        draw_board_background()
        for t in board_tiles: t.draw(screen)
        for t in current_hand: 
            if t != selected_tile: t.draw(screen)
        if selected_tile: selected_tile.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()