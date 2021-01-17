"""
Tratamento de argumentos da linha de comando.
"""
import math
from sys import stdin
from warnings import warn
from argparse import ArgumentParser, ArgumentTypeError, Namespace
from typing import Tuple, Optional, Sequence, Callable
from matplotlib import colors
import numpy as np
from .tipos import Imagem, Color
from .interp import Metodo
from .inout import decode


class Argumentos(ArgumentParser):
    """
    Objeto para tratar opções da linha comando.
    """
    def parse_intermixed_args(self, args: Optional[Sequence[str]]=None, namespace: Optional[Namespace]=None) -> Namespace:
        """
        Parser de argumentos com ordem mistas.
        Só funciona em Python 3.7 ou superior.
        """
        try:
            return super().parse_intermixed_args(args)
        except AttributeError:
            warn('Python 3.6 não suporta argumentos opcionais após entrada')
            return super().parse_args(args)


def imagem(arquivo: str) -> Tuple[Imagem, str]:
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


def metodo(texto: str) -> Metodo:
    """
    Método de interpolação.
    """
    try:
        return Metodo[texto.upper()]
    except KeyError as err:
        raise ArgumentTypeError(f'método inválido: {texto}') from err


# funções válidas na
MATH = {
    nome: getattr(math, nome)
    for nome in dir(math)
        if not nome.startswith('_')
}

def math_eval(expr: str) -> float:
    """
    Reconhecimento de expressões matemáticas.
    """
    try:
        # de https://realpython.com/python-eval-function/
        code = compile(expr, "<input>", "eval", optimize=0)
        # proteção de acessos inválido
        for nome in code.co_names:
            if nome not in MATH:
                raise NameError(f'expressão inválida: {expr}')

        # evaluação
        ans = eval(code, {'__builtins__': {}}, MATH)

    # erros durante a validação da expressão
    except (SyntaxError, NameError, ValueError) as err:
        raise ArgumentTypeError(str(err)) from err

    # resultados não numéricos
    if not isinstance(ans, (int, float)):
        raise ArgumentTypeError(f'expressão não númerica: {expr}')

    return ans


# limite infinito
inf = math.inf

def racional(*, min: float=-inf, max: float=inf) -> Callable[[str], float]:
    """
    Tratamento de argumentos de ponto flutuante dentro de um limite.
    """
    def parse(texto: str) -> float:
        num = math_eval(texto)
        # checa por NaN e Inf
        if not math.isfinite(num):
            raise ArgumentTypeError('número inválido ou infinito')
        # e checa limites
        elif not min < num < max:
            raise ArgumentTypeError('número fora do limite válido')

        return num
    return parse


def natural(*, min: float=-inf, max: float=inf) -> Callable[[str], int]:
    """
    Tratamento de argumentos inteiros em um limite.
    """
    def parse(texto: str) -> int:
        num = math_eval(texto)
        # checa se é inteiro
        if not isinstance(num, int):
            raise ArgumentTypeError(f'inteiro inválido: {num}')
        # e checa limites
        elif not min <= num <= max:
            raise ArgumentTypeError('número fora do limite válido')

        return num
    return parse


def cor(texto: str) -> Color:
    """
    Opções de cor reconhecidas pelo Matplotlib.
    """
    # opções especiais
    if texto == 't' or texto == 'transparente':
        return np.zeros(4, dtype=np.uint8)

    try:
        # conversão RGBA
        rgba = colors.to_rgba(texto)
    except ValueError as err:
        raise ArgumentTypeError(str(err)) from err

    r, g, b, a = map(lambda c: int(255 * c), rgba)
    return np.asarray([b, g, r, a], dtype=np.uint8)
