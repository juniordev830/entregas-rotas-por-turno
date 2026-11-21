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

    def test_reject_non_object_input(self):
        with self.assertRaisesRegex(ValueError, "objeto JSON"):
            run([])

    def test_reject_oversized_or_malformed_deliveries(self):
        for deliveries in ("texto", [None], [1], [{}] * 501):
            with self.subTest(kind=str(deliveries)[:15]), self.assertRaisesRegex(ValueError, "500"):
                run({"base": "Natal", "entregas": deliveries})

    def test_same_turn_with_case_and_accents_is_grouped(self):
        result = run({"base": "Natal", "entregas": [
            {"turno": "Manhã", "local": "A"},
            {"turno": "manha", "local": "B"},
        ]})
        self.assertEqual(result["total_trechos"], 1)
        self.assertEqual(result["turnos"]["manha"][0]["entregas"], ["A", "B"])


if __name__=="__main__": unittest.main()
