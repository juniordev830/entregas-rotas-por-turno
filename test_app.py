import json
from pathlib import Path
import subprocess
import sys
import unittest

from app import run

ROOT = Path(__file__).resolve().parent


class ProjetoTest(unittest.TestCase):
    def test_exemplo_documentado(self):
        data = json.loads((ROOT / "exemplo.json").read_text(encoding="utf-8"))
        result = run(data)
        self.assertEqual(result['total_trechos'], 3)

    def test_cli_com_exemplo(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "app.py"), str(ROOT / "exemplo.json")],
            capture_output=True, text=True, encoding="utf-8", check=True,
        )
        self.assertEqual(json.loads(result.stdout)['total_trechos'], 3)

    def test_rejeita_dados_incompletos(self):
        with self.assertRaises((KeyError, ValueError, TypeError)):
            run({})

    def test_encadeia_lotes_e_normaliza_turno(self):
        result = run(dict(base="Base", entregas=[dict(turno="Manhã" if i % 2 else "manha", local=f"Local {i}") for i in range(9)]))
        trechos = result["turnos"]["manha"]
        self.assertEqual([len(t["entregas"]) for t in trechos], [4, 4, 1])
        self.assertEqual(trechos[1]["origem"], "Local 3")
        self.assertEqual(trechos[2]["origem"], "Local 7")

    def test_sem_entregas(self):
        self.assertEqual(run(dict(base="Base", entregas=[]))["total_trechos"], 0)
