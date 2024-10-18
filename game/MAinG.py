import pygame
import os
import random

pygame.init()

#SCreen :
SCREEN_Width = 800
SCREEN_higth = int(SCREEN_Width * 0.8)

#movement :
moving_left = False
moving_right = False
shoot = False
atk1 = False
walk_shift = False
grenade = False
grenade_thrown = False
throwGRe = False

#function:
clock = pygame.time.Clock()
fps = 60
TILE_SIZE = 40
gravity = 0.6
# mau
RED = (255,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
BLACK = (0,0,0)
#BackGround:
BG = (150,210,100)
def draw_background():
    screen.fill(BG)


#items :
bullet_image = pygame.image.load('image/player/items/bullet/bullet.png')
bullet_image = pygame.transform.scale(bullet_image , (int(bullet_image.get_width()* 1) , int(bullet_image.get_height()* 0.75)))

grenade_image = pygame.image.load('image/player/items/grenade/grenade.png')
grenade_image = pygame.transform.scale(grenade_image, (int(grenade_image.get_width()* 1) , int(grenade_image.get_height()* 0.75)))

screen = pygame.display.set_mode((SCREEN_Width,SCREEN_higth))

#screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
pygame.display.set_caption('GAME SHOOTING')

#pick up boxes 
health_box_image = pygame.image.load('image/player/items/grenade/health_box.png')
health_box_image = pygame.transform.scale(health_box_image , (int(health_box_image.get_width()* 0.5) , int(health_box_image.get_height()* 0.5)))
ammo_box_image = pygame.image.load('image/player/items/grenade/ammo_box.png')
ammo_box_image = pygame.transform.scale(ammo_box_image, (int(ammo_box_image.get_width()* 0.5) , int(ammo_box_image.get_height()* 0.5)))
grenade_box_image = pygame.image.load('image/player/items/grenade/grenade_box.png')
grenade_box_image = pygame.transform.scale(grenade_box_image, (int(grenade_box_image.get_width()* 0.5) , int(grenade_box_image.get_height()* 0.5)))

item_boxes = {
    'Health'   : health_box_image,
    'Ammo'     : ammo_box_image,
    'Grenade'  : grenade_box_image,
}

#define front
font = pygame.font.SysFont('Futura',30)

def draw_text(text,font,text_col , x , y):
    img = font.render(text,True,text_col)
    screen.blit(img,(x,y))
 
#NHAN VAT :
class Character(pygame.sprite.Sprite):
    def __init__(self, char_type , x , y , scale, speed , speed2 , ammo , grenades) :
        super().__init__()
        self.char_type = char_type
        #run:
        self.speed = speed
        #walk:
        self.speed2 = speed2
        #huong':
        self.direction = 1
        self.flip = False
        #grenade:
        self.grenades = grenades


        #heatlh:
        self.health = 100
        self.max_health = self.health

        #Ban cung :
        self.shoot_cooldown = 0
        self.ammo = ammo
        self.ammo_start = ammo

        #..:
        self.jump = False
        self._y = 0
        self.up = False
        self.alive = True

        #..
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        # các biến trong ai
        self.move_counter = 0
        self.vision = pygame.Rect(0,0,200,20)
        self.idling = False
        self.idling_counter = 0

        #.. vong lap cho cac hanh dong :
        animation_list = [ 'idle'  , 'run' , 'jump' , 'shoot' , 'atk1' , 'die' , 'hurt' , 'walk' , 'throwGRE']
        for action in animation_list:
            temp_list =[]
            number_frame = len(os.listdir(f'image//{self.char_type}/{action}'))
            for i in range(number_frame):
                image = pygame.image.load(f'image/{self.char_type}/{action}/{i}.png').convert_alpha()
                image = pygame.transform.scale(image , (int(image.get_width()* scale) , int(image.get_height()* scale)))
                temp_list.append(image)
            self.animation_list.append(temp_list)
    
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x , y)
    
    def update(self):
        self.update_animation()
        self.check_die()
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        self.ATK1

    def move(self, moving_left , moving_right , walk_shift):
        dx = 0
        dy = 0

        # di chuyen trai , phai :
        #RUN
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1
        #walk:
        #if walk_shift:
        #     dx = -self.speed2
        #     self.flip = True
        #     self.direction = -1
        # if walk_shift:
        #     dx = self.speed2
        #     self.flip = False
        #     self.direction = 1

        #di chuyen nhay :
        if self.jump == True and self.up == False:
            self._y = -10.5
            self.jump = False
            self.up = True
        self._y += gravity
        dy  += self._y
        if self.rect.bottom + dy > 363:
            dy = 363 - self.rect.bottom
            self.up = False

        self.rect.x += dx
        self.rect.y += dy
    


    def update_action(self ,new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def ai(self):
        if self.alive and Player.alive:
        
            if self.idling == False and random.randint(1,200) == 1:
                self.update_action(0)
                self.idling = True
                self.idling_counter = 50
            #kiem tra xem dich co gan nguoi choi khong
            if self.vision.colliderect(Player.rect):
                #dung chay va doi mat voi nguoi choi
                self.update_action(0)
                #shoot
                self.shoot()
            else:
                if self.idling == False:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right   
                    self.move(ai_moving_left, ai_moving_right,walk_shift)
                    self.update_action(1)
                    self.move_counter += 1
                    #cap nhat tam nhin cho dich
                    self.vision.center = (self.rect.centerx + 75 * self.direction , self.rect.centery)
                    

                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1
                else:#cho dich dung mot thoi gian r di chuyen tiep
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False

    def shoot(self): 
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20
            bullet = Bullet(self.rect.centerx * 1 + (0.75 * self.rect.size[0] * self.direction) , self.rect.centery * 1.09 ,  self.direction)
            bullet_group.add(bullet)
            self.ammo -= 1

        
    def update_animation(self):
        animation_cooldown = 100
        #animation: 
        self.image = self.animation_list[self.action][self.frame_index]
        #..
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        #
        if self.frame_index >= len(self.animation_list[self.action]):
            ##neu acton la chet thi fram dung o cuoi
            if self.action == 5 :
                self.frame_index = len(self.animation_list[self.action]) - 1
            
            #animation hurt:
            elif self.action == 6 :
                self.frame_index = 0

            #ko thi qquay lai 0
            else :
                self.frame_index = 0
        
        
            
    def check_die(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(5)
        # bien mat 1 luc sau khi chet :
    
    def ATK1(self):
        if Player.action == 4 and  pygame.sprite.spritecollide(enemies, Player):
            # Giảm máu của kẻ thù đã va chạm đi 20
            if enemies.alive:
                enemies.health -= 20
                print(enemies.health)

        

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip , False ), self.rect)

