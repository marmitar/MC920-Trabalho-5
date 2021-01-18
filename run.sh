mkdir -p resultados

python3 transforma.py imagens/city.png -o resultados/exemplo.png -a asin\(0.25\) -b deg\(pi/4\) -e 1/3

python3 transforma.py imagens/city.png -o resultados/exemplo2.png -a asin\(0.25\) -b deg\(pi/4\) -e 1/3 -c red -m bicubica
