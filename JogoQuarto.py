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
        for posicoes in self.posicoes_vencedoras:
            if all(self.tabuleiro[i][j] == jogador for i, j in posicoes):
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

        if self.jogador_venceu(self.jogador_atual):
            return self.jogador_atual
        elif self.empate():
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
        # HEURISTICA
        linhas_jogador1 = sum(
            1 for posicoes in jogo.posicoes_vencedoras if all(jogo.tabuleiro[i][j] == 1 for i, j in posicoes))
        linhas_jogador2 = sum(
            1 for posicoes in jogo.posicoes_vencedoras if all(jogo.tabuleiro[i][j] == 2 for i, j in posicoes))
        return linhas_jogador1 - linhas_jogador2

    def minimax(self, jogo, profundidade, jogador_maximizador, alfa, beta):
        if profundidade == 0 or jogo.jogador_venceu(1) or jogo.jogador_venceu(2) or jogo.empate():
            return self.avaliar(jogo), None

        if jogador_maximizador:
            max_eval = -sys.maxsize
            melhor_jogada = None
            for jogada in jogo.obter_jogadas_validas():
                jogo.fazer_jogada(jogada)
                eval, _ = self.minimax(jogo, profundidade - 1, False, alfa, beta)
                jogo.tabuleiro[jogada[0]][jogada[1]] = None
                jogo.pecas_disponiveis.append(jogada[2:])
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
                jogo.fazer_jogada(jogada)
                eval, _ = self.minimax(jogo, profundidade - 1, True, alfa, beta)
                jogo.tabuleiro[jogada[0]][jogada[1]] = None
                jogo.pecas_disponiveis.append(jogada[2:])
                if eval < min_eval:
                    min_eval = eval
                    melhor_jogada = jogada
                beta = min(beta, eval)
                if beta <= alfa:
                    break
            return min_eval, melhor_jogada

    def escolher_jogada(self, jogo, escolha_peca):
        if escolha_peca not in jogo.pecas_disponiveis:
            raise ValueError("Peça escolhida não está disponível.")
        
        jogadas_validas = jogo.obter_jogadas_validas()
        if not jogadas_validas:
            raise ValueError("Não há jogadas válidas disponíveis.")

        # Adiciona as informações da peça escolhida às jogadas válidas e escolhe aleatoriamente
        jogadas_validas_com_peca = [(i, j, *escolha_peca) for i, j in jogadas_validas]
        return random.choice(jogadas_validas_com_peca)[:4]  # Retorna apenas a jogada escolhida


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
                print("Peças disponíveis para a IA:", jogo.pecas_disponiveis)
                escolha_peca = input("Escolha a peça para a IA jogar (cor altura forma consistencia): ")
                try:
                    escolha_peca = tuple(map(int, escolha_peca.split()))
                    if len(escolha_peca) != 4:
                        raise ValueError
                except (ValueError, IndexError):
                    print("Entrada inválida. Por favor, digite apenas os valores separados por espaços.")
                    continue
                try:
                    jogada = ia.escolher_jogada(jogo, escolha_peca)
                except ValueError as e:
                    print(e)
                    continue
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

