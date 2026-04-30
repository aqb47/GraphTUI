# Takes a function string and a range 
# Returns a list of [x, y] points that can be plotted on the graph

import re

from sympy import Expr, symbols, lambdify, im
from sympy.parsing.sympy_parser import parse_expr

from renderer import draw_axis, get_default_config, plot_points, add_labels

ALLOWED_SYMBOLS: re.Pattern = re.compile(r'^[0-9x\s\+\-\*\/\^\(\)\.\,a-z]+$')
ALLOWED_FUNCTIONS: list[str] = ['sin', 'cos', 'tan', 'log', 'sqrt', 'exp', 'abs']
ALLOWED_CONSTANTS: list[str] = ['pi', 'E']


# Sanitize and validate user function, raise an error if invalid
def validate_function(function: str) -> None:
    is_valid: bool = True

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


# Return a callable function from user input string
def get_function() -> callable:
    # Initially input function. Won't be used in final version when textual is used for input
    function: str = input("Enter a function of x [e.g. sin(x), x**2, log(x)]: ")

    # Sympy recognizes Euler's number as E
    function = re.sub(r'\be\b', 'E', function)

    # Validate function 
    validate_function(function)

    # Parse function and convert to callable
    return parse_function(function)


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
                
            # Add to list
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
    