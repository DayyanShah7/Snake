import pygame
import sys
import random

pygame.init()

SW, SH = 600, 600
Block_Size = 50

screen = pygame.display.set_mode((SW ,  SH))
pygame.display.set_caption("Snake ")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

clock = pygame.time.Clock()


image = pygame.image.load("C:\\Users\\dayya\\PycharmProjects\\Snake\\snake2.png")
new_width, new_height = 300, 200
image = pygame.transform.scale(image, (new_width, new_height))
image_rect = image.get_rect()
image_rect.center = (320, 120)


FONT = pygame.font.SysFont('Arial', 24)


class Button:
    def __init__(self, text, x, y, width, height, color, hover_color):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.font = pygame.font.SysFont(None, 36)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)

        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False


class Snake:

    def __init__(self):
        self.x, self.y = Block_Size, Block_Size
        self.xdir = 1
        self.ydir = 0
        self.head = pygame.Rect(self.x, self.y, Block_Size, Block_Size)
        self.body = [pygame.Rect(self.x - Block_Size, self.y, Block_Size, Block_Size)]
        self.dead = False
        self.score = 0

    def update(self):
        global apple

        # Update body position before moving head
        if len(self.body) > 0:
            self.body = [self.head.copy()] + self.body[:-1]

        # Move the head
        self.head.x += self.xdir * Block_Size
        self.head.y += self.ydir * Block_Size

        # Check collision with body
        for square in self.body:
            if self.head.colliderect(square):
                self.dead = True
                break

        # Check if out of bounds
        if self.head.x not in range(0, SW) or self.head.y not in range(0, SH):
            self.dead = True

        # Reset snake if dead
        if self.dead:
            self.reset()

    def grow(self):
        self.body.append(self.head.copy())  # Add a copy of the head to the body
        self.score += 1

    def reset(self):
        self.x, self.y = Block_Size, Block_Size
        self.head = pygame.Rect(self.x, self.y, Block_Size, Block_Size)
        self.body = [pygame.Rect(self.x - Block_Size, self.y, Block_Size, Block_Size)]
        self.xdir = 1
        self.ydir = 0
        self.dead = False
        self.score = 0
        global apple
        apple = Apple()  # Respawn apple if snake dies

    def save_score(self):
        with open("C:\\Users\\dayya\\PycharmProjects\\Snake\\highscore.txt", "a") as file:
            file.write(f"Score: {self.score}\n")


class Apple:
    def __init__(self):
        self.spawn()

    def spawn(self):
        self.x = random.randint(0, (SW // Block_Size) - 1) * Block_Size
        self.y = random.randint(0, (SH // Block_Size) - 1) * Block_Size
        self.rect = pygame.Rect(self.x, self.y, Block_Size, Block_Size)

    def update(self):
        pygame.draw.rect(screen, "Red", self.rect)



def game_loop():

    global apple

    snake = Snake()
    apple = Apple()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:

                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_DOWN:
                    snake.ydir = 1
                    snake.xdir = 0
                elif event.key == pygame.K_UP:
                    snake.ydir = -1
                    snake.xdir = 0
                elif event.key == pygame.K_RIGHT:
                    snake.ydir = 0
                    snake.xdir = 1
                elif event.key == pygame.K_LEFT:
                    snake.ydir = 0
                    snake.xdir = -1

        snake.update()
        screen.fill("black")
        apple.update()

        pygame.draw.rect(screen, "green", snake.head)
        for square in snake.body:
            pygame.draw.rect(screen, "green", square)

        score = FONT.render(f"{len(snake.body) + 1}", True, "white")
        screen.blit(score, (SW / 2, SH / 20))

        if snake.head.x == apple.x and snake.head.y == apple.y:
            snake.grow()
            apple = Apple()

        pygame.display.update()
        clock.tick(8)


button = Button("Play", 220, 270, 200, 80, BLACK, (50, 50, 50))

def main():
    running = True
    while running:
        screen.fill(BLACK)
        screen.blit(image, image_rect)
        button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if button.is_clicked(event):
                game_loop()

        pygame.display.flip()

    pygame.quit()
    sys.exit()


main()
