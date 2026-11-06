"""Interface no terminal para os algoritmos."""
import argparse
import sys
from algoritmos import (
    subarranjo_bruto, subarranjo_divisao, subarranjo_linear,
    par_mais_proximo_bruto, par_mais_proximo_divisao,
)


def main():
    parser = argparse.ArgumentParser(description='Trabalho: Divisão e Conquista')
    parser.add_argument('problema', choices=['subarranjo', 'pontos'])
    parser.add_argument('--metodo', choices=['bruto', 'divisao', 'linear'], default='divisao')
    parser.add_argument('--valores', help='Inteiros separados por vírgulas: -2,1,-3,4')
    parser.add_argument('--pontos', help='Pontos x,y separados por ;: 0,0;1,2;3,4')
    parser.add_argument('--limiar', type=int, default=32)
    # argparse pode interpretar "-2,1,-3" como outra opção; aceitamos esse
    # formato quando usado após --valores ou --pontos.
    entrada = sys.argv[1:]
    for chave in ('--valores', '--pontos'):
        if chave in entrada:
            pos = entrada.index(chave)
            if pos + 1 < len(entrada) and entrada[pos + 1].startswith('-') and ',' in entrada[pos + 1]:
                entrada[pos] = chave + '=' + entrada[pos + 1]
                entrada.pop(pos + 1)
    args = parser.parse_args(entrada)

    if args.problema == 'subarranjo':
        if args.valores is None:
            parser.error('Para subarranjo, use --valores "-2,1,-3,4"')
        try:
            v = [int(s.strip()) for s in args.valores.split(',')]
        except ValueError:
            parser.error('Todos os valores devem ser inteiros.')
        funcoes = {'bruto': subarranjo_bruto, 'divisao': subarranjo_divisao,
                   'linear': subarranjo_linear}
        soma, inicio, fim = funcoes[args.metodo](v)
        print(f'Soma máxima: {soma}')
        print(f'Intervalo (índices desde zero): [{inicio}, {fim}]')
        print(f'Subarranjo: {v[inicio:fim + 1]}')
    else:
        if args.metodo == 'linear':
            parser.error('Método linear aplica-se apenas ao subarranjo.')
        if args.pontos is None:
            parser.error('Para pontos, use --pontos "0,0;3,4"')
        try:
            pontos = [tuple(float(x.strip()) for x in bloco.split(','))
                      for bloco in args.pontos.split(';')]
        except ValueError:
            parser.error('Pontos devem ter coordenadas numéricas x,y.')
        funcao = par_mais_proximo_bruto if args.metodo == 'bruto' else par_mais_proximo_divisao
        dist, i, j = (funcao(pontos, limiar=args.limiar)
                      if args.metodo == 'divisao' else funcao(pontos))
        print(f'Menor distância: {dist:.8f}')
        print(f'Índices dos pontos: ({i}, {j})')
        print(f'Pontos: {pontos[i]} e {pontos[j]}')


if __name__ == '__main__':
    main()
