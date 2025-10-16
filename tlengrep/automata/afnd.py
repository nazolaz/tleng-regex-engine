from enum import Enum
from typing import Hashable, Union

from automata.af import AF
from automata.afd import AFD


__all__ = ["AFND"]


class SpecialSymbol(Enum):
    Lambda = "λ"


class AFND(AF):
    """Autómata finito no determinístico (con transiciones lambda)."""

    def add_transition(self, state1: Hashable, state2: Hashable, char: Union[str, SpecialSymbol]):
        """Agrega una transición al autómata."""
        if state1 not in self.states:
            raise ValueError(f"El estado {state1} no pertenece al autómata.")
        if state2 not in self.states:
            raise ValueError(f"El estado {state2} no pertenece al autómata.")
        if char not in self.transitions[state1]:
            self.transitions[state1][char] = set()
        self.transitions[state1][char].add(state2)
        if char is not SpecialSymbol.Lambda:
            self.alphabet.add(char)

    def lambda_closure(self, state):
        if state in self.visited:
            return set()

        self.visited.add(state)
        accessible_states = set()
        accessible_states.add(state)

        for new_state in self.transitions[state][SpecialSymbol.Lambda]:
            self.lambda_closure(new_state)

        return accessible_states

    def lambda_closure_palo(self, K):
        accessible_states = set()

        for state in K:
            self.visited = set()
            accessible_states.union(self.lambda_closure(state))

        return accessible_states

    def move(self, T, char):
        accessible_states = set()

        for t in T:
            accessible_states.union(self.transitions[t][char])

        return self.lambda_closure_palo(accessible_states)

    def determinize(self) -> AFD:
        """Determiniza el autómata."""
        afd = AFD()
        nuevoInicial = self.lambda_closure_palo(self.initial_state)
        strInicial = afd.add_set_as_state(nuevoInicial, len(T.intersection(self.final_states)) == 0)
        afd.mark_initial_state(strInicial)

        Qp = [nuevoInicial]
        visited = []

        while len(Qp) != 0:
            T = Qp.pop(0)
            visited.append(T)
            for char in self.alphabet:
                U = self.move(T, char)
                if U in Qp and not (U in visited):
                    Qp.append(U)

                afd.add_transition(
                    afd.add_set_as_state(T, len(T.intersection(self.final_states)) == 0),
                    afd.add_set_as_state(U, len(U.intersection(self.final_states)) == 0),
                    char
                )

        afd.normalize_states()
        return afd

    def _rename_state_in_transitions(self, old_name: Hashable, new_name: Hashable):
        """Renombra un estado dentro de las transiciones del autómata."""
        self.transitions[new_name] = self.transitions[old_name]
        del self.transitions[old_name]
        for state in self.transitions:
            for char in self.transitions[state]:
                if old_name in self.transitions[state][char]:
                    self.transitions[state][char].remove(old_name)
                    self.transitions[state][char].add(new_name)

    def rename_states(self):
        for state in self.states:
            newState = "p" + state[1:]
            self._rename_state(state, newState)
            self._rename_state_in_transitions(state, newState)

    def _get_extended_alphabet(self) -> list[str]:
        """Obtiene el alfabeto extendido del autómata (incluyendo símbolos especiales)."""
        return list(self.alphabet) + [SpecialSymbol.Lambda]

    def _transitions_to_str(self, state: Hashable) -> dict[Hashable, str]:
        """Devuelve las transiciones de un estado para cada símbolo como string."""
        transitions = {}
        for char in self._get_extended_alphabet():
            if char in self.transitions[state]:
                transitions[char] = ",".join(self.transitions[state][char])
            else:
                transitions[char] = "-"
        return transitions
