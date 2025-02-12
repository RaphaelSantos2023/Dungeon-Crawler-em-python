import random
from modalConsumiveis import Pao,Pano,Poscao
from modal_arma import Envenenamento, Sangria
from modal_magica import Sacrificio_Aroth

class Inimigo:
    def __init__(self, nome, nivel, hp_base, dano, exp, str_base, dex, cha, fund, crit_chance,efeito, simbolo):
        self.hp = hp_base * nivel
        self.nome = nome
        self.simbolo = {"simbolo": simbolo}
        self.dano = dano
        self.exp = exp * nivel
        self.str = str_base
        self.dex = dex
        self.cha = cha
        self.fund = fund
        self.nivel = nivel
        self.crit_chance = crit_chance  # Chance de crítico
        self.estado = []
        self.precisao = 0
        self.efeito = efeito
        self.defendendo = False
        self.turnos_c_efeito = 0

    def acerto_attack(self, inimigo):
        dice = random.randrange(1, 13)
        dice -= self.precisao
        return dice + self.str >= inimigo.str

    def tentar_Quebrar_Defesa(self):
        tentativa = random.randrange(1, 13)
        if tentativa > 7:
            return True
        return False

    def attack(self, target):
        text = ""
        base_damage = random.randint(1, self.dano)
        if self.acerto_attack(target) and target.defendendo == False:
            
            if random.uniform(0, 1) < self.crit_chance:
                base_damage *= 2
                text = f"- {self.nome} causou ataque crítico!"
            text += f"\n- {self.nome} causou {base_damage} de dano"
            target.hp -= base_damage

            if self.efeito and self.efeito not in target.estado:
                target.estado.append(self.efeito)
        elif target.defendendo:

            tentativa = self.tentar_Quebrar_Defesa()
            if tentativa:
                base_damage = 1 + base_damage // 2
                target.hp -= base_damage
                text += f"\n- {self.nome} conseguiu passar pela defesa\n- {self.nome} deu {base_damage} de dano"
            else:
                text += f"\n- {self.nome} tentou atacar, mas falhou"
            target.defendendo = False
        else:
            text += f"\n- {self.nome} errou"
        return text

    def getDano(self):
        return self.dano
    
    def sofrer_Efeito(self,inimigo):
        txt = ""
        for i in range(len(self.estado)):
            if self.turnos_c_efeito == 3:
                if len(self.estado) >1:
                    self.estado.pop(i-1)
                else:
                    self.estado.pop(0)
                self.turnos_c_efeito = 0
            else:
                self.turnos_c_efeito +=1
                
                for efeito in self.estado[i]:
                    if efeito == Sangria:
                       txt += efeito.apply_effect(self,inimigo)
                    else:
                        txt += efeito.apply_effect(self)
        return txt

    def perderVida(self, dano):
        self.hp -= dano

class besta_Yithuyesh(Inimigo):
    def __init__(self, nivel):
        super().__init__("Besta de Yithuyesh", nivel, 17, 7, 15, 9, 8, 9, 0, 0.25, [Sangria],"img/Personagens/besta_Yithuyesh.png")

class Aranha(Inimigo):
    def __init__(self, nivel):
        super().__init__("Aranha", nivel, 12, 2, 10, 4, 4, 6, 1, 0.15, [Envenenamento] ,"img/Personagens/aranha1.png")

class Goblin(Inimigo):
    def __init__(self, nivel):
        super().__init__("Goblin", nivel, 13, 4, 10, 4, 4, 6, 3, 0.10, None, "img/Personagens/goblin2.png")

class Xonnominag(Inimigo):
    def __init__(self, nivel):
        super().__init__("Xonnominag", nivel, 14, 8, 15, 8, 5, 7, 0, 0.2, None, "img/Personagens/Xonnominag.png")

class Zombi(Inimigo):
    def __init__(self, nivel):
        super().__init__("Zombi", nivel, 15, 3, 15, 5, 4, 6, 2, 0.05, None,"img/Personagens/zombi.png")

class Kobold(Inimigo):
    def __init__(self, nivel):
        super().__init__("Kobold", nivel, 16, 5, 15, 5, 4, 6, 3, 0.12, None,"img/Personagens/Kobold1.png")

class Vazo_inimigo(Inimigo):
    def __init__(self, nivel):
        super().__init__("Vazo de almas", nivel, 8, 2, 8, 3, 5, 6, 3, 0.12, None,"img/Personagens/vazo_almas.png")
    
    def attack(self, target):
        text = ""
        base_damage = random.randint(1, self.dano)
        if self.acerto_attack(target) and target.defendendo == False:
            
            if random.uniform(0, 1) < self.crit_chance:
                base_damage *= 2
                text = f"- {self.nome} causou ataque crítico!"
            text += f"\n- {self.nome} causou {base_damage} de dano"
            target.mp -= base_damage

            if self.efeito and self.efeito not in target.estado:
                target.estado.append(self.efeito)
        elif target.defendendo:

            tentativa = self.tentar_Quebrar_Defesa()
            if tentativa:
                base_damage = 1 + base_damage // 2
                target.mp -= base_damage
                text += f"\n- {self.nome} conseguiu passar pela defesa\n- {self.nome} deu {base_damage} de dano"
            else:
                text += f"\n- {self.nome} tentou atacar, mas falhou"
            target.defendendo = False
        else:
            text += f"\n- {self.nome} errou"
        return text

