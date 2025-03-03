def Bau():
    label = "No meio das ruinas do comodo,\nvocê encontra um baú\nDeseja abrir?"
    btn1 = "Abrir o Baú"
    btn2 = "<Pode ser um Mimico>"
    evento = 0

    return label,btn1,btn2,evento

def Encontro_Fantasma():
    label = "De subito, você para.\nO cheiro de enchofre invade seu olfato.\nVocê algussa o ouvido no\nque parece ser uma voz\nsussurando, como uma brisa\ngelida.\n"
    btn1 = "Ouvir"
    btn2 = "Fugir"
    evento = 1

    return label,btn1,btn2,evento

def combate_cenario():
    label = "Formas mostruosas grunhem para você, nas trevas!"
    btn1 = "<VENHAM COM TUDO!>"
    btn2 = "Tentar fugir"
    evento = 2

    return label,btn1,btn2,evento

def Tesouro_suspeito():
    label = "Joias e moedas se empilham numa mesa\nCadaveres e esqueletos se extendem no chão\nAlguns ainda frescos"
    btn1 = "Pegar tesouro"
    btn2 = "<Muito ariscado>"
    evento = 3

    return label,btn1,btn2,evento

def fenda():
    label = "Uma fenda fere a pedra sobre seus pés\nCintilando um brilho palido, uma luz\npisca para você, seduzente"
    btn1 = "Tentar pegar o objeto"
    btn2 = "Ignorar"
    evento = 4

    return label,btn1,btn2,evento

def Criatura_Escuro():
    label = "Do escuro da sala,\nVocê ouve os barulhos\nde alguma criatura.\nEla parece estar dorindo"
    btn1 = "Passar furtivo"
    btn2 = "Atacar"
    evento = 5

    return label,btn1,btn2,evento