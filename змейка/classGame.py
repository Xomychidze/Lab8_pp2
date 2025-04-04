import pygame



class GameObject:
    def __init__(self, x, y, width, height, color, weight):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.weight : int = weight

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
    
    def get_weight(self):
        return self.weight
        
# Класс овтечающий за UI 
class UI: 
    def __init__(self, x, y, width, height, color, size):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text_color = (255,255,255)
        if(size == None): 
            size = 36
        self.font = pygame.font.Font(None, size)
        
        
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text_surface = self.font.render(self.count, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
    
class Button:
    def __init__(self, x, y, width, height, color, text, text_color, rounded):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.text_color = text_color
        self.font = pygame.font.Font(None, 36)
        self.rounded = rounded

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect,30, self.rounded)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)    

class UI_level(UI):
    def __init__(self, x, y, width, height, color,size, text):
        super().__init__(x, y, width, height, color, size) 
        self.text = text
        self.text_color = (255,255,255)
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
    

class UI_Count(UI): 
    def __init__(self, x, y, width, height, color,size):
        super().__init__(x, y, width, height, color, size)
        self.count = "0"
        self.num = 0
        
    def count_more(self, weight):
        self.num += weight
        self.count = f"{self.num}"
        
