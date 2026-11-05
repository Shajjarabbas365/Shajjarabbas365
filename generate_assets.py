import math, random
from html import escape
F="Consolas,Menlo,'Courier New',monospace"
CW=0.6
def svg(w,h,body,defs='',style=''):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="{F}">
<defs><pattern id="sl" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#fff" opacity=".05"/></pattern>
<filter id="g" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>{defs}</defs>
<style>{style}@keyframes bl{{50%{{opacity:0}}}}.cur{{animation:bl 1s steps(1) infinite}}</style>
<rect width="{w}" height="{h}" fill="#000"/>{body}<rect width="{w}" height="{h}" fill="url(#sl)"/></svg>'''
def save(n,s): open(f'assets/{n}.svg','w',encoding='utf-8').write(s)
def ext(text,x,y,size,depth=7,anchor='start',tid='t',ls=2,weight=700):
    t=escape(text)
    d=f'<text id="{tid}" x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" letter-spacing="{ls}" text-anchor="{anchor}">{t}</text>'
    out=[]
    for i in range(depth,0,-1):
        c=int(35+(depth-i)*22)
        out.append(f'<use href="#{tid}" x="{i}" y="{i}" fill="rgb({c},{c},{c})"/>')
    out.append(f'<use href="#{tid}" fill="#fff"/>')
    return d, ''.join(out)
def brackets(w,h,m=10,l=18):
    p=f'M{m} {m+l}V{m}H{m+l} M{w-m-l} {m}H{w-m}V{m+l} M{m} {h-m-l}V{h-m}H{m+l} M{w-m-l} {h-m}H{w-m}V{h-m-l}'
    return f'<path d="{p}" fill="none" stroke="#fff" stroke-width="2"/>'
def slab(x,y,w,h,layers=6,step=1.6):
    s=''
    for i in range(layers,0,-1):
        c=int(30+(layers-i)*26)
        s+=f'<rect x="{x+i*step:.1f}" y="{y+i*step:.1f}" width="{w}" height="{h}" fill="rgb({c},{c},{c})"/>'
    return s
def window(x,y,w,h,title,layers=6):
    s=slab(x,y,w,h,layers)
    s+=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#050505" stroke="#fff" stroke-width="2"/>'
    s+=f'<rect x="{x}" y="{y}" width="{w}" height="32" fill="#fff"/>'
    for i in range(3): s+=f'<rect x="{x+14+i*20}" y="{y+11}" width="10" height="10" fill="#000" opacity="{1-i*.3:.1f}"/>'
    s+=f'<text x="{x+84}" y="{y+22}" font-size="14" font-weight="700" fill="#000">{escape(title)}</text>'
    return s

# ---------- cube ----------
def proj(pts,cx,cy,ay,ax,d=420):
    out=[]
    for x,y,z in pts:
        x1=x*math.cos(ay)+z*math.sin(ay); z1=-x*math.sin(ay)+z*math.cos(ay)
        y2=y*math.cos(ax)-z1*math.sin(ax); z2=y*math.sin(ax)+z1*math.cos(ax)
        f=d/(d+z2); out.append((cx+x1*f,cy+y2*f))
    return out
def cube_frames(s,cx,cy,sign,n=32):
    pts=[(a*s,b*s,c*s) for a in(-1,1) for b in(-1,1) for c in(-1,1)]
    ed=[(i,j) for i in range(8) for j in range(i+1,8) if bin(i^j).count('1')==1]
    fr=[]
    for k in range(n+1):
        ay=sign*(math.pi/2)*k/n+0.5; p=proj(pts,cx,cy,ay,0.45)
        fr.append(''.join(f'M{p[i][0]:.1f} {p[i][1]:.1f}L{p[j][0]:.1f} {p[j][1]:.1f}' for i,j in ed))
    return fr
def animpath(fr,dur,stroke,sw,op=1,flt=''):
    return f'<path d="{fr[0]}" fill="none" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" opacity="{op}" {flt}><animate attributeName="d" dur="{dur}s" repeatCount="indefinite" values="{";".join(fr)}"/></path>'

# ---------- hero ----------
def hero():
    W,H=860,380; random.seed(7); rain=''
    for i in range(26):
        x=14+i*33; n=10; chars=''.join(
          f'<tspan x="{x}" dy="16" fill-opacity="{0.08+0.92*(k/(n-1))**2:.2f}">{escape(random.choice("01<>/{}$#"))}</tspan>' for k in range(n))
        rain+=f'<text y="0" font-size="14" fill="#fff" style="animation:fall {random.uniform(7,14):.1f}s linear {-random.uniform(0,12):.1f}s infinite">{chars}</text>'
    floor=''; hz=322; vx=430
    for i in range(-14,15): floor+=f'<line x1="{vx+i*8}" y1="{hz}" x2="{vx+i*75}" y2="{H}"/>'
    for t in [0.05,0.15,0.3,0.5,0.75,1.0]: floor+=f'<line x1="0" y1="{hz+(H-hz)*t**1.6:.1f}" x2="{W}" y2="{hz+(H-hz)*t**1.6:.1f}"/>'
    d1,u1=ext('SHAJJAR',48,160,78,8,tid='a'); d2,u2=ext('ABBAS',48,238,78,8,tid='b')
    c1=animpath(cube_frames(78,690,150,1),4,'#fff',1.8,1,'filter="url(#g)"')
    c2=animpath(cube_frames(40,690,150,-1),4,'#888',1.4)
    body=f'''<g opacity=".2">{rain}</g><g stroke="#fff" stroke-opacity=".22" stroke-width="1">{floor}</g>
