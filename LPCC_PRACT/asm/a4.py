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
    'AREG': '1',
    'BREG': '2',
    'CREG': '3'
}

def pass1(lines):
    locctr = 0
    symtab = {}          # symbol table; key: symbol, value: address
    intermediate = []    # list of intermediate code lines

    for lineno, line in enumerate(lines, 1):
        # Remove comments & trim whitespace
        line = line.split(';')[0].strip()
        if not line:
            continue
        # Tokenize on whitespace or comma
        tokens = [t for t in line.replace(',', ' ').split() if t]

        # Skip empty tokens (if any)
        if not tokens:
            continue

        # Check if this line has a label.
        # If the first token is not a known opcode or declarative then treat it as a label.
        label = None
        first = tokens[0]
        if first not in OPCODE_MAP and first not in DECLARATIVE_MAP:
            label = first
            # record symbol with current LC if not already recorded
            if label not in symtab:
                symtab[label] = locctr
            # Remove the label token from tokens
            tokens = tokens[1:]
            if not tokens:
                continue

        opcode = tokens[0]
        operand = tokens[1] if len(tokens) > 1 else None

        # Process START directive: set LC and generate intermediate code for START.
        if opcode == 'START':
            if not operand or not operand.isdigit():
                print(f"Error: Invalid operand for START on line {lineno}")
                sys.exit(1)
            locctr = int(operand)
            intermediate.append(f"{locctr}\t{OPCODE_MAP[opcode]}\t(C,{operand})")
            continue

        # Process END directive: generate code and break.
        if opcode == 'END':
            intermediate.append(f"{locctr}\t{OPCODE_MAP[opcode]}")
            break

        # Process Declarative statements (DS, DC)
        if opcode in DECLARATIVE_MAP:
            # For DS, operand should be a number (storage size)
            if not operand or not operand.isdigit():
                print(f"Error: Invalid operand for {opcode} on line {lineno}")
                sys.exit(1)
            # If a label was present, it is already in symtab.
            intermediate.append(f"{locctr}\t{DECLARATIVE_MAP[opcode]}\t(C,{operand})")
            locctr += int(operand)
            continue

        # Process Imperative statements
        if opcode in OPCODE_MAP:
            code = OPCODE_MAP[opcode]
            line_intermediate = f"{locctr}\t{code}"
            # For STOP no operand is expected.
            if opcode == 'STOP':
                intermediate.append(line_intermediate)
                locctr += 1
                continue

            # For other imperatives, further processing of operand(s)
            # For instructions like READ that involve a variable:
            if opcode == 'READ':
                # Operand is assumed to be a symbol.
                # Add the symbol to symbol table if not present.
                if operand not in symtab:
                    symtab[operand] = None  # Address to be filled when declared.
                line_intermediate += f"\t(S,{operand})"
            else:
                # Expecting a register and a symbol operand, e.g.,
                # MOVER AREG, A  or  SUB AREG, B
                reg = tokens[1] if tokens[1] in REGISTER_MAP else None
                # If a register is present then the next token is the actual operand.
                if reg:
                    # Remove register from operand processing.
                    sym = tokens[2] if len(tokens) > 2 else None
                    # Add symbol to table if not present.
                    if sym and sym not in symtab:
                        symtab[sym] = None
                    line_intermediate += f"\t(R,{REGISTER_MAP[reg]})\t(S,{sym})"
                else:
                    # If no register is detected, treat operand as symbol.
                    if operand and operand not in symtab:
                        symtab[operand] = None
                    line_intermediate += f"\t(S,{operand})"
            intermediate.append(line_intermediate)
            locctr += 1
            continue

        # If opcode is not recognized, print error.
        print(f"Error: Unknown opcode {opcode} on line {lineno}")
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