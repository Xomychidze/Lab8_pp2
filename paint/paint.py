import pygame
import math

pygame.init()

FPS = 60
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")
CLOCK = pygame.time.Clock()

# canvas
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill((255, 255, 255))


# List of colors
colors = [
    {"name": "white", "image": pygame.image.load("paint/belyi.png"), "color": (255, 255, 255)},
    {"name": "black", "image": pygame.image.load("paint/negr.png"), "color": (0, 0, 0)},
    {"name": "darkRed", "image": pygame.image.load("paint/darkRed.png"), "color": (139, 0, 0)},
    {"name": "gray", "image": pygame.image.load("paint/gray.png"), "color": (128, 128, 128)},
    {"name": "grayLight", "image": pygame.image.load("paint/grayLight.png"), "color": (169, 169, 169)},
    {"name": "lightOrange", "image": pygame.image.load("paint/lightOrange.png"), "color": (255, 140, 0)}
]

# Setting tool button positions
figures = [
    {"name": "rectangle", "image": pygame.image.load("paint/rectangle.png")},
    {"name": "circle", "image": pygame.image.load("paint/circle.png")},
    {"name": "equilateral_triangle", "image": pygame.image.load("paint/triangle.png")},
    {"name": "right_triangle", "image": pygame.image.load("paint/right_triangle.png")},
    {"name": "diamond", "image": pygame.image.load("paint/diamond.png")},
]

# Setting positions of shape buttons
x_offset = 10  # Starting position for the shape
for figure in figures:
    figure["rect"] = figure["image"].get_rect(topleft=(x_offset, 10))
    x_offset += figure["rect"].width + 10

# Setting the position of the color buttons
x_offset = 900  # Starting position for colors
for color in colors:
    color["rect"] = color["image"].get_rect(topleft=(x_offset, 10))
    x_offset += color["rect"].width + 10

# variables
running = True
color_brush = (0, 0, 0)
brush_size = 10
prev_pos = None
current_tool = "brush"
drawing = False
start_pos = None
press = False
preview_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

# Function to check if the color cursor or tool button has been hit
def is_inside_tool_button(pos):
    return any(r["rect"].collidepoint(pos) for r in colors) or any(r["rect"].collidepoint(pos) for r in figures)

# Function for drawing a rectangular triangle
def draw_right_triangle(surface, color, start_pos, end_pos):
    x1, y1 = start_pos
    x2, y2 = end_pos
    points = [(x1, y1), (x1, y2), (x2, y2)]
    pygame.draw.polygon(surface, color, points)

# Function for drawing the right triangle
def draw_equilateral_triangle(surface, color, start_pos, side_length):
    x1, y1 = start_pos
    height = math.sqrt(3) / 2 * side_length  # Right triangle height
    points = [
        (x1, y1),  # Top 1
        (x1 + side_length, y1),  # Top 2
        (x1 + side_length / 2, y1 - height)  # Top 3
    ]
    pygame.draw.polygon(surface, color, points)

while running:
    screen.fill((255, 255, 255))  # Application background
    preview_surface.fill((0, 0, 0, 0))  # Transparent canvas for preview
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Checking the tools to be clicked
            for figure in figures:
                if figure["rect"].collidepoint(pos):
                    current_tool = figure["name"]
                    drawing = False  # Stop drawing if new tool is selected

            # If a shape is selected, start drawing
            if current_tool in ["rectangle", "circle", "diamond", "right_triangle", "equilateral_triangle"]:
                if not is_inside_tool_button(pos):
                    start_pos = pos
                    drawing = True
                    press = True

            # Checking the color selection
            for color in colors:
                if color["rect"].collidepoint(pos):
                    color_brush = color["color"]

        # Painting with a brush and an eraser
        if pygame.mouse.get_pressed()[0] and current_tool in ["brush", "eraser"]:
            if not is_inside_tool_button(pos):
                color = (255, 255, 255) if current_tool == "eraser" else color_brush
                if prev_pos is not None:
                    pygame.draw.line(canvas, color, prev_pos, pos, brush_size * 2)
                prev_pos = pos
        else:
            prev_pos = None

        if event.type == pygame.MOUSEMOTION and drawing:
            end_pos = event.pos

        # Release the mouse - draw a shape
        if event.type == pygame.MOUSEBUTTONUP and drawing:
            LMBpressed = False
            end_pos = event.pos
            x1, y1 = start_pos
            x2, y2 = end_pos
            width = abs(x2 - x1)
            height = abs(y2 - y1)
            top_left = (min(x1, x2), min(y1, y2))

            if current_tool == "rectangle":
                pygame.draw.rect(canvas, color_brush, (*top_left, width, height), 2)
            elif current_tool == "circle":
                radius = max(width, height) // 2
                center = (x1 + (x2 - x1) // 2, y1 + (y2 - y1) // 2)
                pygame.draw.circle(canvas, color_brush, center, radius, 2)
            elif current_tool == "diamond":
                points = [(x1 + width // 2, y1), (x2, y1 + height // 2), (x1 + width // 2, y2), (x1, y1 + height // 2)]
                pygame.draw.polygon(canvas, color_brush, points)
            elif current_tool == "right_triangle":
                draw_right_triangle(canvas, color_brush, start_pos, end_pos)
            elif current_tool == "equilateral_triangle":
                side_length = min(width, height)
                draw_equilateral_triangle(canvas, color_brush, start_pos, side_length)

            drawing = False
            start_pos = None

        # Hotkeys
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                current_tool = "brush"
            elif event.key == pygame.K_e:
                current_tool = "eraser"
            elif event.key == pygame.K_r:
                current_tool = "rectangle"
            elif event.key == pygame.K_c:
                current_tool = "circle"
            elif event.key == pygame.K_d:
                current_tool = "diamond"
            elif event.key == pygame.K_y:  # For a rectangular triangle
                current_tool = "right_triangle"
            elif event.key == pygame.K_u:  # For the right triangle
                current_tool = "equilateral_triangle"

    # Preview of shape display
    if press and start_pos:
        end_pos = event.pos
        x1, y1 = start_pos
        x2, y2 = end_pos
        width = abs(x2 - x1)
        height = abs(y2 - y1)
        top_left = (min(x1, x2), min(y1, y2))

        if current_tool == "rectangle":
            pygame.draw.rect(preview_surface, color_brush, (*top_left, width, height), 2)
        elif current_tool == "circle":
            radius = max(width, height) // 2
            center = (x1 + (x2 - x1) // 2, y1 + (y2 - y1) // 2)
            pygame.draw.circle(preview_surface, color_brush, center, radius, 2)
        elif current_tool == "diamond":
            points = [(x1 + width // 2, y1), (x2, y1 + height // 2), (x1 + width // 2, y2), (x1, y1 + height // 2)]
            pygame.draw.polygon(preview_surface, color_brush, points)
        elif current_tool == "right_triangle":
            draw_right_triangle(preview_surface, color_brush, start_pos, end_pos)
        elif current_tool == "equilateral_triangle":
            side_length = min(width, height)
            draw_equilateral_triangle(preview_surface, color_brush, start_pos, side_length)

    # Drawing canvas and buttons
    screen.blit(canvas, (0, 0))
    screen.blit(preview_surface, (0, 0))
    for figure in figures:
        screen.blit(figure["image"], figure["rect"])
    for color in colors:
        screen.blit(color["image"], color["rect"])

    pygame.display.flip()
    CLOCK.tick(FPS)

pygame.quit()
