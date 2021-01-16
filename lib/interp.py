"""
Interpolação para o resultado das operações lineares
em imagens.
"""
from enum import Enum, unique, auto
from typing import Tuple
import numpy as np
from .tipos import Indices, Imagem, Color
from .idx import acesso, zeros


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


def asimg(mat: np.ndarray, *, round: bool=False) -> Imagem:
    """
    Convesão de matriz numérica para imagem de 8
    bits, com cuidado de underflow e overflow.
    """
    # conversão por arredondamento
    if round:
        mat = np.round(mat)

    # imagem resultante
    img = mat.astype(np.uint8)
    # posições de under e overflow
    img[mat < 0] = 0
    img[mat > 255] = 255
    return img

def modf(ind: Indices, *, round: bool=False) -> Tuple[np.ndarray, np.ndarray]:
    """
    Retorna a parte inteira e a parte fracionária de
    cada coordenada. A coordenada W é descartada.
    """
    # descarta W
    ind = ind[:2]
    # arredonda ou trunca
    if round:
        x = np.round(ind)
    else:
        x = np.floor(ind)
    # parte fracionária
    dx = ind - x
    return x.astype(int), dx


def bilinear(img: Imagem, ind: Indices, fundo: Color) -> Imagem:
    """
    Interpolação bilinear.
    """
    # índices truncados
    ind, dxdy = modf(ind)
    # "erro" do truncamento
    dx, dy = dxdy[...,np.newaxis]

    # vizinhança do ponto
    f = zeros(ind, dtype=float)
    # f(x, y)
    f = acesso(img, ind, fundo, out=f)
    out = (1 - dx) * (1 - dy) * f
    # f(x+1, y)
    ind[0] += 1
    f = acesso(img, ind, fundo, out=f)
    out += dx * (1 - dy) * f
    # f(x+1, y+1)
    ind[1] += 1
    f = acesso(img, ind, fundo, out=f)
    out += (1 - dx) * dy * f
    # f(x, y+1)
    ind[0] -= 1
    f = acesso(img, ind, fundo, out=f)
    out += dx * dy * f

    # transformação para 8 bits
    return asimg(out)


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

    # índices truncados
    (x, y), dxdy = modf(ind)
    # "erro" do truncamento
    dx, dy = dxdy[...,np.newaxis]

    out = zeros(ind, dtype=float)
    # vizinhança do ponto
    f = zeros(ind, dtype=float)
    for m in range(-1, 2+1):
        for n in range(-1, 2+1):
            # acesso do vizinho
            ind = np.stack((x + m, y + n), axis=0)
            f = acesso(img, ind, fundo, out=f)

            out += f * R(m - dx) * R(dy - n)

    # imagem resultante
    return asimg(out)


def lagrange(img: Imagem, ind: Indices, fundo: Color) -> Imagem:
    """
    Interpolação por polinômios de Lagrange.
    """
    # índices truncados
    (x, y), dxdy = modf(ind)
    # "erro" do truncamento
    dx, dy = dxdy[...,np.newaxis]

    # operação interna
    f = zeros(ind, dtype=float)
    def L(n: int) -> np.ndarray:
        ind = np.stack((x - 1, y + n - 2), axis=0)

        # f(x - 1, y + n - 2)
        a = -dx * (dx - 1) * (dx - 2) * acesso(img, ind, fundo, out=f)
        # f(x + 0, y + n - 2)
        ind[0] += 1
        b = (dx + 1) * (dx - 1) * (dx - 2) * acesso(img, ind, fundo, out=f)
        # f(x + 1, y + n - 2)
        ind[0] += 1
        c = -dx * (dx + 1) * (dx - 2) * acesso(img, ind, fundo, out=f)
        # f(x + 2, y + n - 2)
        ind[0] += 1
        d = dx * (dx + 1) * (dx - 1) * acesso(img, ind, fundo, out=f)

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
