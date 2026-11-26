"""Comparação entre o semestre anterior à primeira saída e colegas sem saída.

Usado na issue #9 (P4) e reaproveitável na #10.

Regras:
- Semestre anterior à saída: para cada aluno com evento de saída, o último
  semestre estritamente anterior à primeira saída em que ele cursou o semestre
  (linha ACADEMICA). Pode não ser o semestre imediatamente anterior, por
  exemplo quando há um trancamento no meio.
- Grupo de comparação: semestres ACADEMICA, no mesmo semestre e curso, de
  alunos que ainda não tinham tido evento de saída naquele momento (inclui
  alunos que só vão sair mais tarde, e exclui os próprios semestres anteriores
  à saída).
- Pesos: cada célula semestre × curso pesa no grupo de comparação o mesmo que
  pesa no grupo com saída. Assim a comparação não depende de quantos colegas
  cada célula tem.
"""

import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu


CELULA = ["ANOSEMESTRE_ORD", "SIGLACURSO"]
INDICADORES = {
    "CRENOSEMESTRE": "CRE do semestre",
    "CREATESEMESTRE": "CRE acumulado",
    "IA04_01": "Frequência (%)",
    "IA04_02": "Disciplinas com mais de 25% de faltas",
    "IA34_03": "Reprovações no semestre",
    "IA65_03": "Retiradas no semestre",
}


def preparar_indicadores(aluno_semestre: pd.DataFrame) -> pd.DataFrame:
    """Aplica as decisões de tratamento da issue #5 aos indicadores usados aqui.

    Frequência acima de 100 é inválida (a legenda já aponta esses casos) e vira
    ausente. Os demais vazios continuam vazios: não são trocados por zero.
    """
    resultado = aluno_semestre.copy()
    resultado["IA04_01"] = resultado["IA04_01"].where(resultado["IA04_01"] <= 100)
    return resultado


def semestre_anterior_a_saida(aluno_semestre: pd.DataFrame) -> pd.DataFrame:
    """Uma linha por aluno com saída: o último semestre cursado antes da primeira saída.

    Espera a saída de marcar_saida_semestre_seguinte(). Acrescenta
    SEMESTRES_ATE_SAIDA (1 = semestre imediatamente anterior à saída).
    Alunos sem semestre ACADEMICA anterior (em geral, porque a primeira saída
    é no primeiro semestre em que aparecem na base) ficam de fora.
    """
    candidatos = aluno_semestre.loc[
        (aluno_semestre["TEM_ACADEMICA"] == 1)
        & (aluno_semestre["ANTES_PRIMEIRA_SAIDA"] == 1)
        & aluno_semestre["PRIMEIRA_SAIDA_ORD"].notna()
    ]
    anterior = candidatos.sort_values("ANOSEMESTRE_ORD").drop_duplicates("HANDLEALUNO", keep="last")
    anterior = anterior.assign(
        SEMESTRES_ATE_SAIDA=(anterior["PRIMEIRA_SAIDA_ORD"] - anterior["ANOSEMESTRE_ORD"]).astype(int)
    )
    return anterior.sort_values(CELULA, ignore_index=True)


