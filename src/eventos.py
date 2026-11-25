"""Definições de evento de saída, primeira saída e unidades de análise (issue #6).

Ordem de uso nos notebooks:

    df = carregar_base()
    df = filtrar_graduacao(df)
    df = marcar_evento_saida(df)
    aluno_semestre = consolidar_aluno_semestre(df)
    aluno_semestre = marcar_saida_semestre_seguinte(aluno_semestre)
    alunos = tabela_por_aluno(aluno_semestre)

Definições
----------
Evento de saída (linha): a linha tem ao menos uma das flags TEVEDESISTENCIA,
TEVEABANDONO, TEVECANCELAMENTO ou TEVEDESLIGAMENTO igual a 1. São os mesmos
quatro tipos que alimentam DATAPRIMEIRASAIDA.

Saída por troca: o evento acontece num semestre em que o aluno continua na
instituição por outro caminho, ou seja, tem mudança de curso ou migração de
currículo registrada no semestre, ou tem linha ACADEMICA em outro vínculo
(HANDLEALUNOCURRICULO) no mesmo semestre. Nesses casos o registro de saída
encerra o vínculo antigo e não é tratado como evento de saída.

Evento de saída (aluno-semestre): há evento de saída em alguma linha do aluno
no semestre e ele não é saída por troca.

Primeira saída: o primeiro semestre do aluno com evento de saída.

Não são evento de saída: trancamento, transferência/afastamento, afastamento
sem ocorrência, prazo esgotado, rematrícula, falecimento, mudança de curso,
migração de currículo, diplomação e reingresso.
"""

import pandas as pd


# Código de aluno especial, fora da graduação regular. Identificado na base pela
# concentração de PERIODO = 0 e por não ter outro curso associado; a confirmação
# da sigla junto à fonte é feita na issue #3.
CODIGO_ALUNO_ESPECIAL = "GAE"

FLAGS_SAIDA = {
    "TEVEDESISTENCIA": "Desistência",
    "TEVEABANDONO": "Abandono",
    "TEVECANCELAMENTO": "Cancelamento",
    "TEVEDESLIGAMENTO": "Desligamento",
}

FLAGS_TROCA = ("TEVEMUDANCACURSO", "TEVEMIGRACAOCURRICULO")

CHAVE_ALUNO_SEMESTRE = ["HANDLEALUNO", "ANOSEMESTRE_ORD"]


def filtrar_graduacao(df: pd.DataFrame) -> pd.DataFrame:
    """Remove as linhas do código de aluno especial (fora da graduação regular)."""
    return df.loc[df["SIGLACURSO"] != CODIGO_ALUNO_ESPECIAL].copy()


def marcar_evento_saida(df: pd.DataFrame) -> pd.DataFrame:
    """Acrescenta, em cada linha da base, EVENTO_SAIDA_LINHA (0/1) e TIPO_SAIDA.

    TIPO_SAIDA fica vazio quando não há evento. Na base, nenhuma linha tem mais
    de um tipo de saída ao mesmo tempo; se tiver, vale o primeiro na ordem de
    FLAGS_SAIDA.
    """
    df = df.copy()
    flags = df[list(FLAGS_SAIDA)]
    df["EVENTO_SAIDA_LINHA"] = flags.max(axis=1).astype(int)
    tipo = pd.Series(pd.NA, index=df.index, dtype="string")
    for coluna, nome in reversed(FLAGS_SAIDA.items()):
        tipo = tipo.mask(df[coluna] == 1, nome)
    df["TIPO_SAIDA"] = tipo
    return df


def _linha_principal(df: pd.DataFrame) -> pd.DataFrame:
    """Escolhe uma linha por aluno-semestre para curso, turno e indicadores.

    Prioridade: linha ACADEMICA; entre várias, a do vínculo de ingresso mais
    recente (INGRESSO_ORD); persistindo o empate, a com mais disciplinas
    matriculadas (IA75_04).
    """
    ordenado = df.assign(_academica=(df["ORIGEMREGISTRO"] == "ACADEMICA").astype(int)).sort_values(
        [*CHAVE_ALUNO_SEMESTRE, "_academica", "INGRESSO_ORD", "IA75_04"],
        ascending=[True, True, False, False, False],
        na_position="last",
    )
    return ordenado.drop_duplicates(CHAVE_ALUNO_SEMESTRE, keep="first").drop(columns="_academica")


