import math

import pygame


class Solver:
    def __init__(self, screen):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.hints = [[[i for i in range(1, 10)] for _ in range(9)] for _ in range(9)]  # num hints

        # self.board = [i*9+j]

        self.scr_w = screen.get_width()
        self.scr_h = screen.get_height()
        self.screen = screen
        self.squaresize = 50
        self.font = pygame.font.SysFont('lucidaconsole', 40)
        self.font2 = pygame.font.SysFont('lucidaconsole', 15)
        self.solving = False
        self.ticking = True

    def draw(self):
        for i in range(10):
            pygame.draw.line(self.screen, (0, 0, 0),
                             (self.scr_w / 2 - self.squaresize * 4.5 + self.squaresize * i,
                              self.scr_h / 2 - self.squaresize * 4.5),
                             (self.scr_w / 2 - self.squaresize * 4.5 + self.squaresize * i,
                              self.scr_h / 2 + self.squaresize * 4.5),
                             width=2 if i % 3 == 0 else 1)
        for i in range(10):
            pygame.draw.line(self.screen, (0, 0, 0),
                             (self.scr_w / 2 - self.squaresize * 4.5,
                              self.scr_h / 2 - self.squaresize * 4.5 + self.squaresize * i),
                             (self.scr_w / 2 + self.squaresize * 4.5,
                              self.scr_h / 2 - self.squaresize * 4.5 + self.squaresize * i),
                             width=2 if i % 3 == 0 else 1)
        for i in range(9):
            for j in range(9):
                if self.board[i][j] not in (0,):
                    self.screen.blit(self.font.render(str(self.board[i][j]), False, (0, 0, 0)),
                                     (self.scr_w / 2 - self.squaresize * 4.5 + self.squaresize * j,
                                      self.scr_h / 2 - self.squaresize * 4.5 + self.squaresize * i))
                for k in range(9):
                    if k+1 in self.hints[i][j]:
                        self.screen.blit(self.font2.render(str(k+1), False, (255, 0, 0)),
                                         (self.scr_w / 2 - self.squaresize * 4.5 + self.squaresize * j + k % 3 * 20,
                                          self.scr_h / 2 - self.squaresize * 4.5 + self.squaresize * i + k // 3 * 20))
        # print(self.board)

    def take_input(self):
        mx, my = pygame.mouse.get_pos()
        if self.scr_w / 2 - self.squaresize * 4.5 < mx < self.scr_w / 2 + self.squaresize * 4.5 and \
                self.scr_h / 2 - self.squaresize * 4.5 < my < self.scr_h / 2 + self.squaresize * 4.5:
            pygame.draw.rect(self.screen, (255, 0, 0),
                             (math.floor((mx - self.scr_w / 2 + self.squaresize / 2) / self.squaresize) *
                              self.squaresize + self.scr_w / 2 - self.squaresize / 2,
                              math.floor((my - self.scr_h / 2 + self.squaresize / 2) / self.squaresize) *
                              self.squaresize + self.scr_h / 2 - self.squaresize / 2,
                              self.squaresize, self.squaresize), width=2)
            pressed_keys = pygame.key.get_pressed()
            for i in range(10):
                if pressed_keys[48 + i]:
                    self.board[math.floor((my - self.scr_h / 2 + self.squaresize / 2) / self.squaresize) + 4] \
                        [math.floor((mx - self.scr_w / 2 + self.squaresize / 2) / self.squaresize) + 4] = i
            if pressed_keys[pygame.K_p]:
                print(self.board)
            if pressed_keys[pygame.K_i]:
                # self.board = eval(input())  # defo really stupid
                self.board = [[0, 0, 0, 3, 0, 7, 0, 0, 0], [0, 1, 0, 4, 0, 0, 6, 0, 0], [7, 0, 0, 0, 0, 0, 0, 9, 0],
                              [9, 0, 0, 0, 0, 0, 5, 0, 7], [0, 7, 3, 1, 6, 0, 0, 0, 4], [0, 0, 0, 0, 0, 0, 0, 0, 6],
                              [0, 8, 0, 0, 0, 1, 4, 0, 0], [0, 6, 0, 0, 7, 5, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 2]]
            if pressed_keys[pygame.K_s]:
                self.solving = True
                print(self.board)
                # print(self.hints)
                self.flush()
                # print(self.board)
                print(self.hints)
                print()
            if pressed_keys[pygame.K_t]:
                #self.ticking = not self.ticking
                pass

    def flush(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] != 0:
                    self.hints[i][j] = []

    def solve(self, tick):
        def crossout(num):
            for i in range(9):
                for j in range(9):
                    if self.board[i][j] == num:
                        for k in range(9):
                            if num in self.hints[i][k] and j != k:
                                self.hints[i][k].remove(num)
                            if num in self.hints[k][j] and i != k:
                                self.hints[k][j].remove(num)
                            if num in self.hints[i // 3 * 3 + k // 3][j // 3 * 3 + k % 3]:
                                self.hints[i // 3 * 3 + k // 3][j // 3 * 3 + k % 3].remove(num)
                    if self.board[i][j] == 0:
                        square = []
                        for k in range(3):
                            square.append([])
                            for l in range(3):
                                square[k].append(self.hints[i // 3 * 3 + k][j // 3 * 3 + l])
                        boardsqr = []
                        for k in range(3):
                            for l in range(3):
                                boardsqr.append(self.board[i // 3 * 3 + k][j // 3 * 3 + l])
                        mainloc = (i % 3, j % 3)
                        inline = [True, True]
                        for k in range(3):
                            for l in range(3):
                                if num in square[k][l]:
                                    if k != mainloc[0]:
                                        inline[0] = False
                                    if l != mainloc[1]:
                                        inline[1] = False
                        if inline[0]:
                            for k in range(9):
                                if num in self.hints[mainloc[0]][k]:
                                    self.hints[mainloc[0]][k].remove(num)
                        if inline[1]:
                            for k in range(9):
                                if num in self.hints[k][mainloc[1]]:
                                    self.hints[k][mainloc[1]].remove(num)


        def fill(num):
            for i in range(9):
                for j in range(9):
                    if len(self.hints[i][j]) == 1:
                        self.board[i][j] = self.hints[i][j][0]
                        self.hints[i][j] = []
                    if self.board[i][j] == 0 and num in self.hints[i][j]:
                        filled = [0, 0, 0]
                        for k in range(9):
                            if num in self.hints[i][k] or self.board[i][k] == num:
                                filled[0] += 1
                            if num in self.hints[k][j] or self.board[k][j] == num:
                                filled[1] += 1
                            if num in self.hints[i // 3 * 3 + k // 3][j // 3 * 3 + k % 3] or \
                                    self.board[i // 3 * 3 + k // 3][j // 3 * 3 + k % 3] == num:
                                filled[2] += 1
                        if min(filled) == 1:
                            self.board[i][j] = num
                            self.hints[i][j] = []
                            # print(filled)
                        # print(i, j, min(filled))

        def complete():
            for i in range(9):
                if self.board[i].count(0) > 0:
                    print(f'Unsolved: {i} {self.board[i].count(0)} {self.board[i]}')
                    return False
            print('Solved')
            return True

        if tick % 30 == 0:
            print(self.hints)
            crossout(int(tick % 270 / 30 + 1))
            print(self.hints)
            print(int(tick % 270 / 30 + 1))
        elif tick % 30 == 10:
            fill(int((tick - 10) % 270 / 30 + 1))
            for i in range(9):
                print(self.hints[i])
        elif tick % 30 == 20:
            if complete():
                self.solving = False

# TODO: fix deleting hints in same row and column bc it totally sucks rn
