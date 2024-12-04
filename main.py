import pygame
import sys
from warehouse import Warehouse
import time
import random


def first_fit(weights, capacity, max_weight):
    warehouse = Warehouse()
    full = 0
    # Place items one by one
    bins = warehouse.get_bins()
    for weight in weights:
        if weight == capacity:
            full += 1
            continue
        # Find the first bin that can aclcommodate the weight
        placed = False
        for bin in bins:
            placed = False
            current_weight = bin.get_contents()
            if capacity - current_weight >= weight:
                placed = True
                bin.add_item(weight)

                # Check if the bin is almost full and remove it if so
                if current_weight + weight >= capacity - (max_weight / 8):
                    bins.remove(bin)
                    full += 1
                break

        # If no bin could accommodate the weight, create a new bi
        if placed is False:
            new_bin = warehouse.add_bin(capacity)
            new_bin.add_item(weight)
            bins = warehouse.get_bins()
    return len(warehouse.get_bins()) + full


def next_fit(weights, capacity):
    warehouse = Warehouse()
    # Add the first bin
    current_bin = warehouse.add_bin(capacity)

    for weight in weights:
        current_weight = current_bin.get_contents()
        # Check if the current bin can accommodate the weight
        if capacity - current_weight >= weight:
            current_bin.add_item(weight)

        else:
            # Create a new bin and use it
            current_bin = warehouse.add_bin(capacity)
            current_bin.add_item(weight)

    return len(warehouse.get_bins())

def generate_uneven_distribution(n, size):
    result = []
    if n < 4:
        for _ in range(size):
            result.append(n)
        return result
    for _ in range(size):
        dist = random.random()
        if dist < 0.60:  # 60% probability
            # Generate a number in the lower range
            result.append(random.randint(1, n // 4))
        elif dist < 0.85:  # 25% probability
            result.append(random.randint(n // 4 + 1, n // 2))
        elif dist < 0.95:  # 10% probability
            result.append(random.randint(n // 2 + 1, 3 * n // 4))
        else:
            result.append(random.randint(3 * n // 4 + 1, n))

    return result

def home_screen(screen):

    # Font size of title and buttons
    start_title_font = pygame.font.Font(None, 100)
    button_font = pygame.font.Font(None, 70)

    # Fill the screen with a light color
    screen.fill((255, 255, 255))

    # Add a cleaner, simpler background image
    bg = pygame.image.load("warehouse.png")
    screen.blit(bg, (0, 0))

    # Create the title text
    title_text = start_title_font.render("Bin Sorting", True, (255, 255, 255))  # Title text

    # Create a semi-transparent background for the title text
    title_surface = pygame.Surface((title_text.get_width() + 20, title_text.get_height() + 20), pygame.SRCALPHA)
    title_surface.fill((0, 0, 0, 180))  # Black with 70% transparency
    title_surface.blit(title_text, (10, 10))

    # Position the title at the top-center of the screen
    title_rectangle = title_surface.get_rect(center=(screen.get_width() // 2, 150))
    screen.blit(title_surface, title_rectangle)

    # Render the start and quit buttons with new spacing
    start_text = button_font.render("Start", True, (255, 255, 255))
    quit_text = button_font.render("Quit", True, (255, 255, 255))

    # Make surfaces with padding around the text for the buttons, adjusting sizes to fit exactly
    start_surface = pygame.Surface((start_text.get_width() + 20, start_text.get_height() + 20), pygame.SRCALPHA)
    start_surface.fill((0, 0, 0, 180))  # Semi-transparent background for the button
    start_surface.blit(start_text, (10, 10))

    quit_surface = pygame.Surface((quit_text.get_width() + 20, quit_text.get_height() + 20), pygame.SRCALPHA)
    quit_surface.fill((0, 0, 0, 180))  # Semi-transparent background for the button
    quit_surface.blit(quit_text, (10, 10))

    # Position the buttons below the title with adequate space
    start_rectangle = start_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 50))
    quit_rectangle = quit_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 150))

    # Draw the buttons
    screen.blit(start_surface, start_rectangle)
    screen.blit(quit_surface, quit_rectangle)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            # Check where the user clicked and either start the game or quit
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_rectangle.collidepoint(event.pos):
                    return
                elif quit_rectangle.collidepoint(event.pos):
                    sys.exit()

        pygame.display.update()

def main():
    print("Hello World")


if __name__ == "__main__":
    main()
