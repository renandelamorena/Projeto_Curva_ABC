import streamlit as st
import pandas as pd
from io import BytesIO
import os
import requests

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

# Função para verificar se os arquivos carregados correspondem aos arquivos padrões
def check_files(uploaded_files):
    for uploaded_file in uploaded_files:
        file_name = uploaded_file.name
        
        # Identificar o tipo do arquivo carregado com base no nome
        file_type = None
        for key, value in default_files.items():
            if key.lower() in file_name.lower():
                file_type = key
                break
        
        # Se o tipo do arquivo for identificado
        if file_type:
            # Ler o arquivo .xlsx carregado
            uploaded_df = pd.read_excel(uploaded_file)
            
            # Ler o arquivo padrão correspondente
            default_file_path = default_files[file_type]
            default_df = pd.read_excel(default_file_path)
            
            # Verificar se a primeira linha do arquivo carregado é igual à do arquivo padrão
            if not uploaded_df.iloc[0].equals(default_df.iloc[0]):
                return f"Arquivo {file_name} não corresponde ao arquivo padrão {file_type} ou sua primeira linha está incorreta."
        else:
            return f"Tipo de arquivo {file_name} não reconhecido."
    
    return None

# Função para autenticar e fazer commit no GitHub
def commit_to_github(token, repo_owner, repo_name, commit_message, files_to_commit):
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/"
    
    for file_path, file_content in files_to_commit.items():
        # Verificar se o arquivo já existe no repositório
        response = requests.get(url + file_path, headers=headers)
        
        if response.status_code == 200:
            # Atualizar o arquivo existente
            file_data = {
                "message": commit_message,
                "content": file_content,
                "sha": response.json()["sha"]
            }
        else:
            # Criar um novo arquivo
            file_data = {
                "message": commit_message,
                "content": file_content
            }
        
        # Fazer a requisição para criar ou atualizar o arquivo
        response = requests.put(url + file_path, headers=headers, json=file_data)
        
        if response.status_code != 200 and response.status_code != 201:
            return f"Erro ao enviar arquivo {file_path} para o GitHub."
    
    return "Arquivos enviados com sucesso para o GitHub!"

# Interface Streamlit
st.title("Atualização dos dados brutos")

# Autenticação com o GitHub
github_token = st.text_input("Token de acesso pessoal do GitHub", type="password")
repo_owner = st.text_input("Proprietário do repositório (username)", value="renandelamorena")
repo_name = st.text_input("Nome do repositório", value="projeto_curva_ABC")
commit_message = st.text_input("Mensagem do commit", value="Atualização dos dados brutos de hoje")

# Definir arquivos padrão e suas respectivas primeiras linhas desejadas
default_files = {
    "Curva fracionada" : caminho_absoluto('data/tratamento_curva_abc/datasets/curva_frac.xlsx'),
    "Curva de Caixa" : caminho_absoluto('data/tratamento_curva_abc/datasets/curva_cx.xlsx'),
    "Curva Geral" : caminho_absoluto('data/tratamento_curva_abc/datasets/curva_geral.xlsx'),
    "Cadastro de Produtos" : caminho_absoluto('data/tratamento_curva_abc/datasets/produtos.xlsx'),
}

# Carregar arquivos .xlsx
uploaded_files = st.file_uploader("Escolha os arquivos .xlsx para upload", type="xlsx", accept_multiple_files=True)

if uploaded_files:
    check_result = check_files(uploaded_files)
    
    if check_result is None:
        st.success("Arquivos carregados correspondem aos arquivos padrões.")
        
        # Converter os DataFrames para formato de string para commit
        files_to_commit = {}
        for uploaded_file in uploaded_files:
            file_name = uploaded_file.name
            file_content = pd.read_excel(uploaded_file).to_csv(index=False)
            files_to_commit[file_name] = file_content
        
        # Liberar botão para fazer o commit no GitHub
        if st.button("Fazer Commit no GitHub"):
            commit_status = commit_to_github(github_token, repo_owner, repo_name, commit_message, files_to_commit)
            st.write(commit_status)
    else:
        st.error(check_result)
