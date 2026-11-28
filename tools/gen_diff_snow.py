# ちがいさがし ゆきだるま(うえ・したで3つちがう)
# ちがい: ぼうしの はね / ボタンの かず / そらの おおきな ゆき
def scene(top):
    s=[]
    s.append('<rect class="nf" x="1" y="1" width="98" height="56" rx="3" stroke-width="1"/>')
    s.append('<path class="nf" d="M3 54H97" stroke-width="1"/>')
    # snowman (center)
    s.append('<circle cx="50" cy="42" r="11"/><circle cx="50" cy="24" r="8"/>')
    s.append('<circle class="fb" cx="47" cy="23" r="1"/><circle class="fb" cx="53" cy="23" r="1"/>')
    s.append('<path d="M50 24.8L55.5 26L50 27.2Z"/>')
    # hat
    s.append('<rect x="43" y="10" width="14" height="9"/><rect x="40" y="17.5" width="20" height="3"/>')
    if top: s.append('<path d="M57 11Q64 6 62 14Q60 10 57 14Z"/>')  # はね
    # scarf
    s.append('<rect x="41" y="30" width="18" height="3.4"/><rect x="55" y="33" width="4" height="8"/>')
    # buttons
    for y in ((37,42,47) if top else (37,42)):
        s.append('<circle class="fb" cx="50" cy="%d" r="1.1"/>'%y)
    # arms
    s.append('<path class="nf" d="M39.5 40L28 33M33 36.5L31 31"/><path class="nf" d="M60.5 40L72 33M67 36.5L69 31"/>')
    # small trees
    s.append('<path d="M14 50L22 36L30 50Z"/><path d="M16 42L22 31L28 42Z"/><rect x="21" y="50" width="2" height="4"/>')
    s.append('<path d="M78 50L85 38L92 50Z"/><path d="M80 43L85 33L90 43Z"/><rect x="84" y="50" width="2" height="4"/>')
    # big snowflake (top only)
    if top:
        s.append('<path class="nf" d="M12 8V20M6.8 11L17.2 17M6.8 17L17.2 11" stroke-width="1.4"/>')
    # snow
    for x,y in((26,8),(36,14),(70,8),(80,16),(92,10),(64,20),(6,28),(94,28),(30,24),(72,26)):
        s.append('<circle class="fb" cx="%d" cy="%d" r=".7"/>'%(x,y))
    return '<svg class="art-svg" viewBox="0 0 100 58" style="width:100%%;display:block" role="img" aria-label="%s">%s</svg>'%(
        "ゆきだるまの え(うえ)" if top else "ゆきだるまの え(した) ちがいが 3つ ある",''.join(s))
h=('<div class="sh"><h2>ちがいさがし ゆきだるま<small>3つ みつけよう</small></h2>'
 '<div style="flex:1;min-height:0;display:flex;flex-direction:column;justify-content:space-around;gap:2cqw">'
 +scene(True)+scene(False)+
 '</div><div class="foot"><span>みつけたら ○を つけよう</span><i></i></div></div>')
open("content/sheets/t-diff-snow.html","w").write(h)
