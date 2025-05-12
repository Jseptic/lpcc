import sys

# Mapping for opcodes:
# AD = Assembler Directive, IS = Imperative Statement, DL = Declarative
OPCODE_MAP = {
    'START': '(AD,01)',  # START directive
    'END':   '(AD,02)',  # END directive
    'READ':  '(IS,04)',
    'MOVER': '(IS,05)',
    'SUB':   '(IS,06)',
    'STOP':  '(IS,00)'
}

# Declarative statements mapping
DECLARATIVE_MAP = {
    'DS': '(DL,01)'
}

# Register mapping (if required)
REGISTER_MAP = {
    'AREG': '1',
    'BREG': '2',
    'CREG': '3'
}

def pass1(lines):
    locctr = 0
    symtab = {}       # Symbol Table {symbol: address}
    intermediate = [] # List to hold intermediate code lines

    for lineno, line in enumerate(lines, 1):
        # Remove comments and trim the whitespace
        line = line.split(';')[0].strip()
        if not line:
            continue

        # Tokenize by whitespace and comma
        tokens = [token for token in line.replace(',', ' ').split() if token]

        # Skip if no tokens present
        if not tokens:
            continue

        # If first token is not a known opcode or declarative, treat it as a label.
        label = None
        first = tokens[0]
        if first not in OPCODE_MAP and first not in DECLARATIVE_MAP:
            label = first
            # Record label in symbol table with current LC if not already recorded.
            if label not in symtab:
                symtab[label] = locctr
            tokens = tokens[1:]
            if not tokens:
                continue

        opcode = tokens[0]
        operand = tokens[1] if len(tokens) > 1 else None

        # Process START directive: set LC to given operand.
        if opcode == 'START':
            if not operand or not operand.isdigit():
                print(f"Error on line {lineno}: Invalid operand for START")
                sys.exit(1)
            locctr = int(operand)
            intermediate.append(f"{locctr}\t{OPCODE_MAP[opcode]}\t(C,{operand})")
            continue

        # Process END directive: generate code and break.
        if opcode == 'END':
            intermediate.append(f"{locctr}\t{OPCODE_MAP[opcode]}")
            break

        # Process Declarative Statements (DS)
        if opcode in DECLARATIVE_MAP:
            if not operand or not operand.isdigit():
                print(f"Error on line {lineno}: Invalid operand for {opcode}")
                sys.exit(1)
            # If there's a label, it already exists in symbol table.
            intermediate.append(f"{locctr}\t{DECLARATIVE_MAP[opcode]}\t(C,{operand})")
            locctr += int(operand)
            continue

        # Process Imperative Statements
        if opcode in OPCODE_MAP:
            code = OPCODE_MAP[opcode]
            line_intermediate = f"{locctr}\t{code}"
            if opcode == 'STOP':
                intermediate.append(line_intermediate)
                locctr += 1
                continue

            # For READ, the operand is a symbol.
            if opcode == 'READ':
                # Add symbol to symbol table (address to be backfilled by DS later) if not present.
                if operand not in symtab:
                    symtab[operand] = None
                line_intermediate += f"\t(S,{operand})"
            else:
                # For instructions like MOVER, SUB that require a register and a symbol.
                reg = tokens[1] if tokens[1] in REGISTER_MAP else None
                if reg:
                    sym = tokens[2] if len(tokens) > 2 else None
                    if sym and sym not in symtab:
                        symtab[sym] = None
                    line_intermediate += f"\t(R,{REGISTER_MAP[reg]})\t(S,{sym})"
                else:
                    # Else, process operand as symbol.
                    if operand and operand not in symtab:
                        symtab[operand] = None
                    line_intermediate += f"\t(S,{operand})"
            intermediate.append(line_intermediate)
            locctr += 1
            continue

        # If opcode is unrecognized.
        print(f"Error: Unknown opcode '{opcode}' on line {lineno}")
        sys.exit(1)

    return intermediate, symtab

def main():
    if len(sys.argv) != 2:
        print("Usage: python intermediate_code.py <sourcefile.asm>")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        lines = f.readlines()

    intermediate, symtab = pass1(lines)

    print("Intermediate Code:")
    for line in intermediate:
        print(line)

    print("\nSymbol Table:")
    print("Symbol\tAddress")
    for sym, addr in symtab.items():
        print(f"{sym}\t{addr if addr is not None else '----'}")

if __name__ == '__main__':
    main()