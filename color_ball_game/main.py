import turtle
import random
import time
import math

# 设置游戏窗口
screen = turtle.Screen()
screen.title("彩色弹球游戏 🎮")
screen.bgcolor("black")
screen.setup(800, 600)
screen.tracer(0)  # 关闭自动更新，手动控制刷新

# 游戏变量
score = 0
lives = 3
game_over = False
level = 1
balls = []
particles = []

class Player:
    def __init__(self):
        self.paddle = turtle.Turtle()
        self.paddle.speed(0)
        self.paddle.shape("square")
        self.paddle.color("white")
        self.paddle.shapesize(stretch_wid=1, stretch_len=5)
        self.paddle.penup()
        self.paddle.goto(0, -250)
        
    def move_left(self):
        x = self.paddle.xcor()
        if x > -350:
            x -= 20
            self.paddle.setx(x)
            
    def move_right(self):
        x = self.paddle.xcor()
        if x < 350:
            x += 20
            self.paddle.setx(x)

class Ball:
    def __init__(self):
        self.ball = turtle.Turtle()
        self.ball.speed(0)
        self.ball.shape("circle")
        self.ball.color(random.choice(["red", "blue", "green", "yellow", "purple", "orange"]))
        self.ball.penup()
        self.ball.goto(0, 0)
        
        # 随机初始方向
        angle = random.uniform(30, 150)
        self.dx = math.cos(math.radians(angle)) * 5
        self.dy = math.sin(math.radians(angle)) * 5
        
    def move(self):
        self.ball.setx(self.ball.xcor() + self.dx)
        self.ball.sety(self.ball.ycor() + self.dy)
        
    def bounce_x(self):
        self.dx *= -1
        self.ball.color(random.choice(["red", "blue", "green", "yellow", "purple", "orange"]))
        
    def bounce_y(self):
        self.dy *= -1
        self.ball.color(random.choice(["red", "blue", "green", "yellow", "purple", "orange"]))

class Brick:
    def __init__(self, x, y, color):
        self.brick = turtle.Turtle()
        self.brick.speed(0)
        self.brick.shape("square")
        self.brick.color(color)
        self.brick.shapesize(stretch_wid=1, stretch_len=2)
        self.brick.penup()
        self.brick.goto(x, y)
        self.active = True

class Particle:
    def __init__(self, x, y, color):
        self.particle = turtle.Turtle()
        self.particle.speed(0)
        self.particle.shape("circle")
        self.particle.color(color)
        self.particle.shapesize(stretch_wid=0.3, stretch_len=0.3)
        self.particle.penup()
        self.particle.goto(x, y)
        
        # 随机方向
        angle = random.uniform(0, 360)
        speed = random.uniform(1, 5)
        self.dx = math.cos(math.radians(angle)) * speed
        self.dy = math.sin(math.radians(angle)) * speed
        self.life = 30  # 粒子寿命
        
    def move(self):
        self.particle.setx(self.particle.xcor() + self.dx)
        self.particle.sety(self.particle.ycor() + self.dy)
        self.life -= 1
        # 逐渐变小
        size = max(0.1, self.life / 30 * 0.3)
        self.particle.shapesize(stretch_wid=size, stretch_len=size)

# 创建玩家
player = Player()

# 创建砖块
bricks = []
colors = ["red", "orange", "yellow", "green", "blue"]
for i in range(5):
    for j in range(8):
        brick = Brick(-350 + j * 100, 250 - i * 30, colors[i])
        bricks.append(brick)

# 创建第一个球
balls.append(Ball())

# 显示分数和生命值
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write(f"分数: {score}  生命: {lives}  关卡: {level}", align="center", font=("Arial", 16, "normal"))

# 游戏结束显示
game_over_pen = turtle.Turtle()
game_over_pen.speed(0)
game_over_pen.color("red")
game_over_pen.penup()
game_over_pen.hideturtle()
game_over_pen.goto(0, 0)

# 键盘控制
screen.listen()
screen.onkeypress(player.move_left, "Left")
screen.onkeypress(player.move_right, "Right")
screen.onkeypress(player.move_left, "a")
screen.onkeypress(player.move_right, "d")

def create_particles(x, y, color, count=10):
    for _ in range(count):
        particles.append(Particle(x, y, color))

def next_level():
    global level, balls
    level += 1
    balls = [Ball()]
    
    # 重置砖块
    for brick in bricks:
        brick.active = True
        brick.brick.goto(brick.brick.xcor(), brick.brick.ycor())
        brick.brick.showturtle()

