import streamlit as st
import pandas as pd
from io import BytesIO
import os
import requests
import base64
import json

st.set_page_config(
    page_title='Dados Brutos',
    layout='wide',
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
                        mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
    
def caminho_absoluto(caminho_relativo_com_barras_normais):
    
    caminho_base = os.getcwd()

    caminho_absoluto = os.path.join(caminho_base, caminho_relativo_com_barras_normais)

    return caminho_absoluto

# Streamlit

st.title('Dados brutos')

situacao_final = pd.read_excel(caminho_absoluto('data/tratamento_curva_abc/dados_tratados/situacao_final.xlsx')).set_index('Ordem')

with st.sidebar:
    st.markdown('# Filtros')

    with st.expander('Curvas'):
        frac_toggle = st.toggle('Fracionado', value=True)
        cx_toggle = st.toggle('Caixa Fechada', value=True)
        geral_toggle = st.toggle('Geral', value=True)
    
    with st.expander('Colunas'):
        itens_permite_frac = situacao_final['Permite Frac.'].unique()
        opcoes_permite_frac = st.multiselect('Permite fracionado na caixa fechada:', itens_permite_frac, itens_permite_frac)
        
        itens_tipo = situacao_final['Tipo'].unique()
        opcoes_tipo = st.multiselect('Tipo de endereço fracionado:', itens_tipo, itens_tipo)
        
        itens_local = situacao_final['local'].unique()
        opcoes_local = st.multiselect('Tipo de local de caixa fechada:', itens_local, itens_local)
   
#Seleção curva por tipo
if frac_toggle == False:
    
    situacao_final.drop(['Curva Frac', 'Qtde Venda Frac', 'Dias Pedido Frac', 'Ativ.Ressupr.Frac', 'Média por dia frac'], axis='columns', inplace=True)

if cx_toggle == False:
    
    situacao_final.drop(['Curva Cx', 'Qtde Venda Cx', 'Dias Pedido Cx', 'Ativ.Ressupr.Cx', 'Média por dia cx'], axis='columns', inplace=True)

if geral_toggle == False:
    
    situacao_final.drop(['Curva Geral', 'Qtde Venda Geral', 'Dias Pedido Geral', 'Ativ.Ressupr.Geral', 'Média por dia geral'], axis='columns', inplace=True)

#Seleção coluna de permite fracionado na caixa fechada
selec_permite_frac = situacao_final['Permite Frac.'].isin(opcoes_permite_frac)
situacao_final = situacao_final[selec_permite_frac]

selec_tipo = situacao_final['Tipo'].isin(opcoes_tipo)
situacao_final = situacao_final[selec_tipo]

selec_local = situacao_final['local'].isin(opcoes_local)
situacao_final = situacao_final[selec_local]

with st.expander('Situação final - Dados Brutos'):
    st.dataframe(situacao_final)

# Interface Streamlit
st.title("Atualização dos dados brutos")

# Autenticação com o GitHub
github_token = st.text_input("Token de acesso pessoal do GitHub", type="password")
repo_owner = 'renandelamorena'
repo_name = 'projeto_curva_ABC'
folder_path = 'data/tratamento_curva_abc/datasets/'
commit_message = 'Atualização dos dados brutos de hoje'

# Definir arquivos padrão e suas respectivas primeiras linhas desejadas
default_files = {
    "curva_frac" : caminho_absoluto('data/tratamento_curva_abc/datasets/curva_frac.xlsx'),
    "curva_cx" : caminho_absoluto('data/tratamento_curva_abc/datasets/curva_cx.xlsx'),
    "curva_geral" : caminho_absoluto('data/tratamento_curva_abc/datasets/curva_geral.xlsx'),
    "produtos" : caminho_absoluto('data/tratamento_curva_abc/datasets/produtos.xlsx'),
    "fracionado" : caminho_absoluto('data/tratamento_curva_abc/datasets/fracionado.xlsx'),
    "armazenagens" : caminho_absoluto('data/tratamento_curva_abc/datasets/armazenagens.xlsx'),
    "armazenagens_estoque" : caminho_absoluto('data/tratamento_curva_abc/datasets/armazenagens_estoque.xlsx'),
}

# Função para verificar os arquivos carregados
def check_files(uploaded_files):
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
                    error_messages.append(f"Arquivo {file_name} não corresponde ao arquivo padrão {file_type} ou suas colunas estão incorretas.")
                else:
                    valid_files.append(uploaded_file)
            except Exception as e:
                error_messages.append(f"Erro ao processar arquivo {file_name}: {str(e)}")
        else:
            error_messages.append(f"Tipo de arquivo {file_name} não reconhecido.")
    
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
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{folder_path}"
    
    for file_name, encoded_content in files_to_commit.items():
        full_url = f"{url}{file_name}"
        response = requests.get(full_url, headers=headers)
        
        file_data = {
            "message": commit_message,
            "content": encoded_content,
            "branch": "main",  # Ajuste conforme necessário
        }
        
        if response.status_code == 200:
            file_data["sha"] = response.json()["sha"]
        
        response = requests.put(full_url, headers=headers, data=json.dumps(file_data))
        
        if response.status_code not in [200, 201]:
            st.error(f"Erro ao enviar arquivo {file_name} para o GitHub: {response.json()}")
            return
        
    st.success("Todos os arquivos foram enviados com sucesso para o GitHub!")

# Interface Streamlit
st.title("Atualização de Dados")
uploaded_files = st.file_uploader("Escolha os arquivos .xlsx para upload", type="xlsx", accept_multiple_files=True)

if uploaded_files:
    valid_files, error_messages = check_files(uploaded_files)
    if error_messages:
        for error in error_messages:
            st.error(error)
    else:
        files_to_commit = prepare_and_encode_files(valid_files)
        commit_message = "Atualização dos dados via Streamlit"
        if st.button("Enviar para o GitHub"):
            commit_to_github(github_token, repo_owner, repo_name, commit_message, files_to_commit)