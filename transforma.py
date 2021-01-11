"""
Ferramenta de rotação e escalonamento de imagens.
"""
from lib.args import Argumentos, imagem_entrada, imagem_saida, racional, natural
from lib.inout import imgshow


DESCRICAO = 'Ferramenta de rotação e escalonamento de imagens.'
# parser de argumentos
parser = Argumentos(DESCRICAO)
# modificações na imagem
parser.add_argument('-a', '--angulo', type=racional,
                    help='rotação da imagem, em graus')
parser.add_argument('-e', '--escala', type=racional, # TODO: https://docs.python.org/3/library/argparse.html#mutual-exclusion
                    help='escala de redimensionamento')
parser.add_argument('-d', '--dim', type=natural, nargs=2,
                    help='dimensões da imagem resultante')
# TODO: cor de fundo
# entrada e saída
parser.add_argument('imagem', metavar='IMAGEM', type=imagem_entrada, default='-',
                    help='imagem de entrada')
parser.add_argument('-o', '--output', dest='saida', type=imagem_saida, default=imgshow,
                    help='salva resultado em arquivo (padrão: exibe em nova janela)')


if __name__ == '__main__':
    args = parser.parse_intermixed_args()
    # argumentos da cli
    img, arquivo = args.imagem

    # TODO
    raise NotImplementedError(args)

    # exibição do resultado
    args.saida(img, arquivo)
