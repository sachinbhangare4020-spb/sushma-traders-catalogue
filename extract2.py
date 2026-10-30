src=open('extract.py').read().split('# ---------- DROOLS')[0]
exec(src)
products=json.load(open(S+'work/p1.json'))
def norm(s):return re.sub(r'[^a-z0-9]','',s.lower())
seen=set()
# ---------- ABRO
def cat_abro(n,label):
    n=n.upper()
    if re.search(r'TAPE|GHB|MASKER|ZORROGUARD',n):return 'Tapes'
    if re.search(r'BOND|ADHESIVE|SEAL|FOAM|FIX|SPRAY & SEAL|FILL',n):return 'Adhesives & Sealants'
    if re.search(r'WHEEL|DISC|ABRASIVE|PAPER|CLOTH',n):return 'Abrasives'
    if re.search(r'ZORROFIT|HANDLE|LIFT',n):return 'Hardware fittings'
    if label=='Auto':return 'Car care'
    return 'Hardware & Industrial'
for pat,label in (('40682b95','Auto'),('71e2fbfc','Hardware')):
    d=op(pat)
    for pi,p in enumerate(d):
        dd=p.get_text('dict');H=[];Lines=[]
        for b in dd['blocks']:
            if b['type']!=0:continue
            for l in b['lines']:
                sp=[s for s in l['spans'] if s['text'].strip()]
                if not sp:continue
                t=' '.join(s['text'].strip() for s in sp)
                Lines.append((l['bbox'],t,sp[0]['color'],sp[0]['size']))
        hd=[(bb,t) for bb,t,c,sz in Lines if c==0xffffff and re.match(r'(AIPL )?(ABRO|ZORRO)',t) and sz>8.5]
        hd.sort(key=lambda h:(h[0][1]))
        blocks=[]
        for bb,t in hd:
            # gather continuation lines
            name=t;y=bb[3]
            for bb2,t2,c2,sz2 in sorted(Lines,key=lambda l:l[0][1]):
                if c2==0xffffff and abs(bb2[0]-bb[0])<6 and 0<bb2[1]-y<6 and not re.match(r'(AIPL )?(ABRO|ZORRO)',t2) and sz2>8.5:
                    name+=' '+t2;y=bb2[3]
            blocks.append(dict(x0=bb[0],y0=bb[1],y1=y,name=name))
        for b in blocks:
            below=[o['y0'] for o in blocks if abs(o['x0']-b['x0'])<90 and o['y0']>b['y0']+10]
            yb=min(below) if below else p.rect.height-45
            xl,xr=b['x0']-10,b['x0']+172
            txt=[(bb,t,c) for bb,t,c,sz in Lines if xl<=bb[0]<xr and b['y1']-1<=bb[1]<yb-2 and c!=0xffffff]
            bullets=[];parts=[]
            for bb,t,c in sorted(txt,key=lambda z:z[0][1]):
                if t.startswith('∙'):bullets.append(t.lstrip('∙ ').strip())
                elif t.startswith('PART NO'):parts.append([t[8:].strip(),''])
                elif parts and not parts[-1][1] and re.search(r'/CASE|\bml\b|OZ|mm|\bg\b',t,re.I):parts[-1][1]=t
                elif bullets and bb[0]-xl<20 and not re.search(r'PART|CASE',t) and len(bullets[-1])<90 and c==0x231f20:bullets[-1]+=' '+t
            imgs=[]
            for im in p.get_image_info(xrefs=True):
                x0,y0,x1,y1=im['bbox'];w,h=x1-x0,y1-y0
                if w<26 or h<30 or w>300 or h>300:continue
                if 158<w<176 and 225<h<252:continue
                xc,yc=(x0+x1)/2,(y0+y1)/2
                if xl<=xc<xr and b['y1']<yc<yb:imgs.append((w*h,im['xref'],(x0,y0,x1,y1)))
            nm=re.sub(r'^(AIPL )?(ABRO|ZORRO)®?\s*(& AIPL ZORRO )?','',b['name']).replace('®','').replace('™','').strip()
            if nm=='' or len(nm)<3:continue
            title=('Zorro ' if b['name'].startswith('AIPL ZORRO') and not nm.upper().startswith('ZORRO') else '')+nm.title().replace('Pvc','PVC').replace('Ab-80','AB-80').replace('Pu ','PU ').replace('Ghb','GHB').replace('Ptfe','PTFE')
            k=norm(title)
            if k in seen:continue
            seen.add(k)
            if not imgs:
                continue
            imgs.sort(reverse=True)
            fn=f'ab_{pat[:3]}_{pi}_{abs(hash(k))%9999}.jpg'
            try:im=xref_img(d,imgs[0][1])
            except Exception:continue
            products.append(dict(brand='ABRO',cat=cat_abro(nm,label),name=title,variants=[dict(size=(q[1] or '').replace('  ',' '),part=q[0]) for q in parts] or [],bullets=bullets[:4],img=save(sq(im),fn),page=f'{label} brochure p{pi+1}'))
