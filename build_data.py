import json,re,shutil,os
S='/tmp/claude-0/-home-claude/b008c9cb-7809-58d7-80d4-e19a16ab45c1/scratchpad/'
P=json.load(open(S+'work/all2.json'))
DROP={'Shampoo For Dog & Cat','Drools Toy For Dog'}
REN={'Fpcus Pup Booster':'Focus Pup Booster','Daily Nurition Pup Booster':'Daily Nutrition Pup Booster','Daily Nurition Gravy Dog':'Daily Nutrition Gravy Dog',
"Let'S Bite Kitten":"Let's Bite Kitten","Let'S Bite Cat Active Adult":"Let's Bite Cat Active Adult","Let'S Bite Persian":"Let's Bite Persian",
'Ultium  Performance':'Drools Ultium Performance','Puppy Optimum Performance':'Drools Puppy Optimum Performance (Bulk)','Adult Optimum Performance':'Drools Adult Optimum Performance (Bulk)',
'Mackerel':'PurePet Cat Adult Mackerel','Sea Food':'PurePet Cat Adult Sea Food','Pets':'Absolute Syrup (Pets)','Absolute Syrup':'Absolute Syrup (Cat/Dog)',
'Skin + Coat':'Absolute Tablets Skin + Coat','Vitamins':'Absolute Tablets Vitamins','Calcium':'Absolute Tablets Calcium','Digestion':'Absolute Tablets Digestion','Immunity':'Absolute Tablets Immunity','Mobility':'Absolute Tablets Mobility',
'Calcium Small':'Absolute Calcium Milk Bone Small','Calcium Medium':'Absolute Calcium Milk Bone Medium','Calcium Large':'Absolute Calcium Milk Bone Large',
'Cat Real Chicken In Gravy            Cat Real Tuna In Gravy':'Cat Real Chicken / Tuna In Gravy','Absolute Calcium Milk Bone':'Absolute Calcium Milk Bone Combo',
'Foaming Tire':'Foaming Tire Cleaner','Zorro Bopp Packing Tape/':'Zorro BOPP Packing Tape','Pro Synth Sw-30 Sn/Cf':'Pro Synth SW-30 SN/CF Engine Oil','Fuel Injector':'Fuel Injector Cleaner',
'Aluminium Oxide Fibre Discs':'Zorro Aluminium Oxide Fibre Discs','Zorrofit - Inno Box Zts-Innobox':'Zorrofit Inno Box','Zorrofit - Hydraulic Lift-Up':'Zorrofit Hydraulic Lift-Up','Zorro Bond-Sr 798':'Zorro Bond SR 798','Windshield Washer':'Windshield Washer Concentrate','Diesel Injector':'Diesel Injector Cleaner','Zorroseal':'Zorroseal PVC Cement'}
jar={'Milk Flavor':1,'100% Veg':1,'Chicken Flavor':1,'Mutton Flavor':1}
out=[];cnt={}
def tosize(s):
    s=re.sub(r'\s+','',s.lower()).replace('gm','g').replace('pcs','pcs')
    m=re.match(r'^(\d+(?:\.\d+)?)kg$',s)
    if m and float(m.group(1))>=50:s=m.group(1)+'g'
    return s
def wt(s):
    m=re.match(r'(\d+(?:\.\d+)?)(kg|g|ml|pcs)',s)
    if not m:return 1e9
    v=float(m.group(1));u=m.group(2);return v*(1000 if u=='kg' else 1)
