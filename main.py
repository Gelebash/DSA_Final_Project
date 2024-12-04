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
    title_text = start_title_font.render("Bin Packaging", True, (255, 255, 255))  # Title text

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
        
def draw_bin(screen, t, b, number):
    # Initialize fonts
    title_font = pygame.font.Font(None, 80)
    result_font = pygame.font.Font(None, 40)
    button_font = pygame.font.Font(None, 60)

    # Fill screen with background color
    screen.fill((255, 255, 255))

    # Title text
    title_text = title_font.render(f"Run {number + 1} Stats", True, (0, 0, 0))
    title_rect = title_text.get_rect(center=(screen.get_width() // 2, 50))
    screen.blit(title_text, title_rect)

    # Display bin data
    bin_data = [
        f"Time: {t} seconds",
        f"Bins: {b} bins",
    ]

    # Positioning variables
    y_offset = 150
    spacing = 50

    for data in bin_data:
        bin_text = result_font.render(data, True, (0, 0, 0))
        screen.blit(bin_text, (screen.get_width() // 2 - bin_text.get_width() // 2, y_offset))
        y_offset += spacing

    # Draw the back button
    back_text = button_font.render("Back", True, (255, 255, 255))
    back_surface = pygame.Surface(back_text.get_size(), pygame.SRCALPHA)
    back_surface.fill((0, 0, 0, 180))
    back_surface.blit(back_text, (0, 0))
    back_rect = back_surface.get_rect(center=(screen.get_width() // 2, y_offset + 100))
    screen.blit(back_surface, back_rect)

    # Main event loop for navigating the screen
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Check for mouse clicks on the back button
            if event.type == pygame.MOUSEBUTTONDOWN and back_rect.collidepoint(event.pos):
                return  # Go back to the result screen when the back button is clicked

        pygame.display.update()

def result_screen(screen, nt, nb, ft, fb):
    # Initialize fonts
    title_font = pygame.font.Font(None, 80)
    column_font = pygame.font.Font(None, 60)
    result_font = pygame.font.Font(None, 40)
    button_font = pygame.font.Font(None, 60)

    # Fill screen with background color
    screen.fill((255, 255, 255))

    # Title text
    title_text = title_font.render("Results", True, (0, 0, 0))
    title_rect = title_text.get_rect(center=(screen.get_width() // 2, 50))
    screen.blit(title_text, title_rect)

    # Calculate averages
    avg_first_time = round(sum(ft) / len(ft), 4)
    avg_first_bins = round(sum(fb) / len(fb), 4) // 1
    avg_next_time = round(sum(nt) / len(nt), 4)
    avg_next_bins = round(sum(nb) / len(nb), 4) // 1
    avg_time_ratio = round(avg_first_time / avg_next_time, 4)
    avg_bin_ratio = round(avg_first_bins / avg_next_bins, 4)

    # Column headers
    first_fit_text = column_font.render("First Fit", True, (0, 0, 0))
    next_fit_text = column_font.render("Next Fit", True, (0, 0, 0))
    screen.blit(first_fit_text, (200, 150))
    screen.blit(next_fit_text, (550, 150))  # Shifted right

    # Results display
    first_fit_data = [
        f"Avg Time: {avg_first_time} seconds",
        f"Avg Bins: {int(avg_first_bins)} bins",
    ]
    next_fit_data = [
        f"Avg Time: {avg_next_time} seconds",
        f"Avg Bins: {int(avg_next_bins)} bins",
    ]

    # Positioning variables
    y_offset = 230
    spacing = 50

    # Displaying the results
    for first, next_ in zip(first_fit_data, next_fit_data):
        first_text = result_font.render(first, True, (0, 0, 0))
        next_text = result_font.render(next_, True, (0, 0, 0))
        screen.blit(first_text, (75, y_offset))
        screen.blit(next_text, (480, y_offset))  # Shifted right
        y_offset += spacing


    time_ratio = result_font.render(f"Time Ratio: {avg_time_ratio}", True, (0, 0, 0))
    bin_ratio = result_font.render(f"Bin Ratio: {avg_bin_ratio}", True, (0, 0, 0))
    screen.blit(time_ratio, (75, y_offset + 10))
    screen.blit(bin_ratio, (480, y_offset + 10))

    # Draw vertical line between columns
    pygame.draw.line(screen, (0, 0, 0), (455, 150), (455, y_offset), 3)  # Vertical line

    # Draw horizontal lines between rows
    pygame.draw.line(screen, (0, 0, 0), (50, 200), (screen.get_width() - 50, 200), 3)  # Top line
    pygame.draw.line(screen, (0, 0, 0), (50, y_offset), (screen.get_width() - 50, y_offset), 3) # Bottom line

    # Increase y_offset for bin buttons to avoid overlap
    button_y_offset = y_offset + 100

    button_width = 120  # Button width
    button_height = 50  # Button height

    # Create buttons for First Fit (Bins 1-5)
    first_fit_buttons = []
    for i in range(5):
        button_text = button_font.render(f"Run {i + 1}", True, (255, 255, 255))
        button_surface = pygame.Surface(button_text.get_size(), pygame.SRCALPHA)
        button_surface.fill((0, 0, 0, 180))
        button_surface.blit(button_text, (0, 0))

        # Calculate the button's position
        row_offset = i // 3  # To determine which row the button will be in (0 for the first row, 1 for the second, etc.)
        column_offset = i % 3  # To determine the column in the row (0, 1, 2)

        button_rect = button_surface.get_rect(
            center=(100 + column_offset * button_width,
                    button_y_offset + row_offset * button_height)
        )

        screen.blit(button_surface, button_rect)
        first_fit_buttons.append(button_rect)


    # Create buttons for Next Fit (Bins 6-10)
    next_fit_buttons = []
    for i in range(5):
        button_text = button_font.render(f"Run {i+1}", True, (255, 255, 255))
        button_surface = pygame.Surface(button_text.get_size(), pygame.SRCALPHA)
        button_surface.fill((0, 0, 0, 180))
        button_surface.blit(button_text, (0, 0))

        # Calculate the button's position for "Next Fit" bins
        row_offset = i // 3  # To determine which row the button will be in (0 for the first row, 1 for the second, etc.)
        column_offset = i % 3  # To determine the column in the row (0, 1, 2)

        button_rect = button_surface.get_rect(
            center=(500 + column_offset * button_width,
                    button_y_offset + row_offset * button_height)
        )

        screen.blit(button_surface, button_rect)
        next_fit_buttons.append(button_rect)

    # Draw a button to go back to the home screen or quit
    back_text = button_font.render("Restart", True, (255, 255, 255))
    back_surface = pygame.Surface(back_text.get_size(), pygame.SRCALPHA)
    back_surface.fill((0, 0, 0, 180))
    back_surface.blit(back_text, (0, 0))
    back_rect = back_surface.get_rect(center=(screen.get_width() // 2, button_y_offset + 200))
    screen.blit(back_surface, back_rect)

    # Main event loop for navigating the screen
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Check for mouse clicks on First Fit bin buttons
            for i, button_rect in enumerate(first_fit_buttons):
                if event.type == pygame.MOUSEBUTTONDOWN and button_rect.collidepoint(event.pos):
                    # Pass the corresponding time and bin count for First Fit
                    return [True, ft[i], fb[i], i]

            # Check for mouse clicks on Next Fit bin buttons
            for i, button_rect in enumerate(next_fit_buttons):
                if event.type == pygame.MOUSEBUTTONDOWN and button_rect.collidepoint(event.pos):
                    # Pass the corresponding time and bin count for Next Fit
                    return [True, nt[i], nb[i], i]

            # Check for mouse clicks on the back button
            if event.type == pygame.MOUSEBUTTONDOWN and back_rect.collidepoint(event.pos):
                return ["restart"]  # Exit the result screen and return to the previous screen

        pygame.display.update()

def main():
    pygame.init()
    screen = pygame.display.set_mode((910, 720))
    pygame.display.set_caption("Bin Sorting")

    home_screen_opened = False
    running = True
    backToResult = False
    data_received = False

    while running:
        if not backToResult:
            if not home_screen_opened:
                # Display the home screen
                home_screen(screen)
                home_screen_opened = True

            if not data_received:
                # Draw the parameter input screen and get user inputs
                parameters = draw_parameter_screen(screen)

                # If parameters are valid, proceed with the trials and results
                if parameters:
                    next_times, next_bins, first_times, first_bins = [], [], [], []

                    for _ in range(5):
                        weights = generate_uneven_distribution(parameters[1], parameters[0])

                        # Next Fit Algorithm
                        start_time = time.time()
                        next_trial = next_fit(weights, parameters[2])
                        end_time = time.time()
                        next_times.append(round(end_time - start_time, 5))
                        next_bins.append(next_trial)

                        # First Fit Algorithm
                        start_time = time.time()
                        first_trial = first_fit(weights, parameters[2], parameters[1])
                        end_time = time.time()
                        first_times.append(round(end_time - start_time, 5))
                        first_bins.append(first_trial)
                data_received = True

                # After the trials, show the result screen
            bin_data = result_screen(screen, next_times, next_bins, first_times, first_bins)

            if bin_data[0] == "restart":
                home_screen_opened = False
                data_received = False
            else:
                backToResult = bin_data[0]
                draw_bin(screen, bin_data[1], bin_data[2], bin_data[3])
        else:
            result_screen(screen, next_times, next_bins, first_times, first_bins)
            backToResult = False

        # Main event loop for quitting the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
