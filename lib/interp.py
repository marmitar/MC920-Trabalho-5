"""
Interpolação para o resultado das operações lineares
em imagens.
"""
import numpy as np
from .tipos import Indices, Imagem, Color
from .dim import acesso


def vizinho(img: Imagem, ind: Indices, fundo: Color) -> Imagem:
    """
    Interpolação pelo vizinho mais próximo.

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
        Imagem resultado interpolada da entrada.
    """
    return acesso(img, np.round(ind), fundo=fundo)
