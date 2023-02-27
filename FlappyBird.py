import pygame
import os
import random

# Definição de constantes
TELA_LARGURA = 500
TELA_ALTURA = 800

# Definir as imagens do jogo
# pygame.image.load >>> carregar a imagem
# os.path.join >>> juntar o caminho da pasta de imagens
# pygame.transform.scale2x >>> Ajustar a imagem
IMAGEM_CANO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
IMAGEM_CHAO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
IMAGEM_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))
IMAGENS_PASSARO = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png')))
]

# Fonte que herdará a pontuação do jogo
pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont('arial', 50)

class Passaro:
    IMGS = IMAGENS_PASSARO
    # Animações da Rotação
    ROTACAO_MAXIMA = 25
    VELOCIDADE_ROTACAO = 20
    TEMPO_ANIMACAO = 5

    def __int__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagem_imagem = 0
        self.imagem = IMGS[0]






    pass

class Cano:
    pass

class Chao: