"""
FormaFlux - Interface Grafica do Usuario (GUI).

Modulo desenvolvido com CustomTkinter, responsavel pela interacao
visual com as funcionalidades de cadastro, consulta, simulacao
e comparacao de antecipacoes.

Reutiliza as classes de dominio do sistema, mantendo a separacao
entre a interface grafica e a logica de negocio.

Complementa a interface via terminal (CLI), disponivel em main.py.
"""

from decimal import Decimal
from tkinter import BooleanVar, messagebox

import customtkinter as ctk

from turma import Turma
from parcela import Parcela
from antecipacao_simples import AntecipacaoSimples
from antecipacao_composta import AntecipacaoComposta
from validacao import converter_decimal

# Identidade visual. Cada par de cores representa (tema claro, tema escuro).
FUNDO = ("#F3F6F9", "#101923")
SUPERFICIE = ("#FFFFFF", "#1B2A36")
SUPERFICIE_ALT = ("#F8FAFC", "#213340")
TEXTO = ("#1B3345", "#ECF5F7")
TEXTO_2 = ("#526E7D", "#B6C7D0")
LINHA = ("#DBE5EB", "#415563")
CABECALHO_TABELA = ("#E9F0F5", "#2B414F")
LINHA_PAR = ("#FFFFFF", "#1B2A36")
LINHA_IMPAR = ("#F5F8FA", "#233542")
DIFERENCA = ("#EAF7F1", "#173E35")
VERDE = ("#167F6D", "#29A88D")
VERDE_HOVER = ("#116957", "#208E78")
LATERAL = ("#173344", "#102633")
LATERAL_HOVER = ("#2F5361", "#2B4955")

ctk.set_default_color_theme("green")
ctk.set_appearance_mode("light")

F_TITULO = ("Segoe UI", 26, "bold")
F_SECAO = ("Segoe UI", 17, "bold")
F_TEXTO = ("Segoe UI", 15)
F_ROTULO = ("Segoe UI", 13, "bold")
F_CABECALHO = ("Segoe UI", 13, "bold")
F_KPI = ("Segoe UI", 29, "bold")
F_NAV = ("Segoe UI", 15)
F_LOGO = ("Segoe UI", 28, "bold")


def valor_decimal(texto):
   return converter_decimal(texto)


def valor_monetario(numero):
    texto = f"{numero:,.2f}"
    return "R$ " + texto.replace(",", "X").replace(".", ",").replace("X", ".")


def numero_inteiro(texto, campo):
    try:
        return int(texto.strip())
    except ValueError:
        raise ValueError(f"Informe um número inteiro para {campo}.") from None


class FormaFluxApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("FormaFlux | Gestão de recebíveis")
        self.geometry("1160x760")
        self.minsize(950, 650)
        self.configure(fg_color=FUNDO)

        self.turma = None
        self.paginas = {}
        self.botoes_menu = {}
        self.pagina_atual = None
        self.tema_escuro = BooleanVar(value=False)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self._montar_estrutura()
        self._montar_turma()
        self._montar_parcelas()
        self._montar_consulta()
        self._montar_simulacao()
        self._montar_comparacao()
        self._navegar("Turma")

    def _montar_estrutura(self):
        lateral = ctk.CTkFrame(self, width=230, fg_color=LATERAL, corner_radius=0)
        lateral.grid(row=0, column=0, sticky="nsew")
        lateral.grid_propagate(False)
        self.lateral = lateral

        ctk.CTkLabel(lateral, text="FormaFlux", font=F_LOGO,
                     text_color="#FFFFFF", anchor="w").pack(fill="x", padx=22, pady=(32, 20))
        ctk.CTkFrame(lateral, height=1, fg_color="#496473").pack(
            fill="x", padx=20, pady=(0, 18))

        self.area = ctk.CTkFrame(self, fg_color=FUNDO, corner_radius=0)
        self.area.grid(row=0, column=1, sticky="nsew")
        # As paginas sao colocadas com pack somente quando selecionadas.
        # Isso evita que quadros rolaveis fiquem sobrepostos no Windows.

        for nome in ("Turma", "Parcelas", "Consultar", "Simular", "Comparar"):
            botao = ctk.CTkButton(
                lateral, text=nome, anchor="w", height=47,
                font=F_NAV, corner_radius=10,
                fg_color="transparent", hover_color=LATERAL_HOVER,
                text_color="#E7F2F5", command=lambda n=nome: self._navegar(n)
            )
            botao.pack(fill="x", padx=13, pady=4)
            self.botoes_menu[nome] = botao
            # Nao empilhe paginas na mesma celula do grid: a janela do
            # CTkScrollableFrame tem um contêiner proprio, que pode permanecer
            # visivel sobre outra tela em algumas configuracoes do Windows.
            # Cada pagina começa sem gerenciador de geometria.
            pagina = ctk.CTkScrollableFrame(self.area, fg_color="transparent", corner_radius=0)
            self.paginas[nome] = pagina

        ctk.CTkSwitch(
            lateral, text="Modo escuro", variable=self.tema_escuro,
            command=self._trocar_tema, font=F_TEXTO,
            text_color="#FFFFFF", fg_color="#63818D",
            progress_color="#27A88C", button_color="#FFFFFF",
            button_hover_color="#E0EEE9"
        ).pack(side="bottom", anchor="w", padx=22, pady=(0, 30))

    def _trocar_tema(self):
        ctk.set_appearance_mode("dark" if self.tema_escuro.get() else "light")

    def _navegar(self, nome):
        """Exibe apenas a pagina escolhida, preservando os dados ja digitados."""
        if nome not in self.paginas:
            raise ValueError(f"Tela desconhecida: {nome}")

        # Oculta a tela anterior antes de mostrar a nova. O metodo
        # pack_forget() remove o contêiner visivel do CTkScrollableFrame,
        # nao apenas seu quadro interno.
        if self.pagina_atual is not None:
            self.paginas[self.pagina_atual].pack_forget()
            self.botoes_menu[self.pagina_atual].configure(
                fg_color="transparent", text_color="#E7F2F5")

        self.pagina_atual = nome
        self.paginas[nome].pack(fill="both", expand=True, padx=(26, 24), pady=(24, 24))
        self.botoes_menu[nome].configure(fg_color=VERDE, text_color="#FFFFFF")

        if nome == "Consultar":
            self._atualizar_consulta()

    def _titulo(self, pagina, texto):
        ctk.CTkLabel(pagina, text=texto, font=F_TITULO, text_color=TEXTO,
                     anchor="w").pack(fill="x", pady=(1, 18))

    def _cartao(self, pai, padding=20):
        carta = ctk.CTkFrame(pai, fg_color=SUPERFICIE, corner_radius=14,
                            border_width=1, border_color=LINHA)
        carta.pack(fill="x", pady=(0, 18))
        interior = ctk.CTkFrame(carta, fg_color="transparent")
        interior.pack(fill="x", padx=padding, pady=padding)
        return interior

    def _campo(self, pai, rotulo, exemplo="", largura=None):
        bloco = ctk.CTkFrame(pai, fg_color="transparent")
        ctk.CTkLabel(bloco, text=rotulo, text_color=TEXTO_2, font=F_ROTULO,
                     anchor="w").pack(fill="x", pady=(0, 6))
        entrada = ctk.CTkEntry(
            bloco, height=44, corner_radius=9,
            font=F_TEXTO, text_color=TEXTO, fg_color=SUPERFICIE_ALT,
            border_color=LINHA, placeholder_text=exemplo
        )
        if largura:
            entrada.configure(width=largura)
        entrada.pack(fill="x")
        return bloco, entrada

    def _botao_acao(self, pai, texto, comando):
        botao = ctk.CTkButton(
            pai, text=texto, command=comando, height=44,
            font=("Segoe UI", 14, "bold"),
            fg_color=VERDE, hover_color=VERDE_HOVER, corner_radius=10
        )
        botao.pack(anchor="w", pady=(20, 0))
        return botao

    def _aviso(self, pai, texto=""):
        msg = ctk.CTkLabel(pai, text=texto, text_color=TEXTO_2,
                           font=F_TEXTO, anchor="w", justify="left")
        msg.pack(fill="x", pady=(12, 0))
        return msg

    def _erro(self, exc):
        messagebox.showerror("FormaFlux - confira os dados", str(exc), parent=self)

    def _turma_obrigatoria(self):
        if self.turma is None:
            raise ValueError("Cadastre uma turma na tela Turma antes de continuar.")
        return self.turma

    def _parcela_obrigatoria(self, codigo):
        turma = self._turma_obrigatoria()
        parcela = turma.buscar_parcela(codigo)
        if parcela is None:
            raise ValueError("Parcela não encontrada. Confira o identificador em Consultar.")
        return parcela

    def _parametros(self, taxa, tarifa):
        taxa_decimal = valor_decimal(taxa) / Decimal("100")
        tarifa_decimal = valor_decimal(tarifa)
        if not Decimal("0") <= taxa_decimal < Decimal("1"):
            raise ValueError("A taxa mensal deve estar entre 0% e menos de 100%.")
        if tarifa_decimal < 0:
            raise ValueError("A tarifa fixa não pode ser negativa.")
        return taxa_decimal, tarifa_decimal

    @staticmethod
    def _limpar(pai):
        for filho in pai.winfo_children():
            filho.destroy()

    def _linha_infos(self, pai, infos, colunas=3):
        """Campos informativos em pequenas celulas com divisores."""
        bloco = ctk.CTkFrame(pai, fg_color=SUPERFICIE_ALT,
                             border_color=LINHA, border_width=1, corner_radius=11)
        bloco.pack(fill="x", pady=(0, 16))
        for col in range(colunas):
            bloco.grid_columnconfigure(col, weight=1, uniform="infos")
        for indice, (rotulo, valor) in enumerate(infos):
            coluna = indice % colunas
            linha = indice // colunas
            sub = ctk.CTkFrame(bloco, fg_color="transparent")
            sub.grid(row=linha, column=coluna, sticky="nsew", padx=16, pady=12)
            ctk.CTkLabel(sub, text=rotulo, font=F_ROTULO,
                         text_color=TEXTO_2, anchor="w").pack(fill="x")
            ctk.CTkLabel(sub, text=str(valor), font=F_TEXTO,
                         text_color=TEXTO, anchor="w").pack(fill="x", pady=(4, 0))
        return bloco

    def _tabela(self, pai, colunas, linhas, pesos=None, linha_destaque=None):
        """Tabela nativa CustomTkinter, com grade, cabecalho e linhas alternadas."""
        if pesos is None:
            pesos = [1] * len(colunas)
        externa = ctk.CTkFrame(pai, fg_color=LINHA, corner_radius=10,
                               border_width=1, border_color=LINHA)
        externa.pack(fill="x")
        for coluna, peso in enumerate(pesos):
            externa.grid_columnconfigure(coluna, weight=peso)

        for i, titulo_col in enumerate(colunas):
            self._celula(externa, 0, i, titulo_col, CABECALHO_TABELA,
                         font=F_CABECALHO, cabecalho=True,
                         alinhamento="e" if i in (1, 2) and len(colunas) == 3 else "w")
        for idx, valores in enumerate(linhas):
            cor = DIFERENCA if linha_destaque is not None and idx == linha_destaque else (
                LINHA_PAR if idx % 2 == 0 else LINHA_IMPAR)
            for col, valor in enumerate(valores):
                alinhamento = "e" if (len(colunas) == 3 and col in (1, 2)) or (
                    len(colunas) == 4 and col == 1) else "w"
                self._celula(externa, idx + 1, col, str(valor), cor,
                             font=F_TEXTO, alinhamento=alinhamento)
        return externa

    def _celula(self, tabela, linha, coluna, texto, cor, font, cabecalho=False, alinhamento="w"):
        caixa = ctk.CTkFrame(tabela, fg_color=cor, corner_radius=0)
        caixa.grid(row=linha, column=coluna, sticky="nsew", padx=1, pady=1)
        ctk.CTkLabel(caixa, text=texto, text_color=TEXTO, font=font,
                     height=45 if cabecalho else 48, anchor=alinhamento,
                     justify="left" if alinhamento == "w" else "right").pack(
            fill="both", expand=True, padx=13)

    def _kpi(self, pai, rotulo, valor, destaque=False):
        quadro = ctk.CTkFrame(
            pai, fg_color=DIFERENCA if destaque else SUPERFICIE_ALT,
            corner_radius=12, border_color=VERDE if destaque else LINHA,
            border_width=1
        )
        ctk.CTkLabel(quadro, text=rotulo, font=F_ROTULO,
                     text_color=TEXTO_2, anchor="w").pack(fill="x", padx=17, pady=(16, 3))
        ctk.CTkLabel(quadro, text=str(valor), font=F_KPI,
                     text_color=VERDE if destaque else TEXTO,
                     anchor="w").pack(fill="x", padx=17, pady=(0, 17))
        return quadro

    # CSU01 - Cadastro de turma
    def _montar_turma(self):
        pagina = self.paginas["Turma"]
        self._titulo(pagina, "Cadastrar turma")
        area = self._cartao(pagina)
        nome_bloco, self.nome_turma = self._campo(area, "Nome da turma", "Ex.: BSI 2024")
        nome_bloco.pack(fill="x", pady=(0, 12))
        ano_bloco, self.ano_turma = self._campo(area, "Ano da formatura", "Ex.: 2028")
        ano_bloco.pack(fill="x")
        self._botao_acao(area, "Salvar turma", self._salvar_turma)
        self.status_turma = self._aviso(area, "Nenhuma turma cadastrada.")

    def _salvar_turma(self):
        try:
            if self.turma is not None:
                confirmado = messagebox.askyesno(
                    "Substituir turma", "Substituir a turma atual e perder as parcelas cadastradas?",
                    parent=self)
                if not confirmado:
                    return
            nova_turma = Turma(
                self.nome_turma.get(), numero_inteiro(self.ano_turma.get(), "ano da formatura"))
            self.turma = nova_turma
            self.status_turma.configure(
                text=f"Turma ativa: {nova_turma.nome} | Formatura {nova_turma.ano}",
                text_color=VERDE)
            self._atualizar_consulta()
            self._limpar(self.sim_resultado)
            self._limpar(self.comp_resultado)
        except (ValueError, TypeError) as exc:
            self._erro(exc)

    # CSU02 - Cadastro de parcela
    def _montar_parcelas(self):
        pagina = self.paginas["Parcelas"]
        self._titulo(pagina, "Cadastrar parcela")
        area = self._cartao(pagina)
        id_bloco, self.id_parcela = self._campo(area, "Identificador", "Ex.: P01")
        id_bloco.pack(fill="x", pady=(0, 12))
        valor_bloco, self.valor_parcela = self._campo(area, "Valor nominal (R$)", "Ex.: 1000,00")
        valor_bloco.pack(fill="x", pady=(0, 12))
        prazo_bloco, self.prazo_parcela = self._campo(area, "Prazo até o vencimento (meses)", "Ex.: 3")
        prazo_bloco.pack(fill="x")
        self._botao_acao(area, "Adicionar parcela", self._salvar_parcela)
        self.status_parcela = self._aviso(area)

    def _salvar_parcela(self):
        try:
            turma = self._turma_obrigatoria()
            parcela = Parcela(
                self.id_parcela.get(), valor_decimal(self.valor_parcela.get()),
                numero_inteiro(self.prazo_parcela.get(), "prazo"))
            turma.adicionar_parcela(parcela)
            self.status_parcela.configure(
                text=f"Parcela {parcela.id_parcela} cadastrada com sucesso.", text_color=VERDE)
            self._atualizar_consulta()
        except (ValueError, TypeError) as exc:
            self._erro(exc)

    # CSU03 - Consulta gradeada
    def _montar_consulta(self):
        pagina = self.paginas["Consultar"]
        self._titulo(pagina, "Consultar parcelas")
        area = self._cartao(pagina)
        self.rotulo_turma = ctk.CTkLabel(area, text="", font=F_SECAO,
                                         text_color=TEXTO, anchor="w")
        self.rotulo_turma.pack(fill="x", pady=(0, 14))
        self.resumo_consulta = ctk.CTkFrame(area, fg_color="transparent")
        self.resumo_consulta.pack(fill="x")
        self.grade_consulta = ctk.CTkFrame(area, fg_color="transparent")
        self.grade_consulta.pack(fill="x", pady=(14, 0))
        self._botao_acao(area, "Atualizar consulta", self._atualizar_consulta)

    def _atualizar_consulta(self):
        self._limpar(self.resumo_consulta)
        self._limpar(self.grade_consulta)
        if self.turma is None:
            self.rotulo_turma.configure(text="Nenhuma turma cadastrada")
            self._aviso(self.grade_consulta, "Cadastre uma turma para visualizar os recebíveis.")
            return
        parcelas = self.turma.listar_parcelas()
        total = sum((p.valor_nominal for p in parcelas), Decimal("0"))
        self.rotulo_turma.configure(text=f"{self.turma.nome}  |  Formatura {self.turma.ano}")
        self._linha_infos(self.resumo_consulta, [
            ("Parcelas", str(len(parcelas))),
            ("Total nominal", valor_monetario(total)),
        ], colunas=2)
        if not parcelas:
            self._aviso(self.grade_consulta, "Nenhuma parcela cadastrada até agora.")
            return
        linhas = [
            (p.id_parcela, valor_monetario(p.valor_nominal),
             f"{p.prazo_meses} mês(es)", self.turma.nome)
            for p in parcelas
        ]
        self._tabela(self.grade_consulta,
                     ("ID DA PARCELA", "VALOR NOMINAL", "PRAZO", "TURMA"),
                     linhas, pesos=[1, 2, 1, 2])

    # CSU04 - Simulacao estruturada
    def _montar_simulacao(self):
        pagina = self.paginas["Simular"]
        self._titulo(pagina, "Simular antecipação")
        area = self._cartao(pagina)
        campos = ctk.CTkFrame(area, fg_color="transparent")
        campos.pack(fill="x")
        for i in range(3):
            campos.grid_columnconfigure(i, weight=1, uniform="campos")
        a, self.sim_id = self._campo(campos, "ID da parcela", "P01")
        a.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        b, self.sim_taxa = self._campo(campos, "Taxa mensal (%)", "2")
        b.grid(row=0, column=1, sticky="ew", padx=5)
        c, self.sim_tarifa = self._campo(campos, "Tarifa fixa (R$)", "10")
        c.grid(row=0, column=2, sticky="ew", padx=(10, 0))
        ctk.CTkLabel(area, text="Modalidade", font=F_ROTULO,
                     text_color=TEXTO_2).pack(anchor="w", pady=(15, 6))
        self.sim_modo = ctk.CTkOptionMenu(
            area, height=43, width=265,
            values=["Desconto simples", "Valor presente composto"],
            font=F_TEXTO, fg_color=VERDE, button_color=VERDE_HOVER,
            button_hover_color=VERDE_HOVER
        )
        self.sim_modo.pack(anchor="w")
        self._botao_acao(area, "Calcular antecipação", self._calcular_simulacao)
        self.sim_resultado = ctk.CTkFrame(pagina, fg_color="transparent")
        self.sim_resultado.pack(fill="x")

    def _calcular_simulacao(self):
        try:
            p = self._parcela_obrigatoria(self.sim_id.get())
            taxa, tarifa = self._parametros(self.sim_taxa.get(), self.sim_tarifa.get())
            nome = self.sim_modo.get()
            modelo = (AntecipacaoSimples(taxa, tarifa) if nome == "Desconto simples"
                      else AntecipacaoComposta(taxa, tarifa))
            liquido = modelo.calcular_valor_liquido(p)
            custo = p.valor_nominal - liquido
            self._limpar(self.sim_resultado)
            conteudo = self._cartao(self.sim_resultado)
            ctk.CTkLabel(conteudo, text="Resultado da simulação", font=F_SECAO,
                         text_color=TEXTO, anchor="w").pack(fill="x", pady=(0, 15))
            destaque = ctk.CTkFrame(conteudo, fg_color="transparent")
            destaque.pack(fill="x", pady=(0, 16))
            destaque.grid_columnconfigure(0, weight=2, uniform="res")
            destaque.grid_columnconfigure(1, weight=2, uniform="res")
            self._kpi(destaque, "VALOR LÍQUIDO A RECEBER", valor_monetario(liquido), True).grid(
                row=0, column=0, sticky="nsew", padx=(0, 6))
            self._kpi(destaque, "CUSTO DA ANTECIPAÇÃO", valor_monetario(custo)).grid(
                row=0, column=1, sticky="nsew", padx=(6, 0))
            linhas = [
                ("Parcela", p.id_parcela),
                ("Valor nominal", valor_monetario(p.valor_nominal)),
                ("Prazo", f"{p.prazo_meses} mês(es)"),
                ("Modalidade", nome),
                ("Taxa mensal", f"{self.sim_taxa.get().strip()}%"),
                ("Tarifa fixa", valor_monetario(tarifa)),
            ]
            self._tabela(conteudo, ("INFORMAÇÃO", "VALOR"), linhas, pesos=[2, 3])
        except (ValueError, TypeError, ArithmeticError) as exc:
            self._erro(exc)

    # CSU05 - Comparacao visual
    def _montar_comparacao(self):
        pagina = self.paginas["Comparar"]
        self._titulo(pagina, "Comparar modalidades")
        area = self._cartao(pagina)
        campos = ctk.CTkFrame(area, fg_color="transparent")
        campos.pack(fill="x")
        for i in range(3):
            campos.grid_columnconfigure(i, weight=1, uniform="campos")
        a, self.comp_id = self._campo(campos, "ID da parcela", "P01")
        a.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        b, self.comp_taxa = self._campo(campos, "Taxa mensal (%)", "2")
        b.grid(row=0, column=1, sticky="ew", padx=5)
        c, self.comp_tarifa = self._campo(campos, "Tarifa fixa (R$)", "10")
        c.grid(row=0, column=2, sticky="ew", padx=(10, 0))
        self._botao_acao(area, "Comparar modelos", self._comparar)
        self.comp_resultado = ctk.CTkFrame(pagina, fg_color="transparent")
        self.comp_resultado.pack(fill="x")

    def _comparar(self):
        try:
            p = self._parcela_obrigatoria(self.comp_id.get())
            taxa, tarifa = self._parametros(self.comp_taxa.get(), self.comp_tarifa.get())
            modelos = [
                ("Desconto simples", AntecipacaoSimples(taxa, tarifa)),
                ("Valor presente composto", AntecipacaoComposta(taxa, tarifa)),
            ]
            resultados = []
            falhas = []
            for nome, modelo in modelos:
                try:
                    liquido = modelo.calcular_valor_liquido(p)
                    resultados.append((nome, liquido, p.valor_nominal - liquido))
                except (ValueError, ArithmeticError) as exc:
                    falhas.append((nome, str(exc)))
            self._limpar(self.comp_resultado)
            area = self._cartao(self.comp_resultado)
            ctk.CTkLabel(area, text=f"Comparação da parcela {p.id_parcela}", font=F_SECAO,
                         text_color=TEXTO, anchor="w").pack(fill="x", pady=(0, 15))
            self._linha_infos(area, [
                ("Valor nominal", valor_monetario(p.valor_nominal)),
                ("Prazo", f"{p.prazo_meses} mês(es)"),
                ("Taxa mensal", f"{self.comp_taxa.get().strip()}%"),
                ("Tarifa fixa", valor_monetario(tarifa)),
            ], colunas=4)

            if resultados:
                melhor = max(item[1] for item in resultados)
                vencedores = [r for r in resultados if r[1] == melhor]
                destaque_unico = len(vencedores) == 1 and len(resultados) == 2
                quadros = ctk.CTkFrame(area, fg_color="transparent")
                quadros.pack(fill="x", pady=(0, 16))
                for i in range(len(resultados)):
                    quadros.grid_columnconfigure(i, weight=1, uniform="modelos")
                for i, (nome, liquido, custo) in enumerate(resultados):
                    melhor_unico = destaque_unico and liquido == melhor
                    quadro = ctk.CTkFrame(
                        quadros, fg_color=DIFERENCA if melhor_unico else SUPERFICIE_ALT,
                        border_width=2 if melhor_unico else 1,
                        border_color=VERDE if melhor_unico else LINHA, corner_radius=12
                    )
                    quadro.grid(row=0, column=i, sticky="nsew",
                                padx=(0, 7) if i == 0 else (7, 0))
                    ctk.CTkLabel(quadro, text=nome, font=F_SECAO,
                                 text_color=TEXTO, anchor="w").pack(fill="x", padx=18, pady=(16, 6))
                    if melhor_unico:
                        ctk.CTkLabel(quadro, text="MAIOR VALOR LÍQUIDO",
                                     font=F_ROTULO, text_color=VERDE,
                                     anchor="w").pack(fill="x", padx=18)
                    ctk.CTkLabel(quadro, text=valor_monetario(liquido),
                                 font=F_KPI, text_color=VERDE if melhor_unico else TEXTO,
                                 anchor="w").pack(fill="x", padx=18, pady=(9, 2))
                    ctk.CTkLabel(quadro, text=f"Custo: {valor_monetario(custo)}",
                                 font=F_TEXTO, text_color=TEXTO_2,
                                 anchor="w").pack(fill="x", padx=18, pady=(0, 18))
                linhas = [(n, valor_monetario(l), valor_monetario(c)) for n, l, c in resultados]
                idx = next((i for i, (_, l, _) in enumerate(resultados)
                            if destaque_unico and l == melhor), None)
                self._tabela(area, ("MODALIDADE", "VALOR LÍQUIDO", "CUSTO TOTAL"),
                             linhas, pesos=[3, 2, 2], linha_destaque=idx)
                if destaque_unico:
                    nome = vencedores[0][0]
                    ctk.CTkLabel(area, text=f"Maior retorno líquido: {nome}.",
                                 font=F_ROTULO, text_color=VERDE,
                                 anchor="w").pack(fill="x", pady=(12, 0))
                elif len(vencedores) == 2:
                    ctk.CTkLabel(area, text="As duas modalidades apresentam o mesmo valor líquido.",
                                 font=F_TEXTO, text_color=TEXTO_2,
                                 anchor="w").pack(fill="x", pady=(12, 0))
            if falhas:
                texto = "  |  ".join(f"{nome}: {motivo}" for nome, motivo in falhas)
                self._aviso(area, f"Cálculo indisponível - {texto}")
        except (ValueError, TypeError, ArithmeticError) as exc:
            self._erro(exc)


if __name__ == "__main__":
    FormaFluxApp().mainloop()
