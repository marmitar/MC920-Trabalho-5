"""
Análise de índices e dimensões da imagem.
"""
from typing import Tuple, Type, Union, overload
import numpy as np
from .tipos import OpLin, Indices, Imagem, Color


def indices(shape: Tuple[int, int]) -> Indices:
    """
    Lista de cordenadas homogêneas de todos os pixels
    em uma imagem de dimensões com o mesmo formato. A
    coordenada de cada pixel é considerada em seu centro.

    Parâmetros
    ----------
    shape: (int, int)
        Dimensões da imagem.

    Retorno
    -------
    indices: ndarray
        Tensor `(largura, altura, 3)` com as coordenadas
        `(WX, WY, W)` de cada ponto `(i, j)` da imagem.
    """
    # valores de x e y
    x = np.arange(shape[0], dtype=np.float64)
    y = np.arange(shape[1], dtype=np.float64)
    y, x = np.meshgrid(y, x, copy=False)
    # dimensão de translação
    w = np.ones_like(x, dtype=np.float64)

    return np.stack((x, y, w), axis=0)


def aplica(op: OpLin, ind: Indices) -> Indices:
    """
    Aplica operação linear na matriz de índices e
    normaliza para `W = 1`.

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
    res = np.tensordot(op, ind, axes=1)
    # normalização das coordenadas
    res[0] /= res[2]
    res[1] /= res[2]
    res[2] /= res[2]
    return res


def dim_resultado(ind: Indices) -> Tuple[int, ...]:
    """
    TODO: update
    Dimensões do resultado para uma cor de fundo.
    """
    return ind.shape[1:] + (4,)

@overload
def acesso(img: Imagem, ind: Indices, fundo: Color, dtype: Type[np.uint8]=np.uint8) -> Imagem: ...
@overload
def acesso(img: Imagem, ind: Indices, fundo: Color, dtype: type) -> np.ndarray: ...
def acesso(img: Imagem, ind: Indices, fundo: Color, dtype: type=np.uint8) -> np.ndarray:
    """
    Acesso na imagem pela matriz de índices.

    Parâmetros
    ----------
    img: ndarray
        Imagem de entrada.
    ind: ndarray
        Matriz das coordenadas homogêneas.
    fundo: int
        Cor para índices fora da imagem.

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
    out = np.zeros(dim_resultado(ind), dtype=dtype)
    # acessos válidos
    out[dentro] = img[ind[0, dentro], ind[1, dentro]]
    # e inválidos
    out[~dentro] = fundo

    return out
