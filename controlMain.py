import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from functools import partial
import random
import copy

from modal.modalConsumiveis import Pao,Pano,Poscao
from modal.modal_arma import Weapon, Faca, Espada, Machado, Lanca, Cajado, Envenenamento,Queimadura,Sangramento,Sangria,Congelamento,Atordoamento
from modal.modal_equipamento import Coroa_de_Elenna, Capa_verdade, Armadura_Aroth, Amuleto_Lunar, Capuz_cultista, Armadura_malha, Armadura_couro, Armadura_ferro
from modal.modal_magica import Sacrificio_Ithral,Sacrificio_Aroth,Sacrificio_Selena,Sacrificio_Elenna
from modal.modal import Player, Aranha, Goblin, Kobold, Zombi, Zombi_Controlado,Xonnominag,besta_Yithuyesh
from modal.modal_classes import Carreira, Combate, Divindade

from control.control_events_cenario import Bau,Encontro_Fantasma,combate_cenario,Tesouro_suspeito,fenda,Criatura_Escuro
from control.control_events_conclusao import bau_respsota,Evneto_combate_respsota,tesouro_resposta,fenda_repsosta,fantasma_resposta,Dormindo_reposta

class Config:
    frame_jogador = None
    
    frame_iventario = None
    frame_ItemDados = None
    frame_Inimigo = None
    frame_desc= None
    frame_morte = None

    labelAtributo = []

    labelHp = None
    labelMp = None
    labelExp = None
    labelFund = None

    labelHPInimigo = None

    andar = 1

    saida_batalha = None

class ToolTip:
    def __init__(self, widget, text_callback):
        self.widget = widget
        self.text_callback = text_callback
        self.tooltip_window = None
        widget.bind("<Enter>", self.show_tooltip)
        widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        text = self.text_callback()
        if not text:
            return

        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")
        
        label = tk.Label(self.tooltip_window, text=text, fg="white", bg="black",relief="ridge", font=("Arial", 15), highlightbackground="white",borderwidth=1)
        label.pack()

    def hide_tooltip(self, event):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

