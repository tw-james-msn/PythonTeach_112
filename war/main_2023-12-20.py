import pygame
import sys
import os
# import random

if not os.getcwd().endswith('war'): os.chdir(os.path.join(os.getcwd(),'war'))

WIDTH = 500         # 遊戲視窗高度
HEIGHT = 600        # 遊戲視窗寬度

COLOR_BLACK = (0,0,0)         # 黑色
COLOR_WHITE = (255,255,255)   # 白色

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("太空生存戰")

clock = pygame.time.Clock()     # 控制遊戲速度用
FPS = 60                        # 每秒幾楨畫面

# 載入圖片
background_img = pygame.image.load("img/background.png").convert()
player_img = pygame.image.load("img/player.png").convert()

# 載入音效 & 音樂
pygame.mixer.init()
pygame.mixer.music.load("sound/background.ogg")
pygame.mixer.music.set_volume(0.4)

#############
## 物件類別 ##
############

## 類別--Player
class Player(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)   # 先執行父親的初始化，再執行下面我自己的初始化
    self.img = pygame.transform.scale(player_img, (50, 38))
    
###########
## 副程式 ##
###########
    
## 副程式--結束程式
def theEnd():
  pygame.quit()
  sys.exit()

## 副程式--在遊戲畫面畫出文字(需提供參數：要顯示畫面、文字內容、x座標、y座標)
def draw_text(surf, text, size, x, y):
    font = pygame.font.SysFont('MicrosoftJhenghei,pingfang', size)   # 建立字型物件供顯示文字訊息時用
    text_surface = font.render(text, True, COLOR_WHITE)     # 用所選字型渲染白色非鋸齒的text文字
    text_rect = text_surface.get_rect()       # 取得渲染後的文字圖形(可以放入遊戲畫面的)
    text_rect.centerx = x                     # 設定文字水平軸的顯示位置(中心位置在傳入的x座標)
    text_rect.top = y                         # 設定文字水平軸的顯示位置(上方位置在傳入的y座標)
    surf.blit(text_surface, text_rect)        # 在傳入的畫面上畫上去(尚未更新到真正的螢幕上)

## 副程式--秀出遊戲初始說明畫面直到user按任意鍵開始玩遊戲
def draw_init():
  screen.blit(background_img, (0,0))    # 用blit()貼上背景圖片
  draw_text(screen, '太空生存戰!', 64, WIDTH/2, HEIGHT/4)
  draw_text(screen, '← →移動飛船 空白鍵發射子彈~', 22, WIDTH/2, HEIGHT/2)
  draw_text(screen, '按任意鍵開始遊戲!', 18, WIDTH/2, HEIGHT*3/4)
  pygame.display.update()   # 將畫出的文字真正的更新到顯示器上，使用者可以看到

  # 等待使用選擇下一步要做什麼的迴圈
  while True:     
    clock.tick(FPS)
    for e in pygame.event.get():      # 迭代取得所有發生的events
      if e.type == pygame.QUIT:       # 若使用者按 X 關閉遊戲那就 the end
        theEnd()
      if e.type == pygame.KEYDOWN:    # 否則若使用者隨便按了一個鍵那就
        return                        # 離開本副程式，返回主程式

## 副程式--產生新的rock
def new_rock():
  pass

# 主程式的副程式
def main():
  
  # 開始播放背景音樂
  pygame.mixer.music.play(-1)

  # 秀出遊戲初始說明畫面
  draw_init()

  all_sprites = pygame.sprite.Group()
  # rocks = pygame.sprite.Group()
  # bullets = pygame.sprite.Group()
  # powers = pygame.sprite.Group()

  player = Player()
  all_sprites.add(player)
  for i in range(8):
    new_rock()
  
  score = 0


  # 遊戲迴圈
  while True:
    clock.tick(FPS)

    # 取得輸入
    for e in pygame.event.get():
      if e.type == pygame.QUIT:
        theEnd()
      
    # 更新遊戲


    # 畫面顯示
      screen.fill(COLOR_BLACK)

      pygame.display.update()
  # 遊戲迴圈結束 

# 主程式的副程式結束

main() # 執行主程式副程式