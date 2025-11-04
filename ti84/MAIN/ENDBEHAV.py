# ============================================
# FILE: endbehav.py
# End Behavior Analyzer
# ============================================
print("=EndBehavior=")
deg=int(input("Degree: "))
lc=float(input("LC: "))

print("\nDeg:",deg)
if deg%2==0:
    print("Type: EVEN")
    if lc>0:
        print("\nx->-inf: +inf")
        print("x->+inf: +inf")
        print("Rise both")
    else:
        print("\nx->-inf: -inf")
        print("x->+inf: -inf")
        print("Fall both")
else:
    print("Type: ODD")
    if lc>0:
        print("\nx->-inf: -inf")
        print("x->+inf: +inf")
        print("Fall L, Rise R")
    else:
        print("\nx->-inf: +inf")
        print("x->+inf: -inf")
        print("Rise L, Fall R")

print("\nMaxTurns:",deg-1)

if lc>0:
    print("LC: Positive")
else:
    print("LC: Negative")
