# Fatores acadêmicos associados aos eventos de saída na graduação

Projeto da disciplina C318 – Fundamentos de Machine Learning (Inatel).

## Contexto

A evasão no ensino superior é estudada há décadas. Tinto (1975), em uma síntese das pesquisas da época retomada em Tinto (1993), trata a saída do estudante como um **processo longitudinal**: o que o estudante traz ao ingressar interage, ao longo do curso, com as experiências acadêmicas e sociais que vive na instituição, e essas experiências reforçam ou enfraquecem a permanência. Por isso, este projeto olha para a **trajetória acadêmica**: como rendimento, frequência e progresso no curso se comportam nos semestres que antecedem uma saída registrada.

Tinto (1975) também mostra que as diferentes formas de saída (abandono voluntário, desligamento por desempenho, transferência) não são necessariamente o mesmo fenômeno. Por isso o projeto fala em **evento de saída**, definido de forma explícita a partir dos registros, e não em evasão definitiva.

Técnicas de aprendizado de máquina vêm sendo aplicadas a dados de estudantes para estimar o risco de evasão e identificar as variáveis associadas a ela (BARBOSA et al., 2023; CHAGAS; GOMIDE; SANTANA, 2025; VILLAR; ANDRADE, 2024). Chagas, Gomide e Santana (2025) e Villar e Andrade (2024) organizam os dados com um registro por estudante. Aqui, cada exemplo é um aluno **em um semestre**, para acompanhar a trajetória. Assim como este projeto, Chagas, Gomide e Santana (2025) usaram apenas dados acadêmicos, porque o acesso a informações socioeconômicas era restrito.

## Problema de negócio

Identificar, a partir dos dados acadêmicos, padrões e características associados à saída de estudantes de graduação, para entender quais aspectos da trajetória acadêmica estão relacionados a essa saída.

## Objetivos

**De negócio:** ajudar a instituição a compreender quais padrões acadêmicos aparecem antes das saídas registradas.

**De ciência de dados:**

1. caracterizar a base e avaliar a qualidade dos dados;
2. comparar alunos com e sem evento de saída, por grupo e ao longo da trajetória;
3. comparar modelos de classificação vistos em aula e identificar quais variáveis eles mais associam à saída.

**Fora do escopo:** sistema de alerta, previsão individual de alunos e painel de monitoramento. Os modelos servem para entender os dados, não para serem usados sobre alunos reais.

## Escopo dos fatores

O estudo trata de fatores **acadêmicos e da trajetória**: rendimento, frequência, disciplinas, atividades complementares, vínculo com o curso, sexo e ocorrências (saídas, trancamentos, retornos, diplomação). Ele **não** trata de "todos os fatores" da saída.

Dados **financeiros** (mensalidade, bolsa, financiamento estudantil) e **socioeconômicos** (renda, família, patrimônio) não fazem parte da base nem do estudo, porque o uso deles não foi autorizado. Isso é uma **limitação**: a literatura costuma apontar esses fatores como relevantes para a evasão. Os resultados não permitem dizer que eles não importam, só que não foram observados aqui.

Os resultados descrevem padrões **desta base** e não devem ser lidos como características da instituição.

## Perguntas de negócio

| # | Pergunta | Issues |
|---|---|---|
| P1 | Como a base está distribuída (cursos, semestres, perfil dos alunos) e qual a qualidade dos dados? | #3, #5, #7 |
| P2 | Quantos alunos têm evento de saída, de que tipo, e quantos voltam depois? | #6 |
| P3 | A proporção de alunos com evento de saída difere entre cursos, turnos, sexo e período de ingresso? | #8 |
| P4 | CRE, frequência e reprovações no semestre anterior à primeira saída diferem dos de alunos sem saída? | #9 |
| P5 | Como esses indicadores evoluem nos semestres que antecedem a saída? | #10 |
| P6 | Quais modelos de classificação vistos em aula se ajustam melhor aos dados preparados, e quais variáveis aparecem como mais associadas à saída? | #11, #12, #13 |

**Evento de saída** é o semestre com registro de desistência, abandono, cancelamento ou desligamento. Ele **não** é o mesmo que evasão definitiva, porque o aluno pode voltar depois. A definição completa é feita na issue #6.

## Enquadramento do problema

O projeto combina duas opções do escopo da disciplina, e as duas fazem parte da entrega:

- **Análise Exploratória de Dados**, que responde P1 a P5 e indica quais variáveis são mais relevantes para os modelos;
- **Aprendizagem Supervisionada – Classificação**, que responde P6. O rótulo é **"a primeira saída do aluno acontece no semestre seguinte"** (sim/não), e cada exemplo é um aluno em um semestre.

**Por que classificação, e não regressão:** a resposta que o modelo prevê é qualitativa (sai ou não sai no semestre seguinte), e problemas com resposta qualitativa são de classificação.

**Os três elementos para aplicar machine learning**, como visto em aula:

