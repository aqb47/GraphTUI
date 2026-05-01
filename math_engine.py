# Takes a function string and a range 
# Returns a list of [x, y] points that can be plotted on the graph

import re

from sympy import Expr, symbols, lambdify
from sympy.parsing.sympy_parser import parse_expr

ALLOWED_SYMBOLS: re.Pattern = re.compile(r'^[0-9x\s\+\-\*\/\^\(\)\.\,a-z]+$')
ALLOWED_FUNCTIONS: list[str] = ['sin', 'cos', 'tan', 'log', 'sqrt', 'exp', 'abs']
ALLOWED_CONSTANTS: list[str] = ['pi', 'E']


# Sanitize and validate user function, raise an error if invalid
def validate_function(function: str) -> None:
    # Check if only allowed characters are used
    if not ALLOWED_SYMBOLS.match(function.strip().lower()):
        raise ValueError("Invalid characters in function.")

    # Check if only allowed functions, constants and variables are used
    tokens = re.findall(r'[a-zA-Z]+', function)

    if not all(token in set(ALLOWED_FUNCTIONS + ALLOWED_CONSTANTS + ['x']) for token in tokens):
        raise ValueError("Invalid functions, constants or variables used in function.")

    return


# Parse function string and return a callable function
def parse_function(function: str) -> callable:
    x: symbols = symbols('x')
    expr: Expr = parse_expr(function)
    output_function: callable = lambdify(x, expr, 'math')
    
    return output_function


# Generate points from function for a given range and step size
def generate_points(function: callable, x_min: float, x_max: float, step: float) -> list[list[float]]:
    points: list[list[float, float]] = []
    x: float = x_min
    
    # Within range 
    while x <= x_max:
        try:
            # Calculate y value
            y: float = function(x)

            # If y is complex
            if isinstance(y, complex):
                x += step
                continue
                
            # Add to list
            points.append([x, y])
        
        # Handle math errors
        except (ZeroDivisionError, ValueError):
            pass

        # Increment by step size
        x += step

    return points