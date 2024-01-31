# %% [markdown]
# # Imports

# %%
import pyautogui as pag
import pyperclip as pcl
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta

import pandas as pd
import os

# %%
#define pause geral
pause_geral = 2
pag.PAUSE = pause_geral

#pause personalizado

def p_i(pause):
    pag.PAUSE = pause
    
def p_f():
    pag.PAUSE = pause_geral

# %%
def caminho_absoluto(caminho_relativo_com_barras_normais):
    
    caminho_base = os.getcwd()

    caminho_absoluto = os.path.join(caminho_base, caminho_relativo_com_barras_normais)

    return caminho_absoluto

# %% [markdown]
# ## Func

# %% [markdown]
# ### Data

# %%
def colar_data_1_ano_atras():

    data_atual = datetime.now()

    data_um_ano_atras = data_atual - relativedelta(years=1)

    dia_1_ano_atras = data_um_ano_atras.day
    mes_1_ano_atras = data_um_ano_atras.month
    ano_1_ano_atras = data_um_ano_atras.year

    if dia_1_ano_atras < 10:
        dia_1_ano_atras = '0' + str(dia_1_ano_atras)

    if mes_1_ano_atras < 10:
        mes_1_ano_atras = '0' + str(mes_1_ano_atras)

    p_i(0.5)
    pcl.copy(dia_1_ano_atras)
    pag.hotkey('ctrl', 'v')
    pcl.copy(mes_1_ano_atras)
    pag.hotkey('ctrl', 'v')
    pcl.copy(ano_1_ano_atras)
    pag.hotkey('ctrl', 'v')
    p_f()

# %%
def colar_data_3_meses_atras():

    data_atual = datetime.now()

    data_tres_meses_atras = data_atual - relativedelta(months=3)

    dia_3_meses_atras = data_tres_meses_atras.day
    mes_3_meses_atras = data_tres_meses_atras.month
    ano_3_meses_atras = data_tres_meses_atras.year

    if dia_3_meses_atras < 10:
        dia_3_meses_atras = '0' + str(dia_3_meses_atras)

    if mes_3_meses_atras < 10:
        mes_3_meses_atras = '0' + str(mes_3_meses_atras)

    p_i(0.5)
    pcl.copy(dia_3_meses_atras)
    pag.hotkey('ctrl', 'v')
    pcl.copy(mes_3_meses_atras)
    pag.hotkey('ctrl', 'v')
    pcl.copy(ano_3_meses_atras)
    pag.hotkey('ctrl', 'v')
    p_f()

# %% [markdown]
# ### Verifica tela

# %%
def click(caminho_imagem, qnt_click):

    img = pag.locateCenterOnScreen(caminho_imagem, confidence = 0.9)

    x, y = img

    if qnt_click == 2: # duplo
        pag.doubleClick(x=x, y=y)

    if qnt_click == 1: # click normal
        pag.click(x=x, y=y)

# %%
# Função para verificar se a imagem está presente na tela
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

def verificar_imagem_encontrada(tempo_inicial, timeout, caminho_imagem, tempo_aguardar):

    while time.time() - tempo_inicial < timeout:
        if verificar_imagem(caminho_imagem):
            print("Condição atendida. Continuando com o restante do código.")
            break
        else:
            print("Aguardando a condição ser atendida...")
            time.sleep(tempo_aguardar)  # Aguarde antes de verificar novamente

    # Se o loop sair sem atender à condição, tratar isso como um timeout
    if time.time() - tempo_inicial >= timeout:
        print("Timeout: A condição demorou mais do que o limite de tempo especificado.")

# %% [markdown]
# ### Gerenciamento

# %%
def abre_consulta_cadastro_produto():

    verificar_imagem_encontrada(time.time(), 10, caminho_absoluto('img/gerenciamento/gerenciamento.png'), 0.2)
    
    verificar_imagem_encontrada(time.time(), 10, caminho_absoluto('img/gerenciamento/consultas.png'), 0.2)
    click(caminho_absoluto('img/gerenciamento/consultas.png'), 1)

    verificar_imagem_encontrada(time.time(), 10, caminho_absoluto('img/gerenciamento/consulta_cadastro_endereco_apanha.png'), 0.2)
    click(caminho_absoluto('img/gerenciamento/consulta_cadastro_endereco_apanha.png'), 1)

# %%
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

    verificar_imagem_encontrada(time.time(), 10, caminho_absoluto('img/excel/botao_gerar_excel.png'), 0.2)
    click(caminho_absoluto('img\excel\botao_gerar_excel.png'), 1)

    p_f()

