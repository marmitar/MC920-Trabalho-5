"""
Análise de índices e dimensões da imagem.
"""
from typing import Tuple
import numpy as np
from .tipos import OpLin, Indices, Imagem


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

    return np.stack((x, y, w), axis=0)


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


def aplica(op: OpLin, ind: Indices) -> Indices:
    """
    Aplica operação linear na matriz de índices.

    Parâmetros
    ----------
    op: ndarray
        Operação linear.
    ind: ndarray
        Matriz das coordenadas homogêneas.

    Retorno
    -------
    out: ndarray
        Matriz de coordenadas transformadas.
    """
    return np.tensordot(op, ind, axes=1)


def acesso(img: Imagem, ind: Indices, fundo: int=0) -> Imagem:
    """
    Acesso na imagem pela matriz de índices.

    Parâmetros
    ----------
    img: ndarray
        Imagem de entrada.
    ind: ndarray
        Matriz das coordenadas homogêneas.
    fundo: int, opcional
        Valor para índices fora da imagem. (padrão: 0)

    Retorno
    -------
    out: ndarray
        Imagem com pixels recuperados da entrada nas
        coordenadas especificadas.
    """
    # força inteiro, se necesserário
    ind = ind.astype(int, copy=False)
    # coordenadas de cada ponto
    x, y = ind[0], ind[1]
    # pontos que estão dentra da imagem de entrada
    dentro = (x >= 0) & (x < img.shape[0]) & (y >= 0) & (y < img.shape[1])

    # imagem de saída
    out = np.zeros(ind.shape[1:], dtype=np.uint8)
    # acessos válidos
    out[dentro] = img[ind[0, dentro], ind[1, dentro]]
    # e inválido
    out[~dentro] = fundo

    return out
