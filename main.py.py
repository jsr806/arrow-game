import pygame
import sys
import random

pygame.init()

# ---------- 基础常量 ----------
GRID_W = 5
GRID_H = 5
CELL_SIZE = 80
MARGIN_TOP = 100
MARGIN_LEFT = 50
WIDTH = MARGIN_LEFT * 2 + GRID_W * CELL_SIZE
HEIGHT = MARGIN_TOP + GRID_H * CELL_SIZE + 100
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("一箭又一箭")
clock = pygame.time.Clock()
FPS = 60

# 字体
FONT = pygame.font.SysFont("simhei", 36)
BIG_FONT = pygame.font.SysFont("simhei", 50)

# 颜色
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GRAY = (160,160,160)
RED = (220, 30, 30)
GREEN = (30,170,30)
LIGHT_BLUE = (230,245,255)

# 游戏状态
STATE_START = "start"
STATE_PLAY = "play"
STATE_WIN = "win"
STATE_LOSE = "lose"

# 方向定义
DIR_CHAR = {
    "up": "↑",
    "down": "↓",
    "left": "←",
    "right": "→"
}
DIR_DELTA = {
    "up": (0, -1),
    "down": (0, 1),
    "left": (-1, 0),
    "right": (1, 0)
}

# 3个可通关关卡 (x,y,direction)
LEVELS = [
    [
        (0, 0, "right"),
        (2, 0, "down"),
        (2, 4, "right"),
        (4, 4, "up")
    ],
    [
        (0, 1, "down"),
        (1, 2, "right"),
        (3, 1, "left"),
        (4, 3, "up"),
        (2, 2, "down")
    ],
    [
        (0, 0, "down"),
        (1, 1, "right"),
        (3, 0, "down"),
        (4, 2, "left"),
        (2, 3, "right"),
        (0, 4, "right")
    ]
]


class Arrow:
    def __init__(self, grid_x, grid_y, dire):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.dire = dire
        self.shake = 0
        # 飞行动画
        self.flying = False
        self.px = MARGIN_LEFT + grid_x * CELL_SIZE + CELL_SIZE//2
        self.py = MARGIN_TOP + grid_y * CELL_SIZE + CELL_SIZE//2
        self.fly_dx, self.fly_dy = DIR_DELTA[dire]

    def start_fly(self):
        self.flying = True

    def update(self):
        if self.flying:
            speed = 8
            self.px += self.fly_dx * speed
            self.py += self.fly_dy * speed
        if self.shake > 0:
            self.shake -= 1

    def is_out(self):
        # 判断箭头飞出窗口
        return self.px < 0 or self.px > WIDTH or self.py <0 or self.py>HEIGHT

    def draw(self):
        offset_x, offset_y = 0, 0
        color = BLACK
        if self.shake > 0:
            offset_x = random.randint(-3,3)
            offset_y = random.randint(-3,3)
            color = RED
        text = FONT.render(DIR_CHAR[self.dire], True, color)
        rect = text.get_rect(center=(self.px + offset_x, self.py + offset_y))
        screen.blit(text, rect)


