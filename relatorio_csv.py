import csv


def celula(valor):
    """Mantém texto com aparência de fórmula como texto em planilhas."""
    if not isinstance(valor, str):
        return valor
    prefixos = ("=", "+", "-", "@", "＝", "＋", "－", "＠")
    if valor.lstrip().startswith(prefixos) or valor.startswith(("\t", "\r", "\n")):
        return "'" + valor
    return valor


def linhas(relatorio):
    for turno, trechos in relatorio["turnos"].items():
        for indice, trecho in enumerate(trechos, start=1):
            for ordem, local in enumerate(trecho["entregas"], start=1):
                yield turno, indice, ordem, trecho["origem"], local, trecho["google_maps"]


def escrever_csv(relatorio, destino):
    escritor = csv.writer(destino, delimiter=";", quoting=csv.QUOTE_ALL, lineterminator="\n")
    escritor.writerow(('turno', 'trecho', 'ordem_no_trecho', 'origem_do_trecho', 'local', 'google_maps'))
    for linha in linhas(relatorio):
        escritor.writerow([celula(valor) for valor in linha])
