import pygame
import sys
import random
import math


# Pygame-based menu for player choice
def get_player_choice():
    menu_font = pygame.font.SysFont(None, 60)
    small_font = pygame.font.SysFont(None, 36)
    prompt = menu_font.render("Choose your piece:", True, (0, 0, 0))
    options = [
        ("Rock (R)", ROCK),
        ("Paper (P)", PAPER),
        ("Scissors (S)", SCISSORS)
    ]
    while True:
        screen.fill((255, 255, 255))
        screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 2 - 120))
        for i, (label, _) in enumerate(options):
            text = small_font.render(label, True, (0, 0, 0))
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 30 + i * 50))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return ROCK
                elif event.key == pygame.K_p:
                    return PAPER
                elif event.key == pygame.K_s:
                    return SCISSORS

pygame.init()

WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rock Paper Scissors Survival")

BLACK = (255, 255, 255)
WHITE = (0, 0, 0)

ROCK = 'rock'
PAPER = 'paper'
SCISSORS = 'scissors'

SPEED = 2
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
        if self.kind == PAPER:
            # white rectangle with black border for paper
            rect_width = self.RADIUS * 2
            rect_height = self.RADIUS * 3
            rect_x = int(self.x - rect_width / 2)
            rect_y = int(self.y - rect_height / 2)
            pygame.draw.rect(screen, (255, 255, 255), (rect_x, rect_y, rect_width, rect_height))
            pygame.draw.rect(screen, (0, 0, 0), (rect_x, rect_y, rect_width, rect_height), 2)
        elif self.kind == ROCK:
            # Draw an irregular polygon to represent a rock
            base_radius = self.RADIUS
            center = (int(self.x), int(self.y))
            num_points = 3
            angle_offset = random.uniform(0, 2 * math.pi)
            points = []
            for i in range(num_points):
                angle = angle_offset + (2 * math.pi / num_points) * i
                # Vary the radius for jaggedness
                radius = base_radius + random.randint(-3, 3)
                px = int(self.x + radius * math.cos(angle))
                py = int(self.y + radius * math.sin(angle))
                points.append((px, py))
            pygame.draw.polygon(screen, (169, 169, 169), points)

        else:
            # scissors with red handles and silver blades
            center = (int(self.x), int(self.y))
            blade_length = self.RADIUS * 2
            blade_width = 4

            # Calculate blade end points (two lines crossing)
            # Blade 1
            angle1 = math.radians(30)
            x1_start = self.x + math.cos(angle1) * 0
            y1_start = self.y + math.sin(angle1) * 0
            x1_end = self.x + math.cos(angle1) * blade_length
            y1_end = self.y + math.sin(angle1) * blade_length

            # Blade 2
            angle2 = math.radians(150)
            x2_start = self.x + math.cos(angle2) * 0
            y2_start = self.y + math.sin(angle2) * 0
            x2_end = self.x + math.cos(angle2) * blade_length
            y2_end = self.y + math.sin(angle2) * blade_length

            # Draw blades (silver)
            silver = (192, 192, 192)
            pygame.draw.line(screen, silver, (x1_start, y1_start), (x1_end, y1_end), blade_width)
            pygame.draw.line(screen, silver, (x2_start, y2_start), (x2_end, y2_end), blade_width)

            # Draw handles as red circles near center base of each blade
            red = (200, 0, 0)
            handle_radius = self.RADIUS // 2

            # Position handles slightly offset from center along blade base directions
            offset_dist = handle_radius
            handle1_pos = (int(self.x + math.cos(angle1) * offset_dist), int(self.y + math.sin(angle1) * offset_dist))
            handle2_pos = (int(self.x + math.cos(angle2) * offset_dist), int(self.y + math.sin(angle2) * offset_dist))

            pygame.draw.circle(screen, red, handle1_pos, handle_radius)
            pygame.draw.circle(screen, red, handle2_pos, handle_radius)


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


# Create AI pieces
pieces = []
pieces.extend(create_pieces(PAPER, 10, WIDTH // 2, MARGIN // 2))
pieces.extend(create_pieces(ROCK, 10, MARGIN, HEIGHT - MARGIN))
pieces.extend(create_pieces(SCISSORS, 10, WIDTH - MARGIN, HEIGHT - MARGIN))

# Create player piece
player_kind = get_player_choice()
player = Piece(player_kind, WIDTH // 2, HEIGHT // 2, 0, 0)
player_speed = 4

clock = pygame.time.Clock()
running = True



# Track the original player kind for game over detection
original_player_kind = player.kind
game_over = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        # Handle player movement
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx -= player_speed
        if keys[pygame.K_RIGHT]:
            dx += player_speed
        if keys[pygame.K_UP]:
            dy -= player_speed
        if keys[pygame.K_DOWN]:
            dy += player_speed
        # Move player, keep within bounds
        player.x = max(player.RADIUS, min(WIDTH - player.RADIUS, player.x + dx))
        player.y = max(player.RADIUS, min(HEIGHT - player.RADIUS, player.y + dy))

        screen.fill(WHITE)

        # Move and draw AI pieces
        for p in pieces:
            p.move()
            p.draw()

        # Draw player piece (on top)
        player.draw()

        # Collisions: player vs AI pieces
        for p in pieces:
            if player.collide(p):
                player.transform(p)
                p.transform(player)

        # Check for game over (player changed type)
        if player.kind != original_player_kind:
            game_over = True

        # Collisions: AI pieces vs each other
        for i in range(len(pieces)):
            for j in range(i + 1, len(pieces)):
                if pieces[i].collide(pieces[j]):
                    pieces[i].transform(pieces[j])
                    pieces[j].transform(pieces[i])

        # Update counts (include player)
        rock_count = sum(p.kind == ROCK for p in pieces) + (player.kind == ROCK)
        paper_count = sum(p.kind == PAPER for p in pieces) + (player.kind == PAPER)
        scissors_count = sum(p.kind == SCISSORS for p in pieces) + (player.kind == SCISSORS)


        # Highlight the player's current piece counter in green
        GREEN = (0, 180, 0)
        rock_color = GREEN if player.kind == ROCK else BLACK
        paper_color = GREEN if player.kind == PAPER else BLACK
        scissors_color = GREEN if player.kind == SCISSORS else BLACK
        screen.blit(font.render(f"Rock: {rock_count}", True, rock_color), (10, 10))
        screen.blit(font.render(f"Paper: {paper_count}", True, paper_color), (10, 40))
        screen.blit(font.render(f"Scissors: {scissors_count}", True, scissors_color), (10, 70))

        pygame.display.flip()
        clock.tick(60)
    else:
        # Game over screen
        screen.fill((0, 0, 0))
        over_font = pygame.font.SysFont(None, 80)
        msg = over_font.render("Game Over!", True, (200, 0, 0))
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 60))
        info_font = pygame.font.SysFont(None, 40)
        info = info_font.render("YOU FOOKEN LOST", True, (255, 255, 255))
        screen.blit(info, (WIDTH // 2 - info.get_width() // 2, HEIGHT // 2 + 10))
        pygame.display.flip()
        # Wait for ESC or window close
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

pygame.quit()
sys.exit()