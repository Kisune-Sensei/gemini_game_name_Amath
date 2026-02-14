import re
import source.settings as settings

def get_full_word_info(grid, start_r, start_c, dr, dc):
    """
    ดึงข้อมูลสมการทั้งแถว โดยไล่หาจากจุดเริ่มต้นไปจนสุดขอบทั้งสองด้าน
    คืนค่าเป็น 1. สตริงสมการ (เช่น "14-8=6") 2. รายชื่อพิกัดของเบี้ยในสมการนี้
    """
    r, c = start_r, start_c
    # ถอยหลังไปหาตัวแรกสุด
    while 0 <= r - dr < 15 and 0 <= c - dc < 15 and grid[r - dr][c - dc] is not None:
        r -= dr
        c -= dc
        
    w_str = ""
    w_pos = []
    # เดินหน้าอ่านเบี้ยทีละตัวจนหมด
    while 0 <= r < 15 and 0 <= c < 15 and grid[r][c] is not None:
        w_str += str(grid[r][c])
        w_pos.append((r, c))
        r += dr
        c += dc
        
    return w_str, w_pos

def check_math(eq_str):
    """ตรวจสอบความถูกต้องของสมการคณิตศาสตร์"""
    if '=' not in eq_str: 
        return False
        
    parts = eq_str.split('=')
    # อนุญาตให้มีเครื่องหมาย = แค่ตัวเดียว
    if len(parts) != 2: 
        return False
    
    left, right = parts
    if not left or not right: 
        return False
    
    # ป้องกันเลขที่มีศูนย์นำหน้า (เช่น 05+2=7 ถือว่าผิด ต้องเป็น 5+2=7) แต่ 0 โดดๆ ใช้ได้
    if re.search(r'\b0\d+', left) or re.search(r'\b0\d+', right):
        return False
        
    try:
        # ตรวจสอบความปลอดภัย ห้ามมีตัวอักษรแปลกปลอมนอกจากตัวเลขและเครื่องหมาย
        if not re.match(r'^[\d+\-*/]+$', left) or not re.match(r'^[\d+\-*/]+$', right):
            return False
            
        # คำนวณฝั่งซ้ายและขวาว่าเท่ากันหรือไม่
        return eval(left) == eval(right)
    except:
        # ถ้าสมการพัง (เช่น 5++2=7) จะเข้ากรณีนี้
        return False

