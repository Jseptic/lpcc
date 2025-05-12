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

def pass1(lines):
    symtab = {}
    locctr = 0
    for lineno, line in enumerate(lines, 1):
        # remove comments & trim
        line = line.split(';')[0].strip()
        if not line:
            continue

        # tokenize on whitespace/comma
        parts = [t for t in line.replace(',', ' ').split() if t]
        if not parts:
            continue

        # START directive
        if parts[0] == 'START':
            if len(parts) != 2 or not is_number(parts[1]):
                print(f"Error on line {lineno}: invalid START", file=sys.stderr)
                sys.exit(1)
            locctr = int(parts[1])
            continue

        # detect label
        label = None
        idx = 0
        if parts[0] not in IMPERATIVES and parts[0] not in DECLARATIVES and parts[0] not in DIRECTIVES:
            label = parts[0]
            idx = 1

        opcode = parts[idx]
        operand = parts[idx+1] if len(parts) > idx+1 else None

        # enter symbol
        if label:
            if label in symtab:
                print(f"Error on line {lineno}: duplicate symbol '{label}'", file=sys.stderr)
                sys.exit(1)
            symtab[label] = locctr

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

    return symtab

def main():
    if len(sys.argv) != 2:
        print("Usage: python b1.py <sourcefile.asm>")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        lines = f.readlines()

    symtab = pass1(lines)

    print("Symbol\tAddress")
    print("--------------")
    for sym, addr in symtab.items():
        print(f"{sym}\t{addr}")

if __name__ == '__main__':
    main()