print('after abro',len(products))
# ---------- DOCTOR
d=op('24f21a6c')
DOC=[(1,(77,182,165,294),'Doctor Ultra Detergent Powder','Detergent powder','Floral fresh fragrance. Sizes: 5 kg, 3 kg, 1 kg and ₹10 pack.'),
(1,(266,181,353,294),'Doctor Washing Powder','Detergent powder','Everyday washing powder for cotton and daily wear.'),
(1,(166,373,254,490),'Doctor Advanced Detergent Powder','Detergent powder','Advanced formula detergent powder.'),
(2,(53,157,205,208),'Doctor Green Laundry Soap','Laundry soap','Laundry bar. Works well in hard (khara) water.'),
(2,(233,157,385,208),'Doctor Double Action Soap','Laundry soap','Double action laundry bar. Works well in hard water.'),
(2,(74,267,182,345),'Doctor Superfine Soap','Laundry soap','Laundry soap bar for everyday washing.'),
(2,(271,244,348,345),'Doctor Hi-Power Soap','Laundry soap','Hi-Power laundry soap, 1 kg box pack.'),
(2,(53,419,205,491),'Doctor Shuddh Soap','Laundry soap','Pure laundry soap bar.'),
(2,(237,439,388,490),'Doctor Premium Soap','Laundry soap','Premium laundry soap bar.'),
(3,(136,137,283,273),'Doctor Clean Dishwash Tub','Dishwash','Lemon dishwash paste in a tub.'),
(3,(110,378,309,473),'Doctor Clean Dishwash Bar','Dishwash','Lemon dishwash bar for utensils.'),
(4,(77,137,169,295),'Doctor Clean Dishwash Liquid','Dishwash','Power of lemon dishwash liquid.'),
(4,(255,149,364,311),'Doctor Care Liquid Detergent','Liquid detergent','Fresh breeze fragrance, colour safe technology. Soft and bright clothes.'),
(4,(40,420,200,495),'Doctor Advanced Detergent Cake','Detergent cake','Advanced care detergent cake, 25 g extra pack.'),
(4,(225,415,390,495),'Doctor Blue Detergent Cake','Detergent cake','New Doctor Blue cake, 25% extra.')]
for pi,bx,n,c,desc in DOC:
    p=d[pi];im=clip_img(p,bx,zoom=5);fn=f'doc_{abs(hash(n))%9999}.jpg'
    products.append(dict(brand='Doctor',cat=c,name=n,variants=[],bullets=[desc],img=save(sq(im),fn),page=f'Doctor profile p{pi+1}'))
print('after doctor',len(products))
# ---------- SHINE LINE (CUMI)
d=op('d4f71d5a')
for pi in range(2,6):
    p=d[pi];heads=[]
    for b in p.get_text('dict')['blocks']:
        if b['type']!=0:continue
        for l in b['lines']:
            for s in l['spans']:
                if 'Rogue' in s['font'] and s['text'].strip():heads.append((l['bbox'],s['text'].strip()))
    heads.sort(key=lambda h:(h[0][1],h[0][0]))
    rows={}
    for bb,t in heads:rows.setdefault(round(bb[1]/10),[]).append((bb,t))
    for k,v in rows.items():
        v.sort(key=lambda z:z[0][0]);bb=v[0][0];name=v[0][1].title();sub=' '.join(z[1] for z in v[1:]).title()
        # description text: first MrEaves line block right of image after heading
        desc=[];
        for b in p.get_text('dict')['blocks']:
            if b['type']!=0:continue
            for l in b['lines']:
                t=' '.join(s['text'] for s in l['spans']).strip()
                if l['bbox'][0]>320 and bb[1]<l['bbox'][1]<bb[1]+95 and t and not t.isupper():desc.append(t)
        fn=f'sh_{pi}_{k}.jpg'
        im=clip_img(p,(30,bb[3]+4,322,bb[3]+176),zoom=3.5)
        products.append(dict(brand='CUMI',cat='Shine Line (auto-body)',name='Shine Line '+name,variants=[],bullets=[' '.join(desc)[:170]] if desc else [],sub=sub,img=save(im,fn,640),page=f'Shine Line p{pi+1}'))