1. **Existe um padrão a ser observado?** É o que a análise exploratória verifica (P3 a P5).
2. **O padrão pode ser descrito por uma fórmula exata?** Não: a saída depende de muitos fatores ao mesmo tempo.
3. **Existem dados?** Sim: a trajetória semestral registrada no sistema acadêmico.

## Métricas técnicas e de negócio

A base é **desbalanceada**: a maior parte dos semestres não antecede uma saída. Um modelo que sempre responde "não sai" teria acurácia alta e não serviria para nada. Por isso, a escolha das métricas parte da pergunta de negócio.

**Pergunta de negócio:** para a instituição, o que é pior?

- **falso negativo:** deixar de apontar um semestre que antecede uma saída. O padrão que precede aquela saída passa despercebido;
- **falso positivo:** apontar um semestre que não antecede uma saída. A atenção se dilui em casos que não precisavam dela.

Como o objetivo é **compreender os padrões que antecedem as saídas**, deixar de identificá-los (falso negativo) é o erro mais custoso. Mas um modelo que aponta quase todos os semestres também não ensina nada (precisão muito baixa). Por isso o projeto busca **equilíbrio**, com atenção especial ao recall.

| Métrica | O que responde no projeto |
|---|---|
| Recall | Dos semestres que antecedem uma saída, quantos o modelo identifica |
| Precisão | Dos semestres que o modelo aponta, quantos realmente antecedem uma saída |
| F1 | Equilíbrio entre recall e precisão |
| ROC-AUC | Se o modelo ordena bem os casos com e sem saída, sem depender de um limiar |
| Acurácia | Quantas classificações acertou no geral. **Enganosa** aqui, por causa do desbalanceamento |

