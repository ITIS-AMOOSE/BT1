from pathlib import Path
from docx import Document
root=Path('E:/BT1/output/word')
src=root/'Chuong_3_tu_3_4_co_bieu_do.docx'
d=Document(src)
keep={'BoW + NB','BoW + SVM','TF-IDF + NB','TF-IDF + SVM'}
for t in d.tables[:2]:
 for row in list(t.rows)[1:]:
  if row.cells[0].text.strip() not in keep:
   t._tbl.remove(row._tr)
out=root/'Chuong_3_DA_XOA_CAC_DONG_DUMMY_TRO_XUONG.docx'
d.save(out)
check=Document(out)
for i,t in enumerate(check.tables[:2]):
 names=[row.cells[0].text for row in t.rows[1:]]
 assert set(names)==keep and len(names)==4
 print('Table',i+1, names)
print(out)
