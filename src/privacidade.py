"""Regras de privacidade para tabelas e gráficos publicados.

Grupos com menos de 10 alunos não aparecem com o número exato, para não permitir
identificar pessoas (regra do projeto).
"""

import pandas as pd


LIMITE_MINIMO = 10


def ocultar_contagens_pequenas(contagens, limite: int = LIMITE_MINIMO):
    """Troca contagens entre 1 e limite - 1 por "<10" (ou "<limite").

    Aceita Series ou DataFrame de contagens e devolve uma cópia em texto, pronta
    para exibir. Zero continua aparecendo como 0.
    """
    rotulo = f"<{limite}"

    def formatar(valor):
        if pd.isna(valor):
            return valor
        return rotulo if 0 < valor < limite else f"{int(valor):,}".replace(",", ".")

    if isinstance(contagens, pd.DataFrame):
        return contagens.apply(lambda coluna: coluna.map(formatar))
    return contagens.map(formatar)
