"""
Operações de transformação linear em imagens.

Sempre retorna uma operação com a imagem resultante
iniciando em (0, 0) e os limites dessa imagem.
"""
import logging
from typing import Tuple, Optional, overload
import numpy as np
from .tipos import OpLin, Limites
from .idx import aplica
from . import linop


# Dimensões da imagem
Dim = Tuple[float, float]


def limites(shape: Dim) -> Limites:
    """
    Limites da imagem de entrada.

    Parâmetros
    ----------
    shape: (float, float)
        Dimensões da imagem de entrada.

    Retorno
    -------
    lim: ndarray
        Pontos extremos da imagem.
    """
    H, W = shape
    return np.asarray([
        [0, W, 0, W],
        [0, 0, H, H],
        [1, 1, 1, 1]
    ], dtype=float)


def dimensoes(lim: Limites) -> Tuple[float, float]:
    """
    Dimensões da caixa delimitadora da imagem transformada.

    Parâmetros
    ----------
    lim: ndarray
        Limites da imagem.

    Retorno
    -------
    shape: (float, float)
        Dimensões da imagem.
    """
    xmax, ymax = np.max(lim[:2], axis=1)
    xmin, ymin = np.min(lim[:2], axis=1)

    return ymax - ymin, xmax - xmin


def correcao(T: OpLin, lim: Limites) -> Tuple[OpLin, Limites]:
    """
    Corrige transformação para que a imagem inicie
    na origem do plano. Retorna limites do resultado.

    Parâmetros
    ----------
    T: ndarray
        Matriz das transformações a serem aplicadas.
    lim: ndarray
        Limites da imagem de entrada.

    Retorno
    -------
    T: ndarray
        Transformação corrigida.
    lim: ndarray
        Limites da saída.
    """
    dim = aplica(T, lim)
    # início no (0, 0)
    xmin, ymin = np.min(dim[:2], axis=1)
    L = linop.translacao(-xmin, -ymin)
    # operação corrigida
    T = L @ T
    return T, aplica(T, lim)


def escalonamento(prop: float, lim: Limites) -> Tuple[OpLin, Limites]:
    """
    Mudança de escala.

    Parâmetros
    ----------
    prop: float
        Proporção da escala.
    lim: ndarray
        Limites da imagem de entrada.

    Retorno
    -------
    T: ndarray
        Escala com resultado em (0, 0).
    lim: ndarray
        Limites da saída.
    """
    logging.debug(f'escalonamento de {prop}')

    T = linop.escalonamento(prop)
    return T, aplica(T, lim)


def redimensionamento(lim: Limites, shape: Dim) -> Tuple[OpLin, Limites]:
    """
    Matriz de mudança de escala para dimensões específicas.

    Parâmetros
    ----------
    lim: ndarray
        Limites da imagem de entrada.
    shape: (float, float)
        Dimensões esperadas para a saída.

    Retorno
    -------
    T: ndarray
        Caixa delimitadora com as dimensões dadas.
    lim: ndarray
        Limites da saída.
    """
    (Hi, Wi), (Hf, Wf) = dimensoes(lim), shape
    logging.debug(f'redimensionamento de {Hi, Wi} para {Hf, Wf}')

    T = linop.escalonamento(Wf / Wi, Hf / Hi)
    return T, aplica(T, lim)


def rotacao(angulo: float, lim: Limites) -> Tuple[OpLin, Limites]:
    """
    Rotação no plano XY.

    Parâmetros
    ----------
    angulo: float
        Ângulo em graus.
    lim: ndarray
        Limites da imagem de entrada.

    Retorno
    -------
    T: ndarray
        Rotação com resultado em (0, 0).
    lim: ndarray
        Limites da saída.
    """
    logging.debug(f'rotação em XY de {angulo} graus')

    # a rotação é negativa, já que Y inverte em matrizes
    R = linop.rotacao(-angulo, graus=True)
    return correcao(R, lim)


def rotacao_proj(beta: float, lim: Limites) -> Tuple[OpLin, Limites]:
    """
    Rotação em torno do eixo Y.

    Parâmetros
    ----------
    beta: float
        Ângulo em graus.
    lim: ndarray
        Limites da imagem de entrada.

    Retorno
    -------
    T: ndarray
        Escala com resultado em (0, 0).
    lim: ndarray
        Limites da saída.
    """
    logging.debug(f'rotação com projeção de {beta} graus')

    # imagem normalizada e centrada na origem
    N, _ = redimensionamento(lim, (1, 1))
    T = linop.translacao(-1/2)
    # a rotação é negativa, já que Y inverte em matrizes
    R = linop.rotacao_proj(-beta, graus=True)

    # operação completa e desnormalizada
    Op = linop.inversa(N) @ R @ T @ N
    return correcao(Op, lim)


def arredondamento(lim: Limites) -> Tuple[OpLin, Tuple[int, int]]:
    """
    Redimensionamento da imagem para dimensões
    arredondadas para inteiros positivos.

    Parâmetros
    ----------
    lim: ndarray
        Limites da imagem de entrada.

    Retorno
    -------
    T: ndarray
        Escala com resultado em (0, 0).
    shape: (int, int)
        Dimensões da saída.
    """
    logging.debug('arredodamento')

    # mapeamento para dimensão válida
    def asdim(num: float) -> int:
        res = int(round(num))
        # limita o resultado para um
        if res < 1:
            return 1
        else:
            return res

    H, W = map(asdim, dimensoes(lim))
    T, _ = redimensionamento(lim, (H, W))
    return T, (H, W)
