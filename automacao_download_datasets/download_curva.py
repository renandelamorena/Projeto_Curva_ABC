from time import time
import pyautogui as pag
import func.data, func.geral, func.verifica_tela, func.wms

func.wms.abre_wms()

func.wms.abre_app_wms('GERENCIAMENTO')

func.data.colar_data_1_ano_atras()

func.wms.baixar_analise_curva('curva_geral')
func.geral.salvar_planilha('curva_geral', '2')

func.wms.baixar_analise_curva('curva_cx')
func.geral.salvar_planilha('curva_cx', '2')

func.wms.baixar_analise_curva('curva_frac')
func.geral.salvar_planilha('curva_frac', '2')

pag.hotkey('alt', 'f4')
pag.hotkey('alt', 'f4')
pag.hotkey('alt', 'f4')