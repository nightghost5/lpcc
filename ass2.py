class Literal:
    def __init__(self, literal, address=None):
        self.literal = literal
        self.address = address

def main():
    code = []
    literal_table = []
    literal_pool = []
    location_counter = 0
    start_found = False

    print("Enter Assembly code (type 'END' to finish input):")

    while True:
        line = input().strip()
        if line.upper() == "END":
            break
        if line:
            code.append(line)
    code.append("END")

    print("\n--- PASS 1: Literal Table Generation ---")

    for stmt in code:
        tokens = stmt.split()

        if tokens[0].upper() == "START":
            location_counter = int(tokens[1])
            start_found = True
            continue

        if not start_found:
            print("Error: START directive not found.")
            return

        # Check for LTORG directive – assign addresses to literals in pool
        if tokens[0].upper() == "LTORG" or tokens[0].upper() == "END":
            for lit in literal_pool:
                lit.address = location_counter
                literal_table.append(lit)
                location_counter += 1
            literal_pool.clear()
            if tokens[0].upper() == "END":
                break
            continue

        # Scan for literals in operands
        for token in tokens:
            if token.startswith("=") and all(l.literal != token for l in literal_pool + literal_table):
                literal_pool.append(Literal(token))

        location_counter += 1

    # Print the Literal Table
    print("\n--- LITERAL TABLE ---")
    print(f"{'Index':<10}{'Literal':<10}{'Address':<10}")
    for index, lit in enumerate(literal_table):
        print(f"{index:<10}{lit.literal:<10}{lit.address:<10}")

if __name__ == "__main__":
    main()
