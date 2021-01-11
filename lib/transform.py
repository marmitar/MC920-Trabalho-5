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
    ], dtype=float64)


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
    ], dtype=float64)


def rotacao(theta: float, graus: bool=True) -> Matriz:
    """
    Matriz de rotação.
    """
    # transformação para radianos
    if graus:
        theta = (theta * np.pi) / 180
    # seno e cosseno
    Ct, St = np.cos(theta), np.sin(theta)

    return np.asarray([
        [Ct,-St,  0]
        [St, Ct,  0],
        [ 0,  0,  1]
    ], dtype=float64)


def inversa(mat: Matriz) -> Matriz:
    """
    Matriz da transformação inversa.
    """
    return np.linalg.pinv(mat)
