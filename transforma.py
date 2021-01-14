"""
Ferramenta de rotação e escalonamento de imagens.
"""
from sys import stdout
from argparse import Namespace
from typing import Tuple
from lib.tipos import Imagem, OpLin
from lib.args import Argumentos, imagem, racional, natural
from lib.inout import imgshow, imgwrite, encode
from lib.dim import limites, indices, aplica
from lib.interp import vizinho
from lib.ops import (
    identidade, escalonamento, rotacao, translacao,
    redimensionamento, inversa
)


DESCRICAO = 'Ferramenta de rotação e escalonamento de imagens.'
# parser de argumentos
parser = Argumentos(DESCRICAO)
# modificações na imagem
parser.add_argument('-a', '--angulo', type=racional(),
                    help='rotação da imagem, em graus')
escala = parser.add_mutually_exclusive_group()
escala.add_argument('-e', '--escala', type=racional(min=0),
                    help='escala de redimensionamento')
escala.add_argument('-d', '--dim', metavar=('ALTURA', 'LARGURA'), type=natural(min=0), nargs=2,
                    help='dimensões da imagem resultante')
# TODO: opção de cor de fundo
# TODO: método de interpolação
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
    # rotacao
    if args.angulo is not None:
        T = rotacao(args.angulo, graus=True) @ T
    # escalonamento
    if args.escala is not None:
        T = escalonamento(args.escala) @ T

    # correção da origem
    (xmin, ymin), (xmax, ymax) = limites(T, img.shape)
    Wi, Hi = xmax - xmin, ymax - ymin
    T = translacao(-xmin, -ymin) @ T

    # redimensionamento para saída fixa
    if args.dim is not None:
        T = redimensionamento((Wi, Hi), args.dim) @ T
        return T, args.dim
    # sem redimensionamento
    else:
        return T, (int(Wi), int(Hi))


if __name__ == '__main__':
    args = parser.parse_intermixed_args()
    # argumentos da cli
    img, arquivo = args.imagem

    # operações na imagem
    T, dim = transformacao(img, args)

    # índices da imagem de entrada pela da saída
    ind = indices(dim)
    ind = aplica(inversa(T), ind)

    # interpolação para o resultado
    img = vizinho(img, ind)

    # exibição do resultado
    if args.saida is None:
        imgshow(img, arquivo)
    # imprime o buffer PNG
    elif args.saida == '-':
        stdout.buffer.write(encode(img))
    # ou escrita em arquivo
    else:
        imgwrite(img, args.saida)
