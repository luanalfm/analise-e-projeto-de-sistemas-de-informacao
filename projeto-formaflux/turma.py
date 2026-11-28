"""
FormaFlux - Gerenciamento de Turma.

Modulo responsavel pela representacao da turma de formatura
e pelo gerenciamento de suas parcelas a receber.

Aplica encapsulamento e agregacao de objetos, permitindo
o cadastro, a busca e a listagem de parcelas, com controle
de duplicidade dos identificadores.
"""

from parcela import Parcela


class Turma:
    def __init__(self, nome: str, ano: int):
        nome_limpo = nome.strip()
        if not nome_limpo:
            raise ValueError("O nome da turma nao pode ficar vazio.")
        if isinstance(ano, bool) or not isinstance(ano, int) or ano < 2000:
            raise ValueError("Informe um ano de formatura valido.")

        self._nome = nome_limpo
        self._ano = ano
        self.__parcelas: list[Parcela] = []

    @property
    def nome(self) -> str:
        return self._nome

    @property
    def ano(self) -> int:
        return self._ano

    def adicionar_parcela(self, parcela: Parcela) -> None:
        if not isinstance(parcela, Parcela):
            raise TypeError("A turma so pode receber objetos da classe Parcela.")
        if self.buscar_parcela(parcela.id_parcela) is not None:
            raise ValueError("Ja existe uma parcela com esse identificador.")
        self.__parcelas.append(parcela)

    def buscar_parcela(self, id_parcela: str) -> Parcela | None:
        identificador = str(id_parcela).strip().upper()
        for parcela in self.__parcelas:
            if parcela.id_parcela == identificador:
                return parcela
        return None

    def listar_parcelas(self) -> list[Parcela]:
        # A lista original nao e devolvida, para evitar alteracoes por fora.
        return self.__parcelas.copy()
