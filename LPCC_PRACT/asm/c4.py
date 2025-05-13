import sys

# Opcode mappings:
# AD = Assembler Directive, IS = Imperative Statement, DL = Declarative Statement
OPCODE_MAP = {
    'START': '(AD,01)',
    'END':   '(AD,02)',
    'READ':  '(IS,04)',
    'MOVER': '(IS,05)',
    'SUB':   '(IS,06)',
    'STOP':  '(IS,00)'
}

DECLARATIVE_MAP = {
    'DS': '(DL,01)'
}

# Register mapping (for instructions that use registers)
REGISTER_MAP = {
    'AREG': '1',
    'BREG': '2',
    'CREG': '3'
}

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def pass1(lines):
    locctr = 0
    symtab = {}       # Symbol table: { symbol: address }
    intermediate = [] # List to hold intermediate code lines

    for lineno, line in enumerate(lines, 1):
        # Remove comments and trim whitespace.
        line = line.split(';')[0].strip()
        if not line:
            continue

        # Tokenize: split on whitespace and commas.
        tokens = [token for token in line.replace(',', ' ').split() if token]
        if not tokens:
            continue

        # Check if first token is a label.
        # If the first token isn't a known opcode/directive, assume it's a label.
        label = None
        if tokens[0] not in OPCODE_MAP and tokens[0] not in DECLARATIVE_MAP and tokens[0] != 'END':
            label = tokens[0]
            # Add the label to the symbol table if not already present.
            if label not in symtab:
                symtab[label] = locctr
            # Remove the label token for further processing.
            tokens = tokens[1:]
            if not tokens:
                continue

        opcode = tokens[0]
        operand = tokens[1] if len(tokens) > 1 else None

        # Process START directive.
        if opcode == 'START':
            if not operand or not is_number(operand):
                print(f"Error on line {lineno}: Invalid operand for START")
                sys.exit(1)
            locctr = int(operand)
            intermediate.append(f"{locctr}\t{OPCODE_MAP[opcode]}\t(C,{operand})")
            continue

        # Process END directive.
        if opcode == 'END':
            intermediate.append(f"{locctr}\t{OPCODE_MAP[opcode]}")
            break

        # Process Declarative statements (e.g. DS).
        if opcode in DECLARATIVE_MAP:
            if label is None:
                print(f"Error on line {lineno}: Declarative statement missing a label")
                sys.exit(1)
            if not operand or not is_number(operand):
                print(f"Error on line {lineno}: Invalid operand for {opcode}")
                sys.exit(1)
            # Update the symbol table for the declaration (even if it was referenced earlier).
            symtab[label] = locctr
            intermediate.append(f"{locctr}\t{DECLARATIVE_MAP[opcode]}\t(C,{operand})")
            locctr += int(operand)
            continue

        # Process Imperative statements.
        if opcode in OPCODE_MAP:
            code = OPCODE_MAP[opcode]
            line_intermediate = f"{locctr}\t{code}"
            if opcode == 'STOP':
                intermediate.append(line_intermediate)
                locctr += 1
                continue

            # For READ: operand is assumed to be a symbol.
            if opcode == 'READ':
                if operand not in symtab:
                    # Add symbol with a placeholder (to be updated when defined).
                    symtab[operand] = None
                line_intermediate += f"\t(S,{operand})"
            else:
                # For instructions like MOVER, SUB: expect register and then a symbol.
                reg = tokens[1] if tokens[1] in REGISTER_MAP else None
                if reg:
                    sym = tokens[2] if len(tokens) > 2 else None
                    if sym and sym not in symtab:
                        symtab[sym] = None
                    line_intermediate += f"\t(R,{REGISTER_MAP[reg]})\t(S,{sym})"
                else:
                    if operand and operand not in symtab:
                        symtab[operand] = None
                    line_intermediate += f"\t(S,{operand})"
            intermediate.append(line_intermediate)
            locctr += 1
            continue

        # Unrecognized opcode.
        print(f"Error: Unknown opcode '{opcode}' on line {lineno}")
        sys.exit(1)

    return intermediate, symtab

def main():
    if len(sys.argv) != 2:
        print("Usage: python c4.py <sourcefile.asm>")
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
