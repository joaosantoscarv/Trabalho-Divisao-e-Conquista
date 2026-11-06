# Trabalho Prático — Divisão e Conquista

Implementações em **Python 3** dos dois problemas do enunciado: subarranjo de soma máxima e par de pontos mais próximos, comparando força bruta e divisão e conquista. Também está incluída a variante O(n) do subarranjo (questão-desafio citada nos critérios).

## Arquivos

- `algoritmos.py` — cinco implementações, retornos e validações.
- `main.py` — entrada manual pelo terminal.
- `casos_teste.json` — entradas, saídas esperadas e casos de borda.
- `test_algoritmos.py` — testes documentados e testes aleatórios de comparação.
- `benchmark.py` — repetição dos experimentos e geração dos gráficos.
- `medicoes_brutas.csv` — tempos reais de cada repetição (5 por configuração).
- `experimento_limiar.py` e `limiar_medicoes.csv` — medição complementar de limiares 2, 8, 16, 32 e 64.
- `resumo_medicoes.csv` — médias e dispersão dos tempos.
- `ambiente_medicao.json` — configuração do ambiente em que o experimento foi executado.
- `graficos/` — gráficos de ambas as etapas.
- `Relatorio_Divisao_e_Conquista.pdf` — relatório acadêmico (máximo de 8 páginas).

## Como executar no Windows / PowerShell (VS Code)

Abra a pasta do trabalho no VS Code. No terminal integrado:

```powershell
python --version
python -m pip install -r requirements.txt
python -m unittest -v test_algoritmos.py
```

Se o comando `python` não funcionar, tente `py` no Windows.

### Etapa 1 — Subarranjo

```powershell
python main.py subarranjo --metodo bruto --valores "-2,1,-3,4,-1,2,1,-5,4"
python main.py subarranjo --metodo divisao --valores "-2,1,-3,4,-1,2,1,-5,4"
python main.py subarranjo --metodo linear --valores "-2,1,-3,4,-1,2,1,-5,4"
```

Saída esperada (para os três métodos): soma `6`, índices `[3, 6]`, subarranjo `[4, -1, 2, 1]`. Índices começam em zero e o fim é inclusivo. Empates usam o menor início e, depois, o menor fim. O subarranjo deve conter pelo menos um elemento.

### Etapa 2 — Par de pontos

```powershell
python main.py pontos --metodo bruto --pontos "0,0;3,4;1,1"
python main.py pontos --metodo divisao --pontos "0,0;3,4;1,1"
python main.py pontos --metodo divisao --limiar 2 --pontos "0,0;3,4;1,1"
```

Saída esperada: menor distância `1.41421356`, par de índices `(0, 2)` para os pontos `(0, 0)` e `(1, 1)`. O algoritmo retorna a distância **euclidiana**, não a distância ao quadrado.

### Etapa 3 — Medições reais e gráficos

```powershell
python benchmark.py
```

Por padrão, mede 5 execuções (mais uma de aquecimento, fora das medições) para cada algoritmo e tamanho 100, 200, 400, 800, 1.600, 3.200 e 6.400. A execução completa pode demorar, pois o método de força bruta compara todos os pares. O CSV e os gráficos são substituídos pelos resultados **do seu computador** ao rodar novamente o benchmark. O limiar 32 foi fixado como escolha inicial e não foi o mais rápido no estudo complementar; nesse ambiente, o limiar 8 foi melhor. Para avaliar os limiares na sua máquina, execute `python experimento_limiar.py`.

## Algoritmos e complexidades

| Problema | Método | Tempo | Recorrência |
|---|---|---|---|
| Subarranjo | Força bruta | O(n²) | Não recursivo, soma incremental |
| Subarranjo | Divisão e conquista | O(n log n) | T(n) = 2T(n/2) + O(n) |
| Subarranjo | Linear (desafio) | O(n) | Atualização O(1) por elemento |
| Pontos | Força bruta | O(n²) | Não recursivo, todos os pares |
| Pontos | Divisão e conquista | O(n log n) | T(n) = 2T(n/2) + O(n) + ordenação inicial O(n log n) |

O algoritmo de pontos recebe duas listas inicialmente ordenadas (por x e por y). A divisão preserva a ordem em y; na faixa central, compara no máximo 7 sucessores de cada ponto. Usa o limiar 32 para trocar recursão por força bruta em subproblemas pequenos sem mudar a ordem assintótica.

## Publicar no GitHub

O enunciado pede **repositório Git com histórico de commits ao longo do desenvolvimento**. Este ZIP contém os arquivos, mas **não cria retrospectivamente esse histórico**. Na pasta do trabalho:

```powershell
git init
git add algoritmos.py main.py casos_teste.json test_algoritmos.py
git commit -m "Implementa algoritmos e testes"
git add benchmark.py experimento_limiar.py requirements.txt README.md medicoes_brutas.csv resumo_medicoes.csv limiar_medicoes.csv ambiente_medicao.json graficos/ Relatorio_Divisao_e_Conquista.pdf
git commit -m "Adiciona experimentos, graficos e relatorio"
```

Depois crie um repositório **vazio** no GitHub e use a URL de seu repositório:

```powershell
git branch -M main
git remote add origin URL_DO_SEU_REPOSITORIO
git push -u origin main
```

Os commits gerados agora documentam a preparação atual, **não** substituem o histórico real de semanas pedido pelo professor. Complete autoria, dupla e dados de capa antes da entrega.

## Observação sobre o enunciado

A Etapa 3 dá tamanhos de exemplo e chama-os de "dígitos" embora a Etapa 2 trabalhe com pontos. Aqui os tamanhos representam **quantidades de elementos ou pontos**. Os critérios citam uma versão linear O(n) de "questão desafio" que não é detalhada no corpo do texto; foi fornecida como a versão linear do subarranjo máximo, que possui solução O(n).
