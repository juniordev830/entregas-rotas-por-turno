# Engenharia reversa e estudo — Entregas por turno com Google Maps

## Objetivo e fluxo

Agrupamento de entregas por turno e divisão em trechos. Em app.py, run agrupa os destinos e rota monta links limitados pelo tamanho dos trechos. As regras de entrada também tratam endereços que excedem o limite.

**Tecnologias identificadas** · Python.

**Revisão de referência** · `29e92483c3ea`.

```mermaid
flowchart TD
    Input["Arquivo JSON"] --> CLI["app.py · main"]
    CLI --> Rules["app.py · run"]
    Rules --> Standard["Resultado da análise"]
    Standard --> CSV["relatorio_csv.py"]
```

## Mapa do código

| Caminho | Papel de leitura | Símbolos selecionados |
| --- | --- | --- |
| [app.py](../app.py) | Ponto de leitura para entrada ou composição | `texto`, `chave`, `EnderecoExcedeLimite`, `_url`, `rota`, `run`, `objeto_sem_campos_repetidos`, `rejeitar_constante_json`, `main` |
| [relatorio_csv.py](../relatorio_csv.py) | Implementação | `celula`, `linhas`, `escrever_csv` |

## Roteiro de estudo e desenvolvimento

1. Comece pelo fluxo descrito acima e localize seus pontos de entrada no mapa. Acompanhe uma entrada válida até a transformação ou a resposta.
2. Abra um teste relacionado ao fluxo e descreva qual regra ele protege. Compare o tratamento esperado para entradas válidas, inválidas e nos limites.
3. Ao adicionar uma regra, determine qual módulo controla o dado e cubra o caso nesse nível. Em seguida, confira o efeito no comando, na API ou na interface de entrada.

**Pergunta de entrevista**

Como dividir um turno em trechos garantindo que nenhum endereço seja perdido?

## Testes versionados

Arquivos para começar a leitura dos cenários de teste: [test_app.py](../test_app.py), [test_regressoes.py](../test_regressoes.py), [test_saida_csv.py](../test_saida_csv.py), [test_stdin.py](../test_stdin.py), [test_waypoints_safety.py](../test_waypoints_safety.py).

Os comandos e versões de runtime usados no CI ficam em [.github/workflows/tests.yml](../.github/workflows/tests.yml).

[Voltar ao README](../README.md).
