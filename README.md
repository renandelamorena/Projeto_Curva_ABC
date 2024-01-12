# Projeto de analise e tratamento automatico da curva ABC
Projeto de analise descritiva da curva ABC de produtos em relação a sua produção e orientação da armazenagem 

## Divisão da saída no flowrack

* Organizar o módulo por classes
* Transferir diferença de saída por classes

## Tramento da curva

### Porque tratar a curva?

- As basses de dados são baixadas com alguns problemas que presisam ser tratados, como os nomes de colunas, espaços vazios no meio dos dados, códigos de produtos e etc. A fim de melhorar a leitura e interpretação dos dados, alem de deixa-los mais organizados.

### Requisitos

**Datasets:**

* produtos = cadastro de produtos (Endereços e cadastros);
* curva_frac = curva de certo periodo de saida fracionada (normalmente 3 meses);
* curva_cx = curva de certo periodo de saida de caixas (normalmente 3 meses);
* curva_geral = curva de certo periodo de saida, tando de caixas quanto fracionado em unidades (normalmente 3 meses).

### Caracteristicas

**Ajusta:**

- Coluna de códigos
- Linhas vazias
- Renomeia colunas

- Traz somente os dados necessarios
- Junta as imformações da curva com cadastro
- traz todos informações em _dados_tratados_ com _situacao_final_

**Importante**

- O ideal é atualizar as curvas (Fracionado, Caixa Fechada e Geral) a cada 3 meses

- Os cadastros de produtos podem e *devem* ser atualizados sempre que possível. (Recomendação: Atualizar todo dia, ou quando houver mudanças no estoque)