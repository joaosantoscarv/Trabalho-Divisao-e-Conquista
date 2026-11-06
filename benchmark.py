"""Mede os tempos reais; gera CSV bruto, resumo, gráficos e ambiente.

Uso: python benchmark.py
Dependência para os gráficos: matplotlib
"""
import argparse
import csv
import json
import math
import os
import platform
import random
import statistics
import sys
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from algoritmos import (
    subarranjo_bruto, subarranjo_divisao, subarranjo_linear,
    par_mais_proximo_bruto, par_mais_proximo_divisao,
)

ROOT = Path(__file__).parent


def configura_maquina():
    cpu = platform.processor() or 'CPU não identificado'
    if Path('/proc/cpuinfo').exists():
        for linha in Path('/proc/cpuinfo').read_text(errors='replace').splitlines():
            if linha.lower().startswith('model name'):
                cpu = linha.partition(':')[-1].strip()
                break
    return {
        'momento_utc': datetime.now(timezone.utc).isoformat(timespec='seconds'),
        'sistema': platform.platform(), 'python': sys.version.split()[0],
        'cpu_modelo_reportado': cpu,
        'cpus_logicas_visiveis': os.cpu_count(),
        'nota': ('Medições realizadas no ambiente de execução que gerou o trabalho; '
                 'esses números não representam o computador do aluno.'),
    }


def executar(tamanhos, repeticoes, limiar, seed):
    if repeticoes < 5:
        raise ValueError('A atividade exige pelo menos 5 execuções por tamanho.')
    rng = random.Random(seed)
    bruto = []
    funcoes = {
        'subarranjo': [('Força bruta', subarranjo_bruto),
                       ('Divisão e conquista', subarranjo_divisao),
                       ('Linear O(n)', subarranjo_linear)],
        'pontos': [('Força bruta', par_mais_proximo_bruto),
                   ('Divisão e conquista', lambda ps: par_mais_proximo_divisao(ps, limiar=limiar))],
    }
    for problema in funcoes:
        for n in tamanhos:
            if problema == 'subarranjo':
                dados = [rng.randint(-100, 100) for _ in range(n)]
            else:
                dados = [(rng.uniform(-5000, 5000), rng.uniform(-5000, 5000))
                         for _ in range(n)]

            # Mesmo caso de teste em todas as implementações e repetições.
            referencia = funcoes[problema][0][1](dados) if n <= 100 else None
            for nome, funcao in funcoes[problema]:
                # Chamada de aquecimento fora da medição.
                aquecimento = funcao(dados)
                if referencia is not None:
                    if problema == 'subarranjo' and aquecimento != referencia:
                        raise AssertionError(f'Divergência no problema {problema}, n={n}')
                    if problema == 'pontos' and not math.isclose(aquecimento[0], referencia[0], rel_tol=1e-12):
                        raise AssertionError(f'Divergência no problema {problema}, n={n}')
                for rep in range(1, repeticoes + 1):
                    inicio = time.perf_counter_ns()
                    resultado = funcao(dados)
                    duracao = time.perf_counter_ns() - inicio
                    if problema == 'subarranjo' and resultado != aquecimento:
                        raise AssertionError('Inconsistência de saída no benchmark')
                    if problema == 'pontos' and not math.isclose(resultado[0], aquecimento[0], rel_tol=1e-12):
                        raise AssertionError('Inconsistência de distância no benchmark')
                    bruto.append({'problema': problema, 'algoritmo': nome, 'n': n,
                                  'execucao': rep, 'tempo_ns': duracao,
                                  'tempo_ms': round(duracao / 1e6, 8)})
                tempos = [b['tempo_ms'] for b in bruto
                          if b['problema'] == problema and b['algoritmo'] == nome and b['n'] == n]
                print(f'{problema} n={n:<5} {nome:<20} média={statistics.mean(tempos):.4f} ms', flush=True)

    with (ROOT / 'medicoes_brutas.csv').open('w', newline='', encoding='utf-8-sig') as arquivo:
        writer = csv.DictWriter(arquivo, fieldnames=list(bruto[0]))
        writer.writeheader()
        writer.writerows(bruto)

    grupos = defaultdict(list)
    for linha in bruto:
        grupos[(linha['problema'], linha['algoritmo'], linha['n'])].append(linha['tempo_ms'])
    resumo = []
    for (problema, algoritmo, n), lista in sorted(grupos.items()):
        resumo.append({'problema': problema, 'algoritmo': algoritmo, 'n': n,
                       'execucoes': len(lista),
                       'media_ms': round(statistics.mean(lista), 6),
                       'desvio_padrao_ms': round(statistics.stdev(lista), 6),
                       'min_ms': round(min(lista), 6),
                       'max_ms': round(max(lista), 6)})
    with (ROOT / 'resumo_medicoes.csv').open('w', newline='', encoding='utf-8-sig') as arquivo:
        writer = csv.DictWriter(arquivo, fieldnames=list(resumo[0]))
        writer.writeheader()
        writer.writerows(resumo)

    ambiente = configura_maquina()
    ambiente.update({'seed': seed, 'tamanhos': tamanhos,
                     'execucoes_por_algoritmo_tamanho': repeticoes,
                     'limiar_par_mais_proximo': limiar,
                     'relogio': 'time.perf_counter_ns; tempo em milissegundos',
                     'aquecimento': 'uma chamada não medida para cada configuração',
                     'tipo_entrada_subarranjo': 'inteiros uniformes em [-100,100]',
                     'tipo_entrada_pontos': 'coordenadas uniformes em [-5000,5000]',
                     'comparacoes': 'mesma entrada para métodos do mesmo problema e tamanho'})
    (ROOT / 'ambiente_medicao.json').write_text(
        json.dumps(ambiente, indent=2, ensure_ascii=False), encoding='utf-8')
    graficos(resumo)


def graficos(resumo):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    saida = ROOT / 'graficos'
    saida.mkdir(exist_ok=True)
    for problema, titulo in (
        ('subarranjo', 'Subarranjo de soma máxima'),
        ('pontos', 'Par de pontos mais próximos'),
    ):
        linhas = [r for r in resumo if r['problema'] == problema]
        for log in (False, True):
            fig, ax = plt.subplots(figsize=(9, 5))
            for nome in sorted({r['algoritmo'] for r in linhas}):
                serie = sorted((r for r in linhas if r['algoritmo'] == nome), key=lambda a: a['n'])
                ax.plot([r['n'] for r in serie], [r['media_ms'] for r in serie],
                        marker='o', linewidth=1.8, label=nome)
            ax.set_title(titulo + (' — escala logarítmica' if log else ' — tempo médio'))
            ax.set_xlabel('Tamanho da entrada (n)')
            ax.set_ylabel('Tempo médio de execução (ms)')
            if log:
                ax.set_xscale('log', base=2)
                ax.set_yscale('log')
            ax.grid(alpha=0.25)
            ax.legend()
            fig.tight_layout()
            nome_arquivo = f'{problema}_{"log" if log else "linear"}.png'
            fig.savefig(saida / nome_arquivo, dpi=170)
            plt.close(fig)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--tamanhos', nargs='+', type=int,
                        default=[100, 200, 400, 800, 1600, 3200, 6400])
    parser.add_argument('--repeticoes', type=int, default=5)
    parser.add_argument('--limiar', type=int, default=32)
    parser.add_argument('--seed', type=int, default=2026)
    a = parser.parse_args()
    executar(a.tamanhos, a.repeticoes, a.limiar, a.seed)


if __name__ == '__main__':
    main()