def consolidar_aluno_semestre(df: pd.DataFrame) -> pd.DataFrame:
    """Devolve uma linha por aluno e semestre.

    Espera a saída de marcar_evento_saida(). Colunas:
    - todas as colunas da linha principal (curso, turno, período e indicadores
      acadêmicos vêm da mesma linha; ver _linha_principal);
    - flags TEVE* com o máximo entre as linhas do semestre;
    - datas DATA* com a menor data entre as linhas do semestre;
    - N_LINHAS: quantas linhas a base tinha para o aluno no semestre;
    - TEM_ACADEMICA: 1 se alguma linha é ACADEMICA (o aluno cursou o semestre);
    - EVENTO_SAIDA_BRUTO: 1 se alguma linha tem evento de saída;
    - SAIDA_POR_TROCA: 1 se o evento acontece junto com uma troca de curso ou
      currículo (ver o docstring do módulo);
    - EVENTO_SAIDA: EVENTO_SAIDA_BRUTO sem as saídas por troca;
    - TIPO_SAIDA: tipo do evento de saída, quando houver.
    """
    if "EVENTO_SAIDA_LINHA" not in df.columns:
        raise ValueError("Chame marcar_evento_saida(df) antes de consolidar_aluno_semestre(df).")

    principal = _linha_principal(df).set_index(CHAVE_ALUNO_SEMESTRE)
    grupos = df.groupby(CHAVE_ALUNO_SEMESTRE)

    flags = [c for c in df.columns if c.startswith("TEVE")]
    datas = [c for c in df.columns if c.startswith("DATA")]
    principal[flags] = grupos[flags].max()
    principal[datas] = grupos[datas].min()
    principal["N_LINHAS"] = grupos.size()
    principal["TEM_ACADEMICA"] = grupos["ORIGEMREGISTRO"].agg(lambda s: int((s == "ACADEMICA").any()))
    principal["EVENTO_SAIDA_BRUTO"] = grupos["EVENTO_SAIDA_LINHA"].max()

    # Vínculos com evento × vínculos com linha ACADEMICA no mesmo semestre.
    vinc_evento = (
        df.loc[df["EVENTO_SAIDA_LINHA"] == 1]
        .groupby(CHAVE_ALUNO_SEMESTRE)["HANDLEALUNOCURRICULO"]
        .agg(set)
    )
    vinc_academica = (
        df.loc[df["ORIGEMREGISTRO"] == "ACADEMICA"]
        .groupby(CHAVE_ALUNO_SEMESTRE)["HANDLEALUNOCURRICULO"]
        .agg(set)
    )
    comparacao = pd.DataFrame({"evento": vinc_evento}).join(vinc_academica.rename("academica"))
    academica_em_outro_vinculo = comparacao.apply(
        lambda r: isinstance(r["academica"], set) and bool(r["academica"] - r["evento"]), axis=1
    )
    principal["_outro_vinculo"] = academica_em_outro_vinculo.reindex(principal.index, fill_value=False)
    principal["_troca_registrada"] = principal[list(FLAGS_TROCA)].max(axis=1) == 1

    principal["SAIDA_POR_TROCA"] = (
        (principal["EVENTO_SAIDA_BRUTO"] == 1)
        & (principal["_outro_vinculo"] | principal["_troca_registrada"])
    ).astype(int)
    principal["EVENTO_SAIDA"] = (
        (principal["EVENTO_SAIDA_BRUTO"] == 1) & (principal["SAIDA_POR_TROCA"] == 0)
    ).astype(int)

    tipo = (
        df.loc[df["EVENTO_SAIDA_LINHA"] == 1]
        .sort_values("DATAPRIMEIRASAIDA")
        .groupby(CHAVE_ALUNO_SEMESTRE)["TIPO_SAIDA"]
        .first()
    )
    principal["TIPO_SAIDA"] = tipo.reindex(principal.index).where(principal["EVENTO_SAIDA"] == 1)

    resultado = principal.drop(columns=["_outro_vinculo", "_troca_registrada", "EVENTO_SAIDA_LINHA"])
    return resultado.reset_index().sort_values(CHAVE_ALUNO_SEMESTRE, ignore_index=True)


def primeira_saida(aluno_semestre: pd.DataFrame) -> pd.DataFrame:
    """Uma linha por aluno com evento de saída: semestre e tipo da primeira saída."""
    saidas = aluno_semestre.loc[aluno_semestre["EVENTO_SAIDA"] == 1]
    primeira = saidas.sort_values(CHAVE_ALUNO_SEMESTRE).drop_duplicates("HANDLEALUNO", keep="first")
    return primeira.set_index("HANDLEALUNO")[["ANOSEMESTRE", "ANOSEMESTRE_ORD", "TIPO_SAIDA"]].rename(
        columns={
            "ANOSEMESTRE": "PRIMEIRA_SAIDA",
            "ANOSEMESTRE_ORD": "PRIMEIRA_SAIDA_ORD",
            "TIPO_SAIDA": "TIPO_PRIMEIRA_SAIDA",
        }
    )


