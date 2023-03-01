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
        self.imagem = self.IMGS[0]

    def pular(self):
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y

    def mover(self):
        # calcular o deslocament
        self.tempo += 1
        deslocamento = 1.5 + (self.tempo ** 2) + self.velocidade + self.tempo

        # restringir o deslogamento
        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2

        self.y += deslocamento

        # o ângulo do pássaro
        if deslocamento < 0 or self.y < (self.altura + 50):
            if self.angulo < self.ROTACAO_MAXIMA:
                self.angulo = self.ROTACAO_MAXIMA

        else:
            if self.angulo > -90:
                self.angulo -= self.VELOCIDADE_ROTACAO

    def desenhar(self, tela):
        # definir qual imagem do passaro vai usar
        self.contagem_imagem += 1

        if self.contagem_imagem < self.TEMPO_ANIMACAO:
            self.imagem = self.IMGS[0]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO * 2:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO * 3:
            self.imagem = self.IMGS[2]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO * 4:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem >= self.TEMPO_ANIMACAO * 4 + 1:
            self.imagem = self.IMGS[0]
            self.contagem_imagem = 0

        # se o passaro tiver caindo eu não vou bater asa
        if self.angulo <= -80:
            self.imagem = self.IMGS[1]
            self.contagem_imagem = self.TEMPO_ANIMACAO * 2

        # desenhar imagem
        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        posicao_centro_imagem = self.imagem.get_rect(topleft=(self.x, self.y)).center
        retangulo = imagem_rotacionada.get_rect(center=posicao_centro_imagem)
        tela.blit(imagem_rotacionada, retangulo.topleft)

    def get_mask(self):
        pygame.mask.from_surface(self.imagem)


class Cano:
    DISTANCIA = 200
    VELOCIDADE = 5

    def __int__(self, x):
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0
        self.CANO_TOPO = pygame.transform.flip(IMAGEM_CANO, False, True)
        self.CANO_BASE = IMAGEM_CANO
        self.passou = False
        self.definir_altura()

    def definir_altura(self):
        self.altura = random.randrange(50, 450)
        self.pos_base = self.altura - self.CANO_TOPO.get_height()
        self.pos_base = self.altura + self.DISTANCIA

    def mover(self):
        self.x -= self.VELOCIDADE

    def desenhar(self, tela):
        tela.blit(self.CANO_TOPO, (self.x, self.pos_topo))
        tela.blit(self.CANO_BASE, (self.x, self.pos_base))

    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.CANO_TOPO)
        base_mask = pygame.mask.from_surface(self.CANO_BASE)

        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))

        # Verificar o ponto de colisão com a mask
        # Overlap >>> dois pixels iguais do passaro com o cano

        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)

        # Se um dos forem TRUE, então significa que o pássaro colidiu com o cano
        if base_ponto or topo_ponto:
            return True
        else:
            return False


class Chao:
    # Definir os parâmetros fixos do chão, constantes >>>

    VELOCIDADE = 5

    # .get_width >>> pegar a largura da imagem do chão
    LARGURA = IMAGEM_CHAO.get_width()
    IMAGEM = IMAGEM_CHAO

    def __init__(self, y):
        # A imagem do Backgroud inicia no ponto esquerdo inferior
        # A translação é feita da direita para à esquerda
        self.y = y
        # Posição inicial 0 (Canto esquerdo da tela)
        self.x1 = 0
        # Segunda imagem será a primeira imagem + sua largura
        self.x2 = self.LARGURA

    def mover(self):
        self.x1 -= self.VELOCIDADE
        self.x2 -= self.VELOCIDADE

        if self.x1 + self.LARGURA < 0:
            self.x1 = self.LARGURA
        if self.x2 + self.LARGURA < 0:
            self.x2 = self.x2 + self.LARGURA

    def desenhar(self, tela):
        tela.blit(self.IMAGEM, (self.x1, self.y))
        tela.blit(self.IMAGEM, (self.x2, self.y))


def desenhar_tela(tela, passaros, canos, chao, pontos):

    # Desenhar a tela e o ponto de inserção
    tela.blit(IMAGEM_BACKGROUND, (0,0))

    # Desenhar o pássaro
    for passaro in passaros:
        passaro.desenhar(tela)

    for cano in canos:
        cano.desenhar(tela)

    # render( texto a ser renderizado,
    # Anti-aliasing: valor booleano opcional que determina se o texto deve ser suavizado,
    # Cor do texto, uma tupla (r, g, b),
    # Cor do fundo (r, g, b)
    # Estilo de fonte
    # Angulo de rotação (em graus)
    texto = FONTE_PONTOS.render('Pontuação: {}'.format(pontos), 1, (255, 255, 255))
    tela.blit(texto, (TELA_LARGURA - 10 - texto.get_width(), 10))
    chao.desenhar(tela)
    pygame.display.update()

def main():
    passaros = [Passaro(230,350)]
    chao = Chao(730)
    canos = [Cano(700)]
    tela = pygame.display.set_mode(TELA_LARGURA, TELA_ALTURA)
    pontos = 0
    relogio = pygame.time.Clock()

    rodando = True

    while rodando:
        # Quantos parâmetros por segundo, controlar o tempo
        relogio.tick(30)

        # Formula para interagir com o jogo
        # Pygame possui vários eventos, caso seja identificado que a pessoa clicou em "SAIR"
        # alteramos a variável "RODANDO" para que o WHILE pare / sair da tela pygame

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False # Para o while
                pygame.quit() # Sai da tela do pygame
                quit() # fecha o python

            if evento.type == pygame.KEYDOWN: # Identifica ao clicar em um botão
                if evento.key == pygame.K_SPACE: # Se for SPACE
                    for passaro in passaros: # Verifica na lista de passaros
                        passaro.pular() # Seleciona o passado de pular = SPACE






        desenhar_tela(tela, passaros, canos, chao, pontos)
