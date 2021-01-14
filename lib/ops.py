"""
Operações de transformação linear em imagens.
"""
from typing import Optional
import numpy as np
from .tipos import LinOp


def identidade() -> LinOp:
    """
    Matriz identidade.
    """
    return np.eye(3, dtype=float)


def escalonamento(Sx: float, Sy: Optional[float]=None) -> LinOp:
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


def translacao(Tx: float, Ty: Optional[float]=None) -> LinOp:
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


def rotacao(theta: float, graus: bool=True) -> LinOp:
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


def inversa(mat: LinOp) -> LinOp:
    """
    Matriz da transformação inversa.
    """
    return np.linalg.pinv(mat)
