# -*- coding: utf-8 -*-
"""
Author: Connor Hardin
Program Name: SpaceInvaders.py
"""

import pygame, sys
from player import Player
from alien import Alien, Extra
from random import choice, randint
from laser import Laser


class Game:
    def __init__(self):
        player_sprite = Player((screen_width / 2, screen_height), screen_width, screen_height, 5)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        #health and score setup
        self.lives = 3
        self.live_surf = pygame.image.load('./data/ship.png')
        self.live_surf = pygame.transform.scale(self.live_surf, (40, 40))
        self.live_x_start_pos = screen_width - (self.live_surf.get_size()[0] * 2 + 20)
    self.score = 0
    self.font = pygame.font.Font('./data/Pixeled.ttf',20)

    #alien setup
    self.aliens = pygame.sprite.Group()
    self.alien_lasers = pygame.sprite.Group()
    self.alien_setup(rows = 6, cols = 10)
    self.alien_direction = 1

    self.extra = pygame.sprite.GroupSingle()
    self.extra_spawn_time = randint(40,80)

    def alien_setup(self, rows, cols, x_distance = 60, y_distance = 48, x_offset = 70, y_offset = 100):
        for row_index,row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset

                if row_index == 0: alien_sprite = Alien('yellow',x,y)
                elif 1 <= row_index <=2: alien_sprite = Alien('green',x,y)
                else: alien_sprite = Alien('red',x,y)
                self.aliens.add(alien_sprite)

    def alien_position_checker(self):
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.right >= screen_width:
                self.alien_direction = -1
                self.alien_move_down(2)
            elif alien.rect.left <= 0:
                self.alien_direction = 1
                self.alien_move_down(2)

    def alien_move_down(self,distance):
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y += distance

    def alien_shoot(self):
        if self.aliens.sprites():
            random_alien = choice(self.aliens.sprites())
            laser_sprite = Laser(random_alien.rect.center,6,screen_height)
            self.alien_lasers.add(laser_sprite)

    def extra_alien_timer(self):
        self.extra_spawn_time -= 1
        if self.extra_spawn_time <= 0:
            self.extra.add(Extra(choice(['right','left']),screen_width))
            self.extra_spawn_time = randint(400,800)

    def collision_checks(self):
        #player lasers
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                #alien collisions
                aliens_hit = pygame.sprite.spritecollide(laser,self.aliens,True)
                if aliens_hit:
                    for alien in aliens_hit:
                        self.score += alien.value
                    laser.kill()

                #extra collisions
                if pygame.sprite.spritecollide(laser,self.extra,True):
                    self.score += 500
                    laser.kill()
                    

        #Alien Lasers
        if self.alien_lasers:
            for laser in self.alien_lasers:
                if pygame.sprite.spritecollide(laser,self.player,False):
                    laser.kill()
                    self.lives -= 1
                    if self.lives <= 0:
                        pygame.quit()
                        sys.exit()

    def display_lives(self):
        for live in range(self.lives - 1):
            x = self.live_x_start_pos + (live * (self.live_surf.get_size()[0] + 10))
            screen.blit(self.live_surf,(x,8))

    def display_score(self):
        score_surf = self.font.render(f'score: {self.score}', False, 'white')
        score_rect = score_surf.get_rect(topleft = (10,-10))
        screen.blit(score_surf, score_rect)

    def run(self):
        self.player.update()
        self.alien_lasers.update()
        self.extra.update()
        
        self.aliens.update(self.alien_direction)
        self.alien_position_checker()
        self.extra_alien_timer()
        self.collision_checks()

        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)
        self.aliens.draw(screen)
        self.alien_lasers.draw(screen)
        self.extra.draw(screen)
        self.display_lives()
        self.display_score()

if __name__  == '__main__':
    pygame.init()
    screen_width = 750
    screen_height = 700
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Space Invaders")
    clock = pygame.time.Clock()
    game = Game()

    ALIENLASER = pygame.USEREVENT + 1
    pygame.time.set_timer(ALIENLASER,800)

    while True:
        #Checking for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == ALIENLASER:
                game.alien_shoot()
        
        screen.fill((34, 50, 92))
        game.run()

        pygame.display.flip()
        clock.tick(60)