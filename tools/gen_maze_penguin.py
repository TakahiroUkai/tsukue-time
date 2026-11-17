import random
random.seed(23)
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
peng=('<g><ellipse cx="{x}" cy="{y}" rx="4" ry="4.8" style="fill:#111;stroke-width:.6"/>'
 '<ellipse cx="{x}" cy="{y1}" rx="2.6" ry="2.9" style="fill:#fff;stroke:none"/>'
 '<circle cx="{xl}" cy="{ye}" r=".95" style="fill:#fff;stroke:none"/><circle cx="{xr}" cy="{ye}" r=".95" style="fill:#fff;stroke:none"/>'
 '<circle class="fb" cx="{xl}" cy="{ye}" r=".45" style="stroke:none"/><circle class="fb" cx="{xr}" cy="{ye}" r=".45" style="stroke:none"/>'
 '<path d="M{xl2} {yb}L{xr2} {yb}L{x} {yb2}z" style="stroke-width:.6"/>'
 '<path d="M{xa} {yf}l-2 1.2h2.6zM{xb} {yf}l2 1.2h-2.6z" style="stroke-width:.6"/></g>').format(
 x=sx,y=sy-.3,y1=sy+1.3,xl=sx-1.5,xr=sx+1.5,ye=sy-2.9,xl2=sx-1,xr2=sx+1,yb=sy-1.8,yb2=sy-.5,xa=sx-1.6,xb=sx+1.6,yf=sy+4.6)
gx,gy=cx(C-1),cy(R-1)
fish=('<g><ellipse cx="{x}" cy="{y}" rx="3.8" ry="2.4" style="stroke-width:.9"/>'
 '<path d="M{t} {y}l3 -2.6v5.2z" style="stroke-width:.9"/>'
 '<circle class="fb" cx="{e}" cy="{y0}" r=".6" style="stroke:none"/></g>').format(x=gx-2.2,y=gy,t=gx+1.5,e=gx-4.2,y0=gy-.5)
svg=('<svg class="art-svg" viewBox="0 0 100 120" role="img" aria-label="めいろ ペンギンからおさかなへ"><path class="nf" stroke-width="1.6" d="%s"/>%s%s'
     '<text x="%.1f" y="%.1f" style="font-size:3px;font-weight:700;fill:#111;stroke:none;text-anchor:middle">スタート</text>'
     '<text x="%.1f" y="%.1f" style="font-size:3px;font-weight:700;fill:#111;stroke:none;text-anchor:middle">ゴール</text></svg>')%(
     "".join(walls),peng,fish,sx,oy-1.8,gx,oy+R*S+4.6)
html='<div class="sh"><h2>めいろ ペンギンの こおりのうえ<small>おさかなまで いってみよう</small></h2><div class="art">%s</div><div class="foot"><span>なまえ</span><i></i></div></div>'%svg
open("content/sheets/t-maze-penguin.html","w",encoding="utf8").write(html+"\n")
