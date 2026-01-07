import pygame
from settings import *
from button import Button

import numpy as np
import os
from mapgenerator import generate_full_map_old_version

def load_map_from_txt(filename):
    if not os.path.exists(filename):
        return np.ones((156, 206), dtype=np.uint8)
    default_shape = (156, 206)
    
    try:
        map_array = []
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('#') or not line.strip():
                    continue
                row = [int(char) for char in line.strip() if char.isdigit()]
                # isdigit - checks 0-9
                # line.strip() - delete spaces and \n
                if row:
                    map_array.append(row)

        if not map_array:
            return np.zeros(default_shape, dtype=np.uint8)
            # np.zeros() - all 0 defined size
            
        return np.array(map_array, dtype=np.uint8)
    except Exception as e:
        print(f"Error loading map: {e}")
        return np.ones((156, 206), dtype=np.uint8)

class MapEditor:
    def __init__(self, surface, slot_index):
        self.surface = surface
        self.slot_index = slot_index
        self.filename = f"./data/slot{slot_index}.txt"
        self.visible = False
        
        self.map_data = load_map_from_txt(self.filename)
        self.tile_size = 32 

        self.tile_sprites = {}
        paths = {
            1: TILE_IMAGE_PATH,
            2: DIRT_IMAGE_PATH,
            3: BLUE_SPHERE_PATH,
            4: STONE_ROCK_PATH,
            5: GEM_IMAGE_PATH,
            6: TRAP_IMAGE_PATH
        }
        
        for key, path in paths.items():
            img = pygame.image.load(path).convert_alpha()
            self.tile_sprites[key] = pygame.transform.scale(img, (self.tile_size, self.tile_size))
            
        self.offset_x = 0
        self.offset_y = 0
        self.selected_type = 1 
        self.palette = [0, 1, 2, 3, 4, 5, 6] 
        
        self.small_font = pygame.font.Font(FONT_PATH, 16)

        self.zoom_level = 1.0  
        self.min_zoom = 0.2    
        self.max_zoom = 3.0    
        self.base_tile_size = 32 


    def save_and_exit(self):
        try:
            h, w = self.map_data.shape
            with open(self.filename, 'w', encoding='utf-8') as f:
                f.write(f"# Map Size (H x W): {h} x {w}\n")
                for row in self.map_data:
                    line = "".join(map(str, row))
                    f.write(line + "\n")
            # print(self.filename)
        except Exception as e:
            print(f"Save error: {e}")

    def handle_event(self, event):
        if not self.visible: return None

        #маштаб
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4: 
                self.zoom_level = min(self.max_zoom, self.zoom_level + 0.1)
            elif event.button == 5: 
                self.zoom_level = max(self.min_zoom, self.zoom_level - 0.1)
            
            self.tile_size = int(self.base_tile_size * self.zoom_level)

        if pygame.mouse.get_pressed()[0]:
            mx, my = pygame.mouse.get_pos()
            if my < WINDOW_HEIGHT - 80:
                gx = (mx - self.offset_x) // self.tile_size
                gy = (my - self.offset_y) // self.tile_size
                if 0 <= gy < self.map_data.shape[0] and 0 <= gx < self.map_data.shape[1]:
                    self.map_data[gy, gx] = self.selected_type

        #рух карти
        if pygame.mouse.get_pressed()[2]:
            rel_x, rel_y = pygame.mouse.get_rel()
            self.offset_x += rel_x
            self.offset_y += rel_y
        else:
            pygame.mouse.get_rel()

        #вибір типу
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            if my > WINDOW_HEIGHT - 80:
                for i, t in enumerate(self.palette):
                    # enumerate() - index and value
                    px = 50 + i * 60
                    rect = pygame.Rect(px, WINDOW_HEIGHT - 60, 40, 40)
                    if rect.collidepoint(mx, my):
                        self.selected_type = t
                        return None

        if event.type == pygame.KEYDOWN:
            if pygame.K_1 <= event.key <= pygame.K_7:
                self.selected_type = self.palette[event.key - pygame.K_1]
            if event.key == pygame.K_ESCAPE:
                self.save_and_exit()
                return "back_to_levels"
        return None
    
    def draw(self):
        self.surface.fill((15, 15, 15))

        current_size = self.tile_size
        
        start_gx = max(0, -self.offset_x // current_size)
        start_gy = max(0, -self.offset_y // current_size)
        end_gx = min(self.map_data.shape[1], (WINDOW_WIDTH - self.offset_x) // current_size + 1)
        end_gy = min(self.map_data.shape[0], (WINDOW_HEIGHT - 80 - self.offset_y) // current_size + 1)

        for y in range(start_gy, end_gy):
            for x in range(start_gx, end_gx):
                val = self.map_data[y, x]
                pos = (x * current_size + self.offset_x, y * current_size + self.offset_y)
                
                if val == 0:
                    pygame.draw.rect(self.surface, (40, 40, 40), (pos[0], pos[1], current_size, current_size), 1)
                elif val in self.tile_sprites:
                    scaled_sprite = pygame.transform.scale(self.tile_sprites[val], (current_size, current_size))
                    self.surface.blit(scaled_sprite, pos)

        #нижка панель
        pygame.draw.rect(self.surface, (40, 40, 40), (0, WINDOW_HEIGHT - 80, WINDOW_WIDTH, 80))
        for i, t in enumerate(self.palette):
            px = 50 + i * 60
            py = WINDOW_HEIGHT - 60
            rect = pygame.Rect(px, py, 40, 40)
            
            if t == 0:
                pygame.draw.rect(self.surface, (20, 20, 20), rect)
            elif t in self.tile_sprites:
                icon = pygame.transform.scale(self.tile_sprites[t], (40, 40))
                self.surface.blit(icon, (px, py))
            
            if t == self.selected_type:
                pygame.draw.rect(self.surface, (221, 247, 244), rect, 3)

class LevelsMenu:
    def __init__(self, surface: pygame.Surface):
        self.surface = surface
        self.visible = False
        self.bg_color = (20, 20, 20)
        
        self.current_editor = None
        self.selected_slot = 0

        self.button_image = pygame.image.load(BUTTON_IMAGE_PATH).convert_alpha()
        self.doc_image = pygame.image.load(DOC_IMAGE_PATH).convert_alpha()
        self.doc_image = pygame.transform.scale(self.doc_image, (96, 96))
        
        self.font = pygame.font.Font(FONT_PATH, 32)
        self.small_font = pygame.font.Font(FONT_PATH, 20)
        
        self._result = None
        
        self.slots = []
        slot_w, slot_h = 96, 96
        spacing = 20
        start_x = (WINDOW_WIDTH - (5 * slot_w + 4 * spacing)) // 2
        start_y = WINDOW_HEIGHT // 2 - 100
        
        for i in range(5):
            rect = pygame.Rect(start_x + i * (slot_w + spacing), start_y, slot_w, slot_h)

            btn = Button(
                rect=rect, 
                image=pygame.transform.scale(self.button_image, (slot_w, slot_h)),
                callback=lambda idx=i: self._set_selected_slot(idx)
            )
            self.slots.append(btn)
            
        edit_btn_w, edit_btn_h = 192, 48
        self.editor_btn = Button(
            rect=(WINDOW_WIDTH // 2 - edit_btn_w // 2, WINDOW_HEIGHT - 128, edit_btn_w, edit_btn_h),
            image=pygame.transform.scale(self.button_image, (edit_btn_w, edit_btn_h)),
            callback=self._on_editor
        )

        self.back_btn = Button(
            rect=(WINDOW_WIDTH // 2 - edit_btn_w // 2, WINDOW_HEIGHT - 64, edit_btn_w, edit_btn_h),
            image=pygame.transform.scale(self.button_image, (edit_btn_w, edit_btn_h)),
            callback=self._on_back
        )

        self.start_level_btn = Button(
            rect=(WINDOW_WIDTH // 2 - edit_btn_w // 2, WINDOW_HEIGHT - 192, edit_btn_w, edit_btn_h),
            image=pygame.transform.scale(self.button_image, (edit_btn_w, edit_btn_h)),
            callback=self._on_start_level
        )

        self.generate_img = pygame.image.load(GEN_ICON_PATH).convert_alpha()
        self.generate_img = pygame.transform.scale(self.generate_img, (32, 32))

        self.gen_btn = Button(
            rect=(WINDOW_WIDTH - 64, 64, 32, 32),
            image=self.generate_img,
            callback=self._on_generate_new
        )

        self.clear_img = pygame.image.load(CLEAR_ICON_PATH).convert_alpha()
        self.clear_img = pygame.transform.scale(self.clear_img, (32, 32))

        self.clear_btn = Button(
            rect=(WINDOW_WIDTH - 110, 64, 32, 32),
            image=self.clear_img,
            callback=self._on_clear_slot
        )

    def _set_selected_slot(self, index):
        self.selected_slot = index

    def _on_editor(self):
        self.current_editor = MapEditor(self.surface, self.selected_slot)
        self.current_editor.visible = True
    
    def _on_back(self):
        self._result = {"action": "back"}

    def _on_start_level(self):
        self._result = {"action": "load", "slot": self.selected_slot}

    def handle_event(self, event):
        if not self.visible: return None
        
        if self.current_editor and self.current_editor.visible:
            res = self.current_editor.handle_event(event)
            if res == "back_to_levels":
                self.current_editor.visible = False
                self.current_editor = None
            return None
        
        if self.clear_btn.handle_event(event): return None
        if self.gen_btn.handle_event(event): return None
        if self.editor_btn.handle_event(event): return None
        if self.back_btn.handle_event(event):
            res = self._result
            self._result = None
            return res
        if self.start_level_btn.handle_event(event):
            res = self._result
            self._result = None
            return res 
            
        for btn in self.slots:
            btn.handle_event(event)
            
        return None

    def draw(self):
        if not self.visible: return
        
        if self.current_editor and self.current_editor.visible:
            self.current_editor.draw()
            return

        self.surface.fill(self.bg_color)
        
        title_surf = self.font.render("MAP EDITOR", True, (221, 247, 244))
        title_rect = title_surf.get_rect(center=(WINDOW_WIDTH // 2, 80))
        self.surface.blit(title_surf, title_rect)
        
        for i, btn in enumerate(self.slots):
            if i == self.selected_slot:
                pygame.draw.rect(self.surface, (221, 247, 244), btn.rect.inflate(10, 10), 3)
            
            doc_rect = self.doc_image.get_rect(center=btn.rect.center)
            self.surface.blit(self.doc_image, doc_rect)
            
            label = "From game" if i == 0 else f"Slot {i}"
            label_surf = self.small_font.render(label, True, (221, 247, 244))
            label_rect = label_surf.get_rect(midtop=(btn.rect.centerx, btn.rect.bottom + 10))
            self.surface.blit(label_surf, label_rect)
        
        self.gen_btn.draw(self.surface)
        gen_icon_rect = self.generate_img.get_rect(center=self.gen_btn.rect.center)
        self.surface.blit(self.generate_img, gen_icon_rect)

        self.clear_btn.draw(self.surface)
        clear_icon_rect = self.clear_img.get_rect(center=self.clear_btn.rect.center)
        self.surface.blit(self.clear_img, clear_icon_rect)

        self.start_level_btn.draw(self.surface)
        start_text = self.font.render("Start Game", True, (221, 247, 244))
        self.surface.blit(start_text, start_text.get_rect(center=self.start_level_btn.rect.center))

        self.editor_btn.draw(self.surface)
        edit_text = self.font.render("Open Editor", True, (221, 247, 244))
        self.surface.blit(edit_text, edit_text.get_rect(center=self.editor_btn.rect.center))

        self.back_btn.draw(self.surface)
        back_text = self.font.render("Back", True, (221, 247, 244))
        self.surface.blit(back_text, back_text.get_rect(center=self.back_btn.rect.center))


    def _on_generate_new(self):
        new_map = generate_full_map_old_version(width=206, height=156)
        
        filename = f"./data/slot{self.selected_slot}.txt"
        
        try:
            if not os.path.exists("./data"): os.makedirs("./data")
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"# Generated Map {self.selected_slot}\n")
                for row in new_map:
                    f.write("".join(map(str, row)) + "\n")
        except Exception as e:
            print(f"Gen save error: {e}")


    def _on_clear_slot(self):
        """Заповнює поточний слот порожнечею (нулями)"""
        filename = f"./data/slot{self.selected_slot}.txt"
        default_shape = (156, 206)
        empty_map = np.zeros(default_shape, dtype=np.uint8)
        
        try:
            if not os.path.exists("./data"): os.makedirs("./data")
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"# Empty Map {self.selected_slot}\n")
                for row in empty_map:
                    f.write("".join(map(str, row)) + "\n")
            # print(self.selected_slot)
        except Exception as e:
            print(f"Clear error: {e}")