# Projeto C318 - Fundamentos de Machine Learning

## Contexto


## Problema de negócio


## Perguntas de negócio


## Enquadramento do problema

Análise exploratória de dados, com modelagem supervisionada opcional.

## Dados

### A base

O projeto usa a **base acadêmica v7** (`Base_academica.csv`), uma extração do sistema acadêmico de uma instituição de ensino superior com a trajetória semestral dos alunos de 2009/1 a 2026/1. Cada linha é um aluno em um semestre e currículo. A base traz dados acadêmicos, de vínculo, sexo e ocorrências. Ela **não** contém matrícula, data de nascimento, dados financeiros nem dados socioeconômicos.

O significado de cada coluna está na `Legenda.md`, que acompanha a base.

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


## Resultados


## Equipe

- Karolina Oliveira
- Sabrina Ramos Silveira