# %%
def abre_consulta_analise_curva():

    verificar_imagem_encontrada(time.time(), 10, r'img\gerenciamento\consultas.png', 0.2)
    click(r'img\gerenciamento\consultas.png', 1)

    verificar_imagem_encontrada(time.time(), 10, r'img\gerenciamento\analise_curva_abc.png', 0.2)
    click(r'img\gerenciamento\analise_curva_abc.png', 1)

# %%
def baixar_analise_curva(tipo_curva):
    
    if tipo_curva == 'curva_geral':

        pag.press('tab', presses=2)
        pag.press('enter')

        # espera filtrar para precionar o botão
        verificar_imagem_encontrada(time.time(), 1200, caminho_absoluto('img/excel/botao_gerar_excel.png'), 5)
        click(caminho_absoluto('img/excel/botao_gerar_excel.png'), 1)

        pag.press('tab')
        pag.press('enter')

    if tipo_curva == 'curva_cx':

        verificar_imagem_encontrada(time.time(), 20, caminho_absoluto('img/gerenciamento/limpar_filtro.png'), 1)
        click(caminho_absoluto('img/gerenciamento/limpar_filtro.png'), 1)

        verificar_imagem_encontrada(time.time(), 20, caminho_absoluto('img/gerenciamento/selec_curva_cx.png'), 1)
        click(caminho_absoluto('img/gerenciamento/selec_curva_cx.png'), 1)

        pag.press('tab', presses=3)
        pag.press('enter')

        # espera filtrar para precionar o botão
        verificar_imagem_encontrada(time.time(), 1200, caminho_absoluto('img/excel/botao_gerar_excel.png'), 5)
        click(caminho_absoluto('img/excel/botao_gerar_excel.png'), 1)
        pag.press('tab')
        pag.press('enter')

    if tipo_curva == 'curva_frac':
        
        verificar_imagem_encontrada(time.time(), 20, caminho_absoluto('img/gerenciamento/limpar_filtro.png'), 1)
        click(caminho_absoluto('img/gerenciamento/limpar_filtro.png'), 1)

        verificar_imagem_encontrada(time.time(), 20, caminho_absoluto('img/gerenciamento/selec_curva_frac.png'), 1)
        click(caminho_absoluto('img/gerenciamento/selec_curva_frac.png'), 1)

        pag.press('tab', presses=3)
        pag.press('enter')

        # espera filtrar para precionar o botão
        verificar_imagem_encontrada(time.time(), 1200, caminho_absoluto('img/excel/botao_gerar_excel.png'), 5)
        click(caminho_absoluto('img/excel/botao_gerar_excel.png'), 1)
        pag.press('tab')
        pag.press('enter')

# %% [markdown]
# ### Geral

# %%
def avisar_automação():

    #avisa que vai começar a automação
    pag.alert('A automação vai começar, aperte em OK e NÃO mexa em nada! Caso seja necessario cessar automação, mova o mouse para o canto da tela')

# %%
def abre_wms():
    
    pag.PAUSE = pause_geral
    
    p_i(0.2)
    # minimisa
    with pag.hold('win'):
        pag.press('m')

    pag.press('win')
    pcl.copy('wms')
    pag.hotkey('ctrl', 'v')
    p_f()

    verificar_imagem_encontrada(time.time(), 10, caminho_absoluto('img/aplicativos.png'), 0.2)
    click(caminho_absoluto('img/aplicativos.png'), 1)
    
    # Seleciona WMS
    
    verificar_imagem_encontrada(time.time(), 10, caminho_absoluto('img/wms.png'), 0.2)
    click(caminho_absoluto('img/wms.png'), 1)

    # Executa WMS
    
    verificar_imagem_encontrada(time.time(), 10, caminho_absoluto('img/executar.png'), 0.2)
    click(caminho_absoluto('img/executar.png'), 1)

    # Loguin

    verificar_imagem_encontrada(time.time(), 10, caminho_absoluto('img/usuario.png'), 0.2)
    click(caminho_absoluto('img/usuario.png'), 1)

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

# %%
def abre_app_wms(app):

    p_i(0.1)
    
    verificar_imagem_encontrada(time.time(), 10, caminho_absoluto('img/lupa_wms.png'), 0.2)
    click(caminho_absoluto('img/lupa_wms.png'), 1)

    pcl.copy(app)
    
    pag.hotkey('ctrl', 'v')

    pag.press('tab')
    pag.press('enter')
    
    p_f()

