import functools,sys

#*-------------------------------------------------------------------------------------------------
class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return not self.items

    def __len__(self):
        return len(self.items)

    def push(self, value):
        self.items.append(value)

    def pop(self):
        return None if self.isEmpty() else self.items.pop()

    def peek(self):
        return None if self.isEmpty() else self.items[-1]
#*-------------------------------------------------------------------------------------------------

class Calculator:
    def __init__(self, expr=None):
        self.expr = expr
        self.operators = {
            "+": lambda x,y : x + y,
            "-": lambda x,y : x - y,
            "*": lambda x,y : x * y,
            "/": lambda x,y : x / y,
            "^": lambda x,y : x ** y,
            "√": lambda x: x ** 0.5,
            "!": self.factorial
        }

    def precedence(self, operator):
        operator_list = ['+', '-', '*', '/', '^', '!', '√']
        return 1 if operator in operator_list[:1] else 2 if operator in operator_list[2:4] else 3 if operator == operator_list[4] else 4 if operator == operator_list[5] else 5 if operator == operator_list[6] else 0

    def isBalanced(self, expr):
        equation = Stack()
        i = 0
        while i < len(expr):
            if expr[i] == '(':
                equation.push(expr[i])
            elif expr[i] == ')':
                if not equation.isEmpty():
                    equation.pop()
                else:
                    return False
            i += 1
        return equation.isEmpty()

    def _isNumber(self, expr):
        try:
            float(expr)
            return True
        except ValueError:
            return False

    def addSpaces(self, expr):
        expr = expr.replace(" ", "")
        import re
        split_expression = re.findall(r'\s*[\d.]+\s*|\s*\D\s*', expr)
        i = 0
        
        while i < len(split_expression):
            # If the current token is '-' and the previous token is not a digit, combine the '-' with the next token
            if split_expression[i] == '-' and (i == 0 or not split_expression[i-1].isdigit()):
                split_expression[i] += split_expression[i+1]
                del split_expression[i+1]
            if split_expression[i] == '√':
                if i - 1 >= 0:
                    if split_expression[i-1].isdigit():
                        return "Error"
                # Check if the expression is of the form "√number"
                if i == 0 or not split_expression[i-1].isdigit():
                    if i+1 < len(split_expression) and split_expression[i+1].isdigit():
                        i += 1
                    else:
                        return "Error"
                # Check if the expression is of the form "number√"
                if len(split_expression) < 3 and (split_expression[i-1].isdigit()):
                    return "Error"
                else:
                    i += 1
            else:
                i += 1
        x = ' '.join(split_expression)
        return x

    def _getPostfix(self, expr):
        expr = self.addSpaces(expr)
        equation = Stack()
        output = []
        
        for item in expr.split():
            if self._isNumber(item):
                output.append(item)              
            elif item == '(':
                equation.push(item)
            elif item == ')':
                while equation and equation.peek() != '(':
                    output.append(equation.pop())
                equation.pop()
            elif item == '!':
                output.append(item)
            else:
                while not equation.isEmpty() and equation.peek() != '(' and self.precedence(item) <= self.precedence(equation.peek()):
                    output.append(equation.pop())
                equation.push(item)
        while not equation.isEmpty():
            output.append(equation.pop())
            
        return ' '.join(output)

    @property
    def calculate(self):
        if not isinstance(self.expr,str) or len(self.expr) <= 0:
            print("Argument error in calculate")
            return None
        
        stack = Stack()
        
        for item in self._getPostfix(self.expr).split():
            if self._isNumber(item):
                stack.push(float(item))
            else:
                if item == '!':
                    x = stack.pop()
                    stack.push(self.factorial(x))
                elif item == '√':
                    x = stack.pop()
                    stack.push(self.operators[item](x))
                else:
                    operand1 = stack.pop()
                    operand2 = stack.pop()
                    if operand1 is not None:
                        if item == "/":
                            if operand2 == 0:
                                return "Zero Division Error"
                    stack.push(self.operators[item](operand2, operand1))
                    
        return stack.pop()
    
    @functools.lru_cache(maxsize=None)
    def factorial(self, operand):
        if operand == 1:
            return 1
        return operand * self.factorial(operand - 1)