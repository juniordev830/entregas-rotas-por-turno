import unittest
from app import run

class DeliveriesTests(unittest.TestCase):
    def test_split_into_connected_segments(self):
        data={"base":"Natal","entregas":[{"turno":"Manhã","local":str(i)} for i in range(1,6)]}
        result=run(data)
        self.assertEqual(result["total_trechos"],2)
        trechos=result["turnos"]["manha"]
        self.assertEqual(trechos[0]["entregas"],["1","2","3","4"])
        self.assertEqual(trechos[1]["origem"],"4")
        self.assertEqual(trechos[1]["entregas"],["5"])

    def test_empty_deliveries(self):
        self.assertEqual(run({"base":"Natal","entregas":[]})["total_trechos"],0)

if __name__=="__main__": unittest.main()
