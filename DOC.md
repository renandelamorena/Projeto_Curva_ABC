# Analise curva ABC

# Resumo

Analise de dados de produtos em relação ao seu armazenamento e saída, tendo em vista uma melhor disposição dos produtos para uma maior eficiência do estoque.

# Como se dividem os processos?

## Conhecimento base do estoque e dos processos

### Como o estoque esta disposto:

- Locais de endereços de caixa fechada

    - Ponta - Local destinado para produtos cujo endereço fracionado é 'Ponta De Gôndola' - Tem o intuito de ser o mais próximo do endereço de fracionado por que o tipo de ressuprimento para esse endereço é um por vêz.

    - Prateleira - Destinado para produtos com uma maior saída da prateleira, onde os mesmos não cabem no endereço fracionado Flowrack, para ficarem mais próximos do endereço fracionado.

    - Apanha A - Maior e total concentração de produtos de curva A, onde seus endereços de fracionados são o Flowrack.

    - Apanha B - Produtos que tem uma saída média (Curva B), e tem seus endereços de caixa fechada concentrados mais proximos dos endereços de fracionados que não direcionados nas prateleiras.

    - Apanha C - Endereços de caixa fechada de produtos com as menores saídas ou produtos novos/sem saída. Seus endereços de fracionados localizam-se loges dos fracionados em geral por conta da baixa saída fracionada.

    - Apanha AM - Localização das caixas fechadas de produdos classificados como antibióticos, que tem retensão de receita. - Sua finalidade se dá para uma maior organização dos endereços.

    - Outros locais são destinados para tipos expecificos de grupos de produtos ou para uma melhor disponibilidade de endereços em relação ao foco de otimização

- Ref. https://github.com/renandelamorena/projeto_curva_ABC/blob/main/mapa_estoque/orientacao.xlsx


- Endereços de Fracionado
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

> Toda aplicação é pensada para facilitar todas analises que tem impacto no processo. Minimizando o tempo para fazer relatorios e trazendo insights sobre o estoque com informaçôes visuais e direcionadas.

---

# Funcionalidades

## **1. Dashboard**
- **Métricas**
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
- **Apanha Fracionado**
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
            - <u>Filtar Saída pela classe:</u> Vizualização das saídas da classe do Florack selecionada por módulos.
            - <u>Situação da classe:</u> Comparação das saídas da classe selecionado por módulo.
            ---
            - **Realocar Produtos**: Retirar determinada quantidade de saída de produtos de um módulo.
                - É retornado uma relação dos produtos para serem realocados. (Produtos, que juntos, correspornde exatamente a saída desejada)
            ---
            - **Realocar Classes - Flowrack**: Relação dos produtos que devem ir para determinadas classes.
        ---
        2. Prateleira
            - <u>Filtar Saída por prateleiras:</u> Vizualização das saídas das prateleiras pela localização delas no módulo.
            - <u>Situação das prateleiras:</u> Comparação das saídas das prateleiras, do local selecionado, por módulo.
            ---
            - **Realocar Produtos**: Retirar determinada quantidade de saída de produtos de um módulo.
                - É retornado uma relação dos produtos para serem realocados. (Produtos, que juntos, correspornde exatamente a saída desejada)
        ---
        3. Ponta de Gôndola
            - <u>Filtar Saída por Ponta de Gôndola:</u> Vizualização das saídas das pontas pelo módulo.
            - <u>Situação das Pontas de Gôndolas:</u> Comparação das saídas das pontas, por módulo.
            ---
            - **Realocar Produtos**: Retirar determinada quantidade de saída de produtos de um módulo.
                - É retornado uma relação dos produtos para serem realocados. (Produtos, que juntos, correspornde exatamente a saída desejada)
    ---
- **Apanha Caixa**
    1. **Situação por local:** O que está certo ou errado no local selecionado. (Se está certo ou errado no local).
    ---
    2. **Itens para colocar no local:** O que é destinado para o local selecionado. (O que deve ir para o local).

## **2. Consulta**
- Consutar produtos em expecifico, curva, cadastros entre outros.
1. Saída e Atividade
    - Vizualização do tipo de curva, e informações de saída, etc.

