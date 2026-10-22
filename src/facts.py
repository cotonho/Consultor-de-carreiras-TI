"""Classes de Fatos (Fact) do Sistema Especialista."""

from experta import Fact, Field


class AfinidadeMatematica(Fact):
    """Nível de afinidade com matemática e estatística."""

    nivel = Field(str, mandatory=True)  # baixa | media | alta


class PreferenciaDiaria(Fact):
    """Preferência de atuação no dia a dia."""

    tipo = Field(str, mandatory=True)


class Linguagem(Fact):
    """Linguagem ou ferramenta de maior afinidade atual."""

    nome = Field(str, mandatory=True)  # python | javascript | linux_redes | nenhuma


class EntregaValor(Fact):
    """Tipo de entrega de valor preferida."""

    tipo = Field(str, mandatory=True)


class AspectoTecnico(Fact):
    """Aspecto do trabalho técnico que mais atrai."""

    aspecto = Field(str, mandatory=True)
