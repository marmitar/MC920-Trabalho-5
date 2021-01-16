"""
Operações de transformação linear em imagens.
TODO: docs
"""
from typing import Tuple, overload
import numpy as np
from .tipos import OpLin
from . import ops


Dim = Tuple[float, float]


def correcao(T: OpLin, shape: Dim) -> Tuple[OpLin, Dim]:
    """
    Retorna informações da caixa delimitadora da
    imagem de saída.

    Parâmetros
    ----------
    T: ndarray
        Matriz das transformações a serem aplicadas.
    shape: (float, float)
        Dimensões da imagem de entrada.

    Retorno
    -------
    min: (float, float)
        Limites inferiores da imagem transformada.
    max: (float, float)
        Limites superiores.
    """
    W, H = shape
    dim = T @ np.asarray([
        [0, W, 0, W],
        [0, 0, H, H],
        [1, 1, 1, 1]
    ])
    # limites transformados
    xmax, ymax = np.max(dim[0]), np.max(dim[1])
    xmin, ymin = np.min(dim[0]), np.min(dim[1])

    W, H = xmax - xmin, ymax - ymin
    return ops.translacao(-xmin, -ymin) @ T, (W, H)


def rotacao(angulo: float, shape: Dim) -> Tuple[OpLin, Dim]:
    T1, T2 = ops.translacao(-1/2), ops.translacao(1/2)
    R = ops.rotacao(angulo, graus=True)

    return correcao(T1 @ R @ T2, shape)


def rotacao_proj(beta: float, shape: Dim) -> Tuple[OpLin, Dim]:
    N, _ = redimensionamento(shape, (1, 1))
    T = ops.translacao(-1/2)
    R = ops.rotacao_proj(beta, graus=True)

    Op = ops.inversa(T @ N) @ R @ T @ N
    return correcao(Op, shape)


def escalonamento(S: float, shape: Dim) -> Tuple[OpLin, Dim]:
    T = ops.escalonamento(S)
    W, H = shape
    return T, (S*W, S*H)


def arredondamento(shape: Dim) -> Tuple[OpLin, Tuple[int, int]]:
    W, H = map(int, shape)
    T, _ = redimensionamento(shape, (W, H))
    return T, (W, H)

@overload
def redimensionamento(inicial: Dim, final: Tuple[int, int]) -> Tuple[OpLin, Tuple[int, int]]:...
@overload
def redimensionamento(inicial: Dim, final: Dim) -> Tuple[OpLin, Dim]:...
def redimensionamento(inicial: Dim, final: Dim) -> Tuple[OpLin, Dim]:
    """
    Matriz de mudança de escala para dimensões específicas.
    """
    (Wi, Hi), (Wf, Hf) = inicial, final
    return ops.escalonamento(Wf / Wi, Hf / Hi), final
