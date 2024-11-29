import pygame

class player(pygame.sprite.Sprite):
    DIRECTION_RIGHT = 0
    DIRECTION_LEFT = 1
    HEALTH_BAR_COLOR_BG = (255, 255, 255)
    HEALTH_BAR_COLOR = (55, 208, 70)
    def __init__(self, window, health, damage, x, y, direction, speed, cooldown, id):
        '''
        pygame.Surface, int, int, int, int, int, int, int, int -> None.
        The id has a value of 0 if it is the player on the left of the screen at the start, otherwise 1.
        '''
        super().__init__()

        self.health = health
        self.damage = damage
        self.direction = direction
        self.speed = speed
        self.id = id
        self.cooldown = cooldown
        self.recovery_time = self.cooldown + 1
        self.current_sprite_index = 0
        self.window = window

        self.idle_sprites_left = self.import_sprites(
            ['./art/idle-left-1.png', './art/idle-left-2.png'])
        self.idle_sprites_right = self.import_sprites(
            ['./art/idle-right-1.png', './art/idle-right-2.png'])
        self.attack_sprites_left = self.import_sprites(
            ['./art/attack-left-1.png', './art/attack-left-2.png'])
        self.attack_sprites_right = self.import_sprites(
            ['./art/attack-right-1.png', './art/attack-right-2.png'])

        if self.direction == player.DIRECTION_RIGHT:
            self.image = self.idle_sprites_right[self.current_sprite_index]
        else:
            self.image = self.idle_sprites_left[self.current_sprite_index]

        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]

        # GUI rects
        if self.id == 0:
            self.health_bar_background = pygame.Rect(20, 30, self.health, 30)
            self.health_bar = pygame.Rect(20, 30, self.health, 30)
        else:
            self.health_bar_background = pygame.Rect(20, 80, self.health, 30)
            self.health_bar = pygame.Rect(20, 80, self.health, 30)

    def import_sprites(self, images):
        '''
        [str] -> [pygame.Surface]
        Utility methods wich import the sprites scaled to fit specific needs.
        '''
        sprites = []
        for image in images:
            img_load = pygame.image.load(image)
            scaled = pygame.transform.scale(img_load, (img_load.get_rect().width * 2, img_load.get_rect().height * 2))
            sprites.append(scaled)
        return sprites

    def update(self):
        '''
        None -> None
        Updates the current sprite of each character.
        '''
        self.current_sprite_index += 0.1

        if self.direction == player.DIRECTION_RIGHT:
            if self.current_sprite_index >= len(self.idle_sprites_right):
                self.current_sprite_index = 0

            self.image = self.idle_sprites_right[int(self.current_sprite_index)]

        else:
            if self.current_sprite_index >= len(self.idle_sprites_left):
                self.current_sprite_index = 0

            self.image = self.idle_sprites_left[int(self.current_sprite_index)]

    def update_inputs(self, enemy):
        '''
        player -> None
        Moves and orients the character according to the key pressed.
        '''
        keys = pygame.key.get_pressed()
        self.recovery_time += 1

        # Left player
        if self.id == 0:
            if keys[pygame.K_q]:
                self.rect.x -= self.speed
                self.direction = player.DIRECTION_LEFT

            elif keys[pygame.K_d]:
                self.rect.x += self.speed
                self.direction = player.DIRECTION_RIGHT

            elif keys[pygame.K_v]:
                self.attack(enemy)
        # Right player
        else:
            if keys[pygame.K_LEFT]:
                self.rect.x -= self.speed
                self.direction = player.DIRECTION_LEFT

            elif keys[pygame.K_RIGHT]:
                self.rect.x += self.speed
                self.direction = player.DIRECTION_RIGHT

            elif keys[pygame.K_m]:
                self.attack(enemy)

        win_w = self.window.get_width()
        win_h = self.window.get_height()

        self.rect.clamp_ip((0, 0, win_w, win_h))

    def update_gui(self):
        '''
        None -> None
        Updates the GUI related to the player.
        '''
        self.health_bar.width = self.health

        pygame.draw.rect(self.window, player.HEALTH_BAR_COLOR_BG, self.health_bar_background)
        pygame.draw.rect(self.window, player.HEALTH_BAR_COLOR, self.health_bar)

    def attack(self, enemy):
        '''
        player -> None
        Allows the character to attack another character (takes away a certain number of HP from the latter).
        '''
        if self.recovery_time > self.cooldown:
            if self.direction == player.DIRECTION_RIGHT:
                for i in range(len(self.attack_sprites_right)):
                    self.image = self.attack_sprites_right[i]

            else:
                for i in range(len(self.attack_sprites_left)):
                    self.image = self.attack_sprites_left[i]

            if self.rect.colliderect(enemy.rect):
                if self.direction == player.DIRECTION_RIGHT and self.rect.x < enemy.rect.x or \
                    self.direction == player.DIRECTION_LEFT and self.rect.x > enemy.rect.x:
                    if enemy.health - self.damage < 0:
                        enemy.health = 0
                    else:
                        enemy.health -= self.damage

            self.recovery_time = 0
