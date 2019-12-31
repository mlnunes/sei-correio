import pyautogui
import pandas as pd


documento = "0181900"
im = pyautogui.screenshot()
posicao = pyautogui.locateOnScreen('.\\src\\caixa_pesquisa.png')
caixa_pesquisa = [(posicao[0]+int(posicao[2]/2)), (posicao[1]+int(posicao[3]/2))]
pyautogui.click(caixa_pesquisa, button='left')
pyautogui.typewrite(documento)
pyautogui.typewrite('\n')
pyautogui.PAUSE = 0.5
posicao = None
while posicao == None:
    posicao = pyautogui.locateOnScreen('.\\src\\botao_correio.png')
    
botao_correio = [(posicao[0]+int(posicao[2]/2)), (posicao[1]+int(posicao[3]/2))]
pyautogui.click(botao_correio, button='left')

posicao = None
while posicao == None:
    posicao = pyautogui.locateOnScreen('.\\src\\tipo_impressao.png')

selecao_impressao = [(posicao[0]+10), (posicao[1]+10)]
pyautogui.click(selecao_impressao, button='left')
posicao = pyautogui.locateOnScreen('.\\src\\solicitar_expedicao.png')
botao_expedicao = [(posicao[0]+int(posicao[2]/2)), (posicao[1]+int(posicao[3]/2))]
pyautogui.click(botao_expedicao, button='left')

