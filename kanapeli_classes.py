import pygame, numpy, random
from pygame import mixer

#pixabay Keyframe_Audio: Winner
#Chicken Single Alarm Call

WIDTH = 700
HEIGHT = 700

APPEAR_INTERVAL = 20





class Sprite(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()

        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()

        self.rect.center = [x, y]
        

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
    
    def walk_animation(self):
        self.image = self.walk_cycle[self.animation_index]
        if self.facing_left:
            self.image = pygame.transform.flip(self.image, True, False)
            
        if self.animation_index < len(self.walk_cycle)-1:
            self.animation_index += 1
        else:
            self.animation_index = 0
    

    

class Player(Sprite):
    def __init__(self, x, y):
        super().__init__("p1_walk01.png", x, y)
        self.stand_image = self.image
        self.jump_image = pygame.image.load("p1_jump.png")
        #self.enemy_hit_cycle = [pygame.image.load(f"hit_image{i:0>2}.png") for i in range(1,5)]
        #self.fox_hit_cycle = [pygame.image.load(f"hit_fox{i:0>2}.png") for i in range(1,5)]
        #self.enemy_hit_cycle = [
            #pygame.image.load("hit_image01.png"),
            #pygame.image.load("hit_image02.png")]
        
        self.enemy_hit_image = pygame.image.load("hit_image02.png")
        self.fox_hit_image = pygame.image.load("hit_image02.png")
        
        #self.fox_hit_cycle = [
           # pygame.image.load("hit_fox01.png"),
            #pygame.image.load("hit_fox02.png"),
           # pygame.image.load("hit_fox03.png"),
           # pygame.image.load("hit_fox04.png")]
        

        
        self.walk_cycle = [pygame.image.load(f"p1_walk{i:0>2}.png") for i in range(1,5)]
        self.animation_index = 0
        self.facing_left = False
        
        self.speed = 8
        self.jumpspeed = 23
        self.vsp = 0
        self.gravity = 1
        self.min_jumpspeed = 3
        self.prev_key = pygame.key.get_pressed()
        self.last_direction = "right"
        self.last_collision_time = 0
        self.hit_sound = pygame.mixer.Sound("hit_sound.wav")
        #self.is_colliding_fox = False
        #self.is_colliding_enemy = False

        
    def jump_animation(self):
        self.image = self.jump_image
        if self.facing_left:
            self.image = pygame.transform.flip(self.image, True, False)   

            
    
    def check_collision_with_boxes(self, x, y, boxes):
        self.rect.move_ip([x, y])
        collide_boxes = pygame.sprite.spritecollide(self, boxes, False)
        self.rect.move_ip([-x, -y])
        return collide_boxes

   
    def check_collision_with_enemy(self, x, y, enemies):
        self.rect.move_ip([x, y])
        collide_enemy = pygame.sprite.spritecollide(self, enemies, False)
        if collide_enemy:
            #self.is_colliding_enemy = True
            print("terveisiä check_collision-metodista, osuma tuli kanaan")
            if self.facing_left:
                self.image = pygame.transform.flip(self.enemy_hit_image, True, False)
            else:
                self.image = self.enemy_hit_image
        self.rect.move_ip([-x, -y])
        return collide_enemy
        
            
    
    
    def check_collision_with_fox(self, x, y, foxes):
        self.rect.move_ip([x, y])
        collide_fox = pygame.sprite.spritecollide(self, foxes, False)
        self.rect.move_ip([-x, -y])
        return collide_fox


    
    def fox_hit_animation(self, foxes):
        collide_fox = self.check_collision_with_fox(0, 1, foxes)
        if collide_fox:
            if self.facing_left:
                self.image = pygame.transform.flip(self.fox_hit_image, True, False)
            else:
                self.image = self.fox_hit_image
    
    
    #def fox_hit_animation(self, foxes):
        #self.animation_update_rate = 3
        #collide_fox = pygame.sprite.spritecollide(self, foxes, False)
        #if collide_fox:
            #if self.animation_index % self.animation_update_rate == 0:
                #self.image = self.fox_hit_cycle[self.animation_index]
                #if self.facing_left:
                    #self.image = pygame.transform.flip(self.image, True, False)
            #if self.animation_index < len(self.fox_hit_cycle)-1:
                #self.animation_index += 1  
        
        
    def increase_health(self, health_bar):
        pass
    
    
    def decrease_health(self, enemies, foxes, health_bar):
        collide_enemy = self.check_collision_with_enemy(0, 1, enemies)
        collide_fox = self.check_collision_with_fox(0, 1, foxes)
        current_time = pygame.time.get_ticks()
        if collide_enemy or collide_fox:
            print("terveisiä decrease_health-metodista, osuma tuli")
            if current_time - self.last_collision_time > 1000:
                self.last_collision_time = current_time
                health_bar.hp -= 25
                print("terveisiä decrease_health-metodista, helaa lähti")
        return health_bar.hp
    
            
        
    def update(self, boxes, enemies, health_bar, foxes):
        hsp = 0 

        collide_boxes = self.check_collision_with_boxes(0, 1, boxes)
        collide_fox = self.check_collision_with_fox(0, 1, foxes)
        
        for fox in foxes:
            if collide_fox:
                self.is_colliding_fox = True
                self.fox_hit_animation(foxes)            
                self.decrease_health(enemies, foxes, health_bar)
                self.hit_sound.play()


        for enemy in enemies:
            collide_enemy = self.check_collision_with_enemy(0, 1, pygame.sprite.Group(enemy))
            
            if collide_enemy:
                if self.facing_left:
                    self.image = pygame.transform.flip(self.enemy_hit_image, True, False)
                else:
                    self.image = self.enemy_hit_image
                self.decrease_health(enemies, foxes, health_bar)
                self.hit_sound.play()

                    
                if enemy.rect.x > self.rect.x:
                    self.rect.x -= 20
                elif enemy.rect.x < self.rect.x:
                    self.rect.x += 20
                if self.rect.x <= 0:
                    enemy.rect.x += 20
                if self.rect.x >= WIDTH - self.rect.width:
                    enemy.rect.x -= 20
                

        on_ground = collide_boxes
        
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.facing_left = True
            if collide_enemy:
                self.image = pygame.transform.flip(self.enemy_hit_image, True, False)
            if collide_fox:
                self.image = pygame.transform.flip(self.fox_hit_image, True, False)
            else:
                self.walk_animation()
            hsp = -self.speed
            self.last_direction = "left"
            
        elif key[pygame.K_RIGHT]:
            self.facing_left = False
            if collide_enemy:
                self.image = self.enemy_hit_image
            if collide_fox:
                self.image = self.fox_hit_image
            if not collide_enemy and not collide_fox:
                self.walk_animation()
            hsp = self.speed
            self.last_direction = "right"
            
        else:
            if self.last_direction == "left":
                self.facing_left = True
                if collide_enemy:
                    self.image = pygame.transform.flip(self.enemy_hit_image, True, False)
                if collide_fox:
                    self.image = pygame.transform.flip(self.fox_hit_image, True, False)
                else:
                    self.image = pygame.transform.flip(self.stand_image, True, False)
                    
            elif self.last_direction == "right":
                self.facing_left = False
                if collide_enemy:
                    self.image = self.enemy_hit_image
                if collide_fox:
                    self.image = self.fox_hit_image
                else:
                    self.image = self.stand_image

        
        #prevent jumping in mid-air
        if key[pygame.K_UP] and on_ground:
            self.vsp = -self.jumpspeed
            
        #if the up arrow key was pressed in the previous loop but...
        #...is not longer pressed
        #when that happens, cut off the player's jump by reducing its speed to min_jumpspeed
        #then set self.prev_key to the current keyboard state in preparation for the next loop
        
        if self.prev_key[pygame.K_UP] and not key[pygame.K_UP]:
            if self.vsp < -self.min_jumpspeed:
                self.vsp = -self.min_jumpspeed
                
        self.prev_key = key
        
        #gravity
        if self.vsp < 10 and not on_ground:
            if collide_fox and self.last_direction == "right":
                self.image = self.fox_hit_image
            if collide_fox and self.last_direction == "left":
                self.image = pygame.transform.flip(self.fox_hit_image, True, False)
            if not collide_fox:
                self.jump_animation()
            self.vsp += self.gravity
            
            
        #stop falling when the ground is reached
        if self.vsp > 0 and on_ground:
            self.vsp = 0
            
        #movement    
        self.move(hsp,self.vsp, boxes, enemies)
        
        
    
    def move(self, x, y, boxes, enemies):
        original_pos = self.rect.topleft

        dx = x
        dy = y

    # Move in the x direction
        self.rect.move_ip([dx, 0])

    # Check for collisions with boxes in the x direction
        while self.check_collision_with_boxes(0, 0, boxes):
            self.rect.move_ip([-numpy.sign(dx), 0])

    # Check for collisions with enemies in the x direction
        while self.check_collision_with_enemy(0, 0, enemies):
            self.rect.move_ip([-numpy.sign(dx), 0])

    # Move in the y direction
        self.rect.move_ip([0, dy])

    # Check for collisions with boxes in the y direction
        while self.check_collision_with_boxes(0, 0, boxes):
            self.rect.move_ip([0, -numpy.sign(dy)])

    # Check for collisions with enemies in the y direction
        while self.check_collision_with_enemy(0, 0, enemies):
            self.rect.move_ip([0, -numpy.sign(dy)])

    # If the player is still colliding, move back to the original position
        if self.check_collision_with_boxes(0, 0, boxes) or self.check_collision_with_enemy(0, 0, enemies):
            self.rect.topleft = original_pos


    

class Enemy(Sprite):
    def __init__(self, x, y):
        super().__init__("enemy_walk01.png", x, y)
        
        
        self.walk_cycle = [pygame.image.load(f"enemy_walk{i:0>2}.png") for i in range(1, 5)]
        self.animation_index = 0
        self.facing_left = False
        self.hsp = 4
        self.rect.x = x
        self.rect.y = y
        self.direction = 1
    
    def check_collision_with_boxes(self, x, y, boxes):
        self.rect.move_ip([x, y])
        collide_boxes = pygame.sprite.spritecollide(self, boxes, False)
        self.rect.move_ip([-x, -y])
        return collide_boxes

    def check_collision_with_nests(self, x, y, nests):
        self.rect.move_ip([x, y])
        collide_nests = pygame.sprite.spritecollide(self, nests, False)
        self.rect.move_ip([-x, -y])
        return collide_nests

    

    def update(self, boxes, nests):
        
        self.rect.x += self.direction
        if self.rect.x <= 0 or self.rect.x >= WIDTH - self.rect.width:
            self.direction *= -1
        
        collide_boxes = self.check_collision_with_boxes(self.direction, 1, boxes)
        
        collide_nests = pygame.sprite.spritecollide(self, nests, False)
        
        if collide_nests:
            self.direction *= -1

        if not collide_boxes:        
            self.direction *= -1
                
           
        self.walk_animation()
        if self.direction == -1:
            self.facing_left = True
        if self.direction == 1:
            self.facing_left = False


        
class Fox(Sprite):
    def __init__(self, x, y):
        super().__init__("fox_walk01.png", x, y)
        
        self.walk_cycle = [pygame.image.load(f"fox_walk{i:0>2}.png") for i in range(1, 9)]
        self.jump_image = pygame.image.load("fox_jump.png")
        self.animation_index = 0
        self.facing_left = True
        self.hsp = 1
        self.rect.x = x
        self.rect.y = y
        self.direction = 1
        self.vsp = 0
        self.gravity = 1

    

    def check_collision_with_boxes(self, x, y, boxes):
        self.rect.move_ip([x, y])
        collide_boxes = pygame.sprite.spritecollide(self, boxes, False)
        self.rect.move_ip([-x, -y])
        return collide_boxes



    def update(self, boxes, screen):
        on_ground = self.check_collision_with_boxes(1, 0, boxes)
        collide_boxes = self.check_collision_with_boxes(0, self.vsp, boxes)
             
        if self.direction == -1:
            self.facing_left = True
        if self.direction == 1:
             self.facing_left = False
             
        if not on_ground: 
            self.image = self.jump_image
            self.rect.x += 5 
             
           #gravity
            self.vsp += self.gravity
            self.rect.y += self.vsp

            
        
        if on_ground:
            self.walk_animation()
            self.hsp = 5 
            self.rect.x += self.hsp

            
            self.vsp = 0 
        if self.rect.x >= WIDTH - self.rect.width: 
            self.kill()
    


class Box(Sprite):
    def __init__(self, x, y):
        super().__init__("box.png", x, y)



class HealthBar(Sprite):
    def __init__(self, x, y, w, h, max_hp):
        
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.hp = max_hp
        self.max_hp = max_hp
    
    def draw(self, screen):
        
        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, "red", (self.x, self.y, self.w, self.h))
        pygame.draw.rect(screen, "green", (self.x, self.y, self.w * ratio, self.h))
 

