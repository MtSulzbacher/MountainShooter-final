#!/usr/bin/python
# -*- coding: utf-8 -*-
from code.Const import ENTITY_SPEED, ENTITY_SHOT_DELAY
from code.EnemyShot import EnemyShot
from code.Entity import Entity


class Enemy(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        self.shot_delay = ENTITY_SHOT_DELAY[self.name]

    def move(self):
        self.rect.centerx -= ENTITY_SPEED[self.name]

    def shoot(self):
        self.shot_delay -= 1
        if self.shot_delay == 0:
            self.shot_delay = ENTITY_SHOT_DELAY[self.name]
            return EnemyShot(name=f'{self.name}Shot', position=(self.rect.centerx, self.rect.centery))


class Enemy3(Entity):
    def __init__(self, name: str, position: tuple, screen):
        super().__init__(name, position)
        self.screen = screen  # Armazena a referência para a tela
        self.speed_x = -ENTITY_SPEED[self.name]  # Move da direita para a esquerda
        self.speed_y = 3  # Velocidade vertical inicial
        self.direction = -1  # Inicialmente, o inimigo se move para cima
        self.shot_delay = ENTITY_SHOT_DELAY[self.name]  # Inicializa o shot_delay

    def move(self):
        """Atualiza a posição do Enemy3 com movimento especial."""
        # Movimento horizontal
        self.rect.x += self.speed_x

        # Movimento vertical com comportamento de subir e descer
        self.rect.y += self.speed_y * self.direction

        # Verificação de bordas e ajuste de direção
        if self.rect.top <= 0:  # Bateu na borda superior
            self.direction = 1  # Mudar direção para baixo e dobrar a velocidade
            self.speed_y *= 2
        elif self.rect.bottom >= self.screen.get_height():  # Bateu na borda inferior
            self.direction = -1  # Mudar direção para cima e restaurar a velocidade normal
            self.speed_y = 3

    def shoot(self):
        self.shot_delay -= 1
        if self.shot_delay == 0:
            self.shot_delay = ENTITY_SHOT_DELAY[self.name]
            return EnemyShot(name=f'{self.name}Shot', position=(self.rect.centerx, self.rect.centery))
