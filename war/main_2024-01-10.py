import pygame
import sys
import os
import random

# 切換系統資料夾為本程式所在的資料夾，以方便取用圖片、音效檔案
os.chdir(os.path.dirname(__file__))

WIDTH = 500         # 遊戲視窗高度
HEIGHT = 600        # 遊戲視窗寬度

COLOR_BLACK = (0,0,0)         # 黑色
COLOR_WHITE = (255,255,255)   # 白色
COLOR_GREEN = (0, 255, 0)     # 綠色
COLOR_RED = (255, 0, 0)       # 紅色 
COLOR_YELLOW = (255, 255, 0)  # 黃色

pygame.init()

# 設定遊戲視窗&抬頭
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("太空生存戰")

clock = pygame.time.Clock()     # 控制遊戲速度用
FPS = 60                        # 每秒幾楨畫面

# 載入圖片
## 背景圖、太空船圖
background_img = pygame.image.load("img\\background.png").convert()
player_img = pygame.image.load("img\\player.png").convert()
## 太空船縮小圖，用於「icon圖示」、「幾條命」
player_mini_img = pygame.transform.scale(player_img, (25, 19))  # 用scale()來縮放圖形
player_mini_img.set_colorkey(COLOR_BLACK)   # 設定透明色

## 設定遊戲的圖示(顯示在視窗標題上)
pygame.display.set_icon(player_mini_img)    

## 子彈的圖案
bullet_img = pygame.image.load("img\\bullet.png").convert()

## 岩石的圖
rock_imgs = [] 
for i in range(7):
    rock_imgs.append(pygame.image.load(f"img\\rock{i}.png").convert())

## 爆炸效果圖(多張圖片變成動畫效果)
expl_anim = {             # 各種爆炸的圖形總容器(字典類型)
  'lg': [],               # 大爆炸的容器(清單類型)
  'sm': [],               # 小爆炸的容器(清單類型)
  'player': []            # 太空船爆炸的容器(清單類型)
}

for i in range(9):        # 每一個物件爆炸都有9張圖(0~8)
    expl_img = pygame.image.load(f"img\\expl{i}.png").convert()          # 原圖大小
    expl_img.set_colorkey(COLOR_BLACK)                                  # 設定透明色
    expl_anim['lg'].append(pygame.transform.scale(expl_img, (75, 75)))  # 縮放原圖
    expl_anim['sm'].append(pygame.transform.scale(expl_img, (30, 30)))  # 縮放原圖
    player_expl_img = pygame.image.load(f"img\\player_expl{i}.png").convert()  # 太空船
    player_expl_img.set_colorkey(COLOR_BLACK)                                 # 設定透明色
    expl_anim['player'].append(player_expl_img)

## 寶物的圖(補血、火力)
power_imgs = {}                                                       # 各種寶物的圖形總容器(字典類型)
power_imgs['shield'] = pygame.image.load("img\\shield.png").convert()  # 補血寶物
power_imgs['gun'] = pygame.image.load("img\\gun.png").convert()        # 火力加強寶物

# 載入音效 & 音樂
pygame.mixer.init()
pygame.mixer.music.load("sound\\background.ogg")     # 背景音樂
pygame.mixer.music.set_volume(0.3)                  # 設定音量大小

shoot_sound = pygame.mixer.Sound("sound\\shoot.wav")
gun_sound = pygame.mixer.Sound("sound\\pow1.wav")
shield_sound = pygame.mixer.Sound("sound\\pow0.wav")
die_sound = pygame.mixer.Sound("sound\\rumble.ogg")

expl_sounds = [
  pygame.mixer.Sound("sound\\expl0.wav"), 
  pygame.mixer.Sound("sound\\expl1.wav")
]


#############
## 物件類別 ##
############

