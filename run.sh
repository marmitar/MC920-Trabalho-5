#!/bin/bash

mkdir -p resultados
# echo Exemplos...
# python3 transforma.py imagens/city.png -o resultados/exemplo.png -a asin\(0.25\) -b deg\(pi/4\) -e 1/3
# python3 transforma.py imagens/city.png -o resultados/exemplo2.png -a asin\(0.25\) -b deg\(pi/4\) -e 1/3 -c red -m bicubica

mkdir -p resultados/rotacoes
# rotações
# echo -n Rotações... ALFA...
# echo -n ' ' house.png...
# python3 transforma.py imagens/house.png -o resultados/rotacoes/house_alp_viz.png -a 15 -m vizinho
# python3 transforma.py imagens/house.png -o resultados/rotacoes/house_alp_bil.png -a 15 -m bilinear
# python3 transforma.py imagens/house.png -o resultados/rotacoes/house_alp_bic.png -a 15 -m bicubica
# python3 transforma.py imagens/house.png -o resultados/rotacoes/house_alp_lag.png -a 15 -m lagrange
# echo -n ' ' house16.png...
# python3 transforma.py imagens/house16.png -o resultados/rotacoes/16_alp_viz.png -a 15 -m vizinho
# python3 transforma.py imagens/house16.png -o resultados/rotacoes/16_alp_bil.png -a 15 -m bilinear
# python3 transforma.py imagens/house16.png -o resultados/rotacoes/16_alp_bic.png -a 15 -m bicubica
# python3 transforma.py imagens/house16.png -o resultados/rotacoes/16_alp_lag.png -a 15 -m lagrange
# echo -n ' ' beta...
# python3 transforma.py imagens/house64.png -o resultados/rotacoes/64_alp_viz.png -b -30 -m vizinho
# python3 transforma.py imagens/house64.png -o resultados/rotacoes/64_alp_bil.png -b -30 -m bilinear
# python3 transforma.py imagens/house64.png -o resultados/rotacoes/64_alp_bic.png -b -30 -m bicubica
# python3 transforma.py imagens/house64.png -o resultados/rotacoes/64_alp_lag.png -b -30 -m lagrange
# echo

mkdir -p resultados/escala
# escalonamento
echo -n Escalonamento...
echo -n ' ' 1/4...
python3 transforma.py imagens/city.png -o resultados/escala/city_14_viz.png -e 1/4 -m vizinho
python3 transforma.py imagens/city.png -o resultados/escala/city_14_bil.png -e 1/4 -m bilinear
python3 transforma.py imagens/city.png -o resultados/escala/city_14_bic.png -e 1/4 -m bicubica
python3 transforma.py imagens/city.png -o resultados/escala/city_14_lag.png -e 1/4 -m lagrange
echo -n ' ' 80x60...
python3 transforma.py imagens/city128.png -o resultados/escala/128_86_viz.png -d 80 60 -m vizinho
python3 transforma.py imagens/city128.png -o resultados/escala/128_86_bil.png -d 80 60 -m bilinear
python3 transforma.py imagens/city128.png -o resultados/escala/128_86_bic.png -d 80 60 -m bicubica
python3 transforma.py imagens/city128.png -o resultados/escala/128_86_lag.png -d 80 60 -m lagrange
echo -n ' ' 1.5...
python3 transforma.py imagens/city128.png -o resultados/escala/128_2_viz.png -e 1.5 -m vizinho
python3 transforma.py imagens/city128.png -o resultados/escala/128_2_bil.png -e 1.5 -m bilinear
python3 transforma.py imagens/city128.png -o resultados/escala/128_2_bic.png -e 1.5 -m bicubica
python3 transforma.py imagens/city128.png -o resultados/escala/128_2_lag.png -e 1.5 -m lagrange
echo

# profiling
# echo -n Profiling...
# echo -n ' ' vizinho...
# python3 -m cProfile -s cumtime transforma.py imagens/among.png -o saida.png -c r -a 22 -e 2 -b 20 -m vizinho > resultados/vizinho.txt
# echo -n ' ' bilinear...
# python3 -m cProfile -s cumtime transforma.py imagens/among.png -o saida.png -c r -a 22 -e 2 -b 20 -m bilinear > resultados/bilinear.txt
# echo -n ' ' bicubica...
# python3 -m cProfile -s cumtime transforma.py imagens/among.png -o saida.png -c r -a 22 -e 2 -b 20 -m bicubica > resultados/bicubica.txt
# echo -n ' ' lagrange...
# python3 -m cProfile -s cumtime transforma.py imagens/among.png -o saida.png -c r -a 22 -e 2 -b 20 -m lagrange > resultados/lagrange.txt
# echo
