class Symbol:
    def __init__(self, symbol, address=None):
        self.symbol = symbol
        self.address = address

class Literal:
    def __init__(self, literal, address=None):
        self.literal = literal
        self.address = address

OPCODES = {
    "STOP": ("IS", "00"),
    "ADD": ("IS", "01"),
    "SUB": ("IS", "02"),
    "MULT": ("IS", "03"),
    "MOVER": ("IS", "04"),
    "MOVEM": ("IS", "05"),
    "COMP": ("IS", "06"),
    "BC": ("IS", "07"),
    "DIV": ("IS", "08"),
    "READ": ("IS", "09"),
    "PRINT": ("IS", "10"),
    "START": ("AD", "01"),
    "END": ("AD", "02"),
    "ORIGIN": ("AD", "03"),
    "EQU": ("AD", "04"),
    "LTORG": ("AD", "05"),
    "DS": ("DL", "01"),
    "DC": ("DL", "02")
}

REGISTERS = {
    "AREG": "01",
    "BREG": "02",
    "CREG": "03",
    "DREG": "04"
}

def get_symbol_index(symbol_table, symbol):
    for i, sym in enumerate(symbol_table):
        if sym.symbol == symbol:
            return i
    return -1

def get_literal_index(literal_table, literal):
    for i, lit in enumerate(literal_table):
        if lit.literal == literal:
            return i
    return -1

def clean_operand(operand):
    return operand.strip(",").strip("’'")

def main():
    code = []
    symbol_table = []
    literal_table = []
    pool_table = [0]
    literal_pool = []
    intermediate_code = []

    location_counter = 0
    print("Enter Assembly code (type 'END' to finish input):")

    while True:
        line = input().strip()
        if line.upper() == "END":
            code.append("END")
            break
        if line:
            code.append(line)

    for stmt in code:
        tokens = stmt.strip().split()
        if not tokens:
            continue

        label, opcode, operands = None, None, []

        # Detect opcode position
        if tokens[0].upper() in OPCODES:
            opcode = tokens[0].upper()
            operands = tokens[1:]
        elif len(tokens) >= 2 and tokens[1].upper() in OPCODES:
            label = tokens[0]
            opcode = tokens[1].upper()
            operands = tokens[2:]
        else:
            print(f"Error parsing line: {stmt}")
            continue

        # Clean operands
        operands = [clean_operand(op) for op in operands]

        # Handle START opcode
        if opcode == "START":
            location_counter = int(operands[0])
            intermediate_code.append(f"(AD,01) (C,{operands[0]})")
            continue

        # Handle label (avoid adding register names)
        if label and label not in REGISTERS:
            if get_symbol_index(symbol_table, label) == -1:
                symbol_table.append(Symbol(label, location_counter))

        # Handle LTORG and END opcodes
        if opcode in ["LTORG", "END"]:
            for lit in literal_pool:
                lit.address = location_counter
                literal_table.append(lit)
                location_counter += 1
            literal_pool.clear()

            if opcode == "LTORG":
                pool_table.append(len(literal_table))

            intermediate_code.append(f"(AD,{OPCODES[opcode][1]})")
            continue

        # Handle DS and DC (Data Definition) opcodes
        if opcode in ["DS", "DC"]:
            value = int(operands[0])
            if get_symbol_index(symbol_table, label) == -1:
                symbol_table.append(Symbol(label, location_counter))
            else:
                symbol_table[get_symbol_index(symbol_table, label)].address = location_counter

            ic = f"(DL,{OPCODES[opcode][1]}) (C,{value})"
            intermediate_code.append(ic)
            location_counter += value if opcode == "DS" else 1
            continue

        # Process IS (Instruction Statements)
        ic = f"(IS,{OPCODES[opcode][1]})"
        operand = None

        if operands:
            if operands[0] in REGISTERS:
                ic += f" ({REGISTERS[operands[0]]})"
                operand = operands[1] if len(operands) > 1 else None
            else:
                operand = operands[0]

        if operand:
            if operand.startswith("="):
                if get_literal_index(literal_table + literal_pool, operand) == -1:
                    literal_pool.append(Literal(operand))
                idx = get_literal_index(literal_table + literal_pool, operand)
                ic += f" (L,{idx})"
            else:
                if get_symbol_index(symbol_table, operand) == -1 and operand not in REGISTERS:
                    symbol_table.append(Symbol(operand))
                idx = get_symbol_index(symbol_table, operand)
                ic += f" (S,{idx})"

        intermediate_code.append(ic)
        location_counter += 1

    # Output Tables
    print("\n--- INTERMEDIATE CODE ---")
    for line in intermediate_code:
        print(line)

    # print("\n--- SYMBOL TABLE ---")
    # print(f"{'Index':<10}{'Symbol':<10}{'Address':<10}")
    # for i, sym in enumerate(symbol_table):
    #     print(f"{i:<10}{sym.symbol:<10}{sym.address if sym.address is not None else '-':<10}")

    # print("\n--- LITERAL TABLE ---")
    # print(f"{'Index':<10}{'Literal':<10}{'Address':<10}")
    # for i, lit in enumerate(literal_table):
    #     print(f"{i:<10}{lit.literal:<10}{lit.address if lit.address is not None else '-':<10}")

    # print("\n--- POOL TABLE ---")
    # print(f"{'Pool #':<10}{'Start Index':<15}")
    # for i, idx in enumerate(pool_table):
    #     print(f"{i + 1:<10}{idx:<15}")

if __name__ == "__main__":
    main()
