def Bau():
    img = "img/eventos/Inicio/Bau.png"
    label = "No meio das ruinas do comodo,\nvocê encontra um baú\nDeseja abrir?"
    btn1 = "Abrir o Baú"
    btn2 = "<Pode ser um Mimico>"
    evento = 0

    return img,label,btn1,btn2,evento

def Encontro_Fantasma():
    img = "img/eventos/inicio/Fantasma_evento.png"
    label = "De subito, você para.\nO cheiro de enchofre\ninvade seu olfato.\nVocê algussa o ouvido no\nque parece ser uma voz\nsussurando, como uma brisa\ngelida.\n"
    btn1 = "Ouvir"
    btn2 = "Fugir"
    evento = 1

    return img,label,btn1,btn2,evento

def combate_cenario():
    img = "img/eventos/inicio/Combate_evento.png"
    label = "Formas mostruosas se aproximam!"
    btn1 = "Avançar"
    btn2 = "Fugir"
    evento = 2

    return img,label,btn1,btn2,evento

def Tesouro_suspeito():
    img = "img/eventos/inicio/Tesouro_evento.png"
    label = "Joias e moedas se empilham numa mesa\nCadaveres e esqueletos se extendem no chão\nAlguns ainda frescos"
    btn1 = "Pegar tesouro"
    btn2 = "<Muito ariscado>"
    evento = 3

    return img,label,btn1,btn2,evento

def fenda():
    img = "img/eventos/inicio/Fenda_evento.png"
    label = "Uma fenda fere a pedra sobre seus pés\nCintilando um brilho palido, uma luz\npisca para você, seduzente"
    btn1 = "Tentar pegar o objeto"
    btn2 = "Ignorar"
    evento = 4

    return img,label,btn1,btn2,evento

def Criatura_Escuro():
    img = "img/eventos/inicio/Dormindo_event.png"
    label = "Do escuro da sala,\nVocê ouve os barulhos\nde alguma criatura.\nEla parece estar dorindo"
    btn1 = "Passar furtivo"
    btn2 = "Atacar"
    evento = 5

    return img,label,btn1,btn2,evento

def Comeciante():
    img = "img/eventos/inicio/Comeciante_event.png"
    label = "Uma voz assovia para você\n<Ei, colega, gostaria de algumas trocas?>"
    btn1 = "Aceitar proposta"
    btn2 = "Rejeitar proposta"
    evento = 6

    return img,label,btn1,btn2,evento

def Aranha_evento():
    img = "img/eventos/inicio/Aranha_evento.png"
    label = "No que você perambulava pela\nmasmorra, você sente uma\ndor ardente na mão.\nVocê se vira e vê\numa aranha sobre sua mão"
    btn1 = ">"
    btn2 = ""
    evento = 7

    return img,label,btn1,btn2,evento