for idx,p in enumerate(P):
    n=p['name'].strip()
    if p['brand']=='Drools':
        n=re.sub(r'\s+',' ',n)
        if n in DROP:continue
        if idx in(40,41,42):n='PurePet Biscuits '+n.replace(' Flavor','')
        elif idx in(43,44,45,46):n='PurePet Biscuits '+n.replace(' Flavor','')+' (Jar)'
        if idx==39:n='Drools Biscuits Dog Chicken & Egg'
        n=REN.get(n,n)
        n=n.replace('Drools Drools','Drools')
        vs=[]
        for v in p['variants']:
            s=tosize(v['size']);m=v['mrp']
            if re.match(r'^\d+(\.\d+)?g$',s) and float(s[:-1])<50 and m>800:s=s[:-1]+'kg'
            vs.append(dict(label=s,mrp=m))
        if n=='Maxi Adult Dog & Cat':vs=[dict(label='20kg (Dog)',mrp=2900),dict(label='20kg (Cat)',mrp=3400)]
        seen=set();u=[]
        for v in vs:
            k=(v['label'],v['mrp'])
            if k in seen:continue
            seen.add(k);u.append(v)
        u.sort(key=lambda v:wt(v['label']))
        low=n.lower()
        cat=('Treats & health' if re.search(r'biscuit|treat|bone|stick|dent|sausage|laddi|baked|chew|munchy|calcium|syrup|tablet|vitamin|milk',low) else
             'Cat food' if re.search(r'cat|kitten|kitty|bite|litter|persian|ocean fish|mackerel|tuna|sea food|real chicken',low) else 'Dog food')
        if 'absolute' in low:cat='Treats & health'
        p=dict(p,name=n,variants=u,cat=cat)
        if n in([o['name'] for o in out]):
            for o in out:
                if o['name']==n:
                    ks={(v['label'],v['mrp']) for v in o['variants']}
                    for v in u:
                        if (v['label'],v['mrp']) not in ks:o['variants'].append(v)
                    o['variants'].sort(key=lambda v:wt(v['label']))
            continue
    elif p['brand']=='ABRO':
        n=REN.get(n,n)
        vs=[]
        for v in p['variants']:
            lab=re.sub(r'\s+',' ',v['size']).strip();lab=re.sub(r'\s*\d+/CASE','',lab).strip() or v['part']
            vs.append(dict(label=lab,mrp=None,part=v['part']))
        p=dict(p,name=n,variants=vs)
    else:
        p=dict(p,name=REN.get(n,n),variants=[dict(label=v['size'],mrp=v['mrp']) for v in p['variants']])
    out.append(p)
# Doctor sizes
for p in out:
    if p['name']=='Doctor Ultra Detergent Powder':p['variants']=[dict(label=s,mrp=None) for s in('1 kg','3 kg','5 kg','₹10 pack')]
for i,p in enumerate(out):p['id']='p%03d'%i
BR=[
dict(id='doctor',name='Doctor',tag='Soaps · Detergents · Dishwash',by='Pee Cee Cosma Sope Ltd., Agra',color='#1d8a3a',ink='#ffffff',gst=18),
dict(id='drools',name='Drools',tag='Pet food, treats and health',by='Drools Pet Food',color='#c8183a',ink='#ffffff',gst=18),
dict(id='abro',name='ABRO',tag='Car care, tapes, adhesives, hardware',by='AIPL Group',color='#0d5ea8',ink='#ffffff',gst=18),
dict(id='cumi',name='CUMI',tag='Jawan, Ajax, Tezz, Concord, Shine Line',by='Carborundum Universal Ltd.',color='#0a6fb7',ink='#ffffff',gst=18),
dict(id='vini',name='Vini',tag='Fogg, WhiteTone, Ossum, Kloze',by='Vini Cosmetics',color='#1aa6b8',ink='#ffffff',gst=18)]
V=[dict(id='v1',file='media/v1.mp4',poster='media/v1.jpg',title='Channel Spray fixes stuck windows',match='Channel Spray'),
dict(id='v2',file='media/v2.mp4',poster='media/v2.jpg',title='Microfiber cloth demo',match='Premium Cleaning Cloth'),
dict(id='v3',file='media/v3.mp4',poster='media/v3.jpg',title='Engine losing power? Oil treatment',match='Premium Oil Treatment'),
dict(id='v4',file='media/v4.mp4',poster='media/v4.jpg',title='Throttle Body and Carb Cleaner',match='Carb & Choke Cleaner'),
dict(id='v5',file='media/v5.mp4',poster='media/v5.jpg',title='AB-80 Spray Lubricant',match='AB-80 Spray'),
dict(id='v6',file='media/v6.mp4',poster='media/v6.jpg',title='PU Foam Insulation Sealant',match=''),
dict(id='v7',file='media/v7.mp4',poster='media/v7.jpg',title='Complete car care range',match=''),
dict(id='v8',file='media/v8.mp4',poster='media/v8.jpg',title='ABRO 6123 masking tape',match=''),
dict(id='v9',file='media/v9.mp4',poster='media/v9.jpg',title='Motor Flush clears sludge',match='Motor Flush')]
os.makedirs(S+'site',exist_ok=True)
json.dump(dict(brands=BR,videos=V,products=out),open(S+'site/products.json','w'),ensure_ascii=False,separators=(',',':'))
from collections import Counter
print(len(out),Counter(p['brand'] for p in out),Counter(p['cat'] for p in out if p['brand']=='Drools'))
print(os.path.getsize(S+'site/products.json')//1024,'KB')
used={p['img'] for p in out}
for f in os.listdir(S+'site/img'):
    if 'img/'+f not in used:os.remove(S+'site/img/'+f)
