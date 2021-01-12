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

def indices(altura: int, largura: int) -> Pixels:
    """
    Lista de cordenadas homogêneas de todos os pixels
    em uma imagem de dimensões `largura` x `altura`.

    Parâmetros
    ----------
    altura, largura: int
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
    w = np.ones(altura * largura, dtype=int)

    return np.concatenate(([x], [y], [w]))
