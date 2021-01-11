"""
Tratamento de argumentos da linha de comando.
"""
from sys import stdin
from math import isfinite
from warnings import warn
from argparse import ArgumentParser, ArgumentTypeError, Namespace
from typing import Tuple, Callable, Optional, Sequence
from .tipos import Image
from .inout import decode


class Argumentos(ArgumentParser):
    """
    Objeto para tratar opções da linha comando.

    Parâmetros
    ----------
    descricao: str
        Descrição da ferramenta.
    """
    def __init__(self, descricao: str):
        super().__init__(allow_abbrev=False, description=descricao)

    def parse_intermixed_args(self, args: Optional[Sequence[str]]=None) -> Namespace:
        """
        Parser de argumentos com ordem mistas.
        Só funciona em Python 3.7 ou superior.
        """
        try:
            return super().parse_intermixed_args(args)
        except AttributeError:
            warn('Python 3.6 não suporta argumentos opcionais após entrada')
            return super().parse_args(args)


def imagem(arquivo: str) -> Tuple[Image, str]:
    """
    Leitura e decodificação de imagem.
    """
    try:
        # argumento especial
        if arquivo == '-':
            return decode(stdin.buffer.read()), '[STDIN]'
        # arquivos comuns
        with open(arquivo, 'rb') as file:
            return decode(file.read()), arquivo

    except (OSError, ValueError) as err:
        raise ArgumentTypeError(str(err)) from err


# marcador de infito
inf = float('inf')

def racional(texto: str, *, min: float=-inf, max: float=inf) -> float:
    """
    Tratamento de argumentos de ponto flutuante dentro de um limite.
    """
    try:
        num = float(texto)
        # checa por NaN e Inf
        if not isfinite(num):
            raise ArgumentTypeError('número inválido ou infinito')
        elif not min < num < max:
            raise ArgumentTypeError('número fora do limite válido')
        return num

    except ValueError as err:
        raise ArgumentTypeError(str(err)) from err


def natural(texto: str) -> int:
    """
    Tratamento de argumentos de inteiro positivo.
    """
    try:
        num = int(texto, base=10)
        # checa negativo e zero
        if num <= 0:
            raise ArgumentTypeError('inteiro inválido')
        return num

    except ValueError as err:
        raise ArgumentTypeError(str(err)) from err

