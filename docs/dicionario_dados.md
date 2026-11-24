# Dicionário de dados — Base acadêmica v7

Cada linha representa um aluno em um semestre e currículo. A mesma pessoa pode aparecer em diferentes semestres e currículos. Campos `HANDLE*` são identificadores internos usados para relacionar registros, sem significado quantitativo; nunca devem ser exibidos em tabelas ou gráficos. Campo vazio não equivale a zero.

| Coluna | Significado | Tipo | Grupo temático | Observações |
|---|---|---|---|---|
| `HANDLEANOSEMESTRE` | Código interno do semestre | identificador | identificação | Sem significado numérico ou ordem; 100% preenchido segundo a legenda. |
| `ANOSEMESTRE` | Semestre ao qual a linha se refere | categórica (período letivo) | tempo | Formato `AAAA/S`; legenda indica 2009/1 a 2026/1. |
| `HANDLEALUNOANOSEMESTRE` | Código interno da matrícula do aluno no semestre | identificador | identificação | 81,7% preenchido; vazio quando não há registro de matrícula. |
| `HANDLEALUNO` | Código interno do aluno, usado para juntar seus registros | identificador | identificação | Não exibir valores nem calcular categorias/contagens distintas. |
| `HANDLEALUNOCURRICULO` | Código interno do vínculo do aluno com o currículo | identificador | identificação | Sem interpretação quantitativa. |
| `HANDLECURRICULO` | Código interno do currículo | identificador | identificação | Sem interpretação quantitativa. |
| `PERIODO` | Período curricular do aluno no semestre | numérica (ordinal) | curso/vínculo | Legenda indica 0 a 10; 0 ocorre quase somente no código de aluno especial; 75,5% preenchido. |
| `SIGLACURSO` | Código do curso do currículo | categórica | curso/vínculo | 12 códigos segundo a legenda; categorias agregadas aparecem no notebook. |
| `TURNO` | Turno do currículo | categórica | curso/vínculo | Legenda cita Integral e Noturno. |
| `CRENOSEMESTRE` | Coeficiente de rendimento escolar no semestre | numérica | acadêmica | Faixa indicada 0–100; 72,2% preenchido. |
| `CREATESEMESTRE` | CRE acumulado até o semestre | numérica | acadêmica | Faixa indicada 0–100; 75,9% preenchido. |
| `MEDIANAATESEMESTRE` | Mediana das notas até o semestre | numérica | acadêmica | Faixa indicada 0–100; 72,2% preenchido. |
| `SEXO` | Sexo registrado no cadastro | categórica | perfil | Legenda cita M e F; 99,97% preenchido. |
| `MATRICULAEFETIVADA` | Situação do registro de matrícula no semestre | categórica | curso/vínculo | S = efetivada; N = não efetivada; vazio = sem registro de matrícula. 81,7% preenchido. |
| `CODIGOSTATUSALUNO` | Código da situação do aluno no semestre | categórica (código) | curso/vínculo | Códigos correspondem a `STATUSALUNO`; 80,8% preenchido. |
| `STATUSALUNO` | Situação do aluno registrada ao fim do semestre | categórica | curso/vínculo | Ativo, Inativo, Matrícula Pendente, Em Mobilidade Acadêmica, Matrícula Alterada e Desconhecido (quando o código está vazio). |
| `INGRESSO` | Semestre de ingresso do aluno no currículo | categórica (período letivo) | tempo | Não representa forma de admissão; legenda indica 2009/1 a 2026/1. |
| `APROVEIT` | Semestres aproveitados quando o aluno ingressa no currículo | numérica (contagem) | acadêmica | Legenda indica 1–23; vazio significa nenhum semestre aproveitado (o sistema não grava zero); repete-se no currículo. 14,9% preenchido. |
| `TEVEDESISTENCIA` | Indica ao menos uma desistência no semestre | flag 0/1 | ocorrência | 1 indica ocorrência; evento de saída não equivale a evasão definitiva. |
| `TEVEABANDONO` | Indica ao menos uma desistência por abandono no semestre | flag 0/1 | ocorrência | Evento de saída não equivale a evasão definitiva. |
| `TEVETRANCAMENTO` | Indica ao menos um trancamento de matrícula | flag 0/1 | ocorrência | Pode constar em linhas acadêmicas e de ocorrência. |
| `TEVECANCELAMENTO` | Indica ao menos um cancelamento no semestre | flag 0/1 | ocorrência | Evento de saída não equivale a evasão definitiva. |
| `TEVEDESLIGAMENTO` | Indica ao menos um desligamento no semestre | flag 0/1 | ocorrência | Evento de saída não equivale a evasão definitiva. |
| `TEVETRANSAFASTAMENTO` | Indica transferência/afastamento no semestre | flag 0/1 | ocorrência | Grafia igual à do CSV v7 local. |
| `TEVEDIPLOMACAO` | Indica diplomação no semestre | flag 0/1 | ocorrência | Indicador de ocorrência. |
| `TEVECONCLUSAOPROGRAMA` | Indica conclusão de programa no semestre | flag 0/1 | ocorrência | Legenda informa que não ocorre na base. |
| `TEVEREINGRESSO` | Indica reingresso no semestre | flag 0/1 | ocorrência | Indicador de ocorrência. |
| `TEVEMUDANCACURSO` | Indica mudança de curso no semestre | flag 0/1 | ocorrência | Indicador de ocorrência. |
| `TEVEMIGRACAOCURRICULO` | Indica migração de currículo no semestre | flag 0/1 | ocorrência | Indicador de ocorrência. |
| `QUANTIDADEOCORRENCIAS` | Número de registros de ocorrência no currículo e semestre | numérica (contagem) | ocorrência | Faixa indicada 0–2; 100% preenchido. |
| `DATADESISTENCIA` | Data da primeira desistência no semestre | data | ocorrência | Data administrativa, não necessariamente o dia em que o aluno deixou de frequentar; vazia sem ocorrência. |
| `DATAABANDONO` | Data da primeira desistência por abandono no semestre | data | ocorrência | Data administrativa; vazia sem ocorrência. |
| `DATATRANCAMENTO` | Data do primeiro trancamento no semestre | data | ocorrência | Data administrativa; vazia sem ocorrência. |
| `DATACANCELAMENTO` | Data do primeiro cancelamento no semestre | data | ocorrência | Data administrativa; vazia sem ocorrência. |
| `DATADESLIGAMENTO` | Data do primeiro desligamento no semestre | data | ocorrência | Data administrativa; vazia sem ocorrência. |
| `DATATRANSAFASTAMENTO` | Data da primeira transferência/afastamento no semestre | data | ocorrência | Data administrativa; vazia sem ocorrência. |
| `DATADIPLOMACAO` | Data da primeira diplomação no semestre | data | ocorrência | Data administrativa; vazia sem ocorrência. |
| `DATACONCLUSAOPROGRAMA` | Data da primeira conclusão de programa no semestre | data | ocorrência | Legenda informa que a ocorrência não aparece na base. |
| `DATAREINGRESSO` | Data do primeiro reingresso no semestre | data | ocorrência | Data administrativa; vazia sem ocorrência. |
| `DATAMUDANCACURSO` | Data da primeira mudança de curso no semestre | data | ocorrência | Data administrativa; vazia sem ocorrência. |
| `DATAMIGRACAOCURRICULO` | Data da primeira migração de currículo no semestre | data | ocorrência | Data administrativa; vazia sem ocorrência. |
| `DATAPRIMEIRASAIDA` | Primeira data de saída no semestre entre desistência, abandono, cancelamento e desligamento | data | ocorrência | 6,5% preenchido segundo a legenda. |
| `DATAULTIMASAIDA` | Última data de saída no semestre entre os mesmos quatro tipos | data | ocorrência | 6,5% preenchido segundo a legenda. |
| `DATAINCLUSAOSAIDA` | Data em que a primeira saída foi lançada no sistema | data | ocorrência | Pode indicar lançamento retroativo; 6,5% preenchido. |
| `QTDOCORRENCIASSEMDATA` | Quantidade de ocorrências sem data | numérica (contagem) | ocorrência | Legenda informa que é sempre 0; 100% preenchido. |
| `TEVEREMATRICULA` | Indica rematrícula no semestre | flag 0/1 | ocorrência | Legenda observa que, na maioria dos casos, não tem relação com saída. |
| `TEVEFALECIMENTO` | Indica ocorrência de falecimento | flag 0/1 | ocorrência | Informação sensível; tratar somente de forma agregada. |
| `TEVEPRAZOESGOTADO` | Indica prazo de integralização esgotado | flag 0/1 | ocorrência | Legenda informa que, na prática, não encerra o vínculo. |
| `TEVEAFASTAMENTOSEMOCORRENCIA` | Indica afastamento sem ocorrência | flag 0/1 | ocorrência | Legenda descreve o intervalo entre uma saída e o retorno. |
| `DATAREMATRICULA` | Data da primeira rematrícula no semestre | data | ocorrência | Data administrativa; vazia sem ocorrência. |
| `DATAFALECIMENTO` | Data do primeiro registro de falecimento no semestre | data | ocorrência | Informação sensível; data administrativa. |
| `DATAPRAZOESGOTADO` | Data do primeiro registro de prazo esgotado | data | ocorrência | Data administrativa; vazia sem ocorrência. |
| `DATAAFASTAMENTOSEMOCORRENCIA` | Data do primeiro afastamento sem ocorrência | data | ocorrência | Data administrativa; vazia sem ocorrência. |
| `ORIGEMREGISTRO` | Origem da linha: ACADEMICA ou OCORRENCIA | categórica | identificação | Legenda: 44.417 linhas acadêmicas e 14.642 de ocorrência. Indicadores letivos podem ficar vazios em OCORRENCIA. |
| `IA04_01` | Frequência no semestre | numérica (percentual) | acadêmica | Faixa esperada 0–100; legenda aponta dois valores acima de 100 como inválidos; 71,6% preenchido. |
| `IA04_02` | Disciplinas com mais de 25% de faltas no semestre | numérica (contagem) | acadêmica | Faixa 0–10; 71,6% preenchido. |
| `IA75_01` | Total de disciplinas obrigatórias da grade do currículo | numérica (contagem) | acadêmica | Faixa 4–69; vazio nas linhas OCORRENCIA. |
| `IA75_02` | Disciplinas obrigatórias concluídas até o semestre no currículo | numérica (contagem) | acadêmica | Inclui disciplinas aproveitadas em migração de currículo; faixa 0–69. |
| `IA75_03` | Disciplinas aprovadas no semestre entre as cursadas em turma | numérica (contagem) | acadêmica | Faixa 0–12. |
| `IA75_04` | Disciplinas matriculadas no semestre | numérica (contagem) | acadêmica | Faixa 0–13. |
| `IA75_05` | Disciplinas obrigatórias previstas para o período do aluno | numérica (contagem) | acadêmica | Faixa 0–12. |
| `IA34_03` | Disciplinas reprovadas no semestre | numérica (contagem) | acadêmica | Faixa 0–11. |
| `IA65_03` | Disciplinas retiradas ou canceladas pelo aluno no semestre | numérica (contagem) | acadêmica | Faixa 0–9. |
| `ATIVCOMPL_MATRICULADAS` | Atividades complementares matriculadas no semestre | numérica (contagem) | acadêmica | Faixa 0–13; vazio nas linhas OCORRENCIA. |
| `ATIVCOMPL_APROVADAS` | Atividades complementares aprovadas no semestre | numérica (contagem) | acadêmica | Faixa 0–12; vazio nas linhas OCORRENCIA. |
| `ATIVCOMPL_REPROVADAS` | Atividades complementares reprovadas no semestre | numérica (contagem) | acadêmica | Faixa 0–10; vazio nas linhas OCORRENCIA. |

