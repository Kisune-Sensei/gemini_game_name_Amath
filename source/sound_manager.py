import pygame
import os

# --- ตั้งค่าชื่อไฟล์เสียง ---
MENU_BGM = "sounds/Sakura-Girl-Yay-chosic.com_.mp3"
GAME_BGM = "sounds/Sunset-Landscape(chosic.com).mp3"
CLICK_SFX_PATH = "sounds/a9ne86ocrek-mouse-click-sfx-9.mp3" 
PLACE_SFX_PATH = "sounds/chess-piece-move-r7xqxvpz.wav"

current_music_volume = 0.5
current_sfx_volume = 0.5
click_sfx = None
place_sfx = None

def init_sounds():
    global click_sfx, place_sfx
    pygame.mixer.init()
    
    try:
        if os.path.exists(CLICK_SFX_PATH):
            click_sfx = pygame.mixer.Sound(CLICK_SFX_PATH)
            click_sfx.set_volume(current_sfx_volume)
        if os.path.exists(PLACE_SFX_PATH):
            place_sfx = pygame.mixer.Sound(PLACE_SFX_PATH)
            place_sfx.set_volume(current_sfx_volume)
    except Exception as e:
        print(f"Error loading SFX: {e}")

def play_music(state):
    if not pygame.mixer.get_init(): return
    try:
        if state == "MENU":
            pygame.mixer.music.load(MENU_BGM)
            pygame.mixer.music.set_volume(current_music_volume)
            pygame.mixer.music.play(-1)
        elif state == "GAME":
            pygame.mixer.music.load(GAME_BGM)
            pygame.mixer.music.set_volume(current_music_volume)
            pygame.mixer.music.play(-1)
    except Exception as e:
        print(f"Error loading music ({state}): {e}")

def set_music_volume(vol):
    global current_music_volume
    current_music_volume = vol
    if pygame.mixer.get_init():
        pygame.mixer.music.set_volume(vol)

def set_sfx_volume(vol):
    global current_sfx_volume
    current_sfx_volume = vol
    if click_sfx: click_sfx.set_volume(vol)
    if place_sfx: place_sfx.set_volume(vol)

def play_click():
    if click_sfx: click_sfx.play()

def play_place():
    if place_sfx: place_sfx.play()