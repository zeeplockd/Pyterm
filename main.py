import pygame
import sys
import os
import time

# Initialize Pygame
pygame.init()

# Constants
FONT_SIZE = 16 # Size of font
FONT_PATH = "font.ttf" # Path to font file
TEXT_COLOR = (170, 170, 170) # Text color
BG_COLOR = (0, 0, 0) # Background color
WRAP_PREFIX = "   -" # Prefix for wrapped lines
SHELL_PREFIX = "\n> " # Prefix for shell
GOOD_KEYS = {pygame.K_SPACE} | set(range(pygame.K_a, pygame.K_z + 1)) # Not used right now but might be implemented later

# Initialize the screen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Fullscreen mode
screen_width, screen_height = screen.get_size()

# Load the custom font
if not os.path.exists(FONT_PATH):
    print(f"Font file '{FONT_PATH}' not found. Please download it and place it in the same directory as this script.")
    pygame.quit()
    sys.exit()

font = pygame.font.Font(FONT_PATH, FONT_SIZE)
line_height = int(FONT_SIZE)

# Function to render text with letter-based word wrapping
def render_text(surface, text, x, y, color, scroll_offset):
    lines = text.split("\n")  # Split the text into separate lines
    max_width = screen_width
    current_y = y - scroll_offset  # Apply the scroll offset

    for line in lines:
        # Break the line into characters for letter-based wrapping
        current_line = ""
        for char in line:
            test_line = current_line + char
            test_width = font.size(test_line)[0]

            if test_width > max_width and current_line:
                # Render the current line
                if 0 <= current_y < screen_height:
                    line_surface = font.render(current_line, True, color)
                    surface.blit(line_surface, (x, current_y))

                # Move to the next line with the prefix
                current_line = WRAP_PREFIX + char
                current_y += line_height
            else:
                current_line = test_line

        # Render any remaining text in the current line
        if current_line:
            if 0 <= current_y < screen_height:
                line_surface = font.render(current_line, True, color)
                surface.blit(line_surface, (x, current_y))
            current_y += line_height

    return current_y  # Return the current y position for further alignment if needed

# Main loop
def main():
    clock = pygame.time.Clock()
    running = True

    # Calculate the starting x and y positions to remove margins
    start_x = 0  # No left margin
    start_y = 0  # No top margin

    # Scroll parameters
    scroll_offset = 0
    auto_scroll = True

    # Hold detection
    hold_start_time = None
    holding_up = False
    holding_down = False
    
    pygame.mouse.set_visible(False)
    
    # Initialize text content
    text_content = "Automatically logged in as (root)\n "
    
    text_content = text_content + SHELL_PREFIX
    
    shell_ready = True
    shell_entered_text = ""

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Handle manual scrolling
            if event.type == pygame.KEYDOWN:
                if event.mod & pygame.KMOD_CTRL:  # Check if Ctrl is pressed
                    if event.key == pygame.K_UP:
                        if hold_start_time is None:
                            hold_start_time = time.time()
                        holding_up = True
                        holding_down = False
                        scroll_offset = max(0, scroll_offset - line_height)
                        auto_scroll = False
                    elif event.key == pygame.K_DOWN:
                        if hold_start_time is None:
                            hold_start_time = time.time()
                        holding_down = True
                        holding_up = False
                        scroll_offset += line_height
                        auto_scroll = False
                elif event.key == pygame.K_BACKSPACE:
                    text_content = text_content[0:-1]
                elif event.key == pygame.K_RETURN:
                    shell_entered_text = "temporary"
                    text_content += SHELL_PREFIX
                # elif event.key in GOOD_KEYS:
                else:
                    text_content += event.unicode

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    holding_up = False
                    holding_down = False
                    hold_start_time = None

        # Handle scrolling on key hold
        if hold_start_time is not None:
            elapsed_time = time.time() - hold_start_time
            if elapsed_time >= 1:  # After 2 seconds of holding
                if holding_up:
                    scroll_offset = max(0, scroll_offset - line_height)
                    pygame.time.wait(50)  # Wait 100ms between scrolls
                elif holding_down:
                    scroll_offset += line_height
                    pygame.time.wait(50)  # Wait 100ms between scrolls

        # Auto-scroll if enabled and near the bottom
        if auto_scroll:
            total_height = render_text(screen, text_content, start_x, start_y, TEXT_COLOR, 0)
            if scroll_offset + screen_height < total_height:
                scroll_offset += line_height

        # Clear the screen
        screen.fill(BG_COLOR)

        # Render the text with the current scroll offset
        render_text(screen, text_content, start_x, start_y, TEXT_COLOR, scroll_offset)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
