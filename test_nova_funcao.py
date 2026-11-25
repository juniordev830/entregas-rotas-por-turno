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
