# Entregas por turno com Google Maps

Agrupe destinos por turno e gere links com até quatro entregas em cada trecho.

## Rodar

Python 3.10 ou mais recente. Cada execução lê um JSON local e imprime outro JSON no terminal.

```bash
python app.py exemplo.json
python -m unittest -v
```

## Uso

Os turnos recebem lotes respeitando a ordem de cadastro. A chegada de um lote vira a origem do seguinte dentro do mesmo turno. O roteiro usa a sequência fornecida e pode ser reordenado no arquivo antes da execução.

## Google Maps

Os links seguem a documentação de [Maps URLs](https://developers.google.com/maps/documentation/urls/get-started) e abrem o app ou site sem chave. Confira no Maps a rota oferecida, a cobertura de transporte e as condições do momento. Os valores numéricos no arquivo de exemplo são demonstrações.

## Estado do projeto

Versão inicial funcional por linha de comando, sem interface web. Usa apenas a biblioteca padrão do Python. Os testes executam os exemplos e verificam as regras do projeto.

## Exportação para planilha

Use `python app.py exemplo.json --csv > relatorio.csv` para exportar o itinerário das entregas por turno. O CSV usa ponto e vírgula, conserva a ordem do relatório e inclui o cabeçalho mesmo quando a seleção está vazia. O JSON continua sendo a saída padrão.

Também é possível encadear a ferramenta com outro comando usando `-` como entrada. Exemplo em um terminal Bash:

```bash
cat exemplo.json | python app.py -
```

Para manter os relatórios gerenciáveis, o arquivo de entrada aceita até 500 entregas por execução. Os turnos continuam agrupados ignorando maiúsculas/minúsculas e acentos, e cada trecho comporta até quatro entregas ligadas em sequência.

Arquivos e entrada padrão JSON são limitados a 1 MB (1.000.000 bytes). Este limite vale mesmo quando as entregas seriam divididas em vários links de rota.


## Novo recurso

Com `retornar_base: true`, adiciona um trecho separado de retorno à base após a última entrega de cada turno. Não conta o retorno como entrega nem altera a ordem cadastrada.
