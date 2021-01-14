# TODO: docs
"""
Análise de índices e dimensões da imagem.
"""
from typing import Optional, Tuple, Union
import numpy as np
from .ops import translacao, escalonamento
from .tipos import OpLin, Indices


# Dimensões da imagem
Dim = Tuple[int, int]


def indices(shape: Dim) -> Indices:
    """
    Lista de cordenadas homogêneas de todos os pixels
    em uma imagem de dimensões com o dado formato.

    Parâmetros
    ----------
    shape: (int, int)
        Dimensões da imagem.

    Retorno
    -------
    indices: ndarray
        Tensor `(largura, altura, 3)` com as coordenadas
        `(X, Y, W)` de cada ponto da imagem.
    """
    # valores de x e y
    x = np.arange(shape[0], dtype=int)
    y = np.arange(shape[1], dtype=int)
    x, y = np.meshgrid(x, y, copy=False)
    # dimensão de translação
    w = np.ones_like(x, dtype=int)

    return np.stack((x, y, w), axis=2)


def outerdim(T: OpLin, shape: Dim) -> Tuple[Dim, Dim]:
    """
    Retorna informações da caixa delimitadora da
    imagem de saída.

    Parâmetros
    ----------
    T: ndarray
        Matriz das transformações a serem aplicadas.
    shape: (int, int)
        Dimensões da imagem de entrada.

    Retorno
    -------
    min: (int, int)
        Limites inferiores da imagem transformada.
    max: (int, int)
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

    return (xmin, ymin), (xmax, ymax),


def resultado(entrada: Dim, T: OpLin, saida: Optional[Dim]=None) -> Tuple[OpLin, Dim]:
    """
    Retorna uma transformação de correção para que a saída
    tenha o mínimo na origem `(0, 0)` e, se especificadas,
    que a caixa delimitadora da saída tenha as dimensões
    esperadas. Retorna também as dimensões da

    Parâmetros
    ----------
    entrada: (int, int)
        Dimensões da imagem de entrada.
    T: ndarray
        Matriz das transformações a serem aplicadas.
    saida: (int, int), opcional
        Dimensões fixas para a imagem de saída.

    Retorno
    -------
    C: ndarray
        Transformação total com correção embutida.
    shape: (int, int)
        Dimensões da imagem de saída.
    """
    (xmax, ymax), (xmin, ymin) = outerdim(T, entrada)
    C = translacao(-xmin, -ymin)
    Wi, Hi = xmax - xmin, ymax - ymin

    if saida is not None:
        Wo, Ho = saida
        C = C @ escalonamento(Wo / Wi, Ho / Hi)
        shape = Wo, Ho
    else:
        shape = Wi, Hi

    return C @ T, shape
