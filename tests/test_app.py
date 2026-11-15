"""Testes automatizados do gerenciador de ordens."""
import tempfile
import unittest
from pathlib import Path

from app import carregar_ordens, criar_os, atualizar_status, resumo


class TesteOrdensServico(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name) / "ordens.json"

    def tearDown(self):
        self.temp.cleanup()

    def test_base_inexistente_retorna_lista_vazia(self):
        self.assertEqual(carregar_ordens(self.base), [])

    def test_cria_ordem_e_persiste(self):
        ordem = criar_os("Ana", "Celular", "Tela quebrada", self.base)
        self.assertEqual(ordem["id"], 1)
        self.assertEqual(carregar_ordens(self.base)[0]["cliente"], "Ana")

    def test_identificador_incremental(self):
        criar_os("Ana", "Celular", "Tela quebrada", self.base)
        segunda = criar_os("Bruno", "Notebook", "Sem imagem", self.base)
        self.assertEqual(segunda["id"], 2)

    def test_concluir_ordem(self):
        criar_os("Ana", "Celular", "Tela quebrada", self.base)
        ordem = atualizar_status(1, "Concluida", self.base)
        self.assertEqual(ordem["status"], "Concluida")

    def test_rejeita_status_desconhecido(self):
        criar_os("Ana", "Celular", "Tela quebrada", self.base)
        with self.assertRaises(ValueError):
            atualizar_status(1, "Excluida", self.base)

    def test_rejeita_campos_vazios(self):
        with self.assertRaises(ValueError):
            criar_os("", "Celular", "Tela quebrada", self.base)

    def test_resumo_por_status(self):
        criar_os("Ana", "Celular", "Tela quebrada", self.base)
        criar_os("Bruno", "Notebook", "Não liga", self.base)
        atualizar_status(1, "Concluida", self.base)
        contagem = resumo(carregar_ordens(self.base))
        self.assertEqual(contagem["Concluida"], 1)
        self.assertEqual(contagem["Aberta"], 1)

    def test_os_inexistente(self):
        with self.assertRaises(ValueError):
            atualizar_status(999, "Concluida", self.base)


if __name__ == "__main__":
    unittest.main()
