import random
from collections import deque
random.seed(61)
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
dino=('<g transform="translate({x} {y}) scale(1.15) translate(-{x} -{y})"><ellipse cx="{x}" cy="{y}" rx="5.4" ry="4" stroke-width="1"/>'
 '<circle cx="{hx}" cy="{hy}" r="2.6" stroke-width="1"/>'
 '<circle class="fb" cx="{ex}" cy="{hy1}" r=".6" style="stroke:none"/>'
 '<path class="nf" d="M{mx} {my}q.9 .8 1.8 0" stroke-width=".5"/>'
 '<path class="nf" d="M{t1} {ty}q-2.2 .2 -3.2 -1.6" stroke-width=".9"/>'
 '<path d="M{s1} {sy}l.9 -1.6l.9 1.6M{s2} {sy}l.9 -1.6l.9 1.6" stroke-width=".7"/></g>').format(
 x=x,y=y+1.2,hx=x+4.6,hy=y-2.2,ex=x+5.4,hy1=y-2.7,mx=x+5.4,my=y-1.2,t1=x-5.3,ty=y+1.2,
 s1=x-2.6,s2=x-0.2,sy=y-2.2)
gx,gy=cx(C-1),cy(R-1)
egg=('<g transform="translate({gx} {gy}) scale(1.2) translate(-{gx} -{gy})"><path d="M{l} {nt}Q{gx} {nb} {r} {nt}" stroke-width="1"/>'
 '<ellipse cx="{gx}" cy="{ey}" rx="3.2" ry="4" stroke-width="1"/>'
 '<path class="nf" d="M{z1} {ey}l1.1 -1.3l1.1 1.3l1.1 -1.3l1.1 1.3" stroke-width=".6"/></g>').format(
 l=gx-5.5,r=gx+5.5,nt=gy+1.2,nb=gy+9,gx=gx,gy=gy,ey=gy-1.4,z1=gx-2.2)
svg=('<svg class="art-svg" viewBox="0 0 100 120" role="img" aria-label="めいろ きょうりゅうと たまご"><path class="nf" stroke-width="1.8" d="%s"/>%s%s'
 '<text x="%.1f" y="%.1f" style="font-size:3px;font-weight:700;fill:#111;stroke:none;text-anchor:middle">スタート</text>'
 '<text x="%.1f" y="%.1f" style="font-size:3px;font-weight:700;fill:#111;stroke:none;text-anchor:middle">ゴール</text></svg>')%(
 "".join(walls),dino,egg,x,oy-1.8,gx,oy+R*S+4.6)
html='<div class="sh"><h2>めいろ きょうりゅうと たまご<small>たまごまで いこう</small></h2><div class="art">%s</div><div class="foot"><span>なまえ</span><i></i></div></div>'%svg
open("content/sheets/t-maze-dino.html","w",encoding="utf8").write(html+"\n")
