"""Leitura da base acadêmica v7 (Base_academica.csv).

Formato do arquivo, conforme a seção 2 da Legenda.md:
separador ";", UTF-8 sem BOM, vírgula decimal, datas dd/mm/aa e campo vazio
como único valor ausente.

Esta função só lê e tipa a base. Regras de tratamento (issue #5) e de negócio,
como o evento de saída (issue #6), ficam em outros módulos.
"""

import re
import warnings
from pathlib import Path

import pandas as pd

from src.config import caminho_base


N_COLUNAS_ESPERADO = 66

# Colunas de identificação pessoal que não podem estar na base (nome exato).
COLUNAS_PESSOAIS = ("MATRICULA", "DATANASCIMENTO")

# Trechos de nome que indicariam colunas financeiras ou socioeconômicas.
TRECHOS_FINANCEIROS = ("MENSALIDADE", "BOLSA", "FIES", "FINANCIAMENTO", "RENDA", "VALOR")

# Identificadores com valores vazios: inteiro que aceita nulo, para não virar float.
IDENTIFICADORES = (
    "HANDLEANOSEMESTRE",
    "HANDLEALUNOANOSEMESTRE",
    "HANDLEALUNO",
    "HANDLEALUNOCURRICULO",
    "HANDLECURRICULO",
)

_PADRAO_SEMESTRE = re.compile(r"^(\d{4})/([12])$")


def semestre_para_ordinal(serie: pd.Series) -> pd.Series:
    """Converte semestres no formato 'AAAA/S' em inteiros consecutivos.

    2009/1 -> 4018, 2009/2 -> 4019, 2010/1 -> 4020, ...
    A diferença entre dois valores é o número de semestres entre eles,
    então "semestre seguinte" é sempre o valor + 1.
    """
    texto = serie.astype("string")
    partes = texto.str.extract(_PADRAO_SEMESTRE)
    invalidos = texto.notna() & partes[0].isna()
    if invalidos.any():
        raise ValueError(
            f"{int(invalidos.sum())} valor(es) da coluna {serie.name} fora do formato AAAA/S."
        )
    return (partes[0].astype("Int64") * 2 + partes[1].astype("Int64") - 1).rename(None)


def _conferir_colunas(colunas: pd.Index) -> None:
    pessoais = [c for c in colunas if c.upper() in COLUNAS_PESSOAIS]
    financeiras = [c for c in colunas if any(t in c.upper() for t in TRECHOS_FINANCEIROS)]
    if pessoais or financeiras:
        raise ValueError(
            "A base tem colunas que não fazem parte do estudo "
            f"(pessoais: {pessoais}; financeiras: {financeiras}). "
            "Confira se o arquivo é a base v7."
        )
    if len(colunas) != N_COLUNAS_ESPERADO:
        warnings.warn(
            f"A base tem {len(colunas)} colunas; a legenda da v7 descreve {N_COLUNAS_ESPERADO}. "
            "Confira se o arquivo é a base v7.",
            stacklevel=3,
        )


def carregar_base(caminho: str | Path | None = None) -> pd.DataFrame:
    """Lê a base acadêmica v7 e devolve um DataFrame.

    Parâmetros
    ----------
    caminho : opcional
        Caminho do CSV. Se omitido, usa a variável de ambiente BASE_CSV_PATH.

    O que a função faz:
    - lê o CSV com separador ";", UTF-8 e vírgula decimal;
    - converte as colunas DATA* para datetime (formato dd/mm/aa);
    - lê os identificadores HANDLE* como inteiros (aceitando vazio);
    - cria ANOSEMESTRE_ORD e INGRESSO_ORD, semestres em inteiros consecutivos;
    - confere que não há colunas pessoais ou financeiras e que há 66 colunas.

    O arquivo original não é modificado.
    """
    caminho = Path(caminho) if caminho is not None else caminho_base()

    df = pd.read_csv(
        caminho,
        sep=";",
        encoding="utf-8",
        decimal=",",
        dtype={c: "Int64" for c in IDENTIFICADORES},
        low_memory=False,
    )
    _conferir_colunas(df.columns)

    for coluna in [c for c in df.columns if c.startswith("DATA")]:
        original = df[coluna]
        convertida = pd.to_datetime(original, format="%d/%m/%y", errors="coerce").astype(
            "datetime64[ns]"
        )
        perdidos = int((original.notna() & convertida.isna()).sum())
        if perdidos:
            warnings.warn(
                f"{perdidos} valor(es) de {coluna} não estão no formato dd/mm/aa e viraram nulos.",
                stacklevel=2,
            )
        df[coluna] = convertida

    df["ANOSEMESTRE_ORD"] = semestre_para_ordinal(df["ANOSEMESTRE"])
    df["INGRESSO_ORD"] = semestre_para_ordinal(df["INGRESSO"])
    return df
