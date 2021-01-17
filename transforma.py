"""
Ferramenta de rotação e escalonamento de imagens.
"""
from sys import stdout
from argparse import Namespace
from typing import Tuple
from lib.tipos import Imagem, OpLin
from lib.args import Argumentos, imagem, racional, natural, cor, metodo
from lib.inout import imgshow, imgwrite, encode
from lib.interp import Metodo
from lib.idx import indices, aplica
from lib.linop import inversa, identidade, translacao
from lib.opimg import (
    redimensionamento, arredondamento,
    rotacao, rotacao_proj, escalonamento
)


DESCRICAO = 'Ferramenta de rotação e escalonamento de imagens.'
# parser de argumentos
parser = Argumentos(allow_abbrev=False, description=DESCRICAO, add_help=False)
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
# entrada e saída
inpout = parser.add_argument_group('Entrada e saída')
inpout.add_argument('imagem', metavar='IMAGEM', type=imagem, default='-',
                    help='imagem de entrada')
inpout.add_argument('-o', '--output', dest='saida',
                    help='salva resultado em arquivo (padrão: exibe em nova janela)')

# # # # #
# MAIN  #

def transformacao(img: Imagem, args: Namespace) -> Tuple[OpLin, Tuple[int, int]]:
    """
    Montagem da matriz de transformação linear.
    Também retorna as dimensões da imagem de saída.
    """
    T = identidade()
    shape: Tuple[float, float] = img.shape[:2]

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

    # translação para o centro do pixel e depois de
    # volta pro canto superior esquerdo
    L1, L2 = translacao(-1/2), translacao(1/2)
    return L1 @ R @ T @ L2, dim


if __name__ == '__main__':
    args = parser.parse_intermixed_args()
    # argumentos da cli
    img, arquivo = args.imagem

    # operações na imagem
    T, dim = transformacao(img, args)

    # índices da imagem de saída
    ind = indices(dim)
    # transformados para os da entrada
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
