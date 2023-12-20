import pygame
import sys
# import random
# import os


WIDTH = 500
HEIGHT = 600

COLOR_BLACK = (0,0,0)



# 副程式
def theEnd():
  pygame.quit()
  sys.exit()

# 主程式的副程式
def main():
  
  pygame.init()

  screen = pygame.display.set_mode((WIDTH, HEIGHT))
  pygame.display.set_caption("太空生存戰")

  clock = pygame.time.Clock()
  FPS = 60

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