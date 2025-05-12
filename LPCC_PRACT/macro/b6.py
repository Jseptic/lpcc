import sys

def generate_mdt(lines):
    mdt = {}
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        tokens = line.split()
        if tokens[0].upper() == "MACRO":
            header_parts = line.split(None, 2)  # Split into: MACRO, macro_name, [parameters]
            macro_name = header_parts[1]
            if len(header_parts) > 2:
                formal_params = [param.strip() for param in header_parts[2].split(',')]
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
    return mdt

def main():
    if len(sys.argv) != 2:
        print("Usage: python a6.py <sourcefile.mac>")
        sys.exit(1)
        
    with open(sys.argv[1]) as f:
        lines = f.readlines()
    
    mdt = generate_mdt(lines)
    
    print("Macro Definition Table (MDT):")
    print("Macro Name\tFormal Parameters\tMacro Body")
    print("----------------------------------------------------------")
    for macro, (params, body) in mdt.items():
        print(f"{macro}\t{params}")
        for b in body:
            print(f"\t{b}")
        print("----------------------------------------------------------")

if __name__ == '__main__':
    main()