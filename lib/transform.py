"""
Operações de transformação linear em imagens.
"""
from typing import Optional
import numpy as np
from .inout import Image


Matriz = np.ndarray


def escalonamento(Sx: float, Sy: Optional[float]=None) -> Matriz:
    """
    Matriz de mudança de escala.
    """
    # mesma escala em X e Y
    if Sy is None:
        Sy = Sx

    return np.asarray([
        [Sx,  0,  0],
        [ 0, Sy,  0],
        [ 0,  0,  1]
    ], dtype=float)


def translacao(Tx: float, Ty: Optional[float]=None) -> Matriz:
    """
    Matriz de translação.
    """
    # mesmo valor em X e Y
    if Ty is None:
        Ty = Tx

    return np.asarray([
        [ 1,  0, Tx],
        [ 0,  1, Ty],
        [ 0,  0,  1]
    ], dtype=float)


def rotacao(theta: float, graus: bool=True) -> Matriz:
    """
    Matriz de rotação por um ângulo `theta`.
    """
    # transformação para radianos
    if graus:
        theta = (theta * np.pi) / 180
    # seno e cosseno
    Ct, St = np.cos(theta), np.sin(theta)

    return np.asarray([
        [Ct,-St,  0],
        [St, Ct,  0],
        [ 0,  0,  1]
    ], dtype=float)


def inversa(mat: Matriz) -> Matriz:
    """
    Matriz da transformação inversa.
    """
    return np.linalg.pinv(mat)


Pixels = np.ndarray

def indices(largura: int, altura: int) -> Pixels:
    """
    Lista de cordenadas homogêneas de todos os pixels
    em uma imagem de dimensões `largura` x `altura`.

    Parâmetros
    ----------
    largura, altura: int
        Dimensões da imagem.

    Retorno
    -------
    pixels: ndarray
        Matriz `3 X (largura . altura)` com uma coluna
        com as coordenadas homogêneas `(X, Y, W)` de
        cada ponto da imagem.
    """
    x = np.arange(largura, dtype=int)
    y = np.arange(altura, dtype=int)

    x = np.tile(x, altura)
    y = np.repeat(y, largura)
    w = np.ones(largura * altura, dtype=int)

    return np.concatenate(([x], [y], [w]))


def outerdim(T: Matriz, largura: int, altura: int) -> Tuple[int, int]:
    """
    Retorna informações da caixa delimitadora da
    imagem de saída.

    Parâmetros
    ----------
    T: ndarray
        Matriz das transformações a serem aplicadas.
    largura, altura: int
        Dimensões da imagem de entrada.

    Retorno
    -------
    W, H: int
        Dimensões do resultado.
    xmin, ymin: int
        Limites inferiores da imagem transformada.
    """
    W, H = largura, altura
    dim = T @ np.asarray([
        [0, W, 0, W],
        [0, 0, H, H],
        [1, 1, 1, 1]
    ])

    xmax, ymax = np.max(dim[0]), np.max(dim[1])
    xmin, ymin = np.min(dim[0]), np.min(dim[1])
    W, H = xmax - xmin, ymax - ymin
    return W, H, xmin, ymin
