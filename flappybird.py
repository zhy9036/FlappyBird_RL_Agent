
#!/usr/bin/env python

import pygame
from pygame.locals import *  # noqa
import sys
import random
import time


IMAGES = {} #dict for score digit font

class FlappyBird:
    def __init__(self):
        self.screen = pygame.display.set_mode((400, 720))
        self.bird = pygame.Rect(50, 50, 30, 41)
        self.offset = random.randint(-11, 11) * 10
       
        self.background = pygame.image.load("assets/background.png").convert()
        self.birdSprites = [pygame.image.load("assets/1.png").convert_alpha(),
                            pygame.image.load("assets/2.png").convert_alpha(),
                            pygame.image.load("assets/dead.png")]
        self.wallUp = pygame.image.load("assets/bottom.png").convert_alpha()
        self.wallDown = pygame.image.load("assets/top.png").convert_alpha()
        self.gap = 130
        self.wallx = 400
        self.birdY = 350
        self.q_value = {}
        self.jump = 0
        self.jumpSpeed = 30
        self.gravity = 5
        self.dead = False
        self.sprite = 0
        self.counter = 0
        self.upRect = pygame.Rect(self.wallx,
                             450  - self.offset,
                             self.wallUp.get_width() - 10,
                             self.wallUp.get_height())
        self.downRect = pygame.Rect(self.wallx,
                               -230 - self.offset,
                               self.wallDown.get_width() - 10,
                               self.wallDown.get_height())
        IMAGES['numbers'] = (
        pygame.image.load('assets/numbers/0.png').convert_alpha(),
        pygame.image.load('assets/numbers/1.png').convert_alpha(),
        pygame.image.load('assets/numbers/2.png').convert_alpha(),
        pygame.image.load('assets/numbers/3.png').convert_alpha(),
        pygame.image.load('assets/numbers/4.png').convert_alpha(),
        pygame.image.load('assets/numbers/5.png').convert_alpha(),
        pygame.image.load('assets/numbers/6.png').convert_alpha(),
        pygame.image.load('assets/numbers/7.png').convert_alpha(),
        pygame.image.load('assets/numbers/8.png').convert_alpha(),
        pygame.image.load('assets/numbers/9.png').convert_alpha()
        )
        with open("q_value") as f:
            for line in f:
                pair = line.split(":")
                self.q_value[eval(pair[0])] = eval(pair[1])
        

    
    def showScore(self, score):
        """displays score in center of screen"""
        scoreDigits = [int(x) for x in list(str(score))]
        totalWidth = 0 # total width of all numbers to be printed

        for digit in scoreDigits:
            totalWidth += IMAGES['numbers'][digit].get_width()

        Xoffset = (400 - totalWidth) / 2

        for digit in scoreDigits:
            self.screen.blit(IMAGES['numbers'][digit], (Xoffset, 720 * 0.1))
            Xoffset += IMAGES['numbers'][digit].get_width()


    def colliBot(self, rect1, rect2):
        if rect1.right >= rect2.left and rect1.left <= rect2.right and (rect1.bottom >= rect2.top):
            #print rect1.bottom, rect2.top
            return True
        return False

    def colliTop(self, rect1, rect2):
        if rect1.right >= rect2.left and rect1.left <= rect2.right and (rect1.top <= rect2.bottom):
            #print rect1.top, rect2.bottom
            return True
        return False

    def birdUpdate(self):

        if self.dead:
            self.bird[1] = 50
            #self.birdY = 50
            self.dead = False
            self.counter = 0
            self.wallx = 400
            self.offset = random.randint(-11, 11) * 10
            self.gravity = 5
        else:
            if self.jump > 0:
                self.wallx -= 5
                self.jumpSpeed -= 5
                self.bird.top -= self.jumpSpeed
                self.jump -= 5
            else:
                self.wallx -= 5
                self.bird.top += self.gravity
                self.gravity += 5
            if self.wallx < -80:
                self.wallx = 400
                self.counter += 1
                self.offset = random.randint(-11, 11) * 10
        #self.bird[1] = self.birdY
        self.upRect = pygame.Rect(self.wallx,
                             450 - self.offset,
                             self.wallUp.get_width() - 10,
                             self.wallUp.get_height())
        self.downRect = pygame.Rect(self.wallx,
                               -230 -self.offset,
                               self.wallDown.get_width() - 10,
                               self.wallDown.get_height())
        if self.colliBot(self.bird, self.upRect):
            self.dead = True
            #print 'down'
        #if self.upRect.colliderect(self.bird):
        #    self.dead = True
        #    print 'down'
        if self.colliTop(self.bird, self.downRect):
            self.dead = True
            #print 'up'
        #if self.downRect.colliderect(self.bird):
        #    self.dead = True
        #    print 'up'
        if not 0 < self.bird[1] < 720:
            self.dead = True
    def ui_update(self):
        self.birdUpdate()
        #self.updateWalls()

        self.screen.fill((255, 255, 255))
        self.screen.blit(self.background, (0, 0))
        #self.screen.blit(self.wallUp,(self.wallx, 360 + self.gap - self.offset))
        self.screen.blit(self.wallUp,(self.upRect.left, self.upRect.top - 10))
        #self.screen.blit(self.wallDown,(self.wallx, 0 - self.gap - self.offset))
        self.screen.blit(self.wallDown,(self.downRect.left, self.downRect.top))
       
        if self.dead:
            self.sprite = 2
        elif self.jump:
            self.sprite = 1
        self.screen.blit(self.birdSprites[self.sprite], (self.bird.left, self.bird.top))
        if not self.dead:
            self.sprite = 0

        
        #self.birdUpdate()
        #self.updateWalls()
        self.showScore(self.counter)

        pygame.display.update()
        
    
    def action_jump(self):
        self.jump = 30
        self.gravity = 5
        self.jumpSpeed = 30

    # ai_mode true for ai play otherwise for human play
    def run(self, ai_mode):
        clock = pygame.time.Clock()
        cur_max = 0;
        i = 0
        while True:
            clock.tick(180)
            
            if not ai_mode:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    if (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN) and not self.dead:
                        self.action_jump()
                self.ui_update()
            else:
                i += 1
                pos_x = self.bird.right - self.upRect.right
                pos_y = self.bird.bottom - self.upRect.top
                cur_state = (pos_x, pos_y)
                if cur_state not in self.q_value:
                    self.q_value[cur_state] = [0.0, 0.0]
                action = 0
                
                val = self.q_value[cur_state]
                action = val.index(max(val))
                if action == 1:
                    self.action_jump()

                self.ui_update()
                next_pos_x = self.bird.right - self.upRect.right
                next_pos_y = self.bird.bottom - self.upRect.top
                next_state = (next_pos_x, next_pos_y)
                reward = 1
                if self.dead:
                    reward = -1000
                if next_state not in self.q_value:
                    self.q_value[next_state] = [0.0, 0.0]

                self.q_value[cur_state][action] += 0.7 * (reward + 1 * max(self.q_value[next_state]) - self.q_value[cur_state][action])


               

                if self.counter > cur_max:
                    cur_max = self.counter
                    sys.stdout.write("\rBest score so far: %d" % cur_max)
                    sys.stdout.flush()    
                    sys.stdout.flush()

                # record q_value every 1000 iterations
                if i == 1000:
                    i = 0
                    with open('q_value', 'wb') as f:
                        for(k, v) in self.q_value.items():
                            f.write('%s:%s\n' % (k, v))


            

if __name__ == "__main__":
    FlappyBird().run(True)
