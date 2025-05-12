import sys

def pass1(lines):
    """
    Pass 1: Build the Macro Definition Table (MDT)
    and collect the lines that are not part of macro definitions.
    """
    mdt = {}            # MDT: key = macro name, value = (formal_params, body_lines)
    non_macro_lines = []  # Lines that are not part of any macro definition
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        tokens = line.split()
        # If this line starts with "MACRO", then process a macro definition.
        if tokens[0].upper() == "MACRO":
            # Macro header line format: MACRO <macro_name> [<param1>, <param2>, ...]
            header_parts = line.split(None, 2)  # splits into ["MACRO", macro_name, rest-of-line (optional)]
            if len(header_parts) < 2:
                print("Error: Macro header missing macro name")
                sys.exit(1)
            macro_name = header_parts[1]
            if len(header_parts) > 2:
                # Parameters may be given separated by commas.
                params = [p.strip() for p in header_parts[2].split(',')]
            else:
                params = []
            i += 1
            body = []
            # Read macro body until a line that is exactly "MEND" (case-insensitive)
            while i < len(lines):
                body_line = lines[i].strip()
                if body_line.upper() == "MEND":
                    break
                body.append(body_line)
                i += 1
            mdt[macro_name] = (params, body)
            i += 1  # skip the MEND line
        else:
            non_macro_lines.append(line)
            i += 1
    return mdt, non_macro_lines

def expand_macro(macro_name, actual_params, mdt):
    """
    Given a macro call with actual parameters, use the MDT definition
    to expand the macro. Each occurrence of a formal parameter in the body is
    replaced by its corresponding actual argument.
    """
    formal_params, body = mdt[macro_name]
    # Build substitution dictionary: formal parameter -> actual argument
    sub_dict = {}
    for i, param in enumerate(formal_params):
        if i < len(actual_params):
            sub_dict[param] = actual_params[i]
        else:
            sub_dict[param] = ""
    expansion = []
    for line in body:
        tokens = line.split()
        new_tokens = []
        for token in tokens:
            # Replace token if it matches a formal parameter
            if token in sub_dict:
                new_tokens.append(sub_dict[token])
            else:
                new_tokens.append(token)
        expansion.append(" ".join(new_tokens))
    return expansion

def pass2(non_macro_lines, mdt):
    """
    Pass 2: Process the non‐macro lines. If a line invokes a macro,
    expand it. Otherwise, pass the line through unchanged.
    A simple location counter (LC) is prepended to each intermediate code line.
    """
    lc = 1
    intermediate = []
    for line in non_macro_lines:
        tokens = line.split()
        if not tokens:
            continue
        first = tokens[0]
        # If the first token is a defined macro name, treat this as a macro call.
        if first in mdt:
            # Get the remainder of the line (actual parameters) and split by commas.
            actual_params_str = line[len(first):].strip()
            if actual_params_str:
                actual_params = [p.strip() for p in actual_params_str.split(',')]
            else:
                actual_params = []
            expansion_lines = expand_macro(first, actual_params, mdt)
            for exp_line in expansion_lines:
                intermediate.append(f"{lc}\t{exp_line}")
                lc += 1
        else:
            intermediate.append(f"{lc}\t{line}")
            lc += 1
    return intermediate

def main():
    if len(sys.argv) != 2:
        print("Usage: python a5.py <sourcefile.mac>")
        sys.exit(1)
    with open(sys.argv[1]) as f:
        lines = f.readlines()

    # Pass 1: Build the MDT and get the main program lines.
    mdt, non_macro_lines = pass1(lines)
    # Pass 2: Expand macros and generate intermediate code.
    intermediate = pass2(non_macro_lines, mdt)

    print("Intermediate Code:")
    for line in intermediate:
        print(line)

if __name__ == '__main__':
    main()