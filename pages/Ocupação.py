import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

def caminho_absoluto(caminho_relativo_com_barras_normais):
    
    caminho_base = os.getcwd()

    caminho_absoluto = os.path.join(caminho_base, caminho_relativo_com_barras_normais)

    return caminho_absoluto

situacao_final = pd.read_excel(caminho_absoluto('data/tratamento_curva_abc/dados_tratados/situacao_final.xlsx')).set_index('Ordem')
mapa = pd.read_excel(caminho_absoluto('mapa_estoque/mapa_orientacao.xlsx')).fillna('-').astype(str)

def criar_mapa_de_calor_caixa_fechada(coluna, nome_do_grafico):

  coluna_x_endereço = situacao_final[['Ender.Cx.Fechada', coluna]].groupby(['Ender.Cx.Fechada']).sum().reset_index()
  coluna_x_endereço = pd.Series(coluna_x_endereço[coluna].values, index = coluna_x_endereço['Ender.Cx.Fechada']).to_dict()
  coluna_por_enderço_cx_fechada = mapa.replace(coluna_x_endereço)

  # Criar o mapa de calor
  fig = go.Figure(data=go.Heatmap(
                  z=coluna_por_enderço_cx_fechada.values, # Valores para a cor
                  x=coluna_por_enderço_cx_fechada.columns, # Eixos X
                  y=coluna_por_enderço_cx_fechada.index, # Eixo Y
                  colorbar_title='Saída',
                  colorscale=['LightBlue', 'DarkBlue'],
                  text=mapa,
                  texttemplate='%{text}',
                  textfont={'size':10}
                  ))

  # Ajustes finais no layout
  fig.update_layout(title_text=nome_do_grafico,
                    yaxis=dict(autorange='reversed'),
                    xaxis_showgrid=False, yaxis_showgrid=False,
                    xaxis_zeroline=False, yaxis_zeroline=False,
                    autosize=False,
                    width=1450,
                    height=1200,
                    )

  fig.update_xaxes(side='top')
  return fig
  
st.title('Ocupação do estoque')

aba1, aba2, aba3 = st.tabs(['Caixa Fechada', 'Flowrack', 'Prateleira'])

with aba1:

    opcao_coluna = st.selectbox('Selecione o tipo de saída:',
                                ('Ativ.Ressupr.Frac'),
                                index = None,
                                placeholder = 'Selecione',
                                )

    chart = criar_mapa_de_calor_caixa_fechada(opcao_coluna, 'Ressuprimento fracionado por endereço')
    st.plotly_chart(chart, use_container_width=True)
    
with aba2:
    ''
    
with aba3:
    ''
