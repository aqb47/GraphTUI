from sympy import sympify, symbols, lambdify
from sympy.parsing.sympy_parser import parse_expr

x = symbols('x')
expr = parse_expr('sin(x)')   # safe parsing
f = lambdify(x, expr, 'math')        # converts to a fast callable
print(f(1))                        # use like a normal function