def validate_move(placed_tiles, grid):
    """ตรวจสอบการวางเบี้ยและคิดคะแนนรวม"""
    if not placed_tiles:
        return 0, "No tiles placed"
        
    # 1. จำลองการวางเบี้ยลงบนกระดานชั่วคราว
    temp_grid = [row[:] for row in grid]
    for t in placed_tiles:
        temp_grid[t.grid_pos[0]][t.grid_pos[1]] = t.value
        
    rows = [t.grid_pos[0] for t in placed_tiles]
    cols = [t.grid_pos[1] for t in placed_tiles]
    
    is_horizontal = all(r == rows[0] for r in rows)
    is_vertical = all(c == cols[0] for c in cols)
    
    # 2. ต้องวางในแนวเดียวกัน (แถวเดียวหรือคอลัมน์เดียว)
    if not (is_horizontal or is_vertical):
        return 0, "Tiles must be placed in a single row or column"
        
    is_empty_board = all(grid[r][c] is None for r in range(15) for c in range(15))
    
    # 3. ตรวจสอบตำแหน่งการวาง
    if is_empty_board:
        # ตาแรกต้องทับช่องกลางกระดาน (7,7)
        if not any(t.grid_pos == (7, 7) for t in placed_tiles):
            return 0, "First move must cover the center STAR tile"
    else:
        # ตาต่อไปต้องเชื่อมกับเบี้ยเดิมอย่างน้อย 1 ตัว
        connected = False
        for t in placed_tiles:
            r, c = t.grid_pos
            for dr, dc in [(0,1), (1,0), (0,-1), (-1,0)]:
                nr, nc = r+dr, c+dc
                if 0 <= nr < 15 and 0 <= nc < 15 and grid[nr][nc] is not None:
                    connected = True
                    break
            if connected: break
            
        if not connected:
            return 0, "Tiles must connect to existing tiles on the board"
            
    words_to_score = []
    
    # 4. หาสมการแนวยาว (Main Word)
    if is_horizontal:
        dr, dc = 0, 1
        min_c, max_c = min(cols), max(cols)
        # ตรวจเช็คว่ามีช่องโหว่ตรงกลางหรือไม่
        for c in range(min_c, max_c + 1):
            if temp_grid[rows[0]][c] is None:
                return 0, "There is a gap in your placement"
                
        main_str, main_pos = get_full_word_info(temp_grid, rows[0], cols[0], dr, dc)
        # ---> FIX BUG: ตรวจที่จำนวนชิ้น (len) ไม่ใช่ความยาวตัวอักษร <---
        if len(main_pos) > 1 or is_empty_board:
            words_to_score.append((main_str, main_pos))
            
    if is_vertical and not (is_horizontal and len(placed_tiles) > 1):
        dr, dc = 1, 0
        min_r, max_r = min(rows), max(rows)
        for r in range(min_r, max_r + 1):
            if temp_grid[r][cols[0]] is None:
                return 0, "There is a gap in your placement"
                
        main_str, main_pos = get_full_word_info(temp_grid, rows[0], cols[0], dr, dc)
        if len(main_pos) > 1 or is_empty_board:
            words_to_score.append((main_str, main_pos))
            
    # 5. หาสมการแนวขวาง (Cross Words)
    for t in placed_tiles:
        r, c = t.grid_pos
        if is_horizontal and len(placed_tiles) > 1: 
            # ถ้าวางแนวนอน ให้เช็คแนวขวางคือแนวตั้ง
            c_str, c_pos = get_full_word_info(temp_grid, r, c, 1, 0)
            if len(c_pos) > 1: # ถ้าแนวตั้งมีเบี้ยมากกว่า 1 ตัว ถึงจะเป็นสมการขวาง
                words_to_score.append((c_str, c_pos))
                
        elif is_vertical and len(placed_tiles) > 1: 
            # ถ้าวางแนวตั้ง ให้เช็คแนวขวางคือแนวนอน
            c_str, c_pos = get_full_word_info(temp_grid, r, c, 0, 1)
            if len(c_pos) > 1:
                words_to_score.append((c_str, c_pos))
                
        elif len(placed_tiles) == 1:
            pass # ถตาวางแค่ชิ้นเดียว มันถูกเช็คทั้งสองแนวไปในข้อ 4 แล้ว

    if not words_to_score:
        return 0, "Equation must be at least 2 tiles long"
        
    # 6. ตรวจสอบความถูกต้องและคิดคะแนน
    total_score = 0
    placed_positions = [t.grid_pos for t in placed_tiles]
    
    for w_str, w_pos in words_to_score:
        if not check_math(w_str):
            return 0, f"Invalid Equation: {w_str}"
        
        # คำนวณคะแนนของสมการเส้นนี้
        word_score = 0
        word_mult = 1
        
        for r, c in w_pos:
            val = temp_grid[r][c]
            pts = settings.TILE_POINTS.get(val, 0)
            
            # โบนัสคูณคะแนนจะทำงานเฉพาะเบี้ยที่ "เพิ่งวางลงไปใหม่" เท่านั้น
            if (r, c) in placed_positions:
                if (r, c) in settings.TRIPLE_PIECE: pts *= 3
                elif (r, c) in settings.DOUBLE_PIECE: pts *= 2
                
                if (r, c) in settings.TRIPLE_EQ: word_mult *= 3
                elif (r, c) in settings.DOUBLE_EQ: word_mult *= 2
                
            word_score += pts
            
        total_score += word_score * word_mult
        
    # โบนัส BINGO! เมื่อลงเบี้ยหมดมือ 8 ตัวรวดเดียว
    if len(placed_tiles) == 8:
        total_score += 40
        
    return total_score, "Valid Equation"