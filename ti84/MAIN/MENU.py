# ============================================
# TI-84 Plus CE Python PolyTools Codebase
# Memory-Optimized version 
# ============================================
# Each file < 3KB, MicroPython 1.4-1.5 compatible
# No external libraries. files provided as-is.
# ============================================
# FILE: menu.py
# Main Launcher - Run this first
print("PolyTools v1.0")
print("1.EndBehavior")
print("2.Analyze")
print("3.TinyTool")
print("4.Interval")
print("5.Extrema")
print("6.DomRange")

ch=input("Tool: ")
if ch=='1':
    import endbehav
elif ch=='2':
    import analyze
elif ch=='3':
    import tiny5
elif ch=='4':
    import interval
elif ch=='5':
    import extrema
elif ch=='6':
    import domrange