class Score():
    def __init__(self,player,eggs):
        self.score_font = pygame.font.SysFont(None,100)
        self.score = 0
    
    def update(self,player,eggs):
        collide_eggs = pygame.sprite.spritecollide(player, eggs, False)
        if collide_eggs:
            self.score += 1
        self.score_text = self.score_font.render(str(self.score), True, (0, 0, 0))

     
    
    def draw(self, screen):
        screen.blit(self.score_text, (620, 10))
        
        
    
class Egg(Sprite):
    def __init__(self, player, boxes):
        super().__init__("egg.png", 0, 0)
        self.player = player
        self.spawn_timer = 0
        self.randomize_position(boxes)


    def randomize_position(self, boxes):
        
        while True:
            x = random.randrange(WIDTH - self.rect.width)
            y = random.randrange(HEIGHT - self.rect.height)
            self.rect.x = x
            self.rect.y = y
            
            collide_boxes = pygame.sprite.spritecollide(self, boxes, False)
            collide_player = self.rect.colliderect(self.player.rect)
            if not collide_boxes and not collide_player:
                return
    
    def update(self, boxes, eggs):
        self.spawn_timer += 1

        if self.rect.colliderect(self.player.rect):
            self.kill()
        if self.spawn_timer >= APPEAR_INTERVAL * 30 or len(eggs) == 0:
            if len(eggs) != 0:
                eggs.empty()
            for i in range(5):
                egg = Egg(self.player, boxes)
                eggs.add(egg)
            self.spawn_timer = 0


