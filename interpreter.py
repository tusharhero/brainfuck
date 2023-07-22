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


def get_jumps(program: list[str]):
    pairs = []
    stack = []
    for index, instruction in enumerate(program):
        if instruction == "[":
            stack.append(index)
        elif instruction == "]":
            assert stack
            start_loop_index = stack.pop()
            end_loop_index = index
            pairs.append((start_loop_index, end_loop_index))
    return dict(pairs)


def execute(program: list[str], tape: list[int], initial_pointer: int):
    pointer = initial_pointer
    jumping: dict[int, int] = get_jumps(program)
    reverse_jumping = {v: k for k, v in jumping.items()}
    index = 0
    while index < len(program):
        instruction = program[index]
        match instruction:
            case ".":
                print(chr(tape[pointer]), end="")
            case ">":
                pointer += 1
            case "<":
                pointer -= 1
            case "+":
                tape[pointer] += 1
            case "-":
                tape[pointer] -= 1
            case "]":
                if tape[pointer] != 0:
                    index = reverse_jumping[index]
            case "[":
                if tape[pointer] == 0:
                    index = jumping[index] + 1
            case ",":
                tape[pointer] = ord(input())
        index += 1


TAPE_LENGTH = 3000

program: list[str] = [
    char
    for char in sys.stdin.read()
    if char in (".", ">", "<", "+", "-", "[", "]", ",")
]
tape: list[int] = [0 for _ in range(TAPE_LENGTH)]
pointer: int = 0
execute(program, tape, pointer)
