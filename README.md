# Projeto de analise e tratamento automatico da curva ABC
Projeto de analise descritiva da curva ABC de produtos em relação a sua produção e orientação da armazenagem 

## Divisão da saída no flowrack

### XPE

#### Filtro

Os 'xaropes' são filtrados de forma que: 

* Sua curva de fracionado seja == A;
* Seu padrão de embalagem seja == 60 und;
* Sua descrição do produto contenha ou 100ml ou 100 ml ou 120ml ou 120 ml;
* ou
* Seja algum protudo selecionado previamente, independere de embalagem, porém que seja de curva == A

No final é retirado também qualquer produdo que possa ter passado no filtro acima, que seja selecionado após a analise do filtro, executando-o novamente o filtro, sendo selecionado previamente que seja retirado tal produto.