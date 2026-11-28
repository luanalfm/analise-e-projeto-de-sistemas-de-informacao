
"""
FormaFlux - Desconto Comercial Simples.

Modulo responsavel pelo calculo da antecipacao de recebiveis
com base na modalidade de desconto comercial simples.

Aplica heranca e polimorfismo, especializando o metodo de
calculo da superclasse Antecipacao e validando as condicoes
de viabilidade financeira da modalidade.

Formula: VP = V * (1 - i * n)
"""

from decimal import Decimal

from antecipacao import Antecipacao
from parcela import Parcela


class AntecipacaoSimples(Antecipacao):
    def __init__(self, taxa_mensal: Decimal, tarifa_fixa: Decimal):
        super().__init__(taxa_mensal, tarifa_fixa)

    def calcular_valor_liquido(self, parcela: Parcela) -> Decimal:

        # Valida a viabilidade do desconto comercial simples.
        if self._taxa_mensal * parcela.prazo_meses >= 1:
            raise ValueError(
                "Antecipacao simples inviavel: taxa vezes prazo deve ser inferior a 1."
            )

        # Desconto simples: VP = valor nominal * (1 - taxa * prazo).
        valor_presente = parcela.valor_nominal * (
            1 - self._taxa_mensal * parcela.prazo_meses
        )

        return self._finalizar_calculo(valor_presente)
