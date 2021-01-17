"""
Ferramenta de rotação e escalonamento de imagens.
"""
import logging
from sys import stdout
from time import time
from timeit import timeit
from argparse import Namespace
from typing import Tuple
from lib.tipos import Imagem, Indices
from lib.args import (
    Argumentos, MATH, verbosidade,
    imagem, racional, natural, cor, metodo
)
from lib.inout import imgshow, imgwrite, encode
from lib.interp import Metodo
from lib.idx import indices, aplica
from lib.linop import inversa, identidade, translacao
from lib.opimg import (
    limites, redimensionamento, arredondamento,
    rotacao, rotacao_proj, escalonamento
)


DESCRICAO = 'Ferramenta de rotação e escalonamento de imagens.'
EPILOGO = 'Expressões matemáticas reconhecidas: ' + ', '.join(sorted(MATH.keys()))
# parser de argumentos
parser = Argumentos(allow_abbrev=False, add_help=False, description=DESCRICAO, epilog=EPILOGO)
# modificações na imagem
transf = parser.add_argument_group('Transformações')
transf.add_argument('-a', '--angulo', metavar='ALFA', type=racional(),
                    help='rotação no plano da imagem, em graus')
transf.add_argument('-b', '--beta', type=racional(),
                    help='rotação em torno de Y, em graus, projetado de volta para o plano XY')
escala = transf.add_mutually_exclusive_group()
escala.add_argument('-e', '--escala', type=racional(min=0),
                    help='escala de redimensionamento')
escala.add_argument('-d', '--dim', metavar=('ALTURA', 'LARGURA'), type=natural(min=0), nargs=2,
                    help='dimensões da imagem resultante')
# opções adicionais
optadc = parser.add_argument_group('Opções adicionais')
optadc.add_argument('-m', '--metodo', type=metodo, choices=Metodo, default='bilinear',
                    help='método de interpolação do resultado (padrão: bilinear)')
optadc.add_argument('-c', '--cor', type=cor, default=cor('transparente'),
                    help='cor de fundo da imagem transformada (reconhece opções do Matplotlib)')
optadc.add_argument('-h', '--help', action='help',
                    help='mostra esse texto de ajuda')
optadc.add_argument('-v', '--verboso', action='count', default=0,
                    help='mostra detalhes da execução')
# entrada e saída
inpout = parser.add_argument_group('Entrada e saída')
inpout.add_argument('imagem', metavar='IMAGEM', type=imagem, default='-',
                    help='imagem de entrada')
inpout.add_argument('-o', '--output', dest='saida',
                    help='salva resultado em arquivo (padrão: exibe em nova janela)')

# # # # #
# MAIN  #

def transformacao(img: Imagem, args: Namespace) -> Indices:
    """
    Monta da matriz de transformação linear e aplica
    para conseguir os índices transformados.
    """
    T = identidade()
    lim = limites(img.shape[:2])

    # rotação no plano da imagem
    if args.angulo is not None:
        R, lim = rotacao(args.angulo, lim)
        T = R @ T
    # rotação em torno de y com projeção
    if args.beta is not None:
        R, lim = rotacao_proj(args.beta, lim)
        T = R @ T
    # escalonamento
    if args.escala is not None:
        E, lim = escalonamento(args.escala, lim)
        T = E @ T
    # redimensionamento para saída fixa
    if args.dim is not None:
        E, lim = redimensionamento(lim, args.dim)
        T = E @ T

    # dimensões inteiras
    A, dim = arredondamento(lim)
    # translação para o centro do pixel e depois de
    # volta pro canto superior esquerdo
    T = translacao(-1/2) @ A @ T @ translacao(1/2)

    # índices da imagem de saída transformados
    return aplica(inversa(T), indices(dim))


if __name__ == '__main__':
    args = parser.parse_intermixed_args()
    verbosidade(args.verboso)

    # argumentos da cli
    img, arquivo = args.imagem
    logging.info(f'imagem {arquivo} de dimensões {img.shape}')

    inicio = time()
    # operações na imagem
    ind = transformacao(img, args)
    # tempo de transformação
    logging.info(f'transformação em {time() - inicio} segundos')

    inicio = time()
    # interpolação para o resultado
    img = args.metodo(img, ind, args.cor)
    # tempo de interpolação
    logging.info(f'interpolação em {time() - inicio} segundos')

    # exibição do resultado
    if args.saida is None:
        imgshow(img, arquivo)
    # imprime o buffer PNG
    elif args.saida == '-':
        stdout.buffer.write(encode(img))
    # ou escrita em arquivo
    else:
        imgwrite(img, args.saida)