def marcar_saida_semestre_seguinte(aluno_semestre: pd.DataFrame) -> pd.DataFrame:
    """Acrescenta o rótulo da modelagem e a posição em relação à primeira saída.

    - PRIMEIRA_SAIDA_ORD: semestre da primeira saída do aluno (vazio se não tem);
    - ANTES_PRIMEIRA_SAIDA: 1 se o semestre é anterior à primeira saída, ou se o
      aluno nunca teve saída;
    - SAIDA_SEMESTRE_SEGUINTE: 1 se a primeira saída acontece no semestre
      calendário seguinte (ANOSEMESTRE_ORD + 1), 0 se não; vazio nos semestres
      da primeira saída em diante, que ficam fora da modelagem.
    """
    resultado = aluno_semestre.drop(
        columns=["PRIMEIRA_SAIDA_ORD", "ANTES_PRIMEIRA_SAIDA", "SAIDA_SEMESTRE_SEGUINTE"], errors="ignore"
    )
    primeira = primeira_saida(resultado)["PRIMEIRA_SAIDA_ORD"]
    resultado = resultado.merge(primeira, left_on="HANDLEALUNO", right_index=True, how="left")
    antes = resultado["PRIMEIRA_SAIDA_ORD"].isna() | (
        resultado["ANOSEMESTRE_ORD"] < resultado["PRIMEIRA_SAIDA_ORD"]
    )
    antes = antes.fillna(False).astype(bool)
    resultado["ANTES_PRIMEIRA_SAIDA"] = antes.astype(int)
    seguinte = (resultado["PRIMEIRA_SAIDA_ORD"] == resultado["ANOSEMESTRE_ORD"] + 1).fillna(False)
    resultado["SAIDA_SEMESTRE_SEGUINTE"] = seguinte.astype("Int64").where(antes)
    return resultado


def tabela_por_aluno(aluno_semestre: pd.DataFrame) -> pd.DataFrame:
    """Uma linha por aluno, com os atributos do primeiro semestre e o desfecho.

    Curso, turno e período de ingresso mudam ao longo da base para parte dos
    alunos (troca de curso, migração de currículo); aqui vale o primeiro
    semestre do aluno. INGRESSO é o do primeiro vínculo (menor INGRESSO_ORD).

    Colunas de desfecho:
    - TEVE_SAIDA, PRIMEIRA_SAIDA, PRIMEIRA_SAIDA_ORD, TIPO_PRIMEIRA_SAIDA;
    - N_SEMESTRES_SAIDA: quantos semestres com evento de saída o aluno tem;
    - CURSOU_DEPOIS: 1 se tem semestre ACADEMICA depois da primeira saída;
    - REINGRESSO_DEPOIS e DIPLOMACAO_DEPOIS: 1 se há reingresso ou diplomação
      em semestre posterior à primeira saída.
    """
    ordenado = aluno_semestre.sort_values(CHAVE_ALUNO_SEMESTRE)
    primeiro = ordenado.drop_duplicates("HANDLEALUNO", keep="first").set_index("HANDLEALUNO")
    grupos = ordenado.groupby("HANDLEALUNO")

    alunos = pd.DataFrame(
        {
            "PRIMEIRO_SEMESTRE": primeiro["ANOSEMESTRE"],
            "PRIMEIRO_SEMESTRE_ORD": primeiro["ANOSEMESTRE_ORD"],
            "SIGLACURSO": primeiro["SIGLACURSO"],
            "TURNO": primeiro["TURNO"],
            "SEXO": grupos["SEXO"].agg(lambda s: s.dropna().iloc[0] if s.notna().any() else pd.NA),
            "INGRESSO_ORD": grupos["INGRESSO_ORD"].min(),
            "N_SEMESTRES": grupos.size(),
            "N_SEMESTRES_SAIDA": grupos["EVENTO_SAIDA"].sum(),
        }
    )
    ingresso = ordenado.loc[
        ordenado["INGRESSO_ORD"] == ordenado["HANDLEALUNO"].map(alunos["INGRESSO_ORD"]), ["HANDLEALUNO", "INGRESSO"]
    ].drop_duplicates("HANDLEALUNO")
    alunos["INGRESSO"] = ingresso.set_index("HANDLEALUNO")["INGRESSO"]

    alunos = alunos.join(primeira_saida(aluno_semestre))
    alunos["TEVE_SAIDA"] = alunos["PRIMEIRA_SAIDA_ORD"].notna().astype(int)

    depois = ordenado.drop(columns=["PRIMEIRA_SAIDA_ORD"], errors="ignore").merge(
        alunos["PRIMEIRA_SAIDA_ORD"], left_on="HANDLEALUNO", right_index=True
    )
    depois = depois.loc[depois["ANOSEMESTRE_ORD"] > depois["PRIMEIRA_SAIDA_ORD"]].groupby("HANDLEALUNO")
    for coluna, origem in [
        ("CURSOU_DEPOIS", "TEM_ACADEMICA"),
        ("REINGRESSO_DEPOIS", "TEVEREINGRESSO"),
        ("DIPLOMACAO_DEPOIS", "TEVEDIPLOMACAO"),
    ]:
        valores = depois[origem].max().reindex(alunos.index).fillna(0).astype("Int64")
        alunos[coluna] = valores.where(alunos["TEVE_SAIDA"] == 1)

    colunas = [
        "PRIMEIRO_SEMESTRE", "PRIMEIRO_SEMESTRE_ORD", "SIGLACURSO", "TURNO", "SEXO", "INGRESSO", "INGRESSO_ORD",
        "N_SEMESTRES", "TEVE_SAIDA", "PRIMEIRA_SAIDA", "PRIMEIRA_SAIDA_ORD", "TIPO_PRIMEIRA_SAIDA",
        "N_SEMESTRES_SAIDA", "CURSOU_DEPOIS", "REINGRESSO_DEPOIS", "DIPLOMACAO_DEPOIS",
    ]
    return alunos[colunas]
