# ちがいさがし クリスマスツリー(うえ・したで3つちがう)
import math
def star(cx,cy,R,r):
    pts=[]
    for i in range(10):
        a=-math.pi/2+i*math.pi/5
        rr=R if i%2==0 else r
        pts.append("%.1f %.1f"%(cx+rr*math.cos(a),cy+rr*math.sin(a)))
    return '<path d="M'+'L'.join(pts)+'Z"/>'
def scene(top):
    s=[]
    s.append('<rect class="nf" x="1" y="1" width="98" height="56" rx="3" stroke-width="1"/>')
    s.append('<path class="nf" d="M3 54H97" stroke-width="1"/>')
    # tree
    s.append('<rect x="46" y="48" width="8" height="6"/>')
    s.append('<path d="M30 48L50 25L70 48Z"/><path d="M34 35L50 15L66 35Z"/><path d="M38 23L50 8L62 23Z"/>')
    if top: s.append(star(50,6,4.6,2))
    for x,y in((46,30),(58,39),(40,45),(55,46)):
        s.append('<circle cx="%d" cy="%d" r="2"/><path class="nf th" d="M%.1f %.1fL%.1f %.1f"/>'%(x,y,x-1,y-.6,x-.5,y-1.1))
    # snowman
    s.append('<circle cx="14" cy="46.5" r="7"/><circle cx="14" cy="34.5" r="5"/>')
    s.append('<circle class="fb" cx="12.4" cy="33.6" r=".7"/><circle class="fb" cx="15.6" cy="33.6" r=".7"/><path class="nf" d="M14 35L17.4 35.8"/>')
    s.append('<circle class="fb" cx="14" cy="45" r=".8"/><circle class="fb" cx="14" cy="48" r=".8"/>')
    if top: s.append('<rect x="10.5" y="24.5" width="7" height="5.5"/><rect x="8.4" y="29.4" width="11.2" height="2"/>')
    # present
    s.append('<rect x="75" y="45" width="16" height="9"/><rect x="74" y="42" width="18" height="3.6"/>')
    if top: s.append('<path class="nf" d="M83 42V54"/><ellipse cx="80" cy="39.8" rx="3" ry="2"/><ellipse cx="86" cy="39.8" rx="3" ry="2"/>')
    # snow
    for x,y in((8,10),(22,16),(32,6),(70,10),(86,18),(92,8),(78,28),(6,22),(64,28),(24,26)):
        s.append('<circle class="fb" cx="%d" cy="%d" r=".7"/>'%(x,y))
    return '<svg class="art-svg" viewBox="0 0 100 58" style="width:100%%;display:block" role="img" aria-label="%s">%s</svg>'%(
        "クリスマスツリーの え(うえ)" if top else "クリスマスツリーの え(した) ちがいが 3つ ある",''.join(s))
h=('<div class="sh"><h2>ちがいさがし ツリー<small>3つ みつけよう</small></h2>'
 '<div style="flex:1;min-height:0;display:flex;flex-direction:column;justify-content:space-around;gap:2cqw">'
 +scene(True)+scene(False)+
 '</div><div class="foot"><span>みつけたら ○を つけよう</span><i></i></div></div>')
open("content/sheets/t-diff-xmas.html","w").write(h)