class ItemBox(pygame.sprite.Sprite):
    def __init__(self,item_type,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2 , y + (TILE_SIZE - self.image.get_height()))

    def update(self):
         # kiểm tra người chơi có nhặt được hộp k
         if pygame.sprite.collide_rect(self,Player):
             #kiểm tra xem đó là loại hộp gì
            if self.item_type == 'Health':
                 Player.health += 25
                 if Player.health > Player.max_health:
                     Player.health = Player.max_health
            elif self.item_type == 'Ammo':
                Player.ammo += 15
            elif self.item_type == 'Grenade':
                Player.grenades += 3
            # xóa hộp nếu người chơi nhặt được
            self.kill()

#Thanh mau :
class HealthBar():
    def __init__(self, x , y , health , max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health

    def draw(self,health):
        self.health = health
        # tính tỉ lệ máu còn lại:
        ratio = self.health / self.max_health
        pygame.draw.rect(screen, BLACK,(self.x - 2 , self.y - 2 , 154 , 24))
        pygame.draw.rect(screen, RED , (self.x , self.y , 150 , 20))
        pygame.draw.rect(screen , GREEN, (self.x , self.y , 150 * ratio , 20))


# DAN :
class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y,direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        if Player.direction == 1:
            self.image  = bullet_image
        elif Player.direction == -1:
            self.image = bullet_image
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.direction = direction 
    
    def update(self):
        #.. :
        self.rect.x += (self.direction * self.speed)
        # ban lan luot tung cung ten :
        if self.rect.right < 0 or self.rect.left > SCREEN_Width:
            self.kill()
        #check xem trung nhan vat k :
        if pygame.sprite.spritecollide(Player , bullet_group , False):
            if Player.alive:
                self.kill()
                Player.health -= 5
                # khi bi thuong :
                Player.update_action(6)
        
        # Kiểm tra va chạm giữa các viên đạn và kẻ thù
        collisions = pygame.sprite.groupcollide(enemy_group, bullet_group, False, True) 

        # Lặp qua các va chạm
        for enemy, bullets in collisions.items():
            if enemy.alive:  # Kiểm tra xem kẻ thù còn sống không
                for bullet in bullets:  # Xử lý từng viên đạn đã va chạm với kẻ thù
                    enemy.health -= 20  # Giảm máu của kẻ thù
                    print(f"Enemy health: {enemy.health}")
                    enemy.update_action(6)  # Cập nhật hành động khi bị thương
                        
        # Danh' thuong' :
        if Player.action == 4 and  pygame.sprite.spritecollideany(enemies, Player, False):
            # Giảm máu của kẻ thù đã va chạm đi 20
            if enemies.alive:
                enemies.health -= 20
                print(enemies.health)

# VU NO :
class Explosion(pygame.sprite.Sprite):
	def __init__(self, x, y, scale):
		pygame.sprite.Sprite.__init__(self)
		self.images = []
		for num in range(1, 5):
			img = pygame.image.load(f'image/explosion/exp{num}.png').convert_alpha()
			img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
			self.images.append(img)
		self.frame_index = 0
		self.image = self.images[self.frame_index]
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.counter = 0


	def update(self):
		EXPLOSION_SPEED = 4
		#update explosion amimation
		self.counter += 1

		if self.counter >= EXPLOSION_SPEED:
			self.counter = 0
			self.frame_index += 1
			#if the animation is complete then delete the explosion
			if self.frame_index >= len(self.images):
				self.kill()
			else:
				self.image = self.images[self.frame_index]

# BOM :
class Grenade(pygame.sprite.Sprite):
    def __init__(self, x , y , direction):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 100
        self._y = -11
        self.speed = 7
        self.image = grenade_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        self._y += gravity
        dx = self.direction * self.speed
        dy = self._y

		#check collision with floor
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.speed = 0

		#check collision with walls
        if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_Width:
            self.direction *= -1
            dx = self.direction * self.speed

		#update grenade position
        self.rect.x += dx
        self.rect.y += dy

        #countdount :
        self.timer -= 1
        if self.timer <= 0:
            self.kill()
            explosion = Explosion(self.rect.x, self.rect.y, 0.5)
            explosion_group.add(explosion)
            # giam mau' dich :
            if abs(self.rect.centerx - Player.rect.centerx) < TILE_SIZE * 2 and \
               abs(self.rect.centery - Player.rect.centery) < TILE_SIZE * 2:
               Player.health -= 50
               Player.update_action(6)
            if abs(self.rect.centerx - enemies.rect.centerx) < TILE_SIZE * 2 and \
               abs(self.rect.centery - enemies.rect.centery) < TILE_SIZE * 2:
               enemies.health -= 50
               enemies.update_action(6)
               print(enemies.health)
            

		


#
enemy_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()


#temp - create item boxes
item_box = ItemBox('Health' , 100 ,320)
item_box_group.add(item_box)
item_box = ItemBox('Ammo' , 400 , 320)
item_box_group.add(item_box)
item_box = ItemBox('Grenade' , 500 , 320)
item_box_group.add(item_box)

#.. :
Player = Character('player', 300, 300, 1.2, 3 ,2,10 , 5) 
health_bar = HealthBar(10,10,Player.health,Player.health)

enemies = Character('enemies1', 500 , 286 , 1.2 , 2, 1 ,5, 100)
enemies2 = Character('enemies1', 400 , 200 , 1.2 , 2, 1 ,5, 100)
enemy_group.add(enemies)
enemy_group.add(enemies2)



run = True
while run :
    #dieu chinh do nhay :
    clock.tick(fps)

    #tao phong man vs xoa frane anh cu:
    draw_background()
    # hien thi health nguoi choi:
    health_bar.draw(Player.health)
    #hien thi dan
    draw_text('AMMO: ' , font , WHITE , 10 , 35)
    for x in range(Player.ammo):
        screen.blit(bullet_image, (90 + (x*10), 40))

    #hien luu dan
    draw_text('GRENADES: ' , font , WHITE , 10 , 60)
    for x in range(Player.grenades):
        screen.blit(grenade_image , (135 + (x*15) ,65 ))
    #neu ko nhan vat di chuyen:
    Player.update()
    Player.draw()

    #///
    bullet_group.update()
    bullet_group.draw(screen)
    grenade_group.update()
    grenade_group.draw(screen)
    item_box_group.update()
    item_box_group.draw(screen)
    explosion_group.update()
    explosion_group.draw(screen)
    
    #ve dich:
    for enemies in enemy_group:
        enemies.ai()
        enemies.update()
        enemies.draw()

    #Nhap ban phim giup nhan vat di chuyen :
    Player.move(moving_left, moving_right , walk_shift)
    #neu Nhan Vat di chuyen :
    if Player.alive:

        # Giuong cung khi ban va khi con dan:
        if shoot and Player.ammo > 0 and moving_left == False and moving_right == False:
            Player.update_action(3)
            #khi den fram thủ thi ban cung:
            if Player.frame_index == 3 :
                Player.shoot()
        # throw grenade :
        elif throwGRe and Player.grenades > 0 :
            Player.update_action(8)
            if Player.frame_index == 8:
                if grenade and grenade_thrown == False and Player.grenades > 0:
                    grenade = Grenade(Player.rect.centerx + (1 * Player.rect.size[0] * Player.direction),\
			 			Player.rect.centery, Player.direction)
                    grenade_group.add(grenade)
			        #reduce grenades
                    Player.grenades -= 1
                    grenade_thrown = True
        elif Player.up:
            Player.update_action(2)
        elif moving_left or moving_right :
            Player.update_action(1)
        #walk:
        #elif walk_shift :
           # Player.update_action(7)  
        elif atk1:
            Player.update_action(4)
        # khi bi thuong 1 luc thi tro ve trang thai bthg :
        elif Player.action == 6:
            if Player.frame_index == 2:
                Player.update_action(0)
        else:
            Player.update_action(0)
        #Nhap ban phim giup nhan vat di chuyen :
        Player.move(moving_left, moving_right , walk_shift)

    #neu dich con song :
    if enemies.alive :
        # khi bi thuong 1 luc thi tro ve trang thai bthg :
        if enemies.action == 6:
            if enemies.frame_index == 2:
                enemies.update_action(0)
    

    for event in pygame.event.get():

        #Nhap tu ban phim:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_k:
                shoot = True
            if event.key == pygame.K_j:
                atk1 = True
            if event.key == pygame.K_SPACE or event.key == pygame.K_w:
                Player.jump = True
            if event.key == pygame.K_l:
                grenade = True
                throwGRe = True
            # if event.key == pygame.K_LSHIFT and (moving_left or moving_right):
            #     walk_shift = True
            if event.key == pygame.K_ESCAPE:
                run = False
            

        #nha phim' :
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right =  False
            if event.key == pygame.K_k:
                shoot =  False
            if event.key == pygame.K_j:
                atk1 = False
            # if event.key == pygame.K_LSHIFT and (moving_left or moving_right):
            #     walk_shift = False
            if event.key == pygame.K_l:
                grenade = False
                grenade_thrown = False
                throwGRe = False

        #quit game :
        if event.type == pygame.QUIT:
            run = False
        
    pygame.display.update()

pygame.quit()