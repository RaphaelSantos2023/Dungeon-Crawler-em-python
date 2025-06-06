import random
from modal.modal_arma import Queimadura, Sangria

class Magia:
    def __init__(self, nome, custo_mana, dano, tipo,descricao, preco, ativa=False, efeito=None, concequencia_efeito = None):
        self.nome = nome
        self.custo_mana = custo_mana
        self.dano = dano
        self.efeito = efeito
        self.concequencia_efeito = concequencia_efeito
        self.descricao = descricao
        self.tipo = tipo
        self.ativa = ativa
        self.timer = 0

        self.preco = preco

    def conjurar(self, conjurador, alvo=None):
        if conjurador.mp < self.custo_mana:
            return f"\n- {conjurador.nome} tentou lançar {self.nome}, mas não tinha mana suficiente!"
        
        conjurador.mp -= self.custo_mana

        if self.tipo == "Ataque":
            dano_real = self.dano + random.randint(-5, 5)

            alvo.perderVida(dano_real)
            text = f"\n- {conjurador.nome} lança {self.nome} em {alvo.nome}, causando {dano_real} de dano!"

            if alvo != None:
                text += self.efeito(alvo)

        
        elif self.tipo == "Temporaria":
            conjurador.magiaAtiva.append(self.efeito)
        else:
            text = f"\n- {conjurador.nome} lança {self.nome}"
            text += f"\n- {conjurador.nome} foi afetado por {self.efeito}!"

        return text
    
    def __str__(self):
        return f"{self.nome}: {self.descricao}"

def Sacrificio_sabedoria(jogador):
    jogador.wis += 3
    if jogador.hp == jogador.hpMax:
        jogador.hp -= 3
    jogador.hpMax -= 3

    return "Sacrifico a Ithral"

def Sacrificio_MP(jogador):
    if jogador.mp == jogador.mpMax:
        jogador.mp += 3
    jogador.mpMax += 3
    if jogador.hp == jogador.hpMax:
        jogador.hp -= 3
    jogador.hpMax -= 3

    return "Sacrificio a Selena"

def Sacrificio_Hp(jogador):
    if jogador.mp == jogador.mpMax:
        jogador.mp -= 3
    jogador.mpMax -= 3
    if jogador.hp == jogador.hpMax:
        jogador.hp += 3
    jogador.hpMax += 3

    return "Sacrificio a Elenna"

def Sacrificio_dano(jogador):
    jogador.Dano += jogador.Dano //2
    return "- O dano foi aumentado"

def Penalidade_Sacrificio_dano(jogador):
    jogador.penalidade = jogador.Dano//2

def Bola_fogo(jogador):
    jogador.estado.append(Queimadura)
    return f"\n- {jogador.nome} está em chamas!"

def Sangria_efeito(jogador):
    jogador.estado.append(Sangria)

def Protecao_divina(jogador):
    vida = 2
    jogador.hp += vida
    return "- "+ str(jogador.divindade)+ " ouve suas preçes e te cura\n- Mais "+ str(vida)+ " de vida"

class Bola_de_fogo(Magia):
    def __init__(self):
        super().__init__("Bola de fogo", 2, 3, "Ataque", "Lança bolas de fogo\nAlguns dizem ouvirem\nRisos vinta das chamas",15, efeito=Bola_fogo)

class Sangria_magia(Magia):
    def __init__(self):
        super().__init__("Sangria", 3, 0, "Ataque", "Ao usar, drena\nParte da vida do\nInimigo",17, efeito=Sangria_efeito)

class Intervencao_divina(Magia):
    def __init__(self):
        super().__init__("Interverção divina", 2, 0, "Perpetua", "Reze pela intervenção de seu deus",20, efeito=Protecao_divina)

class Sacrificio_Ithral(Magia):
    def __init__(self):
        super().__init__("Sacrificio a Ithral", 1, 0, "Perpetua", "Sacrifique parte da vida maxima\nPor sabedoria\n(-3 hpmax, +3 wis)",12, efeito=Sacrificio_sabedoria)

class Sacrificio_Aroth(Magia):
    def __init__(self):
        super().__init__("Sacrificio a Aroth", 3, 0, "Temporaria", "Por três turnos,\nseu dano dobra,\nPorém, após isso,\nele diminui pela metado", 12, efeito=Sacrificio_dano,concequencia_efeito = Penalidade_Sacrificio_dano)

class Sacrificio_Selena(Magia):
    def __init__(self):
        super().__init__("Sacrificio a Selena", 3, 0, "Perpetua", "Sacrifique parte da vida maxima\nPor mais Mp\n(-3 hp Max, +3 mp Max)", 12, efeito=Sacrificio_MP)

class Sacrificio_Elenna(Magia):
    def __init__(self):
        super().__init__("Sacrificio a Elenna", 3, 0, "Perpetua", "Sacrifique parte do Mp maxima\nPor mais vida\n(+3 hp Max, -3 mp Max)", 12, efeito=Sacrificio_Hp)
