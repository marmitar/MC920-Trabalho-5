# TODO: docs
"""
Análise de índices e dimensões da imagem.
"""
from typing import Optional, Tuple
import numpy as np
from .ops import translacao, escalonamento
from .tipos import LinOp, Indices


def indices(largura: int, altura: int) -> Indices:
    """
    TODO: update doc, comment
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
    # valores de x e y
    x = np.arange(largura, dtype=int)
    y = np.arange(altura, dtype=int)
    # repetidos de formas diferentes
    x, y = np.meshgrid(x, y, copy=False)
    # dimensão de translação
    w = np.ones_like(x, dtype=int)

    return np.stack((x, y, w), axis=2)


def outerdim(T: LinOp, shape: Tuple[int, int]) -> Tuple[Tuple[int, int], Tuple[int, int]]:
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
    dim: (int, int)
        Dimensões do resultado.
    origem: (int, int)
        Limites inferiores da imagem transformada.
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
    # dimensões novas
    W, H = xmax - xmin, ymax - ymin
    return (W, H), (xmin, ymin)


def resultado(entrada: Tuple[int, int], T: LinOp, saida: Optional[Tuple[int, int]]=None) -> Tuple[LinOp, Tuple[int, int]]:
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
    (Wi, Hi), (xmin, ymin) = outerdim(T, entrada)
    C = translacao(-xmin, -ymin)

    if saida is not None:
        Wo, Ho = saida
        C = C @ escalonamento(Wo / Wi, Ho / Hi)
        shape = Wo, Ho
    else:
        shape = Wi, Hi

    return C @ T, shape
