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
    pontos = [texto(parada) for parada in paradas]
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
    base = texto(data["base"])
    turnos = {}
    for item in data["entregas"]:
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
        rotas[turno] = trechos
    return {"turnos": rotas, "total_trechos": sum(len(v) for v in rotas.values())}


import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("entrada", type=Path, help="Arquivo JSON com os dados")
    args = parser.parse_args()

    try:
        with args.entrada.open(encoding="utf-8") as source:
            data = json.load(source)
        if not isinstance(data, dict):
            raise ValueError("A entrada deve ser um objeto JSON.")
        result = run(data)
    except (KeyError, TypeError, ValueError, OSError) as exc:
        parser.exit(2, f"Erro nos dados ou na execução: {exc}\n")

    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
