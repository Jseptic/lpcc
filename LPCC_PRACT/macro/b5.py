import sys

def pass1(lines):
    mdt = {}
    non_macro_lines = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        tokens = line.split()
        if tokens[0].upper() == "MACRO":
            header_parts = line.split(None, 2)
            if len(header_parts) < 2:
                print("Error: Macro header missing macro name")
                sys.exit(1)
            macro_name = header_parts[1]
            if len(header_parts) > 2:
                formal_params = [p.strip() for p in header_parts[2].split(',')]
            else:
                formal_params = []
            i += 1
            body = []
            while i < len(lines):
                body_line = lines[i].strip()
                if body_line.upper() == "MEND":
                    break
                body.append(body_line)
                i += 1
            mdt[macro_name] = (formal_params, body)
            i += 1
        else:
            non_macro_lines.append(line)
            i += 1
    return mdt, non_macro_lines

def expand_macro(macro_name, actual_params, mdt):
    formal_params, body = mdt[macro_name]
    sub_dict = {}
    for idx, param in enumerate(formal_params):
        if idx < len(actual_params):
            sub_dict[param] = actual_params[idx]
        else:
            sub_dict[param] = ""
    expanded_lines = []
    for line in body:
        tokens = line.split()
        new_tokens = []
        for token in tokens:
            if token in sub_dict:
                new_tokens.append(sub_dict[token])
            else:
                new_tokens.append(token)
        expanded_lines.append(" ".join(new_tokens))
    return expanded_lines

def pass2(non_macro_lines, mdt):
    lc = 1
    intermediate = []
    for line in non_macro_lines:
        tokens = line.split()
        if not tokens:
            continue
        first = tokens[0]
        if first in mdt:
            actual_params_str = line[len(first):].strip()
            if actual_params_str:
                actual_params = [a.strip() for a in actual_params_str.split(',')]
            else:
                actual_params = []
            expansion = expand_macro(first, actual_params, mdt)
            for exp_line in expansion:
                intermediate.append(f"{lc}\t{exp_line}")
                lc += 1
        else:
            intermediate.append(f"{lc}\t{line}")
            lc += 1
    return intermediate

def main():
    if len(sys.argv) != 2:
        print("Usage: python b5.py <sourcefile.mac>")
        sys.exit(1)
    with open(sys.argv[1]) as f:
        lines = f.readlines()
    mdt, non_macro_lines = pass1(lines)
    intermediate = pass2(non_macro_lines, mdt)
    print("Intermediate Code:")
    for line in intermediate:
        print(line)

if __name__ == '__main__':
    main()