class Nest(Sprite):
    def __init__(self, x, y):
        super().__init__("nest.png", x, y)
        self.x = x
        self.y = y
        
        
class Button(Sprite):
    def __init__(self):
        self.play_button = pygame.image.load("play_button.png")
        self.quit_button = pygame.image.load("quit_button.png")
        self.play_button_dark = pygame.image.load("play_button02.png")
        self.quit_button_dark = pygame.image.load("quit_button02.png")
        self.play_rect = self.play_button.get_rect(topleft=(40, 300))
        self.quit_rect = self.quit_button.get_rect(topleft=(370, 300))
        
    def draw(self, screen):
        screen.blit(self.play_button, self.play_rect.topleft)
        screen.blit(self.quit_button, self.quit_rect.topleft)
    
        
    def change_colour(self):

        if self.play_rect.collidepoint(pygame.mouse.get_pos()):
            self.play_button = self.play_button_dark
        if self.quit_rect.collidepoint(pygame.mouse.get_pos()):
            self.quit_button = self.quit_button_dark

                         
        
        
def menu():
    pygame.init()
    bg_img = pygame.image.load("background.png")
    bg_img = pygame.transform.scale(bg_img,(700,700))
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    play_button = Button()
    quit_button = Button()
    running = True

    
    while running:
        
        screen.blit(bg_img,(0,0))                     
        pygame.event.pump()
        play_button.draw(screen)
        quit_button.draw(screen)   
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if play_button.play_rect.collidepoint(pygame.mouse.get_pos()):
                play_button.change_colour()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    main_game()
            if quit_button.quit_rect.collidepoint(pygame.mouse.get_pos()):
                quit_button.change_colour()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    running = False
                    pygame.quit()
        
        

