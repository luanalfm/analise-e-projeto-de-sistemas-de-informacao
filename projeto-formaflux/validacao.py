
"""
FormaFlux - Validacao de Entradas Numericas.

Modulo responsavel pela padronizacao e conversao das entradas
numericas para o tipo Decimal.

Centraliza a validacao dos formatos de entrada, garantindo
consistencia entre as interfaces CLI e GUI e evitando
a duplicacao de codigo.
"""

import re
from decimal import Decimal, InvalidOperation


def converter_decimal(texto: str) -> Decimal:
    texto = texto.strip()

    # Aceita ponto ou virgula como separador decimal,
    # sem separadores de milhar.
    if not re.fullmatch(r"[+-]?[0-9]+(?:[.,][0-9]+)?", texto):
        raise ValueError(
            "Digite um numero valido, sem separador de milhar (ex.: 1000,00)."
        )

    try:
        numero = Decimal(texto.replace(",", "."))
    except InvalidOperation:
        raise ValueError("Digite um numero valido.") from None

    if not numero.is_finite():
        raise ValueError("O valor precisa ser um numero finito.")

    return numero
