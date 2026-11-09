"""Original editorial figures following cathrynlavery/diagram-design guidance."""
from pathlib import Path
from html import escape as esc

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/diagrams'
OUT.mkdir(parents=True,exist_ok=True)
PAPER,INK,MUTED,ACCENT,RULE='#faf9f6','#202936','#58616b','#3659a8','#d9d9d4'
FONTS='https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Geist:wght@400;500;600&family=Geist+Mono:wght@400;500&display=swap'

def text(x,y,s,size=16,fill=INK,weight=400,kind='sans',anchor='start',italic=False):
    family={'sans':"'Geist',system-ui,sans-serif",'serif':"'Instrument Serif',Georgia,serif",'mono':"'Geist Mono',ui-monospace,monospace"}[kind]
    return f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"'+(' font-style="italic"' if italic else '')+'>'+esc(s)+'</text>'

def rule(x1,y1,x2,y2,color=RULE):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="1"/>'

def arrow(d,dashed=False):
    return f'<path d="{d}" fill="none" stroke="{MUTED}" stroke-width="1.2" marker-end="url(#arrow)"'+(' stroke-dasharray="5,4"' if dashed else '')+'/>'

def node(x,y,w,h,tag,name,lines=(),kind='normal'):
    fill={'normal':'#fff','focal':'#edf0f7','optional':'#f1f1ee','external':'#f0f0ed'}[kind]
    color=ACCENT if kind=='focal' else MUTED
    s=f'<g data-node="{esc(name)}"><rect x="{x-4}" y="{y-4}" width="{w+8}" height="{h+8}" fill="{PAPER}"/>'
    s+=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{color}" stroke-width="1"'+(' stroke-dasharray="4,3"' if kind=='optional' else '')+'/>'
    s+=text(x+20,y+24,tag,8,color,500,'mono')+text(x+20,y+52,name,16,ACCENT if kind=='focal' else INK,600)
    for i,t in enumerate(lines):s+=text(x+20,y+76+i*20,t,12,MUTED,400,'mono')
    return s+'</g>'

def chrome(kicker,title):
    return text(48,40,kicker,8,MUTED,500,'mono')+text(48,96,title,40,INK,400,'serif')+rule(48,120,1232,120)

def footer(left,right):
    return rule(48,656,1232,656)+text(48,684,left,12,MUTED,400,'mono')+text(1232,684,right,12,MUTED,400,'mono','end')

def save(slug,title,desc,body):
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" role="img" aria-labelledby="{slug}-title {slug}-desc"><title id="{slug}-title">{esc(title)}</title><desc id="{slug}-desc">{esc(desc)}</desc><defs><marker id="arrow" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="{MUTED}"/></marker></defs><rect width="1280" height="720" fill="{PAPER}"/>{body}</svg>'''
    css='*{box-sizing:border-box}body{margin:0;padding:24px;background:'+PAPER+';color:'+INK+'}main{max-width:1280px;margin:auto}.diagram-container{width:100%;overflow-x:auto}svg{width:100%;min-width:1280px;display:block}@media print{.diagram-container{overflow:visible}svg{min-width:0}}'
    html=f'''<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)}</title><link href="{esc(FONTS,quote=True)}" rel="stylesheet"><style>{css}</style></head><body><main><div class="diagram-container">{svg}</div></main></body></html>'''
    (OUT/(slug+'.html')).write_text(html,encoding='utf-8')

b=chrome('DEVFLOW KIT / 01 / ARCHITECTURE','Specialized guidance. One coherent workflow.')
b+=arrow('M312 360 H424')+arrow('M692 360 H876')+arrow('M560 312 V240')+arrow('M560 408 V488')
b+=arrow('M428 384 H368 Q360 384 360 392 V536 Q360 544 352 544 H316',True)+arrow('M188 312 V240',True)
b+=arrow('M640 312 V280 Q640 272 648 272 H1032 Q1040 272 1040 264 V240')
b+=node(880,132,320,104,'TECHNICAL VISUALS','Diagram Design',['Architecture + workflows','Editable HTML / SVG / PNG'])
b+=node(64,132,248,104,'EXTERNAL / OPTIONAL','Reference systems',['Catalog, APIs, products','License + fit checked'],'external')
b+=node(408,132,324,104,'DESIGN / FOUR SKILLS','UI craft',['Frontend Design + UI/UX Pro Max','Taste + UI Taste'])
b+=node(64,312,248,96,'EXECUTION OWNER','Your AI harness',['Reads files; invokes tools'])
b+=node(428,312,264,96,'COORDINATION','devflow',['Scope + lifecycle routing'],'focal')
b+=node(880,312,320,96,'PROJECT ARTIFACTS','A verifiable result',['Specs, mock, code, evidence'])
b+=node(408,492,324,104,'ENGINEERING / TWO SKILLS','Build with discipline',['Superpowers: 15 profiles','Ponytail: focused changes'])
b+=node(64,492,248,104,'COMMUNICATION / OPT-IN','Caveman',['Concise replies on request'],'optional')
b+=text(880,520,'The agent runs in your host.',14,INK,400,'serif',italic=True)+text(880,548,'Markdown is guidance, not a service.',14,INK,400,'serif',italic=True)
b+=text(880,584,'Missing tools stay explicit.',12,MUTED)
b+=footer('SOLID  routing    DASHED  optional extension','9 COMPONENTS / 1 ROUTER')
save('architecture','DevFlow Kit architecture','The harness reads the devflow router, selects design or engineering guidance, optionally uses references and Caveman, and produces project artifacts.',b)

