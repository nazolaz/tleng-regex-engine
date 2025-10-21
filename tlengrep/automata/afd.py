from typing import Hashable
from automata.af import AF

__all__ = ["AFD"]


class AFD(AF):
    """Autómata finito determinístico."""

    def add_transition(self, state1: Hashable, state2: Hashable, char: str):
        """Agrega una transición al autómata."""
        if state1 not in self.states:
            raise ValueError(f"El estado {state1} no pertenece al autómata.")
        if state2 not in self.states:
            raise ValueError(f"El estado {state2} no pertenece al autómata.")
        self.transitions[state1][char] = state2
        self.alphabet.add(char)

    def add_set_as_state(self, stateSet, isFinal):
        setString = ''.join(stateSet)
        if not (setString in self.states):
            self.add_state(setString, isFinal)
        return setString

    def minimize(self):
        """Minimiza el autómata."""
        accesible = set()
        accesible.add(self.initial_state)
        new = set()
        new.add(self.initial_state)
        while len(new) != 0:
            temp = set()
            for q in new:
                for c in self.alphabet:
                    if c in self.transitions[q]:
                        temp.add(self.transitions[q][c])
            new = temp.difference(accesible)
            accesible = accesible.union(new)   
                    
        afd_accessible = AFD()

        for state in accesible:
            afd_accessible.add_state(state, state in self.final_states)

        afd_accessible.initial_state = self.initial_state

        for state in accesible:
            for char in self.alphabet:
                if state in self.transitions and char in self.transitions[state]:
                    otherState = self.transitions[state][char]
                    if otherState in accesible:
                        afd_accessible.add_transition(state, otherState, char)

        P = set(frozenset())
        P.add(frozenset(afd_accessible.final_states))
        P.add(frozenset(afd_accessible.states.difference(afd_accessible.final_states)))
        W = [afd_accessible.final_states]

        while len(W) != 0:
            A = W.pop()
            for c in afd_accessible.alphabet:
                X = set()
                for state in afd_accessible.transitions:
                    if c in afd_accessible.transitions[state] and afd_accessible.transitions[state][c] in A:
                        X.add(state)
                X = frozenset(X)

                for Y in P:
                    if len(X.intersection(Y)) != 0 and len(Y.difference(X)) != 0:
                        P.remove(Y)
                        P.add(X.intersection(Y))
                        P.add(Y.difference(X))

                        if Y in W:
                            P.remove(Y)
                            P.add(X.intersection(Y))
                            P.add(Y.difference(X))
                        else:
                            if len(X.intersection(Y)) <= len(Y.difference(X)):
                                W.append(X.intersection(Y))
                            else:
                                W.append(Y.difference(X))

        P.discard(set())

        afdmin = AFD()
        afdmin.states = P

        for partition in P:
            for state in partition:
                for char in afd_accessible.alphabet:
                    if state in afd_accessible.transitions and char in afd_accessible.transitions[state]:
                        comingState = afd_accessible.transitions[state][char]
                        for otherPartition in P:
                            if comingState in otherPartition:
                                afdmin.add_transition(partition, otherPartition, char)
                                break # las particiones son disjuntas
        
        for partition in P:
            if "q0" in partition:
                afdmin.initial_state = partition
                break # las particiones son disjuntas

        for partition in P:
            for state in partition:
                if state in afd_accessible.final_states:
                    afdmin.final_states.add(partition)
                    break

        return afdmin

    def match(self, word: str) -> bool:
        return self.match_from(self.initial_state, word)

    def match_from(self, state: str, word: str) -> bool:
        if len(word) == 0:
            return state in self.final_states
        if state in self.transitions and word[0] in self.transitions[state]:
            return self.match_from(self.transitions[state][word[0]], word[1:])
        return False

    def _rename_state_in_transitions(self, old_name: Hashable, new_name: Hashable):
        """Renombra un estado dentro de las transiciones del autómata."""
        self.transitions[new_name] = self.transitions[old_name]
        del self.transitions[old_name]
        for state in self.transitions:
            for char in self.transitions[state]:
                if self.transitions[state][char] == old_name:
                    self.transitions[state][char] = new_name

    def _get_extended_alphabet(self) -> list[str]:
        """Obtiene el alfabeto extendido del autómata (incluyendo símbolos especiales)."""
        return list(self.alphabet)

    def _transitions_to_str(self, state: Hashable) -> dict[Hashable, str]:
        """Devuelve las transiciones de un estado para cada símbolo como string."""
        transitions = {}
        for char in self._get_extended_alphabet():
            if char in self.transitions[state]:
                transitions[char] = self.transitions[state][char]
            else:
                transitions[char] = "-"
        return transitions
        
