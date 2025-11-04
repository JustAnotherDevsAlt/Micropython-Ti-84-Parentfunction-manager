# Y-INTERCEPT FINDER - robust for TI-84 MicroPython and CPython
# Supports: numbers, x, + - * / ^ or **, parentheses, implicit multiplication,
# sin, cos, tan, sqrt, ln, log, abs, pi, e

import math

_FUNCS = {
    'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
    'sqrt': math.sqrt, 'ln': math.log, 'log': lambda v: math.log10(v),
    'abs': abs
}
_CONSTS = {'pi': math.pi, 'e': math.e}

def ev(expr, x):
    s = expr.replace(' ', '')
    if not s:
        raise ValueError("Empty expression")

    # tokenization
    toks = []
    i = 0
    L = len(s)
    while i < L:
        c = s[i]

        # number (support decimals)
        if c.isdigit() or (c == '.' and i+1 < L and s[i+1].isdigit()):
            j = i
            while j < L and (s[j].isdigit() or s[j] == '.'):
                j += 1
            # optional simple exponent notation not implemented to keep small
            num = float(s[i:j])
            toks.append(num)
            i = j
            continue

        # variable x
        if c == 'x':
            toks.append('x')
            i += 1
            continue

        # names: functions or constants (letters)
        if c.isalpha():
            j = i
            while j < L and s[j].isalpha():
                j += 1
            name = s[i:j].lower()
            if name in _FUNCS:
                toks.append(name)
            elif name in _CONSTS:
                toks.append(_CONSTS[name])
            else:
                raise ValueError("Unknown name: " + name)
            i = j
            continue

        # operators: handle '**' as power too
        if s.startswith('**', i):
            toks.append('^'); i += 2; continue
        if c in '+-*/^()':
            # treat unary minus/plus later by context insertion of 0
            toks.append(c)
            i += 1
            continue

        # unknown char -> error
        raise ValueError("Invalid character: " + c)

    # handle unary + and -: convert unary - to (0 - <expr-part>) by inserting 0
    new = []
    prev = None
    for t in toks:
        if t == '+' or t == '-':
            if prev is None or prev in ('+', '-', '*', '/', '^', '('):
                # unary operator
                if t == '+':
                    # unary plus -> ignore
                    prev = t
                    continue
                else:
                    new.append(0.0)
                    new.append('-')
                    prev = '-'
                    continue
        new.append(t)
        prev = t
    toks = new

    # insert implicit multiplication where appropriate
    def is_right_atom(token):
        return (isinstance(token, (int, float)) or token == 'x' or token == ')' or token in _FUNCS)
    def is_left_atom(token):
        return (isinstance(token, (int, float)) or token == 'x' or token == '(' or token in _FUNCS)
    new = []
    for idx, t in enumerate(toks):
        if idx > 0:
            prev = toks[idx-1]
            # if previous is an atom and current is a left atom -> insert '*'
            prev_atom = (isinstance(prev, (int, float)) or prev == 'x' or prev == ')' or prev in _FUNCS)
            cur_atom = (isinstance(t, (int, float)) or t == 'x' or t == '(' or t in _FUNCS)
            if prev_atom and cur_atom:
                new.append('*')
        new.append(t)
    toks = new

    # shunting-yard: convert to RPN
    prec = {'+':1, '-':1, '*':2, '/':2, '^':4}
    assoc = {'+':'L','-':'L','*':'L','/':'L','^':'R'}
    out = []
    ops = []

    for t in toks:
        if isinstance(t, (int, float)):
            out.append(float(t))
        elif t == 'x':
            out.append('x')
        elif t in _FUNCS:
            ops.append(t)
        elif t in prec:
            while ops and ops[-1] in prec:
                top = ops[-1]
                if (assoc[t] == 'L' and prec[t] <= prec[top]) or (assoc[t] == 'R' and prec[t] < prec[top]):
                    out.append(ops.pop())
                else:
                    break
            ops.append(t)
        elif t == '(':
            ops.append(t)
        elif t == ')':
            while ops and ops[-1] != '(':
                out.append(ops.pop())
            if not ops or ops[-1] != '(':
                raise ValueError("Mismatched parentheses")
            ops.pop()  # pop '('
            # if function on top, pop it to output
            if ops and ops[-1] in _FUNCS:
                out.append(ops.pop())
        else:
            # could be a constant float already handled above
            raise ValueError("Unknown token during parsing: " + str(t))

    while ops:
        op = ops.pop()
        if op in ('(', ')'):
            raise ValueError("Mismatched parentheses")
        out.append(op)

    # evaluate RPN
    stack = []
    for t in out:
        if isinstance(t, (int, float)):
            stack.append(float(t))
        elif t == 'x':
            stack.append(float(x))
        elif t in _FUNCS:
            if not stack:
                raise ValueError("Not enough operands for function " + t)
            a = stack.pop()
            # domain errors will raise and be reported to caller
            stack.append(_FUNCS[t](a))
        elif t in ('+', '-', '*', '/', '^'):
            if len(stack) < 2:
                raise ValueError("Not enough operands for operator " + t)
            b = stack.pop(); a = stack.pop()
            if t == '+': stack.append(a + b)
            elif t == '-': stack.append(a - b)
            elif t == '*': stack.append(a * b)
            elif t == '/':
                # handle division by zero
                if b == 0:
                    raise ZeroDivisionError("Division by zero")
                stack.append(a / b)
            elif t == '^':
                # use math.pow for safety; will raise on domain errors
                stack.append(math.pow(a, b))
        else:
            raise ValueError("Unknown RPN token: " + str(t))

    if len(stack) != 1:
        raise ValueError("Invalid expression; stack leftover: " + str(stack))
    return stack[0]


def yint():
    print("Y-INTERCEPT FINDER")
    print("------------------")
    try:
        expr = input("f(x)= ")
    except Exception:
        # older environments sometimes don't accept prompt arg
        try:
            print("Enter function for f(x):")
            expr = input()
        except Exception:
            print("Input not available.")
            return None

    try:
        y = ev(expr, 0)
        # round for nicer display but keep raw if desired
        print("Y-int: (0,", round(y, 6), ")")
        return y
    except ZeroDivisionError:
        print("ERROR: Division by zero in expression")
    except ValueError as ve:
        print("ERROR:", ve)
    except OverflowError:
        print("ERROR: numeric overflow")
    except Exception as exc:
        print("ERROR: Could not evaluate expression -", exc)
    return None


# If run as a script on devices that support it
if __name__ == "__main__":
    yint()