## 類別--Player
class Player(pygame.sprite.Sprite): # 是從Sprite繼承而來
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)   # 先執行父親的初始化，再執行下面我自己的初始化
    self.image = pygame.transform.scale(player_img, (50, 38))   # 縮放圖片大小為(寬50,高38)
    self.image.set_colorkey(COLOR_BLACK)  # 設定黑色為去背透明色
    self.rect = self.image.get_rect()     # 取得圖片的矩型物件(用來方便控制顯示位置等)
    self.rect.centerx = WIDTH / 2         # 設定太空船x軸的位置在左右中間
    self.rect.bottom = HEIGHT - 10        # 設定太空船下緣距視窗下面10點的位置
    self.speedx = 8                       # 設定太空船左右移動速度
    self.radius = 20                      # 用來偵測碰撞的圓形半徑
    self.health = 100                     # 一開始血量是100
    self.lives = 3                        # 一開始3條命
    self.hidden = False
    self.hide_time = 0
    self.gun = 1
    self.gun_time = 0
  
  def update(self):
    now = pygame.time.get_ticks()
    if self.gun > 1 and now - self.gun_time > 5000:
      self.gun -= 1
      self.gun_time = now

    if self.hidden and now - self.hide_time > 1000:
      self.hidden = False
      self.rect.centerx = WIDTH / 2
      self.rect.bottom = HEIGHT - 10
      
    # 取得按鍵被按下的狀態，並更新太空船的座標
    # 設定太空船左右移動不能超出視窗左右
    key_pressed = pygame.key.get_pressed()
    if key_pressed[pygame.K_RIGHT]:
        self.rect.right = min(WIDTH, self.rect.right + self.speedx)
    elif key_pressed[pygame.K_LEFT]:
        self.rect.left = max(0, self.rect.left - self.speedx)

  def shoot(self):
    if not(self.hidden):
      if self.gun == 1:
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot_sound.play()
      elif self.gun >=2:
        bullet1 = Bullet(self.rect.left, self.rect.centery)
        bullet2 = Bullet(self.rect.right, self.rect.centery)
        all_sprites.add(bullet1)
        all_sprites.add(bullet2)
        bullets.add(bullet1)
        bullets.add(bullet2)
        shoot_sound.play()

  def hide(self):
    self.hidden = True
    self.hide_time = pygame.time.get_ticks()
    self.rect.center = (WIDTH/2, HEIGHT+500)

  def gunup(self):
    self.gun += 1
    self.gun_time = pygame.time.get_ticks()

## 類別--Rock
class Rock(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)       # 先執行父親的初始化，再執行下面我自己的初始化
    self.new_rock()

  def new_rock(self):
    self.image_ori = random.choice(rock_imgs) # 隨機取得一個rock圖形
    self.image_ori.set_colorkey(COLOR_BLACK)  # 設定透明色
    self.image = self.image_ori.copy()
    self.rect = self.image.get_rect()
    self.rect.x = random.randrange(0, WIDTH - self.rect.width)
    self.rect.y = random.randrange(-180, -100)
    self.speedy = random.randrange(2, 5)
    self.speedx = random.randrange(-3, 3)
    self.radius = int(self.rect.width * 0.85 / 2) # 用來偵測碰撞的圓形半徑
    self.total_degree = 0
    self.rot_degree = random.randrange(-3, 3)

  def rotate(self):
    self.total_degree += self.rot_degree
    self.total_degree %= 360
    self.image = pygame.transform.rotate(self.image_ori, self.total_degree)
    center = self.rect.center
    self.rect = self.image.get_rect()
    self.rect.center = center

  def update(self):
    self.rotate()
    self.rect.y += self.speedy
    self.rect.x += self.speedx
    if (self.rect.top > HEIGHT or 
        self.rect.left > WIDTH or self.rect.right < 0):
      self.new_rock()

## 類別--Bullet
class Bullet(pygame.sprite.Sprite):
  def __init__(self, x, y):
    pygame.sprite.Sprite.__init__(self)
    self.image = bullet_img
    self.image.set_colorkey(COLOR_BLACK)
    self.rect = self.image.get_rect()
    self.rect.centerx = x
    self.rect.bottom = y
    self.speedy = -10

  def update(self):
    self.rect.y += self.speedy
    if self.rect.bottom < 0:
      self.kill()

