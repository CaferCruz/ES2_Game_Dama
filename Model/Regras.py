from Model.Peca import *
from Model.Jogo import *
import os
import json
from tabuleiro import tabuleiro


class Regras(object):

    # Regra de empate definida pelo grupo. 20 rodadas(1 rodada = 1 jogada preta e 1 jogada branca) sem ninguem comer ninguem
    def empate(self,rodadasSemComer):
        if rodadasSemComer == 20:
            return True
        return False

    # Verifica se alguem venceu. Se preto venceu, retorna 1. Se branco venceu, retorna 0. Se ninguem venceu, retorna -1.
    def vitoria(self, tabuleiro):
        if len(tabuleiro.lista_das_brancas) == 0:
            return 1
        if len(tabuleiro.lista_das_pretas) == 0:
            return 0
        return -1

    # Verifica se a peca que esta sendo movida deve virar dama ou nao.
    def virarDama( peca, altura):
        if peca.tipo == 1:
            return False
        if peca.coordenadas[1] == 0 and peca.cor == 0:
            return True
        if peca.coordenadas[1] == altura and peca.cor == 1:
            return True
        return False

    def mover(self,tabuleiro, cor):
        pertence = False
        if(cor == 0): # Peca branca
            print("informe a jogada:")
            while not pertence:  # Enquanto nao receber input valido

                jogada = raw_input().lower().split()
                if not (len(jogada) == 2):
                    print("Jogada nao e valida, tente novamente:")
                    continue
                origem = (int(jogada[0][1]), ord(jogada[0][0]) - 97)
                peca = Peca(0, origem, 0)
                destino = (int(jogada[1][1]), ord(jogada[1][0]) - 97)

                # A peca movida pertence ao jogador?
                for pecab in tabuleiro.lista_das_brancas:
                    if pecab.coordenadas == peca.coordenadas:
                        pertence = True
                        pecab.coordenadas = destino
                        break

                print("peca: ", peca, " esta dentro de ", tabuleiro.lista_das_brancas)
                print("Voce nao pertence a peca ", origem,
                      ". Por favor, selecione uma das suas pecas.")  # , t.lista_das_brancas

            self.comerPreta(tabuleiro, peca, origem, destino)
            jogada = (peca, destino)
            return jogada
        else:
            print("informe a jogada:")
            while not pertence:  # Enquanto nao receber input valido

                jogada = raw_input().lower().split()
                if not (len(jogada) == 2):
                    print("Jogada nao e valida, tente novamente:")
                    continue
                origem = (int(jogada[0][1]), ord(jogada[0][0]) - 97)
                peca = Peca(1, origem, 0)
                destino = (int(jogada[1][1]), ord(jogada[1][0]) - 97)

                # A peca movida pertence ao jogador?
                for pecab in tabuleiro.lista_das_pretas:
                    if pecab.coordenadas == peca.coordenadas:
                        pertence = True
                        pecab.coordenadas = destino
                        break

                print("peca: ", peca, " esta dentro de ", tabuleiro.lista_das_brancas)
                print("Voce nao pertence a peca ", origem,
                      ". Por favor, selecione uma das suas pecas.")  # , t.lista_das_brancas

            self.comerBranca(tabuleiro, peca, origem, destino)
            jogada = (peca, destino)
            return jogada
        return None

    def comerPreta(self, tabuleiro, peca, origem, destino):
        y = 0
        if(origem[0] < destino[0]):
            for l in range(origem[0] + 1, destino [0] + 1):
                y = y + 1
                coord = (l, origem[1] - y)
                for cod in tabuleiro.lista_das_pretas:
                    if cod.coordenadas == coord:
                        tabuleiro.removePreta(cod)
        else:
            for l in range(origem[0] - 1, destino[0] -1, -1):
                print(origem[0] - 1, destino[0] -1)
                y = y - 1
                coord = (l, origem[1] + y)
                for cod in tabuleiro.lista_das_pretas:
                    if cod.coordenadas == coord:
                        tabuleiro.removePreta(cod)

    def comerBranca(self, tabuleiro, peca, origem, destino):
        y = 0
        print('origem:', origem[0],origem[1])
        if(origem[0] > destino[0]):
            for l in range(origem[0] - 1, destino [0] - 1, -1):
                y = y + 1
                coord = (l, origem[1] + y)
                print(coord)
                for cod in tabuleiro.lista_das_brancas:
                    if cod.coordenadas == coord:
                        tabuleiro.removeBranca(cod)
        else:
            for l in range(origem[0] + 1, destino[0]+1):
                y = y + 1
                coord = (l, origem[1] + y)
                print(coord)
                for cod in tabuleiro.lista_das_brancas:
                    if cod.coordenadas == coord:
                        tabuleiro.removeBranca(cod)


    def novoJogo(self):
        largura = 8
        altura = 8

        tabuleiro = Tabuleiro(largura, altura)
        jogador1 = Jogador(tabuleiro.lista_das_brancas)
        jogador2 = Jogador(tabuleiro.lista_das_pretas)

        return Jogo(jogador1, jogador2, tabuleiro)

    def salvarJogo(self, tabuleiro, nomeSave):
        caminho = "../save/" + nomeSave
        dados_json = {}

        dados_json["altura"] = 8
        dados_json["largura"] = 8
        dados_json["branco_peca"] = []
        dados_json["branco_dama"] = []
        dados_json["preto_peca"] = []
        dados_json["preto_dama"] = []

        for b in tabuleiro.lista_das_brancas:
            if b.tipo :
                dados_json["branco_dama"].append(b.coordenadas)
            else:
                dados_json["branco_peca"].append(b.coordenadas)

        for b in tabuleiro.lista_das_pretas:
            if b.tipo :
                dados_json["preto_dama"].append(b.coordenadas)
            else:
                dados_json["preto_peca"].append(b.coordenadas)

        with open(caminho, 'w') as infile:
            json.dump(dados_json, infile)
        infile.close()

    def carregarJogo(self, nomeSave):
        caminho = "../save/" + nomeSave

        outfile = open(caminho, 'r')
        out = outfile.readline()
        data = json.loads(out)

        tabuleiro = Tabuleiro(data['largura'], data['altura'])
        tabuleiro.esvaziar_lista()
        for b in data['branco_peca']:
            tabuleiro.addPeca(0, b, 0)

        for b in data['branco_dama']:
            tabuleiro.addPeca(0, b, 1)

        for p in data['preto_peca']:
            tabuleiro.addPeca(1, p, 0)

        for p in data['preto_dama']:
            tabuleiro.addPeca(1, p, 1)

        jogador1 = Jogador(tabuleiro.lista_das_brancas)
        jogador2 = Jogador(tabuleiro.lista_das_pretas)

        return Jogo(jogador1, jogador2, tabuleiro)


















