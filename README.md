# Trabalho 5

[Enunciado](papers/enunciado.pdf).

## Execuções

Operações em uma imagem 1544x2000, resultando em outra de 4112x5160.

### Interpolação pelo Vizinho Mais Próximo

```bash
>>> time python3 transforma.py imagens/among.png -o saida.png -c r -a 22 -e 2 -b 20 -m vizinho

________________________________________________________
Executed in    1,99 secs   fish           external
   usr time    2,32 secs    0,00 micros    2,32 secs
   sys time    0,41 secs  593,00 micros    0,41 secs

```

### Interpolação Bilinear

```bash
>>> time python3 transforma.py imagens/among.png -o saida.png -c r -a 22 -e 2 -b 20 -m bilinear

________________________________________________________
Executed in    6,16 secs   fish           external
   usr time    5,79 secs  513,00 micros    5,79 secs
   sys time    1,12 secs  136,00 micros    1,12 secs

```

### Interpolação Bicúbiba

```bash
>>> time python3 transforma.py imagens/among.png -o saida.png -c r -a 22 -e 2 -b 20 -m bicubica

________________________________________________________
Executed in   70,94 secs   fish           external
   usr time   61,12 secs    0,00 micros   61,12 secs
   sys time   10,30 secs  517,00 micros   10,30 secs

```

### Interpolação por Polinômios de Lagrange

```bash
>>> time python3 transforma.py imagens/among.png -o saida.png -c r -a 22 -e 2 -b 20 -m lagrange

________________________________________________________
Executed in   27,04 secs   fish           external
   usr time   22,18 secs  509,00 micros   22,18 secs
   sys time    5,53 secs  120,00 micros    5,53 secs

```
