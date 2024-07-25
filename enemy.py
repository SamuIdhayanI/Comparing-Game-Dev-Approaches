import pygame


class Enemy(pygame.sprite.Sprite):
    ''' reason to make a class is all enemies should not be doing the same thing:
    ie. one should be walking , while one is dead, and other be attacking '''

    def __init__(self, health, animation_list, x, y, speed):
        pygame.sprite.Sprite.__init__(self)  # inheriting
        self.alive = True  # at first all are alive
        self.speed = speed
        self.health = health
        self.last_attack = pygame.time.get_ticks()  # gap btw attacks
        self.attack_cooldown = 1000  # timer for next attack
        self.animation_list = animation_list
        self.frame_index = 0  # 1 to 20 different images
        self.action = 0  # 0: walk, 1: attack, 2: death
        self.update_time = pygame.time.get_ticks()

        # select starting image
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = pygame.Rect(0, 0, 25, 40)  # making our own rectangle around enemy
        self.rect.center = (x, y)

    def update(self, surface, target, bullet_group):  # remember 'target' is castle
        if self.alive:

            # check for collision with bullets
            if pygame.sprite.spritecollide(self, bullet_group, True):  # this 'True' makes bullets disappear once they touch enemies
                # lower enemy's health
                self.health -= 25

            # check if enemy has reached the castle
            if self.rect.right > target.rect.left:
                self.update_action(1)

            # move enemy
            if self.action == 0:
                # update rectangle position
                self.rect.x += self.speed

            # attack
            if self.action == 1:
                # check if enough time has passed since last attack
                if pygame.time.get_ticks() - self.last_attack > self.attack_cooldown:
                    target.health -= 25
                    if target.health < 0:
                        target.health = 0
                    self.last_attack = pygame.time.get_ticks()

            # check if health has dropped to zero
            if self.health <= 0:
                target.money += 100
                target.score += 100
                self.update_action(2)  # death
                self.alive = False


        self.update_animation()

        # draw image on screen
        surface.blit(self.image, (self.rect.x - 10, self.rect.y - 15))

    def update_animation(self):
        # define animation cooldown
        ANIMATION_COOLDOWN = 50

        # update image depending on current action
        self.image = self.animation_list[self.action][self.frame_index]

        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        # if the animation has run out then reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 2:  # if death, stop animating
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

    def update_action(self, new_action):
        # check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # update the animation settings
            self.frame_index = 0  # resetting to the start animation
            self.update_date = pygame.time.get_ticks()
