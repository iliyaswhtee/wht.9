# import modules
import pygame
import math

# Function to draw a line between two points with a gradient color
def drawLineBetween(screen, index, start, end, width, color_mode):
    # Calculate the color based on the index
    c1 = max(0, min(255, 2 * index - 256))
    c2 = max(0, min(255, 2 * index))

    # Set the color modes
    if color_mode == 'blue':
        color = (c1, c1, c2)
    elif color_mode == 'red':
        color = (c2, c1, c1)
    elif color_mode == 'green':
        color = (c1, c2, c1)

    # Calculate the number of iterations based on the distance between the start and end points (coordination)
    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy))

    # Draw the line
    for i in range(iterations):
        progress = 1.0 * i / iterations
        aprogress = 1 - progress
        x = int(aprogress * start[0] + progress * end[0])
        y = int(aprogress * start[1] + progress * end[1])
        pygame.draw.circle(screen, color, (x, y), width)

# Function to draw a rectangle
def draw_rectangle(screen, start, end, width, color_mode):
    pygame.draw.rect(screen, color_mode, pygame.Rect(start[0], start[1], end[0]-start[0], end[1]-start[1]), width)

# Function to draw a circle
def draw_circle(screen, center, radius, color_mode):
    pygame.draw.circle(screen, color_mode, center, radius)

# Function to erase a portion of the screen
def erase(screen, position, radius):
    pygame.draw.circle(screen, (0, 0, 0), position, radius)

# Function to draw a square
def draw_square(screen, start, end, width, color_mode):
    side = min(abs(end[0]-start[0]), abs(end[1]-start[1]))
    pygame.draw.rect(screen, color_mode, pygame.Rect(start[0], start[1], side, side), width)

# Function to draw a right triangle
def draw_right_triangle(screen, start, end, width, color_mode):
    pygame.draw.polygon(screen, color_mode, [start, end, (start[0], end[1])], width)

# Function to draw an equilateral triangle
def draw_equilateral_triangle(screen, start, end, width, color_mode):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    length = math.sqrt(dx**2 + dy**2)
    height = length * math.sqrt(3) / 2
    point1 = start
    point2 = end
    point3 = (start[0] + length/2, start[1] - height)
    pygame.draw.polygon(screen, color_mode, [point1, point2, point3], width)

# Function to draw a rhombus
def draw_rhombus(screen, start, end, width, color_mode):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    pygame.draw.polygon(screen, color_mode, [start, ((start[0]+end[0])/2, start[1]), end, ((start[0]+end[0])/2, start[1]+dy)], width)

def main():
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()

    # variables
    radius = 15
    mode = 'blue'
    draw_mode = 'line'  
    points = []
    drawing = False
    erasing = False

    # Main loop
    while True:
        # Check for key presses
        pressed = pygame.key.get_pressed()
        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]

        # Event handling
        for event in pygame.event.get():
            # Quit
            if event.type == pygame.QUIT:
                return
            # Key down event
            if event.type == pygame.KEYDOWN:
                # Quit keys
                if event.key == pygame.K_w and ctrl_held:
                    return
                if event.key == pygame.K_F4 and alt_held:
                    return
                if event.key == pygame.K_ESCAPE:
                    return

                # Colors
                if event.key == pygame.K_r:
                    mode = 'red'
                elif event.key == pygame.K_g:
                    mode = 'green'
                elif event.key == pygame.K_b:
                    mode = 'blue'

                # Eraser
                elif event.key == pygame.K_e:
                    erasing = not erasing

                # Draw mode atributes
                elif event.key == pygame.K_1:
                    draw_mode = 'line'
                elif event.key == pygame.K_2:
                    draw_mode = 'rectangle'
                elif event.key == pygame.K_3:
                    draw_mode = 'circle'
                elif event.key == pygame.K_4:
                    draw_mode = 'square'
                elif event.key == pygame.K_5:
                    draw_mode = 'right_triangle'
                elif event.key == pygame.K_6:
                    draw_mode = 'equilateral_triangle'
                elif event.key == pygame.K_7:
                    draw_mode = 'rhombus'

            # Mouse button
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Left button
                if event.button == 1:
                    drawing = True
                    points.append(event.pos)
                # Right button
                elif event.button == 3:
                    erasing = True

            # Mouse button up event
            if event.type == pygame.MOUSEBUTTONUP:
                # Left button
                if event.button == 1:
                    drawing = False
                    points.clear()
                # Right button
                elif event.button == 3:
                    erasing = False

            # motion event
            if event.type == pygame.MOUSEMOTION:
                # Drawing
                if drawing:
                    points.append(event.pos)
                # Erasing
                elif erasing:
                    erase(screen, event.pos, radius)

        # Fill the screen with black
        screen.fill((0, 0, 0))

        # Draw based on the draw mode
        if draw_mode == 'line':
            for i in range(len(points) - 1):
                drawLineBetween(screen, i, points[i], points[i + 1], radius, mode)
        elif draw_mode == 'rectangle' and len(points) >= 2:
            draw_rectangle(screen, points[0], points[-1], radius, mode)
        elif draw_mode == 'circle' and len(points) >= 2:
            center = points[0]
            dx = points[-1][0] - center[0]
            dy = points[-1][1] - center[1]
            radius = int((dx * dx + dy * dy) ** 0.5)
            draw_circle(screen, center, radius, mode)
        elif draw_mode == 'square' and len(points) >= 2:
            draw_square(screen, points[0], points[-1], radius, mode)
        elif draw_mode == 'right_triangle' and len(points) >= 2:
            draw_right_triangle(screen, points[0], points[-1], radius, mode)
        elif draw_mode == 'equilateral_triangle' and len(points) >= 2:
            draw_equilateral_triangle(screen, points[0], points[-1], radius, mode)
        elif draw_mode == 'rhombus' and len(points) >= 2:
            draw_rhombus(screen, points[0], points[-1], radius, mode)

        # Update the display
        pygame.display.flip()
        clock.tick(60)

# Run the main function
if __name__ == "__main__":
    main()