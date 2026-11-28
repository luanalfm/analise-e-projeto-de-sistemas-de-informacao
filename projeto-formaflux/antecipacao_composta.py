"""
FormaFlux - Valor Presente Composto.

Modulo responsavel pelo calculo da antecipacao de recebiveis
com base no valor presente sob capitalizacao composta.

Aplica heranca e polimorfismo, especializando o metodo de
calculo da superclasse Antecipacao e reutilizando as regras
financeiras compartilhadas.

Formula: VP = V / (1 + i) ** n
"""

from decimal import Decimal

from antecipacao import Antecipacao
from parcela import Parcela


class AntecipacaoComposta(Antecipacao):
    def __init__(self, taxa_mensal: Decimal, tarifa_fixa: Decimal):
        super().__init__(taxa_mensal, tarifa_fixa)

    def calcular_valor_liquido(self, parcela: Parcela) -> Decimal:
        # Valor presente: VP = valor nominal / (1 + taxa) ** prazo.
        valor_presente = parcela.valor_nominal / (
            (1 + self._taxa_mensal) ** parcela.prazo_meses
        )
        return self._finalizar_calculo(valor_presente)
