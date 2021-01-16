"""
Operações de transformação linear em imagens.

Sempre retorna uma operação com a imagem resultante
iniciando em (0, 0) e a dimensão dessa imagem.
"""
from typing import Tuple, overload
import numpy as np
from .tipos import OpLin
from . import ops


Dim = Tuple[float, float]


def correcao(T: OpLin, shape: Dim) -> Tuple[OpLin, Dim]:
    """
    Corrige transformação para que a imagem inicie
    na origem do plano. Retorna dimensões do resultado.

    Parâmetros
    ----------
    T: ndarray
        Matriz das transformações a serem aplicadas.
    shape: (float, float)
        Dimensões da imagem de entrada.

    Retorno
    -------
    T: ndarray
        Transformação corrigida.
    shape: (float, float)
        Dimensões da saída.
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
    # novas dimensõe
    W, H = xmax - xmin, ymax - ymin
    # início no (0, 0)
    T = ops.translacao(-xmin, -ymin) @ T
    return T, (W, H)


def rotacao(angulo: float, shape: Dim) -> Tuple[OpLin, Dim]:
    """
    Rotação no plano XY.

    Parâmetros
    ----------
    angulo: float
        Ângulo em graus.
    shape: (float, float)
        Dimensões da imagem de entrada.

    Retorno
    -------
    T: ndarray
        Transformação corrigida.
    shape: (float, float)
        Dimensões da saída.
    """
    # a rotação propriamente
    R = ops.rotacao(angulo, graus=True)
    R, shape = correcao(R, shape)
    # translação para o centro do pixel
    T1, T2 = ops.translacao(-1/2), ops.translacao(1/2)
    return T1 @ R @ T2, shape


def rotacao_proj(beta: float, shape: Dim) -> Tuple[OpLin, Dim]:
    """
    Rotação em torno do eixo Y.

    Parâmetros
    ----------
    beta: float
        Ângulo em graus.
    shape: (float, float)
        Dimensões da imagem de entrada.

    Retorno
    -------
    T: ndarray
        Transformação corrigida.
    shape: (float, float)
        Dimensões da saída.
    """
    # imagem normalizada e centrada na origem
    N, _ = redimensionamento(shape, (1, 1))
    T = ops.translacao(-1/2)
    # só então rotaciona e projeta
    R = ops.rotacao_proj(beta, graus=True)

    # operação completa e corrigida
    Op = ops.inversa(T @ N) @ R @ T @ N
    return correcao(Op, shape)


def escalonamento(prop: float, shape: Dim) -> Tuple[OpLin, Dim]:
    """
    Mudança de escala.

    Parâmetros
    ----------
    prop: float
        Proporção da escala.
    shape: (float, float)
        Dimensões da imagem de entrada.

    Retorno
    -------
    T: ndarray
        Transformação corrigida.
    shape: (float, float)
        Dimensões da saída.
    """
    W, H = shape
    T = ops.escalonamento(prop)
    return T, (prop * W, prop * H)


def arredondamento(shape: Dim) -> Tuple[OpLin, Tuple[int, int]]:
    """
    Arredondamento das dimensões da imagem para inteiro.

    Parâmetros
    ----------
    shape: (float, float)
        Dimensões da imagem de entrada.

    Retorno
    -------
    T: ndarray
        Transformação corrigida.
    shape: (float, float)
        Dimensões da saída.
    """
    W, H = map(int, np.round(shape))
    T, _ = redimensionamento(shape, (W, H))
    return T, (W, H)

@overload
def redimensionamento(inicial: Dim, final: Tuple[int, int]) -> Tuple[OpLin, Tuple[int, int]]:...
@overload
def redimensionamento(inicial: Dim, final: Dim) -> Tuple[OpLin, Dim]:...
def redimensionamento(inicial: Dim, final: Dim) -> Tuple[OpLin, Dim]:
    """
    Matriz de mudança de escala para dimensões específicas.

    Parâmetros
    ----------
    inicial: (float, float)
        Dimensões da imagem de entrada.
    final: (float, float)
        Dimensões esperadas para a saída.

    Retorno
    -------
    T: ndarray
        Transformação corrigida.
    shape: (float, float)
        Dimensões da saída.
    """
    (Wi, Hi), (Wf, Hf) = inicial, final
    T = ops.escalonamento(Wf / Wi, Hf / Hi)
    return T, final
