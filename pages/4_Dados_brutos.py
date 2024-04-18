import streamlit as st
import pandas as pd
from io import BytesIO
import os
import requests
import base64
import json
from datetime import datetime

st.set_page_config(
    page_title='Dados Brutos',
    layout='centered',
    page_icon=':bar-chart:'
    )
def botao_donwload(tabela_excel, nome_do_botao, nome_do_arquivo):
    #Criar um DataFrame
    df = pd.DataFrame(tabela_excel)

    #Criar um buffer de bytes para armazenar o Excel em memória
    output = BytesIO()

    #Criar um objeto Excel a partir do DataFrame
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Sheet1', index=False)

    #Configurar o buffer para leitura
    output.seek(0)

    #Adicionar o botão de download
    st.download_button(label = nome_do_botao,
                        data = output.getvalue(),
                        file_name = nome_do_arquivo,
                        mime = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                        )
    
def caminho_absoluto(caminho_relativo_com_barras_normais):
    
    caminho_base = os.getcwd()

    caminho_absoluto = os.path.join(caminho_base, caminho_relativo_com_barras_normais)

    return caminho_absoluto

situacao_final = pd.read_csv(caminho_absoluto('data/tratamento_curva_abc/dados_tratados/csv/situacao_final.csv'))

# with st.sidebar:
#     st.markdown('# Filtros')

#     with st.expander('Curvas'):
#         frac_toggle = st.toggle('Fracionado', value=True)
#         cx_toggle = st.toggle('Caixa Fechada', value=True)
#         geral_toggle = st.toggle('Geral', value=True)
    
#     with st.expander('Colunas'):
#         itens_permite_frac = situacao_final['Permite Frac.'].unique()
#         opcoes_permite_frac = st.multiselect('Permite fracionado na caixa fechada:', itens_permite_frac, itens_permite_frac)
        
#         itens_tipo = situacao_final['Tipo'].unique()
#         opcoes_tipo = st.multiselect('Tipo de endereço fracionado:', itens_tipo, itens_tipo)
        
#         itens_local = situacao_final['local'].unique()
#         opcoes_local = st.multiselect('Tipo de local de caixa fechada:', itens_local, itens_local)
   
# #Seleção curva por tipo
# if frac_toggle == False:
    
#     situacao_final.drop(['Curva Frac', 'Qtde Venda Frac', 'Dias Pedido Frac', 'Ativ.Ressupr.Frac', 'Média por dia frac'], axis='columns', inplace=True)

# if cx_toggle == False:
    
#     situacao_final.drop(['Curva Cx', 'Qtde Venda Cx', 'Dias Pedido Cx', 'Ativ.Ressupr.Cx', 'Média por dia cx'], axis='columns', inplace=True)

# if geral_toggle == False:
    
#     situacao_final.drop(['Curva Geral', 'Qtde Venda Geral', 'Dias Pedido Geral', 'Ativ.Ressupr.Geral', 'Média por dia geral'], axis='columns', inplace=True)

# #Seleção coluna de permite fracionado na caixa fechada
# selec_permite_frac = situacao_final['Permite Frac.'].isin(opcoes_permite_frac)
# situacao_final = situacao_final[selec_permite_frac]

# selec_tipo = situacao_final['Tipo'].isin(opcoes_tipo)
# situacao_final = situacao_final[selec_tipo]

# selec_local = situacao_final['local'].isin(opcoes_local)
# situacao_final = situacao_final[selec_local]

# with st.expander('Situação final - Dados Brutos'):
#     st.dataframe(situacao_final)

st.title('Atualização dos Dados')

# Autenticação com o GitHub
github_token = st.text_input('Token de acesso pessoal do GitHub', type='password')
repo_owner = 'renandelamorena'
repo_name = 'projeto_curva_ABC'
folder_path = 'data/tratamento_curva_abc/datasets/csv/'

horario = datetime.today().strftime('%d/%m/%Y - %H:%M')

commit_message = f'Atualização dos dados brutos - {horario}'

