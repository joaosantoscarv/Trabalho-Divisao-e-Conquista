"""Estudo complementar do limiar de força bruta na Etapa 2.

Execute somente depois de benchmark.py, para evitar experimentos concorrentes.
"""
import csv
import random
import statistics
from pathlib import Path
from time import perf_counter_ns
from algoritmos import par_mais_proximo_divisao

RAIZ = Path(__file__).parent


def main():
    registro = []
    for n in (100, 800, 3200, 6400):
        r = random.Random(10000 + n)
        pontos = [(r.uniform(-5000, 5000), r.uniform(-5000, 5000)) for _ in range(n)]
        for limiar in (2, 8, 16, 32, 64):
            par_mais_proximo_divisao(pontos, limiar=limiar)  # aquecimento
            tempos = []
            for rodada in range(1, 6):
                inicio = perf_counter_ns()
                par_mais_proximo_divisao(pontos, limiar=limiar)
                ms = (perf_counter_ns() - inicio) / 1e6
                tempos.append(ms)
                registro.append({'n': n, 'limiar': limiar, 'execucao': rodada,
                                 'tempo_ms': round(ms, 7)})
            print(f'n={n}, limiar={limiar}: {statistics.mean(tempos):.4f} ms', flush=True)
    with (RAIZ / 'limiar_medicoes.csv').open('w', encoding='utf-8-sig', newline='') as arquivo:
        out = csv.DictWriter(arquivo, fieldnames=['n','limiar','execucao','tempo_ms'])
        out.writeheader()
        out.writerows(registro)


if __name__ == '__main__':
    main()
