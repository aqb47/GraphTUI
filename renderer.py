# Takes a list of [x, y] coordinates and a grid size list in [rows, cols]. 
# Returns a 2D list of characters representing an ASCII graph
# The grid size should have an odd number of rows and columns to have a clear center point and axes

from os import get_terminal_size


# Default configuration for grid size is set to size of terminal, considering the nearest lowest odd number
def get_default_config() -> tuple:
    cols: int = get_terminal_size().columns
    rows: int = get_terminal_size().lines

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
    rows: int = grid_size[0]
    cols: int = grid_size[1]

    if rows % 2 == 0 or cols % 2 == 0:
        raise ValueError("Grid size must have an odd number of rows and columns.")

    # Create a 2D list filled with spaces
    output: list[list] = [[' ' for _ in range(cols)] for _ in range(rows)]

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
    rows: int = len(graph)
    cols: int = len(graph[0])

    for point in points:
        # Get normal x,y values
        x: float = point[0]
        y: float = point[1]

        # Adjust to scale
        x = round(x * col_scale)
        y = round(y * row_scale)

        # Calculate the position on the graph
        row: int = rows // 2 - y
        col: int = cols // 2 + x

        # Do a bounds check
        if row < 0 or row >= rows or col < 0 or col >= cols:
            continue

        # Plot the point
        graph[row][col] = '.'

    return graph


# Add labels to positive and negative x and y axes
def add_labels(graph: list, x_units: int, y_units: int) -> list:
    # Get rows and cols of graph
    rows: int = len(graph)
    cols: int = len(graph[0])

    # x-axis label is the maximum x-axis value divided by 2, y-axis label is maximum y-axis value divided by 2. 
    # TODO: Add more labels for intermediate values
    x_axis_label: str = str(x_units / 2)
    y_axis_label: str = str(y_units / 2)

    
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
        # Do a bounds check
        if col + i > len(graph[0]) - 1 or row > len(graph) - 1:
            break
        
        # Write the character to the graph
        graph[row][col + i] = string[i]
    return graph
