"""
Tratamento de argumentos da linha de comando.
"""
import math
import logging
from sys import stdin
from warnings import warn
from functools import wraps
from argparse import ArgumentParser, Action, ArgumentTypeError, Namespace, BooleanOptionalAction
from typing import Any, Tuple, Optional, Sequence, Callable, Dict, Iterator
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


def verbosidade(level: int) -> None:
    """
    Muda a verbosidade do logger.
    """
    if level < 0:
        log_level = logging.ERROR
    elif level == 0:
        log_level = logging.WARNING
    elif level == 1:
        log_level = logging.INFO
    else: # level > 1
        log_level = logging.DEBUG

    logging.getLogger().setLevel(log_level)


def imagem(arquivo: str) -> Tuple[Imagem, str]:
    """
    Leitura e decodificação da imagem.
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


# limite infinito
inf = math.inf

def racional(*, min: float=-inf, max: float=inf) -> Callable[[str], float]:
    """
    Tratamento de argumentos de ponto flutuante limitados.
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
    Tratamento de argumentos inteiros limitados.
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
    # opções especiais para fundo transparente
    if texto in ('t', 'transparente'):
        return np.zeros(4, dtype=np.uint8)

    try:
        # leitura RGBA entre 0 e 1 do matplotlib
        rgba = colors.to_rgba(texto)
    except ValueError as err:
        raise ArgumentTypeError(str(err)) from err

    r, g, b, a = map(lambda c: int(255 * c), rgba)
    # ordem BGR para OpenCV
    return np.asarray([b, g, r, a], dtype=np.uint8)


def funcoes() -> Iterator[Tuple[str, Callable[..., float]]]:
    """
    Funções matemáticas válidas.
    """
    # todas as funções públicas de math
    for nome in dir(math):
        if not nome.startswith('_'):
            yield nome, getattr(math, nome)

    # alguns builtins
    yield 'int', int
    yield 'abs', abs
    yield 'sum', sum
    yield 'round', round
    # facilidade para conversão de ângulos
    yield 'd', math.degrees
    yield 'deg', math.degrees

    def as_deg(nome: str) -> Callable[..., float]:
        """
        Converte entrada ou saída da função
        trigonométrica para graus.
        """
        # a função trigonométrica
        fun = getattr(math, nome)

        # funções inversas retornam ângulo
        if nome.startswith('a'):
            @wraps(fun)
            def wrapper(x: float) -> float:
                return math.degrees(fun(x))
        # funções diretas recebem o ângulo
        else:
            @wraps(fun)
            def wrapper(x: float) -> float:
                return fun(math.radians(x))

        return wrapper


    # funções trigonométricas que devem ser ajustadas p/ graus
    fns = ('cos', 'sin', 'tan', 'acos', 'asin', 'atan', 'atan2')
    for nome in fns:
        yield nome, as_deg(nome)

# funções matemáicas válidas para 'math_eval'
MATH = {nome: fun for nome, fun in funcoes()}

def math_eval(expr: str) -> float:
    """
    Reconhecimento de expressões matemáticas.
    """
    try:
        # de https://realpython.com/python-eval-function/
        code = compile(expr, "<input>", "eval", optimize=0)
        # proteção de acessos inválidos
        for nome in code.co_names:
            if nome not in MATH:
                raise NameError(f'expressão inválida: {expr}')

        # execução da expressão
        ans = eval(code, {'__builtins__': {}}, MATH)

    # erros durante a validação da expressão
    except (SyntaxError, NameError, ValueError, TypeError) as err:
        raise ArgumentTypeError(str(err)) from err

    # resultados não numéricos
    if not isinstance(ans, (int, float)):
        raise ArgumentTypeError(f'expressão não númerica: {expr}')

    return ans
