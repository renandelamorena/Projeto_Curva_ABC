import time
import pyautogui as pag
import pyperclip as pcl

from func.verifica_tela import verificar_imagem_encontrada, click
from func.geral import caminho_absoluto, pause

def abre_wms():
    
    pause(0.2)
    # minimisa
    with pag.hold('win'):
        pag.press('m')

    pag.press('win')
    pcl.copy('wms')
    pag.hotkey('ctrl', 'v')
    pause()

    verificar_imagem_encontrada(time.time(), 10, caminho_absoluto('automacao_download_datasets/img/aplicativos.png'), 0.2, 'abre_wms - aplicativos')
    click(caminho_absoluto('automacao_download_datasets/img/aplicativos.png'), 1)
    
    # Seleciona WMS
    
    verificar_imagem_encontrada(time.time(), 10, caminho_absoluto('automacao_download_datasets/img/wms.png'), 0.2, 'abre_wms - wms')
    click(caminho_absoluto('automacao_download_datasets/img/wms.png'), 1)

    # Executa WMS
    
    verificar_imagem_encontrada(time.time(), 10, caminho_absoluto('automacao_download_datasets/img/executar.png'), 0.2, 'abre_wms - executar')
    click(caminho_absoluto('automacao_download_datasets/img/executar.png'), 1)

    # Loguin

    verificar_imagem_encontrada(time.time(), 10, caminho_absoluto('automacao_download_datasets/img/usuario.png'), 0.2, 'abre_wms - usuario')
    click(caminho_absoluto('automacao_download_datasets/img/usuario.png'), 1)

    login = 'renan'
    senha = 134679
    
    pause(0.2)
    pcl.copy(login)
    pag.hotkey('ctrl', 'v')
    pag.press('tab')
    pcl.copy(senha)
    pag.hotkey('ctrl', 'v')

    pag.press('tab')
    pag.press('enter')
    pause()

def abre_app_wms(app):

    pause(0.1)
    
    verificar_imagem_encontrada(time.time(), 10, caminho_absoluto('automacao_download_datasets/img/lupa_wms.png'), 0.2, 'abre_app_wms - lupa_wms')
    click(caminho_absoluto('automacao_download_datasets/img/lupa_wms.png'), 1)

    pcl.copy(app)
    
    pag.hotkey('ctrl', 'v')

    pag.press('tab')
    pag.press('enter')
    
    pause()

def abre_consulta_cadastro_produto():

    verificar_imagem_encontrada(time.time(), 10, caminho_absoluto('automacao_download_datasets/img/wms/wms.png'), 0.2, 'abre_consulta_cadastro_produto - wms')
    
    verificar_imagem_encontrada(time.time(), 10, caminho_absoluto('automacao_download_datasets/img/wms/consultas.png'), 0.2, 'abre_consulta_cadastro_produto - consultas')
    click(caminho_absoluto('automacao_download_datasets/img/wms/consultas.png'), 1)

    verificar_imagem_encontrada(time.time(), 10, caminho_absoluto('automacao_download_datasets/img/wms/consulta_cadastro_endereco_apanha.png'), 0.2, 'abre_consulta_cadastro_produto - consulta_cadastro_endereco_apanha')
    click(caminho_absoluto('automacao_download_datasets/img/wms/consulta_cadastro_endereco_apanha.png'), 1)
        
def baixar_cadastro_produto():

    pause(0.1)

    #seleciona 'todos' os flag

    verificar_imagem_encontrada(time.time(), 10, caminho_absoluto('automacao_download_datasets/img/wms/filtro_cadastro_ender_apanha.png'), 0.2, 'baixar_cadastro_produto - filtro_cadastro_ender_apanha')
    click(caminho_absoluto('automacao_download_datasets/img/wms/filtro_cadastro_ender_apanha.png'), 1)

    verificar_imagem_encontrada(time.time(), 10, caminho_absoluto('automacao_download_datasets/img/wms/estoq_apan_frac.png'), 0.2, 'baixar_cadastro_produto - estoq_apan_frac')
    click(caminho_absoluto('automacao_download_datasets/img/wms/estoq_apan_frac.png'), 1)

    verificar_imagem_encontrada(time.time(), 10, caminho_absoluto('automacao_download_datasets/img/wms/estoq_apan_promo_frac.png'), 0.2, 'baixar_cadastro_produto - estoq_apan_promo_frac')
    click(caminho_absoluto('automacao_download_datasets/img/wms/estoq_apan_promo_frac.png'), 1)

    verificar_imagem_encontrada(time.time(), 10, caminho_absoluto('automacao_download_datasets/img/wms/estoq_armazenagem.png'), 0.2, 'baixar_cadastro_produto - estoq_armazenagem')
    click(caminho_absoluto('automacao_download_datasets/img/wms/estoq_armazenagem.png'), 1)

    verificar_imagem_encontrada(time.time(), 10, caminho_absoluto('automacao_download_datasets/img/wms/pedido_pendente.png'), 0.2, 'baixar_cadastro_produto - pedido_pendente')
    click(caminho_absoluto('automacao_download_datasets/img/wms/pedido_pendente.png'), 1)

    # verificar_imagem_encontrada(time.time(), 10, caminho_absoluto('automacao_download_datasets/img/wms/estoq_apan_cx.png'), 0.2, 'baixar_cadastro_produto - estoq_apan_cx')
    # click(caminho_absoluto('automacao_download_datasets/img/wms/estoq_apan_cx.png'), 1)

    # verificar_imagem_encontrada(time.time(), 10, caminho_absoluto('automacao_download_datasets/img/wms/estoque_apan_promo_cx.png'), 0.2, 'baixar_cadastro_produto - estoque_apan_promo_cx')
    # click(caminho_absoluto('automacao_download_datasets/img/wms/estoque_apan_promo_cx.png'), 1)

    verificar_imagem_encontrada(time.time(), 10, caminho_absoluto('automacao_download_datasets/img/wms/receb_pendente.png'), 0.2, 'baixar_cadastro_produto - receb_pendente')
    click(caminho_absoluto('automacao_download_datasets/img/wms/receb_pendente.png'), 1)

    # ---

    verificar_imagem_encontrada(time.time(), 10, caminho_absoluto('automacao_download_datasets/img/excel/botao_gerar_excel.png'), 0.2, 'baixar_cadastro_produto - botao_gerar_excel')
    click(caminho_absoluto('automacao_download_datasets/img/excel/botao_gerar_excel.png'), 1)

    pause()

