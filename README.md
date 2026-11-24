# RentSmart - R.M Imóveis

## Executar
Requer Python 3. No terminal, execute `python rentsmart.py`. O programa cria `projecao_12_meses.csv`.

## Executar testes
Rode `python -m unittest test_rentsmart.py -v`. A suíte verifica as três categorias, adicionais, descontos, validações, parcelamento e CSV.

## Arquivos
- `rentsmart.py`: aplicação Python.
- `test_rentsmart.py`: 11 testes automatizados.
- `parte_teorica.pdf`: análise, entradas/processamentos/saídas, classes e fluxograma visual.
- `fluxograma_rentsmart.png`: fluxograma separado.
- `roteiro_video_pitch.txt`: roteiro do vídeo.
- `resultado_testes.txt`: resultado dos testes.

## Premissas
O aluguel permanece constante porque o enunciado não prevê reajuste. A taxa contratual é mostrada separadamente e cobrada nos primeiros meses conforme o parcelamento. Para estúdio, o programa aceita 0 vagas ou 2 ou mais vagas; o enunciado não informa valor para apenas uma vaga.
