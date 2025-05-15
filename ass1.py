class Symbol:
    def __init__(self, symbol, address):
        self.symbol = symbol
        self.address = address

# Helper function to check if symbol already exists
def symbol_exists(table, label):
    return any(sym.symbol == label for sym in table)

def main():
    code = []
    symbol_table = []

    print("Enter Assembly code (type 'END' to finish input):")

    # Read input lines
    while True:
        line = input().strip()
        if line.upper() == 'END':
            break
        if line:
            code.append(line)
    code.append("END")  # Ensure END is processed

    location_counter = 0
    start_found = False

    print("\n--- PASS 1: Generating Symbol Table ---")

    for stmt in code:
        tokens = stmt.split()

        if tokens[0].upper() == "START":
            location_counter = int(tokens[1])
            start_found = True
            continue

        if not start_found:
            print("Error: START directive not found.")
            return

        label = None
        opcode = ""
        operand = ""

        opcodes = ["READ", "MOVER", "COMP", "BC", "SUB", "STOP", "DS", "END"]

        if tokens[0].upper() not in opcodes:
            label = tokens[0]
            if len(tokens) > 1:
                opcode = tokens[1].upper()
            if len(tokens) > 2:
                operand = tokens[2]
        else:
            opcode = tokens[0].upper()
            if len(tokens) > 1:
                operand = tokens[1]

        if opcode == "DS":
            if label and not symbol_exists(symbol_table, label):
                symbol_table.append(Symbol(label, location_counter))
            location_counter += 1  # assuming DS 1
            continue

        if label and not symbol_exists(symbol_table, label):
            symbol_table.append(Symbol(label, location_counter))

        location_counter += 1

    print("\n--- SYMBOL TABLE ---")
    print(f"{'Symbol':<10} {'Address':<10}")
    for sym in symbol_table:
        print(f"{sym.symbol:<10} {sym.address:<10}")

if __name__ == "__main__":
    main()