# %%
def salvar_planilha(nome_arquivo, onde_fixado):
    
    # click no excel
    verificar_imagem_encontrada(time.time(), 1200 , caminho_absoluto('img/gerenciamento/exel_gerado.png'), 5)
    click(caminho_absoluto('img/gerenciamento/exel_gerado.png'), 1)  

    # tela cheia
    pag.hotkey('ctrl', 'shift', 'f1')
    pag.hotkey('ctrl', 'shift', 'f1')

    # vai em salvar como
    p_i(0.4)
    pag.press('alt')
    pag.press('a')
    pag.press('a')
    pag.press('y')
    pag.press('1')
    pag.press('y')
    pag.press(onde_fixado)

    # coloca o nome do arquivo
    verificar_imagem_encontrada(time.time(), 20 , caminho_absoluto('img/excel/nome_arquivo.png'), 0.1)
    click(caminho_absoluto('img/excel/nome_arquivo.png'), 2)
    pcl.copy(nome_arquivo)
    pag.hotkey('ctrl', 'v')

    # salvar
    verificar_imagem_encontrada(time.time(), 20 , caminho_absoluto('img/excel/salvar_excel.png'), 0.1)
    click(caminho_absoluto('img/excel/salvar_excel.png'), 1)

    # confirmar subistituição
    pag.press('tab')
    pag.press('enter')

    # fechar
    pag.hotkey('alt', 'f4')
    
    p_f()

# %%
def comitar_dados_atualizados():

    p_i(0.2)
    # minimisa
    with pag.hold('win'):
        pag.press('m')

    # abrir vscode
    pag.press('win')
    pcl.copy('vscode')
    pag.hotkey('ctrl', 'v')
    p_f()

    verificar_imagem_encontrada(time.time(), 10, caminho_absoluto('img/aplicativos.png'), 0.2)
    click(caminho_absoluto('img/aplicativos.png'), 1)

    verificar_imagem_encontrada(time.time(), 20 , caminho_absoluto('img/vscode/vscode.png'), 0.1)
    click(caminho_absoluto('img/vscode/vscode.png'), 1)

    # abre nova janela
    pag.hotkey('ctrl', 'shift', 'n')

    # abre sorce control
    pag.hotkey('ctrl', 'shift', 'g')

    # abrir pasta
    verificar_imagem_encontrada(time.time(), 20 , caminho_absoluto('img/vscode/abrir_pasta.png'), 0.1)
    click(caminho_absoluto('img/vscode/abrir_pasta.png'), 1)

    pcl.copy(r'C:\Users\estoque\OneDrive - MAXIFARMA DISTRIBUIDORA DE MEDICAMENTOS LTDA\Documentos\estoque.renan\projetos\projeto_curva_abc')
    pag.hotkey('ctrl', 'v')

    pag.press('tab')
    pag.press('enter')

    # abre sorce control
    pag.hotkey('ctrl', 'shift', 'g')

    # click na caixa de mensagem do commit
    verificar_imagem_encontrada(time.time(), 20 , caminho_absoluto('img/vscode/mensagem_do_commit.png'), 0.1)
    click(caminho_absoluto('img/vscode/mensagem_do_commit.png'), 1)

    pcl.copy('atualizando cadastro de hoje')
    pag.hotkey('ctrl', 'v')

    # click em mudandanças
    verificar_imagem_encontrada(time.time(), 20 , caminho_absoluto('img/vscode/mudancas.png'), 0.1)
    click(caminho_absoluto('img/vscode/mudancas.png'), 1)

    # click em adicionar mudanças
    verificar_imagem_encontrada(time.time(), 20 , caminho_absoluto('img/vscode/stage_all_changens.png'), 0.1)
    click(caminho_absoluto('img/vscode/stage_all_changens.png'), 1)

    # click em configurações do commit
    verificar_imagem_encontrada(time.time(), 20 , caminho_absoluto('img/vscode/config.png'), 0.1)
    click(caminho_absoluto('img/vscode/config.png'), 1)

    # click em commitar e sincronizar
    verificar_imagem_encontrada(time.time(), 20 , caminho_absoluto('img/vscode/comitar_e_sincronizar.png'), 0.1)
    click(caminho_absoluto('img/vscode/comitar_e_sincronizar.png'), 1)

    # click em ok
    verificar_imagem_encontrada(time.time(), 20 , caminho_absoluto('img/vscode/ok.png'), 0.1)
    click(caminho_absoluto('img/vscode/ok.png'), 1)