def abre_consulta_analise_curva():

    verificar_imagem_encontrada(time.time(), 10, caminho_absoluto('automacao_download_datasets/img/wms/consultas.png'), 0.2, 'abre_consulta_analise_curva - consultas')
    click(caminho_absoluto('automacao_download_datasets/img/wms/consultas.png'), 1)

    verificar_imagem_encontrada(time.time(), 10, caminho_absoluto('img/wms/analise_curva_abc.png'), 0.2, 'abre_consulta_analise_curva - analise_curva_abc')
    click(caminho_absoluto('automacao_download_datasets/img/wms/analise_curva_abc.png'), 1)

def baixar_analise_curva(tipo_curva):
    
    if tipo_curva == 'curva_geral':

        pag.press('tab', presses=2)
        pag.press('enter')

        # espera filtrar para precionar o botão
        verificar_imagem_encontrada(time.time(), 1800, caminho_absoluto('automacao_download_datasets/img/excel/botao_gerar_excel.png'), 5, 'baixar_analise_curva - botao_gerar_excel')
        click(caminho_absoluto('automacao_download_datasets/img/excel/botao_gerar_excel.png'), 1)

        pag.press('tab')
        pag.press('enter')

    if tipo_curva == 'curva_cx':

        verificar_imagem_encontrada(time.time(), 20, caminho_absoluto('automacao_download_datasets/img/wms/limpar_filtro.png'), 1, 'baixar_analise_curva - limpar_filtro')
        click(caminho_absoluto('automacao_download_datasets/img/wms/limpar_filtro.png'), 1)

        verificar_imagem_encontrada(time.time(), 20, caminho_absoluto('automacao_download_datasets/img/wms/selec_curva_cx.png'), 1, 'baixar_analise_curva - selec_curva_cx')
        click(caminho_absoluto('automacao_download_datasets/img/wms/selec_curva_cx.png'), 1)

        pag.press('tab', presses=3)
        pag.press('enter')

        # espera filtrar para precionar o botão
        verificar_imagem_encontrada(time.time(), 1800, caminho_absoluto('automacao_download_datasets/img/excel/botao_gerar_excel.png'), 5, 'baixar_analise_curva - botao_gerar_excel')
        click(caminho_absoluto('automacao_download_datasets/img/excel/botao_gerar_excel.png'), 1)
        pag.press('tab')
        pag.press('enter')

    if tipo_curva == 'curva_frac':
        
        verificar_imagem_encontrada(time.time(), 20, caminho_absoluto('automacao_download_datasets/img/wms/limpar_filtro.png'), 1, 'baixar_analise_curva - limpar_filtro')
        click(caminho_absoluto('automacao_download_datasets/img/wms/limpar_filtro.png'), 1)

        verificar_imagem_encontrada(time.time(), 20, caminho_absoluto('automacao_download_datasets/img/wms/selec_curva_frac.png'), 1, 'baixar_analise_curva - selec_curva_frac')
        click(caminho_absoluto('automacao_download_datasets/img/wms/selec_curva_frac.png'), 1)

        pag.press('tab', presses=3)
        pag.press('enter')

        # espera filtrar para precionar o botão
        verificar_imagem_encontrada(time.time(), 1800, caminho_absoluto('automacao_download_datasets/img/excel/botao_gerar_excel.png'), 5, 'baixar_analise_curva - botao_gerar_excel')
        click(caminho_absoluto('automacao_download_datasets/img/excel/botao_gerar_excel.png'), 1)
        pag.press('tab')
        pag.press('enter')