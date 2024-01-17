# Projeto Curva ABC

[![licence mit](https://img.shields.io/badge/licence-MIT-blue.svg)](./LICENSE)

Meu primeiro projeto de Analise de dados.

É um projeto que foi desenvolvido por mim, onde foram colocados em pratica os conhecimentos adquiridos na [formação de Ciencia de Dados](https://cursos.alura.com.br/degree/certificate/72841079-c405-4a94-af5d-e260c9451c76) da escola de tecnologia online [Alura](https://www.alura.com.br/).

O projeto é o tratamento e analise de dados de uma Curva ABC de medicamentos e a automação do download dos mesmos (Dados da curva), além da itegração das analises em uma aplicação para vizualização dos dados criada usando a biblioteca [Streamlit](https://streamlit.io/) do python.

---

> Leia também sobre o desenvolvimento e outros detalhes do projeto no meu [linkedin]().
>
> Dê uma olhada no [projeto final](https://projeto-curva-abc.streamlit.app/)!

---

Objetivo do projeto:

* Tonar eficiênte a analise dos dados da Curva ABC.

* Aumentar a eficácia da a analise baseada no estoque fisico e sua orientação.

* Trazer para o meu ambiente de trabalho uma ferramenta diferenciada.

* Desenvolver novas habilidades na minha área de trabalho pretendida.

---

![Pagina inicial do projeto](img\dashboard-curva-abc.png)

## Sobre o Projeto

Como o projeto esta estruturado?

### Setup de ambiente:

* Streamlit == 

* [Outras bibliotecas](requirements.txt)

### Como rodar localmente?

* Clone o projeto `git clone https://github.com/`

* Rode `streamlit run Dashboard.py`

* Pronto, A aplição vai abrir no seu navegador!

## Projeto-Curva-ABC.app

### Estrutura do projeto

* `.\Dashboard.py` é o arquivo principal da aplicação, ou a pagina pricipal. 

* `.\pages` é a pasta que contem os arquivos `.py` onde o streamlit compõe as paginas.

* `.\data` é a pasta que armazena os dados da curva.

* `.\.stremlit\config.toml` é o arquivo de configuração padrão do aplicativo, tema parão e cores da aplicação.

### Como me localizar no projeto?

* A pasta `.\automacao_donwload_datasets` é exclusivamente a automação para utilização na maquida da empresa, para o download dos data-sets dentro do sistema da mesma.

* Em `.\data\tratamento_curva_abc`, onde ficam os dados brutos e tratados em planilhas do excel, arquivos retirados do sistema da empresa.

    * Em `.\data\tratamento_curva_abc\datasets` é onde ficam armazendos os aquivos de dados ***brutos*** a serem tratados, que devem ser substituidos posterior a alguma alteração dos dados no sistema.

    * Em `.\data\tratamento_curva_abc\dados_tratados` é onde ficam armazendos os aquivos de dados ***tratados***.

    * >💡 Há um arquivo excutavel em `.\data\tratamento_curva_abc\tratamento_curva.exe` que trata separadamente os arquivos de cadastro (`produtos.xlsx`), e as relações de curvas (`curva_frac.xlsx`, `curva_cx.xlsx` e `curva_geral.xlsx`) e salva na pasta, caso seja necessário tratar esses dados separadamente.

        * > 📝 **NOTA:** Na aplicação, os dados são tratados separadamentes em quanto a mesma esta em execução.

* Em `.\data\analise_curva_abc` esta localizada a logica das analises

    * Descrição 

    * Divisão 

    * Localização 

---

> * O arquivo principal da aplicação `.\Dashboard.py` estão as metricas e funcionalidades, respecitivamente:
>
>    * Mertricas' de totais de endereços juntamente com os totais em numeros dos produtos que estão certos ou errados a serem alterados.
>
>    * Vizualição da divisão da saída dos produtos fracionados, e pordutos com locais a serem mudados, com disponibilidade de baixar os dados dos mesmo em excel.
>
>    * Vizualição dos protudos em locais de apanha caixa, em locais certos e errados, com disponibilidade de baixar os dados dos mesmo em excel.

---

* Em `.\pages`, cada página tem sua funcionalidade e funcionamento especifico:

    * `.\pages\Consultas` é basicamente uma página dentro da aplicação com um imput de um código valido de produto, onde são mostradas informações retiradas diretamente dos dados tratados da curva, que são relevantes ao dia a dia dentro do processo.

    * `.\pages\Dados_brutos` é uma vizualização dos dos dados tratados da curva, onde há uma disponibilidade de filtros para alteração da vizualização dos dados de forma mais crua, caso seja necessario.

    * `.\pages\Ocupação` é uma vizualização geral do estoque e seus locais.

* A pasta `.\mapa_estoque` contem a planilha com dados dos locais e localidades de endereços (Fracinado, tando de prateleiras quanto de flowrack, e caixas fechadadas), que foram pensados baseados na construção do estoque da empresa e como a organização do mesmo esta disposta isso, justamente em relação aos processos operacionais da empresa, visando uma melhor disposição das mercadorias.

    * > 📝 **NOTA:** Essa informação faz mas sentido com o conhecimento físico do estoque, e dos processos que envolvem o mesmo. A planilha é usada para consulta dentro do processo, e é a base para a lógica do projeto.

* O arquivo `.\DOC.md` é uma documentação do meu intendimento, interpretação, tudo que foi desenvolvido e pensado diante de toda informação relativa a função executada como () dentro da empresa, onde as informações que eram passadas de pessoa para pessoa dentro do cargo/função/responsabilidade, estão documentadas.

    * > 📝 **NOTA:** Estão listadas/documentadas informações relativas a, (e somente) ligadadas de alguma forma, aos processos e procedimentos com impactos, mesmo que indiretos a 'Analise da Curva ABC', como por exemplo a eficacia de um processo baseado na analise, não contendo informações expecificas sobre o tal processo citado.