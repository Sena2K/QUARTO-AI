import copy
import sys
import random


class JogoQuarto:
    def __init__(self):
        self.tabuleiro = [[None] * 4 for _ in range(4)]
        self.jogador_atual = 1
        self.pecas_disponiveis = [(cor, altura, forma, consistencia) for cor in range(2)
                                  for altura in range(2) for forma in range(2) for consistencia in range(2)]
        random.shuffle(self.pecas_disponiveis)
        self.posicoes_vencedoras = self.gerar_posicoes_vencedoras()
        self.jogadas_jogador = []  # Lista para armazenar as jogadas do jogador

    def obter_jogadas_jogador(self):
        return self.jogadas_jogador

    def gerar_posicoes_vencedoras(self):
        posicoes_vencedoras = []
        for i in range(4):  # linhas e colunas
            posicoes_vencedoras.append([(i, j) for j in range(4)])
            posicoes_vencedoras.append([(j, i) for j in range(4)])
        # diagonais
        posicoes_vencedoras.append([(i, i) for i in range(4)])
        posicoes_vencedoras.append([(i, 3 - i) for i in range(4)])
        return posicoes_vencedoras

    def exibir_tabuleiro(self):
        print("  0 1 2 3")
        for i in range(4):
            print(i, end=" ")
            for j in range(4):
                peca = self.tabuleiro[i][j]
                if peca is None:
                    print("\033[30m.\033[m", end=" ")  # Representa peça vazia com ponto preto
                else:
                    cor = "\033[31m" if peca == 1 else "\033[34m"  # Cor vermelha para jogador 1, azul para jogador 2
                    print(cor + "X" + "\033[m", end=" ")  # X representa uma peça ocupada
            print()

    def jogador_venceu(self, jogador):
        vetores = [
            [self.tabuleiro[i][j] for i in range(4)] for j in range(4)
        ]  # Transforma as colunas do tabuleiro em vetores

        # Verifica se há um elemento em comum na mesma posição em todos os vetores
        for posicoes in self.posicoes_vencedoras:
            elementos = [vetores[i][j] for i, j in posicoes]
            if all(elemento == jogador for elemento in elementos):
                # Verifica se há uma característica em comum no vetor
                caracteristicas = set()
                for i, j in posicoes:
                    caracteristicas.add(self.tabuleiro[i][j])
                if len(caracteristicas) == 1:  # Todas as peças possuem a mesma característica
                    return True
        return False

    def empate(self):
        return all(self.tabuleiro[i][j] is not None for i in range(4) for j in range(4))

    def obter_jogadas_validas(self):
        return [(i, j, *self.pecas_disponiveis[-1]) for i in range(4) for j in range(4) if self.tabuleiro[i][j] is None]

    def fazer_jogada(self, jogada):
        i, j, cor, altura, forma, consistencia = jogada
        if self.tabuleiro[i][j] is not None:
            raise ValueError("Jogada inválida")

        self.tabuleiro[i][j] = self.jogador_atual
        self.pecas_disponiveis.pop()

        print("Tabuleiro após a jogada:")
        self.exibir_tabuleiro()

        print("Vetores:")
        vetores = [[self.tabuleiro[i][j] for i in range(4)] for j in range(4)]
        for vetor in vetores:
            print(vetor)

        if self.jogador_venceu(self.jogador_atual):
            print("Jogador", self.jogador_atual, "venceu!")
            return self.jogador_atual
        elif self.empate():
            print("Empate!")
            return 0  # Empate
        else:
            self.jogador_atual = 3 - self.jogador_atual  # Trocar de jogador
            return None

    def jogar(self):
        while True:
            self.exibir_tabuleiro()
            jogadas_validas = self.obter_jogadas_validas()
            print("Peça disponível:", self.pecas_disponiveis[-1])
            print("Jogadas válidas:", jogadas_validas)
            if jogadas_validas:
                jogada = None
                while jogada not in jogadas_validas:
                    jogada = input("Digite sua jogada (linha coluna cor altura forma consistencia): ")
                    try:
                        jogada = tuple(map(int, jogada.split()))
                        if len(jogada) != 6:
                            raise ValueError
                    except (ValueError, IndexError):
                        print("Entrada inválida. Por favor, digite apenas os valores separados por espaços.")
                        jogada = None
                resultado = self.fazer_jogada(jogada)
                if resultado is not None:
                    if resultado == 0:
                        print("Empate!")
                    elif resultado == "IA":
                        print("IA ganhou!")
                    else:
                        print("Jogador", resultado, "venceu!")
                    break


