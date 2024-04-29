import time
import pyautogui as pag
import pyperclip as pcl

from func_verifica_tela import verificar_imagem_encontrada, click
from func_geral import caminho_absoluto, pause_geral

from func_geral import p_i, p_f

def abre_wms():
    
    pag.PAUSE = pause_geral()
    
    p_i(0.2)
    # minimisa
    with pag.hold('win'):
        pag.press('m')

    pag.press('win')
    pcl.copy('wms')
    pag.hotkey('ctrl', 'v')
    p_f()

    verificar_imagem_encontrada(time.time(), 10, caminho_absoluto('../img/aplicativos.png'), 0.2, 'abre_wms - aplicativos')
    click(caminho_absoluto('../img/aplicativos.png'), 1)
    
    # Seleciona WMS
    
    verificar_imagem_encontrada(time.time(), 10, caminho_absoluto('../img/wms.png'), 0.2, 'abre_wms - wms')
    click(caminho_absoluto('../img/wms.png'), 1)

    # Executa WMS
    
    verificar_imagem_encontrada(time.time(), 10, caminho_absoluto('../img/executar.png'), 0.2, 'abre_wms - executar')
    click(caminho_absoluto('../img/executar.png'), 1)

    # Loguin

    verificar_imagem_encontrada(time.time(), 10, caminho_absoluto('../img/usuario.png'), 0.2, 'abre_wms - usuario')
    click(caminho_absoluto('../img/usuario.png'), 1)

    login = 'renan'
    senha = 134679
    
    p_i(0.2)
    pcl.copy(login)
    pag.hotkey('ctrl', 'v')
    pag.press('tab')
    pcl.copy(senha)
    pag.hotkey('ctrl', 'v')

    pag.press('tab')
    pag.press('enter')
    p_f()

def abre_app_wms(app):

    p_i(0.1)
    
    verificar_imagem_encontrada(time.time(), 10, caminho_absoluto('../img/lupa_wms.png'), 0.2, 'abre_app_wms - lupa_wms')
    click(caminho_absoluto('../img/lupa_wms.png'), 1)

    pcl.copy(app)
    
    pag.hotkey('ctrl', 'v')

    pag.press('tab')
    pag.press('enter')
    
    p_f()

def abre_consulta_cadastro_produto():

    verificar_imagem_encontrada(time.time(), 10, caminho_absoluto('../img/gerenciamento/gerenciamento.png'), 0.2, 'abre_consulta_cadastro_produto - gerenciamento')
    
    verificar_imagem_encontrada(time.time(), 10, caminho_absoluto('../img/gerenciamento/consultas.png'), 0.2, 'abre_consulta_cadastro_produto - consultas')
    click(caminho_absoluto('../img/gerenciamento/consultas.png'), 1)

    verificar_imagem_encontrada(time.time(), 10, caminho_absoluto('../img/gerenciamento/consulta_cadastro_endereco_apanha.png'), 0.2, 'abre_consulta_cadastro_produto - consulta_cadastro_endereco_apanha')
    click(caminho_absoluto('../img/gerenciamento/consulta_cadastro_endereco_apanha.png'), 1)
        
def baixar_cadastro_produto():

    p_i(0.1)

    #seleciona 'todos' os flag

    pag.press('tab', presses=7)

    pag.press('up')

    pag.press('tab', presses=8)
    
    pag.press('up', presses=2)

    pag.press('tab')
    pag.press('up', presses=2)

    pag.press('tab')
    pag.press('up', presses=2)

    pag.press('tab')
    pag.press('up', presses=2)

    pag.press('tab')
    pag.press('up', presses=2)

    pag.press('tab')
    pag.press('up', presses=2)

    verificar_imagem_encontrada(time.time(), 10, caminho_absoluto('../img/excel/botao_gerar_excel.png'), 0.2, 'baixar_cadastro_produto - botao_gerar_excel')
    click(caminho_absoluto('../img/excel/botao_gerar_excel.png'), 1)

    p_f()

def abre_consulta_analise_curva():

    verificar_imagem_encontrada(time.time(), 10, r'img\gerenciamento\consultas.png', 0.2, 'abre_consulta_analise_curva - consultas')
    click(r'img\gerenciamento\consultas.png', 1)

    verificar_imagem_encontrada(time.time(), 10, r'img\gerenciamento\analise_curva_abc.png', 0.2, 'abre_consulta_analise_curva - analise_curva_abc')
    click(r'img\gerenciamento\analise_curva_abc.png', 1)

def baixar_analise_curva(tipo_curva):
    
    if tipo_curva == 'curva_geral':

        pag.press('tab', presses=2)
        pag.press('enter')

        # espera filtrar para precionar o botão
        verificar_imagem_encontrada(time.time(), 1800, caminho_absoluto('../img/excel/botao_gerar_excel.png'), 5, 'baixar_analise_curva - botao_gerar_excel')
        click(caminho_absoluto('../img/excel/botao_gerar_excel.png'), 1)

        pag.press('tab')
        pag.press('enter')

    if tipo_curva == 'curva_cx':

        verificar_imagem_encontrada(time.time(), 20, caminho_absoluto('../img/gerenciamento/limpar_filtro.png'), 1, 'baixar_analise_curva - limpar_filtro')
        click(caminho_absoluto('../img/gerenciamento/limpar_filtro.png'), 1)

        verificar_imagem_encontrada(time.time(), 20, caminho_absoluto('../img/gerenciamento/selec_curva_cx.png'), 1, 'baixar_analise_curva - selec_curva_cx')
        click(caminho_absoluto('../img/gerenciamento/selec_curva_cx.png'), 1)

        pag.press('tab', presses=3)
        pag.press('enter')

        # espera filtrar para precionar o botão
        verificar_imagem_encontrada(time.time(), 1800, caminho_absoluto('../img/excel/botao_gerar_excel.png'), 5, 'baixar_analise_curva - botao_gerar_excel')
        click(caminho_absoluto('../img/excel/botao_gerar_excel.png'), 1)
        pag.press('tab')
        pag.press('enter')

    if tipo_curva == 'curva_frac':
        
        verificar_imagem_encontrada(time.time(), 20, caminho_absoluto('../img/gerenciamento/limpar_filtro.png'), 1, 'baixar_analise_curva - limpar_filtro')
        click(caminho_absoluto('../img/gerenciamento/limpar_filtro.png'), 1)

        verificar_imagem_encontrada(time.time(), 20, caminho_absoluto('../img/gerenciamento/selec_curva_frac.png'), 1, 'baixar_analise_curva - selec_curva_frac')
        click(caminho_absoluto('../img/gerenciamento/selec_curva_frac.png'), 1)

        pag.press('tab', presses=3)
        pag.press('enter')

        # espera filtrar para precionar o botão
        verificar_imagem_encontrada(time.time(), 1800, caminho_absoluto('../img/excel/botao_gerar_excel.png'), 5, 'baixar_analise_curva - botao_gerar_excel')
        click(caminho_absoluto('../img/excel/botao_gerar_excel.png'), 1)
        pag.press('tab')
        pag.press('enter')