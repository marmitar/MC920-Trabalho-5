"""
Interpolação para o resultado das operações lineares
em imagens.
"""
from enum import Enum, unique, auto
import numpy as np
from .tipos import Indices, Imagem, Color
from .idx import acesso, dim_resultado


@unique
class Metodo(Enum):
    """
    Método de interpolação.
    """
    VIZINHO = auto()
    BILINEAR = auto()
    BICUBICA = auto()
    LAGRANGE = auto()

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


def asimg(mat: np.ndarray, trunca: bool=True) -> Imagem:
    """
    Convesão de matriz numérica para imagem de 8
    bits, com cuidado de underflow e overflow.
    """
    # conversão por arredondamento
    if not trunca:
        mat = np.round(mat)

    # posições de under / overflow
    lo, hi = mat <= 0, mat >= 255
    # imagem resultante
    img = mat.astype(np.uint8)
    img[lo] = 0
    img[hi] = 255
    return img


def bilinear(img: Imagem, ind: Indices, fundo: Color) -> Imagem:
    """
    Interpolação bilinear.
    """
    dxdy, ind = np.modf(ind)
    # índices truncados
    ind = ind.astype(int)
    # "erro" do truncamento
    dx, dy, _ = dxdy[...,np.newaxis]

    # vizinhança do ponto
    # f(x, y)
    f00 = acesso(img, ind, fundo, dtype=float)
    # f(x+1, y)
    ind[0] += 1
    f10 = acesso(img, ind, fundo, dtype=float)
    # f(x+1, y+1)
    ind[1] += 1
    f11 = acesso(img, ind, fundo, dtype=float)
    # f(x, y+1)
    ind[0] -= 1
    f01 = acesso(img, ind, fundo, dtype=float)

    # interpolação
    out = (1 - dx) * (1 - dy) * f00 \
        + dx * (1 - dy) * f10 \
        + (1 - dx) * dy * f01 \
        + dx * dy * f11
    return asimg(out)
    # TODO: interpolado para a direita


def bicubica(img: Imagem, ind: Indices, fundo: Color) -> Imagem:
    """
    Interpolação bicúbica.
    """
    # operações internas
    def P(t: np.ndarray) -> np.ndarray:
        return np.where(t > 0, t, 0)

    def R(s: np.ndarray) -> np.ndarray:
        pm1, p0, p1, p2 = (P(s+d)**3 for d in range(-1,2+1))
        return (p2 - 4*p1 + 6*p0 - 4*pm1) / 6

    dxdy, xy = np.modf(ind)
    # índices truncados
    x, y, _ = xy.astype(int)
    # "erro" do truncamento
    dx, dy, _ = dxdy[...,np.newaxis]

    out = np.zeros(dim_resultado(ind), dtype=float)
    # vizinhança do ponto
    for m in range(-1, 2+1):
        for n in range(-1, 2+1):
            # acesso do vizinho
            ind = np.stack((x + m, y + n), axis=0)
            f = acesso(img, ind, fundo, dtype=float)

            out += f * R(m - dx) * R(dy - n)

    # imagem resultante
    return asimg(out)
    # TODO: artefato


def lagrange(img: Imagem, ind: Indices, fundo: Color) -> Imagem:
    """
    Interpolação por polinômios de Lagrange.
    """
    dxdy, xy = np.modf(ind)
    # índices truncados
    x, y, _ = xy.astype(int)
    # "erro" do truncamento
    dx, dy, _ = dxdy[...,np.newaxis]

    # operação interna
    def L(n: int) -> np.ndarray:
        ind = np.stack((x - 1, y + n - 2), axis=0)

        # f(x - 1, y + n - 2)
        a = -dx * (dx - 1) * (dx - 2) * acesso(img, ind, fundo, dtype=float)
        # f(x + 0, y + n - 2)
        ind[0] += 1
        b = (dx + 1) * (dx - 1) * (dx - 2) * acesso(img, ind, fundo, dtype=float)
        # f(x + 1, y + n - 2)
        ind[0] += 1
        c = -dx * (dx + 1) * (dx - 2) * acesso(img, ind, fundo, dtype=float)
        # f(x + 2, y + n - 2)
        ind[0] += 1
        d = dx * (dx + 1) * (dx - 1) * acesso(img, ind, fundo, dtype=float)

        return (a / 6) + (b / 2) + (c / 2) + (d / 6)

    # L(1)
    a = -dy * (dy - 1) * (dy - 2) * L(1)
    # L(2)
    b = (dy + 1) * (dy - 1) * (dy - 2) * L(2)
    # L(3)
    c = -dy * (dy + 1) * (dy - 2) * L(3)
    # L(4)
    d = dy * (dy + 1) * (dy - 1) * L(4)

    # imagem resultante
    out = (a / 6) + (b / 2) + (c / 2) + (d / 6)
    return asimg(out)
