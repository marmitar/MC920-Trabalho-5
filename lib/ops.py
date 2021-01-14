"""
Operações de transformação linear em imagens.
"""
from typing import Tuple, Optional
import numpy as np
from .tipos import OpLin


def identidade() -> OpLin:
    """
    Matriz identidade.
    """
    return np.eye(3, dtype=float)


def escalonamento(Sx: float, Sy: Optional[float]=None) -> OpLin:
    """
    Matriz de mudança de escala.
    """
    if Sy is None:
        # escala repetida
        Sy = Sx

    return np.asarray([
        [Sx,  0,  0],
        [ 0, Sy,  0],
        [ 0,  0,  1]
    ], dtype=float)


def redimensionamento(inicial: Tuple[float, float], final: Tuple[float, float]) -> OpLin:
    """
    Matriz de mudança de escala para dimensões específicas.
    """
    (Wi, Hi), (Wf, Hf) = inicial, final
    return escalonamento(Wf / Wi, Hf / Hi)


def translacao(Tx: float, Ty: Optional[float]=None) -> OpLin:
    """
    Matriz de translação.
    """
    if Ty is None:
        # escala repetida
        Ty = Tx

    return np.asarray([
        [ 1,  0, Tx],
        [ 0,  1, Ty],
        [ 0,  0,  1]
    ], dtype=float)


def rotacao(theta: float, graus: bool=True) -> OpLin:
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


def inversa(mat: OpLin) -> OpLin:
    """
    Matriz da transformação inversa.
    """
    return np.linalg.pinv(mat)
