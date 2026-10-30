src=open('extract.py').read().split('# ---------- DROOLS')[0]
exec(src)
import shutil
P=json.load(open(S+'work/all.json'))
d=op('69349170')
R=[ # page idx, offset-less box in half-scale px, name, cat, bullets
(6,(370,60,515,215),'Sandmaster Deco Water Proof Sheets',['Tough grains ensure fast cutting action','Flexible bond suits sanding of curves and contours','Wet and dry use']),
(6,(370,255,515,410),'Warrior Plus Water Proof Sheets',['Premium grains give fast cut and uniform finish','Ideal for wall, auto after-marble polishing','Wet and dry use']),
(6,(370,465,515,630),'Ajax Sukha Sheets',['Unique design minimises dust loading','Tough grains for fast sanding and uniform finish','Thick paper backing gives better grip']),
(6,(385,660,520,820),'Appu Sukha Sheets',['Sharp grains enable fast sanding','Strong bond gives better area coverage','Flexible paper suits curves and contours']),
(7,(370,105,520,250),'CUMI Stearated Sheets',['Special coating on premium paper prevents clogging','Unique grain-bond combination for uniform cutting','Dry use']),
(7,(365,300,520,465),'CUMI CL 577+ Latex Sheets',['Premium grains for consistent scratch pattern','Flexible anti-slip paper for secure grip','For automotive applications, wet and dry']),
(7,(365,480,520,650),'CUMI CL 577 Latex Sheets',['Uniform surface finish with consistent scratch','Flexible anti-slip paper','Ideal for wood, walls and auto-body']),
(7,(365,660,520,820),'CUMI CL 577 Microfine Sheets',['Excellent surface finish with premium grains','Suitable for wet and dry sanding','Grits 800 to 2000 for automotive finishing']),
(11,(370,95,535,170),'Appu Plus Cloth Roll',['Sharp grains for fast cutting and high material removal','Special backing for better grip on contours','Dry use']),
(11,(370,230,535,300),'CUMI Flex Flexible Roll',['Uniform grain coating, excellent finish','Flexible, easy to use, good area coverage','Wet and dry use']),
(11,(370,415,535,490),'Sandmaster Paper Roll',['Improved technology for non-loading','Tough grains for fast action and high material removal','Dry use']),
(11,(370,565,535,640),'Ajax RMC Roll',['For light stock removal with excellent finish','Cloth backing and special bond for contour sanding on wood','Best for plywood and furniture sanding']),
(11,(370,705,535,790),'Jawan RMC Roll',['For light stock removal with excellent finish','Cloth backing and special bond for contour sanding on wood','Best for plywood and furniture sanding']),
(15,(320,270,515,430),'Concord Fibre Disc',['Fully coated disc with sharp grains for a fast cut','Special non-loading design prevents dust and black marks','Flexible backing follows curves and contours']),
(15,(320,460,515,625),'Tezz Fibre Disc',['Fully coated disc with sharp grains for a fast cut','Special non-loading design prevents dust and black marks','Sizes: 4 inch, 5 inch']),
(15,(320,655,515,820),'Shakti Fibre Disc',['Sharp grains for fast sanding and uniform finish','Flexible backing suits curves','Ideal for all types of wood']),
(16,(340,105,555,265),'Sandmaster NXT IDC Disc',['Designed for 20% faster performance and 20% better life','Sharp grains with increased cut-ability','Unique cross-cut design fits tightly on the backup pad']),
(16,(340,320,555,465),'Concord Plus IDC Disc',['Individually coated with tough grains for easy sanding','Strong backing for uniform finish and better coverage','Special design minimises dust and black marks']),
(16,(340,495,555,640),'Tezz Plus IDC Disc',['Individually coated with tough grains for fast, easy sanding','Strong backing for uniform finish','Prevents black marks']),
(16,(340,665,555,815),'Concord Flap Disc',['Tough grains for faster material removal','High-strength bond and tough backup pad','Thicker cloth for extended life']),
(28,(350,45,545,215),'CUMI Zon Red Ultra Thin Wheel',['Fast and smooth cutting action','Sharper grains deliver more cuts per wheel','Double fabric mesh for safety. 107 x 1 x 16 mm']),
(28,(350,240,545,410),'CUMI Black Ultra Thin Wheel',['Strong grains ensure fast cutting','Special resin bond reduces dust fumes','107 x 1 x 16 mm']),
(28,(350,435,545,600),'Concord Ultra Thin Wheel',['Strong grains deliver more cuts per wheel','Self-cooling bond reduces burn marks','107 x 1 x 16 mm']),
(28,(350,650,545,815),'CUMI Green Chopsaw DF',['Premium grains for precise cuts','Strong resin bond for more cuts per wheel','350 x 3 x 25.4 mm'])]
for pi,bx,n,bl in R:
    p=d[pi];b=[v*2 for v in bx]
    im=clip_img(p,b,zoom=1.0)
    fn=f'cu_{pi}_{abs(hash(n))%9999}.jpg'
    cat='Sanding sheets' if 'Sheet' in n else 'Sanding rolls' if 'Roll' in n else 'Sanding discs' if 'Disc' in n else 'Cutting wheels'
    P.append(dict(brand='CUMI',cat=cat,name=n,variants=[],bullets=bl,img=save(sq(im),fn),page='CUMI retail catalogue p%d'%(pi+1)))
# Doctor care liquid: use shop photo
im=Image.open(A+'81ab516b-image.jpg').crop((0,640,900,1140)) if os.path.exists(A+'81ab516b-image.jpg') else None
if im:
    for p in P:
        if p['name']=='Doctor Care Liquid Detergent':p['img']=save(im,'doc_care_photo.jpg',640)
json.dump(P,open(S+'work/all2.json','w'),ensure_ascii=False,indent=1)
print(len(P))
for p in P:
    if p['brand']=='ABRO':print(p['name'],'|',p['cat'],'|',p['variants'][:2],'|',p['bullets'][:1])
