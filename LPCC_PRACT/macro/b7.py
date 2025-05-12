import sys

def generate_mnt(lines):
    mnt = []
    macro_index = 1
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        tokens = line.split()
        if tokens[0].upper() == "MACRO":
            header_parts = line.split(None, 2)
            macro_name = header_parts[1]
            if len(header_parts) > 2:
                params = [p.strip() for p in header_parts[2].split(',')]
            else:
                params = []
            mnt.append((macro_name, len(params), macro_index))
            macro_index += 1
            while i < len(lines) and lines[i].strip().upper() != "MEND":
                i += 1
        i += 1
    return mnt

def main():
    if len(sys.argv) != 2:
        print("Usage: python mnt.py <sourcefile.mac>")
        sys.exit(1)
    with open(sys.argv[1]) as f:
        lines = f.readlines()
    mnt = generate_mnt(lines)
    print("Macro Name Table (MNT):")
    print("Macro Name\tParam Count\tMacro Index")
    print("---------------------------------------------")
    for name, param_count, index in mnt:
        print(f"{name}\t\t{param_count}\t\t{index}")

if __name__ == '__main__':
    main()