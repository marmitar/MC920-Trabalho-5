"""
Funções de IO com as imagens.
"""
import numpy as np
import cv2
from .tipos import Image


def encode(img: Image) -> bytes:
    """
    Codifica imagem em buffer PNG.

    Parâmetros
    ----------
    img: ndarray
        Matriz representando a imagem.

    Retorno
    -------
    buf: bytes
        Buffer com dados da imagem em PNG.

    Erro
    ----
    ValueError
        A entrada não representa uma imagem.
    """
    ok, buf = cv2.imencode('.png', img)
    # problemas de codificação
    if not ok:
        raise ValueError('não foi possível codificar em PNG')

    return buf.tobytes()


def decode(buffer: bytes) -> Image:
    """
    Decodifica imagem colorida de um buffer PNG.

    Parâmetros
    ----------
    buffer: bytes
        Dados do arquivo da imagem.

    Retorno
    -------
    img: ndarray
        Matriz representando a imagem lida.

    Erro
    ----
    ValueError
        Arquivo não pode ser decodificado como imagem.
    """
    buf = np.frombuffer(buffer, dtype=np.uint8)
    img = cv2.imdecode(buf, cv2.IMREAD_GRAYSCALE)
    # problemas de decodificação
    if img is None:
        raise ValueError('não foi possível parsear dado como imagem')

    return img


def imgwrite(img: Image, caminho: str) -> None:
    """
    Escreve.

    Parâmetros
    ----------
    buffer: bytes
        Dados do arquivo da imagem.

    Retorno
    -------
    img: ndarray
        Matriz representando a imagem lida.

    Erro
    ----
    ValueError
        Problema de escrita no caminho especificado ou
        codificação da imagem.
    """
    if not cv2.imwrite(caminho, img):
        raise ValueError('problema de escrita ou codificação')


def imgshow(img: Image, nome: str="", delay: int=250) -> None:
    """
    Apresenta a imagem em uma janela com um nome.

    Parâmetros
    ----------
    img: ndarray
        Matriz representando uma imagem.
    nome: str, opcional
        Nome da janela a ser aberta.
    delay: int, opcional
        Tempo em milisegundos de checagem da janela.
    """
    try:
        cv2.namedWindow(nome, cv2.WINDOW_AUTOSIZE)
        cv2.imshow(nome, img)

        # espera alguma chave ou a janela ser fechada
        while cv2.waitKey(delay) < 0:
            # problemas com versões diferentes de python e opencv
            prop1 = cv2.getWindowProperty(nome, cv2.WND_PROP_ASPECT_RATIO)
            prop2 = cv2.getWindowProperty(nome, cv2.WND_PROP_VISIBLE)
            if prop1 == prop2:
                break
        cv2.destroyAllWindows()
        cv2.waitKey(1)
    # Ctrl-C não são erros nesse caso
    except KeyboardInterrupt:
        pass
