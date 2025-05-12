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
    symtab = {}       # symbol -> address
    locctr = 0
    for lineno, line in enumerate(lines,1):
        # strip comments and whitespace
        line = line.split(';')[0].strip()
        if not line:
            continue

        # split tokens by whitespace or comma
        parts = [tok.strip() for tok in line.replace(',', ' ').split() if tok.strip()]
        if not parts:
            continue

        # handle START
        if parts[0] == 'START':
            if len(parts) != 2 or not is_number(parts[1]):
                print(f"Error on line {lineno}: invalid START", file=sys.stderr)
                sys.exit(1)
            locctr = int(parts[1])
            continue

        # detect label
        label = None
        opcode_idx = 0
        if parts[0] not in IMPERATIVES and parts[0] not in DECLARATIVES and parts[0] not in DIRECTIVES:
            label = parts[0]
            opcode_idx = 1

        opcode = parts[opcode_idx]
        operand = parts[opcode_idx+1] if len(parts) > opcode_idx+1 else None

        # enter label
        if label:
            if label in symtab:
                print(f"Error: duplicate symbol '{label}' on line {lineno}", file=sys.stderr)
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
    # read source from stdin or a file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            lines = f.readlines()
    else:
        print("Usage: python symbol_table.py <sourcefile.asm>")
        sys.exit(1)

    symtab = pass1(lines)

    # print symbol table
    print("Symbol\tAddress")
    print("--------------")
    for sym, addr in symtab.items():
        print(f"{sym}\t{addr}")

if __name__ == '__main__':
    main()