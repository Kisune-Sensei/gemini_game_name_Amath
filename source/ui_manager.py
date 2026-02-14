import pygame
from .settings import *
from . import settings as game_settings

# --- UI Rects ---
start_btn_rect = pygame.Rect(0,0,0,0)
setting_btn_rect = pygame.Rect(0,0,0,0)
exit_btn_rect = pygame.Rect(0,0,0,0)

single_player_btn_rect = pygame.Rect(0,0,0,0)
multi_player_btn_rect = pygame.Rect(0,0,0,0)
mode_back_btn_rect = pygame.Rect(0,0,0,0)

end_turn_btn = pygame.Rect(0,0,0,0)    
skip_btn_rect = pygame.Rect(0,0,0,0)   
reroll_btn_rect = pygame.Rect(0,0,0,0) 

resume_btn_rect = pygame.Rect(0,0,0,0)
restart_btn_rect = pygame.Rect(0,0,0,0)
pause_setting_btn_rect = pygame.Rect(0,0,0,0)
menu_return_btn_rect = pygame.Rect(0,0,0,0)
game_over_home_btn_rect = pygame.Rect(0,0,0,0) 

music_slider_rect = pygame.Rect(0,0,0,0)
sfx_slider_rect = pygame.Rect(0,0,0,0)

dropdown_rect = pygame.Rect(0,0,0,0)      
fullscreen_dd_rect = pygame.Rect(0,0,0,0) 

apply_btn_rect = pygame.Rect(0,0,0,0)
ok_btn_rect = pygame.Rect(0,0,0,0)
cancel_btn_rect = pygame.Rect(0,0,0,0)

# Fonts
small_font = None
score_font = None
menu_title = None
menu_btn_font = None
setting_font = None

def init_ui():
    """เรียกใช้ฟังก์ชันนี้เพื่อคำนวณขนาด UI ใหม่ทั้งหมด"""
    recalc_ui_positions()

