import copy

print('Advent of Code 2016 - Day 25')
with open('day25.txt') as f:
    given_ins = [line.split(' ') for line in f.read().splitlines()]

def isinteger(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def optimize(instruction):
    instruction = copy.deepcopy(instruction)

    i = 0
    while i <= len(instruction) - 5:
        if instruction[i+2][0] == instruction[i+4][0] == 'jnz':
            if instruction[i+2][2] == '-2' and instruction[i+4][2] == '-5':
                if all((
                    instruction[i][0] == 'inc',
                    instruction[i+1][0] == instruction[i+3][0] == 'dec'
                )):
                    arg_1 = instruction[i+1][1]
                    arg_2 = instruction[i+3][1]
                    prod = instruction[i][1]

                    instruction[i] = ['mul', arg_1, arg_2, prod]
                    instruction[i+1] = ['cpy', 0, arg_1]
                    instruction[i+2] = ['cpy', 0, arg_2]
                    instruction[i+3] = ['jnz', 0, 0]

                    i += 5
                    continue
        i += 1

    return instruction


ins = optimize(given_ins)
def reg_a(reg):
    i = 0
    signal = []
    
    while 0 <= i < len(ins):
        if ins[i][0] == 'inc':
            reg[ins[i][1]] += 1

        elif ins[i][0] == 'dec':
            reg[ins[i][1]] -= 1

        elif ins[i][0] == 'cpy':
            if isinteger(ins[i][1]):
                reg[ins[i][2]] = int(ins[i][1])
            else:
                reg[ins[i][2]] = reg[ins[i][1]]

        elif ins[i][0] == 'jnz':
            if isinteger(ins[i][1]):
                val = int(ins[i][1])
            else:
                val = reg[ins[i][1]]
            if val != 0:
                if isinteger(ins[i][2]):
                    i += int(ins[i][2])
                else:
                    i += reg[ins[i][2]]
                continue

        elif ins[i][0] == 'tgl':
            if isinteger(ins[i][1]):
                index = int(ins[i][1])
            else:
                index = reg[ins[i][1]]

            if 0 <= i+index < len(ins):
                instruction = ins[i+index]
                command = ins[i+index][0]

                if len(instruction) == 2:
                    if command == 'inc':
                        ins[i+index][0] = 'dec'
                    else:
                        ins[i+index][0] = 'inc'
                
                elif len(instruction) == 3:
                    if command == 'jnz':
                        ins[i+index][0] = 'cpy'
                    else:
                        ins[i+index][0] = 'jnz'

        elif ins[i][0] == 'mul':
            reg[ins[i][3]] += reg[ins[i][1]] * reg[ins[i][2]]

        elif ins[i][0] == 'out':
            if len(signal) < REPEATING_PATTERN:
                if isinteger(ins[i][1]):
                    signal.append(int(ins[i][1]))
                else:
                    signal.append(reg[ins[i][1]])
            else:
                break
                
        i += 1

    return signal


def test(a):
    registers = {
        'a': a,
        'b': 0,
        'c': 0,
        'd': 0
    }

    return reg_a(registers)


def find_correct_input():
    clock_signal = [0, 1] * (REPEATING_PATTERN//2)
    register_a = 0

    while test(register_a) != clock_signal:
        register_a += 1

    return register_a

REPEATING_PATTERN = 20
print(f'Part 1: {find_correct_input()}') # 189
print('Part 2: Complete all 49 stars in Advent of Code 2016')
