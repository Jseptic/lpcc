import sys

# Define opcode classes
IMPERATIVES = {'STOP','ADD','SUB','MOVER','MOVEM','COMP','BC','DIV','READ','PRINT'}
DECLARATIVES = {'DS','DC'}
DIRECTIVES   = {'START','END'}

def is_number(s):
    try:
        int(s)
        return True
    except:
        return False

def is_literal(tok):
    return tok.startswith('=')

def pass1(lines):
    lit_pool = []   # list of literals in order of appearance
    locctr = 0

    for lineno, line in enumerate(lines, 1):
        # strip comments & whitespace
        line = line.split(';')[0].strip()
        if not line:
            continue

        # tokenize on whitespace/comma
        parts = [t for t in line.replace(',', ' ').split() if t]
        if not parts:
            continue

        # handle START
        if parts[0] == 'START':
            if len(parts) != 2 or not is_number(parts[1]):
                print(f"Error on line {lineno}: invalid START", file=sys.stderr)
                sys.exit(1)
            locctr = int(parts[1])
            continue

        # skip label if present
        idx = 0
        if parts[0] not in IMPERATIVES and parts[0] not in DECLARATIVES and parts[0] not in DIRECTIVES:
            idx = 1

        opcode  = parts[idx]
        operand = parts[idx+1] if len(parts) > idx+1 else None

        # collect literal
        if operand and is_literal(operand) and operand not in lit_pool:
            lit_pool.append(operand)

        # update LOCCTR
        if opcode in IMPERATIVES:
            locctr += 1
        elif opcode == 'DC':
            locctr += 1
        elif opcode == 'DS':
            if not operand or not is_number(operand):
                print(f"Error on line {lineno}: invalid DS", file=sys.stderr)
                sys.exit(1)
            locctr += int(operand)
        elif opcode == 'END':
            break
        else:
            print(f"Error on line {lineno}: unknown opcode '{opcode}'", file=sys.stderr)
            sys.exit(1)

    # assign addresses to literals at end of program
    lit_tab = {}
    for lit in lit_pool:
        lit_tab[lit] = locctr
        locctr += 1

    return lit_tab

def main():
    if len(sys.argv) != 2:
        print("Usage: python b2.py <sourcefile.asm>")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        lines = f.readlines()

    lit_tab = pass1(lines)

    print("Literal\tAddress")
    print("---------------")
    for lit, addr in lit_tab.items():
        print(f"{lit}\t{addr}")

if __name__ == '__main__':
    main()