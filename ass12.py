class ThreeAddressCodeGenerator:
    def __init__(self, expr):
        self.expr = expr.replace(" ", "")
        self.index = 0
        self.temp_count = 1
        self.code = []
        self.assignment_lhs = None

    def new_temp(self):
        temp = f't{self.temp_count}'
        self.temp_count += 1
        return temp

    def peek(self):
        return self.expr[self.index] if self.index < len(self.expr) else None

    def get(self):
        char = self.peek()
        self.index += 1
        return char

    def parse(self):
        # Handle assignment like x = ...
        if '=' in self.expr:
            parts = self.expr.split('=', 1)
            self.assignment_lhs = parts[0]
            self.expr = parts[1]
            self.index = 0
        result = self.expression()
        if self.assignment_lhs:
            self.code.append(f"{self.assignment_lhs} = {result}")
        return self.code

    def expression(self):
        left = self.term()
        while self.peek() in ('+', '-'):
            op = self.get()
            right = self.term()
            temp = self.new_temp()
            self.code.append(f"{temp} = {left} {op} {right}")
            left = temp
        return left

    def term(self):
        left = self.power()
        while self.peek() in ('*', '/'):
            op = self.get()
            right = self.power()
            temp = self.new_temp()
            self.code.append(f"{temp} = {left} {op} {right}")
            left = temp
        return left

    def power(self):
        left = self.factor()
        while self.peek() == '^':
            op = self.get()
            right = self.power()  # right-associative
            temp = self.new_temp()
            self.code.append(f"{temp} = {left} {op} {right}")
            left = temp
        return left

    def factor(self):
        if self.peek() == '(':
            self.get()  # consume '('
            val = self.expression()
            self.get()  # consume ')'
            return val
        else:
            val = ''
            while self.peek() and (self.peek().isalnum()):
                val += self.get()
            return val

    def generate(self):
        self.parse()
        return self.code


# Example usage
if __name__ == "__main__":
    expr = input("Enter an expression (e.g., x = a + b * (c - d) ^ e): ")
    tac = ThreeAddressCodeGenerator(expr)
    code = tac.generate()
    print("\nThree Address Code:")
    for line in code:
        print(line)
