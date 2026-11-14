from pathlib import Path
from docx import Document
from docx.oxml.ns import qn
r=Path('E:/BT1/output/word')
d=Document(r/'Chuong_3_DA_XOA_CAC_DONG_DUMMY_TRO_XUONG.docx')
removed=False
for p in list(d.paragraphs):
 if p.text.startswith('Bảng 3.7 Ví dụ lỗi'):
  n=p._p.getnext()
  assert n.tag==qn('w:tbl')
  n.getparent().remove(n)
  p._p.getparent().remove(p._p);removed=True
 elif p.text.startswith(('Giải thích ví dụ đầu:','Phạm vi ví dụ:')):
  p._p.getparent().remove(p._p)
assert removed
for p in d.paragraphs:
 if p.text.startswith('Bảng 3.8 Tổng hợp'):
  for run in p.runs:run.text=run.text.replace('Bảng 3.8','Bảng 3.7')
out=r/'Chuong_3_DA_BO_BANG_VI_DU.docx';d.save(out)
c=Document(out)
assert not any('Ví dụ lỗi từ validation' in p.text for p in c.paragraphs)
assert any(p.text=='3.7 Tổng hợp và đánh giá cuối' for p in c.paragraphs)
print(out);print('Tables:',len(c.tables))
