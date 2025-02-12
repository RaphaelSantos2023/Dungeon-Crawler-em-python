

class Pano:
    def __init__(self):
        self.nome = "Pano"
        self.descricao = "Pano esfarapado(+5 vida)"
        self.vida = 5
        self.tipo = "Comestivel"

    def efeito(self,jogador):
        jogador.vida+=self.vida

class Pao:
    def __init__(self):
        self.nome = "Pao"
        self.descricao = "Pão mofado(+3 vida)"
        self.vida = 3
        self.tipo = "Comestivel"

    def efeito(self,jogador):
        jogador.vida+=self.vida

class Pao:
    def __init__(self):
        self.nome = "Pao"
        self.descricao = "Pedaço de carne(+6 vida)"
        self.vida = 6
        self.tipo = "Comestivel"

    def efeito(self,jogador):
        jogador.vida+=self.vida

class Poscao:
    def __init__(self):
        self.nome = "Poção"
        self.descricao = "Poção estranha(+7 vida)"
        self.vida = 7
        self.tipo = "Comestivel"

    def efeito(self,jogador):
        jogador.vida+=self.vida

        if any(efeito.name == "Envenenamento" for efeito in jogador.estado):
            # Remove todos os efeitos chamados "Envenenamento"
            jogador.estado = [efeito for efeito in jogador.estado if efeito.name != "Envenenamento"]


