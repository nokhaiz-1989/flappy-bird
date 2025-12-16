import pygame
import random
import sys

# ---------------- INITIAL SETUP ----------------
pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)

# ---------------- CONSTANTS ----------------
GRAVITY = 0.5
FLAP_STRENGTH = -8
PIPE_GAP = 160
PIPE_SPEED = 4

# ---------------- COLORS ----------------
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
BLUE = (0, 150, 255)

# ---------------- CLASSES ----------------
class Bird:
    def __init__(self):
        self.x = 80
        self.y = HEIGHT // 2
        self.vel = 0
        self.radius = 15

    def flap(self):
        self.vel = FLAP_STRENGTH

    def update(self):
        self.vel += GRAVITY
        self.y += self.vel

    def draw(self):
        pygame.draw.circle(screen, BLUE, (self.x, int(self.y)), self.radius)


class Pipe:
    def __init__(self):
        self.x = WIDTH
        self.height = random.randint(100, 400)

    def update(self):
        self.x -= PIPE_SPEED

    def draw(self):
        pygame.draw.rect(screen, GREEN, (self.x, 0, 60, self.height))
        pygame.draw.rect(
            screen,
            GREEN,
            (self.x, self.height + PIPE_GAP, 60, HEIGHT)
        )

    def collide(self, bird):
        bird_rect = pygame.Rect(
            bird.x - bird.radius,
            bird.y - bird.radius,
            bird.radius * 2,
            bird.radius * 2,
        )

        top_pipe = pygame.Rect(self.x, 0, 60, self.height)
        bottom_pipe = pygame.Rect(
            self.x,
            self.height + PIPE_GAP,
            60,
            HEIGHT
        )

        return bird_rect.colliderect(top_pipe) or bird_rect.colliderect(bottom_pipe)


# ---------------- GAME FUNCTION ----------------
def main():
    bird = Bird()
    pipes = [Pipe()]
    score = 0
    running = True

    while running:
        clock.tick(60)
        screen.fill(WHITE)

        # -------- EVENTS --------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    bird.flap()

        # -------- UPDATE --------
        bird.update()

        for pipe in pipes:
            pipe.update()
            if pipe.collide(bird):
                return

        if pipes[-1].x < WIDTH - 200:
            pipes.append(Pipe())

        if pipes[0].x < -60:
            pipes.pop(0)
            score += 1

        if bird.y > HEIGHT or bird.y < 0:
            return

        # -------- DRAW --------
        bird.draw()
        for pipe in pipes:
            pipe.draw()

        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        pygame.display.update()


# ---------------- RESTART LOOP ----------------
while True:
    main()
