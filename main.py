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

def draw_parameter_screen(screen):
    pygame.font.init()
    title_font = pygame.font.Font(None, 100)
    input_font = pygame.font.Font(None, 50)
    label_font = pygame.font.Font(None, 40)
    error_font = pygame.font.Font(None, 35)

    screen.fill((255, 255, 255))

    # Title
    title_text = title_font.render("Data Input", True, (0, 0, 0))
    title_rectangle = title_text.get_rect(center=(screen.get_width() // 2, 100))
    screen.blit(title_text, title_rectangle)

    # Input fields and labels
    labels = ["Number of Items", "Max Weight", "Bin Capacity"]
    label_x = 50  # X position for labels
    input_boxes = [pygame.Rect(300, 200 + i * 100, 200, 50) for i in range(3)]
    inputs = ["", "", ""]  # To store text for each input field
    active_box = None  # To track the currently active box

    errors = []  # List to store error messages, persists between frames

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Mouse click: Detect active input box
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, box in enumerate(input_boxes):
                    if box.collidepoint(event.pos):
                        active_box = i
                        break
                else:
                    active_box = None  # Deselect all boxes if clicked outside

            # Handle keyboard input
            if event.type == pygame.KEYDOWN and active_box is not None:
                if event.key == pygame.K_RETURN:
                    # Reset errors and validate inputs
                    errors.clear()
                    try:
                        # Convert inputs to integers
                        num_items = int(inputs[0]) if inputs[0] else 0
                        max_weight = int(inputs[1]) if inputs[1] else 0
                        bin_capacity = int(inputs[2]) if inputs[2] else 0

                        # Validate constraints
                        if num_items < 100000 or num_items > 500000:
                            errors.append("Number of Items must be between")
                            errors.append("100,000 and 500,000.")
                        if max_weight < 1:
                            errors.append("Max Weight must be at least 1.")
                        if bin_capacity < max_weight:
                            errors.append("Bin Capacity must be at least Max Weight.")

                        # If no errors, return the valid inputs as a tuple
                        if not errors:
                            return num_items, max_weight, bin_capacity

                    except ValueError:
                        errors.append("All fields must be valid integers.")

                elif event.key == pygame.K_BACKSPACE:
                    inputs[active_box] = inputs[active_box][:-1]
                else:
                    inputs[active_box] += event.unicode

        # Draw screen elements
        screen.fill((255, 255, 255))
        screen.blit(title_text, title_rectangle)

        for i, (label, box, input_text) in enumerate(zip(labels, input_boxes, inputs)):
            # Draw labels
            label_surface = label_font.render(label, True, (0, 0, 0))
            screen.blit(label_surface, (label_x, box.y + 10))  # Place labels to the left of boxes

            # Draw input box
            color = (0, 128, 255) if active_box == i else (200, 200, 200)
            pygame.draw.rect(screen, color, box, 2)

            # Draw input text
            text_surface = input_font.render(input_text, True, (0, 0, 0))
            screen.blit(text_surface, (box.x + 5, box.y + 10))

        # Display error messages
        y_offset = 500  # Shift errors a little lower so they're more centered
        for error in errors:
            error_surface = error_font.render(error, True, (255, 0, 0))
            screen.blit(error_surface, (50, y_offset))
            y_offset += 40  # Move down for the next line

        pygame.display.update()


def main():
    print("Hello World")


if __name__ == "__main__":
    main()
