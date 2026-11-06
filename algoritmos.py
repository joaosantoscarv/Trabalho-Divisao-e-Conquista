"""Algoritmos do trabalho de Divisão e Conquista.

Convenções: índices desde 0; intervalo inclusivo; subarranjo não vazio.
Empates na soma: menor início e depois menor fim.
"""
from math import inf, sqrt


def _melhor_soma(a, b):
    return a if (-a[0], a[1], a[2]) <= (-b[0], b[1], b[2]) else b


def subarranjo_bruto(valores):
    """Soma máxima testando todos os intervalos, O(n²)."""
    if not valores:
        raise ValueError('O vetor precisa ter pelo menos um elemento.')
    melhor = (-inf, 0, 0)
    for inicio in range(len(valores)):
        soma = 0
        for fim in range(inicio, len(valores)):
            soma += valores[fim]
            melhor = _melhor_soma(melhor, (soma, inicio, fim))
    return melhor


def subarranjo_divisao(valores):
    """Soma máxima por divisão e conquista, O(n log n)."""
    if not valores:
        raise ValueError('O vetor precisa ter pelo menos um elemento.')

    def resolver(esq, dir_):
        if esq == dir_:
            return valores[esq], esq, dir_
        meio = (esq + dir_) // 2
        esquerda = resolver(esq, meio)
        direita = resolver(meio + 1, dir_)

        soma = 0
        melhor_esq = (-inf, meio)
        for i in range(meio, esq - 1, -1):
            soma += valores[i]
            if soma > melhor_esq[0] or (soma == melhor_esq[0] and i < melhor_esq[1]):
                melhor_esq = (soma, i)

        soma = 0
        melhor_dir = (-inf, meio + 1)
        for j in range(meio + 1, dir_ + 1):
            soma += valores[j]
            if soma > melhor_dir[0] or (soma == melhor_dir[0] and j < melhor_dir[1]):
                melhor_dir = (soma, j)

        cruzado = (melhor_esq[0] + melhor_dir[0], melhor_esq[1], melhor_dir[1])
        return _melhor_soma(_melhor_soma(esquerda, direita), cruzado)

    return resolver(0, len(valores) - 1)


def subarranjo_linear(valores):
    """Versão desafio em O(n) (Kadane), indicada nos critérios."""
    if not valores:
        raise ValueError('O vetor precisa ter pelo menos um elemento.')
    soma_atual = valores[0]
    inicio_atual = 0
    melhor = (valores[0], 0, 0)
    for i in range(1, len(valores)):
        if valores[i] > soma_atual + valores[i]:
            soma_atual = valores[i]
            inicio_atual = i
        else:
            soma_atual += valores[i]
        melhor = _melhor_soma(melhor, (soma_atual, inicio_atual, i))
    return melhor


def _distancia2(p, q):
    return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2


def _candidato(p, q):
    i, j = sorted((p[2], q[2]))
    return _distancia2(p, q), i, j


def _par_bruto_indexado(pontos):
    melhor = (inf, -1, -1)
    for i in range(len(pontos)):
        for j in range(i + 1, len(pontos)):
            melhor = min(melhor, _candidato(pontos[i], pontos[j]))
    return melhor


def _validar_pontos(pontos):
    if len(pontos) < 2:
        raise ValueError('São necessários pelo menos dois pontos.')
    for p in pontos:
        if len(p) != 2:
            raise ValueError('Cada ponto deve conter coordenadas x e y.')


def par_mais_proximo_bruto(pontos):
    """Retorna (distância, índice1, índice2), O(n²)."""
    _validar_pontos(pontos)
    dados = [(p[0], p[1], i) for i, p in enumerate(pontos)]
    d2, i, j = _par_bruto_indexado(dados)
    return sqrt(d2), i, j


def par_mais_proximo_divisao(pontos, limiar=32):
    """Par mais próximo em O(n log n); faixa de até 7 vizinhos por y."""
    _validar_pontos(pontos)
    if limiar < 2:
        raise ValueError('O limiar deve ser pelo menos 2.')
    dados = [(p[0], p[1], i) for i, p in enumerate(pontos)]
    px = sorted(dados, key=lambda p: (p[0], p[1], p[2]))
    py = sorted(dados, key=lambda p: (p[1], p[0], p[2]))

    def resolver(p_x, p_y):
        if len(p_x) <= limiar:
            return _par_bruto_indexado(p_x)

        m = len(p_x) // 2
        esquerda_x = p_x[:m]
        direita_x = p_x[m:]
        centro_x = direita_x[0][0]
        ids_esquerda = {p[2] for p in esquerda_x}
        esquerda_y = [p for p in p_y if p[2] in ids_esquerda]
        direita_y = [p for p in p_y if p[2] not in ids_esquerda]

        melhor = min(resolver(esquerda_x, esquerda_y), resolver(direita_x, direita_y))
        delta2 = melhor[0]
        faixa = [p for p in p_y if (p[0] - centro_x) ** 2 <= delta2]

        for i, ponto in enumerate(faixa):
            for prox in faixa[i + 1:i + 8]:
                if (prox[1] - ponto[1]) ** 2 > delta2:
                    break
                candidato = _candidato(ponto, prox)
                if candidato < melhor:
                    melhor = candidato
                    delta2 = melhor[0]
        return melhor

    d2, i, j = resolver(px, py)
    return sqrt(d2), i, j
