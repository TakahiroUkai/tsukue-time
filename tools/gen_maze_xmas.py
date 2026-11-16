import random
random.seed(11)
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
# start: reindeer face in cell (0,0), goal tree in cell (C-1,R-1)
sx,sy=cx(0),cy(0)
reindeer=('<g><path class="nf" d="M%.1f %.1fl-2.2 -3.2m2.2 3.2l2.2 -3.2m-4.4 3.2l-1.8 0m5.4 -0l1.8 0" transform="translate(0 0)"/>'%(sx,sy-1.8)) if False else ''
rd=('<g><path class="nf" d="M{l} {t}l-2.2 -3.6m1.1 1.8l-1.8 -.2m2.9 -1.6l1.8 -.2" stroke-width="1"/>'
    '<path class="nf" d="M{r} {t}l2.2 -3.6m-1.1 1.8l1.8 -.2m-2.9 -1.6l-1.8 -.2" stroke-width="1"/>'
    '<ellipse cx="{x}" cy="{y}" rx="4.2" ry="3.6" stroke-width=".9"/>'
    '<circle class="fb" cx="{x1}" cy="{y0}" r=".7"/><circle class="fb" cx="{x2}" cy="{y0}" r=".8"/>'
    '<circle class="fb" cx="{x}" cy="{y3}" r="1.2"/></g>').format(l=sx-2,r=sx+2,t=sy-1.8,x=sx,y=sy+.8,x1=sx-1.6,x2=sx+1.6,y0=sy+.2,y3=sy+2)
gx,gy=cx(C-1),cy(R-1)
tree=('<g><path d="M{x} {a}l3.4 4.2h-1.8l2.4 3h-8l2.4 -3h-1.8z"/><rect x="{r}" y="{b}" width="1.6" height="1.6"/>'
      '<path class="nf" d="M{x} {s}l.5 .9 1 .1 -.7 .7 .2 1 -1 -.5 -1 .5 .2 -1 -.7 -.7 1 -.1z"/></g>').format(x=gx,a=gy-4.4,r=gx-.8,b=gy+3.4,s=gy-6)
svg=('<svg class="art-svg" viewBox="0 0 100 120" role="img" aria-label="めいろ トナカイからツリーへ"><path class="nf" stroke-width="1.6" d="%s"/>%s%s'
     '<text x="%.1f" y="%.1f" style="font-size:3px;font-weight:700;fill:#111;stroke:none;text-anchor:middle">スタート</text>'
     '<text x="%.1f" y="%.1f" style="font-size:3px;font-weight:700;fill:#111;stroke:none;text-anchor:middle">ゴール</text></svg>')%(
     "".join(walls),rd,tree,sx,oy-1.8,gx,oy+R*S+4.6)
html='<div class="sh"><h2>めいろ トナカイと ツリー<small>スタートから ゴールへ</small></h2><div class="art">%s</div><div class="foot"><span>なまえ</span><i></i></div></div>'%svg
open("content/sheets/t-maze-xmas.html","w",encoding="utf8").write(html+"\n")
