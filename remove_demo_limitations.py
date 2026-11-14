from pathlib import Path
from docx import Document
r=Path('E:/BT1/output/word')
d=Document(r/'Chuong_3_DA_CHINH_KHOANG_CACH_BANG.docx')
inside=False;removed=0
for p in list(d.paragraphs):
 if p.text.startswith('3.8.2 Những điểm cần hoàn thiện trong giao diện'):inside=True
 elif inside and p.text.startswith('3.9 '):inside=False
 if inside:
  p._p.getparent().remove(p._p);removed+=1
assert removed==6,removed
out=r/'Chuong_3_DA_BO_MUC_3_8_2.docx';d.save(out)
c=Document(out)
assert not any(p.text.startswith('3.8.2') for p in c.paragraphs)
assert any(p.text.startswith('3.9 ') for p in c.paragraphs)
assert len(c.tables)==7 and len(c.inline_shapes)==9
print(out)
