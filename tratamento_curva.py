# # Importando Bibliotecas

import pandas as pd
pd.set_option('display.max_columns', None)
# # Importando Dados

produtos = pd.read_excel('datasets\produtos.xlsx')

curva_geral = pd.read_excel('datasets\curva_geral.xlsx')

curva_cx = pd.read_excel('datasets\curva_cx.xlsx')

curva_frac = pd.read_excel('datasets\curva_frac.xlsx')
# # Tratando Dados
# # Funções

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
# ## Tratando códigos

dfs = [curva_geral, curva_frac, curva_cx, produtos]
tratar_codigos(dfs)
# ## Juntando as informações
# ### Fracionado

curva_abc_frac = pd.merge(curva_frac, produtos, on='Código', how='outer')

curva_abc_frac['Código'] = pd.to_numeric(curva_abc_frac['Código'])

curva_abc_frac['Ender.Fracionado'] = curva_abc_frac['Ender.Fracionado'].astype(str)

refatorar_indece(curva_abc_frac, 'Ordem')

# ### Caixa Fechada

curva_abc_cx = pd.merge(curva_cx, produtos, on='Código', how='outer')

curva_abc_cx['Código'] = pd.to_numeric(curva_abc_cx['Código'])

curva_abc_cx['Ender.Fracionado'] = curva_abc_cx['Ender.Fracionado'].astype(str)

refatorar_indece(curva_abc_cx, 'Ordem')

# ### Geral

curva_abc_geral = pd.merge(curva_geral, produtos, on='Código', how='outer')

curva_abc_geral['Código'] = pd.to_numeric(curva_abc_geral['Código'])

curva_abc_geral['Ender.Fracionado'] = curva_abc_geral['Ender.Fracionado'].astype(str)

refatorar_indece(curva_abc_geral, 'Ordem')

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

refatorar_indece(situacao_final, 'Ordem')

# # Organizando colunas

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
# ### Tratando NaN
situacao_final['Descrição'] = situacao_final['Descrição'].fillna('-')

situacao_final.to_excel('dados_tratados\situacao_final.xlsx')