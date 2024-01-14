import pygame as pg
import random as r


# 初期化処理
scale_factor = 2
chips_s = int(48 * scale_factor)

class PlayerCharacter:
    
    # コンストラクタ
    def __init__(self,init_pos,img_path):
        self.pos = pg.Vector2(init_pos)
        self.tmp_pos = pg.Vector2(init_pos)
        self.size = pg.Vector2(48,48)*scale_factor
        img_raw = pg.image.load(img_path)
        self.img = pg.transform.scale(img_raw,self.size)
    
    def tmp_move_to(self,vec):
        self.tmp_pos += vec

    def move_to(self,vec):
        self.pos += vec

    def tmp_get_dp(self):
        return self.tmp_pos * chips_s - pg.Vector2(chips_s)
    
    def get_dp(self):
        return self.pos * chips_s - pg.Vector2(chips_s)
    
    # def draw_rect(self,screen,player_pos,field_range):
    #     af_pos_vec = player_pos - pg.Vector2(2,2)
    #     if (af_pos_vec.x < field_range[0].x) or (af_pos_vec.y < field_range[0].y) :
    #         af_pos_vec.x += 1
    #         af_pos_vec.y += 1
    #     # elif (af_pos_vec.x + 2 > field_range[1].x)
    #     af_pos = af_pos_vec * chips_s
    #     pg.draw.rect(screen,(157,173,212),(af_pos.x,af_pos.y,3 *chips_s,3 * chips_s),width=0)
    
class EnemyCharacter:
    def __init__(self,init_pos,img_path):
        self.pos = pg.Vector2(init_pos)
        self.size = pg.Vector2(48,48) * scale_factor
        img_raw = pg.image.load(img_path)
        self.img = pg.transform.scale(img_raw,self.size)
    
    def get_tmp_pos(self):
        af_tmp_pos = pg.Vector2()
        af_tmp_pos.x = r.randint(-1,1)
        af_tmp_pos.y = r.randint(-1,1)
        print(af_tmp_pos)
        return af_tmp_pos

    def move(self,field_range):
        af_tmp_pos = self.get_tmp_pos()
        af_pos = self.pos + af_tmp_pos
        if (field_range[0].x <= af_pos.x <= field_range[1].x) and (field_range[0].y <= af_pos.y <= field_range[1].y):
            self.pos += af_tmp_pos
        else: self.move(field_range)
        
    def get_dp(self):
        return self.pos * chips_s - pg.Vector2(chips_s)


class PlayField:
    def __init__(self,center_pos_vec,chips_on_side,Color):
        self.center_pos_vec = center_pos_vec
        self.center_pos = self.center_pos_vec * chips_s - pg.Vector2(chips_s/2,chips_s/2)
        field_on_side = chips_on_side * chips_s
        self.field_dp_x = int(self.center_pos.x - field_on_side / 2)
        self.field_dp_y = int(self.center_pos.y - field_on_side / 2)
        self.field_ep_x = int(self.center_pos.x + field_on_side / 2)
        self.field_ep_y = int(self.center_pos.y + field_on_side / 2)
        self.grid_c = Color
        print(field_on_side / 2)
    
    def draw_grid(self,screen):
        for x in range(self.field_dp_x, self.field_ep_x + 1, chips_s):
            pg.draw.line(screen,self.grid_c,(x,self.field_dp_y),(x,self.field_ep_y))
        for y in range(self.field_dp_y, self.field_ep_y + 1, chips_s):
            pg.draw.line(screen,self.grid_c,(self.field_dp_x,y),(self.field_ep_x,y))
    
    def get_field_range(self):
        self.field_range_sp = self.center_pos_vec - pg.Vector2(1,1)
        self.field_range_ep = self.center_pos_vec + pg.Vector2(1,1)
        return self.field_range_sp,self.field_range_ep

def main():

    # 初期化処理
    pg.init()
    pg.display.set_caption('9マス鬼ごっこ')
    map_s = pg.Vector2(5,5)
    disp_w = int(chips_s * map_s.x)
    disp_h = int(chips_s * map_s.y)
    screen = pg.display.set_mode((disp_w,disp_h))
    clock = pg.time.Clock()
    font = pg.font.Font(None,50)
    frame = 0
    score = 0
    exit_flag = False
    game_over = False
    move_enable = False
    exit_code = '000'

    # グリッド設定
    grid_c = '#00aa00'
    Field_center_pos_vec = pg.Vector2(3,3) 
    # Field_center_pos = Field_center_pos_vec * chips_s - pg.Vector2(chips_s/2,chips_s/2)
    grid_on_side = 3
    showGrid = PlayField(Field_center_pos_vec,grid_on_side,grid_c)

    # プレイヤーキャラクター移動関連
    cmd_move = -1
    m_vec = [
        pg.Vector2(0,-1),
        pg.Vector2(1,0),
        pg.Vector2(0,1),
        pg.Vector2(-1,0)
    ]

    # フィールドの範囲取得
    field_range = showGrid.get_field_range()
    print(field_range)

    # キャラクターの生成、初期化
    Player = PlayerCharacter((2,3),'./data/img/player.png') # プレイヤー
    Enemy = EnemyCharacter((4,4),'./data/img/shinigami.png') # 鬼

    # ゲームループ
    while not exit_flag:

        
        
        # システムイベントの検出
        cmd_move = -1
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit_flag = True
                exit_code = '001'
            # 移動操作のキー入力受け取り
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_w:     # 上
                    cmd_move = 0
                if event.key == pg.K_d:     # 右
                    cmd_move = 1
                if event.key == pg.K_s:     # 下
                    cmd_move = 2
                if event.key == pg.K_a:     # 左
                    cmd_move = 3
                if (event.key == pg.K_RETURN) or (move_enable) :
                    return
        
        if game_over :
            screen.fill(pg.Color('#000000'))
            screen.blit(font.render("GAME OVER",False,'red'),(disp_w//2 - 100,disp_h//2 - 40))
            screen.blit(font.render(f'Score : {score}',False,'yellow'),(disp_w/2 - 100,disp_h/2))
        else :

            # 背景描画
            screen.fill(pg.Color('WHITE'))

            # Player.draw_rect(screen,Player.pos,field_range)

            # グリッド
            showGrid.draw_grid(screen)

            # ☆移動コマンド処理
            if cmd_move != -1:
                af_pos = Player.pos + m_vec[cmd_move]     # 移動後の「仮」座標
                if (field_range[0].x <= af_pos.x <= field_range[1].x) and (field_range[0].y <= af_pos.y <= field_range[1].y):
                    Player.move_to(m_vec[cmd_move])
                    Enemy.move(field_range)
                    score += 1


            # 自キャラ描画
            screen.blit(Player.img,Player.get_dp())
            screen.blit(Enemy.img,Enemy.get_dp())

            # プレイヤーと鬼が同じ場所になったかどうかの確認
            if Player.get_dp() == Enemy.get_dp() :
                print("finish")
                game_over = True

            # フレームカウンタ・キャラの位置の描画
            frame += 1
            frm_str = f'{frame:05}'
            screen.blit(font.render(frm_str,True,'BLACK'),(10,10))
            screen.blit(font.render(f'player_pos{Player.pos - pg.Vector2(1,1)}',True,'BLACK'),(10,400))
            screen.blit(font.render(f'score:{score}',True,'BLACK'),(10,440))

        # 画面の更新と同期
        pg.display.update()
        clock.tick(30)


    # ゲームループ{ここまで}
    pg.quit()
    return exit_code


if __name__ == "__main__":
    code = main()
    print(f'プログラムを「コード{code}」で終了しました。')
