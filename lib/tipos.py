"""
Procolos para tipagem estática com ``mypy``.
"""
from typing import (
    TYPE_CHECKING, overload,
    Type, Union, Tuple
)
from numpy import ndarray, uint8, float64

if TYPE_CHECKING:
    # Python 3.8+
    from typing import Literal
else:
    from collections import defaultdict
    # Python 3.7-
    Literal = defaultdict(lambda: 'tipo')
    Imagem = 'Imagem' # pylint: disable=invalid-name


class Color(ndarray): # type: ignore # pylint: disable=function-redefined
    """
    Uma cor em BGRA
    """
    dtype: Type[uint8] = uint8
    ndim: Literal[1] = 1
    shape: Tuple[Literal[4]] = (4,)


class OpLin(ndarray): # type: ignore # pylint: disable=function-redefined
    """
    Matrizes de transformação linear em coordenadas homogêneas.
    """
    dtype: Type[float64] = float64
    ndim: Literal[2] = 2
    shape: Tuple[Literal[3], Literal[3]] = (3, 3)


class Indices(ndarray): # type: ignore # pylint: disable=function-redefined
    """
    Matriz de índices da imagem em coordenadas homogêneas.

    Composta por um vetor `(WX, WY, W)` da imagem original para
    cada posição `(i, j)` da nova imagem.
    """
    dtype: Type[float64] = float64
    ndim: Literal[3] = 3
    shape: Tuple[Literal[3], int, int]


class Imagem(ndarray): # type: ignore # pylint: disable=function-redefined
    """
    Matrizes que representam imagens em OpenCV e bibliotecas similares.
    """
    dtype: Type[uint8] = uint8
    ndim: Literal[3] = 3
    # BGRA
    shape: Tuple[int, int, Literal[4]]

    def copy(self) -> Imagem:
        ...

    @overload
    def __add__(self, other: Union[Imagem, int]) -> Imagem: ...
    @overload
    def __add__(self, other: Union[ndarray, float]) -> ndarray: ...
    def __add__(self, other: Union[ndarray, float]) -> ndarray:
        ...

    @overload
    def __sub__(self, other: Union[Imagem, int]) -> Imagem: ...
    @overload
    def __sub__(self, other: Union[ndarray, float]) -> ndarray: ...
    def __sub__(self, other: Union[ndarray, float]) -> ndarray:
        ...

    def __neg__(self) -> Imagem:
        ...

    def __pos__(self) -> Imagem:
        ...

    def __abs__(self) -> Imagem:
        ...

    def __invert__(self) -> Imagem:
        ...

    @overload
    def __mul__(self, other: Union[Imagem, int]) -> Imagem: ...
    @overload
    def __mul__(self, other: Union[ndarray, float]) -> ndarray: ...
    def __mul__(self, other: Union[ndarray, float]) -> ndarray:
        ...

    def __matmul__(self, other: ndarray) -> ndarray:
        ...

    @overload
    def __pow__(self, other: Union[Imagem, int]) -> Imagem: ...
    @overload
    def __pow__(self, other: Union[ndarray, float]) -> ndarray: ...
    def __pow__(self, other: Union[ndarray, float]) -> ndarray:
        ...

    @overload
    def __floordiv__(self, other: Union[Imagem, int]) -> Imagem: ...
    @overload
    def __floordiv__(self, other: ndarray) -> ndarray: ...
    def __floordiv__(self, other: Union[ndarray, int]) -> ndarray:
        ...

    def __truediv__(self, other: Union[ndarray, float]) -> ndarray:
        ...

    @overload
    def __mod__(self, other: Union[Imagem, int]) -> Imagem: ...
    @overload
    def __mod__(self, other: Union[ndarray, float]) -> ndarray: ...
    def __mod__(self, other: Union[ndarray, float]) -> ndarray:
        ...

    def __rshift__(self, other: Union[Imagem, int]) -> Imagem:
        ...

    def __lshift__(self, other: Union[Imagem, int]) -> Imagem:
        ...

    def __and__(self, other: Union[Imagem, int]) -> Imagem:
        ...

    def __xor__(self, other: Union[Imagem, int]) -> Imagem:
        ...

    def __or__(self, other: Union[Imagem, int]) -> Imagem:
        ...
