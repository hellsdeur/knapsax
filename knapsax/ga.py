# from knapsax.populational import Populational

# class GeneticAlgorithm(Populational):
#     def __init__(self, population_size, knapsack):
#         super().__init__(population_size, knapsack)

import numpy as np

class AGenetico:
    def __init__(self, dados: np.ndarray, nr_geracoes: int, **kwargs)-> None: 

        # DADOS 
        self.valor_item = dados[:, 0] 
        self.peso_item = dados[:, -1]
        
        # VARIAVEIS
        self.NR_GERACOES = nr_geracoes #Nr de geracoes
        self.QTY_CROMOSSOMOS = len(self.valor_item) # Qty de cromossomos
        self.TAXA_MUTACAO = kwargs.get("taxa_mutacao", 0.05) # Taxa de mutacao
        self.TAXA_CROMOSSOMOS = kwargs.get("taxa_cromossomos", 0.1)
        self.CAPACIDADE_MAX = kwargs.get("capacidade_max", 1550) # Capacidade máx da mochila
        self.MAX_TESTAR = kwargs.get("max_a_testar", 20000) # Nr de vezes a testar a funcao objetivo

        assert nr_geracoes< self.MAX_TESTAR,\
            "Nr de geracoes deve ser inferior a nr max de func objetivo a testar"

        # POPULACAO 
        # Determinar nr de populacao por cada geracao 
        base, resto = self.MAX_TESTAR // nr_geracoes, self.MAX_TESTAR % nr_geracoes
        self.POP_POR_GERACOES = [base] * nr_geracoes
        for i in range(resto):
            self.POP_POR_GERACOES[i] += 1
        self.POP_POR_GERACOES.sort()
        # # Determinar tamanho min da populacao inicial 
        self.TAM_MIN_POP = self.POP_POR_GERACOES[0]//2
        # Criar array vazio para populacao 
        self.populacao = np.empty((self.TAM_MIN_POP,
                self.QTY_CROMOSSOMOS))
   
        # MELHOR SOLUCAO
        self.melhor_sol = {
            "solucao": [],
            "valor_max": [],
            "custo_max": [],
            "geracao": [],
            "sol_testadas": [],
        }

    def resetar_variaveis(self):
        self.melhor_sol["solucao"]=[]
        self.melhor_sol["valor_max"]=[]
        self.melhor_sol["custo_max"]=[]
        self.melhor_sol["geracao"]=[]
        self.melhor_sol["sol_testadas"]=[]


    """Gerar a populacao. (Solucoes aleatorias)"""
    def gerar_populacao_inicial(self, tamanho_inicial):
        self.populacao = np.random.choice(
            [0,1], size=(
                tamanho_inicial,
                self.QTY_CROMOSSOMOS
                ), p=[1-self.TAXA_CROMOSSOMOS, self.TAXA_CROMOSSOMOS]
            )


    """ cruzamento_single_point"""
    def gerar_filhos (self, pop_por_geracao)->np.ndarray:
        tamanho_pop = len(self.populacao)
        nr_pais = len(self.populacao)
        while tamanho_pop <pop_por_geracao:
            pai_index=np.random.randint(0,nr_pais)
            mae_index=np.random.randint(0,nr_pais)
            pai, mae = np.array([
            self.populacao[pai_index],
            self.populacao[mae_index]
        ])
            corte = np.random.randint(1,len(pai)-1)
            filhos = np.array(
                [np.concatenate((pai[0:corte], mae[corte:])),
                 np.concatenate((mae[0:corte], pai[corte:]))
                 ])

            self.populacao = np.concatenate((self.populacao, filhos), axis=0)
            tamanho_pop = len(self.populacao)

        if tamanho_pop > pop_por_geracao:
            elemento = np.random.randint(nr_pais,tamanho_pop)
            self.populacao = np.delete(self.populacao,[elemento], axis=0)
      

    def mutacao_bit_flip(self, populacao: np.ndarray)-> np.ndarray:
        # 0 com (1-prob)% de chance, 1 com prob% de chance
        mutador = np.random.choice([0, 1],
                                   size=(1,self.QTY_CROMOSSOMOS),
                                   p=[1-self.TAXA_MUTACAO, self.TAXA_MUTACAO])
        return np.abs(populacao-mutador)  


    def avaliar_solucoes(self)->np.ndarray:
        valor = np.sum(self.populacao * self.valor_item.T, axis=1, keepdims=True)
        capacidade = np.sum(self.populacao * self.peso_item.T, axis=1, keepdims=True)
        self.populacao = np.concatenate((self.populacao, valor, capacidade), axis=1)
        """eliminar as solucoes que nao atendem
        a restricao de capacidade maxima"""
        linhas_a_excluir = np.argwhere(self.populacao[:,-1] > self.CAPACIDADE_MAX).reshape(-1,)
        self.populacao = np.delete(self.populacao, linhas_a_excluir, axis=0)

        """Ordenar os melhores valores
        em ordem decrescente"""
        if len(self.populacao)>0:
            self.populacao = self.populacao[np.argsort(self.populacao[:,-2])[::-1]]


    def atualizar_melhor_sol(self, geracao, pop_geracao)->None:

        def atualizar_com_zeros():
            self.melhor_sol["valor_max"].append(0)
            self.melhor_sol["custo_max"].append(0)
            self.melhor_sol["solucao"].append(None)

        def atualizar_novo_valor():
            self.melhor_sol["valor_max"].append(valor_maximo)
            self.melhor_sol["custo_max"].append(custo_maximo)
            self.melhor_sol["solucao"].append(solucao_optima)

        def atualizar_valor_antigo():
            self.melhor_sol["valor_max"].append(self.melhor_sol["valor_max"][-1])
            self.melhor_sol["custo_max"].append(self.melhor_sol["custo_max"][-1])
            self.melhor_sol["solucao"].append(self.melhor_sol["solucao"][-1])

        
        if self.populacao.shape[0] > 0:
            # Se a populacao tiver solucoes validas 
            valor_maximo = self.populacao[0][-2]
            custo_maximo = self.populacao[0][-1]
            solucao_optima = self.populacao[0][:-2]
            if (len(self.melhor_sol["valor_max"])==0):
                # Se a lista estiver vazia (atualizar com o novo valor)
                atualizar_novo_valor()
            else:
                # Se a lista nao estiver vazia
                if self.melhor_sol["valor_max"][-1]<valor_maximo:
                    # Se o ultimo valor for menor que o atual (atualizar com novo valor)
                    atualizar_novo_valor()
                else:
                    # Se o ultimo valor for maior/igual ao atual (manter o ultimo)
                    atualizar_valor_antigo()
        else:
            # se a populacao nao tiver individuos validos
            if (len(self.melhor_sol["valor_max"])==0):
                # Se a lista estiver vazia(Atualizar com zeros)
                atualizar_com_zeros()
            else:
                # Se a lista nao estiver vazia (Atualizar com ultimo valor)
                atualizar_valor_antigo()
                
        # Atualizar a geracao e as solucoes testadas 
        self.melhor_sol["geracao"].append(geracao)
        self.melhor_sol["sol_testadas"].append(pop_geracao)
     
       
    def solucionar(self) -> np.ndarray:
        self.resetar_variaveis()
        self.gerar_populacao_inicial(self.TAM_MIN_POP)
        self.gerar_filhos(self.POP_POR_GERACOES[0])
        # Avaliar, selecionar só os melhores e atualizar solucao
        # solucoes_testadas=len(self.populacao)
        geracao = 1
        self.avaliar_solucoes()
        self.atualizar_melhor_sol(
            geracao, self.POP_POR_GERACOES[0]
            )

        for pop in (self.POP_POR_GERACOES[1:]):
            if self.populacao.shape[0]>0:
                # se a primeira iteracao gerar solucoes validas
                self.populacao = np.delete(
                    self.populacao, [-2,-1], axis=1
                    )  # apaga colunas de valor e custo
                self.populacao = self.mutacao_bit_flip(self.populacao)
            else:
                # se a primeira iteracao nao gerar solucoes validas
                self.gerar_populacao_inicial(pop//2)

            self.gerar_filhos(pop)
            geracao +=1
            self.avaliar_solucoes()
            self.atualizar_melhor_sol(
            geracao, pop
            )
        
