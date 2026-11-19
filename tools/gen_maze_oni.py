import random
from collections import deque
random.seed(53)
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
oni=('<g><path d="M{a} {b}l.6 -4.4l1.8 3.2z" stroke-width="1"/><path d="M{c} {b}l-.6 -4.4l-1.8 3.2z" stroke-width="1"/>'
 '<circle cx="{x}" cy="{y}" r="5" stroke-width="1"/>'
 '<circle class="fb" cx="{xl}" cy="{ye}" r=".75" style="stroke:none"/><circle class="fb" cx="{xr}" cy="{ye}" r=".75" style="stroke:none"/>'
 '<path class="nf" d="M{xm} {ym}q2 2 4 0" stroke-width=".7"/>'
 '<path class="nf" d="M{xl1} {yb}l1.4 -.8M{xr1} {yb}l-1.4 -.8" stroke-width=".6"/></g>').format(
 x=x,y=y+.6,a=x-2.2,c=x+2.2,b=y-3.2,xl=x-1.9,xr=x+1.9,ye=y,xm=x-2,ym=y+2.2,xl1=x-3,xr1=x+3,yb=y-1.4)
gx,gy=cx(C-1),cy(R-1)
masu=('<g><path d="M{l} {t}H{r}L{r2} {bt}H{l2}z" stroke-width="1"/>'
 '<ellipse cx="{b1x}" cy="{by}" rx="1.5" ry="1" stroke-width=".7"/><ellipse cx="{b2x}" cy="{by2}" rx="1.5" ry="1" stroke-width=".7"/>'
 '<ellipse cx="{b3x}" cy="{by}" rx="1.5" ry="1" stroke-width=".7"/></g>').format(
 l=gx-5.5,r=gx+5.5,t=gy-1.5,l2=gx-4.5,r2=gx+4.5,bt=gy+4.5,
 b1x=gx-2.4,b2x=gx,b3x=gx+2.4,by=gy-2.4,by2=gy-3.6)
svg=('<svg class="art-svg" viewBox="0 0 100 120" role="img" aria-label="めいろ おにから まめへ"><path class="nf" stroke-width="1.8" d="%s"/>%s%s'
 '<text x="%.1f" y="%.1f" style="font-size:3px;font-weight:700;fill:#111;stroke:none;text-anchor:middle">スタート</text>'
 '<text x="%.1f" y="%.1f" style="font-size:3px;font-weight:700;fill:#111;stroke:none;text-anchor:middle">ゴール</text></svg>')%(
 "".join(walls),oni,masu,x,oy-1.8,gx,oy+R*S+4.6)
html='<div class="sh"><h2>めいろ おにから まめへ<small>まめの ますまで いこう</small></h2><div class="art">%s</div><div class="foot"><span>なまえ</span><i></i></div></div>'%svg
open("content/sheets/t-maze-oni.html","w",encoding="utf8").write(html+"\n")
