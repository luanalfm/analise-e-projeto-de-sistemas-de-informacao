# Universidade Federal Rural de Pernambuco (UFRPE)

# UNIDADE ACADEMICA DE EDUCACAO A DISTANCIA E TECNOLOGIA (UAEADTec)
# BACHARELADO EM SISTEMAS DE INFORMACA (BSI)
# Disciplina: Analise e Projeto de Sistemas de Informacao
# Docente: Jose Paulo Lima
# Discente: Isabelle Karoline de Oliveira Barbosa e Luana Luzia Ferreira Medeiros
# Polo Jaboatao dos Guararapes - Semestre 2026.2 - Modulo 2
# 2ª Verificação de Aprendizagem 

"""
FormaFlux - Interface via Terminal (CLI).

Modulo principal de execucao, responsavel pelo menu interativo
e pelo gerenciamento do fluxo de operacoes do sistema.

Integra as classes de dominio para cadastro, consulta, simulacao
e comparacao de antecipacoes de recebiveis.

Os dados sao mantidos em memoria durante a sessao de uso.
"""

from decimal import Decimal

from antecipacao_composta import AntecipacaoComposta
from antecipacao_simples import AntecipacaoSimples
from parcela import Parcela
from turma import Turma
from validacao import converter_decimal


def moeda(valor: Decimal) -> str:
    numero = f"{valor:,.2f}"
    return "R$ " + numero.replace(",", "X").replace(".", ",").replace("X", ".")


def ler_decimal(mensagem: str) -> Decimal:
    return converter_decimal(input(mensagem))

def ler_inteiro(mensagem: str) -> int:
    try:
        return int(input(mensagem).strip())
    except ValueError:
        raise ValueError("Digite um numero inteiro valido.") from None


def exigir_turma(turma: Turma | None) -> Turma:
    if turma is None:
        raise ValueError("Cadastre a turma primeiro (opcao 1).")
    return turma


def escolher_parcela(turma: Turma) -> Parcela:
    if not turma.listar_parcelas():
        raise ValueError("Cadastre uma parcela primeiro (opcao 2).")
    codigo = input("Identificador da parcela: ")
    parcela = turma.buscar_parcela(codigo)
    if parcela is None:
        raise ValueError("Parcela nao encontrada.")
    return parcela


def ler_parametros() -> tuple[Decimal, Decimal]:
    taxa_percentual = ler_decimal("Taxa mensal (%): ")
    tarifa = ler_decimal("Tarifa fixa (R$): ")
    # Taxa digitada como 2 representa 2% ao mes.
    taxa_decimal = taxa_percentual / 100
    if not (Decimal("0") <= taxa_decimal < Decimal("1")):
        raise ValueError("A taxa deve estar entre 0% e menos de 100%.")
    if tarifa < 0:
        raise ValueError("A tarifa nao pode ser negativa.")
    return taxa_decimal, tarifa



def exibir_resultado(nome: str, parcela: Parcela, valor_liquido: Decimal) -> None:
    custo_total = parcela.valor_nominal - valor_liquido

    exibir_titulo(nome)

    print(f"  Parcela:       {parcela.id_parcela}")
    print(f"  Prazo:         {parcela.prazo_meses} mes(es)")
    print("-" * 48)
    print(f"  Valor nominal: {moeda(parcela.valor_nominal)}")
    print(f"  Valor liquido: {moeda(valor_liquido)}")
    print(f"  Custo total:   {moeda(custo_total)}")
    print("-" * 48)


def comparar_modalidades(parcela: Parcela, taxa: Decimal, tarifa: Decimal) -> None:
    """CSU05: pode ser acessado pelo menu ou apos uma simulacao."""
    exibir_titulo("Resultado da comparacao")
    modalidades = [
        ("Desconto comercial simples", AntecipacaoSimples(taxa, tarifa)),
        ("Valor presente composto", AntecipacaoComposta(taxa, tarifa)),
    ]
    for nome, modalidade in modalidades:
        try:
            valor = modalidade.calcular_valor_liquido(parcela)
            exibir_resultado(nome, parcela, valor)
        except (ValueError, ArithmeticError) as erro:
            print(f"\n{nome}: nao foi possivel calcular. Motivo: {erro}")


