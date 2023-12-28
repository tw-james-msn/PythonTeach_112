#
# 參考資料：https://hackmd.io/@Derek46518/HyZHsD0Qo
#

import pygame   # 遊戲模組
import sys      # 程式控制
import random   # 亂數
import time     # 

# 初始化pygame的模組(一開始固定要寫的)
pygame.init()

# 遊戲畫面寬、高
WIDTH, HEIGHT = 24, 20
# 放大比例
SCALE = 30

# 設定遊戲視窗的尺寸(size)
screen = pygame.display.set_mode((WIDTH * SCALE, HEIGHT * SCALE))
# 設定遊戲視窗的抬頭
pygame.display.set_caption('我的貪食蛇遊戲')

# 定義遊戲中使用的顏色
COLOR_RED = pygame.Color(255, 0, 0)
COLOR_GREEN = pygame.Color(27, 205, 70, 163)
COLOR_BLACK = pygame.Color(0, 0, 0)
COLOR_WHITE = pygame.Color(255, 255, 255)
COLOR_GREY = pygame.Color(150, 150, 150)

## 背景圖
background_img = pygame.image.load("2023-12-13/background.png").convert()

# 音樂出始化
pygame.mixer.init()

# 載入各種音效
pygame.mixer.music.load("2023-12-13/bgm.wav")                   # 背景音樂
pygame.mixer.music.set_volume(0.2)                              # 設定音量
fruit_sfx = pygame.mixer.Sound("2023-12-13/food.wav")           # 吃到果子的音效
game_over_sfx = pygame.mixer.Sound("2023-12-13/game_over.wav")  # 死掉的音效

# -1表示音樂無限循環播放
pygame.mixer.music.play(-1)


def theEnd():
    pygame.quit()   # 結束pygame(對應pygame.init()，結束固定要寫的)
    sys.exit()      # 結束程式 **THE END**

def gameOver(screen, score):
    '''死了，顯示分數，遊戲結束'''
    
    # 播放音效
    game_over_sfx.play()

    # for i in pygame.font.get_fonts(): print(i)    # 列出這台電腦安裝的所有字型
    # txtFont = pygame.font.SysFont('MicrosoftJhenghei', 54)  # 建立字型物件供顯示文字訊息時用
    txtFont = pygame.font.SysFont('MicrosoftJhenghei, pingfang', 54)  # 建立字型物件供顯示文字訊息時用

    # 顯示「Game Over!」文字
    # 1.產生文字圖形物件
    txtSurf = txtFont.render('你死了(Game Over)!', True, COLOR_GREY)
    # 2.取得圖形的距形物件，用來設定要顯示的位置及範圍
    txtRect = txtSurf.get_rect()    
    txtRect.midbottom = (screen.get_rect().centerx, txtFont.get_height())
    # 3.將文字圖形顯示於矩形的位置範圍
    screen.blit(txtSurf, txtRect)  

    # 同上，顯示分數
    txtSurf = txtFont.render('Score:' + str(score), True, COLOR_GREY)
    txtRect = txtSurf.get_rect()
    txtRect.midtop = (screen.get_rect().centerx, txtFont.get_height())
    screen.blit(txtSurf, txtRect)
    
    pygame.display.update()     # 更新畫面
    
    time.sleep(3)   # 程式暫停3秒

    theEnd()        # 結束程式    

def main():
    '''遊戲主程式'''

    # 建立clock時鐘物件，配合FPS控制遊戲速度用
    fpsClock = pygame.time.Clock()
    # FPS (Frame per second) 每秒顯示影格數(每秒幾楨)
    FPS = 8

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
                theEnd()    # 呼叫副程式，然後結果程式

            # 若事件類型是按鍵被按下
            if e.type == pygame.KEYDOWN:

                if e.key == pygame.K_RIGHT and direction in '上下':
                    direction = "右"
                elif e.key == pygame.K_LEFT and direction in '上下':
                    direction = "左"
                elif e.key == pygame.K_UP and direction in '左右':
                    direction = "上"
                elif e.key == pygame.K_DOWN and direction in '左右':
                    direction = "下"
                elif e.key == pygame.K_SPACE:
                    direction = ""
                    gameOver(screen, 123)

        # --事件檢查-結束-----------

        # 根據移動方向來決定新蛇頭的座標
        (x, y) = head   # 解構
        if direction == "右":
            head = (x + 1 if x < WIDTH else 0 , y)
        elif direction == "左":
            head = (x - 1 if x > 0 else WIDTH , y)
        elif direction == "上":
            head = (x, y - 1 if y > 0 else HEIGHT)
        elif direction == "下":
            head = (x, y + 1 if y < HEIGHT else 0)

        # 先在蛇身上加入新蛇頭(長度增加)
        body.insert(0, head)
        
        # 判斷是否吃掉了果子，再決定是否刪掉蛇尾
        if head != fruit:   # 沒吃到果子
            body.pop()      # 就刪掉最後面一節
        else:
            # 如果吃掉果子，得分加1
            score += 1
            # 播放音效
            fruit_sfx.play()    

            # 重新生成果子
            while fruit in body: # 檢查新產生的果子有沒有剛好在body上面
                fruit = (random.randrange(1, WIDTH-2), random.randrange(1, HEIGHT-2))
        
        # 清空、重繪pygame顯示層
        screen.fill(COLOR_BLACK)            # 塗黑全部背景
        screen.blit(background_img, (0,0))  # 顯示背景圖
        
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

        # 是否吃到自己身體
        if head in body[1:]:
            gameOver(screen, score) # 呼叫副程式，顯示分數，然後結果程式

        # 控制遊戲速度，FPS數字越大遊戲速度越快
        fpsClock.tick(FPS)

    # 遊戲迴圈 --End----------

# 現在這裡才是正式執行main這個副程式，上面def main()只是宣告一個副程式
main()


