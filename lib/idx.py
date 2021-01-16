"""
Análise de índices e dimensões da imagem.
"""
from typing import Tuple, Optional, overload
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
    y = np.arange(shape[0], dtype=float)
    x = np.arange(shape[1], dtype=float)
    x, y = np.meshgrid(x, y, copy=False)
    # dimensão de translação
    w = np.ones(shape, dtype=float)

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

@overload
def zeros(ind: Indices) -> np.ndarray: ...
@overload
def zeros(ind: Indices, *, dtype: type) -> np.ndarray: ...
def zeros(ind: Indices, *, dtype: type=np.uint8) -> np.ndarray:
    """
    Matriz de zeros com o formato da imagem resultante.
    """
    return np.zeros(ind.shape[1:] + (4,), dtype=dtype)

@overload
def acesso(img: Imagem, ind: Indices, fundo: Color) -> Imagem: ...
@overload
def acesso(img: Imagem, ind: Indices, fundo: Color, *, out: np.ndarray) -> np.ndarray: ...
def acesso(img: Imagem, ind: Indices, fundo: Color, *, out: Optional[np.ndarray]=None) -> np.ndarray:
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
    out: ndarray, opcional
        Matriz para salvar o resultado.

    Retorno
    -------
    out: ndarray
        Imagem com pixels recuperados da entrada nas
        coordenadas especificadas.
    """
    H, W, _ = img.shape
    # força inteiro, se necesserário
    x, y = ind[:2].astype(int, copy=False)
    # pontos que estão dentra da imagem de entrada
    dentro = (x >= 0) & (x < W) & (y >= 0) & (y < H)

    # imagem de saída
    if out is None:
        out = zeros(ind)
    # acessos válidos
    out[dentro] = img[y[dentro], x[dentro]]
    # e inválidos
    out[~dentro] = fundo

    return out
