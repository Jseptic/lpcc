import sys

# Opcode mappings
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

# Register mapping example (only AREG is used in this sample)
REGISTER_MAP = {
    'AREG': '1',
    'BREG': '2',
    'CREG': '3'
}

def pass1(lines):
    locctr = 0
    symtab = {}       # Symbol table: { symbol: address }
    intermediate = [] # List to hold intermediate code lines

    for lineno, line in enumerate(lines, 1):
        # Remove comments (if any) and trim whitespace
        line = line.split(';')[0].strip()
        if not line:
            continue

        # Tokenize: split on whitespace and commas
        tokens = [token for token in line.replace(',', ' ').split() if token]

        # If tokens is empty then skip
        if not tokens:
            continue

        # Check if first token is a label: if it's not a directive (START, END, LTORG) or an opcode/declarative.
        label = None
        if tokens[0] not in OPCODE_MAP and tokens[0] not in DECLARATIVE_MAP:
            # Assume it is a label and add it to the symbol table with current LC
            label = tokens[0]
            if label not in symtab:
                symtab[label] = locctr
            tokens = tokens[1:]
            if not tokens:
                continue

        opcode = tokens[0]
        # Operand: might be a symbol or register/symbol combination. For directives like START, DS, the next token is the operand.
        operand = tokens[1] if len(tokens) > 1 else None

        # Process the START directive: initialize LC and generate corresponding intermediate code.
        if opcode == 'START':
            if not operand or not operand.isdigit():
                print(f"Error: Invalid operand for START on line {lineno}")
                sys.exit(1)
            locctr = int(operand)
            intermediate.append(f"{locctr}\t{OPCODE_MAP[opcode]}\t(C,{operand})")
            continue

        # Process END directive
        if opcode == 'END':
            intermediate.append(f"{locctr}\t{OPCODE_MAP[opcode]}")
            break

        # Process Declarative statements (DS)
        if opcode in DECLARATIVE_MAP:
            # For DS, the operand represents the size of the reservation.
            if not operand or not operand.isdigit():
                print(f"Error: Invalid operand for {opcode} on line {lineno}")
                sys.exit(1)
            intermediate.append(f"{locctr}\t{DECLARATIVE_MAP[opcode]}\t(C,{operand})")
            locctr += int(operand)
            continue

        # Process Imperative statements
        if opcode in OPCODE_MAP:
            code = OPCODE_MAP[opcode]
            line_intermediate = f"{locctr}\t{code}"
            if opcode == 'STOP':
                intermediate.append(line_intermediate)
                locctr += 1
                continue

            # Handle READ instruction (assumes operand is a symbol)
            if opcode == 'READ':
                # Add symbol to symbol table if not already present.
                if operand not in symtab:
                    symtab[operand] = None  # address to be defined later via DS
                line_intermediate += f"\t(S,{operand})"
            else:
                # For instructions like MOVER and SUB, expect a register operand followed by a symbol.
                reg = tokens[1] if tokens[1] in REGISTER_MAP else None
                if reg:
                    # Operand is assumed to be in the next token.
                    sym = tokens[2] if len(tokens) > 2 else None
                    if sym and sym not in symtab:
                        symtab[sym] = None
                    line_intermediate += f"\t(R,{REGISTER_MAP[reg]})\t(S,{sym})"
                else:
                    # If no register is detected, assume operand is a symbol.
                    if operand and operand not in symtab:
                        symtab[operand] = None
                    line_intermediate += f"\t(S,{operand})"
            intermediate.append(line_intermediate)
            locctr += 1
            continue

        # If opcode is not recognized, print error and exit.
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