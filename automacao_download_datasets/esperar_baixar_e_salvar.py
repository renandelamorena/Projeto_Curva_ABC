# %% [markdown]
# # Imports

# %%
import pyautogui as pag
import pyperclip as pcl
import time
from time import sleep

# %%
#define pause geral
pause_geral = 2   
pag.PAUSE = pause_geral

#pause personalizado

def p_i(pause):
    pag.PAUSE = pause
    
def p_f():
    pag.PAUSE = pause_geral

# %% [markdown]
# ## Func

# %% [markdown]
# ### Verifica tela

# %%
def verifica_tela(tela_aguardando_local):

    while True:

        tela_aguardando = pag.locateOnScreen(tela_aguardando_local, confidence=0.8)

        sleep(20)

        if tela_aguardando is not None:
            print('Aguardando...')
        else:
            print('Finalizado')
            break

# %%
def encontrar_tela(onde, oque, click, precisão):
    sleep(2)

    img = pag.locateCenterOnScreen(onde, confidence = precisão)
    if img is not None:
        x, y = img

        if click == 2: # duplo
            pag.doubleClick(x=x, y=y)

        if click == 1: # click normal
            pag.click(x=x, y=y)

    else:
        return(pag.alert(f'Não encontrado: {oque}'))
    

# %%
# Função para verificar se a imagem está presente na tela
def verificar_imagem(imagem_path):
    try:
        # Procura a posição da imagem na captura de tela
        posicao = pag.locateOnScreen(imagem_path, confidence = 0.9)

        # Se a posição for encontrada, a imagem está presente
        if posicao:
            print("Imagem encontrada!")
            return True
        else:
            print("Imagem não encontrada.")
            return False

    except Exception as e:
        print(f"Erro ao verificar imagem: {e}")
        return False

def verificar_imagem_encontrada(tempo_inicial, timeout, imagem_path):

    while time.time() - tempo_inicial < timeout:
        if verificar_imagem(imagem_path):
            print("Condição atendida. Continuando com o restante do código.")
            break
        else:
            print("Aguardando a condição ser atendida...")
            time.sleep(5)  # Aguarde 5 segundos antes de verificar novamente

    # Se o loop sair sem atender à condição, você pode tratar isso como um timeout
    if time.time() - tempo_inicial >= timeout:
        print("Timeout: A condição demorou mais do que o limite de tempo especificado.")

# %% [markdown]
# ### Gerenciamento

# %%
def abre_consulta_cadastro_produto():
    
    encontrar_tela(r'img\gerenciamento\consultas.png', 'Botão "Consultas"', 1, 0.9)

    sleep(1)

    encontrar_tela(r'img\gerenciamento\consulta_cadastro_endereco_apanha.png', 'Cadastro de Endereço de Apanha', 1, 0.9)

# %%
def baixar_cadastro_produto():
    
    sleep(2)

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

    sleep(1)

    #gera excel
    pag.press('tab', presses=4)
    pag.press('enter')

    p_f()


# %% [markdown]
# ### Geral

# %%
def avisar_automação():

    #avisa que vai começar a automação
    pag.alert('A automação vai começar, aperte em OK e NÃO mexa em nada! Caso seja necessario cessar automação, mova o mouse para o canto da tela')

# %%
def abre_wms():
    
    pag.PAUSE = pause_geral
        
    sleep(2)
        
    # minimisa
    with pag.hold('win'):
        pag.press('m')
    
    # Seleciona WMS
    
    encontrar_tela(r'img\wms.png', 'WMS', 2, 0.8)

    # Executa WMS
    
    p_i(0.1)
    pag.press('tab')
    pag.press('tab')
    pag.press('enter')
    p_f()

    # Loguin

    sleep(7)

    encontrar_tela(r'img\usuario.png', 'Usuario', 1, 0.9)

    login = 'renan'
    senha = 134679
    
    p_i(0.1)
    sleep(1)
    pcl.copy(login)
    pag.hotkey('ctrl', 'v')
    pag.press('tab')
    pcl.copy(senha)
    pag.hotkey('ctrl', 'v')

    pag.press('tab')
    pag.press('enter')
    p_f()

# %%
def abre_app_wms(app):

    p_i(1)
    
    encontrar_tela(r'img\lupa_wms.png','lupa no wms', 1, 0.8)

    pcl.copy(app)
    
    pag.hotkey('ctrl', 'v')

    pag.press('tab')
    pag.press('enter')
    
    p_f()

# %%
def salvar_planilha(nome_arquivo, onde_fixado):
    
    sleep(5)

    p_i(0.8)

    # fechar as jantlas de donwload
    # pag.hotkey('alt', 'f4')

    # fechar aviso
    # sleep(5)
    # pag.press('enter')
    
    # tela cheia
    pag.hotkey('ctrl', 'shift', 'f1')

    # vai em salvar como
    pag.press('alt')
    pag.press('a')
    pag.press('a')
    pag.press('y')
    pag.press(onde_fixado)

    # coloca o nome do arquivo
    sleep(1)
    pcl.copy(nome_arquivo)
    pag.hotkey('ctrl', 'v')

    # salvar
    pag.press('tab', presses=7, interval=1)
    pag.press('enter')

    # confirmar subistituição
    pag.press('tab')
    pag.press('enter')

    # fechar
    sleep(5)
    pag.hotkey('alt', 'f4')
    
    p_f()

# %% [markdown]
# # Exe

# %%


# %%
# avisar_automação()
# abre_wms()

# sleep(6)

# abre_app_wms('GERENCIAMENTO')
# abre_consulta_cadastro_produto()
# baixar_cadastro_produto()

# sleep(20)
verificar_imagem_encontrada(time.time(), 1200 , r'img\gerenciamento\exel_gerado.png')
sleep(3)
134679
encontrar_tela(r'img\gerenciamento\exel_gerado.png', 'Excel', 1, 0.9)

salvar_planilha('produtos', '2')

pag.hotkey('alt', 'f4')

# %%



