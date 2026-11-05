# Builds courses.json (every course and professor in the given grade reports) from reports/*.pdf.
# Usage: python3 scripts/build_course_index.py courses.json [RECENT_TERM]   e.g. 20253 = Fall 2025
import subprocess, re, glob, json, sys, os
SEM={'SPRING':1,'SUMMER':2,'FALL':3}
RECENT=int(sys.argv[2]) if len(sys.argv)>2 else 0
row=re.compile(r'^([A-Z]{4})-(\d{3})-(\w{3})\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+([\d.]+)?\s*(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s*(.*)$')
depts={}; courses={}; profs={}
from collections import Counter, defaultdict
dc=defaultdict(Counter)
files=sorted(glob.glob('reports/*.pdf'))
for f in files:
    y,s,c=os.path.basename(f)[:-4].split('-',2); term=int(y)*10+SEM[s]
    txt=subprocess.run(['pdftotext','-layout',f,'-'],capture_output=True,text=True).stdout
    dept=None
    for line in txt.splitlines():
        m=re.match(r'\s*DEPARTMENT:\s+(.+?)\s{2,}',line+'  ')
        if m: dept=m.group(1).strip(); continue
        m=row.match(line.strip())
        if not m: continue
        code=m.group(1)+' '+m.group(2)
        graded=int(m.group(9)); prof=m.group(17).strip()
        if dept: dc[m.group(1)][dept]+=graded+1
        e=courses.setdefault(code,{'t':0,'n':0})
        if term>e['t']: e['t']=term
        if term>=RECENT: e['n']+=graded
        if prof: profs.setdefault(prof,set()).add(code)
depts={k:v.most_common(1)[0][0].title().replace(' And ',' and ').replace(' Of ',' of ').replace(' & ',' & ') for k,v in sorted(dc.items())}
out={'depts':depts,'courses':{k:[v['n'],v['t']] for k,v in sorted(courses.items())},'profs':{k:sorted(v) for k,v in sorted(profs.items())}}
s=json.dumps(out,separators=(',',':'))
open(sys.argv[1],'w').write(s)
print(len(files),'pdfs',len(depts),'depts',len(courses),'courses',len(profs),'profs',len(s),'bytes')
print({k:depts[k] for k in list(depts)[:8]}, out['courses'].get('CHEM 107'), out['profs'].get('JOHNSON R'))
