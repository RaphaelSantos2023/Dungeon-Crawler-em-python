class Effect:
    def __init__(self, name, description,tipo , preco, apply_effect):

        self.nome = name
        self.description = description
        self.tipo = tipo
        self.preco = preco
        self.apply_effect = apply_effect

    def trigger(self, target):
        return self.apply_effect(target)

    def __str__(self):
        return f"{self.getnome}: {self.description}\n"
    
    def getnome(self):
        return self.nome

class Weapon:
    def __init__(self, name, weapon_type, damage, weight,preco, crit_chance,elevacao_dano = 2, special_effect=[]):
        self.nome = name
        self.tipo = weapon_type
        self.Dano = damage
        self.weight = weight
        self.crit_chance = crit_chance
        self.elevacao_dano = elevacao_dano
        self.efeito = special_effect
        self.preco = preco

    def __str__(self):
        effect_description = str(self.efeito) if self.efeito else "Nenhum"
        return f"{self.nome} ({self.tipo}): Dano {self.Dano}, Efeito: {effect_description}"

def bleed_effect(target):
    target.hp -= 7
    return f"\n- {target.nome} sofreu sangramento\n- {target.nome} sofreu 7 de dano"

def poison_effect(target):
    print("Hp antes do envenenamento: "+ str(target.hp))
    target.hp -= 2
    print("Hp depois do envenenamento: "+ str(target.hp))
    return f"\n- {target.nome} sofreu envenamento\n- {target.nome} sofreu 2 de dano"

def fire_effect(target):
    target.hp -= 4
    return f"\n- {target.nome} sofreu Queimaduras\n- {target.nome} sofreu 4 de dano"


def Atordoamento_effect(target):
    target.precisao += 2
    return f"\n- Os ataques de {target.nome} ficaram\nimprecisos"

def freeze_effect(target):
    target.dex -= 1  # Reduz a destreza em 1 ponto
    return f"\n- {target.nome} sofreu Congelamento\n- Destreza reduzida em 1 ponto."

def sangria_effect(target,jogador):
    target.hp -= 2
    jogador.hp += 2
    return f"\n- {target.nome} sofreu Sangria\n- {target.nome} perdeu 2 de vida.\n- {jogador.nome} recebeu 2 de vida"

# Criando os efeitos com os métodos corretos
Atordoamento = Effect(name="Atordoamento", description="Reduz a precisão do inimigo", tipo="Atributos", preco=5, apply_effect=Atordoamento_effect)
Congelamento = Effect(name="Congelamento", description="Reduz a destreza do alvo em 1 ponto.", tipo="Atributos", preco=8, apply_effect=freeze_effect)
Sangria = Effect(name="Sangria", description="Causa 2 de dano e dá 2 de vida ao usuario.", tipo="Vida e Dano", preco=6, apply_effect=sangria_effect)

Sangramento = Effect(name="Sangramento", description="Causa 7 de dano contínuo.",tipo="Dano", preco=6, apply_effect=bleed_effect)
Queimadura = Effect(name="Queimadura", description="Causa 4 de dano contínuo.", tipo="Dano",preco=6,apply_effect=fire_effect)
Envenenamento = Effect(name="Envenenamento",description="Causa 2 de dano continuo", tipo="Dano", preco=6, apply_effect=poison_effect)

class Faca(Weapon):
    def __init__(self):
        super().__init__(name="Faca", weapon_type="Arma", damage=4, weight=2, crit_chance=0.20,preco=4)

class Espada(Weapon):
    def __init__(self):
        super().__init__(name="Espada", weapon_type="Arma", damage=6, weight=5, crit_chance=0.15,preco=15)

class Arco(Weapon):
    def __init__(self):
        super().__init__(name="Arco", weapon_type="Arma", damage=3, weight=3, crit_chance=0.4,preco=14)

class Machado(Weapon):
    def __init__(self):
        super().__init__(name="Machado", weapon_type="Arma", damage=7, weight=7, crit_chance=0.1,preco=25)

class Lanca(Weapon):
    def __init__(self):
        super().__init__(name="Lança", weapon_type="Arma", damage=4, weight=4, special_effect=[Sangramento] , crit_chance=0.3,preco=20)

class Sabre(Weapon):
    def __init__(self):
        super().__init__(name="Sabre", weapon_type="Arma", damage=5, weight=3, crit_chance=0.35,preco=15)

class Cajado(Weapon):
    def __init__(self):
        super().__init__(name="Cajado", weapon_type="Arma Magica", damage=2, weight=2, crit_chance=0,preco=5)
