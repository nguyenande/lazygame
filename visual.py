import turtle
import random

# Set up the screen
turtle.bgcolor('black')
turtle.colormode(255)
turtle.speed(0)

# Draw colorful spiral
for x in range(500):
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    turtle.pencolor(r, g, b)
    turtle.forward(x + 130)
    turtle.right(500)

turtle.exitonclick()
