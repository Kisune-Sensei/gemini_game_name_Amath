import pygame
import random
import itertools
import time
import source.settings as settings 
from source.settings import GRID_SIZE
from .sprites import Tile
from source.logic import validate_move 

class AIPlayer:
    def __init__(self):
        self.thinking = False
        self.think_start_time = 0
        self.action_delay = 500 
        self.tried_reroll = False
        self.calculation_limit = 1.5 # ลดเวลาคิดเหลือ 1.5 วินาที

    def start_turn(self):
        if not self.thinking:
            self.thinking = True
            self.think_start_time = pygame.time.get_ticks()
            self.tried_reroll = False

    def update(self, current_hand, grid_logic, tile_bag):
        if not self.thinking:
            return 'WAIT', None, ""

        if pygame.time.get_ticks() - self.think_start_time < self.action_delay:
            return 'WAIT', None, "Bot is thinking..."

        self.thinking = False
        
        start_calc = time.time()
        
        # 1. หาตาเดินที่ดีที่สุด
        move = self.find_best_move(current_hand, grid_logic, start_calc)
        
        if move:
            return 'SUBMIT_BOT', move, "Bot Found a Move!"
        
        # 2. ถ้าหาไม่ได้ ลอง Reroll
        if not self.tried_reroll and len(tile_bag) > 0:
            self.tried_reroll = True
            return 'REROLL', None, "Bot swapped tiles."

        # 3. ถ้าไม่ไหวจริงๆ ก็ Skip
        return 'SKIP', None, "Bot skipped turn."

    def find_best_move(self, hand, grid, start_time):
        hand_values = [t.value for t in hand]
        
        # --- กรณี 1: กระดานว่าง ---
        if self.is_board_empty(grid):
            # สุ่มหาสมการจากมือ
            eq_data = self.find_valid_equation(hand_values)
            if eq_data:
                # ลองวางที่ (7,7) ตรงกลาง
                tiles = self.create_tiles_for_placement(eq_data, 7, 7, horizontal=True, hand_objs=hand)
                score, _ = validate_move(tiles, grid)
                if score > 0: return tiles
            return None # <--- ถ้าหาไม่ได้ ให้ return None เพื่อให้ update() ไปสั่ง Skip

        # --- กรณี 2: มีเบี้ยเดิมอยู่แล้ว (OPTIMIZED) ---
        # 1. รวบรวมตำแหน่งที่มีเบี้ยทั้งหมดบนกระดาน
        occupied_cells = []
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if grid[r][c] is not None:
                    occupied_cells.append((r, c))
        
        # 2. สับตำแหน่ง เพื่อให้บอทเลือกจุดเกาะไม่ซ้ำเดิม
        random.shuffle(occupied_cells)
        
        # 3. ***สำคัญ*** เลือกมาลองแค่ 20 จุดพอ (ไม่ต้องเช็คทั้งกระดาน)
        max_attempts = 20 
        search_candidates = occupied_cells[:max_attempts]

        for r, c in search_candidates:
            # ป้องกันจอค้าง ระหว่างวนลูป
            pygame.event.pump() 
            
            # เช็คเวลา ถ้าคิดนานเกิน ตัดจบเลย -> return None เพื่อให้ Skip
            if time.time() - start_time > self.calculation_limit:
                return None 

            # ลองแนวนอน
            move = self.try_place_at(r, c, grid[r][c], hand_values, grid, hand, horizontal=True)
            if move: return move
            
            # ลองแนวตั้ง
            move = self.try_place_at(r, c, grid[r][c], hand_values, grid, hand, horizontal=False)
            if move: return move
                    
        return None

    def is_board_empty(self, grid):
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if grid[r][c] is not None:
                    return False
        return True

    def find_valid_equation(self, available_chars):
        nums = [x for x in available_chars if x.isdigit()]
        ops = [x for x in available_chars if x in ['+', '-', '*', '/']]
        eq_signs = [x for x in available_chars if x == '=']

        if not eq_signs or len(nums) < 2: return None

        # ลดรอบการสุ่มผสมเลขเหลือ 30 รอบพอ
        for _ in range(30): 
            random.shuffle(nums)
            if len(nums) >= 3 and ops:
                n1, n2, res = nums[0], nums[1], nums[2]
                op = random.choice(ops)
                if self.check_math(f"{n1}{op}{n2}={res}"):
                    return [n1, op, n2, '=', res]
            
            if len(nums) >= 2:
                n1, n2 = nums[0], nums[1]
                if n1 == n2:
                    return [n1, '=', n2]

        return None

    def check_math(self, eq_str):
        try:
            lhs, rhs = eq_str.split('=')
            return eval(lhs) == eval(rhs)
        except:
            return False

    def try_place_at(self, r, c, anchor_val, hand_vals, grid, hand_objs, horizontal):
        temp_pool = hand_vals.copy()
        temp_pool.append(anchor_val)
        
        eq_list = self.find_valid_equation(temp_pool)
        if not eq_list: return None
        
        if anchor_val not in eq_list: return None
        
        # หา index ของ anchor (ถ้ามีหลายตัว เอาตัวแรก)
        anchor_idx = eq_list.index(anchor_val)

        start_r = r if horizontal else r - anchor_idx
        start_c = c - anchor_idx if horizontal else c
        
        length = len(eq_list)
        # เช็คขอบกระดานเบื้องต้น
        if horizontal:
            if start_c < 0 or start_c + length > GRID_SIZE: return None
        else:
            if start_r < 0 or start_r + length > GRID_SIZE: return None

        potential_tiles = self.create_tiles_for_placement_at(start_r, start_c, eq_list, horizontal, hand_objs, grid)
        
        if not potential_tiles: return None

        score, msg = validate_move(potential_tiles, grid)
        
        if score > 0:
            return potential_tiles
        else:
            return None

    def create_tiles_for_placement(self, eq_list, center_r, center_c, horizontal, hand_objs):
        tiles_to_place = []
        start_r = center_r
        start_c = center_c - (len(eq_list) // 2)
        
        temp_hand = hand_objs.copy()
        
        for i, val in enumerate(eq_list):
            found_tile = None
            for t in temp_hand:
                if t.value == val:
                    found_tile = t
                    break
            
            if found_tile:
                found_tile.grid_pos = (start_r, start_c + i)
                found_tile.rect.x = (start_c + i) * settings.CELL_SIZE + settings.BOARD_OFFSET_X + 1
                found_tile.rect.y = start_r * settings.CELL_SIZE + settings.BOARD_OFFSET_Y + 1
                found_tile.on_board = True
                found_tile.update_size() 
                
                tiles_to_place.append(found_tile)
                temp_hand.remove(found_tile)
                
        return tiles_to_place

    def create_tiles_for_placement_at(self, start_r, start_c, eq_list, horizontal, hand_objs, grid):
        tiles_to_place = []
        temp_hand = hand_objs.copy()
        
        for i, val in enumerate(eq_list):
            curr_r = start_r if horizontal else start_r + i
            curr_c = start_c + i if horizontal else start_c
            
            if not (0 <= curr_r < GRID_SIZE and 0 <= curr_c < GRID_SIZE):
                return None

            if grid[curr_r][curr_c] is not None:
                if grid[curr_r][curr_c] != val:
                    return None 
                continue 
                
            found_tile = None
            for t in temp_hand:
                if t.value == val:
                    found_tile = t
                    break
            
            if found_tile:
                found_tile.grid_pos = (curr_r, curr_c)
                found_tile.rect.x = curr_c * settings.CELL_SIZE + settings.BOARD_OFFSET_X + 1
                found_tile.rect.y = curr_r * settings.CELL_SIZE + settings.BOARD_OFFSET_Y + 1
                found_tile.on_board = True
                found_tile.update_size()
                
                tiles_to_place.append(found_tile)
                temp_hand.remove(found_tile)
            else:
                return None 

        return tiles_to_place

bot = AIPlayer()