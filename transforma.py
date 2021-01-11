"""
Ferramenta de rotação e escalonamento de imagens.
"""
from lib.args import Argumentos, imagem_entrada, imagem_saida, racional
from lib.inout import imgshow


DESCRICAO = 'Ferramenta de rotação e escalonamento de imagens.'
# parser de argumentos
parser = Argumentos(DESCRICAO)
# modificações na imagem
parser.add_argument('-a', '--angulo', type=racional,
                    help='rotação da imagem, em graus')
parser.add_argument('-e', '--escala', type=racional, # TODO: e XOU d
                    help='escala de redimensionamento')
parser.add_argument('-d', '--dim', type=racional, # TODO: 2 valores
                    help='dimensões da imagem resultante')
# entrada e saída
parser.add_argument('iamgem', metavar='IMAGEM', type=imagem_entrada, default='-',
                    help='imagem de entrada')
parser.add_argument('-o', '--output', dest='saida', type=imagem_saida, default=imgshow,
                    help='salva resultado em arquivo (padrão: exibe em nova janela)')


if __name__ == '__main__':
    args = parser.parse_intermixed_args()
    # argumentos da cli
    img, arquivo = args.imagem

    # TODO
    raise NotImplementedError()

    # exibição do resultado
    args.saida(img, arquivo)