## Divergências entre a legenda e o CSV

- Os dois arquivos locais são da versão v7. Legenda e CSV têm 66 colunas e os nomes estão alinhados.
- `TEVETRANSAFASTAMENTO` e `DATATRANSAFASTAMENTO` têm a mesma grafia no CSV e na legenda v7. A grafia antiga `TEVETRASAFASTAMENTO` não aparece nos arquivos atuais.
- A legenda informa 12 códigos de curso, sem enumerar as siglas. `GAE` aparece em `SIGLACURSO` no CSV, mas não está documentada nominalmente na legenda.
- `VALORMENSALIDADE`, `MATRICULA` e `DATANASCIMENTO` não aparecem no CSV nem na legenda; a legenda informa que dados financeiros e identificadores pessoais não fazem parte da extração.
- Este checkout não contém `notebooks/00_carga_base.ipynb`; não foi possível validar esse notebook ou comparar seus totais com a issue #2.

## Cuidados de interpretação

Evento de saída registrado não significa evasão definitiva: o aluno pode retornar. Diferenças entre grupos indicam associação, não causalidade. Nas linhas `OCORRENCIA`, indicadores que dependem do semestre cursado podem ficar vazios porque não houve matrícula efetivada; vazio e zero são diferentes. As datas de ocorrência são datas administrativas de registro.
