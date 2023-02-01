from typing import Literal
class Morse:
    # The timing in Morse code is based around the length of one "dit" (or 
    # "dot" if you like). From the dit length we can derive the length of a
    # "dah" (or "dash") and the various pauses.
    # Source: https://morsecode.world/international/timing.html

    # Dit: 1 unit
    DIT: int = 1

    # Dah: 3 units
    DAH: int = 3

    # The gap between dits and dahs within a character: 1 unit
    INTRA_CHAR_SPACE: int = 1

    # The gap between the characters of a word: 3 units
    INTER_CHAR_SPACE: int = 3

    # The gap between two words: 7 units
    WORD_SPACE: int = 7

    MORSE: dict[str, list[int]] = {
        "A": [DIT, DAH],
        "B": [DAH, DIT, DIT, DIT],
        "C": [DAH, DIT, DAH, DIT],
        "D": [DAH, DIT, DIT],
        "E": [DIT],
        "F": [DIT, DIT, DAH, DIT],
        "G": [DAH, DAH, DIT],
        "H": [DIT, DIT, DIT, DIT],
        "I": [DIT, DIT],
        "J": [DIT, DAH, DAH, DAH],
        "K": [DAH, DIT, DAH],
        "L": [DIT, DAH, DIT, DIT],
        "M": [DAH, DAH],
        "N": [DAH, DIT],
        "O": [DAH, DAH, DAH],
        "P": [DIT, DAH, DAH, DIT],
        "Q": [DAH, DAH, DIT, DAH],
        "R": [DIT, DAH, DIT],
        "S": [DIT, DIT, DIT],
        "T": [DAH],
        "U": [DIT, DIT, DAH],
        "V": [DIT, DIT, DIT, DAH],
        "W": [DIT, DAH, DAH],
        "X": [DAH, DIT, DIT, DAH],
        "Y": [DAH, DIT, DAH, DAH],
        "Z": [DAH, DAH, DIT, DIT],
        "1": [DIT, DAH, DAH, DAH, DAH],
        "2": [DIT, DIT, DAH, DAH, DAH],
        "3": [DIT, DIT, DIT, DAH, DAH],       
        "4": [DIT, DIT, DIT, DIT, DAH],
        "5": [DIT, DIT, DIT, DIT, DIT],
        "6": [DAH, DIT, DIT, DIT, DIT],
        "7": [DAH, DAH, DIT, DIT, DIT],       
        "8": [DAH, DAH, DAH, DIT, DIT],                      
        "9": [DAH, DAH, DAH, DAH, DIT],
        "0": [DAH, DAH, DAH, DAH, DAH],
    }

    def _ook_timing(self) -> list[int]:
        """ Generate On Off Keying timing"""

        # 1 = on, 0 = off
        ook_sequence: list[int] = []

        # Loop through characters in text
        for text_idx, character in enumerate(self.text):

            # If character is a space, add a word space
            if character.isspace():
                ook_sequence.extend([0] * self.WORD_SPACE)
                continue

            # If it is a character, add characters and spaces
            if character.isalnum():
                # Example: A = [1, 3]
                morse_character: list[int] = self.MORSE[character]
                for char_idx, i in enumerate(morse_character):
                    ook_sequence.extend([1] * i)
                
                    # Add intra character space, but not after last element
                    if char_idx + 1 < len(morse_character):
                        ook_sequence.extend([0] * self.INTRA_CHAR_SPACE)

            # Add inter character space, but not after last element,
            # and not if next character is a space.
            if text_idx + 1 < len(self.text) and not self.text[text_idx + 1].isspace():
                ook_sequence.extend([0] * self.INTER_CHAR_SPACE)

        return ook_sequence

    def __init__(
        self,
        text: str,
    ) -> None:
        self.text: str = text.upper()
        self.ook_timing: list[int] = self._ook_timing()

def main() -> None:
    morse: Morse = Morse(
        text = "test",
    )
    print(morse.ook_timing)


if __name__ == "__main__":
    main()
