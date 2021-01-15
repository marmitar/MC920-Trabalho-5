"""
Interpolação para o resultado das operações lineares
em imagens.
"""
from enum import Enum, unique, auto
import numpy as np
from .tipos import Indices, Imagem, Color
from .dim import acesso, dim_resultado


@unique
class Metodo(Enum):
    """
    Método de interpolação.
    """
    VIZINHO = auto()
    BILINEAR = auto()
    BICUBICA = auto()

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


def bicubica(img: Imagem, ind: Indices, fundo: Color) -> Imagem:
    """
    Interpolação bicubica.
    """
    # operações internas
    def P(t):
        return np.where(t > 0, t, 0)

    def R(s):
        pn, p0, p1, p2 = (P(s+d)**3 for d in range(-1,2+1))
        return (p2 - 4*p1 + 6*p0 - 4*pn) / 6

    dxdy, xy = np.modf(ind)
    # índices truncados
    x, y, _ = xy.astype(int)
    # erro do truncamento
    dx, dy, _ = dxdy[...,np.newaxis]

    out = np.zeros(dim_resultado(ind, fundo), dtype=float)
    # vizinhança do ponto
    for m in range(-1, 2+1):
        for n in range(-1, 2+1):
            # acesso do vizinho
            ind = np.stack((x + m, y + n), axis=0)
            f = acesso(img, ind, fundo)
            # soma proporcionada
            out += f * R(m - dx) * R(dy - n)

    # imagem resultante
    return out.astype(np.uint8)
    # TODO: artefato
