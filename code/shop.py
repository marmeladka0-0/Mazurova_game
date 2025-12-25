import pygame

from settings import *
from button import Button

class ShopMenu:
    def __init__(self, surface, nickname_input):
        self.surface = surface
        self.nickname_input = nickname_input
        self.visible = False
        self.font = pygame.font.Font(FONT_PATH, 20)
        self.title_font = pygame.font.Font(FONT_PATH, 36)
        
        button_image = pygame.image.load(BUTTON_IMAGE_PATH).convert_alpha()
        
        skin_img = pygame.image.load(PLAYER_IMAGE_PATH).convert_alpha()
        self.skin_preview1 = pygame.transform.scale(skin_img, (96, 87))
        skin_img = pygame.image.load(PLAYER_IMAGE_PATH2).convert_alpha()
        self.skin_preview2 = pygame.transform.scale(skin_img, (96, 87))
        skin_img = pygame.image.load(PLAYER_IMAGE_PATH3).convert_alpha()
        self.skin_preview3 = pygame.transform.scale(skin_img, (96, 87))

        self.owned_skins = int(nickname_input.game_data["skins"])
        self.selected_skin = nickname_input.game_data.get("selected_skin", 0)
        # print(self.owned_skins)
        self.skins = [
            {"name": "Basic", "price": 0, "owned": True, "image": self.skin_preview1,"selected": self.selected_skin == 0},
            {"name": "Bubble", "price": 50, "owned": self.owned_skins % 2 == 1, "image": self.skin_preview2, "selected": self.selected_skin == 1},
            {"name": "Green", "price": 150, "owned": self.owned_skins >= 2, "image": self.skin_preview3, "selected": self.selected_skin == 2}
        ]
        
        self.current_coins = 0
        
        card_w = 180
        card_h = 240
        spacing = 20

        start_x = (WINDOW_WIDTH - (card_w * 3 + spacing * 2)) // 2
        
        self.buttons = []

        for i in range(len(self.skins)):

            btn_x = start_x + i * (card_w + spacing) + (card_w - 140) // 2
            btn_y = FRAME_THICKNESS + 360
            
            btn = Button(
                rect=(btn_x, btn_y, 140, 40),
                image=pygame.transform.scale(button_image, (140, 40)),
                callback=lambda idx=i: self._buy_skin(idx)
            )
            self.buttons.append(btn)


        self.back_btn = Button(
            rect=(WINDOW_WIDTH // 2 - 80, WINDOW_HEIGHT - 60, 160, 40),
            image=pygame.transform.scale(button_image, (160, 40)),
            callback=self.hide
        )

    def _buy_skin(self, index):
        skin = self.skins[index]

        if skin["owned"]:
            for i, s in enumerate(self.skins):
                s["selected"] = (i == index)

            self.selected_skin = index
            self.nickname_input.game_data["selected_skin"] = index
            return True

        if self.current_coins < skin["price"]:
            return False

        self.current_coins -= skin["price"]
        skin["owned"] = True

        if index == 1:
            self.owned_skins = self.owned_skins + 1
        if index == 2:
            self.owned_skins = self.owned_skins + 2

        self.nickname_input.game_data["skins"] = self.owned_skins
        self.nickname_input.game_data["gems"] = self.current_coins

        for i, s in enumerate(self.skins):
            s["selected"] = (i == index)

        self.selected_skin = index
        self.nickname_input.game_data["selected_skin"] = index or 0

        return True

    def handle_event(self, event, player_coins):
        if not self.visible: return None
        self.current_coins = player_coins
        
        if self.back_btn.handle_event(event): return {"action": "back", "gems": self.current_coins,}
        
        for i, btn in enumerate(self.buttons):
            if btn.handle_event(event):
                if self._buy_skin(i):
                    return {"action": "buy", "gems": self.current_coins, "skin_index": i}
        return None

    def draw(self, player_coins):
        if not self.visible: return
        self.current_coins = player_coins

        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT + FRAME_THICKNESS))
        overlay.set_alpha(200)
        overlay.fill((20, 20, 20))
        self.surface.blit(overlay, (0, 0))

        title = self.title_font.render("SHOP", True, (221, 247, 244))
        self.surface.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, FRAME_THICKNESS + 20))
        
        coins_text = self.font.render(f"Gems: {self.current_coins}", True, (221, 247, 244))
        self.surface.blit(coins_text, (WINDOW_WIDTH // 2 - coins_text.get_width() // 2, FRAME_THICKNESS + 70))

        card_w, card_h = 180, 240
        spacing = 20
        start_x = (WINDOW_WIDTH - (card_w * 3 + spacing * 2)) // 2

        for i, skin in enumerate(self.skins):
            x = start_x + i * (card_w + spacing)
            y = FRAME_THICKNESS + 110
            
            card_rect = pygame.Rect(x, y, card_w, card_h)
            pygame.draw.rect(self.surface, (116, 167, 65), card_rect, border_radius=15)
            pygame.draw.rect(self.surface, (182, 213, 60), card_rect, 2, border_radius=15)
            
            name_surf = self.font.render(skin["name"], True, (116, 167, 65))
            self.surface.blit(name_surf, (card_rect.centerx - name_surf.get_width() // 2, y + 20))

            skin_rect = skin["image"].get_rect(center=(card_rect.centerx, y + 110))
            self.surface.blit(skin["image"], skin_rect)

            status = f"Price: {skin['price']}" if not skin["owned"] else "OWNED"
            color = (221, 247, 244) if not skin["owned"] else (221, 247, 244)
            status_surf = self.font.render(status, True, color)
            self.surface.blit(status_surf, (card_rect.centerx - status_surf.get_width() // 2, y + 200))

            self.buttons[i].draw(self.surface)
            btn_txt = "Selected" if skin["selected"] else "Select" if skin["owned"] else "Buy"
            txt_surf = self.font.render(btn_txt, True, (221, 247, 244))
            self.surface.blit(txt_surf, (self.buttons[i].rect.centerx - txt_surf.get_width() // 2, self.buttons[i].rect.centery - 10))

        self.back_btn.draw(self.surface)
        back_surf = self.font.render("Back", True, (221, 247, 244))
        self.surface.blit(back_surf, (self.back_btn.rect.centerx - back_surf.get_width() // 2, self.back_btn.rect.centery - 10))

    def show(self): self.visible = True
    def hide(self): self.visible = False