class Consumivel:
    def __init__(self, nome, descricao, vida, preco,mp):
        self.nome = nome
        self.descricao = descricao
        self.vida = vida
        self.mp = mp
        self.tipo = "Comestível"
        self.preco = preco

    def efeito(self, jogador):
        
        if jogador.hp + self.vida >= jogador.hpMax:
            jogador.hp = jogador.hpMax
        else: 
            jogador.hp += self.vida
        
        if jogador.mp + self.mp >= jogador.mpMax:
            jogador.mp = jogador.mpMax
        else: 
            jogador.mp += self.mp
        
        self.efeito_extra(jogador)

    def efeito_extra(self, jogador):
        """Método para sobrescrever se necessário em subclasses."""
        pass

class Pano(Consumivel):
    def __init__(self):
        super().__init__("Pano", "Pano esfarapado (+5 hp)", 5, 5,0)

class Pao(Consumivel):
    def __init__(self):
        super().__init__("Pão", "Pão mofado (+3 hp)", 3, 2,0)

class Poscao(Consumivel):
    def __init__(self):
        super().__init__("Poção", "Poção estranha (+7 hp)", 7, 10,2)

    def efeito_extra(self, jogador):
        jogador.estado = [efeito for efeito in jogador.estado if efeito.name != "Envenenamento"]

class Raiz_mp(Consumivel):
    def __init__(self):
        super().__init__("Raiz de mandracora", "Raiz de propriedades Magicas\n(+4 mp)", 0, 8, 4)

    def efeito_extra(self, jogador):
        jogador.estado = [efeito for efeito in jogador.estado if efeito.nome != "Envenenamento"]