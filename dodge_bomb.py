import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))
DELTA = {
    pg.K_UP:(0,-5),
    pg.K_DOWN:(0,+5),
    pg.K_LEFT:(-5,0),
    pg.K_RIGHT:(+5,0)
}


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
     """
     引数：こうかとんRectかばくだんRect
     戻り値：タプル（横方向判定結果，縦方向判定結果）
     画面内ならTrue,画面外ならFalse
     """
     yoko, tate = True, True
     # 左右方向判定
     if rct.left < 0 or WIDTH < rct.right: # 画面外だったら
        yoko = False
     if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
     return yoko, tate

def gameover(screen: pg.Surface) -> None:
    """
     黒い画面を描画
     文字列"Game Over"を表示
     こうかとん2体を表示
     """
    bl_img = pg.Surface((WIDTH*2,HEIGHT*2)) #黒い画面を描画
    bl_img.set_alpha(200)
    pg.draw.rect(bl_img,(0, 0, 0),pg.Rect(0,0,WIDTH,HEIGHT))
    bl_rct = bl_img.get_rect()
    bl_rct.center = (WIDTH,HEIGHT)
    screen.blit(bl_img,bl_rct)

    fonto = pg.font.Font(None, 50) # 文字列表示
    txt = fonto.render("Game Over",True, (255, 255, 255))
    screen.blit(txt, [450,310])

    kk_img1 = pg.image.load("fig/8.png") # こうかとん(左)表示 
    kk_img1 = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    kk_rct1 = kk_img1.get_rect()
    kk_rct1.center = 380, 320
    screen.blit(kk_img1, kk_rct1)
    kk_img2 = pg.image.load("fig/8.png")    
    kk_img2 = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    kk_rct2 = kk_img1.get_rect()
    kk_rct2.center = 700, 320
    screen.blit(kk_img2, kk_rct2)
    pg.display.update()
    time.sleep(5)


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    clock = pg.time.Clock()
    tmr = 0
    bb_img = pg.Surface((20,20))
    pg.draw.circle(bb_img,(255,0,0),(10,10),10)
    bb_img.set_colorkey((0,0,0))
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0,WIDTH),random.randint(0,HEIGHT)
    vx,vy = +5,+5,
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0])

        if kk_rct.colliderect(bb_rct): 
        #  こうかとんが爆弾に当たったときに関数gameover()を実行
            gameover(screen)
            return
            
            

        key_lst = pg.key.get_pressed() # こうかとん移動
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
                if key_lst[key]:
                     sum_mv[0] += mv[0] 
                     sum_mv[1] += mv[1]
        kk_rct.move_ip(sum_mv)

        if check_bound(kk_rct) != (True, True): # 画面判定
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1]) # 画面内に戻す
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1

        screen.blit(kk_img, kk_rct) # こうかとん描画
        screen.blit(bb_img,bb_rct) #爆弾描画
        bb_rct.move_ip(vx,vy)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