class IAQuarto:
    def __init__(self, profundidade):
        self.profundidade = profundidade

    def avaliar(self, jogo):
        # Inicializa a pontuação para cada jogador
        pontuacao_jogador1 = 0
        pontuacao_jogador2 = 0

        # Avalia as linhas, colunas e diagonais vitoriosas
        for posicoes in jogo.posicoes_vencedoras:
            elementos = [jogo.tabuleiro[i][j] for i, j in posicoes]
            if all(elem is not None for elem in elementos):
                jogador = elementos[0]
                if all(elem == jogador for elem in elementos):
                    caracteristicas = set(elementos)
                    if len(caracteristicas) == 1:
                        if jogador == 1:
                            pontuacao_jogador1 += 1
                        else:
                            pontuacao_jogador2 += 1

        # Contagem de possíveis vitórias
        for jogador in [1, 2]:
            for posicoes in jogo.posicoes_vencedoras:
                vitorias_possiveis = 0
                for i, j in posicoes:
                    if jogo.tabuleiro[i][j] is None:
                        if all(jogo.tabuleiro[x][y] != jogador for x, y in posicoes):
                            vitorias_possiveis += 1
                if jogador == 1:
                    pontuacao_jogador1 += vitorias_possiveis
                else:
                    pontuacao_jogador2 += vitorias_possiveis

        # Contagem de peças em linhas e colunas
        for jogador in [1, 2]:
            for i in range(4):
                pecas_linha = sum(1 for j in range(4) if jogo.tabuleiro[i][j] == jogador)
                pecas_coluna = sum(1 for j in range(4) if jogo.tabuleiro[j][i] == jogador)
                if jogador == 1:
                    pontuacao_jogador1 += pecas_linha + pecas_coluna
                else:
                    pontuacao_jogador2 += pecas_linha + pecas_coluna

        # Formação de blocos de peças
        for jogador in [1, 2]:
            for i in range(4):
                for j in range(4):
                    if jogo.tabuleiro[i][j] == jogador:
                        pecas_similares_linha = sum(1 for k in range(4) if jogo.tabuleiro[i][k] == jogador)
                        pecas_similares_coluna = sum(1 for k in range(4) if jogo.tabuleiro[k][j] == jogador)
                        if jogador == 1:
                            pontuacao_jogador1 += pecas_similares_linha + pecas_similares_coluna
                        else:
                            pontuacao_jogador2 += pecas_similares_linha + pecas_similares_coluna

        # Retorna a diferença de pontuação entre os jogadores
        return pontuacao_jogador1 - pontuacao_jogador2

    def minimax(self, jogo, profundidade, jogador_maximizador, alfa, beta):
        if profundidade == 0 or jogo.jogador_venceu(1) or jogo.jogador_venceu(2) or jogo.empate():
            return self.avaliar(jogo), None

        if jogador_maximizador:
            max_eval = -sys.maxsize
            melhor_jogada = None
            for jogada in jogo.obter_jogadas_validas():
                # Faz uma cópia do estado do jogo antes de realizar a jogada
                jogo_copia = copy.deepcopy(jogo)
                jogo_copia.fazer_jogada(jogada)
                eval, _ = self.minimax(jogo_copia, profundidade - 1, False, alfa, beta)
                # Desfaz a jogada após a avaliação
                jogo_copia.tabuleiro[jogada[0]][jogada[1]] = None
                jogo_copia.pecas_disponiveis.append(jogada[2:])
                if eval > max_eval:
                    max_eval = eval
                    melhor_jogada = jogada
                alfa = max(alfa, eval)
                if beta <= alfa:
                    break
            return max_eval, melhor_jogada
        else:
            min_eval = sys.maxsize
            melhor_jogada = None
            for jogada in jogo.obter_jogadas_validas():
                # Faz uma cópia do estado do jogo antes de realizar a jogada
                jogo_copia = copy.deepcopy(jogo)
                jogo_copia.fazer_jogada(jogada)
                eval, _ = self.minimax(jogo_copia, profundidade - 1, True, alfa, beta)
                # Desfaz a jogada após a avaliação
                jogo_copia.tabuleiro[jogada[0]][jogada[1]] = None
                jogo_copia.pecas_disponiveis.append(jogada[2:])
                if eval < min_eval:
                    min_eval = eval
                    melhor_jogada = jogada
                beta = min(beta, eval)
                if beta <= alfa:
                    break
            return min_eval, melhor_jogada

    def escolher_jogada(self, jogo):
        _, melhor_jogada = self.minimax(jogo, self.profundidade, True, -sys.maxsize, sys.maxsize)
        return melhor_jogada


if __name__ == "__main__":
    jogo = JogoQuarto()
    ia = IAQuarto(profundidade=3)
    while True:
        jogo.exibir_tabuleiro()
        jogadas_validas = jogo.obter_jogadas_validas()
        print("Peça disponível:", jogo.pecas_disponiveis[-1])
        print("Jogadas válidas:", jogadas_validas)
        if jogadas_validas:
            if jogo.jogador_atual == 1:
                jogada = None
                while jogada not in jogadas_validas:
                    jogada = input("Digite sua jogada (linha coluna cor altura forma consistencia): ")
                    try:
                        jogada = tuple(map(int, jogada.split()))
                        if len(jogada) != 6:
                            raise ValueError
                    except (ValueError, IndexError):
                        print("Entrada inválida. Por favor, digite apenas os valores separados por espaços.")
                        jogada = None
            else:
                jogada = ia.escolher_jogada(jogo)
            resultado = jogo.fazer_jogada(jogada)
            if resultado is not None:
                if resultado == 0:
                    print("Empate!")
                elif resultado == "IA":
                    print("IA ganhou!")
                else:
                    print("Jogador", resultado, "venceu!")
                break
        else:
            print("Nenhuma jogada válida restante. É um empate!")
            break
