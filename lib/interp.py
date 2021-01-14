"""
Interpolação para o resultado das operações lineares
em imagens.
"""
import numpy as np
from .tipos import Indices, Imagem
from .dim import acesso


def vizinho(img: Imagem, ind: Indices, fundo: int=0) -> Imagem:
    """
    Interpolação pelo vizinho mais próximo.

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
        Imagem resultado interpolada da entrada.
    """
    return acesso(img, np.round(ind), fundo=fundo)
