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

## Funcionalidades

1. Dashboard
    - Métricas
        1. Produtos com endereço de fracionado ineficiente - Soma dos produtos com apanha fracionada errada
        2. Curva A "medicamento” - Todos produtos que devem ir para o flowrack
        3. Produtos sem endereço de fracionado
        4. Produtos com endereço de caixa fechada ineficiente - Soma dos produtos com apanha caixa fechada errada
        5. Produtos sem endereço de caixa fechado
    - Apanha Fracionado
        1. Curvas B e C no Flowrack - Produtos para retirar do flowrack por conta da baixa saída
        2. Curvas A da prateleira (No Flowrack) - Produtos para serem realocados para prateleira pois existem produtos com maior saída
        3. Curvas A do Flowrack (Na prateleira) - Devem ser colocados no flowrack, pois tem alta saída e estão na prateleira
        4. **Comparação das Saídas Fracionadas**
        5. **Divisão das Saídas Fracionadas**
            1. Flowrack
            2. Prateleira
            3. Ponta de Gôndola
    - Apanha Caixa
        1. **Situação por local**
        2. Itens para colocar no local

---

2. Consulta
    - Consutar produtos em expecifico, curva, cadastros entre outros
    1. Saída e Atividade
        - Vizualização do tipo de curva, e informações de saída, filtrados

---

3. Dados Brutos
    - Atualização dos dados brutos
        - Campo para token de acesso pessoal do Github - Credencial para a para atualização dos dados
        - Seleção dos dados - Se são os dados da cuva/cadastro ou as metricas de ocupação
        - Upload dos arquivos - É verificados se os arquivos são correspondentes aos dados selecionados

---

4. Ocupação
    - Métricas
        1. Fracionado
            1. Total de endereços
            2. Total de endereços bloqueados
            3. Total de endereços utilizáveis
            4. **Motivo do bloqueio**
            5. **Situação das apanhas utilizáveis**
        2. Armazenagem
            1. Total de porta-pallets
            2. Total de armazenagens bloqueadas
            3. Total de armazenagens utilizáveis
            4. **Motivo do bloqueio**
            5. **Situação dos porta-pallets utilizáveis**
            6. **Situação dos porta-pallets em uso**
    - Caixa Fechada
        1. Selecione o tipo de visualização
        2. Selecione o tipo de saída
    - Flowrack
        1. Selecione o tipo de visualização do Flowrack
    - Prateleira
        1. Selecione o tipo de visualização das prateleiras