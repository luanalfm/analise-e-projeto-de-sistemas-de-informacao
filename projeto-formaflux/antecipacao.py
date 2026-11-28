"""
FormaFlux - Modelo Abstrato de Antecipacao Financeira.

Modulo responsavel pela definicao da superclasse Antecipacao,
que estabelece o comportamento comum das modalidades de calculo.

Aplica abstracao e encapsulamento, centralizando a validacao
dos parametros financeiros, a deducao da tarifa fixa,
o arredondamento e a validacao do valor liquido.
"""

from abc import ABC, abstractmethod
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

from parcela import Parcela

CENTAVO = Decimal("0.01")


class Antecipacao(ABC):
    def __init__(self, taxa_mensal: Decimal, tarifa_fixa: Decimal):
        try:
            taxa = Decimal(str(taxa_mensal))
            tarifa = Decimal(str(tarifa_fixa))
        except (InvalidOperation, ValueError):
            raise ValueError("Taxa e tarifa devem ser numeros validos.") from None

        if not taxa.is_finite() or taxa < 0 or taxa >= 1:
            raise ValueError("A taxa mensal deve estar entre 0% e menos de 100%.")
        if not tarifa.is_finite() or tarifa < 0:
            raise ValueError("A tarifa fixa nao pode ser negativa.")

        # Valida a precisao monetaria da tarifa.
        if tarifa.as_tuple().exponent < -2:
            raise ValueError(
                "A tarifa fixa deve ter no maximo duas casas decimais.")

        self._taxa_mensal = taxa
        self._tarifa_fixa = tarifa

    @property
    def taxa_mensal(self) -> Decimal:
        return self._taxa_mensal

    @property
    def tarifa_fixa(self) -> Decimal:
        return self._tarifa_fixa

    
    def _finalizar_calculo(self, valor_presente: Decimal) -> Decimal:
        liquido = valor_presente - self._tarifa_fixa

        if not liquido.is_finite():
            raise ValueError("Valor liquido invalido.")

        # Arredonda o valor antes de validar a viabilidade.
        liquido = liquido.quantize(
            CENTAVO, rounding=ROUND_HALF_UP
        )

        if liquido <= 0:
            raise ValueError(
                "Antecipacao inviavel: desconto e tarifa consomem o valor da parcela."
            )

        return liquido


    @abstractmethod
    def calcular_valor_liquido(self, parcela: Parcela) -> Decimal:
        """Calcula quanto a comissao receberia agora."""
        raise NotImplementedError
