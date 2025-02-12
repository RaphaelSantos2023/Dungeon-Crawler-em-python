import random

class Mapa:
    def __init__(self, linhas, colunas):
        self.linhas = linhas
        self.colunas = colunas
        self.matriz = self.criar_matriz_pontos()
        self.entrada = None
        self.saida = None

    def criar_matriz_pontos(self):
        return [["." for _ in range(self.colunas)] for _ in range(self.linhas)]

    def adicionar_qs_aleatorios(self, quantidade_q):
        coordenadas = []
        for _ in range(quantidade_q):
            while True:
                linha = random.randint(0, self.linhas - 1)
                coluna = random.randint(0, self.colunas - 1)
                if self.matriz[linha][coluna] == ".":
                    self.matriz[linha][coluna] = "Q"
                    coordenadas.append((linha, coluna))
                    break
        return coordenadas

    def adicionar_entrada_saida(self):
        while True:
            entrada_linha = random.randint(0, self.linhas - 1)
            entrada_coluna = random.randint(0, self.colunas - 1)
            if self.matriz[entrada_linha][entrada_coluna] == ".":
                self.matriz[entrada_linha][entrada_coluna] = "E"
                self.entrada = (entrada_linha, entrada_coluna)
                break

        while True:
            saida_linha = random.randint(0, self.linhas - 1)
            saida_coluna = random.randint(0, self.colunas - 1)
            if self.matriz[saida_linha][saida_coluna] == "." and (saida_linha, saida_coluna) != self.entrada:
                self.matriz[saida_linha][saida_coluna] = "S"
                self.saida = (saida_linha, saida_coluna)
                break

    def conectar_qs(self, coordenadas):
        if not coordenadas:
            return
        for i in range(len(coordenadas) - 1):
            x1, y1 = coordenadas[i]
            x2, y2 = coordenadas[i + 1]
            if x1 == x2:
                for j in range(min(y1, y2) + 1, max(y1, y2)):
                    if self.matriz[x1][j] == ".":
                        self.matriz[x1][j] = "+"
            elif y1 == y2:
                for i in range(min(x1, x2) + 1, max(x1, x2)):
                    if self.matriz[i][y1] == ".":
                        self.matriz[i][y1] = "+"
            else:
                for j in range(min(y1, y2) + 1, max(y1, y2)):
                    if self.matriz[x1][j] == ".":
                        self.matriz[x1][j] = "+"
                for i in range(min(x1, x2) + 1, max(x1, x2)):
                    if self.matriz[i][y2] == ".":
                        self.matriz[i][y2] = "+"

    def conectar_entrada_saida(self, coordenadas):
        if not self.entrada or not self.saida or not coordenadas:
            return
        
        # Combinar entrada, coordenadas de Q, e saída em uma sequência única
        caminho = [self.entrada] + coordenadas + [self.saida]
        
        for i in range(len(caminho) - 1):
            x1, y1 = caminho[i]
            x2, y2 = caminho[i + 1]
            
            # Conectar horizontalmente ou verticalmente
            if x1 == x2:  # Mesma linha
                for j in range(min(y1, y2) + 1, max(y1, y2)):
                    if self.matriz[x1][j] == ".":
                        self.matriz[x1][j] = "+"
            elif y1 == y2:  # Mesma coluna
                for i in range(min(x1, x2) + 1, max(x1, x2)):
                    if self.matriz[i][y1] == ".":
                        self.matriz[i][y1] = "+"
            else:  # Diferente linha e coluna
                # Caminho em "L": horizontal primeiro, depois vertical
                for j in range(min(y1, y2) + 1, max(y1, y2)):
                    if self.matriz[x1][j] == ".":
                        self.matriz[x1][j] = "+"
                for i in range(min(x1, x2) + 1, max(x1, x2)):
                    if self.matriz[i][y2] == ".":
                        self.matriz[i][y2] = "+"

    def exibir_matriz(self):
        for linha in self.matriz:
            print(" ".join(linha))

    def exibir_area(self, viewX, viewY):
        centro_x, centro_y = self.entrada
        p_x = max(0, centro_x - viewX // 2)
        p_y = max(0, centro_y - viewY // 2)

        for i in range(p_x, min(p_x + viewX, self.linhas)):
            for j in range(p_y, min(p_y + viewY, self.colunas)):
                print(self.matriz[i][j], end=" ")
            print()

# Uso da classe atualizado
linhas = 50
colunas = 50
mapa = Mapa(linhas, colunas)

def MontarMapa():
    coordenadas_q = mapa.adicionar_qs_aleatorios(10)
    mapa.adicionar_entrada_saida()
    mapa.conectar_qs(coordenadas_q)
    mapa.conectar_entrada_saida(coordenadas_q)
    mapa.exibir_matriz()

    print("\nÁrea visível:")
    mapa.exibir_area(5, 5)

MontarMapa()

print("---------------------------------------------")

MontarMapa()