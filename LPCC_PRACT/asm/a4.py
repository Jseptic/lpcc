import sys

# Mapping for opcodes (AD = Assembler Directive, IS = Imperative Statement, DL = Declarative)
OPCODE_MAP = {
    'START': '(AD,01)',
    'END':   '(AD,02)',
    'READ':  '(IS,04)',
    'MOVER': '(IS,05)',
    'SUB':   '(IS,08)',
    'STOP':  '(IS,00)'
}

# Declarative statement mapping
DECLARATIVE_MAP = {
    'DS': '(DL,01)',
    'DC': '(DL,02)'
}

# Register mapping
REGISTER_MAP = {
    'AREG': '(R,1)',
    'BREG': '(R,2)',
    'CREG': '(R,3)'
}

# Global symbol table. Initially, symbols referenced in imperative statements may be added
# with a placeholder address (None). Later, when a declarative statement appears, the address
# is updated.
symbol_table = {}

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def pass1(lines):
    locctr = 0
    intermediate = []

    for lineno, line in enumerate(lines, 1):
        # Remove comments and trim whitespace.
        line = line.split(';')[0].strip()
        if not line:
            continue

        # Tokenize on whitespace and commas.
        # (For simplicity, this version assumes tokens are separated by spaces and commas.)
        parts = [t for t in line.replace(',', ' ').split() if t]
        if not parts:
            continue

        # Handle START directive.
        if parts[0] == 'START':
            if len(parts) != 2 or not is_number(parts[1]):
                print(f"Error on line {lineno}: invalid START", file=sys.stderr)
                sys.exit(1)
            locctr = int(parts[1])
            intermediate.append(f"{locctr}\t{OPCODE_MAP['START']} (C,{parts[1]})")
            continue

        # Check if the line begins with a label. If the first token isn't an opcode (imperative,
        # declarative, or directive), then it is a label.
        idx = 0
        if parts[0] not in OPCODE_MAP and parts[0] not in DECLARATIVE_MAP and parts[0] not in {'END'}:
            label = parts[0]
            # If this label is not already in the symbol table, add it.
            # (It might have been previously referenced in an imperative.)
            symbol_table[label] = None
            idx = 1
        else:
            label = None

        # Determine the opcode.
        opcode = parts[idx]

        # Process declarative statements (DS or DC).
        if opcode in DECLARATIVE_MAP:
            # The label must be defined (either from a prior reference or here).
            if label is None:
                # Declarative statement without a label is an error.
                print(f"Error on line {lineno}: missing label in declarative statement", file=sys.stderr)
                sys.exit(1)
            # Update the symbol's address in the symbol table with the current LOCCTR.
            symbol_table[label] = locctr
            # The next token should be the constant size.
            if len(parts) <= idx+1 or not is_number(parts[idx+1]):
                print(f"Error on line {lineno}: invalid {opcode}", file=sys.stderr)
                sys.exit(1)
            data_size = int(parts[idx+1])
            intermediate.append(f"{locctr}\t{DECLARATIVE_MAP[opcode]} (C,{parts[idx+1]})")
            locctr += data_size
            continue

        # Process imperative statements.
        if opcode in OPCODE_MAP:
            # For READ, operand is a symbol
            if opcode == 'READ':
                operand = parts[idx+1]
                if operand not in symbol_table:
                    symbol_table[operand] = None  # add as undefined for now
                intermediate.append(f"{locctr}\t{OPCODE_MAP[opcode]} (S,{operand})")
                locctr += 1
            # For MOVER, SUB, etc.
            elif opcode in {'MOVER', 'SUB'}:
                reg = parts[idx+1].rstrip(',')  # e.g., AREG
                operand = parts[idx+2]
                if operand not in symbol_table:
                    symbol_table[operand] = None
                reg_code = REGISTER_MAP.get(reg, f"(R,{reg})")
                intermediate.append(f"{locctr}\t{OPCODE_MAP[opcode]} {reg_code} (S,{operand})")
                locctr += 1
            # For STOP or any single operand instruction.
            elif opcode == 'STOP':
                intermediate.append(f"{locctr}\t{OPCODE_MAP[opcode]}")
                locctr += 1
            else:
                # Other imperatives can be added as needed.
                locctr += 1
        elif opcode == 'END':
            intermediate.append(f"{locctr}\t{OPCODE_MAP['END']}")
            break
        else:
            # If opcode is unrecognized, just increment LOCCTR (or print error).
            locctr += 1

    return intermediate, symbol_table

def main():
    if len(sys.argv) != 2:
        print("Usage: python a4.py <sourcefile.asm>")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        lines = f.readlines()

    intermediate, symbols = pass1(lines)

    print("Intermediate Code:")
    for line in intermediate:
        print(line)

    print("\nSymbol Table:")
    print("Symbol\tAddress")
    print("------\t-------")
    for sym, addr in symbols.items():
        print(f"{sym}\t{addr if addr is not None else '----'}")

if __name__ == '__main__':
    main()
