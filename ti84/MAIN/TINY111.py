def _e(expr,x):
    ops=[];vals=[]
    def prec(o):
        return 1 if o in '+-' else 2 if o in '*/' else 3 if o=='^' else 0
    def apply():
        o=ops.pop()
        if o=='sin': vals.append(__import__('math').sin(vals.pop()))
        elif o=='cos': vals.append(__import__('math').cos(vals.pop()))
        else:
            b=vals.pop(); a=vals.pop()
            if o=='+': vals.append(a+b)
            elif o=='-': vals.append(a-b)
            elif o=='*': vals.append(a*b)
            elif o=='/': vals.append(a/b)
            elif o=='^': vals.append(a**b)
    i=0;L=len(expr)
    while i<L:
        c=expr[i]
        if c.isspace(): i+=1; continue
        if c.isdigit() or c=='.':
            n=c;i+=1
            while i<L and (expr[i].isdigit() or expr[i]=='.'): n+=expr[i]; i+=1
            vals.append(float(n)); continue
        if c=='x': vals.append(x); i+=1; continue
        if c.isalpha():
            f=c;i+=1
            while i<L and expr[i].isalpha(): f+=expr[i]; i+=1
            ops.append(f); continue
        if c in '+-*/^':
            if c=='-' and (i==0 or expr[i-1] in '()+-*/^'):
                i+=1; n='-'
                while i<L and (expr[i].isdigit() or expr[i]=='.'): n+=expr[i]; i+=1
                vals.append(float(n)); continue
            while ops and prec(ops[-1])>=prec(c):
                try: apply()
                except: return None
            ops.append(c); i+=1; continue
        if c=='(': ops.append('('); i+=1; continue
        if c==')':
            while ops and ops[-1]!='(':
                try: apply()
                except: return None
            if ops and ops[-1]=='(': ops.pop()
            if ops and ops[-1] in ('sin','cos'):
                try: apply()
                except: return None
            i+=1; continue
        i+=1
    while ops:
        try: apply()
        except: return None
    return vals[0] if vals else None

def run(expr=None,preset='x^2-3x+2'):
    e = expr if expr else preset
    y0 = _e(e,0.0)
    if y0 is None: print('Yint: ?'); return
    print('Yint:', round(y0,3))
    zs=[]; x=-10.0; last=None
    while x<=10.0:
        y=_e(e,x)
        if y is None: last=None; x+=1.0; continue
        if last is not None and last*y<0: zs.append(round(x-1.0,3))
        last=y; x+=1.0
    print('Zeros:', zs if zs else 'none')

if __name__=='__main__':
    print('calc2_tiny2')
    run()