# %% [markdown]
# # Tratamento de dados

# %%
def tratar_dados():

    # Importando Bibliotecas

    pd.set_option('display.max_columns', None)

    # Importando Dados

    produtos = pd.read_excel(caminho_absoluto('../data/tratamento_curva_abc/datasets/produtos.xlsx'))

    curva_geral = pd.read_excel(caminho_absoluto('../data/tratamento_curva_abc/datasets/curva_geral.xlsx'))

    curva_cx = pd.read_excel(caminho_absoluto('../data/tratamento_curva_abc/datasets/curva_cx.xlsx'))

    curva_frac = pd.read_excel(caminho_absoluto('../data/tratamento_curva_abc/datasets/curva_frac.xlsx'))

    # Tratando Dados

    # Funções

    def tratar_codigos(dfs):
        
        for df in dfs:
            
            df['Código'] = df['Código'].astype(str)

            df['Código'] = df['Código'].str.slice(start=2)
            df['Código'] = df['Código'].str.lstrip('0')

        return df

    def refatorar_indece(df, nome_index):
        
        qnt_linha = df.shape[0] + 1

        index = [i for i in range(1, qnt_linha)]

        df.set_index(pd.Index(index), inplace=True)

        df.index.name = nome_index
        
        return df

    def procurar(df, coluna, oque):
        
        selecao = df[coluna] == oque
        
        return df[selecao]

    ## Tratamento cadastro produtos

    # Excluir linhas vazias
    produtos = produtos.dropna(how='all')

    # Selecionando somente as principais colunas
    produtos = produtos[['Código',
                        'Descrição',
                        'Estoque Armaz.',
                        'Apanha',
                        'Permite Frac.',
                        'Ender.Cx.Fechada',
                        'Embal.',
                        'Capacidade',
                        'Estoque',
                        'Apanha.1',
                        'Ender.Fracionado',
                        'Tipo',
                        'Capacidade.1',
                        'Estoque.1'
                        ]]

    # Renomear colunas de geral
    renomear_produtos = {'Apanha.1' : 'Apanha Frac',
                        'Apanha' : 'Apanha Cx',
                        'Capacidade.1' : 'Capacidade Frac',
                        'Capacidade' : 'Capacidade Cx',
                        'Estoque.1' : 'Estoque Frac',
                        'Estoque' : 'Estoque Cx'
                    }

    produtos.rename(columns = renomear_produtos, inplace = True)

    ## Tratamento Curvas

    ### Geral

    # Excluir linhas vazias
    curva_geral = curva_geral.dropna(how='all')

    # Selecionando somente as principais colunas
    curva_geral = curva_geral[['Cód.Produto', 'Curva', 'Qtde Venda', 'Dias Pedido', 'Média por dia', 'Ativ.Ressupr.']]

    # Renomear colunas de geral
    renomear_geral = {'Cód.Produto' : 'Código',
                    'Curva' : 'Curva Geral',
                    'Qtde Venda' : 'Qtde Venda Geral',
                    'Dias Pedido' : 'Dias Pedido Geral',
                    'Média por dia' : 'Média por dia geral',
                    'Ativ.Ressupr.' : 'Ativ.Ressupr.Geral',
                    }

    curva_geral.rename(columns = renomear_geral, inplace = True)

    ### Fracionado

    # Excluir linhas vazias
    curva_frac = curva_frac.dropna(how='all')

    # Selecionando somente as principais colunas
    curva_frac = curva_frac[['Cód.Produto', 'Curva', 'Qtde Venda', 'Dias Pedido', 'Média por dia', 'Ativ.Ressupr.', 'Qtde Desvio Picking']]

    # Renomear colunas de frac
    renomear_frac = {'Cód.Produto' : 'Código',
                'Curva' : 'Curva Frac',
                'Qtde Venda' : 'Qtde Venda Frac',
                'Dias Pedido' : 'Dias Pedido Frac',
                'Média por dia' : 'Média por dia frac',
                'Ativ.Ressupr.' : 'Ativ.Ressupr.Frac',
                }

    curva_frac.rename(columns = renomear_frac, inplace = True)

    # ### Caixa Fechada

    # Excluir linhas vazias
    curva_cx = curva_cx.dropna(how='all')

    # Selecionando somente as principais colunas
    curva_cx = curva_cx[['Cód.Produto', 'Curva', 'Qtde Venda', 'Dias Pedido', 'Média por dia', 'Ativ.Ressupr.']]

    # Renomear colunas de cx
    renomear_cx = {'Cód.Produto' : 'Código',
                'Curva' : 'Curva Cx',
                'Qtde Venda' : 'Qtde Venda Cx',
                'Dias Pedido' : 'Dias Pedido Cx',
                'Média por dia' : 'Média por dia cx',
                'Ativ.Ressupr.' : 'Ativ.Ressupr.Cx',
                }

    curva_cx.rename(columns = renomear_cx, inplace = True)

    ## Tratando códigos

    dfs = [curva_geral, curva_frac, curva_cx, produtos]
    tratar_codigos(dfs)

    ## Juntando as informações

    ### Fracionado

    curva_abc_frac = pd.merge(curva_frac, produtos, on='Código', how='outer')

    curva_abc_frac['Código'] = pd.to_numeric(curva_abc_frac['Código'])

    curva_abc_frac['Ender.Fracionado'] = curva_abc_frac['Ender.Fracionado'].astype(str)

    refatorar_indece(curva_abc_frac, 'Ordem')

    ### Caixa Fechada

    curva_abc_cx = pd.merge(curva_cx, produtos, on='Código', how='outer')

    curva_abc_cx['Código'] = pd.to_numeric(curva_abc_cx['Código'])

    curva_abc_cx['Ender.Fracionado'] = curva_abc_cx['Ender.Fracionado'].astype(str)

    refatorar_indece(curva_abc_cx, 'Ordem')

    ### Geral

    curva_abc_geral = pd.merge(curva_geral, produtos, on='Código', how='outer')

    curva_abc_geral['Código'] = pd.to_numeric(curva_abc_geral['Código'])

    curva_abc_geral['Ender.Fracionado'] = curva_abc_geral['Ender.Fracionado'].astype(str)

    refatorar_indece(curva_abc_geral, 'Ordem')

    ### Situação Final

    situacao_final = pd.merge(curva_geral, produtos, on='Código', how='outer')

    situacao_final['Código'] = pd.to_numeric(situacao_final['Código'])

    situacao_final['Ender.Fracionado'] = situacao_final['Ender.Fracionado'].astype(str)

    # Juntando a curva geral com a cx fech e fracionada
    curva_cx_final = curva_cx[['Código', 'Curva Cx', 'Qtde Venda Cx', 'Dias Pedido Cx', 'Média por dia cx', 'Ativ.Ressupr.Cx']]
    curva_frac_final = curva_frac[['Código', 'Curva Frac', 'Qtde Venda Frac', 'Dias Pedido Frac', 'Média por dia frac', 'Ativ.Ressupr.Frac', 'Qtde Desvio Picking']]

    situacao_final['Código'] = situacao_final['Código'].astype(str)
    situacao_final = pd.merge(situacao_final, curva_cx_final, on='Código', how='outer')

    situacao_final['Código'] = situacao_final['Código'].astype(str)
    situacao_final = pd.merge(situacao_final, curva_frac_final, on='Código', how='outer')

    situacao_final['Código'] = pd.to_numeric(situacao_final['Código'])

    situacao_final.drop_duplicates(subset=['Código'], keep='last', inplace=True)

    refatorar_indece(situacao_final, 'Ordem')

    # # Organizando colunas

    # Organizar as colunas curva geral

    curva_abc_geral = curva_abc_geral[['Código', 
                                    'Descrição', 
                                    'Curva Geral', 
                                    'Qtde Venda Geral', 
                                    'Dias Pedido Geral', 
                                    'Ativ.Ressupr.Geral',
                                    'Média por dia geral',
                                    'Estoque Armaz.',
                                    'Ender.Cx.Fechada',
                                    'Estoque Cx',
                                    'Capacidade Cx',
                                    'Embal.',
                                    'Permite Frac.',
                                    'Ender.Fracionado',
                                    'Capacidade Frac',
                                    'Estoque Frac',
                                    'Tipo',
                                    ]]

    # Organizar as colunas curva frac

    curva_abc_frac = curva_abc_frac[['Código', 
                                    'Descrição', 
                                    'Curva Frac', 
                                    'Qtde Venda Frac', 
                                    'Dias Pedido Frac', 
                                    'Ativ.Ressupr.Frac',
                                    'Média por dia frac',
                                    'Qtde Desvio Picking'
                                    ]]

    # Organizar as colunas curva cx

    curva_abc_cx = curva_abc_cx[['Código', 
                                    'Descrição', 
                                    'Curva Cx', 
                                    'Qtde Venda Cx', 
                                    'Dias Pedido Cx',
                                    'Ativ.Ressupr.Cx',
                                    'Média por dia cx',
                                    'Permite Frac.',
                                    ]]

    # Organizar as colunas da situacao final

    situacao_final = situacao_final[['Código', 
                                    'Descrição', 
                                    'Curva Frac',
                                    'Curva Cx',
                                    'Curva Geral', 
                                    'Qtde Venda Frac', 
                                    'Qtde Venda Cx', 
                                    'Qtde Venda Geral', 
                                    'Dias Pedido Frac', 
                                    'Dias Pedido Cx', 
                                    'Dias Pedido Geral', 
                                    'Ativ.Ressupr.Frac',
                                    'Ativ.Ressupr.Cx',
                                    'Ativ.Ressupr.Geral',
                                    'Média por dia frac',
                                    'Média por dia cx',
                                    'Média por dia geral',
                                    'Estoque Armaz.',
                                    'Ender.Cx.Fechada',
                                    'Estoque Cx',
                                    'Capacidade Cx',
                                    'Embal.',
                                    'Estoque Frac',
                                    'Capacidade Frac',
                                    'Permite Frac.',
                                    'Ender.Fracionado',
                                    'Tipo',
                                    'Qtde Desvio Picking',
                                    ]]

    # %% [markdown]
    # ### Tratando NaN

    # %%
    curva_abc_geral['Descrição'] = curva_abc_geral['Descrição'].fillna('-')

    curva_abc_cx['Descrição'] = curva_abc_cx['Descrição'].fillna('-')

    curva_abc_frac['Descrição'] = curva_abc_frac['Descrição'].fillna('-')

    situacao_final['Descrição'] = situacao_final['Descrição'].fillna('-')

    # %%
    curva_abc_geral.to_excel(caminho_absoluto('../data/tratamento_curva_abc/dados_tratados/curva_abc_geral.xlsx'))
    curva_abc_frac.to_excel(caminho_absoluto('../data/tratamento_curva_abc/dados_tratados/curva_abc_frac.xlsx'))
    curva_abc_cx.to_excel(caminho_absoluto('../data/tratamento_curva_abc/dados_tratados/curva_abc_cx.xlsx'))
    situacao_final.to_excel(caminho_absoluto('../data/tratamento_curva_abc/dados_tratados/situacao_final.xlsx'))

    # Comparar locais

    situacao_final = pd.read_excel(caminho_absoluto('../data/tratamento_curva_abc/dados_tratados/situacao_final.xlsx'))

    enderecos = situacao_final[['Ender.Cx.Fechada']].astype(str)

    locais = pd.read_excel(caminho_absoluto('../data/analise_curva_abc/local/datasets/local_apanha_cx.xlsx')).astype(str)

    def refatorar_indece(df, nome_index):
        
        qnt_linha = df.shape[0] + 1

        index = [i for i in range(1, qnt_linha)]

        df.set_index(pd.Index(index), inplace=True)

        df.index.name = nome_index
        
        return df

    enderecos_x_locais = pd.merge(enderecos, locais)

    total_enderecos_usados = enderecos.drop_duplicates()

    item_com_end = ~(enderecos['Ender.Cx.Fechada'] == 'nan')

    teste = pd.merge(situacao_final, enderecos_x_locais, how = 'left')

    teste.drop_duplicates(inplace = True)
    teste.set_index('Ordem', inplace=True)
    teste.sort_values(by='Qtde Venda Frac', ascending=False, inplace=True)
    teste = refatorar_indece(teste, 'Ordem')

    teste.to_excel(caminho_absoluto('../data/tratamento_curva_abc/dados_tratados/situacao_final.xlsx'))

# %% [markdown]
# # Exe

# %%
abre_wms()

abre_app_wms('GERENCIAMENTO')
abre_consulta_cadastro_produto()
baixar_cadastro_produto()

salvar_planilha('produtos', '2')

time.sleep(5)
pag.hotkey('alt', 'f4')

abre_consulta_analise_curva()

colar_data_1_ano_atras()

baixar_analise_curva('curva_geral')
salvar_planilha('curva_geral', '2')

baixar_analise_curva('curva_cx')
salvar_planilha('curva_cx', '2')

baixar_analise_curva('curva_frac')
salvar_planilha('curva_frac', '2')

pag.hotkey('alt', 'f4')
pag.hotkey('alt', 'f4')
pag.hotkey('alt', 'f4')

tratar_dados()

# %%
comitar_dados_atualizados()

# %%



