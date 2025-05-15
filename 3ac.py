class ThreeAddressCodeGenerator:
    def __init__(self, temp_prefix='t'):
        self.temp_prefix = temp_prefix
        self.temp_count = 1
        self.code = []
    
    def get_temp(self):
        """Generate a new temporary variable name"""
        temp = f"{self.temp_prefix}{self.temp_count}"
        self.temp_count += 1
        return temp
    
    def reset(self, temp_prefix=None):
        """Reset the generator for a new expression"""
        if temp_prefix is not None:
            self.temp_prefix = temp_prefix
        self.temp_count = 1
        self.code = []
    
    def tokenize(self, expression):
        """Simple tokenizer for the expression"""
        tokens = []
        i = 0
        
        while i < len(expression):
            if expression[i].isalpha():
                # Extract variable name
                var = ""
                while i < len(expression) and (expression[i].isalnum() or expression[i] == '_'):
                    var += expression[i]
                    i += 1
                tokens.append(var)
            elif expression[i].isdigit():
                # Extract number
                num = ""
                while i < len(expression) and expression[i].isdigit():
                    num += expression[i]
                    i += 1
                tokens.append(num)
            elif expression[i] in "+-*/^()=":
                tokens.append(expression[i])
                i += 1
            else:
                # Skip whitespace and other characters
                i += 1
                
        return tokens
    
    def parse_expression(self, expression):
        """Parse the expression and generate three-address code"""
        # Remove spaces and split on '=' to get left and right part
        expression = expression.replace(" ", "")
        parts = expression.split("=")
        if len(parts) != 2:
            raise ValueError("Invalid expression format, must contain exactly one '='")
        
        left_side = parts[0].strip()
        right_side = parts[1].strip()
        
        # Generate code for the right side expression
        result = self.parse_subexpression(right_side)
        
        # Assign final result to the left side
        if result != left_side:  # Only add this if the result is not already the target variable
            self.code.append(f"{left_side} = {result}")
        
        return self.code
    
    def parse_subexpression(self, expr):
        """Recursively parse a subexpression"""
        # Handle parentheses first
        if '(' in expr:
            return self.handle_parentheses(expr)
        
        # Handle operators in order of precedence
        # ^ has highest precedence, then * and /, then + and -
        operators = ['^', '*/', '+-']  # Groups of operators with same precedence
        
        for op_group in operators:
            # For left-to-right associativity, scan from left
            # For right-to-left (like ^), we would scan from right
            if op_group == '^':
                # Right-to-left for exponentiation
                i = len(expr) - 1
                step = -1
            else:
                # Left-to-right for other operators
                i = 0
                step = 1
                
            while 0 <= i < len(expr):
                if expr[i] in op_group:
                    # Found an operator, split and process
                    left = expr[:i]
                    right = expr[i+1:]
                    op = expr[i]
                    
                    # Skip if left or right is empty
                    if not left or not right:
                        i += step
                        continue
                    
                    # Recursively parse left and right parts
                    left_result = self.parse_subexpression(left)
                    right_result = self.parse_subexpression(right)
                    
                    # Generate a temporary variable for this operation
                    temp = self.get_temp()
                    self.code.append(f"{temp} = {left_result} {op} {right_result}")
                    
                    return temp
                i += step
                
        # If no operators found, this is a single operand (variable or constant)
        return expr
    
    def handle_parentheses(self, expr):
        """Handle expressions with parentheses"""
        # Find matching pairs of parentheses
        if '(' not in expr:
            return self.parse_subexpression(expr)
        
        # Find the outermost matching parentheses
        level = 0
        start = -1
        
        for i, char in enumerate(expr):
            if char == '(':
                if level == 0:
                    start = i
                level += 1
            elif char == ')':
                level -= 1
                if level == 0:
                    # Found a matching pair
                    before = expr[:start]
                    inside = expr[start+1:i]
                    after = expr[i+1:]
                    
                    # Process the expression inside parentheses
                    inside_result = self.parse_subexpression(inside)
                    
                    # Create a new expression without these parentheses
                    new_expr = before + inside_result + after
                    
                    # Continue parsing
                    return self.parse_subexpression(new_expr)
        
        raise ValueError("Mismatched parentheses")
    
    def generate_code(self, expression):
        """Generate three address code for the given expression"""
        self.reset()
        return self.parse_expression(expression)


def process_expression(expression):
    """Process a single expression and return the three address code"""
    generator = ThreeAddressCodeGenerator()
    
    # Replace special dash characters with regular minus
    expression = expression.replace('–', '-')
    
    print(f"\nExpression: {expression}")
    print("Three Address Code:")
    
    try:
        code = generator.generate_code(expression)
        for line in code:
            print(line)
        return code
    except Exception as e:
        print(f"Error processing expression: {e}")
        return []

# Main program
if __name__ == "__main__":
    print("Three Address Code Generator")
    print("===========================")
    print("Enter expressions to convert to three address code.")
    print("Enter 'exit' to quit.")
    
    while True:
        expression = input("\nEnter an expression (e.g., 'w = u*u - u*v + v*v'): ")
        
        if expression.lower() == 'exit':
            break
            
        if not expression or '=' not in expression:
            print("Invalid expression. Please include an assignment (=).")
            continue
            
        process_expression(expression)
