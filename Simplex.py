
class Simplex:

    # Inicializo a tabela que o algoritmo irá operacionar sobre.        
    def __init__(self):
        self.tabela = []
    
    #    Aqui, recebemos uma lista (que é a própria função objetivo)
    #    e atribuímos essa lista à primeira a da tabela, já que
    #    sempre a primeira linha será a linha da função objetiva.
    def indicarFuncaoObjetivo(self, funcaoObjetiva: list):
        self.tabela.append(funcaoObjetiva)

    #   Restricoes as quais a função objetiva esta sujeita à.
    def adicionarRestricoes(self, restricoesSujeitas: list):
        self.tabela.append(restricoesSujeitas)


    #   Identificando as variáveis que entrarão na base:
    #   "A coluna que entra"
    def recuperarColunaDeEntrada(self) -> int:
        # Encontramos o pivo pegando o menor valor da tabela na linha 0,
        # que é a linha da função objetiva, e retornamos sua posição.
        pivo_coluna = min(self.tabela[0])
        indice = self.tabela[0].index(pivo_coluna)

        return indice

    def recuperarLinhaQueSai(self, indiceColunaDeEntrada: int) -> int:
        resultados = {}
        tamanhoTabela = len(self.tabela)
        # itera as linhas da tabela
        for linha in range(tamanhoTabela):
            # devo ignorar a linha 0, pois ela contem minha função objetivo, que não vem ao caso.
            if linha > 0:
                # nesse ponto, ele verifica que o pivô é maior que zero.
                if self.tabela[linha][indiceColunaDeEntrada] > 0:
            #  Com o -1 pego a última coluna (que me dá o último número da linha em questão)
            #  e com o indiceColunaDeEntrada pego o pivo dessa mesma linha
                    divisao = self.tabela[linha][-1] / self.tabela[linha][indiceColunaDeEntrada]
                    # nesse ponto, precisamos armazenar o resultado da divisão e em qual 
                    # linha esse resultado está sendo armazenado
                    resultados[linha] = divisao
        # o menor valor de divisao encontrado no dicionário "results"
        # retorna seu índice, que será a linha a ser removida.  
        indice = min(resultados, key=resultados.get)

        return indice

    def recuperarNovaLinhaPivo(self, indiceColunaDeEntrada, indiceLinhaASerRemovida):
        linhaASair = self.tabela[indiceLinhaASerRemovida]

        pivo = linhaASair[indiceColunaDeEntrada]
        
        # Essa nova linha é obtida pela divisao de todos os valores da linha a ser removida
        # divididos pelo pivo da linha
        novaLinhaPivo = [i / pivo for i in linhaASair]

        return novaLinhaPivo


    def calcularNovaLinha(self, linhaASerSubstituida: list, indiceColunaDeEntrada: int, linhaPivo: list): 
        # aqui, o pivo deve ter seu sinal invertido, por regra do algoritmo simplex.
        pivoLinhaASerSubstituida = linhaASerSubstituida[indiceColunaDeEntrada] * -1

        # a linha de resultado, i.e, a nova linha que será retornada, é composta pela multiplicacao
        # do pivo por cada elemento da linhaPivo somada com cada elemento da linha a ser substituida

        aux_line = [ i * pivoLinhaASerSubstituida for i in linhaPivo]
# return [ (linhaASerSubstituida[i] + (i * pivoLinhaASerSubstituida)) for i in linhaPivo] (((((POSSIVEL ALTERNATIVA)))))
        
        linha_resultado = []

        for i in range(len(aux_line)):
            valor_somado = aux_line[i] + linhaASerSubstituida[i]
            linha_resultado.append(valor_somado)

        return linha_resultado

    def existemValoresNegativos(self):
        # utilizamos função lambda para exemplificar como isso é 
        # feito de forma intuitiva. todos os elementos da primei
        # ra linha tem seu sinal verificado, caso haja algum que
        # seja negativo, o método retorna true e o Simplex continua.
        valoresNegativos = list(filter(lambda x: x < 0,self.tabela[0]))
        
        # se algum valor negativo foi encontrado, retornamos True,
        # e o Simplex deve continuar.
        return len(valoresNegativos) > 0 


    def calcular(self):

        colunaQueEntra = self.recuperarColunaDeEntrada()

        indicePrimeiraLinhaASair = self.recuperarLinhaQueSai(colunaQueEntra)

        # Essa é a minha linha pivo, que teve o índice recuperado
        # no método "recuperarLinhaQueSai"
        linhaPivo = self.recuperarNovaLinhaPivo(colunaQueEntra, indicePrimeiraLinhaASair)

        #Agora, precisamos substituir essa linha a sair na própria tabela
        self.tabela[indicePrimeiraLinhaASair] = linhaPivo

        # Nesse momento, precisamos manipular a tabela sem alterar a origi
        # nal, então, criamos uma tabela de copia.

        tabelaCopia = self.tabela.copy()

        index = 0

        # Agora, precisaremos realizar as operações feitas acima(na primeira linha)
        # para todas as linhas da tabela.
        while( index < len(self.tabela)):
            if(index != indicePrimeiraLinhaASair):
                linhaQueVaiSair = tabelaCopia[index]
                novaLinha = self.calcularNovaLinha(linhaQueVaiSair, colunaQueEntra, linhaPivo)
                self.tabela[index] = novaLinha
            index += 1
        

    def exibirTabela(self):
        for i in range(len(self.tabela)):
            for j in range(len(self.tabela[i])):
                print('{:.4f}\t'.format(self.tabela[i][j]), end='')
            print()
        print('\n=-=-=-=-\nNesse caso, a primeira linha da tabela é referente a função objetiva\ne a segunda linha é nosso resultado.')

    def solve(self):
        self.calcular()

        while(self.existemValoresNegativos()):
            self.calcular()
            
        
        self.exibirTabela()

