import pygame

pygame.init()
screen = pygame.display.set_mode([500, 500])
screen.fill((0, 0, 0))

class PlayerSprite(pygame.sprite.Sprite):
    def __init__(self):
        super(pygame.sprite.Sprite, self).__init__()
        self.surf = pygame.Surface((75, 25))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[pygame.K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[pygame.K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[pygame.K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[pygame.K_RIGHT]:
            self.rect.move_ip(5, 0)
            
            # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 500:
            self.rect.right = 500
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= 500:
            self.rect.bottom = 500

class Player(PlayerSprite):
    def __init__(self):
        super().__init__()
        self.health = 100
        
    def take_damage(self, damage):
        if self.health <= damage:
            self.health = 0
        else:
            self.health -= damage            

clock = pygame.time.Clock()
   
player = Player()
running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        
        elif event.type == pygame.QUIT:
            running = False
        
    pressed_keys = pygame.key.get_pressed()
    screen.blit(player.surf, player.rect)
    player.update(pressed_keys)
    pygame.display.flip()
    screen.fill((0, 0, 0))
    
pygame.quit()