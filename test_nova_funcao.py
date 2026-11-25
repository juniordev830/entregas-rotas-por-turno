import unittest
from urllib.parse import urlparse, parse_qs
from app import run
class RetornoBase(unittest.TestCase):
    def test_retorno(self):
        data={"base":"Natal","retornar_base":True,"entregas":[{"turno":"manhã","local":"Macaíba"}]}
        result=run(data)
        self.assertEqual(result["total_trechos"],2)
        last=next(iter(result["turnos"].values()))[-1]
        self.assertTrue(last["retorno_base"])
        self.assertEqual(last["entregas"],[])
        self.assertEqual(parse_qs(urlparse(last["google_maps"]).query)["destination"],["Natal"])
        data["retornar_base"]=False
        self.assertEqual(run(data)["total_trechos"],1)

    def test_exporta_retorno_sem_contar_entrega(self):
        import csv
        from io import StringIO
        from relatorio_csv import escrever_csv
        data={"base":"Natal","retornar_base":True,"entregas":[{"turno":"manhã","local":"Macaíba"}]}
        buffer=StringIO()
        escrever_csv(run(data),buffer)
        buffer.seek(0)
        rows=list(csv.DictReader(buffer,delimiter=";"))
        self.assertEqual(len(rows),2)
        self.assertEqual(rows[-1]["ordem_no_trecho"],"0")
        self.assertEqual(rows[-1]["local"],"Natal")
