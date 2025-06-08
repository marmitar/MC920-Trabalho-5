# Image Processing (MC920) - Interpolation

- [Requirements](papers/enunciado.pdf)
- [Report](papers/entrega.pdf)

A versatile CLI tool that applies affine and projective transformations to images. Beyond simple resizing, you can rotate in-plane (angle α), rotate around the Y-axis with perspective projection (beta), scale by factor or target dimensions, and translate. The script computes the output bounding box, adjusts transformations so the result starts at (0,0), and resamples using your chosen interpolation method.

**Transformations:**

- In-plane rotation (`--angulo α`)
- Y-axis rotation with projection (`--beta β`)
- Uniform scaling (`--escala s`) or explicit dimensions (`--dim H W`)
- Translation, implicit in correction step

**Interpolation methods:**

- nearest neighbor (`vizinho`)
- bilinear (`bilinear`)
- bicubic (`bicubica`)
- Lagrange polynomials (`lagrange`)

![Small cut of city128.png upscaled with Nearest Neighbor](resultados/escala/128_15_viz.png "Nearest Neighbor")

![Small cut of city128.png upscaled with Langrange Polynomials](resultados/escala/128_15_lag.png "Langrange Polynomials")

## Performance check

Operation on a 1544x2000 input image, resulting in a 4112x5160 output.

### Nearest Neighbor Interpolation

```fish
>>> time python3 transforma.py imagens/among.png -o saida.png -c r -a 22 -e 2 -b 20 -m vizinho

________________________________________________________
Executed in  847.79 millis    fish           external
   usr time    2.99 secs      0.00 millis    2.99 secs
   sys time    0.14 secs      1.06 millis    0.14 secs

```

### Bilinear Interpolation

```fish
>>> time python3 transforma.py imagens/among.png -o saida.png -c r -a 22 -e 2 -b 20 -m bilinear

________________________________________________________
Executed in    2.74 secs    fish           external
   usr time    4.70 secs    0.00 millis    4.70 secs
   sys time    0.35 secs    1.07 millis    0.35 secs

```

### Bicubic Interpolation

```fish
>>> time python3 transforma.py imagens/among.png -o saida.png -c r -a 22 -e 2 -b 20 -m bicubica

________________________________________________________
Executed in   21.64 secs    fish           external
   usr time   20.38 secs   10.88 millis   20.37 secs
   sys time    3.51 secs    1.80 millis    3.51 secs

```

### Interpolation by Lagrange Polynomials

```fish
>>> time python3 transforma.py imagens/among.png -o saida.png -c r -a 22 -e 2 -b 20 -m lagrange

________________________________________________________
Executed in   12.11 secs    fish           external
   usr time   12.54 secs    0.00 millis   12.54 secs
   sys time    1.85 secs    1.07 millis    1.85 secs

```
