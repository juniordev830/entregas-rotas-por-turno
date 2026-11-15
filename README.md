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