<ellipse cx="690" cy="262" rx="70" ry="9" fill="#fff" opacity=".09"/>{c1}{c2}
<text x="48" y="58" font-size="16" fill="#9a9a9a">root@shajjar:~# whoami<tspan class="cur" fill="#fff"> █</tspan></text>
<defs>{d1}{d2}</defs>{u1}{u2}
<text x="48" y="282" font-size="15" fill="#e6e6e6">Full Stack Developer  /  Full Stack AI Developer  /  Computer Engineer</text>
<text x="48" y="306" font-size="13" fill="#777">&gt; access granted<tspan class="cur" fill="#fff">_</tspan></text>
{brackets(W,H)}'''
    save('hero',svg(W,H,body,style='@keyframes fall{from{transform:translateY(-200px)}to{transform:translateY(400px)}}'))

# ---------- typing ----------
def typing():
    W,H=860,64; T=4.6; lines=["Full Stack Developer","Full Stack AI Developer","Building Modern Web Applications","I think I am funny :)"]
    C=T*len(lines); body=f'<rect x="1" y="1" width="{W-2}" height="{H-2}" fill="#050505" stroke="#444"/><text x="22" y="40" font-size="22" font-weight="700" fill="#777">$</text>'
    defs=''; fs=22; cw=fs*CW
    for i,l in enumerate(lines):
        n=len(l); a=i*T; ev=[(0,0)]
        if a>0: ev.append((a,0))
        for k in range(1,n+1): ev.append((a+0.15+1.6*k/n,k))
        end=a+0.15+1.6+1.9
        for k in range(n-1,-1,-1): ev.append((end+0.5*(n-k)/n,k))
        ev=[(min(t,C-0.01),k) for t,k in ev]
        kt=';'.join(f'{t/C:.4f}' for t,_ in ev)
        ww=';'.join(f'{k*cw:.1f}' for _,k in ev); xx=';'.join(f'{58+k*cw:.1f}' for _,k in ev)
        oo=';'.join('0' if k==0 and t<=a or t>=end+0.5-0.001 and k==0 else '1' for t,k in ev)
        defs+=f'<clipPath id="c{i}"><rect x="58" y="14" height="40" width="0"><animate attributeName="width" calcMode="discrete" dur="{C}s" repeatCount="indefinite" keyTimes="{kt}" values="{ww}"/></rect></clipPath>'
        body+=f'<text x="58" y="40" font-size="{fs}" font-weight="700" fill="#fff" clip-path="url(#c{i})">{escape(l)}</text>'
        body+=f'<rect x="58" y="22" width="{cw*0.9:.1f}" height="22" fill="#fff"><animate attributeName="x" calcMode="discrete" dur="{C}s" repeatCount="indefinite" keyTimes="{kt}" values="{xx}"/><animate attributeName="opacity" calcMode="discrete" dur="{C}s" repeatCount="indefinite" keyTimes="{kt}" values="{oo}"/></rect>'
    save('typing',svg(W,H,body,defs))

# ---------- ticker ----------
def ticker():
    W,H=860,64; items="HTML CSS JavaScript TypeScript React Next.js Node.js Express Python Django FastAPI TensorFlow PyTorch OpenCV MySQL PostgreSQL MongoDB Docker Git Linux Flutter Arduino".split()
    s="  //  ".join(items)+"  //  "; fs=18; L=len(s)*fs*CW
    t=lambda x,c,dy=0:f'<text x="{x}" y="{40+dy}" font-size="{fs}" font-weight="700" fill="{c}" textLength="{L:.0f}" lengthAdjust="spacing" xml:space="preserve">{escape(s)}</text>'
    g=''.join(t(k*L+dx,c,dy) for k in (0,1) for dx,dy,c in ((2.5,2.5,'#555'),(0,0,'#fff')))
    body=f'''<line x1="0" y1="8" x2="{W}" y2="8" stroke="#fff" stroke-width="2"/><line x1="0" y1="{H-8}" x2="{W}" y2="{H-8}" stroke="#fff" stroke-width="2"/>
