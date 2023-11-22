#
# 參考資料：https://hackmd.io/@Derek46518/HyZHsD0Qo
#

import pygame   # 遊戲模組
import sys      # 程式控制
import random   # 亂數

# 初始化pygame的模組(一開始固定要寫的)
pygame.init()

# 遊戲畫面寬、高
WIDTH, HEIGHT = 40, 25
# 放大比例
SCALE = 20

# 設定遊戲視窗的尺寸(size)
screen = pygame.display.set_mode((WIDTH * SCALE, HEIGHT * SCALE))
# 設定遊戲視窗的抬頭
pygame.display.set_caption('我的貪食蛇遊戲')

# 建立clock時鐘物件，配合FPS控制遊戲速度用
fpsClock = pygame.time.Clock()
# FPS (Frame per second) 每秒顯示影格數(每秒幾楨)
FPS = 15

# 定義遊戲中使用的顏色
COLOR_RED = pygame.Color(255, 0, 0)
COLOR_GREEN = pygame.Color(27, 205, 70, 163)
COLOR_BLACK = pygame.Color(0, 0, 0)
COLOR_WHITE = pygame.Color(255, 255, 255)
COLOR_GREY = pygame.Color(150, 150, 150)


# 設定蛇頭一開始的座標(有兩個數字)
head = (WIDTH // 2, HEIGHT // 2)

# 蛇的身體，用list(清單、陣列)來記錄每一節的座標
# 一開始身體裡只有一個「頭」
body = [head]

# 一開始蛇要走的方向，由亂數決定
direction = random.choice('上下左右')

# 利用亂數設定果子座標
# 如果果子和蛇頭是相同座標，就再產生一次果子座標
fruit = head
while fruit == head: 
    fruit = (random.randrange(1, WIDTH-2), random.randrange(1, HEIGHT-2))

# 遊戲得分
score = 0

# 遊戲迴圈 --Begin--------
while True:

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
    # --事件檢查-結束-----------

    # 根據移動方向來決定新蛇頭的座標
    (x, y) = head   # 解構
    if direction == "右":
        head = (x + 1, y)
    elif direction == "左":
        head = (x - 1, y)
    elif direction == "上":
        head = (x, y - 1)
    elif direction == "下":
        head = (x, y + 1)

    # 先在蛇身上加入新蛇頭(長度增加)
    body.insert(0, head)
    
    # 判斷是否吃掉了果子，再決定是否刪掉蛇尾
    if head != fruit:
        body.pop()
    else:
        # 如果吃掉果子，則重新生成樹莓
        fruit = (random.randrange(1, WIDTH-2), random.randrange(1, HEIGHT-2))
        # 得分加1
        score += 1

    # 清空、重繪pygame顯示層
    screen.fill(COLOR_BLACK)  # 塗黑全部背景

    # 繪出蛇身體
    for (x, y) in body[1:]:
        # 定義一個pygame的矩形物件(pygame.Rect())，等一下要用
        rect = pygame.Rect(x * SCALE, y * SCALE, SCALE, SCALE)
        # 使用rect()來畫矩形，需要指定要畫在哪裡(screen)，畫什麼顏色(COLOR_GREEN)，畫的Rect物件
        pygame.draw.rect(screen, COLOR_WHITE, rect)
    
    # 繪出蛇頭(先畫身體再畫頭方能使頭吃到身體時畫面能表現出來)
    (x, y) = body[0]
    pygame.draw.rect(screen, COLOR_GREEN, pygame.Rect(x * SCALE, y * SCALE, SCALE, SCALE))
    
    # 繪出果子
    (x, y) = fruit
    pygame.draw.rect(screen, COLOR_RED, pygame.Rect(x * SCALE, y * SCALE, SCALE, SCALE))

    # 更新pygame顯示層
    pygame.display.update()
    
    # # 判斷是否死亡
    # (x, y) = head
    # if not (0 <= x < WIDTH and 0 <= y < HEIGHT):  # 如果蛇頭在X、Y軸方向沒有在視窗範圍內
    #     gameOver(screen, score)

    # # 是否吃到自己身體
    # elif head in body[1:]:
    #     gameOver(screen, score)


    # 控制遊戲速度，FPS數字越大遊戲速度越快
    fpsClock.tick(FPS)

# 遊戲迴圈 --End----------
