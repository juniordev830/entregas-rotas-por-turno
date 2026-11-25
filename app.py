'Agrupe destinos por turno e gere links com até quatro entregas em cada trecho.'


from unicodedata import combining, normalize


def texto(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Use texto não vazio.")
    return value.strip()


def chave(value):
    return "".join(c for c in normalize("NFKD", texto(value).casefold()) if not combining(c))


from urllib.parse import urlencode


MODOS = {"carro": "driving", "a-pe": "walking", "bicicleta": "bicycling", "onibus": "transit"}


class EnderecoExcedeLimite(ValueError):
    pass


def _url(acao, parametros):
    url = "https://www.google.com/maps/" + acao + "?" + urlencode({"api": 1, **parametros})
    if len(url) > 2048:
        raise EnderecoExcedeLimite("O endereço gerado ultrapassa o limite do Google Maps.")
    return url


def rota(origem, destino, modo="carro", paradas=(), evitar_pedagios=False):
    if isinstance(paradas, (str, bytes)) or paradas is None:
        raise ValueError("As paradas devem ser uma sequência de endereços.")
    try:
        from itertools import islice
        pontos = [texto(parada) for parada in islice(paradas, 4)]
    except TypeError as exc:
        raise ValueError("As paradas devem ser uma sequência de endereços.") from exc
    if len(pontos) > 3 or any("|" in parada for parada in pontos):
        raise ValueError("Use até 3 paradas por link e evite o caractere |.")
    if modo not in MODOS:
        raise ValueError(f"Modo desconhecido: {modo}")
    params = {"origin": texto(origem), "destination": texto(destino), "travelmode": MODOS[modo]}
    if pontos:
        params["waypoints"] = "|".join(pontos)
    if evitar_pedagios:
        params["avoid"] = "tolls"
    return _url("dir/", params)


def run(data):
    if not isinstance(data, dict):
        raise ValueError("A entrada deve ser um objeto JSON.")
    entregas = data.get("entregas")
    if not isinstance(entregas, list) or len(entregas) > 500 or any(
        not isinstance(item, dict) for item in entregas
    ):
        raise ValueError("Informe até 500 entregas como objetos.")
    base = texto(data["base"])
    retornar = data.get("retornar_base", False)
    if type(retornar) is not bool:
        raise ValueError("retornar_base deve ser verdadeiro ou falso.")
    turnos = {}
    for item in entregas:
        turno = chave(item["turno"])
        turnos.setdefault(turno, []).append(texto(item["local"]))
    rotas = {}
    for turno, locais in turnos.items():
        origem = base
        trechos = []
        inicio = 0
        while inicio < len(locais):
            tamanho = min(4, len(locais) - inicio)
            while True:
                paradas = locais[inicio:inicio + tamanho]
                destino = paradas[-1]
                try:
                    link = rota(origem, destino, paradas=paradas[:-1])
                except EnderecoExcedeLimite:
                    if tamanho == 1:
                        raise
                    tamanho -= 1
                else:
                    break
            trechos.append({"origem": origem, "entregas": paradas, "google_maps": link})
            inicio += tamanho
            origem = destino
        if retornar and origem != base:
            trechos.append({"origem": origem, "entregas": [],
                            "google_maps": rota(origem, base), "retorno_base": True, "destino": base})
        rotas[turno] = trechos
    return {"turnos": rotas, "total_trechos": sum(len(v) for v in rotas.values())}


import argparse
from contextlib import nullcontext
import sys
from relatorio_csv import escrever_csv
import json
from pathlib import Path

MAX_JSON_BYTES = 1_000_000


def objeto_sem_campos_repetidos(pares):
    objeto = {}
    for chave, valor in pares:
        if chave in objeto:
            raise ValueError(f"Campo JSON repetido: {chave!r}.")
        objeto[chave] = valor
    return objeto


def rejeitar_constante_json(constante):
    raise ValueError(f"Constante numérica inválida em JSON: {constante}.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("entrada", help="Arquivo JSON com os dados ou - para a entrada padrão")
    parser.add_argument("--csv", action="store_true", help="Exportar o itinerário das entregas por turno em CSV")
    args = parser.parse_args()

    try:
        entrada = nullcontext(sys.stdin.buffer) if args.entrada == "-" else Path(args.entrada).open("rb")
        with entrada as source:
            raw = source.read(MAX_JSON_BYTES + 1)
        if len(raw) > MAX_JSON_BYTES:
            raise ValueError("JSON excede o limite de 1 MB.")
        data = json.loads(
            raw,
            object_pairs_hook=objeto_sem_campos_repetidos,
            parse_constant=rejeitar_constante_json,
        )
        if not isinstance(data, dict):
            raise ValueError("A entrada deve ser um objeto JSON.")
        result = run(data)
    except RecursionError:
        parser.exit(2, "O JSON tem níveis de aninhamento demais.\n")
    except (KeyError, TypeError, ValueError, UnicodeError, OSError) as exc:
        parser.exit(2, f"Erro nos dados ou na execução: {exc}\n")

    sys.stdout.reconfigure(encoding="utf-8", newline="\n")
    if args.csv:
        escrever_csv(result, sys.stdout)
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
