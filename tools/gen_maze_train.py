import random
from collections import deque
import sys
random.seed(7)
C,R,S=6,8,14
vis={(0,0)};open_=set();stack=[(0,0)]
while stack:
    x,y=stack[-1]
    nb=[(x+dx,y+dy) for dx,dy in((1,0),(-1,0),(0,1),(0,-1)) if 0<=x+dx<C and 0<=y+dy<R and (x+dx,y+dy) not in vis]
    if not nb: stack.pop();continue
    n=random.choice(nb);vis.add(n);open_.add(frozenset(((x,y),n)));stack.append(n)
prev={(0,0):None};d=deque([(0,0)])
while d:
    c=d.popleft()
    for dx,dy in((1,0),(-1,0),(0,1),(0,-1)):
        n=(c[0]+dx,c[1]+dy)
        if frozenset((c,n)) in open_ and n not in prev:prev[n]=c;d.append(n)
L=0;c=(C-1,R-1)
while c:L+=1;c=prev[c]
print("pathlen",L)
ox,oy=8,6
walls=[]
def seg(x1,y1,x2,y2):walls.append("M%d %dL%d %d"%(ox+x1*S,oy+y1*S,ox+x2*S,oy+y2*S))
for y in range(R+1):
    for x in range(C):
        if y==0:
            if x!=0: seg(x,0,x+1,0)
        elif y==R:
            if x!=C-1: seg(x,R,x+1,R)
        elif frozenset(((x,y-1),(x,y))) not in open_: seg(x,y,x+1,y)
for x in range(C+1):
    for y in range(R):
        if x in(0,C) or frozenset(((x-1,y),(x,y))) not in open_: seg(x,y,x,y+1)
cx=lambda i:ox+i*S+S/2
cy=lambda j:oy+j*S+S/2
x,y=cx(0),cy(0)
train=('<g stroke-width="1"><rect x="{a}" y="{t}" width="8" height="5.2" rx=".8"/>'
 '<rect x="{b}" y="{t2}" width="3.2" height="6.4" rx=".6"/>'
 '<rect class="nf" x="{c}" y="{t3}" width="2" height="2.2"/>'
 '<rect class="nf" x="{w}" y="{t4}" width="1.6" height="1.8" stroke-width=".6"/>'
 '<circle cx="{w1}" cy="{wy}" r="1.4"/><circle cx="{w2}" cy="{wy}" r="1.4"/><circle cx="{w3}" cy="{wy}" r="1.4"/></g>').format(
 a=x-5.6,t=y-3,b=x+2.4,t2=y-4.2,c=x-4,t3=y-5.2,w=x+3.2,t4=y-3.2,w1=x-3.6,w2=x,w3=x+3.8,wy=y+3.2)
gx,gy=cx(C-1),cy(R-1)
station=('<g stroke-width="1"><path d="M{l} {r0}L{gx} {top}L{r} {r0}Z"/>'
 '<rect x="{wl}" y="{r0}" width="9" height="6.2"/>'
 '<rect class="nf" x="{d1}" y="{dy}" width="2.4" height="3.8"/>'
 '<rect class="nf" x="{k1}" y="{ky}" width="1.8" height="1.8" stroke-width=".6"/><rect class="nf" x="{k2}" y="{ky}" width="1.8" height="1.8" stroke-width=".6"/>'
 '<circle class="nf" cx="{gx}" cy="{cy}" r="1.1" stroke-width=".6"/></g>').format(
 l=gx-6,r=gx+6,r0=gy-1.4,gx=gx,top=gy-6.4,wl=gx-4.5,d1=gx-1.2,dy=gy+1.0,k1=gx-3.7,k2=gx+1.9+0.0,ky=gy+0.2,cy=gy-3.2)
dino=train;egg=station
svg=('<svg class="art-svg" viewBox="0 0 100 120" role="img" aria-label="めいろ でんしゃの えき"><path class="nf" stroke-width="1.8" d="%s"/>%s%s'
 '<text x="%.1f" y="%.1f" style="font-size:3px;font-weight:700;fill:#111;stroke:none;text-anchor:middle">スタート</text>'
 '<text x="%.1f" y="%.1f" style="font-size:3px;font-weight:700;fill:#111;stroke:none;text-anchor:middle">ゴール</text></svg>')%(
 "".join(walls),dino,egg,x,oy-1.8,gx,oy+R*S+4.6)
html='<div class="sh"><h2>めいろ でんしゃの えき<small>えきまで いこう</small></h2><div class="art">%s</div><div class="foot"><span>なまえ</span><i></i></div></div>'%svg
open("content/sheets/t-maze-train.html","w",encoding="utf8").write(html+"\n")
