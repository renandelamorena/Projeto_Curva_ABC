import pyautogui as pag
import time

def click(caminho_imagem, qnt_click):

    img = pag.locateCenterOnScreen(caminho_imagem, confidence = 0.9)

    x, y = img

    if qnt_click == 2: # duplo
        pag.doubleClick(x=x, y=y)

    if qnt_click == 1: # click normal
        pag.click(x=x, y=y)

def verificar_imagem(caminho_imagem):
    try:
        # Procura a posição da imagem na captura de tela
        posicao = pag.locateOnScreen(caminho_imagem, confidence = 0.9)

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

def verificar_imagem_encontrada(tempo_inicial, timeout, caminho_imagem, tempo_aguardar, nome_imagem):

    while time.time() - tempo_inicial < timeout:
        if verificar_imagem(caminho_imagem):
            print(f"Condição atendida imagem {nome_imagem} encontrada. Continuando com o restante do código.")
            break
        else:
            print(f"Aguardando a condição ser atendida...")
            time.sleep(tempo_aguardar)  # Aguarde antes de verificar novamente

    # Se o loop sair sem atender à condição, tratar isso como um timeout
    if time.time() - tempo_inicial >= timeout:
        print(f"Timeout: A condição demorou mais do que o limite de tempo especificado. {nome_imagem}")
        pag.alert(title='imagem não encontrada', text=f'Imagem "{nome_imagem}" não foi encontrada')