---

## **3. Dados Brutos**
- **Atualização dos dados brutos**
    - Campo para token de acesso pessoal do Github - Credencial para a para atualização dos dados
    --- 
    - Seleção dos dados - Se são os dados da cuva/cadastro ou as metricas de ocupação
    ---
    - Upload dos arquivos - É verificado se os arquivos são correspondentes aos dados selecionados

        - Dados da curva e/ou cadastros: Se for feito o upload de todos os arquivos corretamente, os dados são tratados automaticamente e será liberado o botão para enviar os dados, arquivos necessarios são - (curva_frac.xlsx, curva_cx.xlsx, curva_geral, produtos.xlsx). Caso contrario os arquivos seram enviados separadamente, não atualizando as informações em 'situação_final'.

            > Fonte 'curva_frac': wms; gerenciamento de estoque; consultas; curva; (1 ano atras, a partir de ontem); selecionar fracionado; filtrar; gerar excel.
            >
            > Fonte 'curva_cx': wms; gerenciamento de estoque; consultas; curva; (1 ano atras, a partir de ontem); selecionar caixa fechada; filtrar; gerar excel.
            >
            > Fonte 'curva_geral': wms; gerenciamento de estoque; consultas; curva; (1 ano atras, a partir de ontem); selecionar geral; filtrar; gerar excel.
            >
            > Fonte 'produtos': wms; gerenciamento de estoque; consultas; cadastro de produtos; selecionar **todos** em todos dos flags; filtrar; gerar excel.

        - Dados das métricas: São os arquivos necessarios os arquivos: armazenagens.xlsx, armazenagem_estoque.xlsx e fracionado.xlsx.

            > Fonte 'armazenagens': wms; gerenciamento de estoque; no filtro "Função do endereço" - Armazegem; filtrar; gerar excel.
            >
            > Fonte 'armazenagem_estoque': wms; gerenciamento de estoque; consultas; consulta por endereço; deixar selecionado somente "Armagenagens" .
            >
            > Fonte 'fracionado': wms; gerenciamento de estoque; no filtro "Rua" - 995; filtrar; gerar excel.

---

## **4. Ocupação**

- **Métricas**
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
- **Caixa Fechada**
    1. Selecione o tipo de visualização:
        - Cadastro: É a vizualização de ocupação dos endereços de caixa fechada pelo seu cadastro de produtos.
        - Sáida: É a vizualização de ocupação dos endereços de caixa fechada por um tipo de saída determinada. 
        ---
    2. Selecione o tipo de saída:
        - Cadastro selecionado:
            - Produtos vinculados: Produtos vinculados por endereço.
            - Produtos com estoque: Produtos com estoque por endereço.
            ---
        - Sáida: 'Tipo de saída selecionada' por endereço, por exemplo, ressuprimento fracionado por endereço.
        ---
    3. Gráfico de calor dos endereços de caixa fechada, baseado nos filtros acima.

---
- **Flowrack**
    1. Selecione o tipo de visualização do Flowrack:
        - Por corredor: Somente o corredor que é selecionado.
        ---
        - Geral: Vizualição do Flowrack inteiro.
    ---
    2. Selecione o tipo de saída do FLowrack:
        - Por venda (UND): Quantidade de venda fracionada por endereço.
        ---
        - Por Ressuprimento (Frac): Quantidade de ressuprimento fracionado por endereço.
    ---
    3. Gráfico de calor dos endereços de fracionados, baseado nos filtros acima.

---
- **Prateleira**
    1. Selecione o tipo de visualização do Prateleira:
        - Por corredor: Somente o corredor que é selecionado.
        ---
        - Geral: Vizualição da Prateleira inteira.
    ---
    2. Selecione o tipo de saída da Prateleira:
        - Por venda (UND): Quantidade de venda fracionada por endereço.
        ---
        - Por Ressuprimento (Frac): Quantidade de ressuprimento fracionado por endereço.
    ---
    3. Gráfico de calor dos endereços de fracionados, baseado nos filtros acima.