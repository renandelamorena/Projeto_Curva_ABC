#python -m venv venv
#./venv/Scripts/activate

import streamlit as st
import pandas as pd
import plotly.express as px
import time
from io import BytesIO

st.set_page_config(layout='wide')

## Func

def formata_numero(valor, prefixo = ''):
    for unidade in ['', 'mil']:
        if valor < 1000:
            return f'{prefixo} {valor} {unidade}'
        valor /= 1000
    return f'{prefixo} {valor} milhões'

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

st.title('Dashbord - Projeto Curva ABC') #Titulo

situacao_final = pd.read_excel(r'..\tratamento_curva_abc\dados_tratados\situacao_final.xlsx').set_index('Ordem')

## Barra lateral com filtros

with st.sidebar:

    AC = 20
    AB = 32
    AA = 27
    AM = 8
    XPE = 9

    total_enderecos_mosdulo = AC + AB + AA

    numero_modulos = st.number_input('Número de modulos:', step=1, min_value=1, value=6, max_value=6)

    total_enderecos_molulos = numero_modulos * total_enderecos_mosdulo
    total_enderecos_aa = numero_modulos * AA
    total_enderecos_ab = numero_modulos * AB
    total_enderecos_ac = numero_modulos * AC
    total_enderecos_am = numero_modulos * AM
    total_enderecos_xpe = numero_modulos * XPE

    st.write('Endereços utilizaveis (XPE não): ', total_enderecos_molulos)
    st.write('Endereços classe AA é: ', total_enderecos_aa)
    st.write('Endereços classe AB é: ', total_enderecos_ab)
    st.write('Endereços classe AC é: ', total_enderecos_ac)
    st.write('Endereços liberados para antibióticos é: ', total_enderecos_am)
    st.write('Endereços destinados para XAROPE é: ', total_enderecos_xpe)

## Tabelas

### Tabelas - Apanha Caixa

### Tabelas - Apanha Fracionado

total_curva_frac = pd.DataFrame(situacao_final['Curva Frac'].value_counts()).reset_index().rename(columns={'Curva Frac':'Curva', 'count':'Total'})

#### Seleção e tabela de itens errados com o fracionado errado:
#Medicamentos curva b e c no flowrack que devem ir para a prateleira
selecao_curva_bc_frac_errado = (situacao_final['Tipo'] == 'Flowrack') & \
                               (situacao_final['Curva Frac'].isin(['B', 'C'])) & \
                               (situacao_final['Ender.Fracionado'] > 18.000) & \
                               (situacao_final['Ender.Fracionado'] != 9010.000)
                       
curva_bc_flowrack = situacao_final[selecao_curva_bc_frac_errado]
curva_bc_flowrack = curva_bc_flowrack[['Código',
                                        'Descrição',
                                        'Curva Frac',
                                        'Qtde Venda Frac',
                                        'Dias Pedido Frac',
                                        'Ativ.Ressupr.Frac',
                                        'Estoque Frac',
                                        'Embal.',
                                        'Ender.Cx.Fechada',
                                        'Ender.Fracionado',
                                        ]]
total_curva_bc_flowrack = curva_bc_flowrack.shape[0]

#### Seleção e tabela de itens errados (curva A no flowrack - mudar para a prateleira [itens cuja ordem é mair o do que a quantidade de endereços do flowrack])

#Itens de curva A, que são medicamentos normais
selecao_med_normal = (~situacao_final['Descrição'].str.contains('xpe|susp|sol|elixir', case=False)) & \
                     (~situacao_final['Descrição'].str.contains('SPRAYZIIN|escova|ABS|DENTAL|TOALHAS|AG ABSORVENTE|COMPRESSA|AG MULTIFRAL|AG PANTS|FITA|MASCARA|ATADURA|CERA ORTODONTICA|ESPARADRAPO', case=False)) & \
                     (situacao_final['Ender.Fracionado'] > 12.999) & \
                     (situacao_final['Curva Frac'] == 'A')

somente_med_A = situacao_final[selecao_med_normal]
total_somente_med_A = somente_med_A.shape[0]

