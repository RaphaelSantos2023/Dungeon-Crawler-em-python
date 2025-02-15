class Carreira:
    def __init__(self, nome, descricao, str_, dex, int_, lck, wis, cha, fund, hp, mp):
        self.nome = nome
        self.descricao = descricao
        self.str = str_
        self.dex = dex
        self.int = int_
        self.lck = lck
        self.wis = wis
        self.cha = cha
        self.fund = fund
        self.hp = hp
        self.mp = mp

class Combate:
    def __init__(self, nome, descricao, arma, str_, dex, int_, lck, wis, cha, fund, hp, mp):
        self.nome = nome
        self.descricao = descricao
        self.arma = arma
        self.str = str_
        self.dex = dex
        self.int = int_
        self.lck = lck
        self.wis = wis
        self.cha = cha
        self.fund = fund
        self.hp = hp
        self.mp = mp

class Divindade:
    def __init__(self, nome, descricao, bencao, item):
        self.nome = nome
        self.descricao = descricao
        self.bencao = bencao
        self.item = item
