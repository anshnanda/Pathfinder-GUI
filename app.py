import tkinter
from queue import PriorityQueue
import pygame
import sys
import math

window = pygame.display.set_mode((1000, 1000))
ROWS = 50

# Color codes found on an online python forum - reorganized into a dictionary
pygame_colors = {
'white': ((255,255,255)),
'blue': ((0,0,255)),
'green': ((0,255,0)),
'red': ((255,0,0)),
'black': ((0,0,0)),
'orange': ((255,100,10)),
'yellow': ((255,255,0)),
'blue-green': ((0,255,170)),
'marroon':((115,0,0)),
'lime': ((180,255,100)),
'pink': ((255,100,180)),
'purple' : ((240,0,255)),
'gray' : ((127,127,127)),
'magenta' : ((255,0,230)),
'brown' : ((100,40,0)),
'forest_green' : ((0,50,0)),
'navy_blue' : ((0,0,100)),
'rust' : ((210,150,75)),
'dandilion_yellow' : ((255,200,0)),
'highlighter' : ((255,255,100)),
'sky_blue' : ((0,255,255)),
'light_gray' : ((200,200,200)),
'dark_gray' : ((50,50,50)),
'tan' : ((230,220,170)),
'coffee_brown' : ((200,190,140)),
'moon_glow' : ((235,245,255))
}

class Point():
    def __init__(self, row, col, width):
        self.r = row
        self.c = col
        self.x = row * width
        self.y = col * width
        self.color = pygame_colors['white']
        self.adj = []
        self.prev = None
        self.w = width
         
    def position(self):
        return (self.r, self.c)
    
    def is_open(self):
        return self.color == pygame_colors['green']
        
    def is_closed(self):
        return self.color == pygame_colors['red']

    def is_wall(self):
        return self.color == pygame_colors['black']
    
    def set_color(self, color):
        self.color = pygame_colors[color]
    
    def draw(self):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.w, self.w))

    def get_neighbors(self, grid):
        # Neighbor above current point
        if self.r > 0:
            above = grid[self.r - 1][self.c]
            if not above.is_wall():
                self.adj.append(above)
        
        # Neighbor below current point
        if self.r < ROWS - 1:
            below = grid[self.r + 1][self.c]
            if not below.is_wall():
                self.adj.append(below)
        
        # Neighbor left of current point
        if self.c > 0:
            left = grid[self.r][self.c - 1]
            if not left.is_wall():
                self.adj.append(left)

        # Neighbor right of current point
        if self.c < ROWS - 1:
            right = grid[self.r][self.c + 1]
            if not right.is_wall():
                self.adj.append(right)
def make_path(points, current, draw_func):
    while current in points:
        current = current.prev
        current.set_color('pink')
        draw_func()

#Heuristic function - finds Euclidian distance between 2 points
def h(p1, p2):
    distance = math.sqrt((p1.x - p2.x) ** 2 + (p2.y - p2.y) ** 2)
    return distance
    
def a_star(draw_func, grid, start, end):
    count = 0
    open = PriorityQueue()
    open.put((0, count, start))
    f = {point: float('inf') for row in grid for point in row}
    f[start] = h(start, end)
    g = {point: float('inf') for row in grid for point in row}
    g[start] = 0
    so_far = {}
    points = [start]

    while not open.empty():

        curr_point = open.get()[2]
        points.remove(curr_point)

        if curr_point == end:
            make_path(so_far, curr_point, draw_func)
            end.set_color('yellow')
            return True
        
        for adj in curr_point.adj:
            temp = g[curr_point] + 1
            if temp < g[adj]:
                adj.prev = curr_point
                so_far[adj] = curr_point
                g[adj] = temp
                f[adj] = temp + h(adj, end)
                if adj not in points:
                    count += 1
                    open.put((f[adj], count, adj))
                    points.append(adj)
                    adj.set_color('green')
        
        draw_func()

        if curr_point != start:
            curr_point.set_color('red')

    return False

def draw_grid(r, w):
    for x in range(r):
        pygame.draw.line(window, pygame_colors['gray'],
        (0, x * (w // r)), (w, x * (w // r)))
        for y in range(r):
            pygame.draw.line(window, pygame_colors['gray'],
        (y * (w // r), 0), (y * (w // r), w))

def draw(window, grid, r, w):
    window.fill(pygame_colors['white'])
    
    for row in grid:
        for p in row:
            p.draw()
    
    draw_grid(r, w)
    pygame.display.update()

def clicked(pos, r, w):
    y, x = pos
    row = y // (w // r)
    col = x // (w // r)
    return row, col

def main(window, w):
    total_rows = ROWS
    grid = []
    for x in range(total_rows):
        curr_row = []
        for y in range(total_rows):
            curr_point = Point(x, y, w // total_rows)
            curr_row.append(curr_point)
        grid.append(curr_row)

    start, end = None, None

    running = False
    while True:
        draw(window, grid, total_rows, 1000)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
            if running:
                continue

            #Handle Left Click
            if pygame.mouse.get_pressed()[0]:
                row, col = clicked(pygame.mouse.get_pos(), total_rows, w)
                curr_point = grid[row][col]
                if not start and curr_point != end:
                    start = curr_point
                    start.set_color('sky_blue')
                elif not end and curr_point != start:
                    end = curr_point
                    end.set_color('yellow')
                elif curr_point != start and curr_point != end:
                    curr_point.set_color('black')

            #Handle Right Click
            elif pygame.mouse.get_pressed()[2]:
                row, col = clicked(pygame.mouse.get_pos(), total_rows, w)
                curr_point = grid[row][col]
                curr_point.reset()
                if curr_point == start:
                    start = None
                elif curr_point == end:
                    end = None
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for point in row:
                            point.get_neighbors(grid)

                    a_star(lambda: draw(window, grid, total_rows, w), grid, start, end)
                

    pygame.display.quit()

main(window, 1000)