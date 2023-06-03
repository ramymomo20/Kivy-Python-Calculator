import operator
import re
import math

class Calculator:
    def __init__(self):
        self.operators = {
            "+": operator.add,
            "-": operator.sub,
            "*": operator.mul,
            "/": operator.truediv,
            "^": operator.pow,
            "√": math.sqrt,
            "!": math.factorial,
            "unary-": operator.neg
        }
        self.precedence = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2,
            "^": 3,
            "!": 4,
            "√": 4,
            "unary-": 5
        }

    def _getPostfix(self, expr):
        stack = []
        output = []
        tokens = re.findall(r"(\b\w+[\.]?\w*\b|[\(\)\+\-\*/\^!√])", expr)
        for i, token in enumerate(tokens):
            try:
                output.append(float(token))
            except ValueError:
                if token == '(':
                    stack.append(token)
                elif token == ')':
                    while stack and stack[-1] != '(':
                        output.append(stack.pop())
                    if not stack or stack[-1] != '(':
                        return 'Error'
                    stack.pop()  # Discard the '('
                else:
                    # Handle unary minus
                    if token == '-' and (i == 0 or tokens[i-1] in self.operators or tokens[i-1] == '('):
                        stack.append('unary-')
                    else:
                        while stack and stack[-1] != '(' and self.precedence[token] <= self.precedence.get(stack[-1], 0):
                            output.append(stack.pop())
                        stack.append(token)
        while stack:
            if stack[-1] == '(':
                return 'Error'
            output.append(stack.pop())
        return output

    def calculate(self):
        if not isinstance(self.expr, str) or len(self.expr) <= 0:
            return 'Error'

        stack = []
        for token in self._getPostfix(self.expr):
            if isinstance(token, float):
                stack.append(token)
            elif token in ['!', '√', 'unary-']:
                operand = stack.pop()
                if token == '!':
                    if operand != int(operand):
                        return 'Error'
                    operand = int(operand)
                stack.append(self.operators[token](operand))
            else:
                operand1 = stack.pop()
                if stack:  # Check if there is another operand on the stack
                    operand2 = stack.pop()
                else:
                    return 'Error'
                stack.append(self.operators[token](operand2, operand1))

        ans = stack.pop()
        return int(ans) if ans - int(ans) == 0 else round(ans, 4)