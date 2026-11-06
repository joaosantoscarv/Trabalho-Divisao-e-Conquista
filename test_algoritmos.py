"""Rodar com: python -m unittest -v test_algoritmos.py"""
import json
import math
import random
import unittest
from pathlib import Path
from algoritmos import (
    subarranjo_bruto, subarranjo_divisao, subarranjo_linear,
    par_mais_proximo_bruto, par_mais_proximo_divisao,
)

DADOS = json.loads(Path(__file__).with_name('casos_teste.json').read_text(encoding='utf-8'))


class TesteSubarranjo(unittest.TestCase):
    def test_casos_documentados(self):
        for caso in DADOS['subarranjos']:
            with self.subTest(caso=caso['nome']):
                esperado = tuple(caso['esperado'])
                for funcao in (subarranjo_bruto, subarranjo_divisao, subarranjo_linear):
                    self.assertEqual(funcao(caso['entrada']), esperado)

    def test_aleatorios_com_paridade(self):
        rng = random.Random(2026)
        for n in range(1, 70):
            for _ in range(7):
                valores = [rng.randint(-20, 20) for _ in range(n)]
                esperado = subarranjo_bruto(valores)
                self.assertEqual(subarranjo_divisao(valores), esperado)
                self.assertEqual(subarranjo_linear(valores), esperado)

    def test_vetor_vazio(self):
        for funcao in (subarranjo_bruto, subarranjo_divisao, subarranjo_linear):
            with self.assertRaises(ValueError):
                funcao([])


class TestePontos(unittest.TestCase):
    def test_casos_documentados(self):
        for caso in DADOS['pontos']:
            with self.subTest(caso=caso['nome']):
                for funcao in (par_mais_proximo_bruto,
                               lambda p: par_mais_proximo_divisao(p, limiar=2),
                               lambda p: par_mais_proximo_divisao(p, limiar=32)):
                    d, i, j = funcao(caso['entrada'])
                    self.assertTrue(math.isclose(d, caso['distancia_esperada'], abs_tol=1e-10))
                    self.assertEqual([i, j], caso['par_esperado'])

    def test_aleatorios_com_paridade(self):
        rng = random.Random(2026)
        for n in (2, 3, 7, 16, 33, 65, 90):
            for _ in range(30):
                pontos = [(rng.uniform(-1000, 1000), rng.uniform(-1000, 1000))
                          for _ in range(n)]
                esperado = par_mais_proximo_bruto(pontos)
                for limiar in (2, 8, 32):
                    obtido = par_mais_proximo_divisao(pontos, limiar=limiar)
                    self.assertTrue(math.isclose(obtido[0], esperado[0], rel_tol=1e-12))
                    self.assertEqual(obtido[1:], esperado[1:])

    def test_colineares_e_repetidos(self):
        rng = random.Random(75)
        for _ in range(100):
            n = rng.randint(2, 50)
            pontos = [(rng.randint(-4, 4), rng.randint(-4, 4)) for _ in range(n)]
            bruto = par_mais_proximo_bruto(pontos)[0]
            divisao = par_mais_proximo_divisao(pontos, limiar=2)[0]
            self.assertAlmostEqual(bruto, divisao)

    def test_entrada_invalida(self):
        for funcao in (par_mais_proximo_bruto, par_mais_proximo_divisao):
            with self.assertRaises(ValueError):
                funcao([(0, 0)])
        with self.assertRaises(ValueError):
            par_mais_proximo_divisao([(0, 0), (1, 1)], limiar=1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
