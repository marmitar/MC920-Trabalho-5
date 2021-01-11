"""
Operações de transformação linear em imagens.
"""
from typing import Optional
import numpy as np
from .inout import Image


def escalonamento(Sx: float, Sy: Optional[float]=None) -> np.ndarray: # TODO: saída
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


def translacao(Tx: float, Ty: Optional[float]=None) -> np.ndarray: # TODO: saída
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


def rotacao(theta: float, graus: bool=True) -> np.ndarray: # TODO: saída
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
