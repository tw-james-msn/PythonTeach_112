#
# 參考資料：https://hackmd.io/@Derek46518/HyZHsD0Qo
#

import pygame   # 遊戲模組
import sys      # 程式控制
import random   # 亂數

# 初始化pygame的模組(一開始固定要寫的)
pygame.init()

# 定義頻色變數
redColor = pygame.Color(255, 0, 0)
greenColor = pygame.Color(27, 205, 70, 163)
blackColor = pygame.Color(0, 0, 0)
whiteColor = pygame.Color(255, 255, 255)
greyColor = pygame.Color(150, 150, 150)

# 遊戲畫面寬、高
WIDTH, HEIGHT = 40, 25
# 放大比例
SCALE = 20

# 設定遊戲視窗的尺寸(size)
screen = pygame.display.set_mode((WIDTH * SCALE, HEIGHT * SCALE))
# 設定遊戲視窗的抬頭
pygame.display.set_caption('我的貪食蛇遊戲')

# 設定蛇頭一開始的座標
head_x, head_y = WIDTH // 2, HEIGHT // 2
# 蛇的身體，用list(清單、陣列)來記錄每一節的座標
# 一開始身體裡只有一個「頭」
body = [].append((head_x, head_y))
# 一開始蛇要走的方向，由亂數決定
direction = random.choice('上下左右')
# 建立clock時鐘物件，遊戲速度控制用
fpsClock = pygame.time.Clock()

# 遊戲迴圈 --Begin--------
while True:

    # 控制遊戲速度，數字越大遊戲速度越快
    fpsClock.tick(5)

    # 取得所有曾發生的event(事件)
    events = pygame.event.get()

    # 一一取得所有曾發生的event(事件)來檢查
    for e in events:

        # 若事件類型是「視窗右上角x被按下」則結束遊戲
        if e.type == pygame.QUIT:
            pygame.quit()   # 結束pygame(對應pygame.init()，結束固定要寫的)
            sys.exit()      # 結束程式 **THE END**

        # 若事件類型是按鍵被按下
        if e.type == pygame.KEYDOWN:

            if e.key == pygame.K_RIGHT:
                direction = "右"
            elif e.key == pygame.K_LEFT:
                direction = "左"
            elif e.key == pygame.K_UP:
                direction = "上"
            elif e.key == pygame.K_DOWN:
                direction = "下"
            elif e.key == pygame.K_SPACE:
                direction = ""

    # --事件檢查-------------

    if direction == "右":
        head_x = head_x + 1
    elif direction == "左":
        head_x = head_x - 1
    elif direction == "上":
        head_y = head_y - 1
    elif direction == "下":
        head_y = head_y + 1

    # 清空、重繪pygame顯示層
    screen.fill(blackColor)  # 塗黑全部背景

    # 定義一個pygame的矩形物件(pygame.Rect())，等一下要用
    rect = pygame.Rect(head_x * SCALE, head_y * SCALE, SCALE, SCALE)
    # 使用rect()來畫矩形，需要指定要畫在哪裡(screen)，畫什麼顏色(greenColor)，畫的Rect物件
    pygame.draw.rect(screen, greenColor, rect)

    # 更新pygame顯示層
    pygame.display.update()

# 遊戲迴圈 --End--
