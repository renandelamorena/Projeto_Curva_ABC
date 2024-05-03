from time import time
import pyautogui as pag
import func.data, func.geral, func.verifica_tela, func.wms

func.wms.abre_wms()

func.wms.abre_app_wms('GERENCIAMENTO')

func.wms.abre_consulta_cadastro_produto()
func.wms.baixar_cadastro_produto()

# func.geral.salvar_planilha('produtos', '2')

# time.sleep(5)
# pag.hotkey('alt', 'f4')

# pag.hotkey('alt', 'f4')
# pag.hotkey('alt', 'f4')
# pag.hotkey('alt', 'f4')