def exibir_titulo(titulo: str) -> None:
    """Padroniza os titulos das operacoes no terminal."""
    print("\n" + "-" * 48)
    print(titulo.upper().center(48))
    print("-" * 48)

def mostrar_menu() -> None:
    print("\n" + "=" * 48)
    print("FORMAFLUX".center(48))
    print("Simulador de Antecipacao Financeira".center(48))
    print("=" * 48)

    print("  [1] Cadastrar turma")
    print("  [2] Cadastrar parcela")
    print("  [3] Consultar parcelas")
    print("  [4] Simular antecipacao")
    print("  [5] Comparar modalidades")
    print("-" * 48)
    print("  [0] Sair do sistema")

    print("=" * 48)


def executar() -> None:
    turma: Turma | None = None
    while True:
        mostrar_menu()
        opcao = input("Escolha: ").strip()
        if opcao == "0":
            print("\n[INFO] Encerrando o FormaFlux. Cadastros nao sao salvos.")
            break
        try:
            if opcao == "1":
                exibir_titulo("Cadastro de turma")

                if turma is not None:
                    confirmar = input("Substituir turma e perder parcelas atuais? (s/n): ")
                    if confirmar.strip().lower() != "s":
                        continue
                nome = input("Nome da turma: ")
                ano = ler_inteiro("Ano da formatura: ")
                turma = Turma(nome, ano)
                print("\n[SUCESSO] Turma cadastrada com sucesso.")

            elif opcao == "2":
                exibir_titulo("Cadastro de parcela")

                turma_atual = exigir_turma(turma)
                identificador = input("Identificador (ex.: P01): ")
                valor = ler_decimal("Valor nominal (R$): ")
                meses = ler_inteiro("Prazo em meses: ")
                turma_atual.adicionar_parcela(Parcela(identificador, valor, meses))
                print("\n[SUCESSO] Parcela cadastrada com sucesso.")

            elif opcao == "3":
                exibir_titulo("Consulta de parcelas")

                turma_atual = exigir_turma(turma)
                parcelas = turma_atual.listar_parcelas()
                if not parcelas:
                    print("\n[INFO] Nenhuma parcela cadastrada.")
                else:
                    print(f"\nTurma: {turma_atual.nome} ({turma_atual.ano})")
                    for parcela in parcelas:
                        print(f"{parcela.id_parcela} | {moeda(parcela.valor_nominal)} | "
                              f"prazo: {parcela.prazo_meses} mes(es)")

            elif opcao == "4":
                exibir_titulo("Simulacao de antecipacao")

                parcela = escolher_parcela(exigir_turma(turma))
                taxa, tarifa = ler_parametros()
                print("\n1 - Desconto comercial simples")
                print("2 - Valor presente composto")
                escolha = input("Modalidade: ").strip()
                if escolha == "1":
                    modelo = AntecipacaoSimples(taxa, tarifa)
                    nome = "Desconto comercial simples"
                elif escolha == "2":
                    modelo = AntecipacaoComposta(taxa, tarifa)
                    nome = "Valor presente composto"
                else:
                    raise ValueError("Modalidade inexistente.")
                valor = modelo.calcular_valor_liquido(parcela)                
                exibir_resultado(nome, parcela, valor)
                # CSU05 pode estender CSU04 se o usuario quiser comparar.
                comparar = input("Deseja comparar as duas modalidades? (s/n): ")
                if comparar.strip().lower() == "s":
                    comparar_modalidades(parcela, taxa, tarifa)

            elif opcao == "5":
                exibir_titulo("Comparacao de modalidades")

                parcela = escolher_parcela(exigir_turma(turma))
                taxa, tarifa = ler_parametros()
                comparar_modalidades(parcela, taxa, tarifa)

            else:
                print("\n[ATENCAO] Opcao desconhecida. Tente novamente.")
        except (ValueError, ArithmeticError) as erro:
            print(f"\n[ERRO] {erro}")
        input("\nPressione ENTER para retornar ao menu...")

if __name__ == "__main__":
    try:
        executar()
    except (KeyboardInterrupt, EOFError):
        print("\nExecucao encerrada.")
