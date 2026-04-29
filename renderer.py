# Takes a list of [x, y] coordinates and a grid size list in [rows, cols]. 
# Returns a 2D list of characters representing an ASCII graph
# The grid size should have an odd number of rows and columns to have a clear center point and axes

from os import get_terminal_size
from math import sin


# Default configuration for grid size is set to size of terminal, considering the nearest lowest odd number
def get_default_config() -> tuple:
    cols = get_terminal_size().columns
    rows = get_terminal_size().lines

    if cols % 2 == 0:
        cols -= 1
    if rows % 2 == 0: 
        rows -= 1
    
    return rows, cols


# Takes grid size tuple and returns a 2D list with x and y axes. By default, grid size it set to current size of terminal window.
def draw_axis(grid_size: tuple = None) -> list:
    # If grid size is not provided, use default configuration
    if grid_size is None:
        grid_size = get_default_config()
        
    # Check for odd number of rows and columns
    rows = grid_size[0]
    cols = grid_size[1]

    if rows % 2 == 0 or cols % 2 == 0:
        raise ValueError("Grid size must have an odd number of rows and columns.")

    # Create a 2D list filled with spaces
    output = [[' ' for _ in range(cols)] for _ in range(rows)]

    # Add the axes to the output
    for row in range(rows):
        output[row][cols // 2] = '|'
    for col in range(cols):
        output[rows // 2][col] = '-'

    # Add the center point
    output[rows // 2][cols // 2] = '+'

    return output


# Plot points on input graph list and return updated graph list. Points should be in format [[x1, y1], [x2, y2], ...]
def plot_points(graph: list, points: list, col_scale: float, row_scale: float) -> list:
    rows = len(graph)
    cols = len(graph[0])

    for point in points:
        # Get normal x,y values
        x = point[0]
        y = point[1]

        # Adjust to scale
        x = round(x * col_scale)
        y = round(y * row_scale)

        # Calculate the position on the graph
        row = rows // 2 - y
        col = cols // 2 + x

        # Do a bounds check
        if row < 0 or row >= rows or col < 0 or col >= cols:
            continue

        # Plot the point
        graph[row][col] = '*'

    return graph


# Add labels to positive and negative x and y axes
def add_labels(graph: list, x_units: int, y_units: int) -> list:
    # Get rows and cols of graph
    rows = len(graph)
    cols = len(graph[0])

    # x-axis label is the maximum x-axis value divided by 2, y-axis label is maximum y-axis value divided by 2. 
    # TODO: Add more labels for intermediate values
    x_axis_label = str(x_units / 2)
    y_axis_label = str(y_units / 2)

    
    # Add x-axis labels
    graph = write_string(graph, x_axis_label, rows // 2 + 1, cols - len(x_axis_label))
    graph = write_string(graph, '-' + x_axis_label, rows // 2 + 1, 0)

    # Add y-axis labels
    graph = write_string(graph, y_axis_label, 0, cols // 2 + 1)
    graph = write_string(graph, '-' + y_axis_label, rows - 1, cols // 2 + 1)

    return graph


# Helper function to write a string on the graph at a specific row and column
def write_string(graph: list, string: str, row: int, col: int) -> list:
    for i in range(len(string)):
        graph[row][col + i] = string[i]
    return graph


# Temporary test code to demonstrate functionality
if __name__ == "__main__":
    # My default values for testing purposes
    TOTAL_X_UNITS = 20
    TOTAL_Y_UNITS = 10

    # The scale is rows or cols per unit on x or y-axis respectively
    ROW_SCALE = get_default_config()[0] / TOTAL_Y_UNITS
    COL_SCALE = get_default_config()[1] / TOTAL_X_UNITS

    # The step is interval between x-axis values for calculatng y-axis values. Won't use in final version as point generation will be done in another script.
    STEP = 0.01

    # Initialize graph and points
    graph = draw_axis()
    points = []

    # Generate points from a mathematical function
    x = - TOTAL_X_UNITS / 2
    step = STEP

    while x <= TOTAL_X_UNITS / 2:
        y = sin(x)

        points.append([x, y])
        x += step

    # Plot the points and add labels to the graph
    graph = plot_points(graph, points, COL_SCALE, ROW_SCALE)
    graph = add_labels(graph, TOTAL_X_UNITS, TOTAL_Y_UNITS)

    # Print the graph to the terminal
    for row in graph:
        for char in row:
            print(char, end='')
        print()
    
    input("")