# Definir arquivos padrão e suas respectivas primeiras linhas desejadas
default_files_curva_cadastro = {
    'curva_frac' : caminho_absoluto('data/tratamento_curva_abc/datasets/curva_frac.xlsx'),
    'curva_cx' : caminho_absoluto('data/tratamento_curva_abc/datasets/curva_cx.xlsx'),
    'curva_geral' : caminho_absoluto('data/tratamento_curva_abc/datasets/curva_geral.xlsx'),
    'produtos' : caminho_absoluto('data/tratamento_curva_abc/datasets/produtos.xlsx'),
}

default_files_metricas = {
    'fracionado' : caminho_absoluto('data/tratamento_curva_abc/datasets/fracionado.xlsx'),
    'armazenagens' : caminho_absoluto('data/tratamento_curva_abc/datasets/armazenagens.xlsx'),
    'armazenagem_estoque' : caminho_absoluto('data/tratamento_curva_abc/datasets/armazenagem_estoque.xlsx'),
}

# Função para verificar os arquivos carregados
def check_files(uploaded_files):
    
    if selec_tipo_atualizacao_cadastro == 'Dados da curva e/ou cadastros':
        default_files = default_files_curva_cadastro
    else:
        default_files = default_files_metricas
        
    error_messages = []
    valid_files = []
    for uploaded_file in uploaded_files:
        file_name = uploaded_file.name
        file_type = None
        for key in default_files:
            if key.lower() in file_name.lower():
                file_type = key
                break
        if file_type:
            try:
                uploaded_df = pd.read_excel(uploaded_file)
                default_df = pd.read_excel(default_files[file_type])
                if not uploaded_df.columns.equals(default_df.columns):
                    error_messages.append(f'Arquivo {file_name} não corresponde ao arquivo padrão {file_type} ou suas colunas estão incorretas.')
                else:
                    valid_files.append(uploaded_file)
            except Exception as e:
                error_messages.append(f'Erro ao processar arquivo {file_name}: {str(e)}')
        else:
            error_messages.append(f'Tipo de arquivo {file_name} não reconhecido.')
    
    return valid_files, error_messages

# Função para preparar e codificar os arquivos em Base64
def prepare_and_encode_files(uploaded_files):
    files_to_commit = {}
    for uploaded_file in uploaded_files:
        # Ler o arquivo Excel e converter para DataFrame
        df = pd.read_excel(uploaded_file)
        
        # Converter o DataFrame para CSV (em memória, sem salvar no disco)
        csv_content = df.to_csv(index=False)
        
        # Codificar o conteúdo CSV em Base64
        encoded_content = base64.b64encode(csv_content.encode()).decode('utf-8')
        files_to_commit[uploaded_file.name.replace('.xlsx', '.csv')] = encoded_content
    
    return files_to_commit

# Função para fazer commit no GitHub
def commit_to_github(token, repo_owner, repo_name, commit_message, files_to_commit):
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{folder_path}'
    
    for file_name, encoded_content in files_to_commit.items():
        full_url = f'{url}{file_name}'
        response = requests.get(full_url, headers=headers)
        
        file_data = {
            'message': commit_message,
            'content': encoded_content,
            'branch': 'main',  # Ajuste conforme necessário
        }
        
        if response.status_code == 200:
            file_data['sha'] = response.json()['sha']
        
        response = requests.put(full_url, headers=headers, data=json.dumps(file_data))
        
        if response.status_code not in [200, 201]:
            st.error(f'Erro ao enviar arquivo {file_name} para o GitHub: {response.json()}')
            return
        
    st.success('Todos os arquivos foram enviados com sucesso para o GitHub!')

selec_tipo_atualizacao_cadastro = st.radio('Selecione os Dados', ['Dados da curva e/ou cadastros', 'Dados das métricas'])

uploaded_files = st.file_uploader('Escolha os arquivos .xlsx para upload', type='xlsx', accept_multiple_files=True)