**Métrica de escolha do modelo (issue #13):** **F1 da classe positiva**, na validação cruzada do treino. Recall e precisão são reportados separadamente na leitura de negócio, e a ROC-AUC compara os modelos sem depender do limiar. Todo modelo é comparado com uma **linha de base** que sempre responde "não sai". *Proposta a confirmar na mentoria com o professor (issue #17).*

## Dados

### A base

O projeto usa a **base acadêmica v7** (`Base_academica.csv`), uma extração do sistema acadêmico de uma instituição de ensino superior com a trajetória semestral dos alunos de 2009/1 a 2026/1. Cada linha é um aluno em um semestre e currículo. A base traz dados acadêmicos, de vínculo, sexo e ocorrências. Ela **não** contém matrícula, data de nascimento, dados financeiros nem dados socioeconômicos.

O significado de cada coluna está na `Legenda.md`, que acompanha a base.

### Coleta e avaliação dos dados

- **Fonte:** uma única fonte, a extração do sistema acadêmico feita para um trabalho de conclusão de curso (TCC), com acesso restrito. Nenhuma fonte externa foi ou será cruzada com a base. Para o foco da disciplina, que são os fundamentos de machine learning, uma fonte já tratada e documentada evita gastar o projeto em engenharia de dados.
- **Cobertura:** semestres de 2009/1 a 2026/1 e 12 códigos de curso (8 engenharias, 3 cursos superiores de tecnologia e 1 código de aluno especial, fora da graduação regular). A unidade de observação é aluno × semestre × currículo, e o mesmo aluno aparece em vários semestres.
- **Composição:** a base é formada por **turmas de ingresso** a partir de 2009/1, e não por todos os alunos de cada semestre. De 2009 a 2013 ela só tem alunos dos primeiros períodos, e o número de alunos por ano se estabiliza a partir de 2014.
- **Dois tipos de linha:** `ACADEMICA`, quando o aluno tem matrícula efetivada no semestre, e `OCORRENCIA`, quando não tem, mas há algum registro (uma saída, um trancamento, o currículo antigo de quem migrou). Frequência e disciplinas só existem nas linhas acadêmicas.
- **O que a base não tem, e por quê:** dados financeiros e socioeconômicos, porque o uso não foi autorizado, e identificadores pessoais (matrícula, data de nascimento), que não fazem parte da extração. As colunas `HANDLE*` são códigos internos, usados só para juntar os registros de um mesmo aluno.
- **Adequação às perguntas:** a base permite responder P1 a P6 com indicadores acadêmicos, de vínculo, sexo e ocorrências. Ela **não** permite avaliar o papel de fatores financeiros, socioeconômicos, familiares ou de saúde, nem o motivo declarado da saída.

### Como obter

A base tem **acesso restrito** e **não vai para o GitHub**. Ela fica numa pasta compartilhada só com a equipe, por convite. Para ter acesso, peça à Karolina.

1. Baixe `Base_academica.csv` e `Legenda.md` para a pasta `data/` do repositório. O `.gitignore` impede que arquivos de `data/` e qualquer `.csv` sejam commitados.
2. Defina a variável de ambiente `BASE_CSV_PATH` com o caminho completo do CSV, como mostrado abaixo.

### Configurar `BASE_CSV_PATH`

**Windows (PowerShell)**

```powershell
# Só para a sessão atual do terminal:
$env:BASE_CSV_PATH = "C:\caminho\para\Projeto_C318\data\Base_academica.csv"

# Permanente para o seu usuário. Feche e abra o VS Code ou o Jupyter depois:
setx BASE_CSV_PATH "C:\caminho\para\Projeto_C318\data\Base_academica.csv"
```

**Linux / macOS**

```bash
# Só para a sessão atual do terminal:
export BASE_CSV_PATH="/caminho/para/Projeto_C318/data/Base_academica.csv"

# Permanente: acrescente a mesma linha ao ~/.bashrc ou ~/.zshrc e abra um novo terminal.
echo 'export BASE_CSV_PATH="/caminho/para/Projeto_C318/data/Base_academica.csv"' >> ~/.bashrc
```

### Carregar a base

Todos os notebooks leem a base pela mesma função:

```python
from src.dados import carregar_base

df = carregar_base()
```

A função lê o CSV no formato da v7 (separador `;`, UTF-8, vírgula decimal, datas `dd/mm/aa`) e converte as datas. Ela também cria `ANOSEMESTRE_ORD` e `INGRESSO_ORD`, que numeram os semestres de forma consecutiva (o semestre seguinte é sempre o valor + 1). Se a variável `BASE_CSV_PATH` não estiver definida, a função dá um erro explicando o que fazer.

Para conferir a instalação, rode `notebooks/00_carga_base.ipynb`: os totais devem bater com a ficha da `Legenda.md`.


## Metodologia

O projeto segue o fluxo de ciência de dados visto em aula:

```
Problema de negócio → Dados → Análise de dados → Preparação → Modelagem → Avaliação
```

A etapa de produção, que colocaria um modelo em uso, está fora do escopo.

| Etapa | O que é feito | Issues |
|---|---|---|
| Problema de negócio | Contexto, objetivos, perguntas, enquadramento e métricas (este README) | #4 |
| Dados | Carga única da base e conferência da legenda | #2, #3 |
| Análise de dados | Qualidade, definição do evento de saída, análise univariada, comparações entre grupos, trajetória e correlação | #5 a #11 |
| Preparação | Tabela aluno-semestre com rótulo, sem vazamento, e divisão treino/teste por aluno | #12 |
| Modelagem e avaliação | Comparação de modelos de classificação com validação cruzada e avaliação final no teste | #13 |
| Resultados e apresentação | Respostas às perguntas, conclusões, limitações e apresentação | #14, #15 |

As dúvidas levadas às mentorias com o professor e as decisões que mudam o projeto ficam registradas em `docs/mentorias.md` (issue #17).

## Resultados

*Preenchido na issue #14: uma subseção por pergunta de negócio (P1 a P6), com a figura principal e os números das saídas dos notebooks.*

## Conclusões

*Preenchido na issue #14: o que a análise mostra para a instituição (negócio) e o que mostra tecnicamente (dados e modelos), com as limitações do estudo.*


## Referências

BARBOSA, D.; CABRAL, L.; DWAN, F.; FEITAS, E.; MELLO, R. F. Previsão da evasão escolar através da análise de dados e aprendizagem de máquina: um estudo de caso. *In*: WORKSHOP DE APLICAÇÕES PRÁTICAS DE LEARNING ANALYTICS EM INSTITUIÇÕES DE ENSINO NO BRASIL (WAPLA), 2., 2023. **Anais** [...]. Porto Alegre: Sociedade Brasileira de Computação, 2023. p. 42-50. DOI: [10.5753/wapla.2023.236137](https://doi.org/10.5753/wapla.2023.236137).

CHAGAS, P. A.; GOMIDE, J. S.; SANTANA, L. E. A. S. Previsão do risco de evasão universitária utilizando aprendizado de máquina: características e dinâmica da evasão nos cursos de Engenharia da UFRJ-Macaé. **Revista Brasileira de Informática na Educação**, v. 33, p. 1226-1247, 2025. DOI: [10.5753/rbie.2025.5196](https://doi.org/10.5753/rbie.2025.5196).

TINTO, V. Dropout from higher education: a theoretical synthesis of recent research. **Review of Educational Research**, v. 45, n. 1, p. 89-125, 1975. DOI: [10.3102/00346543045001089](https://doi.org/10.3102/00346543045001089).

TINTO, V. **Leaving college**: rethinking the causes and cures of student attrition. 2. ed. Chicago: University of Chicago Press, 1993.

VILLAR, A.; ANDRADE, C. R. V. Supervised machine learning algorithms for predicting student dropout and academic success: a comparative study. **Discover Artificial Intelligence**, v. 4, n. 1, art. 2, 2024. DOI: [10.1007/s44163-023-00079-z](https://doi.org/10.1007/s44163-023-00079-z).

## Equipe

- Karolina Oliveira
- Sabrina Ramos Silveira
