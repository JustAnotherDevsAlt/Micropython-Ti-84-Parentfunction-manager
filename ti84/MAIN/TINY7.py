# ============================================
# TI-84 Plus CE Python PolyTools
# Function Notation Input + JSON Output
# No external imports
# ============================================
from time import sleep

def parse_fx(fx_str):
    """Parse F(x) = ... notation into coefficients list"""
    fx_str = fx_str.replace(" ","").lower()
    if "=" in fx_str:
        fx_str = fx_str.split("=")[1]
    
    fx_str = fx_str.replace("**","^")
    
    # Find highest degree
    max_deg = 0
    i = 0
    while i < len(fx_str):
        if fx_str[i] == 'x':
            if i+1 < len(fx_str) and fx_str[i+1] == '^':
                j = i+2
                num_str = ""
                while j < len(fx_str) and fx_str[j].isdigit():
                    num_str += fx_str[j]
                    j += 1
                if num_str:
                    deg = int(num_str)
                    if deg > max_deg:
                        max_deg = deg
            else:
                if max_deg < 1:
                    max_deg = 1
        i += 1
    
    if max_deg == 0 and 'x' not in fx_str:
        max_deg = 0
    
    coeffs = [0.0] * (max_deg + 1)
    
    if fx_str and fx_str[0] not in ['+','-']:
        fx_str = '+' + fx_str
    
    i = 0
    while i < len(fx_str):
        if fx_str[i] in ['+','-']:
            sign = 1 if fx_str[i] == '+' else -1
            i += 1
            
            coef_str = ""
            while i < len(fx_str) and (fx_str[i].isdigit() or fx_str[i] == '.'):
                coef_str += fx_str[i]
                i += 1
            
            if i < len(fx_str) and fx_str[i] == 'x':
                if coef_str == "":
                    coef = 1.0
                else:
                    coef = float(coef_str)
                coef *= sign
                
                i += 1
                
                if i < len(fx_str) and fx_str[i] == '^':
                    i += 1
                    deg_str = ""
                    while i < len(fx_str) and fx_str[i].isdigit():
                        deg_str += fx_str[i]
                        i += 1
                    deg = int(deg_str)
                else:
                    deg = 1
                
                coeffs[max_deg - deg] = coef
            else:
                if coef_str:
                    coef = float(coef_str) * sign
                    coeffs[max_deg] = coef
        else:
            i += 1
    
    return coeffs, max_deg

def f(cs,x):
    s=0
    d=len(cs)-1
    for c in cs:
        s+=c*(x**d)
        d-=1
    return s

print("PolyTools FX Mode")
print("JSON Output")
print()

fx_input = input("F(x) = ")
if not fx_input.strip():
    fx_input = "x^2"

try:
    cs, deg = parse_fx(fx_input)
except:
    print("Parse error, using x^2")
    cs = [1.0, 0.0, 0.0]
    deg = 2

lc=cs[0]
st=-10
en=10
stp=0.25

# ============================================
# OUTPUT START
# ============================================
print()
print("{")

# End Behavior
print(' "degree":',deg,',')
print(' "lc_sign":"'+('pos' if lc>0 else 'neg')+'",')
sleep(0.1)
if deg%2==0:
    print(' "deg_type":"even",')
    if lc>0:
        print(' "eb_left":"rise",')
        print(' "eb_right":"rise",')
    else:
        print(' "eb_left":"fall",')
        print(' "eb_right":"fall",')
else:
    print(' "deg_type":"odd",')
    if lc>0:
        print(' "eb_left":"fall",')
        print(' "eb_right":"rise",')
    else:
        print(' "eb_left":"rise",')
        print(' "eb_right":"fall",')

print(' "max_turns":',deg-1,',')
sleep(0.1)

# Y-intercept
try:
    yi=f(cs,0)
    print(' "y_int":',round(yi,2),',')
except:
    print(' "y_int":"undef",')
sleep(0.1)

# Find increase/decrease intervals
incs=[]
decs=[]
x=st
lv=None
ci=None
istart=None

while x<=en:
    try:
        v=f(cs,x)
        if lv is not None:
            ni=(v>lv)
            if ci is None:
                ci=ni
                istart=x-stp
            elif ci!=ni:
                if ci:
                    incs.append((round(istart,1),round(x-stp,1)))
                else:
                    decs.append((round(istart,1),round(x-stp,1)))
                ci=ni
                istart=x-stp
        lv=v
    except:
        pass
    x+=stp

# Output increase intervals
print(' "increase":[')
if incs:
    for i,iv in enumerate(incs):
        if i<len(incs)-1:
            print('  [',iv[0],',',iv[1],'],')
        else:
            print('  [',iv[0],',',iv[1],']')
print(' ],')
sleep(0.1)

# Output decrease intervals
print(' "decrease":[')
if decs:
    for i,iv in enumerate(decs):
        if i<len(decs)-1:
            print('  [',iv[0],',',iv[1],'],')
        else:
            print('  [',iv[0],',',iv[1],']')
print(' ],')

# Find zeros
zs=[]
x=st
lv=None
while x<=en:
    try:
        v=f(cs,x)
        if abs(v)<0.05:
            if not zs or abs(x-zs[-1])>0.5:
                zs.append(round(x,2))
        elif lv is not None:
            if (lv<0 and v>0)or(lv>0 and v<0):
                if not zs or abs(x-zs[-1])>0.5:
                    zs.append(round(x-stp/2,2))
        lv=v
    except:
        pass
    x+=stp

print(' "zeros":[')
if zs:
    for i,z in enumerate(zs):
        if i<len(zs)-1:
            print('  ',z,',')
        else:
            print('  ',z)
print(' ],')
sleep(0.1)

# Domain and Range
print(' "domain":"(-inf,inf)",')
if deg%2==1:
    print(' "range":"(-inf,inf)"')
else:
    if lc>0:
        print(' "range":"[min,inf)"')
    else:
        print(' "range":"(-inf,max]"')

print("}")
print()
print("Done")
