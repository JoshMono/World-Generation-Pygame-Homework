import pygame
import random


pygame.init()
screen_width = 512
screen_height = 512
screen = pygame.display.set_mode([screen_width, screen_height])
screen.fill((0, 0, 0))


###
### Player
###

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


###
### Blocks
###

class Block:
    def __init__(self, durablity: int, blast_protection: int, gravity_effected: bool, x: int, y: int):
        self.durablity = durablity
        self.health = durablity
        self.blast_protection = blast_protection
        self.gravity_effected = gravity_effected
        self.destroyed = False
        self.x = x
        self.y = y

    def take_damage(self, damage: int, damage_type: str):

        if damage_type == "TNT":
            damage /= self.blast_protection
            if self.health > damage:
                self.health -= damage
            else:
                self.health = 0
                self.destroyed = True
        elif damage_type == "Player":
            if self.health > damage:
                self.health -= damage
            else:
                self.health = 0
                self.destroyed = True

        print(F"Damage: {damage}")
        print(F"Health: {self.health}")

block_dict = {
        1 : pygame.image.load("iron.png"),
        2 : pygame.image.load("dirt.png"),
        3 : pygame.image.load("obsidian.png"),
        4 : pygame.image.load("sand.png")
    }

class Iron(Block):
    def __init__(self, x: int, y: int):
        super().__init__(10, 5, False, x, y)
        self.image = block_dict[1]
        
class Dirt(Block):
    def __init__(self, x: int, y: int):
        super().__init__(5, 1, False, x, y)
        self.image = block_dict[2]

class Obsidian(Block):
    def __init__(self, x: int, y: int):
        super().__init__(50, 30, False, x, y)
        self.image = block_dict[3]

class Sand(Block):
   def __init__(self, x: int, y: int):
        super().__init__(5, 1, True, x, y)
        self.image = block_dict[4]


all_blocks = [Iron, Dirt, Obsidian, Sand]


block_list = []
def generate_world(block_list: list):
    block_list = []
    for x in range(round(screen_width/64)):
        for y in range(round(screen_height/64)):
            block = all_blocks[random.randint(0,len(all_blocks)-1)]
            block_list.append(block(x*64, y*64))

    return block_list

    






            
clock = pygame.time.Clock()
   
block_list = generate_world(block_list)

player = Player()
running = True
while running:
    
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                block_list = generate_world(block_list)
        
        elif event.type == pygame.QUIT:
            running = False
        
    pressed_keys = pygame.key.get_pressed()
    screen.blit(player.surf, player.rect)
    player.update(pressed_keys)
    pygame.display.flip()
    screen.fill((0, 0, 0))
    for block in block_list:
        screen.blit(block.image, (block.x, block.y))
   
pygame.quit()