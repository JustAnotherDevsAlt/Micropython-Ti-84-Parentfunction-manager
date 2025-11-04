# END BEHAVIOR IDENTIFIER (NO IMPORTS)
# Works with input like "f(x)=x^3-2*x" or just "x^2-4"

def f(expr, x):
    expr = expr.replace('^', '**')
    # Strip "f(x)=" if user includes it
    if "f(x)=" in expr:
        expr = expr.split("=", 1)[1]
    return eval(expr, {"x": x})

def describe(value):
    # Gives a readable description of the output
    if value is None:
        return "undefined"
    if value > 1e6:
        return "∞"
    if value < -1e6:
        return "-∞"
    return str(round(value, 3))

def end_behavior(expr):
    print("="*28)
    print("END BEHAVIOR ANALYSIS")
    print("="*28)
    try:
        left = f(expr, -999999)
    except:
        left = None
    try:
        right = f(expr, 999999)
    except:
        right = None

    print("As x → -∞, f(x) →", describe(left))
    print("As x → ∞,  f(x) →", describe(right))
    print("="*28)

def main():
    print("END BEHAVIOR TOOL")
    expr = input("Enter function f(x): ")
    end_behavior(expr)

main()
# --- coarse root finding (bounded) ---
