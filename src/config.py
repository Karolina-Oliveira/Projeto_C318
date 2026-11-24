import os
from pathlib import Path


BASE_CSV_PATH = os.getenv("BASE_CSV_PATH")


def caminho_base() -> Path:
    """Devolve o caminho do CSV da base, lido da variável de ambiente BASE_CSV_PATH.

    A variável é lida no momento da chamada, e não na importação, para que um
    notebook possa defini-la depois de importar o módulo.
    """
    valor = os.getenv("BASE_CSV_PATH")
    if not valor:
        raise RuntimeError(
            "A variável de ambiente BASE_CSV_PATH não está definida. "
            "Defina-a com o caminho do Base_academica.csv (veja a seção Dados do README)."
        )
    caminho = Path(valor).expanduser()
    if not caminho.is_file():
        raise FileNotFoundError(
            "BASE_CSV_PATH está definida, mas não aponta para um arquivo existente. "
            "Confira o caminho (veja a seção Dados do README)."
        )
    return caminho