num_linhas_a_excluir = total_somente_med_A - total_enderecos_molulos

if total_somente_med_A > total_enderecos_molulos:
    num_total_linhas = len(somente_med_A)
    produtos_para_flowrack = somente_med_A.drop(somente_med_A.tail(num_linhas_a_excluir).index)
    linhas_excluidas = somente_med_A.tail(num_linhas_a_excluir)
else:
    produtos_para_flowrack = somente_med_A
    linhas_excluidas = []

total_produtos_para_flowrack = produtos_para_flowrack.shape[0]

#Medicamentos curva A normais que estão na prateleira e devem ir para o flowrack
selecao_curva_a_normal_prateleira_para_flowrack = (situacao_final['Tipo'] == 'Prateleira').isin(produtos_para_flowrack)

curva_a_normal_prateleira_para_flowrack = situacao_final[selecao_curva_a_normal_prateleira_para_flowrack]

total_curva_a_normal_prateleira_para_flowrack = curva_a_normal_prateleira_para_flowrack.shape[0]

#Medicamentos curva A normais que estão no flowrack e devem ir para a prateleira
selecao_curva_a_normal_flowrack_para_prateleira = (situacao_final['Tipo'] == 'Flowrack').isin(linhas_excluidas)

curva_a_normal_flowrack_para_prateleira = situacao_final[selecao_curva_a_normal_flowrack_para_prateleira]

total_curva_a_normal_prateleira_para_flowrack = curva_a_normal_flowrack_para_prateleira.shape[0]

## Graficos

### Graficos - Apanha Caixa

### Graficos - Apanha Fracionado

fig_total_curva_frac = px.bar(total_curva_frac,
                              x='Curva',
                              y='Total', 
                              text_auto=True,
                              title='Total de curvas (Fraciondo)'
                              )

## Vizualização

aba1, aba2, aba3 = st.tabs(['Métricas', 'Apanha Caixa', 'Apanha Fracionado'])

#Métricas
with aba1:

    with st.expander('Fracionado'):
        coluna1, coluna2, coluna3, coluna4 = st.columns(4)
        with coluna1:   
            st.metric('Total de itens cadastrados:', formata_numero(situacao_final['Código'].shape[0]))
        with coluna2:
            st.metric('Total de curvas A (Medicamentos filtrados):', formata_numero(somente_med_A.shape[0]))

    coluna1, coluna2, coluna3 = st.columns(3)
    with coluna1:
        st.metric('Total de produtos inificientes (Fracionado):', formata_numero(total_curva_bc_flowrack + total_curva_a_normal_prateleira_para_flowrack + total_curva_a_normal_prateleira_para_flowrack))

#Apanha Caixa
# with aba2:

#Apanha Fracionado
with aba3:

    coluna1, coluna2, coluna3 = st.columns(3)
    with coluna1:
        st.metric('Curvas B e C no Flowrack:', total_curva_bc_flowrack)
        botao_donwload(curva_bc_flowrack, 'Download B e C - Flowrack', 'curva_bc_flowrack_mudar_para_prateleira.xlsx')
    with coluna2:
        st.metric('Curvas A da prateleira (No flowrack)', total_curva_a_normal_prateleira_para_flowrack)
        botao_donwload(curva_a_normal_flowrack_para_prateleira,'Donwload A - Flowrack', 'curva_a_flowrack_mudar_para_prateleira.xlsx')
    with coluna3:
        st.metric('Curvas A do Flowrack (Na prateleira)', total_curva_a_normal_prateleira_para_flowrack)
        botao_donwload(curva_a_normal_prateleira_para_flowrack,'Donwload A - Prateleira', 'curva_a_prateleira_mudar_para_flowrack.xlsx')

    #Fazer - graficos mostrando a saida por moulo (em unidade)

    #Ideia - Mapa de calor com a saida por endereço do flowrack

    #Fazer - grafico mostrando a saída por classe (em unidade)

    modulos = {1:{'29_28':[29, 28]}
               }

    coluna1, coluna2 = st.columns(2)
    with coluna1:
        st.plotly_chart(fig_total_curva_frac, use_container_width=True)