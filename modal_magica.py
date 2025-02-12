import random

class Magia:
    def __init__(self, nome, custo_mana, dano, tipo,descricao,ativa=False, efeito=None):
        self.nome = nome
        self.custo_mana = custo_mana
        self.dano = dano
        self.efeito = efeito
        self.descricao = descricao
        self.tipo = tipo
        self.ativa = ativa
        self.timer = 0

    def conjurar(self, conjurador, alvo):
        if conjurador.mp < self.custo_mana:
            return f"\n- {conjurador.nome} tentou lançar {self.nome}, mas não tinha mana suficiente!"
        
        conjurador.mana -= self.custo_mana

        if self.tipo == "Ataque":
            dano_real = self.dano + random.randint(-5, 5)

            alvo.perderVida(dano_real)
            text = f"\n- {conjurador.nome} lança {self.nome} em {alvo.nome}, causando {dano_real} de dano!"

            if self.efeito:
                text += f"\n- {alvo.nome} foi afetado por {self.efeito}!"
        
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

def Sacrificio_dano(dano):
    dano += dano //2


class Sacrificio_Ithral(Magia):
    def __init__(self):
        super().__init__("Sacrificio a Ithral", 1, 0, "Perpetua", "Sacrifique parte da vida maxima\nPor sabedoria\n(-3 hpmax, +3 wis)", efeito=Sacrificio_sabedoria)

class Sacrificio_Aroth(Magia):
    def __init__(self):
        super().__init__("Sacrificio a Aroth", 3, 0, "Temporaria", "Por três turnos, seu dano dobra,\nPorém, após isso, ele diminui pela metado", efeito=Sacrificio_dano)

class Sacrificio_Selena(Magia):
    def __init__(self):
        super().__init__("Sacrificio a Selena", 3, 0, "Perpetua", "Sacrifique parte da vida maxima\nPor mais Mp\n(-3 hp Max, +3 mp Max)", efeito=Sacrificio_MP)

class Sacrificio_Elenna(Magia):
    def __init__(self):
        super().__init__("Sacrificio a Elenna", 3, 0, "Perpetua", "Sacrifique parte do Mp maxima\nPor mais vida\n(+3 hp Max, -3 mp Max)", efeito=Sacrificio_Hp)
