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
                    print(".", end=" ")
                else:
                    print("X" if peca == 1 else "O", end=" ")
            print()
        print()

    def jogador_venceu(self, jogador):
        for posicoes in self.posicoes_vencedoras:
            if all(self.tabuleiro[i][j] == jogador for i, j in posicoes):
                return True
        return False

    def empate(self):
        return all(self.tabuleiro[i][j] is not None for i in range(4) for j in range(4) if self.tabuleiro[i][j] is not None)

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


class IAQuarto:
    def __init__(self, profundidade):
        self.profundidade = profundidade

    def avaliar(self, jogo):
        linhas_jogador1 = sum(
            1 for posicoes in jogo.posicoes_vencedoras if all(jogo.tabuleiro[i][j] == 1 for i, j in posicoes))
        linhas_jogador2 = sum(
            1 for posicoes in jogo.posicoes_vencedoras if all(jogo.tabuleiro[i][j] == 2 for i, j in posicoes))
        return linhas_jogador1 - linhas_jogador2


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
                else:
                    print("Jogador", resultado, "venceu!")
                break
        else:
            print("Nenhuma jogada válida restante. É um empate!")
            break
