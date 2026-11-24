# Conferência da legenda v7 contra o CSV

Conferência executada em `notebooks/01_conferencia_legenda.ipynb` sobre os arquivos locais v7. As saídas do notebook são agregadas; não são exibidos valores de identificadores, e frequências de categorias abaixo de 10 são agrupadas/suprimidas.

## Resultados conferidos

- **Estrutura:** as 66 colunas do CSV correspondem às 66 posições numeradas na legenda, na mesma ordem. Não há coluna extra no CSV nem coluna numerada ausente.
- **Tipos:** os tipos semânticos das 66 colunas são compatíveis com a legenda. Nenhuma coluna apresentou tipo incompatível na conferência.
- **Origem dos registros:** a base tem 44.417 linhas `ACADEMICA` e 14.642 `OCORRENCIA`, iguais aos totais informados na legenda.
- **Categorias documentadas:** os domínios observados de `TURNO`, `SEXO`, `MATRICULAEFETIVADA`, `STATUSALUNO` e `ORIGEMREGISTRO` estão dentro dos valores descritos na legenda. `SIGLACURSO` tem 12 códigos, como esperado.
- **Faixas numéricas:** as faixas observadas estão de acordo com a legenda, exceto `IA04_01`, cuja frequência máxima observada é **100,56**, acima do limite de 100. A legenda já alerta que existem valores inválidos acima de 100.
- **Flags:** os indicadores `TEVE...` têm valores dentro do domínio 0/1. `TEVECONCLUSAOPROGRAMA` contém apenas zero, coerente com a observação de que não há ocorrência desse tipo.
- **Preenchimento:** para as 36 colunas com percentual de preenchimento informado na legenda, o CSV confere com o percentual esperado (arredondado a uma casa decimal). Para as outras 30 colunas de ocorrência (`TEVE...` e `DATA...`), a legenda não publica percentual individual porque o preenchimento depende de o aluno ter tido o evento, e não da extração. O notebook mostra os percentuais observados como descrição; esses valores, por si só, não indicam falha de extração nem dados faltantes.
- **Períodos letivos:** `ANOSEMESTRE` e `INGRESSO` seguem o formato e o intervalo 2009/1–2026/1 descritos na legenda.

## Divergências e pontos a confirmar

### Siglas de curso e `PERIODO = 0`

As 12 siglas de curso são `GAE`, `GEA`, `GEB`, `GEC`, `GEE`, `GEL`, `GEP`, `GES`, `GET`, `TAI`, `TGT` e `TRC`; `TAI`, `TGT` e `TRC` são cursos tecnológicos. `GAE` identifica aluno especial, como aluno de intercâmbio, que segue uma grade própria e não um curso padrão. Por isso, alunos especiais não têm um período regular associado, e `PERIODO = 0` é usado principalmente para esses casos. No CSV, 72,7% das linhas com `PERIODO = 0` correspondem a GAE; o valor zero não é exclusivo desse código. As contagens pequenas por curso são agrupadas ou suprimidas no notebook.

### Chave de unicidade da linha

A chave única é aluno + semestre + `HANDLEALUNOCURRICULO`: esse identificador representa o vínculo do aluno com o currículo, e a combinação não tem repetições na base. `HANDLECURRICULO` identifica apenas o currículo; por isso, aluno + semestre + `HANDLECURRICULO` apresenta **35 combinações repetidas**. Um aluno pode ter mais de um vínculo com o mesmo currículo, por exemplo, ao reingressar. Scripts que precisem identificar unicamente o vínculo por aluno e semestre devem usar `HANDLEALUNOCURRICULO`. A afirmação da seção 3 da legenda deve ser interpretada com esse identificador.

### Grafia da transferência/afastamento

`TEVETRANSAFASTAMENTO` e `DATATRANSAFASTAMENTO` têm a mesma grafia no CSV v7 e na legenda v7. A grafia antiga `TEVETRASAFASTAMENTO` não aparece nos arquivos atuais.

### Colunas ausentes por escopo

`VALORMENSALIDADE`, `MATRICULA` e `DATANASCIMENTO` não aparecem no CSV, conforme a legenda, que informa que dados financeiros e identificadores pessoais não fazem parte da extração. A v7 não tem grupo temático financeiro.

## Limites desta conferência

O notebook `00_carga_base.ipynb` foi executado na branch `issue-2-carga-base`; os totais exibidos nele conferem com a referência v7 embutida no próprio notebook. O texto do PR da issue #2 não foi confirmado diretamente nesta conferência.

Este registro incorpora os esclarecimentos recebidos sobre as siglas de curso, `GAE`, `PERIODO = 0` e a chave do vínculo.
