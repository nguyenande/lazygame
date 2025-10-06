import pygame
import sys
import random
import math

pygame.init()

WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rock Paper Scissors Bounce")

BLACK = (255, 255, 255)
WHITE = (0, 0, 0)

ROCK = 'rock'
PAPER = 'paper'
SCISSORS = 'scissors'

SPEED = 3
MARGIN = 140  # margin from edges for starting positions

font = pygame.font.SysFont(None, 40)

class Piece:
    RADIUS = 10

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
        dist = math.hypot(self.x - other.x, self.y - other.y)
        return dist <= 2 * self.RADIUS

    def transform(self, other):
        if self.kind == ROCK and other.kind == PAPER:
            self.kind = PAPER
        elif self.kind == ROCK and other.kind == SCISSORS:
            other.kind = ROCK
        elif self.kind == PAPER and other.kind == SCISSORS:
            self.kind = SCISSORS
        elif self.kind == PAPER and other.kind == ROCK:
            other.kind = PAPER
        elif self.kind == SCISSORS and other.kind == ROCK:
            self.kind = ROCK
        elif self.kind == SCISSORS and other.kind == PAPER:
            other.kind = SCISSORS

def random_velocity(speed):
    angle = random.uniform(0, 2 * math.pi)
    dx = math.cos(angle) * speed
    dy = math.sin(angle) * speed
    return dx, dy

def create_pieces(kind, count, start_x, start_y, spread_x=50, spread_y=50):
    pieces = []
    for i in range(count):
        x = start_x + (i % 5) * spread_x - (spread_x * 2)
        y = start_y + (i // 5) * spread_y
        dx, dy = random_velocity(SPEED)
        pieces.append(Piece(kind, x, y, dx, dy))
    return pieces

pieces = []
pieces.extend(create_pieces(PAPER, 10, WIDTH // 2, MARGIN // 2))
pieces.extend(create_pieces(ROCK, 10, MARGIN, HEIGHT - MARGIN))
pieces.extend(create_pieces(SCISSORS, 10, WIDTH - MARGIN, HEIGHT - MARGIN))

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

    rock_count = sum(p.kind == ROCK for p in pieces)
    paper_count = sum(p.kind == PAPER for p in pieces)
    scissors_count = sum(p.kind == SCISSORS for p in pieces)

    screen.blit(font.render(f"Rock: {rock_count}", True, BLACK), (10, 10))
    screen.blit(font.render(f"Paper: {paper_count}", True, BLACK), (10, 40))
    screen.blit(font.render(f"Scissors: {scissors_count}", True, BLACK), (10, 70))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
