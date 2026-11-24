# Projeto C318 - Fundamentos de Machine Learning

## Configuração local da base

Os arquivos da base são restritos e não devem ser versionados. Mantenha o CSV somente em `data/` e defina `BASE_CSV_PATH` para o caminho do arquivo antes de abrir os notebooks.

No PowerShell, a partir da raiz do repositório:

```powershell
$env:BASE_CSV_PATH = (Resolve-Path "data/Base_academica.csv").Path
```

Essa definição vale para a sessão atual do PowerShell. Ative o ambiente virtual e inicie o Jupyter:

```powershell
.\.venv\Scripts\Activate.ps1
jupyter lab
```

No Linux/macOS, use `export BASE_CSV_PATH="$(pwd)/data/Base_academica.csv"` antes de iniciar o Jupyter.

## Contexto


## Problema de negócio


## Perguntas de negócio


## Enquadramento do problema

Análise exploratória de dados, com modelagem supervisionada opcional.

## Dados


## Metodologia


## Resultados


## Equipe

- Karolina Oliveira
- Sabrina Ramos Silveira
