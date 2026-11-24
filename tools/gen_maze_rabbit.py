import random
from collections import deque
import sys
random.seed(11)
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
dino=('<g stroke-width="1"><ellipse cx="{bx}" cy="{by}" rx="4.6" ry="3.4"/>'
 '<circle cx="{hx}" cy="{hy}" r="3"/>'
 '<ellipse cx="{e1}" cy="{ey}" rx="1.1" ry="3.4"/><ellipse cx="{e2}" cy="{ey}" rx="1.1" ry="3.4"/>'
 '<circle class="nf" cx="{tx}" cy="{by}" r="1.3" stroke-width=".7"/>'
 '<circle cx="{ex}" cy="{hy}" r=".55" style="fill:#111;stroke:none"/>'
 '<circle class="nf" cx="{nx}" cy="{ny}" r=".5" stroke-width=".5"/></g>').format(
 bx=x-1.4,by=y+2.4,hx=x+3.2,hy=y-0.6,e1=x+2.2,e2=x+4.4,ey=y-5.0,tx=x-6.2,ex=x+3.9,nx=x+5.7,ny=y-0.2)
gx,gy=cx(C-1),cy(R-1)
dino='<g transform="translate(%.1f %.1f) scale(.78) translate(%.1f %.1f)">'%(x,y,-x,-y)+dino+'</g>'
egg=('<g stroke-width="1"><path d="M{l} {t}L{r} {t}L{gx} {b}Z"/>'
 '<path d="M{gx} {t}L{a} {l1}M{gx} {t}L{gx} {l2}M{gx} {t}L{c} {l1}"/>'
 '<path class="nf" d="M{p1} {y1}L{p2} {y1}M{p3} {y2}L{p4} {y2}" stroke-width=".6"/></g>').format(
 l=gx-4.4,r=gx+4.4,t=gy-3.6,b=gy+5.4,gx=gx,a=gx-4,c=gx+4,l1=gy-8.2,l2=gy-9,
 p1=gx-2.8,p2=gx-0.8,y1=gy-1.0,p3=gx+0.6,p4=gx+2.6,y2=gy+1.6)
egg='<g transform="translate(%.1f %.1f) scale(.8) translate(%.1f %.1f)">'%(gx,gy,-gx,-gy)+egg+'</g>'
svg=('<svg class="art-svg" viewBox="0 0 100 120" role="img" aria-label="めいろ うさぎの にんじん"><path class="nf" stroke-width="1.8" d="%s"/>%s%s'
 '<text x="%.1f" y="%.1f" style="font-size:3px;font-weight:700;fill:#111;stroke:none;text-anchor:middle">スタート</text>'
 '<text x="%.1f" y="%.1f" style="font-size:3px;font-weight:700;fill:#111;stroke:none;text-anchor:middle">ゴール</text></svg>')%(
 "".join(walls),dino,egg,x,oy-1.8,gx,oy+R*S+4.6)
html='<div class="sh"><h2>めいろ うさぎの にんじん<small>にんじんまで いこう</small></h2><div class="art">%s</div><div class="foot"><span>なまえ</span><i></i></div></div>'%svg
open("content/sheets/t-maze-rabbit.html","w",encoding="utf8").write(html+"\n")
