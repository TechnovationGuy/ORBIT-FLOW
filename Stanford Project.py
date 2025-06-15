import turtle
import math
import time
import random

# ------------------ SETUP -------------------
screen = turtle.Screen()
screen.bgcolor("black")  # Set space-like background
screen.title("Orbital Traffic Controller")  # Our game title
screen.setup(width=800, height=800)
screen.tracer(0)  # Disable auto-refresh for better manual control

# Global variables
game_started = False  # Flag to track if the game has started
num_sats = 0  # Number of satellites based on difficulty
earth_angle = 0  # Earth rotation angle for spinning effect
satellites = []  # Holds all satellites in orbit
current_index = 0  # Index of currently selected satellite
controlled = None  # The satellite currently being controlled
start_time = None  # Start time to calculate survival duration
best_time = 0  # Track the best survival record
buttons = []  # Store all difficulty buttons

# --------- EARTH SETUP -------------
earth = turtle.Turtle()
earth.shape("circle")
earth.color("blue")  # Earth colored blue, naturally :)
earth.shapesize(2)
earth.penup()
earth.goto(0, 0)  # Earth at center of the screen

# --------- TEXT DISPLAY OBJECTS -------------
title_text = turtle.Turtle()  # For game title
title_text.hideturtle()
title_text.color("white")
title_text.penup()

instruction_text = turtle.Turtle()  # For control instructions
instruction_text.hideturtle()
instruction_text.color("white")
instruction_text.penup()

# HUD to display survival time
score_display = turtle.Turtle()
score_display.hideturtle()
score_display.color("white")
score_display.penup()
score_display.goto(-350, 350)

# --------- GAME OVER MESSAGE ----------
def game_over(survival_time, best_time):
    """
    Called when a collision is detected.
    Displays final survival time and best record so far.
    """
    msg = turtle.Turtle()
    msg.hideturtle()
    msg.color("white")
    msg.penup()
    msg.goto(0, 20)
    msg.write("\U0001F4A5 COLLISION DETECTED!\nGAME OVER", align="center", font=("Arial", 20, "bold"))
    msg.goto(0, -20)
    msg.write(f"You survived for {int(survival_time)} sec", align="center", font=("Arial", 16, "normal"))
    msg.goto(0, -50)
    msg.write(f"Best time: {int(best_time)} sec", align="center", font=("Arial", 14, "italic"))

# --------- SATELLITE CLASS --------
class Satellite:
    def __init__(self, radius, angle_speed, color, angle_offset=0):
        # Each satellite orbits the Earth at a fixed radius and speed
        self.radius = radius
        self.angle = angle_offset
        self.angle_speed = angle_speed
        self.t = turtle.Turtle()
        self.t.shape("circle")
        self.t.color(color)
        self.t.shapesize(0.5)
        self.t.penup()
        self.highlight = turtle.Turtle()
        self.highlight.hideturtle()
        self.highlight.penup()

    def update_position(self):
        # Recalculate the new position in orbit using polar coordinates
        self.angle += self.angle_speed
        x = self.radius * math.cos(math.radians(self.angle))
        y = self.radius * math.sin(math.radians(self.angle))
        self.t.goto(x, y)

    def draw_glow(self):
        self.highlight.clear()
        self.highlight.color("white")
        self.highlight.goto(self.t.pos())
        self.highlight.dot(20)

    def clear_glow(self):
        self.highlight.clear()

# --------- COLLISION CHECK -----------
def check_collisions():
    for i in range(len(satellites)):
        for j in range(i + 1, len(satellites)):
            x1, y1 = satellites[i].t.pos()
            x2, y2 = satellites[j].t.pos()
            dist = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
            if dist < 30:
                return "collision"
            elif dist < 50:
                return "warning"
    return "clear"

# --------- CONTROLS ----------
def move_up():
    if controlled:
        controlled.radius += 10

def move_down():
    if controlled:
        controlled.radius = max(50, controlled.radius - 10)

def turn_left():
    if controlled:
        controlled.angle_speed += 0.1

def turn_right():
    if controlled:
        controlled.angle_speed -= 0.1

def switch_control():
    global current_index, controlled
    if not game_started:
        return
    controlled.clear_glow()
    current_index = (current_index + 1) % len(satellites)
    controlled = satellites[current_index]

# Assign control keys
screen.listen()
screen.onkey(move_up, "w")
screen.onkey(move_down, "s")
screen.onkey(turn_left, "a")
screen.onkey(turn_right, "d")
screen.onkey(switch_control, "space")

# --------- BUTTON CLASS -------------
class Button:
    def __init__(self, label, x, y):
        self.label = label
        self.x = x
        self.y = y
        self.width = 160
        self.height = 40
        self.draw()

    def draw(self):
        self.btn = turtle.Turtle()
        self.btn.hideturtle()
        self.btn.penup()
        self.btn.goto(self.x, self.y)
        self.btn.color("white")
        self.btn.write(self.label, align="center", font=("Arial", 14, "bold"))
        buttons.append(self)

    def is_clicked(self, click_x, click_y):
        return (
            self.x - self.width//2 < click_x < self.x + self.width//2 and
            self.y - self.height//2 < click_y < self.y + self.height//2
        )

# -------- BUTTON HANDLERS ----------
def start_game(difficulty):
    global num_sats, controlled, satellites, game_started, start_time, current_index
    if difficulty == "Easy": num_sats = 3
    elif difficulty == "Medium": num_sats = 5
    elif difficulty == "Hard": num_sats = 7
    else: num_sats = 3

    # Clear menu text
    title_text.clear()
    instruction_text.clear()
    for btn in buttons:
        btn.btn.clear()

    # Initialize satellites with various speeds and offsets
    colors = ["red", "yellow", "green", "white", "orange", "cyan", "magenta"]
    satellites.clear()
    for i in range(num_sats):
        radius = 120 + i * 20
        speed = random.uniform(1, 3)
        color = colors[i % len(colors)]
        angle_offset = i * (360 // num_sats)
        sat = Satellite(radius, speed, color, angle_offset)
        satellites.append(sat)

    controlled = satellites[0]
    current_index = 0
    game_started = True
    start_time = time.time()

# --------- MENU SETUP ------------
def show_menu():
    title_text.goto(0, 200)
    title_text.write("\U0001F30D Orbital Traffic Controller \U0001F30D", align="center", font=("Arial", 24, "bold"))

    instruction_text.goto(0, 100)
    instruction_text.write("Use W/S to move up/down, A/D to change orbit speed\nSPACE to switch between satellites",
                           align="center", font=("Arial", 14, "normal"))

    Button("Easy", 0, 0)
    Button("Medium", 0, -60)
    Button("Hard", 0, -120)

def handle_click(x, y):
    for btn in buttons:
        if btn.is_clicked(x, y):
            start_game(btn.label)
            break

screen.onclick(handle_click)
show_menu()

# --------- MAIN GAME LOOP ----------
def main_loop():
    global earth_angle, best_time
    if game_started:
        for sat in satellites:
            sat.update_position()

        controlled.draw_glow()

        # Rotate Earth for visual effect
        earth_angle += 0.5
        earth.setheading(earth_angle)

        now = time.time()
        survival = now - start_time
        score_display.clear()
        score_display.write(f"\u23F1\ufe0f Time: {int(survival)}s", font=("Arial", 14, "normal"))

        result = check_collisions()
        if result == "collision":
            best_time = max(best_time, survival)
            game_over(survival, best_time)
            return

    screen.update()
    screen.ontimer(main_loop, 20)

main_loop()
screen.mainloop()
