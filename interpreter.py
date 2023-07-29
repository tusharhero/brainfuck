# The GPLv3 License (GPLv3)

# Copyright © 2023 Tushar Maharana

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
A simple brainfuck interpreter
"""
import sys


class BrainFuckMachine:
    def __init__(self, tape_length: int, program: list[str]):
        self.tape: list[int] = [0 for _ in range(tape_length)]
        self.program: list[str] = program
        self.pointer = 0
        self.jumps = self.get_jumps()
        self.reverse_jumps = {v: k for k, v in self.jumps.items()}

    def get_jumps(self):
        pairs = []
        stack = []
        for index, instruction in enumerate(self.program):
            if instruction == "[":
                stack.append(index)
            elif instruction == "]":
                assert stack
                start_loop_index = stack.pop()
                end_loop_index = index
                pairs.append((start_loop_index, end_loop_index))
        return dict(pairs)

    def execute(self):
        index = 0
        while index < len(self.program):
            instruction = self.program[index]
            self.pointer %= TAPE_LENGTH
            match instruction:
                case ".":
                    print(chr(self.tape[self.pointer]), end="")
                case ">":
                    self.pointer += 1
                case "<":
                    self.pointer -= 1
                case "+":
                    self.tape[self.pointer] += 1
                case "-":
                    self.tape[self.pointer] -= 1
                case "]":
                    if self.tape[self.pointer] != 0:
                        self.index = self.reverse_jumps[index]
                case "[":
                    if self.tape[self.pointer] == 0:
                        index = self.jumps[index] + 1
                case ",":
                    self.tape[self.pointer] = ord(sys.stdin.read(1))
                case "#":
                    self.debug(max(5, self.pointer))
            index += 1

    def debug(self, slice: int):
        print(f"\n\nDEBUG INFO: pointer at {self.pointer}")
        print("\n|", end="")
        sliced_tape = self.tape[:slice]
        for cell in sliced_tape:
            print(f"{cell}", end="|")
        print("\n", end=" ")
        for current_pointer, cell in enumerate(sliced_tape):
            print(f"{'^'if current_pointer == self.pointer else ' '}", end=" ")


TAPE_LENGTH = 30000

with open(sys.argv[1], "r") as program_file:
    program: list[str] = [
        char
        for char in program_file.read()
        if char in {".", ">", "<", "+", "-", "[", "]", ",", "#"}
    ]
machine = BrainFuckMachine(TAPE_LENGTH, program)
machine.execute()
