import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cartoon Person in Car")

# Load assets
bg = pygame.image.load("car_background.jpg")
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

# Load cartoon person images
awake = pygame.image.load("person_openeyes.png")
eyes_closed = pygame.image.load("person_closeeyes.png")
#sleeping = pygame.image.load("person_sleeping.png")

# Resize person images
char_size = (300, 400)
awake = pygame.transform.scale(awake, char_size)
eyes_closed = pygame.transform.scale(eyes_closed, char_size)
#sleeping = pygame.transform.scale(sleeping, char_size)

# Character position
char_rect = awake.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

# State: 'awake', 'eyes_closed', 'sleeping'
state = "awake"

# Game loop
clock = pygame.time.Clock()

def draw():
    screen.blit(bg, (0, 0))
    if state == "awake":
        screen.blit(awake, char_rect)
    elif state == "eyes_closed":
        screen.blit(eyes_closed, char_rect)
   # elif state == "sleeping":
  #      screen.blit(sleeping, char_rect)
    pygame.display.flip()

# Main loop
while True:
    draw()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if char_rect.collidepoint(x, y):
                state = "eyes_closed"
            #elif y > HEIGHT * 0.8:
            #    state = "sleeping"
            else:
                state = "awake"

    clock.tick(30)
