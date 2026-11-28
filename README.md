
# Análise e Projeto de Sistemas de Informação

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![POO](https://img.shields.io/badge/Paradigma-POO-0078D4?style=flat-square)
![UML](https://img.shields.io/badge/Modelagem-UML-7952B3?style=flat-square)
![Testes](https://img.shields.io/badge/Testes-14%20aprovados-2EA44F?style=flat-square)
![Semestre](https://img.shields.io/badge/Semestre-2026.2-orange?style=flat-square)

## 1. Identificação acadêmica

**Universidade Federal Rural de Pernambuco (UFRPE)**  
Unidade Acadêmica de Educação a Distância e Tecnologia (UAEADTec)  
Bacharelado em Sistemas de Informação (BSI)

| Informação | Descrição |
|---|---|
| Disciplina | Análise e Projeto de Sistemas de Informação |
| Docente | Prof. Me. José Paulo Lima |
| Discentes | Isabelle Karoline de Oliveira Barbosa e Luana Luzia Ferreira Medeiros |
| Polo | Jaboatão dos Guararapes |
| Semestre | 2026.2 |
| Módulo | 2 |
| Avaliação | 2ª Verificação de Aprendizagem (2ª VA) |

## 2. Sobre o repositório

Repositório acadêmico destinado ao desenvolvimento e à documentação
dos projetos e atividades da disciplina de Análise e Projeto de
Sistemas de Informação.

Busca articular os fundamentos teóricos da disciplina à prática
de desenvolvimento de software, contemplando análise de requisitos,
regras de negócio, modelagem UML, programação orientada a objetos
e validação de software.

O conteúdo está organizado por projeto, preservando as decisões
de modelagem, implementação e evolução do código-fonte.

## 3. Projeto desenvolvido

### [FormaFlux — Simulador de Antecipação de Recebíveis](./projeto-formaflux)

Projeto desenvolvido em dupla para a 2ª Verificação de
Aprendizagem (2ª VA), voltado ao apoio ao planejamento
financeiro de comissões de formatura.

O FormaFlux permite simular a antecipação de parcelas futuras,
estimar o valor líquido disponível e comparar os custos
associados a duas modalidades de cálculo financeiro:

- Desconto comercial simples;
- Valor presente composto.

### 3.1. Funcionalidades

- Cadastro de turma de formatura;
- Cadastro de parcelas a receber;
- Consulta de parcelas cadastradas;
- Simulação de antecipação de recebíveis;
- Comparação entre modalidades de cálculo;
- Validação de entradas e regras de negócio;
- Apresentação dos valores líquidos e custos financeiros.

O sistema possui duas interfaces de execução:

- **CLI (Command Line Interface):** menu interativo via terminal;
- **GUI (Graphical User Interface):** interface gráfica complementar,
  desenvolvida com CustomTkinter.

### 3.2. Fundamentos técnicos

O projeto contempla os seguintes conceitos e práticas:

| Conceito | Aplicação no projeto |
|---|---|
| Abstração | Definição de uma superclasse abstrata de antecipação. |
| Encapsulamento | Proteção dos atributos e validação por propriedades e setters. |
| Herança | Especialização das modalidades de antecipação. |
| Polimorfismo | Sobrescrita do método de cálculo financeiro. |
| Agregação | Relacionamento entre a turma e suas parcelas. |
| Modularidade | Separação das responsabilidades entre classes e módulos. |
| Modelagem UML | Representação estrutural e comportamental do sistema. |
| Qualidade de software | Testes unitários, testes de regressão e validação das regras de negócio. |
| Versionamento | Controle de alterações e desenvolvimento colaborativo com Git e GitHub. |

### 3.3. Tecnologias e ferramentas

- Python;
- CustomTkinter;
- Decimal;
- Unittest;
- UML (Unified Modeling Language);
- Visual Studio Code;
- Git, GitHub e GitHub Desktop.

## 4. Estrutura do repositório

```text
analise-e-projeto-de-sistemas-de-informacao/
│
├── projeto-formaflux/
│   ├── main.py
│   ├── interface.py
│   ├── turma.py
│   ├── parcela.py
│   ├── antecipacao.py
│   ├── antecipacao_simples.py
│   ├── antecipacao_composta.py
│   ├── validacao.py
│   ├── testes/
│   │   └── test_formaflux.py
│   ├── requirements.txt
│   └── README.md
│
├── .gitignore
├── .gitattributes
└── README.md
```

## 5. Execução do projeto

Acesse a pasta do FormaFlux:

```bash
cd projeto-formaflux
```

### Interface via terminal (CLI)

```bash
python main.py
```

### Interface gráfica (GUI)

Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

Execute a aplicação:

```bash
python interface.py
```

### Testes automatizados

```bash
python -m unittest discover -s testes -v
```

A versão validada do projeto contempla 14 testes unitários
aprovados, abrangendo os cálculos financeiros, os pilares da
programação orientada a objetos, as regras de negócio,
os valores limite e os formatos de entrada.

## 6. Documentação

A documentação específica do projeto, incluindo suas regras
de negócio, organização, instruções de execução e cenários
de teste, está disponível no:

[README do FormaFlux](./projeto-formaflux/README.md)

A modelagem UML contempla quatro perspectivas do sistema:

- Diagrama de Casos de Uso;
- Diagrama de Classes;
- Diagrama de Sequência;
- Diagrama de Atividades.

## 7. Escopo e limitações

O FormaFlux é um protótipo acadêmico de caráter exclusivamente
educacional.

As operações são simuladas, os dados são mantidos em memória
durante a execução e não há integração com instituições
financeiras, persistência em banco de dados ou movimentação
de recursos reais.

Os resultados destinam-se à compreensão dos conceitos
financeiros e à aplicação prática dos fundamentos de
análise, projeto e desenvolvimento de sistemas de informação.

---

**Universidade Federal Rural de Pernambuco — UFRPE**  
Bacharelado em Sistemas de Informação | UAEADTec | 2026.2
