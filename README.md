# knapsax
Aplicação de metaheurísticas ao problema da mochila, para disciplina de Metaheurísticas para Otimização Combinatória ofertada pelo PPGCC-UFPA, realizado no período 2025.1.

# Configuração

1. Crie um ambiente virtual para o projeto.

1.1. Usando Poetry.

```poetry install```

1.2. Usando pip.

```python -m venv env```

```source activate env```

```pip install -r requirements.txt```

2. Utilize a receita `all` do Makefile para criar os diretórios e baixar os arquivos necessários:

```make all```

3. Realize ou consulte os experimentos no diretório `notebooks`, e os códigos-fonte no diretório `knapsack`.