"""
Ferramenta de rotação e escalonamento de imagens.
"""
from sys import stdout
from lib.args import Argumentos, imagem, racional, natural
from lib.inout import imgshow, imgwrite, encode


DESCRICAO = 'Ferramenta de rotação e escalonamento de imagens.'
# parser de argumentos
parser = Argumentos(DESCRICAO)
# modificações na imagem
parser.add_argument('-a', '--angulo', type=racional,
                    help='rotação da imagem, em graus')
parser.add_argument('-e', '--escala', type=lambda s: racional(s, min=0),
                    help='escala de redimensionamento')
parser.add_argument('-d', '--dim', type=natural, nargs=2,
                    help='dimensões da imagem resultante')
# TODO: https://docs.python.org/3/library/argparse.html#mutual-exclusion
# TODO: opção de cor de fundo
# entrada e saída
parser.add_argument('imagem', metavar='IMAGEM', type=imagem, default='-',
                    help='imagem de entrada')
parser.add_argument('-o', '--output', dest='saida',
                    help='salva resultado em arquivo (padrão: exibe em nova janela)')


if __name__ == '__main__':
    args = parser.parse_intermixed_args()
    # argumentos da cli
    img, arquivo = args.imagem

    # TODO
    raise NotImplementedError(args)

    # exibição do resultado
    if args.saida is None:
        imgshow(img, arquivo)
    # imprime o buffer PNG
    elif args.saida == '-':
        stdout.buffer.write(encode(img))
    # ou escrita em arquivo
    else:
        imgwrite(img, args.saida)
