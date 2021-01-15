"""
Interpolação para o resultado das operações lineares
em imagens.
"""
from enum import Enum, unique, auto
import numpy as np
from .tipos import Indices, Imagem, Color
from .dim import acesso


@unique
class Metodo(Enum):
    """
    Método de interpolação.
    """
    VIZINHO = auto()
    BILINEAR = auto()

    def __call__(self, img: Imagem, ind: Indices, fundo: Color) -> Imagem:
        """
        Aplica a interpolação selecionada.

        Parâmetros
        ----------
        img: ndarray
            Imagem de entrada.
        ind: ndarray
            Matriz das coordenadas homogêneas.
        fundo: int
            Cor para índices fora da imagem.

        Retorno
        -------
        out: ndarray
            Imagem resultado interpolada da entrada.
        """
        fn = globals()[str(self)]
        return fn(img, ind, fundo)

    def __str__(self) -> str:
        """
        Formatação do método pelo nome.
        """
        return self.name.lower() # pylint: disable=no-member


def vizinho(img: Imagem, ind: Indices, fundo: Color) -> Imagem:
    """
    Interpolação pelo vizinho mais próximo.
    """
    return acesso(img, np.round(ind), fundo=fundo)


def bilinear(img: Imagem, ind: Indices, fundo: Color) -> Imagem:
    """
    Interpolação bilinear.
    """
    # índices truncados
    indt = np.trunc(ind).astype(int)
    # erro do truncamento
    ind -= indt
    _, dx, dy = ind

    # vizinhança do ponto
    # f(x, y)
    f00 = acesso(img, indt, fundo)
    # f(x+1, y)
    indt[1] += 1
    f10 = acesso(img, indt, fundo)
    # f(x+1, y+1)
    indt[2] += 1
    f11 = acesso(img, indt, fundo)
    # f(x, y+1)
    indt[1] -= 1
    f01 = acesso(img, indt, fundo)

    # interpolação
    return (1 - dx) * (1 - dy) * f00 \
        + dx * (1 - dy) * f10 \
        + (1 - dx) * dy * f01 \
        + dx * dy * f11
