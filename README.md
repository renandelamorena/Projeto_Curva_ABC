# Projeto Curva ABC

[![licence mit](https://img.shields.io/badge/licence-MIT-blue.svg)](./LICENSE)

Meu primeiro projeto de Análise de dados.

Desenvolvi este projeto para colocar em pratica os conhecimentos obtidos na [formação de Ciencia de Dados](https://cursos.alura.com.br/degree/certificate/72841079-c405-4a94-af5d-e260c9451c76) da escola de tecnologia online [Alura](https://www.alura.com.br/).

O projeto consiste no tratamento e análise de dados de uma Curva ABC de medicamentos, incluindo uma automação para o download dos mesmos e a integração das Análises em uma aplicação para visualização, criada usando a biblioteca [Streamlit](https://streamlit.io/) do python.

A análise da Curva ABC de medicamentos surgiu da minha experiência no primeiro emprego em uma distribuidora de medicamentos. Após trabalhar na parte operacional da empresa, assumi a responsabilidade pelo controle de estoque. Senti a necessidade de criar e aprimorar as ferramentas disponíveis, visando eficiência e simplicidade, o que traria conhecimento e valor agregado à empresa.

---

> Leia também sobre o desenvolvimento e outros detalhes do projeto no meu [linkedin]().
>
> Confira o [projeto final](https://projeto-curva-abc.streamlit.app/)!

---

Objetivo do projeto:

* Tornar eficiente a Análise dos dados da Curva ABC.

* Aumentar a eficácia da análise baseada no estoque fisico e sua orientação.

* Introduzir uma ferramenta inovadora no ambiente de trabalho.

* Desenvolver novas habilidades na minha área de atuação pretendida (Programação, Ciência de dados).

---

![Pagina inicial do projeto](/img/dashboard-apanha-frac_1.png)

![Pagina inicial do projeto](/img/dashboard-apanha-frac_2.png)

## Sobre o Projeto

Como o projeto esta estruturado?

### Setup de ambiente:

* Streamlit == 1.29.0

* [Outras bibliotecas](requirements.txt)

### Como rodar localmente?

* Clone o projeto `git clone https://github.com/renandelamorena/Projeto_Curva_ABC.git`

* Execute: `streamlit run Dashboard.py`

* A aplicação abrirá no seu navegador.

## Projeto-Curva-ABC.app

### Estrutura do projeto

* `.\Dashboard.py` é o arquivo principal da aplicação ou a pagina principal. 

* `.\pages` contem os arquivos `.py` que compõem as páginas no Streamlit.

* `.\data` armazena os dados da curva.

* `.\.stremlit\config.toml` é o arquivo de configuração padrão do aplicativo.

* `.\requirements.txt` lista as dependências do projeto.

### Como me localizar no projeto?

* `.\automacao_download_datasets` contém a automação para o download dos datasets no sistema da empresa.

* `.\data\tratamento_curva_abc` inclui os dados brutos e tratados em planilhas do Excel.

    * `.\data\tratamento_curva_abc\datasets` armazena os dados ***brutos***. (Devem ser substituidos posteriormente a alguma alteração dos dados no sistema)

    * `.\data\tratamento_curva_abc\dados_tratados` contém os dados ***tratados***.

---

> * O arquivo principal da aplicação `.\Dashboard.py` estão as métricas e funcionalidades, respectivamente:
>
>    * Métricas' - totais de endereços, com os totais em números dos produtos que estão certos ou errados a serem alterados.
>
>    * Visualização da divisão da saída dos produtos fracionados, e produtos com locais a serem alterados, com disponibilidade de baixar os dados em excel.
>
>    * Visualização dos protudos em locais de apanha caixa, em locais certos e errados, com disponibilidade de baixar os dados em excel.

---

* Em `.\pages` cada página tem sua funcionalidade específica:

    * `.\pages\Consultas` oferece informações da curva baseadas em um código de produto válido.

    * `.\pages\Dados_brutos` permite atualizar as informações de dados do projeto.

    * `.\pages\Ocupação` mostra uma visão geral do estoque e seus locais.

* O arquivo `.\mapa_estoque\orientacao.xlxs` contem a planilha com dados dos locais e localidades de endereços (fracinado, [prateleiras e flowrack] e caixas fechadadas), que foram pensados baseados na construção do estoque da empresa e como a organização do mesmo está disposta, isso, justamente em relação aos processos operacionais da empresa, visando uma melhor disposição das mercadorias.

    * > 📝 **NOTA:** Essa informação faz mais sentido com o conhecimento físico do estoque, e dos processos operacionais que envolvem o mesmo. A planilha é usada para consulta dentro do processo, e é a base para a lógica do projeto.

---

![Pagina inicial do projeto](/img/ocupacao-caixa-fechada_1.png)

![Pagina inicial do projeto](/img/ocupacao-caixa-fechada_2.png)

# Análise curva ABC

# Resumo

Análise de dados de produtos em relação ao seu armazenamento e saída, tendo em vista uma melhor disposição dos produtos para uma maior eficiência do estoque.

# Como se dividem os processos?

## Conhecimento base do estoque e dos processos

### Como o estoque esta disposto:

#### Locais de endereços de caixa fechada

- Ponta - Local destinado para produtos cujo endereço fracionado é 'Ponta De Gôndola' - Tem o intuito de ser o mais próximo do endereço de fracionado por que o tipo de ressuprimento para esse endereço é um por vêz.

- Prateleira - Destinado para produtos com uma maior saída da prateleira, onde os mesmos não cabem no endereço fracionado Flowrack, para ficarem mais próximos do endereço fracionado.

- Apanha A - Maior e total concentração de produtos de curva A, onde seus endereços de fracionados são o Flowrack.

- Apanha B - Produtos que tem uma saída média (Curva B), e tem seus endereços de caixa fechada concentrados mais proximos dos endereços de fracionados que não direcionados nas prateleiras.

- Apanha C - Endereços de caixa fechada de produtos com as menores saídas ou produtos novos/sem saída. Seus endereços de fracionados localizam-se loges dos fracionados em geral por conta da baixa saída fracionada.

- Apanha AM - Localização das caixas fechadas de produdos classificados como antibióticos, que tem retensão de receita. - Sua finalidade se dá para uma maior organização dos endereços.

- Outros locais são destinados para tipos específicos de grupos de produtos ou para uma melhor disponibilidade de endereços em relação ao foco de otimização

- Ref. https://github.com/renandelamorena/projeto_curva_ABC/blob/main/mapa_estoque/orientacao.xlsx


#### Endereços de Fracionado
- Flowrack:
    - É o tipo de endereço de fracionado onde devem ficar localizados os produtos descritos como CURVA A , sendo eles medicamentos.
    - Saída constate de medicamentos e ressuprimento
    - Devem ficar os primeiros medicamentos em saída
    - Curva A
    - Endereço vinculado de caixa fechada = Não permite fracionado na caixa fechada, pois a capacidade do produto deve ser ajustada para o ressuprimento em caixas, afim de maximizar a eficiência.
- Ponta de gondola
    - É o tipo de endereço fracionado onde devem ficar localizados os produtos com dimensões maiores que o padrão, produtos que dificultam o ressuprimento e produtos que tem uma saída fora do padrão (para facilitar ressuprimento e saída de fracionado)
    - Outliers, produtos com saídas acima da média
    - Produtos grandes
    - Produtos chatos de abastecer
    - Endereços de apanha caixa fechada de pontas de gondola devem ficar no local de ponta (para caixas), ou ressuprimento por pallet no caso das altas demandas
    - Não é necessária uma curva em especifico (A, B ou C).
- Prateleira
    - É o tipo de endereço de fracionado destinado para as curvas B e C, ou para os medicamentos de curva A que não cabem no Flowrack. Os corredores são divididos por modulo cada modulo tendo 2 corredores, sendo um divido por tipos de produtos (Nutraceuticos, Alimentos, Higiene, Suplementos e outros) e um para medicamentos em exclusivo.
    - Curva B
    - Curva C
    - Curva A de produtos não medicamentos
    - Curva A de medicamentos que não cabem no Flowrack
    - Divisão de prateleiras por módulos, e por tipo de produto

- Ref. https://github.com/renandelamorena/projeto_curva_ABC/blob/main/mapa_estoque/orientacao.xlsx

> O projeto tem como foco a otimização das atividades: separação de pedidos fracionados e abastecimento de medicamentos fracionados. Porém viza a melhora de outras atividades inseridas no processo.

> Toda aplicação é pensada para facilitar todas Análises que tem impacto no processo. Minimizando o tempo para fazer relatorios e trazendo insights sobre o estoque com informaçôes visuais e direcionadas.

---

# Funcionalidades

## **1. Dashboard**
### **Métricas**
1. <u>**Produtos com endereço de fracionado ineficiente:**</u> Soma dos produtos com apanha fracionada errada.
---
2. <u>**Curva A "medicamento”:**</u> Todos produtos que devem ir para o flowrack.
---
3. <u>**Produtos sem endereço de fracionado:**</u> Endereçar.
---
4. <u>**Produtos com endereço de caixa fechada ineficiente:**</u> Soma dos produtos com apanha caixa fechada errada.
---
5. <u>**Produtos sem endereço de caixa fechado:**</u> Endereçar.
---
### **Apanha Fracionado**
1. **Curvas B e C no Flowrack:** Produtos para retirar do flowrack por conta da baixa saída.
---
2. **Curvas A da prateleira (No Flowrack):** Produtos para serem realocados para prateleira pois existem produtos com maior saída.
---
3. **Curvas A do Flowrack (Na prateleira):** Devem ser colocados no flowrack, pois tem alta saída e estão na prateleira.
---
4. **Comparação das Saídas Fracionadas:**
    - Selecione o tipo de endereço fracionado: Para a vizualizar nos graficos abaixo, a quantidade de saída fracionada pelos modulos e corredores do tipo de endereço fracionado selecionado. 
---
5. **Divisão das Saídas Fracionadas**
    1. Flowrack
        - <u>Filtar Saída pela classe:</u> visualização das saídas da classe do Florack selecionada por módulos.
        - <u>Situação da classe:</u> Comparação das saídas da classe selecionado por módulo.
        ---
        - **Realocar Produtos**: Retirar determinada quantidade de saída de produtos de um módulo.
            - É retornado uma relação dos produtos para serem realocados. (Produtos, que juntos, correspornde exatamente a saída desejada)
        ---
        - **Realocar Classes - Flowrack**: Relação dos produtos que devem ir para determinadas classes.
    ---
    2. Prateleira
        - <u>Filtar Saída por prateleiras:</u> visualização das saídas das prateleiras pela localização delas no módulo.
        - <u>Situação das prateleiras:</u> Comparação das saídas das prateleiras, do local selecionado, por módulo.
        ---
        - **Realocar Produtos**: Retirar determinada quantidade de saída de produtos de um módulo.
            - É retornado uma relação dos produtos para serem realocados. (Produtos, que juntos, correspornde exatamente a saída desejada)
    ---
    3. Ponta de Gôndola
        - <u>Filtar Saída por Ponta de Gôndola:</u> visualização das saídas das pontas pelo módulo.
        - <u>Situação das Pontas de Gôndolas:</u> Comparação das saídas das pontas, por módulo.
        ---
        - **Realocar Produtos**: Retirar determinada quantidade de saída de produtos de um módulo.
            - É retornado uma relação dos produtos para serem realocados. (Produtos, que juntos, correspornde exatamente a saída desejada)
---
### **Apanha Caixa**
    1. **Situação por local:** O que está certo ou errado no local selecionado. (Se está certo ou errado no local).
    ---
    2. **Itens para colocar no local:** O que é destinado para o local selecionado. (O que deve ir para o local).

## **2. Consulta**
- Consutar produtos em específico, curva, cadastros entre outros.
1. Saída e Atividade
    - visualização do tipo de curva, e informações de saída, etc.

---

## **3. Dados Brutos**
### **Atualização dos dados brutos**

Para atualizar os dados brutos do projeto, siga os passos abaixo:

- Token de Acesso Pessoal do Github:

    Insira o seu token de acesso pessoal do Github no campo correspondente.

- Seleção dos Dados:

    Escolha se você deseja atualizar os dados da curva/cadastro ou as métricas de ocupação.
    Upload dos Arquivos:

- Faça o upload dos arquivos necessários conforme as instruções abaixo:

    - Para Dados da Curva e/ou Cadastros os arquivos necessários são:

        <u>**curva_frac.xlsx**</u>

        <u>**curva_cx.xlsx**</u>

        <u>**curva_geral.xlsx**</u>

        <u>**produtos.xlsx**</u>

    ---

    - Instruções para Atualização:

        > Fonte todas as curvas: Acesse o sistema WMS -> Gerenciamento de Estoque -> Consultas -> Curva -> Selecione o período desejado -> Filtrar -> Gerar Excel.
        >
        > Fonte 'produtos': Acesse o sistema WMS -> Gerenciamento de Estoque -> Consultas -> Consulta Cadastro de Endereços Apanha por Produto; selecionar **todos** em todos dos flags -> filtrar -> Gerar Excel.

---

- Faça o upload dos arquivos gerados para atualizar as informações.

    - Para Dados das Métricas os arquivos necessários são:

        <u>**armazenagens.xlsx**</u>

        <u>**armazenagem_estoque.xlsx**</u>

        <u>**fracionado.xlsx**</u>

    ---

    - Instruções para Atualização:

        > Fonte 'armazenagens': Acesse o sistema WMS -> Gerenciamento de Estoque -> No filtro "Função do endereço" selecione "Armazenagem" -> Filtrar -> Gerar Excel.
        >
        > Fonte 'armazenagem_estoque': Acesse o sistema WMS -> Gerenciamento de Estoque -> Consultas -> Consulta por endereço -> Deixe selecionado somente "Armazenagens".
        >
        > Fonte 'fracionado': Acesse o sistema WMS -> Gerenciamento de Estoque -> No filtro "Rua" selecione "995" -> Filtrar -> Gerar Excel.
        >
        > Faça o upload dos arquivos gerados para atualizar as informações.

---

## **4. Ocupação**

### **Métricas**
1. Fracionado
    1. Total de endereços:
        - Total de endereços fracionados brutos.
        ---
    2. Total de endereços bloqueados:
        - Total de endereços fracionados que estão 'bloqueados'.
        ---
    3. Total de endereços utilizáveis:
        - Diferença entre total de endereços brutos e os que estão bloqueados "Tudo o que pode ser utilizado".
        ---
    4. Motivo do bloqueio:
        - Os motivos de bloqueios de endereços fracionados e a quantidade de endereços bloqueados pelo motivo.
        ---
    5. Situação das apanhas utilizáveis:
        - Dentro do que pode ser utilizado dos endereços, é o que se encontra em uso ou liberado, sendo liberado e com cadastro de produtos, ou liberado e sem produtos cadastrados no endereço
        ---

    > PARA ATUALIZAR AS INFORMAÇÕES DE MÉTRICAS: Página de 'Dados Brutos' -> Atualização dos dados brutos -> (Atualizar os dados das métricas)

---
2. Armazenagem
    1. Total de porta-pallets:
        - Total de emdereços de armazenagens brutas.
        ---
    2. Total de armazenagens bloqueadas:
        - Total de endereços de armazenagens que estão 'bloqueadas'.
        --- 
    3. Total de armazenagens utilizáveis:
        - Diferença entre total de endereços de armazenagens brutas e as que estão bloqueadas "Tudo o que pode ser utilizado".
        ---
    4. Motivo do bloqueio:
        - Os motivos de bloqueios de endereços de armazenagens e a quantidade de endereços bloqueados pelo motivo. (Motivo e total de endereços)
        ---
    5. Situação dos porta-pallets utilizáveis:
        - Dentro do que pode ser utilizado dos endereços, é o que se encontra em uso ou liberado.
        ---
    6. Situação dos porta-pallets em uso:
        - Dentro do que está em uso, os tipos dos produtos que estão armazenados
        ---

    > PARA ATUALIZAR AS INFORMAÇÕES DE MÉTRICAS: Página de 'Dados Brutos' -> Atualização dos dados brutos -> (Atualizar os dados das métricas)

---
### **Caixa Fechada**
1. <u>**Selecione o tipo de visualização:**</u>
    - Cadastro: É a visualização de ocupação dos endereços de caixa fechada pelo seu cadastro de produtos.
    - Sáida: É a visualização de ocupação dos endereços de caixa fechada por um tipo de saída determinada. 
    ---
2. <u>**Selecione o tipo de saída:**</u>
    - Cadastro selecionado:
        - Produtos vinculados: Produtos vinculados por endereço.
        - Produtos com estoque: Produtos com estoque por endereço.
        ---
    - Sáida: 'Tipo de saída selecionada' por endereço, por exemplo, ressuprimento fracionado por endereço.
    ---
3. Gráfico de calor dos endereços de caixa fechada, baseado nos filtros acima.

---
### **Flowrack**
1. <u>**Selecione o tipo de visualização do Flowrack:**</u>
    - Por corredor: Somente o corredor que é selecionado.
    ---
    - Geral: Visualização do Flowrack inteiro.
---
2. <u>**Selecione o tipo de saída do FLowrack:**</u>
    - Por venda (UND): Quantidade de venda fracionada por endereço.
    ---
    - Por Ressuprimento (Frac): Quantidade de ressuprimento fracionado por endereço.
---
3. Gráfico de calor dos endereços de fracionados, baseado nos filtros acima.

---
### **Prateleira**
1. <u>**Selecione o tipo de visualização do Prateleira:**</u>
    - Por corredor: Somente o corredor que é selecionado.
    ---
    - Geral: Visualização da Prateleira inteira.
---
2. <u>**Selecione o tipo de saída da Prateleira:**</u>
    - Por venda (UND): Quantidade de venda fracionada por endereço.
    ---
    - Por Ressuprimento (Frac): Quantidade de ressuprimento fracionado por endereço.
---
3. Gráfico de calor dos endereços de fracionados, baseado nos filtros acima.