def recalc_ui_positions():
    """คำนวณตำแหน่งและขนาดปุ่ม/ฟอนต์ ตาม UI_SCALE"""
    global small_font, score_font, menu_title, menu_btn_font, setting_font
    
    W = game_settings.SCREEN_WIDTH
    H = game_settings.SCREEN_HEIGHT
    SCALE = game_settings.UI_SCALE # ดึงค่า Scale ที่คำนวณไว้จาก settings
    
    # 1. สร้าง Font ใหม่ตาม Scale (คูณขนาดด้วย SCALE)
    small_font = pygame.font.SysFont("arial", int(16 * SCALE), bold=True)
    score_font = pygame.font.SysFont("arial", int(30 * SCALE), bold=True)
    menu_title = pygame.font.SysFont("arial", int(80 * SCALE), bold=True)
    menu_btn_font = pygame.font.SysFont("arial", int(40 * SCALE), bold=True)
    setting_font = pygame.font.SysFont("arial", int(20 * SCALE), bold=True)
    
    CX, CY = W // 2, H // 2
    
    # 2. ขนาดปุ่มพื้นฐาน (คูณ Scale)
    btn_w = int(200 * SCALE)
    btn_h = int(60 * SCALE)
    spacing = int(20 * SCALE)
    
    # --- Menu ---
    start_btn_rect.update(CX - btn_w//2, CY - btn_h, btn_w, btn_h)
    setting_btn_rect.update(CX - btn_w//2, CY + spacing, btn_w, btn_h)
    exit_btn_rect.update(CX - btn_w//2, CY + btn_h + spacing*2, btn_w, btn_h)

    # --- Mode Select ---
    mode_w = int(240 * SCALE)
    single_player_btn_rect.update(CX - mode_w//2, CY - btn_h, mode_w, btn_h)
    multi_player_btn_rect.update(CX - mode_w//2, CY + spacing, mode_w, btn_h)
    mode_back_btn_rect.update(CX - mode_w//2, CY + btn_h + spacing*2, mode_w, btn_h)
    
    # --- Game Interface ---
    game_btn_w = int(110 * SCALE)
    game_btn_h = int(45 * SCALE)
    game_spacing = int(15 * SCALE)
    y_pos = H - int(95 * SCALE)
    
    end_turn_btn.update(W - game_btn_w - int(30*SCALE), y_pos, game_btn_w, game_btn_h)
    skip_btn_rect.update(end_turn_btn.x - game_btn_w - game_spacing, y_pos, game_btn_w, game_btn_h)
    reroll_btn_rect.update(int(30*SCALE), y_pos, game_btn_w, game_btn_h)
    
    # --- Pause ---
    resume_btn_rect.update(CX - btn_w//2, CY - 140*SCALE, btn_w, btn_h)
    restart_btn_rect.update(CX - btn_w//2, CY - 60*SCALE, btn_w, btn_h)
    pause_setting_btn_rect.update(CX - btn_w//2, CY + 20*SCALE, btn_w, btn_h)
    menu_return_btn_rect.update(CX - btn_w//2, CY + 100*SCALE, btn_w, btn_h)
    
    # --- Game Over ---
    game_over_home_btn_rect.update(CX - btn_w//2, CY + 100*SCALE, btn_w, btn_h)
    
    # --- Settings ---
    slider_w = int(200 * SCALE)
    slider_h = int(10 * SCALE)
    dd_h = int(30 * SCALE)
    
    music_slider_rect.update(CX - slider_w//2, CY - 110*SCALE, slider_w, slider_h)
    sfx_slider_rect.update(CX - slider_w//2, CY - 50*SCALE, slider_w, slider_h)
    
    dropdown_rect.update(CX - slider_w//2, CY + 20*SCALE, slider_w, dd_h)      
    fullscreen_dd_rect.update(CX - slider_w//2, CY + 90*SCALE, slider_w, dd_h) 
    
    setting_btn_w = int(100 * SCALE)
    setting_btn_h = int(40 * SCALE)
    s_spacing = int(20 * SCALE)
    
    total_w = (setting_btn_w * 3) + (s_spacing * 2)
    start_x = CX - (total_w // 2)
    s_y_pos = H - int(80 * SCALE)
    
    apply_btn_rect.update(start_x, s_y_pos, setting_btn_w, setting_btn_h)
    ok_btn_rect.update(start_x + setting_btn_w + s_spacing, s_y_pos, setting_btn_w, setting_btn_h)
    cancel_btn_rect.update(start_x + (setting_btn_w + s_spacing) * 2, s_y_pos, setting_btn_w, setting_btn_h)

def draw_menu(screen):
    screen.fill(MENU_BG)
    W, H = game_settings.SCREEN_WIDTH, game_settings.SCREEN_HEIGHT
    title = menu_title.render("A-MATH SIM", True, GREEN)
    screen.blit(title, title.get_rect(center=(W//2, H//4)))
    mouse_pos = pygame.mouse.get_pos()
    for rect, text in [(start_btn_rect, "PLAY"), (setting_btn_rect, "SETTINGS"), (exit_btn_rect, "EXIT")]:
        color = BTN_HOVER if rect.collidepoint(mouse_pos) else BTN_COLOR
        pygame.draw.rect(screen, color, rect, border_radius=int(15*game_settings.UI_SCALE))
        txt = menu_btn_font.render(text, True, WHITE)
        screen.blit(txt, txt.get_rect(center=rect.center))

def draw_mode_select(screen):
    screen.fill(MENU_BG)
    W, H = game_settings.SCREEN_WIDTH, game_settings.SCREEN_HEIGHT
    title = menu_title.render("SELECT MODE", True, WHITE)
    screen.blit(title, title.get_rect(center=(W//2, H//4)))
    mouse_pos = pygame.mouse.get_pos()
    
    for rect, text in [(single_player_btn_rect, "VS BOT"), (multi_player_btn_rect, "VS PLAYER"), (mode_back_btn_rect, "BACK")]:
        color = BTN_HOVER if rect.collidepoint(mouse_pos) else BTN_COLOR
        pygame.draw.rect(screen, color, rect, border_radius=int(15*game_settings.UI_SCALE))
        txt = menu_btn_font.render(text, True, WHITE)
        screen.blit(txt, txt.get_rect(center=rect.center))

def draw_pause_menu(screen):
    W, H = game_settings.SCREEN_WIDTH, game_settings.SCREEN_HEIGHT
    overlay = pygame.Surface((W, H))
    overlay.set_alpha(200)
    overlay.fill(BLACK)
    screen.blit(overlay, (0,0))
    title = menu_title.render("PAUSED", True, WHITE)
    screen.blit(title, title.get_rect(center=(W//2, H//4 - 50*game_settings.UI_SCALE)))
    mouse_pos = pygame.mouse.get_pos()
    btns = [(resume_btn_rect, "RETURN"), (restart_btn_rect, "RESTART"), 
            (pause_setting_btn_rect, "SETTINGS"), (menu_return_btn_rect, "MENU")]
    for rect, text in btns:
        color = BTN_HOVER if rect.collidepoint(mouse_pos) else BTN_COLOR
        pygame.draw.rect(screen, color, rect, border_radius=int(15*game_settings.UI_SCALE))
        txt = menu_btn_font.render(text, True, WHITE)
        screen.blit(txt, txt.get_rect(center=rect.center))

def draw_settings(screen, music_vol, sfx_vol, resolutions, res_idx, dropdown_active, fullscreen_active, is_fullscreen_temp):
    screen.fill(MENU_BG)
    W, H = game_settings.SCREEN_WIDTH, game_settings.SCREEN_HEIGHT
    SCALE = game_settings.UI_SCALE
    
    title = menu_title.render("SETTINGS", True, WHITE)
    screen.blit(title, title.get_rect(center=(W//2, H//6)))
    mouse_pos = pygame.mouse.get_pos()
    
    # Music
    music_txt = setting_font.render(f"Music: {int(music_vol * 100)}%", True, WHITE)
    screen.blit(music_txt, (music_slider_rect.x, music_slider_rect.y - 25*SCALE))
    pygame.draw.rect(screen, SLIDER_BG, music_slider_rect, border_radius=5)
    music_knob = music_slider_rect.x + (music_slider_rect.width * music_vol)
    pygame.draw.circle(screen, SLIDER_FG, (int(music_knob), music_slider_rect.centery), int(10*SCALE))

    # SFX
    sfx_txt = setting_font.render(f"SFX: {int(sfx_vol * 100)}%", True, WHITE)
    screen.blit(sfx_txt, (sfx_slider_rect.x, sfx_slider_rect.y - 25*SCALE))
    pygame.draw.rect(screen, SLIDER_BG, sfx_slider_rect, border_radius=5)
    sfx_knob = sfx_slider_rect.x + (sfx_slider_rect.width * sfx_vol)
    pygame.draw.circle(screen, SLIDER_FG, (int(sfx_knob), sfx_slider_rect.centery), int(10*SCALE))
    
    # Dropdowns
    opt_h = int(30 * SCALE)
    
    # 1. Resolution
    res_txt = setting_font.render("Resolution:", True, WHITE)
    screen.blit(res_txt, (dropdown_rect.x, dropdown_rect.y - 25*SCALE))
    pygame.draw.rect(screen, WHITE, dropdown_rect)
    pygame.draw.rect(screen, BLACK, dropdown_rect, 2)
    curr_txt = f"{resolutions[res_idx][0]} x {resolutions[res_idx][1]}"
    txt = setting_font.render(curr_txt, True, BLACK)
    screen.blit(txt, txt.get_rect(center=dropdown_rect.center))
    
    # 2. Fullscreen
    fs_label = setting_font.render("Display Mode:", True, WHITE)
    screen.blit(fs_label, (fullscreen_dd_rect.x, fullscreen_dd_rect.y - 25*SCALE))
    pygame.draw.rect(screen, WHITE, fullscreen_dd_rect)
    pygame.draw.rect(screen, BLACK, fullscreen_dd_rect, 2)
    mode_text = "Fullscreen" if is_fullscreen_temp else "Windowed"
    fs_txt_surf = setting_font.render(mode_text, True, BLACK)
    screen.blit(fs_txt_surf, fs_txt_surf.get_rect(center=fullscreen_dd_rect.center))
    
    # Draw Active Dropdowns (Overlay)
    if dropdown_active:
        for i, res in enumerate(resolutions):
            opt = pygame.Rect(dropdown_rect.x, dropdown_rect.bottom + (i*opt_h), dropdown_rect.width, opt_h)
            color = (200, 200, 255) if opt.collidepoint(mouse_pos) else DROPDOWN_BG
            pygame.draw.rect(screen, color, opt)
            pygame.draw.rect(screen, BLACK, opt, 1)
            opt_s = setting_font.render(f"{res[0]} x {res[1]}", True, BLACK)
            screen.blit(opt_s, opt_s.get_rect(center=opt.center))
            
    if fullscreen_active:
        modes = ["Windowed", "Fullscreen"]
        for i, mode in enumerate(modes):
            opt = pygame.Rect(fullscreen_dd_rect.x, fullscreen_dd_rect.bottom + (i*opt_h), fullscreen_dd_rect.width, opt_h)
            color = (200, 200, 255) if opt.collidepoint(mouse_pos) else DROPDOWN_BG
            pygame.draw.rect(screen, color, opt)
            pygame.draw.rect(screen, BLACK, opt, 1)
            opt_s = setting_font.render(mode, True, BLACK)
            screen.blit(opt_s, opt_s.get_rect(center=opt.center))
            
    # Bottom Buttons
    for rect, text in [(apply_btn_rect, "APPLY"), (ok_btn_rect, "OK"), (cancel_btn_rect, "CANCEL")]:
        color = BTN_HOVER if rect.collidepoint(mouse_pos) else BTN_COLOR
        pygame.draw.rect(screen, color, rect, border_radius=10)
        txt = small_font.render(text, True, WHITE)
        screen.blit(txt, txt.get_rect(center=rect.center))

def draw_game_interface(screen, p1_score, p2_score, turn, message, has_rerolled, tiles_left):
    W, H = game_settings.SCREEN_WIDTH, game_settings.SCREEN_HEIGHT
    SCALE = game_settings.UI_SCALE
    
    # Player 1 Box
    p1_bg = pygame.Rect(20*SCALE, 80*SCALE, 150*SCALE, 100*SCALE)
    pygame.draw.rect(screen, DARK_GRAY, p1_bg, border_radius=10)
    pygame.draw.rect(screen, RED if turn == 1 else BLACK, p1_bg, 3, border_radius=10)
    
    lbl1 = small_font.render("PLAYER 1", True, WHITE)
    screen.blit(lbl1, (p1_bg.x + 30*SCALE, p1_bg.y + 10*SCALE))
    sc1 = score_font.render(str(p1_score), True, GOLD)
    screen.blit(sc1, sc1.get_rect(center=p1_bg.center))
    
    if turn == 1:
        bag_txt = small_font.render(f"Bag: {tiles_left}", True, (180, 180, 180))
        screen.blit(bag_txt, bag_txt.get_rect(center=(p1_bg.centerx, p1_bg.bottom - 15*SCALE)))

    # Player 2 Box
    p2_bg = pygame.Rect(W - 170*SCALE, 80*SCALE, 150*SCALE, 100*SCALE)
    pygame.draw.rect(screen, DARK_GRAY, p2_bg, border_radius=10)
    pygame.draw.rect(screen, BLUE if turn == 2 else BLACK, p2_bg, 3, border_radius=10)
    
    lbl2 = small_font.render("PLAYER 2", True, WHITE)
    screen.blit(lbl2, (p2_bg.x + 30*SCALE, p2_bg.y + 10*SCALE))
    sc2 = score_font.render(str(p2_score), True, GOLD)
    screen.blit(sc2, sc2.get_rect(center=p2_bg.center))
    
    if turn == 2:
        bag_txt = small_font.render(f"Bag: {tiles_left}", True, (180, 180, 180))
        screen.blit(bag_txt, bag_txt.get_rect(center=(p2_bg.centerx, p2_bg.bottom - 15*SCALE)))

    # Message Box
    msg_bg = pygame.Rect(game_settings.BOARD_OFFSET_X, 10*SCALE, game_settings.BOARD_PIXEL_SIZE, 30*SCALE)
    pygame.draw.rect(screen, BLACK, msg_bg)
    msg_surf = small_font.render(message, True, WHITE)
    screen.blit(msg_surf, msg_surf.get_rect(center=msg_bg.center))
    
    # Rack Background
    rack_h = 120 * SCALE
    rack_bg = pygame.Rect(0, H - rack_h, W, rack_h)
    pygame.draw.rect(screen, DARK_GRAY, rack_bg)
    pygame.draw.line(screen, WHITE, (0, H - rack_h), (W, H - rack_h), 2)
    
    # Buttons
    rad = int(15*SCALE)
    pygame.draw.rect(screen, RED if turn == 1 else BLUE, end_turn_btn, border_radius=rad)
    pygame.draw.rect(screen, WHITE, end_turn_btn, 2, border_radius=rad)
    btn_text = small_font.render("SUBMIT", True, WHITE)
    screen.blit(btn_text, btn_text.get_rect(center=end_turn_btn.center))

    pygame.draw.rect(screen, CYAN, skip_btn_rect, border_radius=rad)
    pygame.draw.rect(screen, WHITE, skip_btn_rect, 2, border_radius=rad)
    skip_txt = small_font.render("SKIP", True, WHITE)
    screen.blit(skip_txt, skip_txt.get_rect(center=skip_btn_rect.center))

    reroll_c = DISABLED if has_rerolled else CYAN
    pygame.draw.rect(screen, reroll_c, reroll_btn_rect, border_radius=rad)
    pygame.draw.rect(screen, WHITE, reroll_btn_rect, 2, border_radius=rad)
    rr_txt = small_font.render("REROLL", True, WHITE)
    screen.blit(rr_txt, rr_txt.get_rect(center=reroll_btn_rect.center))

def draw_game_over(screen, p1_score, p2_score):
    W, H = game_settings.SCREEN_WIDTH, game_settings.SCREEN_HEIGHT
    overlay = pygame.Surface((W, H))
    overlay.set_alpha(220)
    overlay.fill(BLACK)
    screen.blit(overlay, (0,0))
    
    if p1_score > p2_score:
        winner_text = "PLAYER 1 WINS!"
        color = RED
    elif p2_score > p1_score:
        winner_text = "PLAYER 2 WINS!"
        color = BLUE
    else:
        winner_text = "DRAW!"
        color = GREEN
        
    win_surf = menu_title.render(winner_text, True, color)
    screen.blit(win_surf, win_surf.get_rect(center=(W//2, H//4)))
    
    score_text = menu_btn_font.render(f"Final Score: {p1_score} - {p2_score}", True, WHITE)
    screen.blit(score_text, score_text.get_rect(center=(W//2, H//2)))

    mouse_pos = pygame.mouse.get_pos()
    color_btn = BTN_HOVER if game_over_home_btn_rect.collidepoint(mouse_pos) else BTN_COLOR
    pygame.draw.rect(screen, color_btn, game_over_home_btn_rect, border_radius=int(15*game_settings.UI_SCALE))
    
    btn_txt = menu_btn_font.render("MAIN MENU", True, WHITE)
    screen.blit(btn_txt, btn_txt.get_rect(center=game_over_home_btn_rect.center))