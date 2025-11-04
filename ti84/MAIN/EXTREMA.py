
# ============================================
# FILE: extrema.py
# Min/Max Finder
# ============================================
def f(cs,x):
    s=0
    d=len(cs)-1
    for c in cs:
        s+=c*(x**d)
        d-=1
    return s

print("=Extrema=")
deg=int(input("Degree: "))
cs=[]
for i in range(deg,-1,-1):
    cs.append(float(input("x^"+str(i)+": ")))

st=-10
en=10
stp=0.2

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

print("\n=Results=")
if exs:
    print("Found:",len(exs))
    print()
    for e in exs:
        print(e[2],"@",e[0])
        print(" y=",e[1])
        print()
    
    # Absolute extrema
    mins=[e for e in exs if e[2]=='Min']
    maxs=[e for e in exs if e[2]=='Max']
    
    if mins:
        am=min(mins,key=lambda e:e[1])
        print("AbsMin:",am[1])
        print(" @x=",am[0])
    
    if maxs:
        am=max(maxs,key=lambda e:e[1])
        print("\nAbsMax:",am[1])
        print(" @x=",am[0])
else:
    print("No extrema found")
