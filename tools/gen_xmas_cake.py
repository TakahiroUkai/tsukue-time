# ぬりえ クリスマスケーキ(太い線)
import math
def star(cx,cy,R,r):
    pts=[]
    for i in range(10):
        a=-math.pi/2+i*math.pi/5
        rr=R if i%2==0 else r
        pts.append("%.1f %.1f"%(cx+rr*math.cos(a),cy+rr*math.sin(a)))
    return '<path class="tk" d="M'+'L'.join(pts)+'Z"/>'
s=[]
# candles (behind cream)
for x in (38,62):
    s.append('<rect class="tk" x="%d" y="34" width="6" height="22"/>'%(x-3))
    s.append('<path class="tk" d="M%d 20 Q%d 27 %d 31 Q%d 27 %d 20Z"/>'%(x,x-5,x,x+5,x))
    s.append('<path class="nf th" d="M%d 40 L%d 44 M%d 47 L%d 51"/>'%(x-3,x+3,x-3,x+3))
# plate
s.append('<ellipse class="tk" cx="50" cy="102" rx="46" ry="7"/>')
# cake body
s.append('<path class="tk" d="M14 62 V92 Q14 98 20 98 H80 Q86 98 86 92 V62 Z"/>')
s.append('<path class="nf th" d="M14 80 H86"/>')
for x in (26,38,50,62,74):
    s.append('<circle class="tk" cx="%d" cy="89" r="3.6"/>'%x)
# cream top
s.append('<path class="tk" d="M12 62 Q12 52 22 52 H78 Q88 52 88 62 Q84 71 79 64 Q75 73 69 64 Q64 73 58 64 Q52 73 46 64 Q41 73 35 64 Q30 73 24 64 Q19 71 12 62Z"/>')
# strawberries
for x in (26,50,74):
    s.append('<g transform="translate(%d 46)"><path class="tk" d="M-9 -6 Q0 -11 9 -6 Q10 5 0 13 Q-10 5 -9 -6Z"/>'
             '<path class="tk" d="M-6 -7 L-3 -11 L0 -8 L3 -11 L6 -7Z"/>'
             '<circle class="fb" cx="-3" cy="0" r=".9"/><circle class="fb" cx="3" cy="0" r=".9"/><circle class="fb" cx="0" cy="5" r=".9"/></g>'%x)
# stars and snow
s.append(star(12,12,6,2.8)); s.append(star(88,12,6,2.8))
for x,y in((24,6),(76,6),(8,30),(92,30),(50,8),(20,24),(80,24)):
    s.append('<circle class="tk" cx="%d" cy="%d" r="1.8"/>'%(x,y))
h=('<div class="sh"><h2>ぬりえ クリスマスケーキ<small>すきな いろで ぬってね</small></h2><div class="art">'
 '<svg class="art-svg" viewBox="0 0 100 112" role="img" aria-label="ぬりえ クリスマスケーキ">'+''.join(s)+'</svg></div>'
 '<div class="foot"><span>なまえ</span><i></i></div></div>')
open("content/sheets/s-xmas-cake.html","w").write(h)
