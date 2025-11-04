def find_y_intercept(expression):
    """Find the Y-intercept of a function by evaluating f(0)"""
    try:
        x = 0
        # Use our existing expression evaluation logic
        tokens = tokenize(expression)
        rpn = to_rpn(tokens)
        y = evaluate_rpn(rpn, x)
        return (0, y)  # Return as coordinate pair
    except:
        return None


def estimate_memory_usage(expression, start=-10, end=10, step=0.1, memory_limit=200000):
    """Estimate memory usage for parsing/evaluating the expression on TI-84.

    This is a conservative, platform-friendly estimator (does not use sys.getsizeof)
    because the TI-84 Python environment does not expose full memory introspection.

    Assumptions (configurable):
    - average token size: ~16 bytes
    - average RPN token size: ~12 bytes
    - stack depth small (<= 16) -> ~16 * 8 bytes
    - evaluation will allocate per-step transient values; we estimate one float per step
    - memory_limit default: 200000 bytes (≈200 KB) as a safe TI-84 CE budget

    Returns (fits, estimated_bytes)
    """
    # Basic tokenization cost estimate
    tokens = tokenize(expression)
    num_tokens = len(tokens)
    est_tokens_bytes = num_tokens * 16

    # RPN cost estimate
    rpn = to_rpn(tokens)
    num_rpn = len(rpn)
    est_rpn_bytes = num_rpn * 12

    # Per-step transient floats (we estimate one float per step stored temporarily)
    steps = max(1, int(((end - start) / step) + 0.5))
    est_per_step = steps * 8  # 8 bytes per float (conservative)

    # Stack & overhead estimate (small)
    est_stack = 16 * 8

    estimated = est_tokens_bytes + est_rpn_bytes + est_per_step + est_stack

    fits = estimated <= memory_limit
    return fits, int(estimated)

def tokenize(expression):
    tokens = []
    i = 0
    while i < len(expression):
        char = expression[i]
        
        # Handle numbers (including decimals)
        if char.isdigit() or char == '.':
            num = char
            i += 1
            while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                num += expression[i]
                i += 1
            tokens.append(num)
            continue
            
        # Handle operators and parentheses
        elif char in '+-*/^()':
            if char == '-' and (i == 0 or expression[i-1] in '(+-*/^'):
                # Handle unary minus
                num = char
                i += 1
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    num += expression[i]
                    i += 1
                tokens.append(num)
                continue
            tokens.append(char)
            i += 1
            continue
            
        # Handle variables and functions
        elif char.isalpha():
            func = char
            i += 1
            while i < len(expression) and expression[i].isalpha():
                func += expression[i]
                i += 1
            tokens.append(func)
            continue
            
        # Skip spaces
        elif char.isspace():
            i += 1
            continue
            
        else:
            raise ValueError(f"Invalid character: {char}")
    
    return tokens

def to_rpn(tokens):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    output = []
    operators = []
    
    for token in tokens:
        if token.replace('.','',1).replace('-','',1).isdigit():
            output.append(token)
        elif token == 'x':
            output.append(token)
        elif token in '+-*/^':
            while (operators and operators[-1] != '(' and 
                   precedence.get(operators[-1], 0) >= precedence.get(token, 0)):
                output.append(operators.pop())
            operators.append(token)
        elif token == '(':
            operators.append(token)
        elif token == ')':
            while operators and operators[-1] != '(':
                output.append(operators.pop())
            if operators and operators[-1] == '(':
                operators.pop()
        elif token in ['sin', 'cos', 'tan']:
            operators.append(token)
    
    while operators:
        output.append(operators.pop())
    
    return output

def evaluate_rpn(rpn, x):
    from math import sin, cos, tan
    stack = []
    
    for token in rpn:
        if token.replace('.','',1).replace('-','',1).isdigit():
            stack.append(float(token))
        elif token == 'x':
            stack.append(x)
        elif token in '+-*/^':
            b = stack.pop()
            a = stack.pop()
            if token == '+': stack.append(a + b)
            elif token == '-': stack.append(a - b)
            elif token == '*': stack.append(a * b)
            elif token == '/': stack.append(a / b)
            elif token == '^': stack.append(a ** b)
        elif token in ['sin', 'cos', 'tan']:
            a = stack.pop()
            if token == 'sin': stack.append(sin(a))
            elif token == 'cos': stack.append(cos(a))
            elif token == 'tan': stack.append(tan(a))
    
    return stack[0]

def find_extrema(expression, start=-10, end=10, step=0.1):
    """Find local extrema (minima and maxima) in the given interval"""
    x = start
    last_y = None
    increasing = None
    extrema = []
    
    while x <= end:
        try:
            tokens = tokenize(expression)
            rpn = to_rpn(tokens)
            y = evaluate_rpn(rpn, x)
            
            if last_y is not None:
                current_increasing = y > last_y
                
                if increasing is not None and increasing != current_increasing:
                    # We found an extremum
                    extrema.append((x - step, last_y, "Maximum" if increasing else "Minimum"))
                
                increasing = current_increasing
            
            last_y = y
            x += step
            
        except:
            x += step
            continue
    
    return extrema

def analyze_function(expression):
    """Analyze a function completely - find Y-intercept, extrema, and intervals"""
    print(f"\nAnalyzing function: {expression}")

    # Memory safety check for TI-84 style environments
    fits, est = estimate_memory_usage(expression)
    if not fits:
        print("\nWARNING: Estimated memory usage may exceed TI-84 limits.")
        print(f"Estimated memory: {est} bytes (limit default 200000).")
        print("Reduce interval range or increase step size to lower memory usage, or run on a desktop Python.")
        return
    
    # Find Y-intercept
    y_int = find_y_intercept(expression)
    if y_int:
        print(f"Y-intercept: (0, {y_int[1]})")
    else:
        print("Could not determine Y-intercept")
    
    # Find extrema
    extrema = find_extrema(expression)
    if extrema:
        print("\nLocal Extrema:")
        for x, y, type_ in extrema:
            print(f"{type_} at ({x:.2f}, {y:.2f})")
    else:
        print("\nNo local extrema found in the given interval")
    
    # Determine intervals of increase/decrease
    if extrema:
        print("\nIntervals:")
        x_points = [-10] + [x for x, _, _ in extrema] + [10]
        for i in range(len(x_points) - 1):
            mid_x = (x_points[i] + x_points[i + 1]) / 2
            tokens = tokenize(expression)
            rpn = to_rpn(tokens)
            try:
                y1 = evaluate_rpn(rpn, x_points[i])
                y2 = evaluate_rpn(rpn, mid_x)
                increasing = y2 > y1
                print(f"Function is {'increasing' if increasing else 'decreasing'} on interval ({x_points[i]:.2f}, {x_points[i+1]:.2f})")
            except:
                continue

if __name__ == "__main__":
    print("TI-84 Compatible Function Analyzer v5.0")
    print("Enter a mathematical expression (using x as variable)")
    print("Example: x^2, sin(x), 2*x+1")
    
    try:
        expression = input()
        analyze_function(expression)
    except Exception as e:
        print(f"Error: {str(e)}")