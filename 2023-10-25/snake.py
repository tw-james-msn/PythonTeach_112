import pygame


pygame.init() # 初始化pygame的模組(一開始固定要寫的)


screen = pygame.display.set_mode((800,600))  # 遊戲視窗的寬(800)、高(600)

pygame.display.set_caption('我的貪食蛇遊戲') # 遊戲視窗的抬頭

running = True  # 控制遊戲迴圈的變數
# 遊戲迴圈 --Begin--------
while running:

  # 一一取得所有曾發生的event(事件)來檢查
  for event in pygame.event.get():  

    if event.type == pygame.QUIT: # 按視窗右上角x的事件
      running = False   # 離開遊戲迴圈 while running
      break             # 離開 for event 迴圈

    # 檢查其它事件
    #  .
    #  .
    #  .

  #--事件檢查-------------


# 遊戲迴圈 --End--

pygame.quit() # 結束 pygame模組(結束固定要寫的)