class Player:
    def __init__(self):
        self.level = 1
        self.exp = 230
        
        self.hp = 0
        self.hpMax = 0
        self.mp = 0
        self.mpMax = 0

        self.Condicoes = []

        self.carreira = ""
        self.combate = ""
        self.divindade = ""

        self.armadura = ""

        self.nome = "Você"

        self.simbolo = {
            "simbolo": "img/Personagens/player.png",
            "status": "img/Personagens/jogador_status.png",
        }
        
        self.str = 0
        self.dex = 0
        self.inte = 0
        self.lck = 0
        self.wis = 0
        self.cha = 0
        self.fund =0 

        self.magiaAtiva = []
        self.Bencaos = []

        self.weapon = None
        self.inventario = [Pao(),Pano()]
        
        self.estado = []
        self.precisao = 0
        self.turnos_c_efeito = 0
        self.turnos_c_Magia = 0

        self.penalidade = 0
        self.Dano = 0

        self.defendendo = False
    
    def sofrer_Efeito(self,inimigo):
        txt = ""
        for i in range(len(self.estado)):
            if self.turnos_c_efeito == 3:
                if len(self.estado) >1:
                    self.estado.pop(i-1)
                else:
                    self.estado.pop(0)
                self.turnos_c_efeito = 0
            else:
                self.turnos_c_efeito +=1
                
                for efeito in self.estado[i]:
                    if efeito == Sangria:
                       txt += efeito.apply_effect(self,inimigo)
                    else:
                        txt += efeito.apply_effect(self)
        return txt
    
    def get_estado(self):
        txt = ""
        for i in range(len(self.estado)):
            txt += "- " + f"{self.estado[i].name}: {self.estado[i].description}" +"\n" 
        
        return txt if self.estado else "Nenhum efeito ativo"

    def levelUp(self,exp):
        self.exp += exp
    
    def AumentarLevel(self):
        if self.exp >= 100:
            pontos = self.exp // 100
            resto = self.exp % 100  # Experiência restante
            self.level += pontos
            self.exp = resto 
            return pontos
        return None

    def acerto_attack(self, inimigo):
        dice = random.randrange(1,13)
        diceEn = random.randrange(1,13)
        dice -= self.precisao 

        if self.str+ dice >= inimigo.str+diceEn:
            return True
        return False
    
    def conjurarMagia(self, magia, alvo=None):
        if self.mp < magia.custo_mana:
            return f"\n- {self.nome} tentou lançar {magia.nome}, mas não tinha mana suficiente!"
        
        self.mp -= magia.custo_mana
        
        if magia.tipo == "Temporaria":
            self.magiaAtiva.append(magia)
            return f"\n- {self.nome} lançou {magia.nome}! Seu efeito foi ativado."
        return ""

    def attack(self, target):
        text = ""
        if self.acerto_attack(target):
            base_damage = random.randint(1, self.weapon.Dano)
            
            # Verifica se a magia de Sacrifício a Aroth está ativa
            if any(isinstance(magia, Sacrificio_Aroth) for magia in self.magiaAtiva):
                if self.turnos_c_Magia < 3:
                    base_damage *= 2
                else:
                    base_damage //= 2
                self.turnos_c_Magia += 1
                
                # Remove a magia após o efeito completo
                if self.turnos_c_Magia == 6:
                    self.magiaAtiva = [magia for magia in self.magiaAtiva if not isinstance(magia, Sacrificio_Aroth)]
                    self.turnos_c_Magia = 0
            
            if self.penalidade > 0:
                base_damage -= self.penalidade
            
            if random.uniform(0, 1) < self.weapon.crit_chance:
                base_damage *= self.weapon.elevacao_dano
                text += f"\n- {self.nome} causou ataque crítico!"
            
            text += f"\n- {self.nome} causou {base_damage} de dano"
            target.hp -= base_damage
        else:
            text += f"\n- {self.nome} errou"
        return text

    def defender(self):
        self.defendendo = True
        return f"\n- {self.nome} se defendeu"
        
    def Fugir(self, inimigo):
        dice = random.randrange(1,7)

        if self.dex +dice <= inimigo.dex:
            return True
        return False
    
    def definir_atributo(self,strt,dex,inte,lck,wis,cha):
        self.str = strt
        self.dex = dex
        self.inte = inte
        self.lck = lck
        self.wis = wis
        self.cha = cha
        self.Dano = self.weapon.Dano
    
    def Usar(self, item,tipo,id):
        print("Usou1")
        if tipo == "Armadura":
            print("tipo: "+tipo.nome)
        else:
            if self.hp + item.vida <= self.hpMax:
                self.hp += item.vida
            else:
                self.hp = self.hpMax
                self.RemoveInventario(id)
        print("Usou2")
    
    def RemoveInventario(self,id):
        self.inventario.pop(id)

    def AddInventario(self,item):
        self.inventario.append(item)

    def AddEfeito(self,item):
        self.efeitos.append(item)
    
    def getInventario(self):
        return self.inventario
    
    def getDano(self):
        return self.weapon.Dano
    
    def perderVida(self,dano):
        self.hp -= dano
    
    def receberMoeda(self,moeda):
        self.fund += moeda