# 游戏主循环
while True:
    if not game_over:
        screen.update()
        
        # 移动所有球
        for ball in balls[:]:  # 使用切片创建副本以便在循环中删除
            ball.move()
            
            # 边界检测
            if ball.ball.xcor() > 390:
                ball.ball.setx(390)
                ball.bounce_x()
                
            if ball.ball.xcor() < -390:
                ball.ball.setx(-390)
                ball.bounce_x()
                
            if ball.ball.ycor() > 290:
                ball.ball.sety(290)
                ball.bounce_y()
                
            # 球落到底部
            if ball.ball.ycor() < -290:
                ball.ball.goto(0, 0)
                ball.bounce_y()
                lives -= 1
                pen.clear()
                pen.write(f"分数: {score}  生命: {lives}  关卡: {level}", align="center", font=("Arial", 16, "normal"))
                
                if lives <= 0:
                    game_over = True
                    game_over_pen.write("游戏结束! 按R键重新开始", align="center", font=("Arial", 24, "normal"))
            
            # 球与挡板碰撞
            if (ball.ball.ycor() < -240 and ball.ball.ycor() > -250 and 
                ball.ball.xcor() < player.paddle.xcor() + 50 and 
                ball.ball.xcor() > player.paddle.xcor() - 50):
                ball.ball.sety(-240)
                ball.bounce_y()
                
                # 根据击中挡板的位置改变反弹角度
                paddle_center = player.paddle.xcor()
                hit_pos = ball.ball.xcor() - paddle_center
                angle = hit_pos / 50 * 60  # -60到60度
                ball.dx = math.sin(math.radians(angle)) * 5
                ball.dy = math.cos(math.radians(angle)) * 5
                
                create_particles(ball.ball.xcor(), ball.ball.ycor(), ball.ball.color()[0], 5)
            
            # 球与砖块碰撞
            for brick in bricks:
                if brick.active and (
                    (ball.ball.ycor() + 10 > brick.brick.ycor() - 15 and 
                     ball.ball.ycor() - 10 < brick.brick.ycor() + 15 and
                     ball.ball.xcor() + 10 > brick.brick.xcor() - 20 and 
                     ball.ball.xcor() - 10 < brick.brick.xcor() + 20)):
                    
                    brick.active = False
                    brick.brick.hideturtle()
                    score += 10
                    pen.clear()
                    pen.write(f"分数: {score}  生命: {lives}  关卡: {level}", align="center", font=("Arial", 16, "normal"))
                    
                    # 创建粒子效果
                    create_particles(brick.brick.xcor(), brick.brick.ycor(), brick.brick.color()[0], 15)
                    
                    # 随机改变球的颜色
                    ball.ball.color(random.choice(["red", "blue", "green", "yellow", "purple", "orange"]))
                    
                    # 确定从哪个方向碰撞
                    if ball.ball.xcor() < brick.brick.xcor() - 15 or ball.ball.xcor() > brick.brick.xcor() + 15:
                        ball.bounce_x()
                    else:
                        ball.bounce_y()
                    
                    # 随机几率产生新球
                    if random.random() < 0.1 and len(balls) < 3:
                        balls.append(Ball())
        
        # 移动所有粒子
        for particle in particles[:]:
            particle.move()
            if particle.life <= 0:
                particle.particle.hideturtle()
                particles.remove(particle)
        
        # 检查是否过关
        if all(not brick.active for brick in bricks):
            next_level()
            pen.clear()
            pen.write(f"分数: {score}  生命: {lives}  关卡: {level}", align="center", font=("Arial", 16, "normal"))
    
    else:
        # 游戏结束状态
        screen.update()
        
        def restart_game():
            global score, lives, game_over, level, balls, particles
            score = 0
            lives = 3
            game_over = False
            level = 1
            balls = [Ball()]
            particles = []
            
            # 重置砖块
            for brick in bricks:
                brick.active = True
                brick.brick.showturtle()
            
            # 重置玩家位置
            player.paddle.goto(0, -250)
            
            # 清除游戏结束文字
            game_over_pen.clear()
            pen.clear()
            pen.write(f"分数: {score}  生命: {lives}  关卡: {level}", align="center", font=("Arial", 16, "normal"))
        
        screen.onkeypress(restart_game, "r")
    
    # 控制游戏速度
    time.sleep(0.01)

# 保持窗口打开
screen.mainloop()