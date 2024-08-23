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
        self.surf = pygame.Surface((25, 75))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.jump = False
        self.gravity = 1
        self.velocity = 12
        self.current_scene = 0

    def update(self, pressed_keys):
        if self.jump:
            self.rect.move_ip(0, -1*self.velocity)
            self.velocity -= self.gravity
        
        
        elif pressed_keys[pygame.K_w] and not self.jump:
            self.rect.move_ip(0, -5)
            self.jump = True
            

        if pressed_keys[pygame.K_a]:
            self.rect.move_ip(-5, 0)
            


        if pressed_keys[pygame.K_d]:
            self.rect.move_ip(5, 0)
            
            # Keep player on the screen
        if self.rect.left < 0:
            self.rect.right = screen_width
            self.next_scene("Left")

        if self.rect.right > screen_width:
            self.rect.left = 0
            self.next_scene("Right")

        if self.rect.top <= 0:
            self.rect.top = 0

        if self.rect.bottom >= screen_height/2:
            self.rect.bottom = screen_height/2
            self.jump = False
            self.gravity = 1
            self.velocity = 12
            
        elif not self.jump:
            self.rect.move_ip(0, self.gravity)
            self.gravity += 0.5

    def next_scene(self, direction):
        if direction == "Left":
            if self.current_scene - 1 in world_dict:
                self.current_scene -= 1
                world_dict[self.current_scene]

            else:
                self.current_scene -= 1
                block_list = []
                block_list = generate_world(block_list)
                world_dict[self.current_scene] = block_list

        else:
            if self.current_scene + 1 in world_dict:
                self.current_scene += 1
                world_dict[self.current_scene]

            else:
                self.current_scene += 1
                block_list = []
                block_list = generate_world(block_list)
                world_dict[self.current_scene] = block_list

           

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
        4 : pygame.image.load("sand.png"),
        5 : pygame.image.load("grass.png")
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

class Grass(Block):
   def __init__(self, x: int, y: int):
        super().__init__(5, 1, False, x, y)
        self.image = block_dict[5]


all_blocks = [Iron, Dirt, Obsidian, Sand]


block_list = []

# Generates World Terrain
def generate_world(block_list: list):
    block_list = []
    for x in range(round(screen_width/64)):
        for y in range(round(screen_height/64/2)):
            if y == 0:
                block_list.append(Grass(x*64, y*64+screen_height/2))
            else:
                block = all_blocks[random.randint(0,len(all_blocks)-1)]
                block_list.append(block(x*64, y*64+screen_height/2))

    return block_list

            
world_dict = {}


clock = pygame.time.Clock()
block_list = generate_world(block_list)

world_dict[0] = block_list

player = Player()
running = True
while running:
    print(world_dict.keys())
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                world_dict.clear()
                world_dict[0] = generate_world(block_list)
                player.current_scene = 0
        
        elif event.type == pygame.QUIT:
            running = False
        
    pressed_keys = pygame.key.get_pressed()
    screen.blit(player.surf, player.rect)
    player.update(pressed_keys)
    pygame.display.flip()
    screen.fill((50, 157, 168))
    for block in world_dict[player.current_scene]:
        screen.blit(block.image, (block.x, block.y))
   
pygame.quit()