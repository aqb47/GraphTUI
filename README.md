# GraphTUI
An ASCII-styled graphing calculator that runs in your terminal. 

### The Concept
I really like generating graphs and visualisations using matplotlib, and I absolutely love making ASCII art. So, I wanted to combine these two things and make a project in Python where you could generate simple graphs of mathematical functions in a copy-pastable format. 

You definitely won't get the clearest graphs in the world with my project but I aimed to make it a tool which can be used to quickly and roughly visualize simple functions while having easy control on the scale and step of the graph generation.

### My Implementation Details
#### The UI
I knew I wanted to make this in Python, and with the use of ASCII graphs clearly depending on monospace fonts (like consolas) I thought it would be good to have it run in the terminal using a TUI (Terminal User Interface) with a basic menu and input handling. 

I contemplated between using the windows-curses and Textual packages for making this project, but ended up using Textual due to it's incredible simplicity yet powerful features. Seriously, this module was so fun to use, it's like writing simple HTML and CSS in your terminal, all the while getting an amazing looking UI with minimal effort. It's very beginner-friendly too and I would highly recommend for someone to pick it up. Textual mainly works with classes so this project was a good way to get started with Object Oriented Programming for me. 

#### Graph Rendering
Having decided on the UI with Textual, I started building the main graph rendering logic in renderer.py. Depending on the current screen size of the terminal, the program just generates a 2D list, draws the axes, plots the points (which depends on the total x, y axes values) and adds labels on the axes.  

#### Point Generation
The point generation before plotting is done in math_engine.py. Specifically, I decided on using the sympy module for parsing a function string. Deciding on how to parse user input was a headache, I couldn't use the built in eval() due to it's vulnerabilities so I used the parse_expr() function in sympy with sanitized user input. For this I had to use some regular expressions and limit some functions and constants.

After getting the function though the point generation is pretty simple. Based on the step value (interval between points x values) the program generates a list of points. I made sure to use lambdify() with a math module backend to get quicker point generation beforehand.

#### Tying It Together
The Textual App uses a graph generation screen to get the total x-axis, y-axis values along with the function string and step value input from the user. Based on that information using the math engine and renderer you get a finished graph, free to be copied and resized as one wishes. 

I made sure to put in a few other screens - a help screen for general instructions and an error screen in case something goes wrong. With the help of Textual and it's event handlers, resizing the terminal window automatically regenerates the graph. And with some debouncing to smooth everything out I managed to implement a basic version of my intial idea.

### How To Use
Clone the repository and run 'app.py'. Make sure you have the sympy and Textual modules installed along with Python.

### Issues
- Certain functions don't generate due to an overflow error (e.g x^x^x). This problem can get amplified with a huge x-axis range and small step sizes. 

- One of the biggest gripes I have is that you can't generate a whole circle, just half of it. 
This is because when we write y (/f(x)) = sqrt(16 - x**2) for example, the sqrt() function returns only the principal (non-negative) square root. This should be a simple fix, but I'd have to write my own square root function and change the expression parsing logic for it to work.

### What I Learnt
- OOP with Textual

- Using 2D lists in Python 

- Validation and parsing of user input

- Use of math-based libraries like Sympy for symbolic expressions

- Some UI design with .tcss files

- Event handling

- Actually reading documentation

### What I Want to Add
- Abillity to plot two or more functions at once

- Riemann-sum integration

- Tangents at specified points

- A fixed sqrt() function