def montar_grupos(aluno_semestre: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Devolve (saida, comparacao), só com células semestre × curso que têm os dois grupos.

    A coluna GRUPO_PESO da comparação já traz o peso da célula
    (alunos com saída na célula / semestres de comparação na célula).
    """
    anterior = semestre_anterior_a_saida(aluno_semestre)
    cursados = aluno_semestre.loc[
        (aluno_semestre["TEM_ACADEMICA"] == 1) & (aluno_semestre["ANTES_PRIMEIRA_SAIDA"] == 1)
    ]
    chave_anterior = pd.MultiIndex.from_frame(anterior[["HANDLEALUNO", "ANOSEMESTRE_ORD"]])
    chave_cursados = pd.MultiIndex.from_frame(cursados[["HANDLEALUNO", "ANOSEMESTRE_ORD"]])
    comparacao = cursados.loc[~chave_cursados.isin(chave_anterior)]

    celulas_saida = anterior.groupby(CELULA).size().rename("n_saida")
    celulas_comp = comparacao.groupby(CELULA).size().rename("n_comp")
    celulas = pd.concat([celulas_saida, celulas_comp], axis=1, join="inner")

    saida = anterior.merge(celulas, left_on=CELULA, right_index=True)
    comparacao = comparacao.merge(celulas, left_on=CELULA, right_index=True)
    saida["GRUPO_PESO"] = 1.0
    comparacao["GRUPO_PESO"] = comparacao["n_saida"] / comparacao["n_comp"]
    return saida.drop(columns=["n_saida", "n_comp"]), comparacao.drop(columns=["n_saida", "n_comp"])


def quantil_ponderado(valores, pesos, q):
    """Quantil q (0 a 1) de valores com pesos (CDF invertida). Ignora valores ausentes.

    Devolve o menor valor cuja proporção acumulada de peso chega a q, então
    um valor com peso 3 conta como o mesmo valor repetido 3 vezes.
    """
    valores = np.asarray(valores, dtype=float)
    pesos = np.asarray(pesos, dtype=float)
    validos = ~np.isnan(valores)
    valores, pesos = valores[validos], pesos[validos]
    ordem = np.argsort(valores, kind="stable")
    valores, pesos = valores[ordem], pesos[ordem]
    acumulado = np.cumsum(pesos) / pesos.sum()
    return float(valores[np.searchsorted(acumulado, q - 1e-12)])


def _pesos_da_variavel(saida, comparacao, coluna):
    """Recalcula os pesos da comparação só com quem tem a variável preenchida."""
    s = saida.loc[saida[coluna].notna()]
    c = comparacao.loc[comparacao[coluna].notna()]
    n_s = s.groupby(CELULA).size()
    n_c = c.groupby(CELULA).size()
    celulas = n_s.index.intersection(n_c.index)
    s = s.set_index(CELULA).loc[lambda d: d.index.isin(celulas)].reset_index()
    c = c.set_index(CELULA).loc[lambda d: d.index.isin(celulas)].reset_index()
    peso = (n_s / n_c).reindex(pd.MultiIndex.from_frame(c[CELULA])).to_numpy()
    return s, c.assign(GRUPO_PESO=peso)


def probabilidade_superioridade(saida, comparacao, coluna):
    """Chance de um aluno com saída ter valor maior que um colega do mesmo semestre e curso.

    É a estatística U de Mann-Whitney dividida por n1 × n2, calculada dentro de
    cada célula e combinada com peso igual ao número de alunos com saída na
    célula. 0,5 = sem diferença; abaixo de 0,5 = o grupo com saída tende a ter
    valores menores. Empates contam meio.
    """
    s, c = _pesos_da_variavel(saida, comparacao, coluna)
    total, peso_total = 0.0, 0
    for celula, grupo_s in s.groupby(CELULA):
        x = grupo_s[coluna].to_numpy(dtype=float)
        y = c.loc[(c[CELULA[0]] == celula[0]) & (c[CELULA[1]] == celula[1]), coluna].to_numpy(dtype=float)
        u = mannwhitneyu(x, y, alternative="two-sided").statistic
        total += len(x) * u / (len(x) * len(y))
        peso_total += len(x)
    return total / peso_total


def resumo_ponderado(saida: pd.DataFrame, comparacao: pd.DataFrame, colunas=None) -> pd.DataFrame:
    """Tabela por indicador: n, ausentes, média, mediana, quartis e probabilidade de superioridade."""
    colunas = colunas or list(INDICADORES)
    linhas = []
    for coluna in colunas:
        s, c = _pesos_da_variavel(saida, comparacao, coluna)
        linha = {
            "Indicador": INDICADORES.get(coluna, coluna),
            "n saída (alunos)": s["HANDLEALUNO"].nunique(),
            "ausentes saída": int(saida[coluna].isna().sum()),
            "n comparação (semestres)": len(c),
            "média saída": s[coluna].mean(),
            "média comparação": np.average(c[coluna], weights=c["GRUPO_PESO"]),
            "mediana saída": quantil_ponderado(s[coluna], np.ones(len(s)), 0.5),
            "mediana comparação": quantil_ponderado(c[coluna], c["GRUPO_PESO"], 0.5),
            "prob. superioridade": probabilidade_superioridade(saida, comparacao, coluna),
        }
        linhas.append(linha)
    return pd.DataFrame(linhas).set_index("Indicador")


def proporcao_ao_menos_um(saida: pd.DataFrame, comparacao: pd.DataFrame, coluna: str) -> tuple[float, float]:
    """Percentual de semestres com valor >= 1 (saída, comparação ponderada).

    Mais legível que o boxplot para contagens em que a maioria dos valores é zero.
    """
    s, c = _pesos_da_variavel(saida, comparacao, coluna)
    p_saida = (s[coluna] >= 1).mean() * 100
    p_comp = np.average(c[coluna] >= 1, weights=c["GRUPO_PESO"]) * 100
    return float(p_saida), float(p_comp)


def estatisticas_boxplot(valores, pesos=None, label=""):
    """Estatísticas para matplotlib.axes.Axes.bxp, com bigodes no 5º e no 95º percentil.

    Não devolve pontos extremos: cada ponto seria o valor de um aluno.
    """
    valores = np.asarray(valores, dtype=float)
    pesos = np.ones_like(valores) if pesos is None else np.asarray(pesos, dtype=float)
    q = {p: quantil_ponderado(valores, pesos, p) for p in (0.05, 0.25, 0.5, 0.75, 0.95)}
    return {
        "label": label,
        "whislo": q[0.05], "q1": q[0.25], "med": q[0.5], "q3": q[0.75], "whishi": q[0.95],
        "fliers": [],
    }
