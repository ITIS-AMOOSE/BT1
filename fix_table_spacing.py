from pathlib import Path
from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph
r=Path('E:/BT1/output/word')
d=Document(r/'Chuong_3_DA_SUA_THEO_GOP_Y.docx')
count=0
for table in d.tables:
 node=table._tbl.getnext()
 while node is not None and node.tag==qn('w:p'):
  p=Paragraph(node,d._body)
  if p.text.strip() or node.findall('.//'+qn('w:drawing')):
   p.paragraph_format.space_before=Pt(12)
   count+=1
   break
  node=node.getnext()
out=r/'Chuong_3_DA_CHINH_KHOANG_CACH_BANG.docx'
d.save(out)
check=Document(out)
assert len(check.tables)==7 and len(check.inline_shapes)==9
print('Added 12pt spacing after',count,'tables.');print(out)
