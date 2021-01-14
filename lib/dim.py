"""
Análise de índices e dimensões da imagem.
"""
from typing import Tuple
import numpy as np
from .tipos import OpLin, Indices


def indices(shape: Tuple[int, int]) -> Indices:
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
        `(X, Y, W)` de cada ponto `(i, j)` da imagem.
    """
    # valores de x e y
    x = np.arange(shape[0], dtype=int)
    y = np.arange(shape[1], dtype=int)
    y, x = np.meshgrid(y, x, copy=False)
    # dimensão de translação
    w = np.ones_like(x, dtype=int)

    return np.stack((x, y, w), axis=2)


# Um ponto na imagem
Ponto = Tuple[float, float]

def limites(T: OpLin, shape: Tuple[int, int]) -> Tuple[Ponto, Ponto]:
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

    return (xmin, ymin), (xmax, ymax)