## 類別--Explosion
class Explosion(pygame.sprite.Sprite):
  def __init__(self, center, size):
    pygame.sprite.Sprite.__init__(self)
    self.size = size
    self.frame = 0
    self.image_number = len(expl_anim[self.size])
    self.image = expl_anim[self.size][0]
    self.rect = self.image.get_rect()
    self.rect.center = center
    self.last_update = pygame.time.get_ticks()
    self.frame_rate = 50

  def update(self):
    now = pygame.time.get_ticks()
    if now - self.last_update > self.frame_rate:
      self.last_update = now
      self.frame += 1
      if self.frame == self.image_number:
        self.kill()
      else:
        self.image = expl_anim[self.size][self.frame]
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

## 類別--Power
class Power(pygame.sprite.Sprite):
  def __init__(self, center):
    pygame.sprite.Sprite.__init__(self)
    self.type = random.choice(['shield', 'gun'])
    self.image = power_imgs[self.type]
    self.image.set_colorkey(COLOR_BLACK)
    self.rect = self.image.get_rect()
    self.rect.center = center
    self.speedy = 3

  def update(self):
    self.rect.y += self.speedy
    if self.rect.top > HEIGHT:
      self.kill()

###########
## 副程式 ##
###########
    
## 副程式--結束程式
def theEnd():
  pygame.quit()
  sys.exit()

## 副程式--在遊戲畫面畫出文字(需提供參數：文字內容、x座標、y座標)
def draw_text(text, size, x, y):
    font = pygame.font.SysFont('MicrosoftJhenghei, pingfang', size)    # 建立字型物件供顯示文字訊息時用
    text_surface = font.render(text, True, COLOR_WHITE)               # 用所選字型渲染白色非鋸齒的text文字
    x -= text_surface.get_width()/2       # 修正傳入的座標x,y為文字圖形中心點
    y -= text_surface.get_height()/2
    screen.blit(text_surface, (x, y))     # 將文字的圖形畫在screen上(尚未更新到真正的螢幕上)

## 副程式--在遊戲畫面畫出太空船的血量(需提供參數：血量、x座標、y座標)
def draw_health(hp, x, y):
    if hp < 0: hp = 0 # 如果血量小於0，設為0下面程式才不會出錯
    BAR_LENGTH = 100  # 血條滿血時的寬度
    BAR_HEIGHT = 10   # 血條的高度
    fill_length = (hp/100) * BAR_LENGTH                       # 將剩下的血量轉換成長度的百分比
    fill_rect = pygame.Rect(x, y, fill_length, BAR_HEIGHT)    # 剩下的血量
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)  # 外框
    pygame.draw.rect(screen, COLOR_GREEN, fill_rect)          # 畫血，沒有框
    pygame.draw.rect(screen, COLOR_WHITE, outline_rect, 2)    # 畫框，粗細2點

## 副程式--在遊戲畫面畫出太空船還有幾條命(需提供參數：命數、x座標、y座標)
def draw_lives(lives, x, y):
    for i in range(lives):
        img_rect = player_mini_img.get_rect()   # 取得圖的大小、位置的值(物件)
        img_rect.x = x + 32 * i                 # 太空船並排效果(每次位移32點)
        img_rect.y = y
        screen.blit(player_mini_img, img_rect)

## 副程式--秀出遊戲初始說明畫面直到user按任意鍵開始玩遊戲
def draw_init():
  screen.blit(background_img, (0,0))  # 用blit()畫上背景圖片
  draw_text('太空生存戰!', 64, WIDTH/2, HEIGHT/4)
  draw_text('← →移動飛船 空白鍵發射子彈~', 22, WIDTH/2, HEIGHT/2)
  draw_text('按任意鍵開始遊戲!', 18, WIDTH/2, HEIGHT*3/4)
  pygame.display.update()             # 將畫出的文字真正的更新到顯示器上，使用者可以看到

  # 等待使用選擇下一步要做什麼的迴圈
  while True:     
    clock.tick(FPS)
    for e in pygame.event.get():      # 迭代取得所有發生的events
      if e.type == pygame.QUIT:       # 若使用者按 X 關閉遊戲那就 the end
        theEnd()
      if e.type == pygame.KEYDOWN:    # 否則若使用者隨便按了一個鍵那就
        return                        # 離開本副程式，返回主程式

