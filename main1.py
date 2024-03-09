import pygame
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BALL_RADIUS = 20
NUM_BALLS = 10

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chain Reaction")

# Ball class
class Ball:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), BALL_RADIUS)

# Initialize balls
balls = []
for _ in range(NUM_BALLS):
    x = random.randint(BALL_RADIUS, WIDTH - BALL_RADIUS)
    y = random.randint(BALL_RADIUS, HEIGHT - BALL_RADIUS)
    color = random.choice([RED, GREEN, BLUE])
    balls.append(Ball(x, y, color))

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update game state

    # Check for collisions
    for ball in balls:
        for other_ball in balls:
            if ball != other_ball and abs(ball.x - other_ball.x) < BALL_RADIUS * 2 and abs(ball.y - other_ball.y) < BALL_RADIUS * 2:
                if ball.color == other_ball.color:
                    ball.x = random.randint(BALL_RADIUS, WIDTH - BALL_RADIUS)
                    ball.y = random.randint(BALL_RADIUS, HEIGHT - BALL_RADIUS)
                    ball.color = random.choice([RED, GREEN, BLUE])
                    other_ball.x = random.randint(BALL_RADIUS, WIDTH - BALL_RADIUS)
                    other_ball.y = random.randint(BALL_RADIUS, HEIGHT - BALL_RADIUS)
                    other_ball.color = random.choice([RED, GREEN, BLUE])

    # Clear screen
    screen.fill(WHITE)

    # Draw balls
    for ball in balls:
        ball.draw()

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(FPS)

# Quit pygame
pygame.quit()
