"""
Ferramenta de rotação e escalonamento de imagens.
"""
from sys import stdout
from argparse import Namespace, ArgumentTypeError
from typing import Tuple
from lib.tipos import Imagem, OpLin
from lib.args import Argumentos, imagem, racional, natural, cor
from lib.inout import imgshow, imgwrite, encode
from lib.idx import indices, aplica
from lib.interp import Metodo
from lib.ops import inversa, identidade
from lib.imgop import (
    redimensionamento, arredondamento,
    rotacao, rotacao_proj, escalonamento
)


def metodo(texto: str) -> Metodo:
    """
    Tratamento do método escolhido na entrada padrão.
    """
    try:
        return Metodo[texto.upper()]
    except KeyError as err:
        raise ArgumentTypeError(f'método inválido: {texto}') from err


DESCRICAO = 'Ferramenta de rotação e escalonamento de imagens.'
# parser de argumentos
parser = Argumentos(DESCRICAO)
# modificações na imagem
parser.add_argument('-a', '--angulo', type=racional(),
                    help='rotação no plano da imagem, em graus')
parser.add_argument('-b', '--beta', type=racional(),
                    help='rotação em torno de Y, em graus, projetado de volta para o plano XY')
escala = parser.add_mutually_exclusive_group()
escala.add_argument('-e', '--escala', type=racional(min=0),
                    help='escala de redimensionamento')
escala.add_argument('-d', '--dim', metavar=('ALTURA', 'LARGURA'), type=natural(min=0), nargs=2,
                    help='dimensões da imagem resultante')
# opções relacionadas ao processamento
parser.add_argument('-m', '--metodo', type=metodo, choices=Metodo, default='vizinho',
                    help='método de interpolação do resultado (padrão: vizinho)')
parser.add_argument('-c', '--cor', type=cor, default=(0, 0, 0, 255),
                    help='cor de fundo da imagem transformada (reconhece opções do Matplotlib)')
# entrada e saída
parser.add_argument('imagem', metavar='IMAGEM', type=imagem, default='-',
                    help='imagem de entrada')
parser.add_argument('-o', '--output', dest='saida',
                    help='salva resultado em arquivo (padrão: exibe em nova janela)')

# # # # #
# MAIN  #

def transformacao(img: Imagem, args: Namespace) -> Tuple[OpLin, Tuple[int, int]]:
    """
    Montagem da matriz de transformação da imagem.
    Também retorna as dimensões da imagem de saída.
    """
    T = identidade()
    shape = img.shape[:2]

    # rotação no plano da imagem
    if args.angulo is not None:
        R, shape = rotacao(args.angulo, shape)
        T = R @ T
    # rotação em torno de y com projeção
    if args.beta is not None:
        R, shape = rotacao_proj(args.beta, shape)
        T = R @ T
    # escalonamento
    if args.escala is not None:
        E, shape = escalonamento(args.escala, shape)
        T = E @ T

    # redimensionamento para saída fixa
    if args.dim is not None:
        R, dim = redimensionamento(shape, args.dim)
    # sem redimensionamento
    else:
        R, dim = arredondamento(shape)

    return R @ T, dim


if __name__ == '__main__':
    args = parser.parse_intermixed_args()
    # argumentos da cli
    img, arquivo = args.imagem

    # operações na imagem
    T, dim = transformacao(img, args)
    # posições representadas pelo centro do pixel
    # T = translacao(-1/2) @ T @ translacao(1/2)

    # índices da imagem de entrada pela da saída
    ind = indices(dim)
    ind = aplica(inversa(T), ind)

    # interpolação para o resultado
    img = args.metodo(img, ind, args.cor)

    # exibição do resultado
    if args.saida is None:
        imgshow(img, arquivo)
    # imprime o buffer PNG
    elif args.saida == '-':
        stdout.buffer.write(encode(img))
    # ou escrita em arquivo
    else:
        imgwrite(img, args.saida)
