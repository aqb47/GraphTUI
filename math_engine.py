# Takes a function string and a range (although for now it is fixed to -10 to 10)
# Returns a list of [x, y] points that can be plotted on the graph

import re

from sympy import Expr, symbols, lambdify, im
from sympy.parsing.sympy_parser import parse_expr

from renderer import draw_axis, get_default_config, plot_points, add_labels

ALLOWED_SYMBOLS: re.Pattern = re.compile(r'^[0-9x\s\+\-\*\/\^\(\)\.\,a-z]+$')
ALLOWED_FUNCTIONS: list[str] = ['sin()', 'cos()', 'tan()', 'log()', 'sqrt()', 'exp()', 'abs()']
ALLOWED_CONSTANTS: list[str] = ['pi', 'E']


# Sanitize and validate user function
def validate_function(function: str) -> bool:
    # Check if only allowed characters are used
    if not ALLOWED_SYMBOLS.match(function.strip().lower()):
        return False

    # Get alphabet characters (except x) and parentheses from function to check for used functions
    used_functions: str = "".join([char for char in function if char.isalpha() or char == '(' or char == ')']).replace('x', '')

    # Replace constants for function checking
    for allowed_constant in ALLOWED_CONSTANTS:
        used_functions = used_functions.replace(allowed_constant, '')

    # Check if only allowed functions are used
    if used_functions:
        for allowed_function in ALLOWED_FUNCTIONS:
            if allowed_function in used_functions:
                break
        else:
            return False
    
    return True


# Return a callable function from user input string
def get_function() -> callable:
    # Initially input function
    function: str = input("Enter a function of x [e.g. sin(x), x**2, log(x)]: ")

    # Sympy recognizes Euler's number as E
    function = re.sub(r'\be\b', 'E', function)

    # Validate function and raise error if invalid
    is_valid: bool = validate_function(function)
    if not is_valid:
        raise ValueError("Invalid function.")

    # Parse function and convert to callable
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
            if im(y) != 0:
                x += step
                continue
                
            points.append([x, y])
        
        # Handle math errors
        except (ZeroDivisionError, ValueError):
            pass

        # Increment by step size
        x += step

    return points


# Temporary test code to demonstrate functionality
if __name__ == "__main__":
    # My default values for testing purposes
    TOTAL_X_UNITS: int = 12
    TOTAL_Y_UNITS: int = 10

    # The step is interval between x-axis values for calculating y-axis values. 
    STEP: float = 0.05

    # Generate points from a mathematical function
    function: callable = get_function()
    points: list[list[float]] = generate_points(function, - TOTAL_X_UNITS / 2, TOTAL_X_UNITS / 2, STEP)

    # The scale is rows or cols per unit on x or y-axis respectively
    ROW_SCALE: float = get_default_config()[0] / TOTAL_Y_UNITS
    COL_SCALE: float = get_default_config()[1] / TOTAL_X_UNITS

    # Initialize graph 
    graph: list = draw_axis()

    # Plot the points and add labels to the graph
    graph = plot_points(graph, points, COL_SCALE, ROW_SCALE)
    graph = add_labels(graph, TOTAL_X_UNITS, TOTAL_Y_UNITS)

    # Print the graph to the terminal
    for row in graph:
        for char in row:
            print(char, end='')
        print()
    
    input("")
    