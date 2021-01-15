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
    dxdy, ind = np.modf(ind)
    # índices truncados
    ind = ind.astype(int)
    # erro do truncamento
    dx, dy, _ = dxdy[...,np.newaxis]

    # vizinhança do ponto
    # f(x, y)
    f00 = acesso(img, ind, fundo)
    # f(x+1, y)
    ind[1] += 1
    f10 = acesso(img, ind, fundo)
    # f(x+1, y+1)
    ind[2] += 1
    f11 = acesso(img, ind, fundo)
    # f(x, y+1)
    ind[1] -= 1
    f01 = acesso(img, ind, fundo)

    # interpolação
    out = (1 - dx) * (1 - dy) * f00 \
        + dx * (1 - dy) * f10 \
        + (1 - dx) * dy * f01 \
        + dx * dy * f11
    return out.astype(np.uint8)
    # TODO: interpolado para a direita


def P(t: np.ndarray) -> np.ndarray:
    return np.where(t > 0, t, 0)

def R(s: np.ndarray) -> np.ndarray:
    return (P(s+2)**3 - 4*P(s+1)**2 + 6*P(s)**2 - 4*P(s-1)**3)/6


def bicubica(img: Imagem, ind: Indices, fundo: Color) -> Imagem:
    """
    Interpolação bicubica.
    """
    dxdy, xy = np.modf(ind)
    # índices truncados
    x, y, w = xy.astype(int)
    # erro do truncamento
    dx, dy, _ = dxdy[...,np.newaxis]

    out = np.zeros_like(img, dtype=float)
    # vizinhança do ponto
    for m in range(-1, 2+1):
        for n in range(-1, 2+1):
            # acesso do vizinho
            ind = np.stack((x + m, y + n, w), axis=0)
            f = acesso(img, ind, fundo)
            # soma proporcionada
            out += f * R(m - dx) * R(n - dy)

    # imagem resultante
    return out.astype(np.uint8)
