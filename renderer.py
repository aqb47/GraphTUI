# Takes a list of (x, y) coordinates and a grid size list in [rows, cols]. 
# Returns a 2D list of characters representing an ASCII graph
# The grid size should have an odd number of rows and columns to have a clear center point and axes


# Takes grid size and returns a 2D list with x and y axes
def draw_axis(grid_size: list) -> list:
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


def plot_points(graph: list, points: list) -> list:
    rows = len(graph)
    cols = len(graph[0])

    for point in points:
        x = point[0]
        y = point[1]

        # Calculate the position on the graph
        row = rows // 2 - y
        col = cols // 2 + x

        # Check if the point is within the bounds of the graph, and is an integer
        if not isinstance(x, int):
            x = round(x)
        if not isinstance(y, int):
            y = round(y)

        if row < 0 or row >= rows or col < 0 or col >= cols:
            continue

        # Plot the point
        graph[row][col] = '*'

    return graph


# Temporary test code
if __name__ == "__main__":
    graph = draw_axis([29, 119])

    points = []

    for i in range(-60, 61):
        points.append([i, i**3])  

    graph = plot_points(graph, points)

    for row in graph:
        for char in row:
            print(char, end='')
        print()
    
    input("")