b=chrome('DEVFLOW KIT / 02 / DEVELOPMENT FLOW','From an open question to an accepted outcome.')
xs=[228,432,636,840,1044]
stages=['Understand','Specify','Prototype','Implement','Verify & accept']
for i in range(4):b+=arrow(f'M{xs[i]+152} 192 H{xs[i+1]-20}')
for i,(x,label) in enumerate(zip(xs,stages)):
    b+=text(x,164,f'0{i+1}',8,MUTED,500,'mono')+text(x,192,label,16,ACCENT if i==2 else INK,600)
    if i==2:b+=rule(x,212,x+156,212,ACCENT)
    if i<4:b+=rule(x+176,240,x+176,572)
for y,label in [(276,'WORK'),(388,'CONSTRAINT'),(500,'OUTPUT')]:b+=text(48,y,label,8,MUTED,500,'mono')
for y in (316,428,572):b+=rule(48,y,1232,y)
cells=[
    [('Clarify the need','Compare references'),('Check fit, rights','and feasibility'),('Brief + shortlist','Known assumptions')],
    [('Define scope','and behavior'),('Make acceptance','criteria explicit'),('Specification','and test criteria')],
    [('Build clickable UI','Review and refine'),('Keep approved','brand and stack'),('Interactive mock','Accepted direction')],
    [('Reverse if needed','Build agreed scope'),('Use only authorized','observable behavior'),('Working system','and focused tests')],
    [('Run real checks','Record acceptance'),('Separate technical','and human sign-off'),('Evidence + decision','Open limitations')]
]
for x,rows in zip(xs,cells):
    for y,lines in zip((264,376,488),rows):
        for j,t in enumerate(lines):b+=text(x,y+j*24,t,16,INK if y==264 else MUTED)
b+=text(48,612,'Small fix? Enter at the relevant stage. Reuse approved decisions; verify the affected interaction.',14,INK,400,'serif',italic=True)
b+=footer('REVERSE IS OPTIONAL / MOCK DATA IS NOT A BACKEND','REQUIREMENTS → ACCEPTANCE')
save('workflow','DevFlow Kit development flow','Five phases group requirements and references, specifications, interactive mock and feedback, optional reverse and implementation, then verification and acceptance.',b)

b=chrome('DEVFLOW KIT / 03 / DISTRIBUTION','One complete capsule. Your choice of harness.')
b+=arrow('M352 336 H476')+arrow('M720 336 H844')
b+=node(64,252,288,168,'PORTABLE PACKAGE','devflow/',['SKILL.md','bundle/ — nine components','Integrity manifests'])
b+=node(480,280,240,112,'COPY + VERIFY','Installer',['Select one target','Preserve existing content'],'focal')
b+=f'<rect x="848" y="176" width="352" height="336" rx="6" fill="#fff" stroke="{MUTED}" stroke-width="1"/>'+text(872,208,'HARNESS / PROJECT SKILLS ROOT',8,MUTED,500,'mono')
for i,(name,folder) in enumerate([('Codex','.agents/skills'),('Claude Code','.claude/skills'),('DeepSeek Harness','.dsh/skills'),('Trae / Trae CN','.trae/skills'),('Other hosts','explicit skills root')]):
    y=248+i*52
    b+=text(872,y,name,16,INK,600)+text(872,y+20,folder,12,MUTED,400,'mono')
    if i<4:b+=rule(872,y+32,1176,y+32)
b+=text(64,496,'Preserve the whole capsule.',14,INK,400,'serif',italic=True)+text(64,524,'Sibling policies and resources travel together.',14,INK,400,'serif',italic=True)+rule(64,568,1200,568)
for x,n,label in [(64,'01','Copy checked'),(304,'02','Discovered'),(544,'03','Activated'),(784,'04','Executed'),(1024,'05','Verified')]:
    b+=text(x,600,n,8,MUTED,500,'mono')+text(x,624,label,16,INK,600)
b+=footer('INSTALLATION ≠ MODEL EXECUTION / VERIFY EACH STEP','5 NAMED TARGETS + GENERIC')
save('portability','DevFlow Kit portable installation','The installer copies one complete devflow capsule into a selected harness, with separate file, discovery, activation, execution and outcome checks.',b)

print('Wrote three technical diagram HTML/SVG sources in docs/diagrams/.')