## 副程式--建立一個新的Rock
def new_rock():
  r = Rock()            # 建立新的 Rock 物件實體
  rocks.add(r)          # 將rock物件實體加入 rocks sprite group
  all_sprites.add(r)    # 將rock物件實體加入 all sprite group

#############################################################
## 主程式 ##
###########
  
# 開始播放背景音樂(不停)
pygame.mixer.music.play(-1)
show_init = True  # 新遊戲

# 遊戲迴圈
while True:
  clock.tick(FPS)

  # 如果是新遊戲的話 --vvvvvv----------------------------
  if show_init:   
    # 秀出遊戲初始說明畫面，準備進入遊戲(或是離開遊戲)
    draw_init()

    # 準備各種Sprite的Group容器，方便統一一起更新
    all_sprites = pygame.sprite.Group()
    rocks = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    powers = pygame.sprite.Group()

    player = Player()           # 建立Play物件實體(instance)
    all_sprites.add(player)     # 加入 sprite總group 方便後續使用
    for i in range(8):          # 建立8個Rock物件實體，當然也會加入相對應的 sprite group
      new_rock()

    score = 0                   # 一開始得分=0分
    show_init = False
  # 新遊戲 --^^^^^^----------------------------

  # 迭代發生的所有事件
  for e in pygame.event.get():
    if e.type == pygame.QUIT:
      theEnd()
    if (e.type == pygame.KEYDOWN and 
        e.key == pygame.K_SPACE  ):
        player.shoot()    # 如果按「空白鍵」則執行Player的發射子彈副程式(shoot())

  # 更新遊戲
  all_sprites.update()    # 所有sprite group裡的sprite 都執行更新副程式(update())
  
  # 各種sprite碰撞的處理(飛船、石頭、子彈、寶物等)

  # 判斷石頭 子彈相撞
  hits = pygame.sprite.groupcollide(rocks, bullets, True, True)
  for hit in hits:
    random.choice(expl_sounds).play()
    score += hit.radius
    expl = Explosion(hit.rect.center, 'lg')
    all_sprites.add(expl)
    if random.random() > 0.9:
      pow = Power(hit.rect.center)
      all_sprites.add(pow)
      powers.add(pow)
    new_rock()

  ## 判斷石頭 飛船相撞(用圓形邊界)
  hits = pygame.sprite.spritecollide(player, rocks, True, pygame.sprite.collide_circle)
  for hit in hits:
    new_rock()
    player.health -= hit.radius * 2
    expl = Explosion(hit.rect.center, 'sm')
    all_sprites.add(expl)
    if player.health <= 0:
      death_expl = Explosion(player.rect.center, 'player')
      all_sprites.add(death_expl)
      die_sound.play()
      player.lives -= 1
      player.health = 100
      player.hide()
          
  ## 判斷寶物 飛船相撞
  hits = pygame.sprite.spritecollide(player, powers, True)
  for hit in hits:
    if hit.type == 'shield':
      player.health += 20
      if player.health > 100:
        player.health = 100
      shield_sound.play()
    elif hit.type == 'gun':
      player.gunup()
      gun_sound.play()

  if player.lives == 0 and not(death_expl.alive()):
    show_init = True

  # 畫面顯示
  screen.fill(COLOR_BLACK)
  screen.blit(background_img, (0,0))

  all_sprites.draw(screen)    # Draws all of the member sprites onto the given surface

  draw_text(str(score), 18, WIDTH/2, 10)    # 更新顯示得分
  draw_health(player.health, 5, 15)         # 更新顯示血量
  draw_lives(player.lives, WIDTH - 100, 15)  # 更新顯示幾條命

  pygame.display.update()   # 實際更新到螢幕上

# 遊戲迴圈結束