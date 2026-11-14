from pathlib import Path
from docx import Document
r=Path('E:/BT1/output/word')
d=Document(r/'Chuong_3_DA_BO_BANG_VI_DU.docx')
prefixes=('Lưu ý về OOF:','PhoBERT: Checkpoint','SVM cải tiến:','Hướng tiếp theo:','Lý do làm V3:','Nguồn:')
in_sources=False;removed=[]
for p in list(d.paragraphs):
 text=p.text.strip()
 if text=='Nguồn số liệu':in_sources=True
 if in_sources or text.startswith(prefixes):
  removed.append(text);p._p.getparent().remove(p._p)
 elif text.startswith('Mô hình:'):
  for run in p.runs:run.text=run.text.replace('SVM cải tiến; ','')
out=r/'Chuong_3_DA_SUA_THEO_GOP_Y.docx';d.save(out)
check=Document(out)
assert not any(p.text.strip().startswith(prefixes) for p in check.paragraphs)
assert not any(p.text=='Nguồn số liệu' for p in check.paragraphs)
assert len(check.inline_shapes)==9
assert len(check.tables)==7
print('Removed',len(removed),'paragraphs; preserved 9 figures and 7 tables.')
print(out)