print('after shine',len(products))
# ---------- VINI
d=op('b94adc5c')
VINI=[(3,'Fogg Men Body Spray 120 ml','Men fragrance',[('120 ml',225)],'No gas, only perfume liquid. Marco, Imperial, Royal, Napoleon, Majestic, Victor, Monarch.'),
(4,'Fogg Women Body Spray 120 ml','Women fragrance',[('120 ml',225)],'No gas. Delicious, Essence, Paradise, Radiate.'),
(5,'Fogg Men Body Spray 65 ml','Men fragrance',[('65 ml',150)],'Marco, Napoleon, Royal, Majestic, Paradise.'),
(6,'Fogg Mobile Pack 25 ml','Men fragrance',[('25 ml',85)],'Pocket packs: Amaze, Charm, Happy, Nice, Relish, Dash.'),
(7,'Fogg Mobile Pack 25 ml (Force, Punch, Rush)','Men fragrance',[('25 ml',85)],'Strong fragrances in a carry pack.'),
(8,'Fogg Master Men 125 ml','Men fragrance',[('125 ml',250)],'Agar, Oak, Cedar, Pine. Long-lasting, office-ready.'),
(9,'Fogg Fantastic 150 ml','Men fragrance',[('150 ml',275)],'Sweet and musky: Extreme, Dynamic, Absolute.'),
(10,'Fogg Fine Men 120 ml','Men fragrance',[('120 ml',275)],'Mild fragrances: Bay Breeze, Brazilian Burst, Fizzy Dew, Rio Wave.'),
(11,'Fogg Fine Women 120 ml','Women fragrance',[('120 ml',275)],'Mild fragrances: Breeze, Peaceful, Spring, You & Me.'),
(12,'Fogg Black Men 120 ml','Men fragrance',[('120 ml',299)],'Party fragrances: Fresh Aromatic, Woody, Aqua, Spicy, Fougere, Oriental.'),
(14,'Fogg Scent Eau de Parfum','Men fragrance',[('50 ml',399),('75 ml',499),('100 ml',650)],'Impressio, Xpressio, Xtremo, Intensio.'),
(15,'Fogg Scent Everyday','Men fragrance',[('15 ml',99),('30 ml',140)],'Sultan, Tycoon, Czar, Prince.'),
(17,'WhiteTone Face Powder','Skin care',[('30 g',65),('50 g',85),('70 g',115)],'Oil-free look, even tone, radiant skin in 2 minutes.'),
(18,'WhiteTone Face Cream','Skin care',[('25 g',75),('50 g',140)],'Oil-free look, even tone, radiant skin.'),
(20,'Glam-Up Glomatic Cream','Skin care',[('25 g',99)],'Moisturising light makeup cream for a special glow.'),
(22,'Real Man Deodorant 200 ml','Men fragrance',[('200 ml',299)],'Long lasting deodorant: Attract, Thrill, Fresh Spirit, Fresh Mood.'),
(24,'Ossum Perfumed Body Mist 115 ml','Women fragrance',[('115 ml',275)],'All-day perfume for women: Blossom, Delight, Romance, Pleasure.'),
(25,'Ossum Perfume Spray 25 ml','Women fragrance',[('25 ml',85)],'Teaser, Desire, Appeal, Cherish.'),
(26,'Kloze Advance Razors','Grooming',[('Advance 3',299),('Advance 5',375)],'Get a perfect shave in the first shave. 1 handle, 2 cartridges.')]
for pi,n,c,vs,desc in VINI:
    p=d[pi];r=p.rect
    im=clip_img(p,(0,r.height*0.13,r.width,r.height*0.93),zoom=2.4)
    fn=f'vi_{pi}.jpg';products.append(dict(brand='Vini',cat=c,name=n,variants=[dict(size=s,mrp=m) for s,m in vs],bullets=[desc],img=save(im,fn,760),page=f'Vini p{pi+1}'))
print('total',len(products))
json.dump(products,open(S+'work/all.json','w'),ensure_ascii=False,indent=1)
from collections import Counter;print(Counter((p['brand']) for p in products))
