import pyautogui as pag
import pyperclip as pcl
import os
import time

from func.verifica_tela import verificar_imagem_encontrada, click

def pause(seg=2):
    pag.PAUSE = seg

def caminho_absoluto(caminho_relativo_com_barras_normais):
    
    caminho_base = os.getcwd()

    caminho_absoluto = os.path.join(caminho_base, caminho_relativo_com_barras_normais)

    return caminho_absoluto

def salvar_planilha(nome_arquivo, onde_fixado):
    
    # click no excel
    verificar_imagem_encontrada(time.time(), 1800 , caminho_absoluto('img/gerenciamento/exel_gerado.png'), 5, 'salvar_planilha - exel_gerado')
    click(caminho_absoluto('img/gerenciamento/exel_gerado.png'), 1)  

    # tela cheia
    pag.hotkey('ctrl', 'shift', 'f1')
    pag.hotkey('ctrl', 'shift', 'f1')

    # vai em salvar como
    pause(0.4)
    pag.press('alt')
    pag.press('a')
    pag.press('a')
    pag.press('y')
    pag.press('1')
    pag.press('y')
    pag.press(onde_fixado)

    # coloca o nome do arquivo
    verificar_imagem_encontrada(time.time(), 20 , caminho_absoluto('img/excel/nome_arquivo.png'), 0.1, 'salvar_planilha - nome_arquivo')
    click(caminho_absoluto('img/excel/nome_arquivo.png'), 2)
    pcl.copy(nome_arquivo)
    pag.hotkey('ctrl', 'v')

    # salvar
    verificar_imagem_encontrada(time.time(), 20 , caminho_absoluto('img/excel/salvar_excel.png'), 0.1, 'salvar_planilha - salvar_excel')
    click(caminho_absoluto('img/excel/salvar_excel.png'), 1)

    # confirmar subistituição
    pag.press('tab')
    pag.press('enter')

    # fechar
    pag.hotkey('alt', 'f4')
    
    pause(2)

def salvar_dados():
    pass