class Game:
    def __init__(self):
        self.state = STATE_START
        self.level_idx = 0
        self.max_mistake = 3
        self.mistake = 0
        self.arrows = []

    def load_level(self, idx):
        self.level_idx = idx
        self.mistake = 0
        self.arrows = []
        level_data = LEVELS[idx]
        for x,y,d in level_data:
            self.arrows.append(Arrow(x,y,d))

    def get_arrow_at_grid(self, gx, gy):
        for arr in self.arrows:
            if arr.grid_x == gx and arr.grid_y == gy and not arr.flying:
                return arr
        return None

    def check_can_fly(self, arrow:Arrow):
        dx, dy = DIR_DELTA[arrow.dire]
        cx = arrow.grid_x + dx
        cy = arrow.grid_y + dy
        while 0 <= cx < GRID_W and 0 <= cy < GRID_H:
            if self.get_arrow_at_grid(cx, cy):
                return False
            cx += dx
            cy += dy
        return True

    def on_click_grid(self, mx, my):
        gx = (mx - MARGIN_LEFT) // CELL_SIZE
        gy = (my - MARGIN_TOP) // CELL_SIZE
        if not (0 <= gx < GRID_W and 0 <= gy < GRID_H):
            return
        clicked_arrow = self.get_arrow_at_grid(gx, gy)
        if clicked_arrow is None:
            return

        if self.check_can_fly(clicked_arrow):
            # ✅ 可以飞出，启动动画
            clicked_arrow.start_fly()
        else:
            # ❌ 被阻挡，抖动+扣失误
            clicked_arrow.shake = 22
            self.mistake += 1
            if self.mistake >= self.max_mistake:
                self.state = STATE_LOSE

    def update_all(self):
        # 更新所有箭头，删除飞出屏幕的箭头
        for arr in self.arrows[:]:
            arr.update()
            if arr.flying and arr.is_out():
                self.arrows.remove(arr)
        # 检查通关：棋盘内静止箭头数量为0
        remain = [a for a in self.arrows if not a.flying]
        if len(remain) == 0 and self.state == STATE_PLAY:
            self.state = STATE_WIN

    def draw_grid(self):
        # 绘制网格
        for x in range(GRID_W + 1):
            pygame.draw.line(screen, GRAY,
                (MARGIN_LEFT + x*CELL_SIZE, MARGIN_TOP),
                (MARGIN_LEFT + x*CELL_SIZE, MARGIN_TOP + GRID_H*CELL_SIZE),2)
        for y in range(GRID_H +1):
            pygame.draw.line(screen, GRAY,
                (MARGIN_LEFT, MARGIN_TOP + y*CELL_SIZE),
                (MARGIN_LEFT + GRID_W*CELL_SIZE, MARGIN_TOP + y*CELL_SIZE),2)

    def draw_ui(self):
        # 顶部UI：关卡 + 爱心失误
        level_text = FONT.render(f"关卡 {self.level_idx+1}", True, BLACK)
        heart_text = FONT.render(f"失误 {self.mistake}/{self.max_mistake}", True, RED)
        screen.blit(level_text, (50, 30))
        screen.blit(heart_text, (220,30))
        # 底部【重新开始】按钮
        btn_reset = pygame.Rect(60, HEIGHT -70, 150, 50)
        pygame.draw.rect(screen, GRAY, btn_reset, border_radius=8)
        txt_reset = FONT.render("重新开始", True, WHITE)
        screen.blit(txt_reset, txt_reset.get_rect(center=btn_reset.center))
        return btn_reset

    def draw_start(self):
        screen.fill(LIGHT_BLUE)
        title = BIG_FONT.render("一箭又一箭", True, BLACK)
        tip = FONT.render("点击任意位置开始游戏", True, BLACK)
        rule = FONT.render("点击箭头，无阻挡则飞出棋盘", True, GRAY)
        screen.blit(title, title.get_rect(center=(WIDTH//2,160)))
        screen.blit(rule, rule.get_rect(center=(WIDTH//2,240)))
        screen.blit(tip, tip.get_rect(center=(WIDTH//2,310)))

    def draw_play(self):
        screen.fill(LIGHT_BLUE)
        self.draw_grid()
        for arr in self.arrows:
            arr.draw()
        return self.draw_ui()

    def draw_win(self):
        screen.fill(LIGHT_BLUE)
        txt = BIG_FONT.render("恭喜通关！", True, GREEN)
        tip = FONT.render("点击屏幕进入下一关", True, BLACK)
        screen.blit(txt, txt.get_rect(center=(WIDTH//2,180)))
        screen.blit(tip, tip.get_rect(center=(WIDTH//2,260)))

    def draw_lose(self):
        screen.fill(LIGHT_BLUE)
        txt = BIG_FONT.render("挑战失败", True, RED)
        tip = FONT.render("点击屏幕，重玩本关", True, BLACK)
        screen.blit(txt, txt.get_rect(center=(WIDTH//2,180)))
        screen.blit(tip, tip.get_rect(center=(WIDTH//2,260)))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button ==1:
                    mx, my = event.pos
                    if self.state == STATE_START:
                        self.load_level(0)
                        self.state = STATE_PLAY
                    elif self.state == STATE_PLAY:
                        btn_reset = self.draw_ui()
                        if btn_reset.collidepoint(mx, my):
                            self.load_level(self.level_idx)
                        else:
                            self.on_click_grid(mx, my)
                    elif self.state == STATE_WIN:
                        self.level_idx +=1
                        if self.level_idx >= len(LEVELS):
                            self.level_idx = 0
                        self.load_level(self.level_idx)
                        self.state = STATE_PLAY
                    elif self.state == STATE_LOSE:
                        self.load_level(self.level_idx)
                        self.state = STATE_PLAY
            self.update_all()
            if self.state == STATE_START:
                self.draw_start()
            elif self.state == STATE_PLAY:
                self.draw_play()
            elif self.state == STATE_WIN:
                self.draw_win()
            elif self.state == STATE_LOSE:
                self.draw_lose()
            pygame.display.flip()
            clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()
