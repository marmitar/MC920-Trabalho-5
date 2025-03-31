# Trabalho 5

[Enunciado](papers/enunciado.pdf) e [entrega](papers/entrega.pdf).

## Execuções

Operações em uma imagem 1544x2000, resultando em outra de 4112x5160.

### Interpolação pelo Vizinho Mais Próximo

```bash
>>> time python3 transforma.py imagens/among.png -o saida.png -c r -a 22 -e 2 -b 20 -m vizinho

________________________________________________________
Executed in  847.79 millis    fish           external
   usr time    2.99 secs      0.00 millis    2.99 secs
   sys time    0.14 secs      1.06 millis    0.14 secs

```

### Interpolação Bilinear

```bash
>>> time python3 transforma.py imagens/among.png -o saida.png -c r -a 22 -e 2 -b 20 -m bilinear

________________________________________________________
Executed in    2.74 secs    fish           external
   usr time    4.70 secs    0.00 millis    4.70 secs
   sys time    0.35 secs    1.07 millis    0.35 secs

```

### Interpolação Bicúbiba

```bash
>>> time python3 transforma.py imagens/among.png -o saida.png -c r -a 22 -e 2 -b 20 -m bicubica

________________________________________________________
Executed in   21.64 secs    fish           external
   usr time   20.38 secs   10.88 millis   20.37 secs
   sys time    3.51 secs    1.80 millis    3.51 secs

```

### Interpolação por Polinômios de Lagrange

```bash
>>> time python3 transforma.py imagens/among.png -o saida.png -c r -a 22 -e 2 -b 20 -m lagrange

________________________________________________________
Executed in   12.11 secs    fish           external
   usr time   12.54 secs    0.00 millis   12.54 secs
   sys time    1.85 secs    1.07 millis    1.85 secs

```
