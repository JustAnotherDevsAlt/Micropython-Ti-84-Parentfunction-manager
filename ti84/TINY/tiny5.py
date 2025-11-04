# ============================================
# TI-84 Plus CE Python PolyTools
# Memory-Optimized JSON Output
# ============================================

def f(cs,x):
    s=0
    d=len(cs)-1
    for c in cs:
        s+=c*(x**d)
        d-=1
    return s

print("PolyTools Minimal")
print("JSON Output Mode")
print()

# Input
deg=int(input("Degree: "))
cs=[]
for i in range(deg,-1,-1):
    cs.append(float(input("x^"+str(i)+": ")))

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

# Y-intercept
try:
    yi=f(cs,0)
    print(' "y_int":',round(yi,2),',')
except:
    print(' "y_int":"undef",')

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