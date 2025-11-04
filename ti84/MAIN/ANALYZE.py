
# ============================================
# FILE: analyze.py
# Comprehensive Function Analyzer
# ============================================
import math

def f(cs,x):
    s=0
    d=len(cs)-1
    for c in cs:
        s+=c*(x**d)
        d-=1
    return s

def sgn_chg(a,b):
    return (a<0 and b>0)or(a>0 and b<0)

print("=Analyze=")
deg=int(input("Degree: "))
cs=[]
for i in range(deg,-1,-1):
    if i==0:
        cs.append(float(input("x^0: ")))
    else:
        cs.append(float(input("x^"+str(i)+": ")))

lc=cs[0]
st=-10
en=10
stp=0.2

print("\n=Results=")

# End behavior
if deg%2==0:
    print("Deg: EVEN")
    if lc>0:
        print("EB: Rise both")
    else:
        print("EB: Fall both")
else:
    print("Deg: ODD")
    if lc>0:
        print("EB: Fall L, Rise R")
    else:
        print("EB: Rise L, Fall R")

print("MaxTurns:",deg-1)

# Y-intercept
try:
    yi=f(cs,0)
    print("Yint:",round(yi,2))
except:
    print("Yint: undef")

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
        elif lv is not None and sgn_chg(lv,v):
            if not zs or abs(x-zs[-1])>0.5:
                zs.append(round(x-stp/2,2))
        lv=v
    except:
        pass
    x+=stp

if zs:
    print("Zeros:",len(zs))
    for z in zs[:5]:
        print(" x="+str(z))
else:
    print("Zeros: none")

# Find extrema
exs=[]
x=st
lv=None
inc=None
while x<=en:
    try:
        v=f(cs,x)
        if lv is not None:
            ci=(v>lv)
            if inc is not None and ci!=inc:
                exs.append((round(x-stp,2),round(lv,2),'Max' if inc else 'Min'))
            inc=ci
        lv=v
    except:
        pass
    x+=stp

if exs:
    print("Extrema:",len(exs))
    for e in exs[:5]:
        print(" "+e[2],e[0],e[1])
    
    # Abs min/max
    mins=[e for e in exs if e[2]=='Min']
    maxs=[e for e in exs if e[2]=='Max']
    if mins:
        am=min(mins,key=lambda e:e[1])
        print("AbsMin:",am[1],"@",am[0])
    if maxs:
        am=max(maxs,key=lambda e:e[1])
        print("AbsMax:",am[1],"@",am[0])
else:
    print("Extrema: none")

# Increasing/Decreasing
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

if incs:
    print("Inc:",len(incs),"int")
    for iv in incs[:3]:
        print(" (",iv[0],",",iv[1],")")
if decs:
    print("Dec:",len(decs),"int")
    for iv in decs[:3]:
        print(" (",iv[0],",",iv[1],")")

# Positive/Negative
poss=[]
negs=[]
x=st
lv=None
ci=None
istart=None
while x<=en:
    try:
        v=f(cs,x)
        ni=(v>0)
        if ci is None:
            ci=ni
            istart=x
        elif ci!=ni:
            if ci:
                poss.append((round(istart,1),round(x,1)))
            else:
                negs.append((round(istart,1),round(x,1)))
            ci=ni
            istart=x
        lv=v
    except:
        pass
    x+=stp

if poss:
    print("Pos:",len(poss),"int")
    for iv in poss[:3]:
        print(" (",iv[0],",",iv[1],")")
if negs:
    print("Neg:",len(negs),"int")
    for iv in negs[:3]:
        print(" (",iv[0],",",iv[1],")")

print("\nDom: (-inf,inf)")
if deg%2==1:
    print("Rng: (-inf,inf)")
else:
    if lc>0:
        print("Rng: [min,inf)")
    else:
        print("Rng: (-inf,max]")
