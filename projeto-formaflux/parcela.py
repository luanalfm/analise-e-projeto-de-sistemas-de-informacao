"""
FormaFlux - Representacao de Parcela.

Modulo responsavel pela representacao dos recebiveis da turma,
considerando identificador, valor nominal e prazo em meses.

Aplica encapsulamento por meio de atributos protegidos,
propriedades e setters, preservando a integridade dos dados
e o cumprimento das regras de negocio.
"""

from decimal import Decimal, InvalidOperation


class Parcela:
    def __init__(self, id_parcela: str, valor_nominal: Decimal, prazo_meses: int):
        identificador = str(id_parcela).strip().upper()
        if not identificador:
            raise ValueError("O identificador da parcela nao pode ficar vazio.")

        self._id_parcela = identificador
        self.valor_nominal = valor_nominal
        self.prazo_meses = prazo_meses

    @property
    def id_parcela(self) -> str:
        """O identificador pode ser consultado, mas nao alterado."""
        return self._id_parcela

    @property
    def valor_nominal(self) -> Decimal:
        return self._valor_nominal

    @valor_nominal.setter
    def valor_nominal(self, valor: Decimal):
        try:
            valor_decimal = Decimal(str(valor))

            if not valor_decimal.is_finite() or valor_decimal <= 0:
                raise ValueError

        except (InvalidOperation, ValueError):
            raise ValueError(
                "O valor nominal deve ser maior que zero."
        ) from None

        # Valida a quantidade de casas decimais.
        if valor_decimal.as_tuple().exponent < -2:
            raise ValueError(
                "O valor nominal deve ter no maximo duas casas decimais."
        )

        self._valor_nominal = valor_decimal

    @property
    def prazo_meses(self) -> int:
        return self._prazo_meses

    @prazo_meses.setter
    def prazo_meses(self, meses: int):
        if isinstance(meses, bool) or not isinstance(meses, int) or meses < 1:
            raise ValueError("O prazo deve ser um numero inteiro de pelo menos 1 mes.")
        self._prazo_meses = meses
