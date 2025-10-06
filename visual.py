import pygame
import sys
import random

# Initialize Pygame
pygame.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rock Paper Scissors Bounce")

WHITE = (255, 255, 255)

ROCK = 'rock'
PAPER = 'paper'
SCISSORS = 'scissors'

SPEED = 3

class Piece:
    RADIUS = 20

    def __init__(self, kind, x, y, dx, dy):
        self.kind = kind
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

    def move(self):
        self.x += self.dx
        self.y += self.dy
        if self.x <= self.RADIUS or self.x >= WIDTH - self.RADIUS:
            self.dx *= -1
        if self.y <= self.RADIUS or self.y >= HEIGHT - self.RADIUS:
            self.dy *= -1

    def draw(self):
        color = (139, 69, 19) if self.kind == ROCK else (135, 206, 250) if self.kind == PAPER else (192, 192, 192)
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.RADIUS)

    def collide(self, other):
        dist = ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5
        return dist <= 2 * self.RADIUS

    def transform(self, other):
        # rock touches paper -> rock becomes paper
        if self.kind == ROCK and other.kind == PAPER:
            self.kind = PAPER
        # rock touches scissors -> scissors becomes rock
        elif self.kind == ROCK and other.kind == SCISSORS:
            other.kind = ROCK
        # paper touches scissors -> paper becomes scissors
        elif self.kind == PAPER and other.kind == SCISSORS:
            self.kind = SCISSORS
        # paper touches rock -> rock becomes paper
        elif self.kind == PAPER and other.kind == ROCK:
            other.kind = PAPER
        # scissors touches rock -> scissors becomes rock
        elif self.kind == SCISSORS and other.kind == ROCK:
            self.kind = ROCK
        # scissors touches paper -> paper becomes scissors
        elif self.kind == SCISSORS and other.kind == PAPER:
            other.kind = SCISSORS

def create_pieces(kind, count, x_range, y_range):
    pieces = []
    for _ in range(count):
        x = random.randint(x_range[0], x_range[1])
        y = random.randint(y_range[0], y_range[1])
        dx = random.choice([-SPEED, SPEED])
        dy = random.choice([-SPEED, SPEED])
        pieces.append(Piece(kind, x, y, dx, dy))
    return pieces

pieces = []
pieces.extend(create_pieces(PAPER, 10, (50, WIDTH - 50), (50, HEIGHT - 50)))
pieces.extend(create_pieces(SCISSORS, 10, (50, WIDTH - 50), (50, HEIGHT - 50)))
pieces.extend(create_pieces(ROCK, 10, (50, WIDTH - 50), (50, HEIGHT - 50)))

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)

    for p in pieces:
        p.move()
        p.draw()

    for i in range(len(pieces)):
        for j in range(i + 1, len(pieces)):
            if pieces[i].collide(pieces[j]):
                pieces[i].transform(pieces[j])
                pieces[j].transform(pieces[i])

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
