import sys

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
    # Checks if the token starts with '=' (assumes ASCII '=')
    return tok.startswith("=")

def pass1(lines):
    locctr       = 0
    all_literals = []  # List of all literals in order of first appearance.
    pending      = []  # Literals waiting to be assigned an address.
    pool_table   = []  # Starting index (1-based) for each literal pool

    for lineno, line in enumerate(lines, 1):
        # Remove comments and trim whitespace.
        line = line.split(';')[0].strip()
        if not line:
            continue

        # Tokenize on whitespace and commas.
        parts = [t for t in line.replace(',', ' ').split() if t]
        if not parts:
            continue

        # Handle START directive.
        if parts[0] == 'START':
            if len(parts) != 2 or not is_number(parts[1]):
                print(f"Error on line {lineno}: invalid START", file=sys.stderr)
                sys.exit(1)
            locctr = int(parts[1])
            continue

        # Handle LTORG directive - assign addresses to pending literals and record pool start.
        if parts[0] == 'LTORG':
            if pending:
                start_idx = len(all_literals) - len(pending) + 1  # 1-based index.
                pool_table.append(start_idx)
                locctr += len(pending)
                pending.clear()
            continue

        # Detect label: if the first token is not an opcode or directive, treat it as a label.
        idx = 0
        if parts[0] not in IMPERATIVES and parts[0] not in DECLARATIVES and parts[0] not in DIRECTIVES:
            idx = 1

        opcode = parts[idx]

        # Process all tokens in the operand part (everything from parts[idx+1:])
        for tok in parts[idx+1:]:
            # Optionally, normalize token if needed (e.g. fancy quotes).
            norm_tok = tok.replace("’", "'")
            if is_literal(norm_tok) and norm_tok not in all_literals:
                all_literals.append(norm_tok)
                pending.append(norm_tok)

        # Update locctr based on opcode.
        if opcode in IMPERATIVES:
            locctr += 1
        elif opcode == 'DC':
            locctr += 1
        elif opcode == 'DS':
            if len(parts) <= idx+1 or not is_number(parts[idx+1]):
                print(f"Error on line {lineno}: invalid DS", file=sys.stderr)
                sys.exit(1)
            locctr += int(parts[idx+1])
        elif opcode == 'END':
            # Process any remaining pending literals on encountering END.
            if pending:
                start_idx = len(all_literals) - len(pending) + 1
                pool_table.append(start_idx)
                locctr += len(pending)
                pending.clear()
            break
        else:
            # For directives or unrecognized opcodes, no LOCCTR update.
            pass

    return all_literals, pool_table

def main():
    if len(sys.argv) != 2:
        print("Usage: python b3.py <sourcefile.asm>")
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
    for j, start in enumerate(pools, 1):
        print(f"{j}\t{start}")

if __name__ == '__main__':
    main()
