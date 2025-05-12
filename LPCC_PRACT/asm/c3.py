import sys

# Define opcode classes
IMPERATIVES  = {'STOP', 'ADD', 'SUB', 'MOVER', 'MOVEM', 'COMP', 'BC', 'DIV', 'READ', 'PRINT'}
DECLARATIVES = {'DS', 'DC'}
DIRECTIVES   = {'START', 'END', 'LTORG'}

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def is_literal(tok):
    return tok.startswith('=')

def pass1(lines):
    locctr = 0
    all_literals = []  # stores all literals in order of appearance
    pending = []       # literals waiting to be assigned an address (current pool)
    pool_table = []    # list of starting literal numbers (1-based) for each pool

    for lineno, line in enumerate(lines, 1):
        # Remove comments and trim whitespace
        line = line.split(';')[0].strip()
        if not line:
            continue

        # Tokenize on whitespace or comma
        parts = [t for t in line.replace(',', ' ').split() if t]
        if not parts:
            continue

        # Handle START directive
        if parts[0] == 'START':
            if len(parts) != 2 or not is_number(parts[1]):
                print(f"Error on line {lineno}: invalid START", file=sys.stderr)
                sys.exit(1)
            locctr = int(parts[1])
            continue

        # Handle LTORG directive - assign addresses to pending literals and mark a new pool
        if parts[0] == 'LTORG':
            if pending:
                start_idx = len(all_literals) - len(pending) + 1  # 1-based index of first literal in current pool
                pool_table.append(start_idx)
                locctr += len(pending)
                pending.clear()
            continue

        # Check for label; if first token is not an opcode, declarative, or directive then skip it as a label.
        idx = 0
        if parts[0] not in IMPERATIVES and parts[0] not in DECLARATIVES and parts[0] not in DIRECTIVES:
            idx = 1

        opcode = parts[idx]
        operand = parts[idx+1] if len(parts) > (idx+1) else None

        # Collect literal if operand is literal and not already recorded
        if operand and is_literal(operand) and operand not in all_literals:
            all_literals.append(operand)
            pending.append(operand)

        # Update the location counter
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
            # At END, process remaining pending literals (if any) as a final pool
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
        print("Usage: python c3.py <sourcefile.asm>")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        lines = f.readlines()

    literals, pools = pass1(lines)

    print("Literal Table:")
    print("Lit#\tLiteral")
    print("----\t-------")
    for i, lit in enumerate(literals, 1):
        print(f"{i}\t{lit}")

    print("\nPool Table:")
    print("Pool#\tStart Lit#")
    print("-----\t----------")
    for p, start in enumerate(pools, 1):
        print(f"{p}\t{start}")

if __name__ == '__main__':
    main()