if __name__ == "__main__":
    simplex = Simplex()
    simplex.indicarFuncaoObjetivo([1.6, 20 , 25.6 , 13.25, 1.87, 30.0, 20.0, 30.0 , 6.0 , 15.0 , 37 , 3.2 , 7.6 , 24.9,30.0 , 6.0 , 15.0 , 37 , 3.2 , 7.6 , 24.9 ,0])

    # proteina
    simplex.adicionarRestricoes([1.0, 20, 25.58, 13.25, 1.87, 30, 20, 30, 6, 15, 37.04, 3.22, 7.55, 24.9, 22.5, 1.3, 7.2, 3.3, 21, 2.82, 1.0, 0.27])

    # #complexo
    simplex.adicionarRestricoes([0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 2, 1, 0, 1.2, 0.05])

    # #gord totais
    simplex.adicionarRestricoes([0, 22, 8.193, 6.75, 3.2, 20, 20, 3, 8, 28, 28.04, 0.906, 12.87, 12.14, 19.4, 0, 30, 5, 28.7, 0.049, 0, 0.11])
    
    # #fibra
    simplex.adicionarRestricoes([0, 0, 0, 0, 1.1, 1, 0, 1, 0.5, 0, 0, 2.7, 0, 0, 0, 1.4, 2.5, 3.5, 0, 2.6, 0, 0.02])

    # #minerais
    simplex.adicionarRestricoes([0.912, 0.47, 0.138, 0, 0.12, 1, 0.3, 0.2, 0.05, 0.11, 0.565, 0.285, 0.12, 0.098, 0, 0.8, 0.9, 0, 1.3, 0.316, 0, 0.01])

    #vitaminas
    simplex.adicionarRestricoes([0.0, 0.0, 0.0, 0.0, 0.22, 1, 0.95, 1.0, 0.1, 0.21, 0.0, 0.0, 0.0, 0.0, 0.0, 1.12, 0.9, 0.05, 1.92, 0.0, 0.1, 0.02])


    # colesterol
    simplex.adicionarRestricoes([0 , 1.15 , 0.07 , 1 , 0.96 , 0.1 , 0.3 , 0 , 0.3 , 1.3 , 0.11 , 0 , 0.11 , 0.105 , 0.07 , 0.5 , 0 , 0.01 , 0.09 , 0 , 0 , 0.03])
    #sodio
    simplex.adicionarRestricoes([0.0453 , 13.8 , 0.876 , 1.2 , 0.7 , 0.2 , 0.6 , 0.15 , 0.5 , 0.9 , 2.31 , 0 , 0.296 , 0.621 , 0.72 , 0.03 , 0 , 0.1 , 0.4 , 0.033 , 0.34, 0.04])
    #sat
    simplex.adicionarRestricoes([0 , 8.16 , 17.08 , 3.25 , 0.5 , 15 , 19.5 , 0 , 3 , 8.8 , 13.74 , 0.182 , 21.97 , 21.092 , 15.6 , 0 , 17.5 , 1 , 18.66 , 0.039 , 0, 0.15])
    #trans
    simplex.adicionarRestricoes([0 , 0.43,	0 , 1.20,0 , 0 , 0.75 , 0 , 0 , 0.23 , 0 , 0 , 0 , 0.32 , 0 , 0 , 0 , 0 , 0 , 0 , 0, 0.05])

    #carb simples
    simplex.adicionarRestricoes([0 , 8.16 , 17.08 , 3.25 , 0.5 , 15 , 19.5 , 0 , 3 , 8.8 , 13.74 , 0.182 , 21.97 , 21.092 , 15.6 , 0 , 17.5 , 1 , 18.66 , 0.039 , 0  ,0.25])
    simplex.solve()
