import math

def tokenize(expr):
    toks=[]
    i=0
    L=len(expr)
    while i<L:
        c=expr[i]
        if c.isdigit() or c=='.':
            num=c; i+=1
            while i<L and (expr[i].isdigit() or expr[i]=='.'):
                num+=expr[i]; i+=1
            toks.append(num); continue
        if c in '+-*/^()':
            if c=='-' and (i==0 or expr[i-1] in '(+-*/^'):
                num=c; i+=1
                while i<L and (expr[i].isdigit() or expr[i]=='.'):
                    num+=expr[i]; i+=1
                toks.append(num); continue
            toks.append(c); i+=1; continue
        if c.isalpha():
            name=c; i+=1
            while i<L and expr[i].isalpha():
                name+=expr[i]; i+=1
            toks.append(name); continue
        if c.isspace():
            i+=1; continue
        raise ValueError("Bad char: {}".format(c))
    return toks


def to_rpn(toks):
    prec={'+':1,'-':1,'*':2,'/':2,'^':3}
    out=[]; ops=[]
    for t in toks:
        if t.lstrip('-.').replace('.','',1).isdigit() or t=='x':
            out.append(t)
        elif t in '+-*/^':
            while ops and ops[-1] != '(' and prec.get(ops[-1],0) >= prec.get(t,0):
                out.append(ops.pop())
            ops.append(t)
        elif t=='(':
            ops.append(t)
        elif t==')':
            while ops and ops[-1] != '(':
                out.append(ops.pop())
            if ops and ops[-1]=='(':
                ops.pop()
        else:
            ops.append(t)
    while ops:
        out.append(ops.pop())
    return out


def eval_rpn(rpn,x):
    st=[]
    for t in rpn:
        if t.lstrip('-.').replace('.','',1).isdigit():
            st.append(float(t))
        elif t=='x':
            st.append(x)
        elif t in '+-*/^':
            b=st.pop(); a=st.pop()
            if t=='+': st.append(a+b)
            elif t=='-': st.append(a-b)
            elif t=='*': st.append(a*b)
            elif t=='/': st.append(a/b)
            elif t=='^': st.append(a**b)
        elif t=='sin':
            a=st.pop(); st.append(math.sin(a))
        elif t=='cos':
            a=st.pop(); st.append(math.cos(a))
        elif t=='tan':
            a=st.pop(); st.append(math.tan(a))
        else:
            # unknown function, pass-through
            a=st.pop(); st.append(a)
    return st[0]


def y_int(rpn):
    try:
        return (0, eval_rpn(rpn,0))
    except:
        return None


def extrema(rpn,start=-10,end=10,step=0.5):
    x=start
    last_y=None; inc=None
    ex=[]
    while x<=end:
        try:
            y=eval_rpn(rpn,x)
            if last_y is not None:
                cur_inc=(y>last_y)
                if inc is not None and cur_inc!=inc:
                    ex.append((x-step,last_y,'Max' if inc else 'Min'))
                inc=cur_inc
            last_y=y
        except:
            pass
        x+=step
    return ex


def mem_est(expr,start=-10,end=10,step=0.5,limit=160000):
    toks=tokenize(expr)
    est=len(toks)*12+max(1,int(((end-start)/step)+0.5))*8+8*16
    return est<=limit,est


print("TI84 Anlz v5")
expr=input("Expr: ")

try:
    fits,est=mem_est(expr)
    if not fits:
        print("Warn: mem", est)
    toks=tokenize(expr)
    rpn=to_rpn(toks)
    yi=y_int(rpn)
    if yi:
        print("Yint:", round(yi[1],3))
    else:
        print("Yint: ?")
    ex=extrema(rpn)
    if ex:
        for e in ex:
            print(e[2], "@", round(e[0],2), round(e[1],2))
    else:
        print("No extrema")
except Exception as e:
    print("Err:", str(e))
