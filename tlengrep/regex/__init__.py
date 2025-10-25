from abc import ABC, abstractmethod

from automata.afnd import AFND, SpecialSymbol

__all__ = [
    "RegEx",
    "Empty",
    "Lambda",
    "Char",
    "Union",
    "Concat",
    "Star",
    "Plus"
]


class RegEx(ABC):
    """Clase abstracta para representar expresiones regulares."""
    def __init__(self): #nos podriamos quedar con uno de los dos atributos, dejo los dos por ahora
        self._afd = self.to_afnd().determinize().minimize() 
        self._afnd = self._afd.to_afnd() 

    @abstractmethod
    def naive_match(self, word: str) -> bool:
        """
        Indica si la expresión regular acepta la cadena dada.
        Implementación recursiva, poco eficiente.
        """
        pass

    def match(self, word: str) -> bool:
        """Indica si la expresión regular acepta la cadena dada."""
        return self._afd.match(word)

    @abstractmethod
    def to_afnd(self) -> AFND:
        """Convierte la expresión regular a un AFND."""
        pass

    @abstractmethod
    def _atomic(self) -> bool:
        """
        (Interno) Indica si la expresión regular es atómica. Útil para
        implementar la función __str__.
        """
        pass


class Empty(RegEx):
    """Expresión regular que denota el lenguaje vacío (∅)."""

    def naive_match(self, word: str):
        return False

    def to_afnd(self) -> AFND:
        afnd = AFND()
        afnd.add_state("q0", False)
        afnd.add_state("q1", True)
        afnd.mark_initial_state("q0")
        return afnd

    def _atomic(self):
        return True

    def __str__(self):
        return "∅"


class Lambda(RegEx):
    """Expresión regular que denota el lenguaje de la cadena vacía (Λ)."""

    def naive_match(self, word: str):
        return word == ""

    def to_afnd(self) -> AFND:
        afnd = AFND()
        afnd.add_state("q0", True)
        afnd.mark_initial_state("q0")
        return afnd

    def _atomic(self):
        return True

    def __str__(self):
        return "λ"


class Char(RegEx):
    """Expresión regular que denota el lenguaje de un determinado carácter."""

    def __init__(self, char: str):
        assert len(char) == 1
        self.char = char
        super().__init__()

    def naive_match(self, word: str):
        return word == self.char

    def to_afnd(self) -> AFND:
        afnd = AFND()
        afnd.add_state("q0", False)
        afnd.add_state("q1", True)
        afnd.mark_initial_state("q0")
        afnd.add_transition("q0", "q1", self.char)
        return afnd

    def _atomic(self):
        return True

    def __str__(self):
        return self.char


class Concat(RegEx):
    """Expresión regular que denota la concatenación de dos expresiones regulares."""

    def __init__(self, exp1: RegEx, exp2: RegEx):
        self.exp1 = exp1
        self.exp2 = exp2
        super().__init__()

    def naive_match(self, word: str):
        for i in range(len(word) + 1):
            if self.exp1.naive_match(word[:i]) and self.exp2.naive_match(word[i:]):
                return True
        return False

    def to_afnd(self) -> AFND:
        afnd1 = self.exp1._afnd
        afnd2 = self.exp2._afd.to_afnd()
        afnd2.normalize_states()
        afnd2.rename_states()

        afnd = AFND()
    
        afnd.copy_states_as_not_final(afnd1)
        afnd.copy_transitions(afnd1)

        for state in afnd2.states:
            afnd.add_state(state, state in afnd2.final_states)
        afnd.copy_transitions(afnd2)

        afnd.mark_initial_state(afnd1.initial_state)
        afnd.add_transition(list(afnd1.final_states)[0], afnd2.initial_state, SpecialSymbol.Lambda)

        afnd.normalize_states()

        return afnd

    def _atomic(self):
        return False

    def __str__(self):
        return f"{f'({self.exp1})' if not self.exp1._atomic() else self.exp1}" \
            f"{f'({self.exp2})' if not self.exp2._atomic() else self.exp2}"


class Union(RegEx):
    """Expresión regular que denota la unión de dos expresiones regulares."""

    def __init__(self, exp1: RegEx, exp2: RegEx):
        self.exp1 = exp1
        self.exp2 = exp2
        super().__init__()

    def naive_match(self, word: str):
        return self.exp1.naive_match(word) or self.exp2.naive_match(word)

    def to_afnd(self) -> AFND:
        afnd1 = self.exp1._afnd
        afnd2 = self.exp2._afnd
        afnd2.normalize_states()
        afnd2.rename_states()

        afnd = AFND()
        afnd.copy_states_as_not_final(afnd1)
        afnd.copy_transitions(afnd1)     
   
        afnd.copy_states_as_not_final(afnd2)
        afnd.copy_transitions(afnd2)

        afnd.add_state("qi", False)
        afnd.add_state("qf", True)
        afnd.mark_initial_state("qi")

        afnd.add_transition("qi", afnd1.initial_state, SpecialSymbol.Lambda)
        afnd.add_transition("qi", afnd2.initial_state, SpecialSymbol.Lambda)
        afnd.add_transition(list(afnd1.final_states)[0], "qf", SpecialSymbol.Lambda)
        afnd.add_transition(list(afnd2.final_states)[0], "qf", SpecialSymbol.Lambda)

        afnd.normalize_states()

        return afnd

    def _atomic(self):
        return False

    def __str__(self):
        return f"{f'({self.exp1})' if not self.exp1._atomic() else self.exp1}" \
            f"|{f'({self.exp2})' if not self.exp2._atomic() else self.exp2}"


class Star(RegEx):
    """Expresión regular que denota la clausura de Kleene de otra expresión regular."""

    def __init__(self, exp: RegEx):
        self.exp = exp
        super().__init__()

    def naive_match(self, word: str):
        if word == "" or self.exp.naive_match(word):
            return True
        for i in range(1, len(word) + 1):
            if self.exp.naive_match(word[:i]) and self.naive_match(word[i:]):
                return True
        return False

    def to_afnd(self) -> AFND:
        afnd1 = self.exp._afnd

        afnd = AFND()
        afnd.copy_states_as_not_final(afnd1)
        afnd.copy_transitions(afnd1)

        afnd.add_state("qi", False)
        afnd.mark_initial_state("qi")
        afnd.add_state("qf", True)

        afnd.add_transition("qi", afnd1.initial_state, SpecialSymbol.Lambda)
        afnd.add_transition(list(afnd1.final_states)[0], "qf", SpecialSymbol.Lambda)
        afnd.add_transition(list(afnd1.final_states)[0], afnd1.initial_state, SpecialSymbol.Lambda)
        afnd.add_transition("qi", "qf", SpecialSymbol.Lambda)

        afnd.normalize_states()

        return afnd

    def _atomic(self):
        return False

    def __str__(self):
        return f"({self.exp})*" if not self.exp._atomic() else f"{self.exp}*"


class Plus(RegEx):
    """Expresión regular que denota la clausura positiva de otra expresión regular."""

    def __init__(self, exp: RegEx):
        self.exp = exp
        super().__init__()

    def naive_match(self, word: str):
        if self.exp.naive_match(word):
            return True
        for i in range(1, len(word) + 1):
            if self.exp.naive_match(word[:i]) and self.naive_match(word[i:]):
                return True
        return False

    def to_afnd(self) -> AFND:
        return Concat(self.exp, Star(self.exp)).to_afnd()

    def _atomic(self) -> bool:
        return False

    def __str__(self):
        return f"({self.exp})+" if not self.exp._atomic() else f"{self.exp}+"
