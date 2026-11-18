import random
random.seed(31)
C,R,S=7,9,12
vis={(0,0)};adj={}
stack=[(0,0)]
open_=set()
while stack:
    x,y=stack[-1]
    nb=[(x+dx,y+dy) for dx,dy in((1,0),(-1,0),(0,1),(0,-1)) if 0<=x+dx<C and 0<=y+dy<R and (x+dx,y+dy) not in vis]
    if not nb: stack.pop();continue
    n=random.choice(nb);vis.add(n);open_.add(frozenset(((x,y),n)));stack.append(n)
# solution length
from collections import deque
prev={(0,0):None};d=deque([(0,0)])
while d:
    c=d.popleft()
    for dx,dy in((1,0),(-1,0),(0,1),(0,-1)):
        n=(c[0]+dx,c[1]+dy)
        if frozenset((c,n)) in open_ and n not in prev:prev[n]=c;d.append(n)
L=0;c=(C-1,R-1)
while c:L+=1;c=prev[c]
print("pathlen",L)
ox,oy=8,6  # offset in viewBox
walls=[]
def seg(x1,y1,x2,y2):walls.append("M%d %dL%d %d"%(ox+x1*S,oy+y1*S,ox+x2*S,oy+y2*S))
for y in range(R+1):
    for x in range(C):
        if y==0:
            if x!=0: seg(x,0,x+1,0)   # entrance top-left open
        elif y==R:
            if x!=C-1: seg(x,R,x+1,R)  # exit bottom-right open
        elif frozenset(((x,y-1),(x,y))) not in open_: seg(x,y,x+1,y)
for x in range(C+1):
    for y in range(R):
        if x in(0,C): seg(x,y,x,y+1)
        elif frozenset(((x-1,y),(x,y))) not in open_: seg(x,y,x,y+1)
def cx(i):return ox+i*S+S/2
def cy(j):return oy+j*S+S/2

sx,sy=cx(0),cy(0)
mochi=('<g><ellipse cx="{x}" cy="{y2}" rx="4.8" ry="2.9" stroke-width=".9"/>'
 '<ellipse cx="{x}" cy="{y1}" rx="3.4" ry="2.4" stroke-width=".9"/>'
 '<circle class="fb" cx="{xl}" cy="{ye}" r=".6" style="stroke:none"/><circle class="fb" cx="{xr}" cy="{ye}" r=".6" style="stroke:none"/>'
 '<path class="nf" d="M{xm1} {ym}q1 1 2 0" stroke-width=".5"/>'
 '<path class="nf" d="M{x} {yo}v-1.1" stroke-width=".7"/><circle cx="{x}" cy="{yo2}" r="1.5" stroke-width=".7"/></g>').format(
 x=sx,y1=sy-.6,y2=sy+2.4,xa=sx-3.2,yt=sy-3.5,xl=sx-1.2,xr=sx+1.2,ye=sy-.9,xm1=sx-1,ym=sy+.2,yo=sy-2.9,yo2=sy-4.4)
gx,gy=cx(C-1),cy(R-1)
bowl=('<g><ellipse cx="{x}" cy="{ym}" rx="3.2" ry="2.2" stroke-width=".8"/>'
 '<path d="M{xl} {yr}H{xr}C{xr} {yb1} {xi} {yb} {x} {yb}C{xo} {yb} {xl} {yb1} {xl} {yr}z" stroke-width=".9"/>'
 '<path class="nf" d="M{xs1} {ys}q-1 -1.2 0 -2.4M{xs2} {ys}q-1 -1.2 0 -2.4" stroke-width=".6"/></g>').format(
 x=gx,ym=gy-1.8,xl=gx-5,xr=gx+5,yr=gy-1,yb1=gy+3.6,yb=gy+4.8,xi=gx+2.4,xo=gx-2.4,xs1=gx-1.2,xs2=gx+1.4,ys=gy-3.6)
svg=('<svg class="art-svg" viewBox="0 0 100 120" role="img" aria-label="めいろ おもちとおぞうに"><path class="nf" stroke-width="1.6" d="%s"/>%s%s'
     '<text x="%.1f" y="%.1f" style="font-size:3px;font-weight:700;fill:#111;stroke:none;text-anchor:middle">スタート</text>'
     '<text x="%.1f" y="%.1f" style="font-size:3px;font-weight:700;fill:#111;stroke:none;text-anchor:middle">ゴール</text></svg>')%(
     "".join(walls),mochi,bowl,sx,oy-1.8,gx,oy+R*S+4.6)
html='<div class="sh"><h2>めいろ おもちと おぞうに<small>おわんまで いこう</small></h2><div class="art">%s</div><div class="foot"><span>なまえ</span><i></i></div></div>'%svg
open("content/sheets/t-maze-mochi.html","w",encoding="utf8").write(html+"\n")
