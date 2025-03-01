from functools import partial
from modal import Player, Aranha, Goblin, Kobold, Zombi, Xonnominag,Vazo_inimigo,besta_Yithuyesh, mimico
import random

def bau_respsota(btn,btn1,btn2,label,txt,teste,jogador,btn1T,get_money,get_Consumivel,frame,destruir_Tela_evento):             
    if btn == 1:
        if jogador.lck >= teste:
            tesouro = random.choice(["Consumivel","Dinheiro"])
            txt = "(Teste de sorte:Sucesso)\nVocê conseguiu "
            sufixo = ''

            if tesouro == "Consumivel":
                item = get_Consumivel()
                jogador.AddInventario(item)
                item = item.nome
            else:
                item = get_money()
                jogador.receberMoeda(item)
                item = str(item)
                sufixo = " moeda(s)"
            
            txt += item + sufixo
        else:
            txt = "(Teste de sorte:Falha)\nNo que você abre, dentes amolados\nagarram seu braço e puxam pra dentro\n(-2 de vida)\nVocê se contorce e grita, mas consegue tirar seu braço\nO mimico avança na sua direção"
            jogador.perderVida(2)
    else:
        txt = "Você saí do quarto"
        btn1T = ">"
        btn2T = ""
        label.config(text=txt)
        btn1.config(text=btn1T,command=partial(destruir_Tela_evento,frame))
        btn2.config(text=btn2T)
    label.config(text=txt)

def Evneto_combate_respsota(btn, btn1, txt, teste, jogador, btn1T, Criar_Tela_Combat, get_Inimigo, frame, label):
    
    EmCombate = True
    if btn == 1:
        txt = "Você saca sua arma e avança"
        btn1.config(text=btn1T, command=partial(Criar_Tela_Combat, get_Inimigo(), frame))
    else:
        if jogador.dex >= teste:
            txt = "(Teste de Destreza:Sucesso)\nPassos violentos se perseguem por corredores,\nmas você é mais rápido e consegue fugir"
            EmCombate = False
        else:
            txt = "(Teste de Destreza:Falha)\nNo que você ia se virar para fugir\nA criatura corta parte do seu braço\n(-3 vida)\ne intercepta o caminho"
            jogador.perderVida(3)
            btn1.config(text=btn1T, command=partial(Criar_Tela_Combat, get_Inimigo(), frame))

    label.config(text=txt)
    return EmCombate

def tesouro_respsota(btn, btn1, txt, teste, jogador, btn1T, Criar_Tela_Combat, get_money, get_Armamento, frame, label):
    
    EmCombate = False

    if btn == 1:
        if jogador.wis >= teste:
            dinheiro = get_money()
            arma = get_Armamento()

            jogador.AddInventario(arma)
            jogador.receberMoeda(dinheiro)
            txt = "(Teste de Sabedoria:Sucesso)\nVocê pegou "+ str(dinheiro)+" moedas e "+ arma.nome
        else:
            txt = "(Teste de Sabedoria:Falha)\nAs moedas se desmancham e escorrem dos dedos\nNuma massa negra e pútrida.\nUm mau presentimento se sufoca na garganta\nAlgo de ruim te acompanha das sombras"
            EmCombate = True  # Ativa combate
            inimigoC = random.choice([Vazo_inimigo(), mimico()])
            btn1.config(text=btn1T, command=partial(Criar_Tela_Combat, inimigoC, frame))
    else:
        txt = "Você sai do quarto"

    label.config(text=txt)
    return EmCombate 

def fantasma_resposta(btn,jogador,teste,txt,label):
    if btn == 1 and jogador.wis >= teste:
        txt = "(Tesde de Sabedoria: Sucesso)\nNão é uma voz, mas varias, em coral.\nA melidiadesencarnada lhe traz paz,\nMesmo num lugar tão sombrio\nQuanto a masmorra\n(+2 mp)"
    elif btn == 2 and jogador.dex >= teste:
        txt = "(Teste de Dextreza: Sucesso)\nVocê consegue fugir da sala\nsem maiores problemas. Qualquer que fosse a fonte da vozes\nprovavelmente não é coisa boa.\nNada nessa masmorra é boa"
    else:
        txt = ""
        if btn== 2:
            txt="(Teste de Dextreza: Falha)\nNão importa o quanto você corra, a voz se agrava em uma crescente."
        else:
            txt="(Teste de Sabedoria: Falha)"
        txt+="\nVocê percebe que não são vozes, mas gritos.\nUm pandemonio de almas condenadas berrão em dor.\nO horror e exaustão te levam aos joelhos.\nVocê desmaia.\nAo acordar, as vozes sairam, mas o eco\nde seu sofrimento vai permanecer pra sempre com você\n(- 3 mp)"
    label.config(text=txt)

def fenda_repsosta(btn,btn1,btn2,txt,teste,jogador,btn1T,label,get_money,get_Consumivel,frame,destruir_Tela_evento):
    if btn == 1:
        if jogador.lck >= teste:
            peso = [1,4]
            tesouro = random.choices(["Consumivel","dineiro"], weights=peso,k=1)

            if tesouro == "Arma":
                item = get_Consumivel()
                jogador.AddInventario(item)
                txt = "(Teste de sorte:Sucesso)\nVocê pega um(a) "+item.nome+ "do buraco"
            else:
                item = get_money()
                jogador.receberMoeda(item)
                txt = "(Teste de sorte:Sucesso)\nVocê pega "+str(item)+" moedas"
        else:
                        txt = "(Teste de sorte:Falha)\nÁ instantes de pegar o que quer que brilhace na fenda,\nSua face é tomada por horro, no que o brilho piscou\nUm braço te agarra da penumbra\nGarras afundam na sua pele e você solta um grito\nVocê saca sua arma e espanta a criatura de volta ás trevas\n(-3 de vida)"
                        jogador.perderVida(3)
    else:
        txt = "No que você saia, você conseguiu ouvir\num murmurio gutural vindo do buraco\nVocê sai da sala a passos rapidos"
        btn1T = ">"
        btn2T = ""
        label.config(text=txt)
        btn1.config(text=btn1T,command=partial(destruir_Tela_evento,frame))
        btn2.config(text=btn2T)
    label.config(text=txt)