import pygame
import source.settings as settings # ---> เปลี่ยนวิธี Import เพื่อดึงค่าล่าสุดเสมอ

class Tile(pygame.sprite.Sprite):
    def __init__(self, value, x, y):
        super().__init__()
        self.value = value
        # ใช้ settings.CELL_SIZE เพื่อให้ได้ค่าที่คำนวณใหม่ล่าสุด
        self.rect = pygame.Rect(x, y, settings.CELL_SIZE, settings.CELL_SIZE) 
        self.orig_pos = (x, y)
        self.grid_pos = None 
        self.on_board = False
        self.dragging = False
        
        self.update_size() 

    def update_size(self):
        """สร้างรูปเบี้ยใหม่ตามขนาด CELL_SIZE ปัจจุบัน"""
        # คำนวณขนาดเบี้ย (ลบขอบออกนิดหน่อยเพื่อให้เห็นเส้นตารางสวยๆ)
        # ใช้ settings.CELL_SIZE เสมอ
        size = settings.CELL_SIZE - 2 
        
        self.image = pygame.Surface((size, size))
        self.image.fill(settings.BEIGE) 
        
        # คำนวณขนาดฟอนต์ (ประมาณ 60% ของช่อง)
        font_size = int(settings.CELL_SIZE * 0.6)
        if font_size < 12: font_size = 12
            
        font = pygame.font.SysFont("arial", font_size, bold=True)
        
        # วาดตัวเลข
        text_surf = font.render(self.value, True, settings.BLACK)
        text_rect = text_surf.get_rect(center=(size//2, size//2))
        self.image.blit(text_surf, text_rect)
        
        # วาดคะแนนตัวเล็ก
        pts = settings.TILE_POINTS.get(self.value, 0)
        pt_font_size = int(settings.CELL_SIZE * 0.25)
        if pt_font_size < 8: pt_font_size = 8
            
        pt_font = pygame.font.SysFont("arial", pt_font_size)
        pt_surf = pt_font.render(str(pts), True, settings.BLACK)
        
        # จัดตำแหน่งคะแนน (มุมขวาล่าง)
        pt_x = size - pt_surf.get_width() - 4
        pt_y = size - pt_surf.get_height() - 2
        self.image.blit(pt_surf, (pt_x, pt_y))

        # อัปเดต Rect ให้ขนาดเท่าภาพใหม่
        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center

    def draw(self, surface):
        surface.blit(self.image, self.rect)