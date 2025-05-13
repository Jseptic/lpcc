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
    # Checks if the token starts with '=' (assumes ASCII '=')
    return tok.startswith("=")

def pass1(lines):
    locctr       = 0
    all_literals = []   # Global literal pool (in order of appearance)
    pending      = []   # Literals waiting for pool assignment
    pool_table   = []   # Starting index (1-based) for each literal pool

    for lineno, line in enumerate(lines, 1):
        # Remove comments and trim whitespace.
        line = line.split(';')[0].strip()
        if not line:
            continue

        # Tokenize on whitespace and commas.
        parts = [t for t in line.replace(',', ' ').split() if t]
        if not parts:
            continue

        # Handle START.
        if parts[0] == 'START':
            if len(parts) != 2 or not is_number(parts[1]):
                print(f"Error on line {lineno}: invalid START", file=sys.stderr)
                sys.exit(1)
            locctr = int(parts[1])
            continue

        # Handle LTORG – close the current literal pool.
        if parts[0] == 'LTORG':
            if pending:
                start_idx = len(all_literals) - len(pending) + 1
                pool_table.append(start_idx)
                locctr += len(pending)
                pending.clear()
            continue

        # If a label is present, skip it.
        idx = 0
        if parts[0] not in IMPERATIVES and parts[0] not in DECLARATIVES and parts[0] not in DIRECTIVES:
            idx = 1

        opcode = parts[idx]
        
        # Process all tokens in the operand part (everything from idx+1 onwards).
        for tok in parts[idx+1:]:
            # Normalize fancy quotes to ASCII quotes (if any).
            norm_tok = tok.replace("’", "'")
            if is_literal(norm_tok):
                if norm_tok not in all_literals:
                    all_literals.append(norm_tok)
                    pending.append(norm_tok)
        
        # Update locctr for various instructions/declarations.
        if opcode in IMPERATIVES:
            locctr += 1
        elif opcode in DECLARATIVES:
            # For declarations, the operand must be a number.
            if len(parts) <= idx+1 or not is_number(parts[idx+1]):
                print(f"Error on line {lineno}: invalid {opcode}", file=sys.stderr)
                sys.exit(1)
            locctr += int(parts[idx+1])
        elif opcode == 'END':
            # Finalize any pending literal pool at END.
            if pending:
                start_idx = len(all_literals) - len(pending) + 1
                pool_table.append(start_idx)
                locctr += len(pending)
                pending.clear()
            break
        # For DIRECTIVES (other than START, LTORG, END), no locctr update is needed.
        
    return all_literals, pool_table

def main():
    if len(sys.argv) != 2:
        print("Usage: python a3.py <sourcefile.asm>")
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        lines = f.readlines()

    literals, pools = pass1(lines)

    # Print Literal Table.
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