if uploaded_files:
    valid_files, error_messages = check_files(uploaded_files)
    if error_messages:
        for error in error_messages:
            st.error(error)
    else:
        if selec_tipo_atualizacao_cadastro == 'Dados da curva e/ou cadastros':
            if len(valid_files) == 4:
                    
                # Tratar os dados da curva e cadastro
                produtos = pd.read_excel(valid_files[3])

                curva_geral = pd.read_excel(valid_files[2])

                curva_frac = pd.read_excel(valid_files[1])

                curva_cx = pd.read_excel(valid_files[0])
                # # Tratando Dados
                # # Funções

                def tratar_codigos(dfs):
                    
                    for df in dfs:
                        
                        df['Código'] = df['Código'].astype(str)

                        df['Código'] = df['Código'].str.slice(start=2)
                        df['Código'] = df['Código'].str.lstrip('0')

                    return df

                def refatorar_indice(df, nome_index):
                    
                    qnt_linha = df.shape[0] + 1

                    index = [i for i in range(1, qnt_linha)]

                    df.set_index(pd.Index(index), inplace=True)

                    df.index.name = nome_index
                    
                    return df

                def procurar(df, coluna, oque):
                    
                    selecao = df[coluna] == oque
                    
                    return df[selecao]
                # ## Tratamento cadastro produtos

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
                #  ## Tratamento Curvas
                # ### Geral

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
                # ### Fracionado

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
                # Caixa Fechada

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
                # Tratando códigos

                dfs = [curva_geral, curva_frac, curva_cx, produtos]
                tratar_codigos(dfs)
                # Juntando as informações
                # Fracionado

                curva_abc_frac = pd.merge(curva_frac, produtos, on='Código', how='outer')

                curva_abc_frac['Código'] = pd.to_numeric(curva_abc_frac['Código'])

                curva_abc_frac['Ender.Fracionado'] = curva_abc_frac['Ender.Fracionado'].astype(str)

                refatorar_indice(curva_abc_frac, 'Ordem')

                # Caixa Fechada

                curva_abc_cx = pd.merge(curva_cx, produtos, on='Código', how='outer')

                curva_abc_cx['Código'] = pd.to_numeric(curva_abc_cx['Código'])

                curva_abc_cx['Ender.Fracionado'] = curva_abc_cx['Ender.Fracionado'].astype(str)

                refatorar_indice(curva_abc_cx, 'Ordem')

                # ### Geral

                curva_abc_geral = pd.merge(curva_geral, produtos, on='Código', how='outer')

                curva_abc_geral['Código'] = pd.to_numeric(curva_abc_geral['Código'])

                curva_abc_geral['Ender.Fracionado'] = curva_abc_geral['Ender.Fracionado'].astype(str)

                refatorar_indice(curva_abc_geral, 'Ordem')

                # ### Situação Final

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
                # Tratando NaN
                situacao_final['Descrição'] = situacao_final['Descrição'].fillna('-')
                
                enderecos = situacao_final[['Ender.Cx.Fechada']].astype(str)

                locais = pd.read_excel(caminho_absoluto('data/analise_curva_abc/local/datasets/local_apanha_cx.xlsx')).astype(str)

                enderecos_x_locais = pd.merge(enderecos, locais)

                total_enderecos_usados = enderecos.drop_duplicates()

                item_com_end = ~(enderecos['Ender.Cx.Fechada'] == 'nan')

                situacao_final = pd.merge(situacao_final, enderecos_x_locais, how = 'left')

                situacao_final.drop_duplicates(inplace = True)
                situacao_final.sort_values(by='Qtde Venda Frac', ascending=False, inplace=True)
                
                situacao_final = refatorar_indice(situacao_final, 'Ordem')

                # Converter o DataFrame para CSV (em memória, sem salvar no disco)
                csv_content = situacao_final.to_csv(index=False)
                # Codificar o conteúdo CSV em Base64
                encoded_content = base64.b64encode(csv_content.encode()).decode('utf-8')

                files_to_commit = {'situacao_final.csv' : encoded_content}
                                
                folder_path = 'data/tratamento_curva_abc/dados_tratados/csv/'
                
                st.success('Dados tratados!!!')
                    
            else:
                files_to_commit = prepare_and_encode_files(valid_files)
                st.error('Ainda há arquivos faltantes para trartar os dados!')            

        else:
            files_to_commit = prepare_and_encode_files(valid_files)

        if st.button('Enviar Dados'):
            commit_to_github(github_token, repo_owner, repo_name, commit_message, files_to_commit)