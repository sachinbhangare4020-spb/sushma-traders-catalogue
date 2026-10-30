import pymupdf,glob,re,json,io,os
from PIL import Image
A='/mnt/user-data/attachments/b008c9cb-7809-58d7-80d4-e19a16ab45c1/'
S='/tmp/claude-0/-home-claude/b008c9cb-7809-58d7-80d4-e19a16ab45c1/scratchpad/'
IMG=S+'site/img/'
def op(p):return pymupdf.open(glob.glob(A+p+'*')[0])
def save(im,name,maxd=560):
    im=im.convert('RGB');im.thumbnail((maxd,maxd));im.save(IMG+name,'JPEG',quality=82);return 'img/'+name
def xref_img(doc,xref):
    pix=pymupdf.Pixmap(doc,xref)
    if pix.colorspace and pix.colorspace.n>3: pix=pymupdf.Pixmap(pymupdf.csRGB,pix)
    try:
        sm=doc.extract_image(xref).get('smask',0)
    except Exception:sm=0
    im=Image.open(io.BytesIO(pix.tobytes('png'))).convert('RGBA')
    if sm:
        m=pymupdf.Pixmap(doc,sm);mi=Image.open(io.BytesIO(m.tobytes('png'))).convert('L').resize(im.size);im.putalpha(mi)
    bg=Image.new('RGBA',im.size,(255,255,255,255));bg.alpha_composite(im);return bg.convert('RGB')
def clip_img(page,box,zoom=4):
    pix=page.get_pixmap(matrix=pymupdf.Matrix(zoom,zoom),clip=pymupdf.Rect(*box),alpha=False)
    return Image.open(io.BytesIO(pix.tobytes('png')))
def trim(im,pad=6):
    from PIL import ImageChops
    bg=Image.new('RGB',im.size,(255,255,255));diff=ImageChops.difference(im,bg).convert('L').point(lambda v:255 if v>14 else 0)
    bb=diff.getbbox()
    if not bb:return im
    x0,y0,x1,y1=bb;return im.crop((max(0,x0-pad),max(0,y0-pad),min(im.width,x1+pad),min(im.height,y1+pad)))
def sq(im,s=520):
    im=trim(im);im.thumbnail((s,s));c=Image.new('RGB',(im.width+30,im.height+30),(255,255,255));c.paste(im,(15,15));return c
products=[]
# ---------- DROOLS
d=op('43093204')
for pi in range(1,24):
    p=d[pi];words=p.get_text('words')
    heads=[]
    for b in p.get_text('dict')['blocks']:
        if b['type']!=0:continue
        for l in b['lines']:
            sp=[s for s in l['spans'] if s['text'].strip()]
            if not sp:continue
            sz=max(s['size'] for s in sp)
            t=' '.join(s['text'].strip() for s in sp)
            if sz>=9.5 and not re.search(r'MRP|\d+\s?(g|kg|gm|ml|pcs)\b',t,re.I) and len(t)>3:
                bb=l['bbox'];heads.append((t,(bb[0]+bb[2])/2,bb[3]))
    mrps=[w for w in words if w[4].startswith('MRP')]
    groups={}
    for im in p.get_image_info(xrefs=True):
        x0,y0,x1,y1=im['bbox']
        if x1-x0<25 or y1-y0<40 or y0<60:continue
        xc=(x0+x1)/2
        cand=[m for m in mrps if abs((m[0]+m[2])/2+10-xc)<40 and y0-75<m[1]<y0+4]
        if not cand:continue
        m=max(cand,key=lambda m:m[1]);
        line=[w for w in words if abs(w[1]-m[1])<4 and w[0]>m[2]-2 and w[0]<m[2]+60]
        price=''.join(w[4] for w in sorted(line,key=lambda w:w[0]))
        pr=re.search(r'(\d[\d,]*)',price)
        if not pr:continue
        mrp=int(pr.group(1).replace(',',''))
        wl=[w for w in words if m[1]-24<w[1]<m[1]-6 and abs((w[0]+w[2])/2-(m[0]+m[2])/2-10)<32]
        size=' '.join(w[4] for w in sorted(wl,key=lambda w:w[0])).strip() or ''
        hs=[h for h in heads if h[2]<y0+5 and abs(h[1]-xc)<190]
        if not hs:continue
        h=min(hs,key=lambda h:(y0-h[2])+0.6*abs(h[1]-xc))
        groups.setdefault((h[0],round(h[1])),[]).append(dict(size=size,mrp=mrp,xref=im['xref'],area=(x1-x0)*(y1-y0),x=xc))
    for (t,hx),vs in groups.items():
        vs.sort(key=lambda v:v['x'])
        big=max(vs,key=lambda v:v['area'])
        fn=f'dr_{pi}_{abs(hash(t+str(hx)))%9999}.jpg'
        try:img=save(sq(xref_img(d,big['xref'])),fn)
        except Exception as e:continue
        products.append(dict(brand='Drools',cat=('Cat' if re.search(r'CAT|KITTY|KITTEN|WORLD',t,re.I) else 'Dog' if re.search(r'DOG|PUP|CANINE|FOCUS',t,re.I) else 'Pet care'),
            name=t.title().replace('Purepet','PurePet').replace('Vet-Pro','Vet-Pro'),variants=[dict(size=v['size'],mrp=v['mrp']) for v in vs],img=img,page=f'Drools p{pi+1}'))
print('drools',len(products))
# ---------- ABRO (auto + hardware)
for pat,label in (('40682b95','Auto'),('71e2fbfc','Hardware')):
    d=op(pat)
    for pi,p in enumerate(d):
        heads=[]
        for b in p.get_text('dict')['blocks']:
            if b['type']!=0:continue
            for l in b['lines']:
                for s in l['spans']:
                    if s['color']==0xffffff and re.match(r'(AIPL )?(ABRO|ZORRO)',s['text'].strip()) and s['size']>8.5:
                        heads.append((l['bbox'],s['text'].strip()))
        # merge continuation lines (same x, close y)
        hs=[]
        for bb,t in sorted(heads,key=lambda h:(round(h[0][0]/40),h[0][1])):
            if hs and abs(hs[-1][0][0]-bb[0])<6 and 0<bb[1]-hs[-1][0][3]<8 and False:pass
            hs.append((list(bb),t))
        print(label,pi+1,[h[1][:30] for h in hs])
json.dump(products,open(S+'work/p1.json','w'))
