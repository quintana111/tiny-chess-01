import os,sys,json,urllib.request
U='abcdefgh';V={'p':100,'n':320,'b':330,'r':500,'q':900,'k':20000}
E=os.environ.get('MAKEFUN_ENV_URL') or sys.exit('MAKEFUN_ENV_URL is not set')
def post(p,x):
 r=urllib.request.Request(E+p,data=json.dumps(x).encode(),headers={'content-type':'application/json'})
 return json.load(urllib.request.urlopen(r))
def sq(x):return (int(x[1])-1)*8+U.index(x[0])
def name(x):return U[x&7]+str(x//8+1)
def parse(f):
 a=[]
 for r in f.split()[0].split('/'):
  for c in r:a += [0]*int(c) if c.isdigit() else [c]
 return a,int(f.split()[1]=='w'),f.split()[2],-1 if f.split()[3]=='-' else sq(f.split()[3])
def atk(b,x,us):
 r=x//8;f=x&7
 for d in (-1,1):
  y=x-8*us+d
  if 0<=y<64 and abs((y&7)-f)==1 and b[y]==('P' if us>0 else 'p'):return 1
 for d in ((1,2),(2,1),(-1,2),(-2,1),(1,-2),(2,-1),(-1,-2),(-2,-1)):
  q=(r+d[1])*8+f+d[0]
  if 0<=q<64 and abs((q&7)-f)==abs(d[0]) and b[q]==('N' if us>0 else 'n'):return 1
 for d in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)):
  q=x
  while 1:
   q+=(d[1]*8+d[0]);
   if not 0<=q<64 or abs((q&7)-(q-d[1]*8-d[0])&7)>1:break
   p=b[q]
   if p:
    if (p.isupper()==(us>0)) and (p.lower()=='q' or (p.lower()=='r' and not d[0]*d[1]) or (p.lower()=='b' and d[0]*d[1])):return 1
    break
 for d in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)):
  q=x+d[1]*8+d[0]
  if 0<=q<64 and abs((q&7)-f)<=1 and b[q]==('K' if us>0 else 'k'):return 1
 return 0
def play(s,m):
 b,z,c,e=s; b=b[:];a,d=sq(m[:2]),sq(m[2:4]);p=b[a];b[a]=0
 if p.lower()=='p' and d==e and not b[d]:b[d-8*z]=0
 if p.lower()=='k' and abs(d-a)==2:
  h=7 if d>a else 0; t=5 if d>a else 3;b[t]=b[h];b[h]=0
 if len(m)>4:p=m[4].upper() if z else m[4]
 b[d]=p
 C=c
 for q in ('K','Q') if z else ('k','q'):
  if a==sq('e1' if z else 'e8') or (q=='K' and a==7) or (q=='Q' and a==0) or (q=='k' and a==63) or (q=='q' and a==56):C=C.replace(q,'')
 for q in 'KQkq':
  if d=={'K':7,'Q':0,'k':63,'q':56}[q]:C=C.replace(q,'')
 ne=(a+d)//2 if p.lower()=='p' and abs(d-a)==16 else -1
 return b,-z,C,ne
def gen(s):
 b,z,c,e=s;out=[];us=1 if z else -1
 def add(a,d,x=''):
  m=name(a)+name(d)+x;t=play(s,m);k=next((i for i,p in enumerate(t[0]) if p==('K' if us>0 else 'k')), -1)
  if k>=0 and not atk(t[0],k,-us):out.append((m,t))
 for a,p in enumerate(b):
  if not p or p.isupper()!=bool(z):continue
  r=a//8;f=a&7
  if p.lower()=='p':
   v=8*us;d=a+v;pr='qrbn' if us>0 else 'QRBN'
   if 0<=d<64 and not b[d]:
    if d//8 in (0,7):
     for x in pr:add(a,d,x)
    else:
     add(a,d)
     if r==(1 if us>0 else 6) and not b[a+2*v]:add(a,a+2*v)
   for h in (a+v-1,a+v+1):
    if 0<=h<64 and abs((h&7)-f)==1 and ((b[h] and b[h].isupper()!=bool(z)) or h==e):
     if h//8 in (0,7):
      for x in pr:add(a,h,x)
     else:add(a,h)
  elif p.lower() in 'nk':
   ds=((1,2),(2,1),(-1,2),(-2,1),(1,-2),(2,-1),(-1,-2),(-2,-1)) if p.lower()=='n' else ((1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1))
   for x,y in ds:
    d=a+y*8+x
    if 0<=d<64 and abs((d&7)-f)<=2 and (not b[d] or b[d].isupper()!=bool(z)):add(a,d)
   if p.lower()=='k':
    for q,R in ((6,'K' if z else 'k'),(2,'Q' if z else 'q')):
     h=(0 if z else 56)+q
     if R in c and not any(b[i] for i in ((5,6) if q==6 else (1,2,3))) and not atk(b,a,-us) and not atk(b,a+(1 if q==6 else -1),-us):add(a,h)
  else:
   ds=((1,0),(-1,0),(0,1),(0,-1)) if p.lower()=='r' else ((1,1),(1,-1),(-1,1),(-1,-1)) if p.lower()=='b' else ((1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1))
   for x,y in ds:
    d=a
    while 1:
     q=d+y*8+x
     if not 0<=q<64 or abs((q&7)-(d&7))>1:break
     d=q
     if not b[d]:add(a,d);continue
     if b[d].isupper()!=bool(z):add(a,d)
     break
 return out
N=0
def val(s):
 b,z,_,_=s;return (1 if z else -1)*sum(V[p.lower()]*(1 if p.isupper() else -1) for p in b if p)
def search(s,d,a=-10**6,b=10**6):
 global N
 N+=1
 ms=gen(s)
 if not ms:return -100000 if atk(s[0],next((i for i,p in enumerate(s[0]) if p==('K' if s[1] else 'k')),0),-1 if s[1] else 1) else 0
 if d<1:return val(s)
 ms.sort(key=lambda x:(-(V.get(s[0][sq(x[0][2:4])].lower(),0) if s[0][sq(x[0][2:4])] else 0),x[0]))
 best=-10**6
 for _,t in ms:
  q=-search(t,d-1,-b,-a);best=max(best,q);a=max(a,q)
  if a>=b or N>25000:break
 return best
def choose(f,legal):
 global N
 s=parse(f);best=-10**9;bm=legal[0]
 for m in sorted(legal,key=lambda x:(-(V.get(s[0][sq(x[2:4])].lower(),0) if s[0][sq(x[2:4])] else 0),x)):
  N=0;q=-search(play(s,m),2)
  if q>best:best,bm=q,m
 return bm
while 1:
 g=post('/game',{})
 if g['status']=='done':break
 while g['status']=='your_move':g=post('/move',{'game':g['game'],'move':choose(g['fen'],g['legal_moves'])})
print('done',file=sys.stderr)