def main_game():

    pygame.init()
    bg_img = pygame.image.load("background.png")
    bg_img = pygame.transform.scale(bg_img,(700,700))
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.mixer.init()
    pygame.mixer.music.load("background_music.mp3") 
    pygame.mixer.music.play()
    clock = pygame.time.Clock()
    
    foxes = pygame.sprite.Group()

        
    player = Player(300, 400)

    #x-akseli, y-akseli, pituus, paksuus, maksimi-hp
    health_bar = HealthBar(10, 10, 100, 30, 100)
    
    enemies = pygame.sprite.Group()
    
    enemy1 = Enemy(100, 343)
    enemies.add(enemy1)

    enemy2 = Enemy(100, 113)
    enemies.add(enemy2)
    
    enemy3 = Enemy(400, 543)
    enemies.add(enemy3)
    
    enemy4 = Enemy(600, 343)
    enemies.add(enemy4)
    
    enemy5 = Enemy(400, 13)
    enemies.add(enemy5)

    
    boxes = pygame.sprite.Group()
    #1) mistä kohtaa boksit alkavat ja mihin loppuvat x-akselilla(vaakasuunta)
    #2) miten pitkälle laitetaan x-akselille
    #3) boksien etäisyys toisistaan
    #4) boksien sijoittuminen ruudulla korkeussuunnassa
    for bx in range(0,750,70):
        boxes.add(Box(bx,630))
        
    
    boxes.add(Box(100, 430)) #alarivi vas
    boxes.add(Box(30, 430))
    boxes.add(Box(170, 430))
    
    boxes.add(Box(100, 200)) #toinen rivi vas
    boxes.add(Box(30, 200))
    boxes.add(Box(170, 200))
              
    boxes.add(Box(670, 430)) #rivi oik
    boxes.add(Box(600, 430))
    boxes.add(Box(530, 430))
    
    
    boxes.add(Box(380, 290)) #yksittäinen kesk
    
    boxes.add(Box(665, 250))
    
    
    boxes.add(Box(500, 100)) #ylärivi keskellä
    boxes.add(Box(430, 100))
    boxes.add(Box(360, 100))

    
    eggs = pygame.sprite.Group()

    for egg in range(5):
        egg = Egg(player,boxes)
        eggs.add(egg)
    
    nests = pygame.sprite.Group()
    
    nest1 = Nest(185, 380)
    nests.add(nest1)
    
    nest2 = Nest(185, 150)
    nests.add(nest2)
    
    nest3 = Nest(340, 50)
    nests.add(nest3)
    
    nest4 = Nest(520, 50)
    nests.add(nest4)
    
    nest5 = Nest(515, 380)
    nests.add(nest5)
 

    score = Score(player,eggs)


    fox1_appear_time = random.randrange(6000, 8000)
    fox2_appear_time = 0
    fox3_appear_time = 0
    
    running = True
    fox1_appeared = False
    fox2_appeared = False
    fox3_appeared = False
    
    while running:
        time_now = pygame.time.get_ticks()
        screen.blit(bg_img,(0,0))                   
        pygame.event.pump()
        boxes.draw(screen)
        nests.draw(screen)
        player.update(boxes, enemies, health_bar, foxes)
        player.draw(screen)
        score.update(player,eggs)
        for enemy in enemies:
            enemy.update(boxes, nests)
            enemy.draw(screen)
        if time_now >= fox1_appear_time and fox1_appeared == False:
            fox1 = Fox(0, 280)
            foxes.add(fox1)
            fox1_appeared = True
        if fox1_appeared == True and fox2_appeared == False:
            if time_now - fox1_appear_time > 500:
                fox2_appear_time = time_now
                fox2 = Fox(0, 280)
                foxes.add(fox2)
                fox2_appeared = True
        if fox2_appeared == True and fox3_appeared == False:
            if time_now - fox2_appear_time > 1000:
                fox3_appear_time = time_now
                fox3 = Fox(0, 280)
                foxes.add(fox3)
                fox3_appeared = True
        foxes.draw(screen)
        foxes.update(boxes, screen)
        health_bar.draw(screen)
        eggs.update(boxes,eggs)
        eggs.draw(screen)
        score.draw(screen)
        
        pygame.display.flip()


        clock.tick(40)
        
        
        if player.rect.left < 0:
            player.rect.left = 0
        if player.rect.right > WIDTH:
            player.rect.right = WIDTH
        if player.rect.top <= 0:
            player.rect.top = 0
        if player.rect.bottom >= HEIGHT:
            player.rect.bottom = HEIGHT
                
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()


#if __name__ == "__main__":
    #main_game()



menu()


































