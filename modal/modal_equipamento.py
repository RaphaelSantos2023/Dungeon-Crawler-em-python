class Equipamento:
    def __init__(self,nome,descricao,tipo,Vitalidade,Sanidade,Efeito,str,dex,inte,lck,wis,cha,preco):
        self.nome = nome
        self.descricao = descricao
        self.tipo = tipo
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
        super().__init__(self,"Armadura de ferro","Armadura de ferro",4,0,None,2,2,0,0,0,0,18)

class Armadura_couro(Equipamento):
    def __init__(self):
        super().__init__(self,"Armadura de couro","Armadura de ferro",2,0,None,0,2,0,0,0,4,8)

class Armadura_malha(Equipamento):
    def __init__(self):
        super().__init__(self,"Armadura de malha","Armadura de ferro",3,0,None,1,2,0,0,0,0,12)

class Capuz_cultista(Equipamento):
    def __init__(self):
        super().__init__(self,"Capuz de ocultista","Armadura de ferro",1,3,None,0,0,0,1,2,-1,16)

class Amuleto_Lunar(Equipamento):
    def __init__(self):
        super().__init__("Amuleto Lunar","Amuleto dos sacerdotes lunares","Armadura",0,4,None,0,0,0,0,3,0,23)

class Armadura_Aroth(Equipamento):
    def __init__(self):
        super().__init__("Armadura de Aroth","Armadura de malha \ndos soldados do \ntemplo de Aroth","Armadura",4,0,None,3,2,0,0,-1,0,20)

class Capa_verdade(Equipamento):
    def __init__(self):
        super().__init__("Capa da verdade","Capuz dos sacerdotes da deusa","Armadura",-1,2,None,0,0,0,0,4,-2,23)

class Coroa_de_Elenna(Equipamento):
    def __init__(self):
        super().__init__("Coroa de Elenna","Ornamento da deusa","Armadura",-1,4,None,0,3,0,2,4,-1,23)
