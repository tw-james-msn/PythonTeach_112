import pygame
import sys
import os
import random

# 切換工作資料夾到 war 裡
if not os.getcwd().endswith('war'): os.chdir(os.path.join(os.getcwd(),'war'))

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
background_img = pygame.image.load("img/background.png").convert()
player_img = pygame.image.load("img/player.png").convert()

## 太空船縮小圖，用於「icon圖示」、「幾條命」
player_mini_img = pygame.transform.scale(player_img, (25, 19))  # 用scale()來縮放圖形
player_mini_img.set_colorkey(COLOR_BLACK)   # 設定透明色

## 設定遊戲的圖示
pygame.display.set_icon(player_mini_img)    

## 子彈的圖案
bullet_img = pygame.image.load("img/bullet.png").convert()

## 岩石的圖
rock_imgs = []
for i in range(7):
    rock_imgs.append(pygame.image.load(f"img/rock{i}.png").convert())

## 爆炸效果圖(多張圖片變成動畫效果)
expl_anim = {}            # 各種爆炸的總容器(字典類型)
expl_anim['lg'] = []      # 大爆炸的容器(清單類型)
expl_anim['sm'] = []      # 小爆炸的容器(清單類型)
expl_anim['player'] = []  # 太空船爆炸的容器(清單類型)
for i in range(9):        # 每一個物件爆炸都有9張圖(0~8)
    expl_img = pygame.image.load(f"img/expl{i}.png").convert()          # 原圖大小
    expl_img.set_colorkey(COLOR_BLACK)
    expl_anim['lg'].append(pygame.transform.scale(expl_img, (75, 75)))  # 縮放原圖
    expl_anim['sm'].append(pygame.transform.scale(expl_img, (30, 30)))  # 縮放原圖
    
    player_expl_img = pygame.image.load(f"img/player_expl{i}.png").convert()  # 太空船
    player_expl_img.set_colorkey(COLOR_BLACK)     # 透明色
    expl_anim['player'].append(player_expl_img)

## 寶物的圖(補血、火力)
power_imgs = {}
power_imgs['shield'] = pygame.image.load("img/shield.png").convert()  # 補血寶物
power_imgs['gun'] = pygame.image.load("img/gun.png").convert()        # 火力加強寶物

# 載入音效 & 音樂
pygame.mixer.init()
pygame.mixer.music.load("sound/background.ogg")
pygame.mixer.music.set_volume(0.3)

#############
## 物件類別 ##
############

## 類別--Player
class Player(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)   # 先執行父親的初始化，再執行下面我自己的初始化
    self.image = pygame.transform.scale(player_img, (50, 38))   # 縮放圖片大小為(寬50,高38)
    self.image.set_colorkey(COLOR_BLACK)  # 設定黑色為去背透明色
    self.rect = self.image.get_rect()     # 取得圖片的矩型物件(用來方便控制顯示位置等)
    self.rect.centerx = WIDTH / 2
    self.rect.bottom = HEIGHT - 10
    self.speedx = 8
    self.health = 100
    self.lives = 3
  
  def update(self):
    key_pressed = pygame.key.get_pressed()
    if key_pressed[pygame.K_RIGHT]:
        self.rect.x += self.speedx
    if key_pressed[pygame.K_LEFT]:
        self.rect.x -= self.speedx

    if self.rect.right > WIDTH:
        self.rect.right = WIDTH
    if self.rect.left < 0:
        self.rect.left = 0

  def shoot(self):
    pass

## 類別--Rock
class Rock(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)   # 先執行父親的初始化，再執行下面我自己的初始化
    self.image_ori = random.choice(rock_imgs)
    self.image_ori.set_colorkey(COLOR_BLACK)
    self.image = self.image_ori.copy()
    self.image = self.image_ori.copy()
    self.rect = self.image.get_rect()
  
  def update(self):
    pass

###########
## 副程式 ##
###########
    
## 副程式--結束程式
def theEnd():
  pygame.quit()
  sys.exit()

## 副程式--在遊戲畫面畫出文字(需提供參數：文字內容、x座標、y座標)
def draw_text(text, size, x, y):
    font = pygame.font.SysFont('MicrosoftJhenghei,pingfang', size)    # 建立字型物件供顯示文字訊息時用
    text_surface = font.render(text, True, COLOR_WHITE)               # 用所選字型渲染白色非鋸齒的text文字
    x -= text_surface.get_width()/2       # 修正傳入的座標x,y為文字圖形中心點
    y -= text_surface.get_height()/2
    screen.blit(text_surface, (x, y))     # 將文字的圖形畫在screen上(尚未更新到真正的螢幕上)

## 副程式--在遊戲畫面畫出太空船的血量(需提供參數：血量、x座標、y座標)
def draw_health(hp, x, y):
    if hp < 0:        # 如果血量小於0，設為0下面程式才不會出錯
        hp = 0
    BAR_LENGTH = 100  # 血條滿血時的寬度
    BAR_HEIGHT = 10   # 血條的高度
    fill = (hp/100) * BAR_LENGTH  # 將血量轉換成長度的百分比
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)           # 剩下的血量
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)  # 外框
    pygame.draw.rect(screen, COLOR_GREEN, fill_rect)          # 畫血，沒有框
    pygame.draw.rect(screen, COLOR_WHITE, outline_rect, 2)    # 畫框，粗細2點

## 副程式--在遊戲畫面畫出太空船還有幾條命(需提供參數：命數、圖案、x座標、y座標)
def draw_lives(lives, img, x, y):
    for i in range(lives):
        img_rect = img.get_rect()   # 取得圖的大小、位置的值(物件)
        img_rect.x = x + 32 * i
        img_rect.y = y
        screen.blit(img, img_rect)

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
  
# 開始播放背景音樂
pygame.mixer.music.play(-1)

# 新遊戲 --vvvvvv----------------------------

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

# 新遊戲 --^^^^^^----------------------------

# 遊戲迴圈
while True:
  clock.tick(FPS)

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




  # 畫面顯示
  screen.fill(COLOR_BLACK)
  screen.blit(background_img, (0,0))

  all_sprites.draw(screen)    # Draws all of the member sprites onto the given surface

  draw_text(str(score), 18, WIDTH/2, 10)    # 更新顯示得分
  draw_health(player.health, 5, 15)         # 更新顯示血量
  draw_lives(player.lives, player_mini_img, WIDTH - 100, 15)  # 更新顯示幾條命

  pygame.display.update()   # 實際更新到螢幕上

# 遊戲迴圈結束