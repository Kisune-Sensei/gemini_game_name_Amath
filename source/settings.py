import pygame

# --- Screen & Grid Configuration ---
BASE_WIDTH = 1000
BASE_HEIGHT = 800

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

GRID_SIZE = 15
CELL_SIZE = 40 
BOARD_PIXEL_SIZE = GRID_SIZE * CELL_SIZE
BOARD_OFFSET_X = (SCREEN_WIDTH - BOARD_PIXEL_SIZE) // 2
BOARD_OFFSET_Y = (SCREEN_HEIGHT - BOARD_PIXEL_SIZE) // 2

UI_SCALE = 1.0 

IS_FULLSCREEN = False 

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)
RED = (200, 50, 50)
GREEN = (50, 200, 50)
BLUE = (50, 50, 200)
CYAN = (0, 200, 200)
GOLD = (255, 215, 0)
MENU_BG = (30, 30, 30)
BTN_COLOR = (70, 70, 70)
BTN_HOVER = (100, 100, 100)
SLIDER_BG = (100, 100, 100)
SLIDER_FG = (0, 255, 0)
DROPDOWN_BG = (230, 230, 230)
DISABLED = (100, 100, 100)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
BEIGE = (245, 222, 179)

def set_resolution(w, h):
    global SCREEN_WIDTH, SCREEN_HEIGHT, BOARD_OFFSET_X, BOARD_OFFSET_Y, CELL_SIZE, BOARD_PIXEL_SIZE, UI_SCALE
    SCREEN_WIDTH = w
    SCREEN_HEIGHT = h
    
    scale_w = w / BASE_WIDTH
    scale_h = h / BASE_HEIGHT
    UI_SCALE = min(scale_w, scale_h)
    
    reserved_ui_height = 260 * UI_SCALE 
    reserved_ui_width = 380 * UI_SCALE  
    
    available_h = h - reserved_ui_height
    available_w = w - reserved_ui_width
    
    target_board_size = min(available_h, available_w)
    
    CELL_SIZE = int(target_board_size // GRID_SIZE)
    if CELL_SIZE < 20: CELL_SIZE = 20
        
    BOARD_PIXEL_SIZE = GRID_SIZE * CELL_SIZE
    BOARD_OFFSET_X = (SCREEN_WIDTH - BOARD_PIXEL_SIZE) // 2
    
    center_y = (SCREEN_HEIGHT - (120 * UI_SCALE)) // 2 
    BOARD_OFFSET_Y = int(center_y - (BOARD_PIXEL_SIZE // 2))
    
    if BOARD_OFFSET_Y < 10: BOARD_OFFSET_Y = 10

# --- Game Data (ปรับเบี้ยใหม่รวม 80 ตัว) ---
FULL_TILE_SET = (
    # ตัวเลข 40 ตัว (0-3 มีอย่างละ 4 ตัว, 4-9 มีอย่างละ 3 ตัว, 10-15 มีอย่างละ 1 ตัว)
    ['0', '1', '2', '3'] * 4 + 
    ['4', '5', '6', '7', '8', '9'] * 3 +
    ['10', '11', '12', '13', '14', '15'] +
    
    # เครื่องหมายคณิตศาสตร์ 20 ตัว (+, -, *, / อย่างละ 5 ตัว)
    ['+'] * 5 + ['-'] * 5 + ['*'] * 5 + ['/'] * 5 +
    
    # เครื่องหมายเท่ากับ 20 ตัว
    ['='] * 20
)

TILE_POINTS = {
    '0': 1, '1': 1, '2': 1, '3': 1, '4': 2, '5': 2, '6': 2, '7': 2, '8': 2, '9': 2,
    '10': 3, '11': 4, '12': 4, '13': 6, '14': 6, '15': 6, '16': 7, '17': 7, '18': 7, '19': 9, '20': 9,
    '+': 2, '-': 2, '*': 2, '/': 2, '=': 1
}

TRIPLE_EQ = [(0,0), (0,7), (0,14), (7,0), (7,14), (14,0), (14,7), (14,14)]
DOUBLE_EQ = [(1,1), (2,2), (3,3), (4,4), (10,10), (11,11), (12,12), (13,13),
             (1,13), (2,12), (3,11), (4,10), (10,4), (11,3), (12,2), (13,1)]
TRIPLE_PIECE = [(1,5), (1,9), (5,1), (5,5), (5,9), (5,13), 
                (9,1), (9,5), (9,9), (9,13), (13,5), (13,9)]
DOUBLE_PIECE = [(0,3), (0,11), (2,6), (2,8), (3,0), (3,7), (3,14), (6,2), (6,6), (6,8), (6,12),
                (7,3), (7,11), (8,2), (8,6), (8,8), (8,12), (11,0), (11,7), (11,14),
                (12,6), (12,8), (14,3), (14,11)]