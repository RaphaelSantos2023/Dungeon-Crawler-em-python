class Equipamento:
    def __init__(self,nome,Vitalidade,Sanidade,Efeito,str,dex,inte,lck,wis,cha,preco):
        self.nome = nome
        self.Vitalidade = Vitalidade
        self.Sanidade = Sanidade

        self.Efeito = Efeito

        self.str = str
        self.dex = dex
        self.inte = inte
        self.lck = lck
        self.wis = wis
        self.cha = cha

        self.preco = preco

class Armadura_ferro(Equipamento):
    def __init__(self):
        super().__init__(self,"Armadura de ferro",4,0,None,2,2,0,0,0,0,18)

class Armadura_couro(Equipamento):
    def __init__(self):
        super().__init__(self,"Armadura de couro",2,0,None,0,2,0,0,0,4,8)

class Armadura_malha(Equipamento):
    def __init__(self):
        super().__init__(self,"Armadura de malha",3,0,None,1,2,0,0,0,0,12)

class Capuz_cultista(Equipamento):
    def __init__(self):
        super().__init__(self,"Capuz de ocultista",1,3,None,0,0,0,1,2,-1,16)

class Amuleto_Lunar(Equipamento):
    def __init__(self):
        super().__init__("Amuleto Lunar",0,4,None,0,0,0,0,3,0,23)

class Armadura_Aroth(Equipamento):
    def __init__(self):
        super().__init__("Armadura de Aroth",4,0,None,3,2,0,0,-1,0,20)

class Capa_verdade(Equipamento):
    def __init__(self):
        super().__init__("Capa da verdade",-1,2,None,0,0,0,0,4,-2,23)

class Coroa_de_Elenna(Equipamento):
    def __init__(self):
        super().__init__("Coroa de Elenna",-1,4,None,0,3,0,2,4,-1,23)