<g><animateTransform attributeName="transform" type="translate" from="0 0" to="-{L:.0f} 0" dur="45s" repeatCount="indefinite"/>{g}</g>
<rect width="90" height="{H}" fill="url(#fl)"/><rect x="{W-90}" width="90" height="{H}" fill="url(#fr)"/>'''
    defs='<linearGradient id="fl"><stop offset="0" stop-color="#000"/><stop offset="1" stop-color="#000" stop-opacity="0"/></linearGradient><linearGradient id="fr"><stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000"/></linearGradient>'
    save('ticker',svg(W,H,body,defs))

# ---------- about ----------
def about():
    W,H=860,352; rows=[('$ whoami',1),('> Shajjar Abbas',0),('',2),('$ cat roles.txt',1),('> Full Stack Developer',0),('> Full Stack AI Developer',0),('> Computer Engineer',0),('',2),('$ echo $MISSION',1),('> Building modern web applications and AI-powered products.',0)]
    body=window(12,12,812,318,'shajjar@github: ~/about'); y=70
    for t,k in rows:
        if k!=2: body+=f'<text x="38" y="{y}" font-size="17" fill="{"#9a9a9a" if k else "#fff"}" font-weight="{400 if k else 700}">{escape(t)}</text>'
        y+=23
    body+=f'<text x="38" y="{y+2}" font-size="17" fill="#9a9a9a">$ <tspan class="cur" fill="#fff">█</tspan></text>'
    save('about',svg(W,H,body))

# ---------- section header ----------
def section(name,cmd,text):
    W,H=860,100; d,u=ext(text,6,78,46,6,tid='h')
    tw=len(text)*46*CW+6+2
    body=f'<text x="8" y="26" font-size="14" fill="#8a8a8a">{escape(cmd)}</text><defs>{d}</defs>{u}<line x1="{tw+34:.0f}" y1="64" x2="{W-10}" y2="64" stroke="#fff" stroke-width="2"/><line x1="{tw+34:.0f}" y1="72" x2="{W-10}" y2="72" stroke="#555" stroke-width="2" stroke-dasharray="6 6"/><rect x="{W-18}" y="56" width="18" height="24" fill="#fff"/>'
    save(name,svg(W,H,body))

# ---------- link buttons ----------
def button(name,label,mark,sub):
    W,H=418,108; fw,fh=396,82
    s=slab(4,4,fw,fh,8,1.5)
    s+=f'<rect x="4" y="4" width="{fw}" height="{fh}" fill="#f1f1f1"/><clipPath id="k"><rect x="4" y="4" width="{fw}" height="{fh}"/></clipPath>'
    s+=f'<g clip-path="url(#k)"><rect x="-60" y="0" width="40" height="120" fill="#fff" opacity=".9" transform="skewX(-20)"><animateTransform attributeName="transform" type="translate" additive="sum" from="0 0" to="560 0" dur="3.6s" repeatCount="indefinite"/></rect></g>'
    s+=f'<rect x="22" y="20" width="54" height="54" fill="#000"/><text x="49" y="59" font-size="30" font-weight="700" fill="#fff" text-anchor="middle">{mark}</text>'
    s+=f'<text x="94" y="47" font-size="28" font-weight="700" fill="#000">{label}</text><text x="94" y="68" font-size="13" fill="#555">{escape(sub)}</text>'
    s+=f'<path d="M370 36l14 10-14 10" fill="none" stroke="#000" stroke-width="3"/>'
    save(name,svg(W,H,s))

# ---------- skills ----------
def skills(name,title,items):
    W=860; fs=16; h=30; d=7; x0=36; xmax=W-52; rows=[[]]; x=x0
    for it in items:
        w=len(it)*fs*CW+30
        if x+w>xmax: rows.append([]); x=x0
        rows[-1].append((x,it,w)); x+=w+d+16
    rh=h+30; Hwin=32+30+len(rows)*rh+12; H=Hwin+34
    body=window(12,12,812,Hwin,f'~/skills/{title}  [{len(items)}]')
    for r,row in enumerate(rows):
        y=12+32+34+d+r*rh
        for x,it,w in row:
            body+=f'<polygon points="{x+w},{y} {x+w+d},{y-d} {x+w+d},{y+h-d} {x+w},{y+h}" fill="#7a7a7a"/><polygon points="{x},{y} {x+d},{y-d} {x+w+d},{y-d} {x+w},{y}" fill="#fff"/><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#e6e6e6"/><text x="{x+w/2}" y="{y+20}" font-size="{fs}" font-weight="700" fill="#000" text-anchor="middle">{escape(it)}</text>'
    save(name,svg(W,H,body))

# ---------- footer ----------
def footer():
    W,H=860,190; d,u=ext('THANKS FOR VISITING',430,76,46,7,'middle','f',1)
    fl=''.join(f'<line x1="{430+i*10}" y1="150" x2="{430+i*80}" y2="{H}"/>' for i in range(-14,15))+''.join(f'<line x1="0" y1="{150+40*t**1.6:.0f}" x2="{W}" y2="{150+40*t**1.6:.0f}"/>' for t in (.1,.3,.55,.8,1))
    body=f'<g stroke="#fff" stroke-opacity=".2">{fl}</g><defs>{d}</defs>{u}<text x="430" y="118" font-size="16" fill="#9a9a9a" text-anchor="middle">$ exit 0</text><text x="430" y="140" font-size="14" fill="#fff" text-anchor="middle">connection closed. see you in the next commit<tspan class="cur">_</tspan></text>{brackets(W,H)}'
    save('footer',svg(W,H,body))

hero();typing();ticker();about()
section('s_connect','> ./connect.sh','CONNECT WITH ME');section('s_tools','> ls ~/skills','LANGUAGES &amp; TOOLS'.replace('&amp;','&'))
button('linkedin','LinkedIn','in','/in/shajar-abbas');button('facebook','Facebook','f','open profile')
skills('skill_front','frontend','HTML5 CSS3 JavaScript TypeScript React Next.js Tailwind Bootstrap Redux Vite'.split())
skills('skill_back','backend','Node.js Express Django FastAPI Flask PHP Laravel REST GraphQL Socket.IO'.split())
skills('skill_lang','languages','Python JavaScript TypeScript C C++ Java PHP SQL Bash'.split())
skills('skill_mobile','mobile-games-iot','Flutter React-Native Dart Unity Arduino Raspberry-Pi ESP32 MQTT'.split())
skills('skill_ai','ai-ml-data','TensorFlow PyTorch scikit-learn OpenCV Pandas NumPy LangChain OpenAI-API HuggingFace Jupyter'.split())
skills('skill_db','databases','MySQL PostgreSQL MongoDB SQLite Redis Firebase Supabase'.split())
skills('skill_cloud','cloud-devops','Git GitHub-Actions Docker AWS Linux Nginx Vercel'.split())
footer()
