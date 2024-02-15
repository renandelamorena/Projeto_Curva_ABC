# Projeto Curva ABC

[![licence mit](https://img.shields.io/badge/licence-MIT-blue.svg)](./LICENSE)

Meu primeiro projeto de Analise de dados.

Desenvolvi este projeto para colocar em pratica os conhecimentos obtidos na [formação de Ciencia de Dados](https://cursos.alura.com.br/degree/certificate/72841079-c405-4a94-af5d-e260c9451c76) da escola de tecnologia online [Alura](https://www.alura.com.br/).

O projeto consiste no tratamento e análise de dados de uma Curva ABC de medicamentos, incluindo uma automação para o download dos mesmos e a itegração das analises em uma aplicação para vizualização, criada usando a biblioteca [Streamlit](https://streamlit.io/) do python.

A análise da Curva ABC de medicamentos surgiu da minha experiência no primeiro emprego em uma distribuidora de medicamentos. Após trabalhar na parte operacional da empresa, assumi a responsabilidade pelo controle de estoque. Senti a necessidade de criar e aprimorar as ferramentas disponíveis, visando eficiência e simplicidade, o que traria conhecimento e valor agregado à empresa.

---

> Leia também sobre o desenvolvimento e outros detalhes do projeto no meu [linkedin]().
>
> Confira o [projeto final](https://projeto-curva-abc.streamlit.app/)!

---

Objetivo do projeto:

* Tonar eficiênte a analise dos dados da Curva ABC.

* Aumentar a eficácia da a analise baseada no estoque fisico e sua orientação.

* Introduzir no ambiente de trabalho uma ferramenta inovadora.

* Desenvolver novas habilidades na minha área de atuação pretendida (Programação, Ciência de dados).

---

![Pagina inicial do projeto](/img/dashboard-curva-abc.png)

## Sobre o Projeto

Como o projeto esta estruturado?

### Setup de ambiente:

* Streamlit == 1.29.0

* [Outras bibliotecas](requirements.txt)

### Como rodar localmente?

* Clone o projeto `git clone https://github.com/`

* Execute: `streamlit run Dashboard.py`

* A aplicação abrirá no seu navegador.

## Projeto-Curva-ABC.app

### Estrutura do projeto

* `.\Dashboard.py` é o arquivo principal da aplicação ou a pagina pricipal. 

* `.\pages` contem os arquivos `.py` que compõem as páginas no Streamlit.

* `.\data` armazena os dados da curva.

* `.\.stremlit\config.toml` é o arquivo de configuração padrão do aplicativo.

* `.\requirements.txt` lista as dependências do projeto.

### Como me localizar no projeto?

* `.\automacao_donwload_datasets` contém a automação para o download dos datasets no sistema da empresa.

* `.\data\tratamento_curva_abc` inclui os dados brutos e tratados em planilhas do Excel.

    * `.\data\tratamento_curva_abc\datasets` armazena os dados ***brutos***. (Devem ser substituidos posteriormente a alguma alteração dos dados no sistema)

    * `.\data\tratamento_curva_abc\dados_tratados` contém os dados ***tratados***.

    * >💡 Há um executável em `.\data\tratamento_curva_abc\tratamento_curva.exe` para tratar os dados separadamente.

* Em `.\data\analise_curva_abc` contém a lógica das análises:

    * Divisão

    * Localização 

---

> * O arquivo principal da aplicação `.\Dashboard.py` estão as metricas e funcionalidades, respecitivamente:
>
>    * Mertricas' - totais de endereços, com os totais em números dos produtos que estão certos ou errados a serem alterados.
>
>    * Vizualição da divisão da saída dos produtos fracionados, e produtos com locais a serem alterados, com disponibilidade de baixar os dados em excel.
>
>    * Vizualição dos protudos em locais de apanha caixa, em locais certos e errados, com disponibilidade de baixar os dados em excel.

---

* Em `.\pages` cada página tem sua funcionalidade específica:

    * `.\pages\Consultas` oferece informações da curva baseadas em um código de produto válido.

    * `.\pages\Dados_brutos` permite visualizar e filtrar os dados tratados.

    * `.\pages\Ocupação` mostra uma visão geral do estoque e seus locais.

* O arquivo `.\mapa_estoque\orientacao.xlxs` contem a planilha com dados dos locais e localidades de endereços (fracinado, [prateleiras e flowrack] e caixas fechadadas), que foram pensados baseados na construção do estoque da empresa e como a organização do mesmo está disposta, isso, justamente em relação aos processos operacionais da empresa, visando uma melhor disposição das mercadorias.

    * > 📝 **NOTA:** Essa informação faz mas sentido com o conhecimento físico do estoque, e dos processos operacionais que envolvem o mesmo. A planilha é usada para consulta dentro do processo, e é a base para a lógica do projeto.

* O arquivo `.\DOC.md` é uma documentação do meu intendimento, interpretação, tudo que foi desenvolvido e pensado diante de toda informação relativa a função executada como "controle de estoque" dentro da empresa, onde as informações que eram passadas de pessoa para pessoa dentro do cargo/função/responsabilidade, estão documentadas.

    * > 📝 **NOTA:** Estão listadas/documentadas informações relativas a processos e procedimentos com impactos, mesmo que indiretos a 'Analise da Curva ABC', como por exemplo a eficácia de um processo baseado na analise, não contendo informações expecificas sobre o tal processo citado.