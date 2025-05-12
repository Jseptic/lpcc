import sys

# Define opcode classes
IMPERATIVES  = {'STOP','ADD','SUB','MOVER','MOVEM','COMP','BC','DIV','READ','PRINT'}
DECLARATIVES = {'DS','DC'}
DIRECTIVES   = {'START','END','LTORG'}

def is_number(s):
    try:
        int(s)
        return True
    except:
        return False

def is_literal(tok):
    return tok.startswith('=')

def pass1(lines):
    locctr        = 0
    all_literals  = []   # all literals in order of first appearance
    pending       = []   # literals waiting for pool assignment
    pool_table    = []   # starting index (1-based) of each literal pool

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

        # handle LTORG → close a pool
        if parts[0] == 'LTORG':
            if pending:
                # first-pending literal index in the global literal list
                start_idx = len(all_literals) - len(pending) + 1
                pool_table.append(start_idx)
                # assign addresses (just advance LOCCTR)
                locctr += len(pending)
                pending.clear()
            continue

        # detect label skip
        idx = 0
        if parts[0] not in IMPERATIVES and parts[0] not in DECLARATIVES and parts[0] not in DIRECTIVES:
            idx = 1

        opcode  = parts[idx]
        operand = parts[idx+1] if len(parts) > idx+1 else None

        # collect literal
        if operand and is_literal(operand) and operand not in all_literals:
            all_literals.append(operand)
            pending.append(operand)

        # update LOCCTR for instructions/declarations
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
            # final pool if any pending
            if pending:
                start_idx = len(all_literals) - len(pending) + 1
                pool_table.append(start_idx)
                locctr += len(pending)
                pending.clear()
            break
        else:
            print(f"Error on line {lineno}: unknown opcode '{opcode}'", file=sys.stderr)
            sys.exit(1)

    return all_literals, pool_table

def main():
    if len(sys.argv) != 2:
        print("Usage: python pool_table.py <sourcefile.asm>")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        lines = f.readlines()

    literals, pools = pass1(lines)

    # Print Literal Table
    print("Literal Table")
    print("Lit#\tLiteral")
    print("----\t-------")
    for i, lit in enumerate(literals, 1):
        print(f"{i}\t{lit}")

    print("\nPool Table")
    print("Pool#\tStart Lit#")
    print("-----\t----------")
    for p, start in enumerate(pools, 1):
        print(f"{p}\t{start}")

if __name__ == '__main__':
    main()