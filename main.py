import pygame
from pygame.locals import *
import sys

from Solver import Solver

if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.set_caption("SudukuSolver")
    screen = pygame.display.set_mode((1000, 700))
    scr_w = screen.get_width()
    scr_h = screen.get_height()
    font = pygame.font.SysFont('lucidaconsole', 60)
    font2 = pygame.font.SysFont('lucidaconsole', 20)
    solver = Solver(screen)
    tick = 0
    while 1:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            if event.type == KEYDOWN and event.key == pygame.K_t:
                solver.ticking = not solver.ticking
            if event.type == KEYDOWN and event.key == pygame.K_LEFT:
                solver.solving = True
                tick += 10

        screen.fill((255,255,255))
        solver.draw()
        solver.take_input()
        if solver.solving:
            solver.solve(tick)
            if solver.ticking:
                tick += 1
        pygame.display.update()
