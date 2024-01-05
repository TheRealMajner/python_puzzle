import pygame
import sys
import random
import requests
from io import BytesIO

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Function to get a random image URL from Lorem Picsum
def get_random_image_url():
    response = requests.get("https://picsum.photos/800/600")
    if response.status_code == 200:
        return response.url
    else:
        raise Exception("Failed to fetch image URL")

# Function to load a new random image
def load_new_image():
    image_url = get_random_image_url()
    image_response = requests.get(image_url)
    return pygame.image.load(BytesIO(image_response.content))

# Function to generate a new cut piece
def generate_cut_piece(image):
    puzzle_size = 100
    cut_x = random.randint(0, WIDTH - puzzle_size)
    cut_y = random.randint(0, HEIGHT - puzzle_size)
    cut_piece_rect = pygame.Rect(cut_x, cut_y, puzzle_size, puzzle_size)
    cut_piece = image.subsurface(cut_piece_rect).copy()
    return cut_piece, cut_x, cut_y

# Load the initial random image
current_image = load_new_image()
current_image = pygame.transform.scale(current_image, (WIDTH, HEIGHT))

# Get image rect for reference
image_rect = current_image.get_rect()

# Initialize Pygame
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Puzzle Game")
clock = pygame.time.Clock()

# Define draggable piece parameters
draggable_size = 100
draggable_rect = pygame.Rect(0, 0, draggable_size, draggable_size)
draggable_piece, cut_x, cut_y = generate_cut_piece(current_image)
offset_x, offset_y = 0, 0

solved = False

def reset_puzzle():
    global current_image, draggable_piece, cut_x, cut_y, solved
    current_image = load_new_image()
    current_image = pygame.transform.scale(current_image, (WIDTH, HEIGHT))
    draggable_piece, cut_x, cut_y = generate_cut_piece(current_image)
    solved = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if draggable_rect.collidepoint(event.pos) and not solved:
                offset_x = event.pos[0] - draggable_rect.x
                offset_y = event.pos[1] - draggable_rect.y
        elif event.type == pygame.MOUSEBUTTONUP:
            if draggable_piece is not None and cut_x < draggable_rect.x < cut_x + draggable_size and cut_y < draggable_rect.y < cut_y + draggable_size:
                print("Well done! You solved the puzzle.")
                solved = True
                draggable_rect.topleft = (cut_x, cut_y)  # Adjust draggable piece to its original place
                pygame.time.wait(2000)  # Pause for 2 seconds to display the solved state
                reset_puzzle()  # Load a new image and reset puzzle state

    screen.fill(WHITE)

    # Draw the current image
    screen.blit(current_image, image_rect)

    # Draw the cut area on top
    pygame.draw.rect(screen, WHITE, (cut_x, cut_y, draggable_size, draggable_size))
    pygame.draw.rect(screen, BLACK, (cut_x, cut_y, draggable_size, draggable_size), 2)

    # Draw the draggable piece
    if draggable_piece is not None:
        draggable_rect.topleft = pygame.mouse.get_pos()
        screen.blit(draggable_piece, draggable_rect)

    pygame.display.flip()
    clock.tick(FPS)