class Mapa:
    def __init__(self, linhas, colunas):
        self.linhas = linhas
        self.colunas = colunas
        self.matriz = self.criar_matriz_pontos()
        self.entrada = None
        self.saida = None
        self.descer_Saida = True

        self.EmEvento = False
        self.EmCombate = False
        self.CenterSliceX = None
        self.CenterSliceY = None
        self.contador_eventos = 0

        self.Coord_caminho =  []
        
        self.x= None
        self.y = None

        self.coordenadas = []
        self.localAtual = None
        self.begining = True
        self.Combate = True

        self.btn1 = None
        self.btn2 = None

    def criar_matriz_pontos(self):
        return [["." for _ in range(self.colunas)] for _ in range(self.linhas)]

    def turnBeginig(self):
        self.begining = not self.begining

    def adicionar_qs_aleatorios(self, quantidade_q):
        coordenadas = []
        for _ in range(quantidade_q):
            while True:
                linha = random.randint(2, self.linhas - 3)
                coluna = random.randint(2, self.colunas - 3)
                if self.matriz[linha][coluna] == ".":
                    self.matriz[linha][coluna] = "Q"
                    coordenadas.append((linha, coluna))
                    self.coordenadas.append({
                        "linha": linha,
                        "colune": coluna,
                        "Entrada": True
                    })
                    break

        return coordenadas

    def adicionar_entrada_saida(self):
        while True:
            entrada_linha = random.randint(2, self.linhas - 3)
            entrada_coluna = random.randint(2, self.colunas - 3)
            if self.matriz[entrada_linha][entrada_coluna] == ".":
                self.matriz[entrada_linha][entrada_coluna] = "E"
                self.entrada = (entrada_linha, entrada_coluna)
                break

        while True:
            saida_linha = random.randint(2, self.linhas - 3)
            saida_coluna = random.randint(2, self.colunas - 3)
            if self.matriz[saida_linha][saida_coluna] == "." and (saida_linha, saida_coluna) != self.entrada:
                self.matriz[saida_linha][saida_coluna] = "S"
                self.saida = (saida_linha, saida_coluna)
                break

    def conectar_qs(self, coordenadas):
        if not coordenadas:
            return

        # Criar um grafo para conectar os pontos com base na proximidade
        visitados = set()
        fila = [coordenadas[0]]
        visitados.add(coordenadas[0])

        while fila:
            atual = fila.pop(0)
            atual_x, atual_y = atual

            # Encontrar o ponto mais próximo ainda não conectado
            mais_proximo = None
            menor_distancia = float("inf")

            for ponto in coordenadas:
                if ponto not in visitados:
                    ponto_x, ponto_y = ponto
                    distancia = abs(atual_x - ponto_x) + abs(atual_y - ponto_y)
                    if distancia < menor_distancia:
                        menor_distancia = distancia
                        mais_proximo = ponto

            if mais_proximo:
                prox_x, prox_y = mais_proximo
                self.conectar_dois_pontos(atual_x, atual_y, prox_x, prox_y)
                visitados.add(mais_proximo)
                fila.append(mais_proximo)

    def conectar_entrada_saida(self, coordenadas):
        if not self.entrada or not self.saida or not coordenadas:
            return

        # Conectar entrada ao ponto mais próximo
        mais_proximo_entrada = min(
            coordenadas, key=lambda ponto: abs(self.entrada[0] - ponto[0]) + abs(self.entrada[1] - ponto[1])
        )
        self.conectar_dois_pontos(self.entrada[0], self.entrada[1], mais_proximo_entrada[0], mais_proximo_entrada[1])

        # Conectar saída ao ponto mais próximo
        mais_proximo_saida = min(
            coordenadas, key=lambda ponto: abs(self.saida[0] - ponto[0]) + abs(self.saida[1] - ponto[1])
        )
        self.conectar_dois_pontos(self.saida[0], self.saida[1], mais_proximo_saida[0], mais_proximo_saida[1])

        # Conectar os pontos intermediários
        self.conectar_qs(coordenadas)

    def conectar_dois_pontos(self, x1, y1, x2, y2):
        if x1 == x2:  # Mesma linha
            for j in range(min(y1, y2), max(y1, y2) + 1):
                if self.matriz[x1][j] == ".":
                    self.matriz[x1][j] = "+"
        elif y1 == y2:  # Mesma coluna
            for i in range(min(x1, x2), max(x1, x2) + 1):
                if self.matriz[i][y1] == ".":
                    self.matriz[i][y1] = "+"
        else:
            # Conexão em "L", horizontais e verticais
            for j in range(min(y1, y2), max(y1, y2) + 1):
                if self.matriz[x1][j] == ".":
                    self.matriz[x1][j] = "+"
            for i in range(min(x1, x2), max(x1, x2) + 1):
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

    def exibir_area_com_imagens(self, viewX, viewY, imagens):
        frame = tk.Frame()
        
        if self.begining:
            centro_x, centro_y = self.entrada
            self.x, self.y = (centro_x, centro_y)
        else:
            centro_x, centro_y = (self.x, self.y)
            frame_event = self.Eventos(centro_x, centro_y)
            if frame_event is not None:
                self.EmEvento = True
                return frame_event

        p_x = max(0, centro_x - viewX // 2)
        p_y = max(0, centro_y - viewY // 2)

        for i in range(p_x, min(p_x + viewX, self.linhas)):
            for j in range(p_y, min(p_y + viewY, self.colunas)):
                char = self.matriz[i][j]
                if char == "E":
                    img = self.redimensionar_imagem(imagens["entrada"])
                elif char == "S":
                    img = self.redimensionar_imagem(imagens["saida"])
                elif char == "Q":
                    img = self.redimensionar_imagem(imagens["q"])
                elif char == "+":
                    img = self.redimensionar_imagem(imagens["caminho"])
                else:
                    img = self.redimensionar_imagem(imagens["vazio"])

                label = tk.Label(frame, image=img)
                label.image = img
                label.grid(row=i - p_x, column=j - p_y, padx=0, pady=0)

        return frame
    
    def sortear_eventos_especiais(self):
        self.eventos_especiais = set(random.sample(range(self.contador_eventos, self.contador_eventos + 10), 2))

    def Eventos(self, x, y):
        frame = None

        if self.matriz[x][y] != "S" and self.matriz[x][y] != "Q":
            self.contador_eventos += 1
            if self.verificar_caminho(x,y) == False and self.Combate and self.contador_eventos % 3 == 0:

                self.sortear_eventos_especiais()

                self.Combate = True
                self.EmEvento = True
                self.localAtual = {"x": x, "y": y}
                frame = self.Criar_Evento("Quarto")

        elif self.matriz[x][y] == "S" and self.descer_Saida:
            self.EmEvento = True
            frame = self.Criar_Evento("saída")
        else:
            validade = self.verificar_coordenada(x, y)
            if self.matriz[x][y] == "Q" and validade:
                self.EmEvento = True
                self.localAtual = {"x": x, "y": y}

                label = "No meio das ruinas do comodo,\nvocê encontra um baú\nDeseja abrir?"
                btn1 = "Abrir o Baú"
                btn2 = "<Pode ser um Mimico>"

                tipo = 0
                frame = tk.Frame(bg="black", relief="ridge", highlightbackground="white", highlightthickness=4)
                self.Criar_Tela(frame, btn1, btn2, "img/eventos/inicio/Bau.png",label, tipo)

        return frame
    
    def verificar_coordenada(self, linha, coluna):

        for coord in self.coordenadas:
            if coord["linha"] == linha and coord["colune"] == coluna and coord.get("Entrada", False):
                coord["Entrada"] = False
                return True
        return False
    
    def verificar_caminho(self,linha,coluna):
        for coord in self.Coord_caminho:
            if coord["linha"] == linha and coord["coluna"] == coluna:
                print("\n\nTruee\n\n")
                return True
        print("\n\nFALSO\n\n")
        self.Coord_caminho.append({"linha": linha, "coluna": coluna})
        return False

    def colocar_Jogador(self, frame, jogador,x,y):
        
        # Redimensionar a imagem do jogador
        caminho = jogador.simbolo["simbolo"]
        img = self.redimensionar_imagem(caminho)
        
        label = tk.Label(frame, image=img)
        label.image = img
        label.grid(row= x, column= y, padx=0, pady=0)
        return frame

    def redimensionar_imagem(self, caminho):
        imagem = Image.open(caminho)
        imagem = imagem.resize((100, 100), Image.LANCZOS)
        return ImageTk.PhotoImage(imagem)
    
    def Criar_Evento(self,evento):
        frame = tk.Frame(bg="black", relief="ridge", highlightbackground="white", highlightthickness=4,width=400,height=150)
        
        if evento == "saída":
            img = "img/eventos/Inicio/Saida_evento.png"
            txt = "Uma escadaria espiralaza desce a penumbra.\nCheios putridos emergem da passagem,\narrebatando os sentidos\nDeseja descee?"
            btn1T = "Sim"
            btn2T = "Não"
            tipo= "Saida"

        if evento == "Quarto":       
            img,txt,btn1T,btn2T,tipo = self.selecionar_evento()
        
        return self.Criar_Tela(frame,btn1T,btn2T,img,txt,tipo)

    def Criar_Tela(self,frame,btn1T,btn2T,img,txt,tipo):
        frame_geral = tk.Frame(frame,bg="black")
        frame_geral.pack()

        imgM = redimensionarImagem(img, 400, 300)

        frame_img = tk.Frame(frame_geral,bg="black")
        frame_img.grid(row=1, column=1, padx=2, pady=2)

        ImagemEvento = tk.Label(frame_img, image=imgM, bg="black")
        ImagemEvento.image = imgM
        ImagemEvento.pack()

        frame_lbl = tk.Frame(frame_geral,bg="black")
        frame_lbl.grid(row=1, column=2, padx=2, pady=2)

        label = tk.Label(frame_lbl, text=txt,bg="black",fg="white", highlightthickness=4, highlightbackground="black",padx=50, pady=25,font=("Arial", 15))
        label.pack()

        frame_btn = tk.Frame(frame_lbl,bg="black")
        frame_btn.pack()
        
        self.btn1 = tk.Button(frame_btn,text=btn1T,bg="black",fg="white",borderwidth=3, relief="sunken",padx=50, pady=25,command=partial(self.Metodo_resposta,tipo,frame,label,1),width=10)
        self.btn1.grid(row=0, column=0, padx=5, pady=5)
        
        self.btn2 = tk.Button(frame_btn,text=btn2T,bg="black",fg="white",borderwidth=3, relief="sunken",padx=50, pady=25,command=partial(self.Metodo_resposta,tipo,frame,label,2),width=10)
        self.btn2.grid(row=0, column=2, padx=5, pady=5)

        return frame
    
    def selecionar_evento(self):
        peso = [1,1,3,2,2,2]

        eventos = [Bau,Encontro_Fantasma, combate_cenario,Tesouro_suspeito,fenda,Criatura_Escuro]

        eventos_escolhido = random.choices(eventos, weights=peso, k=1)[0]

        img,label,btn1,btn2,evento = eventos_escolhido()

        return img,label,btn1,btn2,evento
    
    def Metodo_resposta(self,tipo,frame,label,btn):

        if tipo == "Saida":
            if btn == 1:
                txt = "Você desce a escadaria"
                btn1T = ">"
                btn2T = ""
                label.config(text=txt)
                self.btn1.config(text=btn1T,command=partial(refazer_mapa,frame))
                self.btn2.config(text=btn2T)
            else:
                txt = "Você dá meia volta"
                btn1T = ">"
                btn2T = ""
                label.config(text=txt)
                self.btn1.config(text=btn1T,command=partial(self.destruir_Tela_evento,frame))
                self.btn2.config(text=btn2T)
                self.descer_Saida = False
        else:

            teste = random.randrange(1,13)
            txt = ""

            btn1T = ">"
            self.btn1.config(text=btn1T,command=partial(self.destruir_Tela_evento,frame))
            self.btn2.grid_forget() 

            if tipo == 0:
                bau_respsota(btn,self.btn1,self.btn2,label,txt,teste,jogador,btn1T,get_money,get_Consumivel,frame,self.destruir_Tela_evento)

            elif tipo == 1:
                self.EmCombate = fantasma_resposta(btn,jogador,teste,txt,label)
            elif tipo == 2:
                self.EmCombate = Evneto_combate_respsota(btn, self.btn1, txt, teste, jogador, btn1T, Criar_Tela_Combat, get_Inimigo, frame, label)
            
            elif tipo == 3:
                tesouro_resposta(btn, self.btn1, txt, teste, jogador, btn1T, Criar_Tela_Combat, get_money, frame, label)
            
            elif tipo == 4:
                fenda_repsosta(btn,self.btn1,self.btn2,txt,teste,jogador,btn1T,label,get_money,get_Consumivel,frame,self.destruir_Tela_evento)
            
            elif tipo ==5:
                Dormindo_reposta(btn,self.btn1,txt,teste,jogador,btn1T,label,get_Inimigo,Criar_Tela_Combat,frame,self.destruir_Tela_evento,get_money,get_Consumivel)
            
    
    def destruir_Tela_evento(self, frame):
        frame.destroy()

        self.EmEvento = False

        atualizar_Mapa()

        Atualizar_Dados()

    def copiar(self):
        mapa_copiado = copy.deepcopy(self)
        return mapa_copiado

def on_key_press(event):
    global estadoSaida, jogador

    if mapa_copiado.begining:
        mapa_copiado.turnBeginig()

    if mapa_copiado.EmEvento is False:
        key = event.keysym
        if key == "Up":
            movimentar("Cima")
        elif key == "Down":
            movimentar("Baixo")
        elif key == "Left":
            movimentar("Esquerda")
        elif key == "Right":
            movimentar("Direita")
        mapa_copiado.descer_Saida = True

        atualizar_Mapa()

def refazer_mapa(frame):
    frame.destroy()
    global mapa_copiado, frame_imagens, jogador

    Config.andar += 1

    fator_crescimento = 2
    largura = 20 + Config.andar * fator_crescimento
    altura = 20 + Config.andar * fator_crescimento

    mapa_copiado = Mapa(largura, altura)
    coordenadas_q = mapa_copiado.adicionar_qs_aleatorios(10)
    mapa_copiado.adicionar_entrada_saida()
    mapa_copiado.conectar_qs(coordenadas_q)
    mapa_copiado.conectar_entrada_saida(coordenadas_q)

    atualizar_Mapa()

def movimentar(comando):
    if comando == "Cima" and mapa_copiado.x - 1 >= 0 and mapa_copiado.matriz[mapa_copiado.x - 1][mapa_copiado.y] in ["+", "E", "S", "Q"]:
        mapa_copiado.x -= 1
    elif comando == "Baixo" and mapa_copiado.x + 1 < mapa_copiado.linhas and mapa_copiado.matriz[mapa_copiado.x + 1][mapa_copiado.y] in ["+", "E", "S", "Q"]:
        mapa_copiado.x += 1
    elif comando == "Esquerda" and mapa_copiado.y - 1 >= 0 and mapa_copiado.matriz[mapa_copiado.x][mapa_copiado.y - 1] in ["+", "E", "S", "Q"]:
        mapa_copiado.y -= 1
    elif comando == "Direita" and mapa_copiado.y + 1 < mapa_copiado.colunas and mapa_copiado.matriz[mapa_copiado.x][mapa_copiado.y + 1] in ["+", "E", "S", "Q"]:
        mapa_copiado.y += 1

def atualizar_Mapa():
    global frame_imagens

    if frame_imagens:
        frame_imagens.destroy()
        frame_imagens = None

    frame_imagens = mapa_copiado.exibir_area_com_imagens(viewX, viewY, imagens)

    if mapa_copiado.EmEvento != True:
        frame_imagens = mapa_copiado.colocar_Jogador(
            frame_imagens,
            jogador,
            mapa_copiado.x - max(0, mapa_copiado.x - viewX // 2),
            mapa_copiado.y - max(0, mapa_copiado.y - viewY // 2),
        )
    
    frame_imagens.place(relx=0.35, rely=0.45, anchor="center")

def redimensionarImagem(caminho,x,y):
    imagem = Image.open(caminho)
    imagem = imagem.resize((x,y), Image.LANCZOS)
    return ImageTk.PhotoImage(imagem)

def Criar_Tela_Combat(inimigo, root):
    root.destroy()
    Turno = True

    Config.frame_desc = tk.Frame(bg="black", relief="ridge", highlightbackground="white", highlightthickness=4)
    Config.frame_desc.place(relx=0.35, rely=0.45, anchor="center")

    Dados_Inimigo(inimigo)

    frame_inimigo  = tk.Frame(Config.frame_desc,bg="black")
    frame_inimigo.pack()

    frame_visual  = tk.Frame(frame_inimigo,bg="black")
    frame_visual.grid(row=1, column=2, padx=2, pady=2)

    frame_desc  = tk.Frame(frame_visual,bg="black")
    frame_desc.grid(row=1, column=2, padx=2, pady=2)

    scrollbar = tk.Scrollbar(frame_desc)
    scrollbar.pack(side="right", fill="y")

    LabelDescri = tk.Text(frame_desc, bg="black", fg="white", font=("Arial", 12), wrap="word", height=10, width=30)
    LabelDescri.pack(side="left", fill="both", expand=True)

    LabelDescri.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=LabelDescri.yview)

    LabelDescri.insert("end", "A batalha começou!")
    LabelDescri.config(state="disabled")

    Frame_inimigo = tk.Frame(frame_inimigo,bg="black", relief="ridge", highlightbackground="white", highlightthickness=4)
    Frame_inimigo.grid(row=1, column=1, padx=2, pady=2)

    img = redimensionarImagem(inimigo.simbolo["simbolo"],444, 391)

    LabelInimigo = tk.Label(Frame_inimigo, image=img, bg="black")
    LabelInimigo.image = img
    LabelInimigo.grid(row=1, column=0, padx=2, pady=2)

    frame_btn  = tk.Frame(Config.frame_desc,bg="black")
    frame_btn.pack()

    LabelAcao = tk.Label(frame_btn, text="Ataques: ", bg="black", fg="white", font=("Arial", 12))
    LabelAcao.grid(row=1, column=0, padx=3, pady=3)

    btnAtck = tk.Button(frame_btn, text="Atck", bg="black", fg="white", font=("Arial", 12), 
                        command=partial(Descisao, jogador, inimigo, "Ataque", LabelDescri, Turno),width=15)
    btnAtck.grid(row=1, column=1, padx=3, pady=3)

    btnDef = tk.Button(frame_btn, text="Def", bg="black", fg="white", font=("Arial", 12), 
                        command=partial(Descisao, jogador, inimigo, "Defender", LabelDescri, Turno),width=15)
    btnDef.grid(row=1, column=2, padx=3, pady=3)

    btnRun = tk.Button(frame_btn, text="Run", bg="black", fg="white", font=("Arial", 12), 
                       command=partial(Descisao, jogador, inimigo, "Fugir", LabelDescri, Turno),width=15)
    btnRun.grid(row=1, column=3, padx=3, pady=3)

    LabelTalk = tk.Label(frame_btn, text="Chat: ", bg="black", fg="white", font=("Arial", 12))
    LabelTalk.grid(row=2, column=0, padx=3, pady=3)

    btnConv = tk.Button(frame_btn, text="Convencer", bg="black", fg="white", font=("Arial", 12), 
                        command=partial(Descisao, jogador, inimigo, "Convencer", LabelDescri, Turno),width=15)
    btnConv.grid(row=2, column=1, padx=3, pady=3)

    btnAmea= tk.Button(frame_btn, text="Intimidar", bg="black", fg="white", font=("Arial", 12), 
                       command=partial(Descisao, jogador, inimigo, "Ameaça", LabelDescri, Turno),width=15)
    btnAmea.grid(row=2, column=2, padx=3, pady=3)

    LabelMag = tk.Label(frame_btn, text="Magias: ", bg="black", fg="white", font=("Arial", 12))
    LabelMag.grid(row=3, column=0, padx=3, pady=3)
    
    for i in range(len(jogador.Bencaos)):
        if (jogador.Bencaos[i].tipo =="Temporaria" ):
            btnConv = tk.Button(frame_btn, text=jogador.Bencaos[i].nome, bg="black", fg="white", font=("Arial", 12), 
                            command=partial(Conjurar_magia_Temporaria, jogador,jogador.Bencaos[i], LabelDescri),width=15)
            btnConv.grid(row=3+i, column=1, padx=3, pady=3)

def Conjurar_magia_Temporaria(personagem, magia,LabelDescri):
    LabelDescri.config(state="normal")

    txt= "\n"
    txt += personagem.conjurarMagia(magia)
    
    LabelDescri.insert("end", txt + "\n")
    Atualizar_Dados()
    
def Descisao(personagem, adversario, tipo, LabelDescri, Turno):
    LabelDescri.config(state="normal")

    txt = Acao(personagem, adversario, tipo)
    LabelDescri.insert("end", txt + "\n")

    if adversario.hp > 0:
        txt = Acao(adversario, personagem, "Ataque")
        LabelDescri.insert("end", txt + "\n")
        Config.labelHPInimigo.config(text="HP: "+ str(adversario.hp))

    LabelDescri.see("end")
    LabelDescri.config(state="disabled")

    State = definir_vitoria(personagem, adversario)
    
    Atualizar_Dados()

    if State is not None:
        Turno = False
        Tela_vitoria(State, personagem, adversario)

def Acao(personagem, adiversario, tipo):

    if tipo == "Ataque":
        txt = personagem.attack(adiversario)
    elif tipo == "Fugir":
        
        acerto = personagem.Fugir(adiversario)
        if acerto:
            txt = f"\n- {personagem.nome} fugiu com sucesso."
            adiversario.hp = 0
            Config.saida_batalha = "Fuga"
        else:
            txt = f"\n- {personagem.nome} falhou ao fugir."
    
    elif tipo == "Defender":
        txt = personagem.defender()
    else:
        txt= f"\n- {personagem.nome} falhou"
        dice = random.randrange(1, 11)
        diceEn = random.randrange(1, 11)
        if tipo == "Ameaça":
            if personagem.str + dice > adiversario.str +diceEn:
                adiversario.hp = 0
                Config.saida_batalha = "Conversa"
                txt = f"\n- {personagem.nome} conseguiu intimidar {adiversario.nome}"
        elif tipo == "Convencer":
            if personagem.cha + dice > adiversario.cha +diceEn:
                adiversario.hp = 0
                Config.saida_batalha = "Conversa"
                txt = f"\n- {personagem.nome} conseguiu convencer\n{adiversario.nome} a parar"
    
    if adiversario.estado:
        txt += adiversario.sofrer_Efeito(personagem)

    return txt

def definir_vitoria(personagem, adversario):

    if personagem.hp <=0 or personagem.mp <= 0:
        Config.saida_batalha = None
        return False
    
    if adversario.hp <=0 :
        return True
    return None

def Dados_Inimigo(inimigo):
    if Config.frame_Inimigo  is not None:
        Config.frame_Inimigo.destroy()
        Config.frame_Inimigo = None

    Config.frame_Inimigo = tk.Frame(Config.frame_desc,bg="black")
    Config.frame_Inimigo.pack()

    Config.labelHPInimigo = tk.Label(Config.frame_Inimigo, text="HP:"+str(inimigo.hp),bg="black",fg="white",font=("Arial", 18))
    Config.labelHPInimigo.grid(row=0, column=2, padx=6, pady=6)

    labelNome = tk.Label(Config.frame_Inimigo,text=inimigo.nome,bg="black",fg="white",font=("Arial", 18))
    labelNome.grid(row=0, column=0, padx=6, pady=6)

def Tela_vitoria(caso, personagem, adversario):
    
    Config.frame_desc.destroy()
    Config.frame_Inimigo.destroy()

    frame = tk.Frame(root,bg="black", relief="ridge", highlightbackground="white", highlightthickness=4, width=100, height= 100)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    btn1T = ">"

    mapa_copiado.EmEvento == True
    if Config.saida_batalha is None:
        if caso:
            fund = random.randint(1, adversario.fund)+1
            item = get_Consumivel()
            txt = f"Você venceu!\nVocê conseguiu {adversario.exp} exp\n{fund} funds\n {item.nome}"
            
            if jogador.magiaAtiva:
                for metodo in jogador.magiaAtiva:
                    metodo.concequencia_efeito(jogador)
                    txt += f'\nHaverá consequencias para seus atos'

            personagem.exp += adversario.exp
            personagem.fund += fund
            personagem.AddInventario(item)
            
        else:
            Config.frame_jogador.destroy()
            frame.destroy()
            return
    else:
        txt = "Você saiu da batalha"
        Config.saida_batalha = None
       
    label = tk.Label(frame, text=txt, bg="black", fg="white", highlightthickness=4, highlightbackground="black", font=("Arial", 12),width=100)
    label.grid(row=1, column=1, padx=6, pady=6)

    btn1 = tk.Button(frame, text=btn1T, bg="black", fg="white", borderwidth=3, relief="sunken", padx=25, pady=12,
                     command=partial(Reinicio, caso,frame))
    btn1.grid(row=3, column=1, padx=5, pady=5)
    
def Reinicio(caso,frame):
    global mapa_copiado
    
    if frame is not None:
        frame.destroy()
        frame = None
    
    if caso == False:
        Config.frame_jogador = None
        reiniciar_jogo()
    else:
        mapa_copiado.EmEvento = False
        atualizar_Mapa()

def reiniciar_jogo():
    global mapa_copiado, jogador, frame_imagens
    
    mapa_copiado = Mapa(20, 20)  
    coordenadas_q = mapa_copiado.adicionar_qs_aleatorios(10)  
    mapa_copiado.adicionar_entrada_saida()
    mapa_copiado.conectar_qs(coordenadas_q)
    mapa_copiado.conectar_entrada_saida(coordenadas_q)

    jogador = Player() 
    jogador.exp = 0
    jogador.fund = 0

    frame_classes()

    frame_imagens = mapa_copiado.exibir_area_com_imagens(viewX, viewY, imagens)

def iventario_Frame(root):
    if Config.frame_iventario is None:

        Config.frame_iventario = tk.Frame(root, bg="black", relief="ridge", 
                                          highlightbackground="white", highlightthickness=4, 
                                          width=200, height=80)
        Config.frame_iventario.place(relx=0.5, rely=0.8, anchor="center")

        frame_Intermedio = tk.Frame(Config.frame_iventario, bg="black")
        frame_Intermedio.grid(row=0,column=0)

        canvas = tk.Canvas(frame_Intermedio, bg="black",width=300,height=150)

        scrollbar = tk.Scrollbar(frame_Intermedio, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="black")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        iventario = jogador.getInventario()
        for i in range(len(iventario)):
            btn = tk.Button(scrollable_frame, text=iventario[i].nome, bg="black", fg="white", font=("Arial", 12),
                            command=partial(Dados_item, iventario[i], Config.frame_iventario, i, root),width=15)
            btn.pack(padx=1, pady=1, anchor="w")
    else:
        Config.frame_iventario.destroy()
        Config.frame_iventario = None

def Dados_item(item, frame, i, root):
    if Config.frame_ItemDados is None:
        Config.frame_ItemDados = tk.Frame(frame, bg="black")
        Config.frame_ItemDados.grid(row=0,column=1)
        LabelNome = tk.Label(Config.frame_ItemDados, text=item.nome, bg="black", fg="white", font=("Arial", 12))
        LabelNome.pack(padx=6, pady=6)

        # Descrição do item
        LabelDescri = tk.Label(Config.frame_ItemDados, text=item.descricao, bg="black", fg="white", font=("Arial", 10))
        LabelDescri.pack(padx=6, pady=6)

        # Botão de uso
        btn = tk.Button(Config.frame_ItemDados, text="Usar", bg="black", fg="white", font=("Arial", 12), 
                        command=partial(Uso_do_item, item, item.tipo, i, root))
        btn.pack(padx=6, pady=6)
    else:
        Config.frame_ItemDados.destroy()
        Config.frame_ItemDados = None
        Dados_item(item, frame, i, root)

def Uso_do_item(item,tipo,i,root):

    Config.frame_ItemDados.destroy()
    Config.frame_ItemDados = None

    jogador.Usar(item,tipo,i)

    if tipo == "Armadura":
        atualizarAtributo()
    
    Config.frame_iventario.destroy()
    Config.frame_iventario = None

    Atualizar_Dados()
    iventario_Frame(root)

def Status(root):

    notebook = ttk.Notebook(root)

    def status_magia(notebook):

        def mudar_texto(frame, label,magia):

            def btn_clicado(magia):
                jogador.conjurarMagia(magia)
                Atualizar_Dados()

            label.config(text= magia.descricao)
            if magia.tipo != "Temporaria":
                btn = tk.Button(frame, text=magias.nome, bg="black", fg="white", font=("Arial", 12),
                                    command=partial(btn_clicado,magia),width=15)
                btn.grid(row=1, column=1, padx=6, pady=6)

        frame = ttk.Frame(notebook, relief="ridge", style="Custom.TFrame")

        frame_magias =tk.Frame(frame,bg="black",relief="ridge")
        frame_magias.pack()

        frame_descricao =tk.Frame(frame,bg="black")
        frame_descricao.pack()

        label = tk.Label(frame_descricao, text="",bg="black",fg="white",font=("Arial", 15))
        label.grid(row =0, column =1, padx=6, pady=6)

        i = 0
        for magias in jogador.Bencaos:
            btn = tk.Button(frame_magias, text=magias.nome, bg="black", fg="white", font=("Arial", 12),
                                    command=partial(mudar_texto,frame_descricao,label,magias),width=15)
            btn.pack()
            i+=1
        return frame

    def status_geral(notebook):

        frame = ttk.Frame(notebook, relief="ridge", style="Custom.TFrame")
        frame_img = tk.Frame(frame,bg="black")
        frame_img.pack()

        img = redimensionarImagem(jogador.simbolo["status"],302, 391)

        labelStatus = tk.Label(frame_img, image=img,bg="black")
        labelStatus.image = img
        labelStatus.grid(row=1, column=1, padx=6, pady=6)

        ToolTip(labelStatus, jogador.get_estado)

        frame_HP = tk.Frame(frame,bg="black",relief="ridge", highlightbackground="white",highlightthickness=4)
        frame_HP.pack()

        Config.labelHp = tk.Label(frame_HP, text=("HP: "+str(jogador.hp)),bg="black",fg="white",font=("Arial", 15))
        Config.labelHp.grid(row=0, column=1, padx=6, pady=6)

        Config.labelMp = tk.Label(frame_HP, text=("MP: "+str(jogador.mp)),bg="black",fg="white",font=("Arial", 15))
        Config.labelMp.grid(row=0, column=3, padx=6, pady=6)

        Config.labelFund = tk.Label(frame_HP, text=("Fund: "+str(jogador.fund)),bg="black",fg="white",font=("Arial", 12))
        Config.labelFund.grid(row=0, column=2, padx=6, pady=6)

        frame_dados = tk.Frame(frame,bg="black",relief="ridge", highlightbackground="white",highlightthickness=4)
        frame_dados.pack()

        labelLV = tk.Label(frame_dados, text=("LV:"+str(jogador.level)),bg="black",fg="white",font=("Arial", 12))
        labelLV.grid(row=0, column=0, padx=6, pady=6)

        Config.labelExp = tk.Label(frame_dados, text=("exp: "+str(jogador.exp)),bg="black",fg="white",font=("Arial", 12))
        Config.labelExp.grid(row=0, column=1, padx=6, pady=6)

        btn = tk.Button(frame_dados, text="Level up", bg="black", fg="white", font=("Arial", 12),
                                command=partial(Tela_de_atributos),width=15)
        btn.grid(row=0, column=3, padx=6, pady=6)
        
        frame_Invent = tk.Frame(frame,bg="black")
        frame_Invent.pack()

        btn = tk.Button(frame_Invent, text= "Inventario",bg="black",fg="white",font=("Arial", 14),command=partial(iventario_Frame,root))
        btn.grid(row=0,column=1,padx=6,pady=6)

        ToolTip(labelStatus, jogador.get_estado)
        dados_atributos(frame_dados)

        return frame
    
    style = ttk.Style()
    style.configure("Custom.TFrame", background="black")

    frame_magia = status_magia(notebook)
    frame_geral = status_geral(notebook)

    notebook.add(frame_geral, text="Status")
    notebook.add(frame_magia, text="Magias")

    return notebook

def dados_atributos(frame):
    atributos = {
        "STR": jogador.str,
        "DEX": jogador.dex,
        "INT": jogador.inte,
        "LCK": jogador.lck,
        "WIS": jogador.wis,
        "CHA": jogador.cha,
    }

    for i, (nome, valor) in enumerate(atributos.items()):
        row = (i // 3) + 1 
        col = i % 3 
        label = tk.Label(
            frame,
            text=(nome + ":" + str(valor)),
            bg="black",
            fg="white",
            font=("Arial", 12),
        )
        label.grid(row=row, column=col, padx=6, pady=6)
        Config.labelAtributo.append(label)

def atualizarAtributo():
    atributos = {
        "STR": jogador.str,
        "DEX": jogador.dex,
        "INT": jogador.inte,
        "LCK": jogador.lck,
        "WIS": jogador.wis,
        "CHA": jogador.cha,
    }

    for i, (nome, valor) in enumerate(atributos.items()):
        Config.labelAtributo[i].config(text=(nome + ":" + str(valor)))

def Subitrair_Aumentar_Atributo(atributos, nome, pontos, label, labelPontos, varSelecionada):
    atributo = varSelecionada.get()

    if atributo:
        if atributo in ["HP", "MP"]:
            incremento = 2
        else:
            incremento = 1

        if pontos["valor"] > 0 and (atributo in ["HP", "MP"] or atributos[atributo] < 9):
            pontos["valor"] -= 1
            atributos[atributo] += incremento

        labelPontos.config(text=("Pontos restantes: " + str(pontos["valor"])))
        label[atributo].config(text=str(atributos[atributo]))

def Criar_Lable_radio(frame, nome, atributos, row, varSelecionada, label):
    labelT = tk.Label(frame, text=nome, bg="black", fg="white", font=("Arial", 12))
    labelT.grid(row=row, column=0, padx=6, pady=6)

    radioBtn = tk.Radiobutton(frame, text="", variable=varSelecionada, value=nome, bg="black", fg="white")
    radioBtn.grid(row=row, column=1, padx=6, pady=6)

    labelValor = tk.Label(frame, text=str(atributos[nome]), bg="black", fg="white", font=("Arial", 12))
    labelValor.grid(row=row, column=2, padx=6, pady=6)
    
    label[nome] = labelValor 

def Tela_de_atributos():
    pontos = jogador.AumentarLevel()

    if pontos is not None:
        frame = tk.Frame(root, bg="black", relief="ridge", highlightbackground="white", highlightthickness=4)

        pontos = {"valor": pontos}

        atributos = {
            "HP": jogador.hpMax,
            "MP": jogador.mpMax,
            "STR": jogador.str,
            "DEX": jogador.dex,
            "INT": jogador.inte,
            "LCK": jogador.lck,
            "WIS": jogador.wis,
            "CHA": jogador.cha,
        }

        def Destruir_atualizar(atributos):
            jogador.str = atributos["STR"]
            jogador.dex = atributos["DEX"]
            jogador.inte = atributos["INT"]
            jogador.lck = atributos["LCK"]
            jogador.wis = atributos["WIS"]
            jogador.cha = atributos["CHA"]
            jogador.hp = atributos["HP"]
            jogador.mp = atributos["MP"]
            jogador.hpMax = atributos["HP"]
            jogador.mpMax = atributos["MP"]

            Config.frame_jogador.destroy()

            Destrui_frame(frame)


        labelTitulo = tk.Label(frame, text="Atributos", bg="black", fg="white", font=("Arial", 15))
        labelTitulo.grid(row=0, column=0, padx=6, pady=6)

        labelPontos = tk.Label(frame, text="Pontos restantes: " + str(pontos["valor"]), bg="black", fg="white", font=("Arial", 12))
        labelPontos.grid(row=1, column=0, padx=6, pady=6)

        varSelecionada = tk.StringVar()
        varSelecionada.set("STR")  # Define um atributo padrão para evitar que fique vazio

        label_dict = {}

        row = 2
        for nome in atributos.keys():
            Criar_Lable_radio(frame, nome, atributos, row, varSelecionada, label_dict)
            row += 1

        btnAumentar = tk.Button(
            frame, text="Aumentar", bg="black", fg="white", font=("Arial", 12),
            command=partial(Subitrair_Aumentar_Atributo, atributos, nome, pontos, label_dict, labelPontos, varSelecionada)
        )
        btnAumentar.grid(row=row, column=1, padx=6, pady=6)

        btnProx = tk.Button(
            frame, text=">", bg="black", fg="white", font=("Arial", 12),
            command=partial(Destruir_atualizar, atributos)
        )
        btnProx.grid(row=row, column=3, padx=6, pady=6)

        frame.place(relx=0.5, rely=0.5, anchor="center")

def Atualizar_Dados():

    if jogador.hp <= 0 or jogador.mp <= 0:
        mapa_copiado.EmEvento = True
        tela_morte()
    else:
        Config.labelHp.config(text="HP: "+str(jogador.hp))
        Config.labelMp.config(text="MP: "+str(jogador.mp))
        Config.labelFund.config(text="Fund: "+str(jogador.fund))
        Config.labelExp.config(text="exp: "+ str(jogador.exp))

def get_Armamento():
    itens = [Faca(),Espada(),Machado()]
    peso = [4,2,2]
    item = random.choices(itens,weights=peso,k=1)[0]
    return item

def tela_morte():

    global frame_imagens

    if Config.frame_jogador != None:
        Config.frame_jogador.destroy()
    
    if frame_imagens != None:
        frame_imagens.destroy()
    
    Config.frame_morte = tk.Frame(bg="black", relief="ridge", highlightbackground="white", highlightthickness=2)
    Config.frame_morte.place(relx=0.5, rely=0.5, anchor="center")

    label = tk.Label(Config.frame_morte,text="Você morreu",bg="black", fg="white", font=("Arial", 30))
    label.grid(row=1, column=0, padx=50, pady=50)

    btn = tk.Button(Config.frame_morte, text=">", bg="black", fg="white", command=partial(Reinicio,False,Config.frame_morte), font=("Arial", 20))
    btn.grid(row=2, column=0, padx=12, pady=12)
    

def get_Inimigo():
    inimigos_disponiveis = [
        (Goblin(), 1, 3, 3),   # Aparece do andar 1 ao 3 (peso 3)
        (Kobold(), 2, 5, 2),   # Aparece do andar 2 ao 5 (peso 2)
        (Aranha(), 1, 7, 3),   # Aparece do andar 3 ao 7 (peso 2)
        (Zombi(), 2, 10, 2),   # Aparece do andar 4 ao 10 (peso 2)
        (Xonnominag(), 4, 12, 2),
        (besta_Yithuyesh(),5,14,2),
        (Zombi_Controlado(),4,20,3)
    ]

    # Filtra os inimigos que podem aparecer no andar atual
    inimigos_filtrados = [(inimigo, peso) for inimigo, min_andar, max_andar, peso in inimigos_disponiveis
                          if min_andar <= Config.andar <= max_andar]

    if not inimigos_filtrados:
        return None  # Retorna None se não houver inimigos disponíveis
    
    itens, pesos = zip(*inimigos_filtrados)

    # Escolhe um inimigo aleatoriamente com base no peso
    return random.choices(itens, weights=pesos, k=1)[0]

def get_money():
    dinheiro = random.randint(1,5)
    return dinheiro

def get_Consumivel():
    itens = [Pao(),Pano(),Poscao()]
    peso = [4,2,2]
    item = random.choices(itens,weights=peso,k=1)[0] 
    return item

def get_Runa():
    itens = [Envenenamento, Queimadura, Sangramento, Sangria, Congelamento, Atordoamento]
    item = random.choices(itens,k=1)[0] 
    return item

def get_Equipamento():
    itens = [Coroa_de_Elenna(), Capa_verdade(), Armadura_Aroth(), Amuleto_Lunar(), Capuz_cultista(), Armadura_malha(), Armadura_couro(), Armadura_ferro()]
    peso = [4,2,4,4,2,2,2,2]
    item = random.choices(itens,weights=peso,k=1)[0] 
    return item

def colocar_atributos(classes_selecionadas, frame):

    def setAtributos(tipo):
        jogador.str += classes_selecionadas[tipo].str
        jogador.dex += classes_selecionadas[tipo].dex
        jogador.inte += classes_selecionadas[tipo].int
        jogador.lck += classes_selecionadas[tipo].lck
        jogador.wis += classes_selecionadas[tipo].wis
        jogador.cha += classes_selecionadas[tipo].cha
        jogador.fund += classes_selecionadas[tipo].fund
        jogador.hpMax += classes_selecionadas[tipo].hp
        jogador.mpMax += classes_selecionadas[tipo].mp
    
    jogador.carreira = classes_selecionadas["Carreira"].nome
    setAtributos("Carreira")

    jogador.combate = classes_selecionadas["Combate"].nome
    setAtributos("Combate")

    jogador.weapon = classes_selecionadas["Combate"].arma

    jogador.divindade = classes_selecionadas["Deuses"].nome
    jogador.AddInventario(classes_selecionadas["Deuses"].item)
    jogador.Bencaos.append(classes_selecionadas["Deuses"].bencao)

    if jogador.carreira == "Herbalista":
        jogador.weapon.efeito.append(Envenenamento)

    jogador.hp = jogador.hpMax
    jogador.mp = jogador.mpMax

    if Config.labelAtributo != []:
        Config.labelAtributo = []
    
    Config.frame_jogador = Status(root)
    Config.frame_jogador.place(relx=0.8, rely=0.5, anchor="center")

    Destrui_frame(frame)

def carreiras_civis():
    carreiras_civis = [
        Carreira("Erudito", "Estudiosos dedicados a compreender o mundo.", 2, 2, 5, 2, 4, 3, 1, 4, 5),
        Carreira("Comerciante", "Especialista em influenciar mercados.", 2, 3, 3, 4, 3, 5, 3, 4, 3),
        Carreira("Ferreiro", "Criador e reparador de armas e ferramentas.", 5, 2, 2, 2, 3, 3, 1, 5, 4),
        Carreira("Herbalista", "Mestre da alquimia e natureza.", 2, 3, 4, 3, 5, 3, 1, 3, 4)
    ]
    return carreiras_civis

def aspecto_combate():
    aspectos_combate = [
        Combate("Cavaleiro", "Guerreiro resistente e poderoso.", Espada(), 3, 3, 0, 0, 0, 1, 1, 5, 2),
        Combate("Bárbaro", "Guerreiro feroz e resistente.", Machado(), 4, 2, 0, 2, 0, -1, 3, 6, 1),
        Combate("Lanceiro", "Controla o campo de batalha.", Lanca(), 1, 5, 3, 0, 2, 2, 1, 3, 2),
        Combate("Sacerdote", "Ocultista das artes divinas.", Cajado(), -1, 2, 2, 1, 3, -1, 0, 3, 6)
    ]
    return aspectos_combate

def divindades_lista():
    
    divindades_lista = [
        Divindade("Ithral, Deusa da Sabedoria", "Sabedoria e conhecimento arcano.", Sacrificio_Ithral(), Capa_verdade()),
        Divindade("Aroth, Deus da Guerra", "Força e combate.", Sacrificio_Aroth(), Armadura_Aroth()),
        Divindade("Selena, Deusa da Lua", "Mistério e ciclos cósmicos.", Sacrificio_Selena(), Amuleto_Lunar()),
        Divindade("Elenna, Deusa da Natureza", "Vida e cura.", Sacrificio_Elenna(), Coroa_de_Elenna())
    ]
    return divindades_lista

def frame_classes():
    radio_secao = [
        {"tipo": "Carreira", "Estado": False, "Array": carreiras_civis()},
        {"tipo": "Combate", "Estado": False, "Array": aspecto_combate()},
        {"tipo": "Deuses", "Estado": False, "Array": divindades_lista()},
    ]
    
    classes_selecionadas = {"Carreira": None, "Combate": None, "Deuses": None}
    
    def mostrar_info(array, tipo, info, index_secao):
        global btnProximo
        classes_selecionadas[tipo] = array
        
        if tipo == "Carreira":
            info_text = (
                f"Nome: {array.nome}\n"
                f"Descrição: {array.descricao}\n\n"
                f"Atributos:\n"
                f"HP: {array.hp} | MP: {array.mp}\n"
                f"STR: {array.str} | DEX: {array.dex} | LCK: {array.lck}\n"
                f"WIS: {array.wis} | CHA: {array.cha} | Fund: {array.fund}"
            )
        elif tipo == "Combate":
            info_text = (
                f"Nome: {array.nome}\n"
                f"Descrição: {array.descricao}\n\n"
                f"Arma: {array.arma.nome}\n"
                f"Atributos:\n"
            )
            atributos = {"HP": array.hp, "MP": array.mp, "STR": array.str, "DEX": array.dex,
                         "INT": array.int, "LCK": array.lck, "WIS": array.wis, "CHA": array.cha, "Fund": array.fund}
            atributos_formatados = [f"{k}: {v}" for k, v in atributos.items() if v != 0]
            info_text += "\n".join([" | ".join(atributos_formatados[i:i+3]) for i in range(0, len(atributos_formatados), 3)])
        elif tipo == "Deuses":
            info_text = (
                f"Nome: {array.nome}\n"
                f"Descrição: {array.descricao}\n\n"
                f"Bênção: {array.bencao}\n"
                f"Item: {array.item.nome}"
            )
        
        info.config(text=info_text)
        
        for i, secao in enumerate(radio_secao):
            secao["Estado"] = i == index_secao

        if all(classes_selecionadas.values()):
            if btnProximo:
                btnProximo.destroy()
            btnProximo = tk.Button(Btn_frame, bg="black", text=">", fg="white", font=("Arial", 15),
                                   command=partial(colocar_atributos, classes_selecionadas, frame), width=60)
            btnProximo.pack()
    
    frame = tk.Frame(root, bg="black", relief="ridge", highlightbackground="white", highlightthickness=2)
    frame.place(relx=0.5, rely=0.5, anchor="center")
    
    frame_categorias = tk.Frame(frame, bg="black")
    frame_categorias.pack()
    
    Btn_frame = tk.Frame(frame, bg="black")
    Btn_frame.pack()
    
    for j, secao in enumerate(radio_secao):
        frame_tipo = tk.Frame(frame_categorias, bg="black", relief="ridge", highlightbackground="white", highlightthickness=4)
        frame_tipo.pack()
        
        frame_label = tk.Frame(frame_categorias, bg="black")
        frame_label.pack()

        labelTipo = tk.Label(frame_label, bg="black", fg="white", font=("Arial", 15), text=secao["tipo"])
        labelTipo.pack()
        
        frame_info_Classes = tk.Frame(frame_categorias, bg="black", relief="ridge", highlightbackground="white", highlightthickness=2)
        frame_info_Classes.pack()
        
        frame_radio = tk.Frame(frame_info_Classes, bg="black")
        frame_dados = tk.Frame(frame_info_Classes, bg="black")
        
        info = tk.Label(frame_dados, justify="left", bg="black", fg="white", font=("Arial", 12), width=75, height=10)
        
        for i in range(len(secao["Array"])):
            radio_button = tk.Radiobutton(
                frame_radio,
                text=secao["Array"][i].nome,
                command=partial(mostrar_info, secao["Array"][i], secao["tipo"], info, j),
                bg="black",
                fg="white",
                font=("Arial", 15), width=20
            )
            radio_button.grid(row=i, column=0, padx=6, pady=6)
        
        info.pack()
        frame_radio.grid(row=j+1, column=0)
        frame_dados.grid(row=j+1, column=1)

def Destrui_frame(frame):
    frame.destroy()

    frame_imagens.place(relx=0.35, rely=0.45, anchor="center")
    
    root.bind("<Up>", on_key_press)
    root.bind("<Down>", on_key_press)
    root.bind("<Left>", on_key_press)
    root.bind("<Right>", on_key_press)

def Transiscao_inicio_classes(frame):
    frame.destroy()
    frame_classes()

def tela_inicial():
    frame = tk.Frame(root,bg="black")
    frame.place(relx=0.5, rely=0.35, anchor="center")

    label = tk.Label(frame,text="RPG", bg="black", fg="white", font=("Arial", 80))
    label.grid(row=0, column=0, padx=20, pady=200)

    btn = tk.Button(frame,text="Iniciar", bg="black", fg="white", font=("Arial", 25),command=partial(Transiscao_inicio_classes,frame))
    btn.grid(row=1, column=0, padx=6, pady=6)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Matriz de Imagens")
    root.attributes('-fullscreen', True)
    root.configure(bg="black")
    
    btnProximo = None 

    weapon = Weapon("",0,0,0,0,None)
    imagens = {
        "entrada": "img/entrada.png",
        "saida": "img/saida.png",
        "q": "img/quarto.png",
        "caminho": "img/caminho.png",
        "vazio": "img/vazio.png",
    }

    viewX = 5
    viewY = 5

    mapa = Mapa(23, 23)
    coordenadas_q = mapa.adicionar_qs_aleatorios(5)
    mapa.adicionar_entrada_saida()
    mapa.conectar_qs(coordenadas_q)
    mapa.conectar_entrada_saida(coordenadas_q)

    mapa_copiado = mapa.copiar()

    Config.frame_jogador = "Valor inicial"
    tela_inicial()

    jogador = Player()
    frame_imagens = mapa_copiado.exibir_area_com_imagens(viewX, viewY, imagens)

    root.mainloop()
