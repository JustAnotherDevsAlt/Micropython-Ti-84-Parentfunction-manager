# ============================================
# FILE: domrange.py
# Domain & Range Helper
# ============================================
def f(cs,x):
    s=0
    d=len(cs)-1
    for c in cs:
        s+=c*(x**d)
        d-=1
    return s

print("=DomRange=")
deg=int(input("Degree: "))
cs=[]
for i in range(deg,-1,-1):
    cs.append(float(input("x^"+str(i)+": ")))

lc=cs[0]

print("\n=Results=")
print("Domain:")
print("(-inf,inf)")
print("All reals")

print("\nRange:")
if deg%2==1:
    print("(-inf,inf)")
    print("All reals")
else:
    if lc>0:
        # Find minimum
        st=-10
        en=10
        stp=0.2
        mn=None
        x=st
        while x<=en:
            try:
                v=f(cs,x)
                if mn is None or v<mn:
                    mn=v
            except:
                pass
            x+=stp
        
        if mn is not None:
            print("["+str(round(mn,2))+",inf)")
            print("y>="+str(round(mn,2)))
        else:
            print("[min,inf)")
    else:
        # Find maximum
        st=-10
        en=10
        stp=0.2
        mx=None
        x=st
        while x<=en:
            try:
                v=f(cs,x)
                if mx is None or v>mx:
                    mx=v
            except:
                pass
            x+=stp
        
        if mx is not None:
            print("(-inf,"+str(round(mx,2))+"]")
            print("y<="+str(round(mx,2)))
        else:
            print("(-inf,max]")

# For quadratics, show vertex
if deg==2:
    a=cs[0]
    b=cs[1]
    c=cs[2]
    h=-b/(2*a)
    k=f(cs,h)
    print("\nVertex:")
    print("("+str(round(h,2))+","+str(round(k,2))+")")
    if a>0:
        print("Opens: UP")
    else:
        print("Opens: DOWN")
