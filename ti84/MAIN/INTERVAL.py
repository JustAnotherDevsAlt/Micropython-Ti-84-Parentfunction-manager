# ============================================
# FILE: interval / s.py
# Sign & Monotonicity Analyzer
# ============================================
def f(cs,x):
    s=0
    d=len(cs)-1
    for c in cs:
        s+=c*(x**d)
        d-=1
    return s

print("=Interval=")
deg=int(input("Degree: "))
cs=[]
for i in range(deg,-1,-1):
    cs.append(float(input("x^"+str(i)+": ")))

st=-10
en=10
stp=0.2

print("\n=Results=")

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
    print("Increasing:")
    for iv in incs:
        print("(",iv[0],",",iv[1],")")
else:
    print("Increasing: none")

if decs:
    print("\nDecreasing:")
    for iv in decs:
        print("(",iv[0],",",iv[1],")")
else:
    print("\nDecreasing: none")

# Positive/Negative
poss=[]
negs=[]
x=st
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
    except:
        pass
    x+=stp

if poss:
    print("\nPositive:")
    for iv in poss:
        print("(",iv[0],",",iv[1],")")
else:
    print("\nPositive: none")

if negs:
    print("\nNegative:")
    for iv in negs:
        print("(",iv[0],",",iv[1],")")
else:
    print("\nNegative: none")
# ============================================
