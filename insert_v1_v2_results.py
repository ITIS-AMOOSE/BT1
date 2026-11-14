from pathlib import Path
from docx import Document
from docx.shared import Cm,Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
r=Path('E:/BT1/output/word');d=Document(r/'Chuong_3_NLP_VIET_TIEP_THEO_V1.docx')
target=next(p for p in d.paragraphs if p.text=='3.5.6 Nhận xét về thực nghiệm V2')
p=d.add_paragraph('Bảng so sánh kết quả trên tập xác thực V1 và V2 (đơn vị %)',style='Caption')
p.paragraph_format.keep_with_next=True;target._p.addprevious(p._p)
t=d.add_table(rows=2,cols=7);t.autofit=False
widths=[4.6]+[1.92]*6
for i,w in enumerate(widths):t.columns[i].width=Cm(w)
for i,title in [(0,'Mô hình'),(1,'Macro-F1'),(3,'F1-toxic'),(5,'Recall-toxic')]:
 if i==0:t.cell(0,0).merge(t.cell(1,0)).text=title
 else:t.cell(0,i).merge(t.cell(0,i+1)).text=title;t.cell(1,i).text='V1';t.cell(1,i+1).text='V2'
data=[['BoW + Naive Bayes','64,49','74,05','32,56','51,06','25,30','44,44'],['TF-IDF + Naive Bayes','49,50','59,36','2,35','21,88','1,20','12,96'],['BoW + SVM','66,29','75,82','36,49','54,35','32,53','46,30'],['TF-IDF + SVM','67,10','74,67','40,00','52,17','54,22','44,44'],['SVM cải tiến','68,86','78,83','42,33','60,38','48,19','59,26'],['PhoBERT','68,88','78,88','42,05','60,55','44,58','61,11']]
for values in data:
 row=t.add_row()
 for i,(c,value) in enumerate(zip(row.cells,values)):c.text=value;c.width=Cm(widths[i])
seen=set()
for j,row in enumerate(t.rows):
 trpr=row._tr.get_or_add_trPr();e=OxmlElement('w:cantSplit');trpr.append(e)
 if j<2:e=OxmlElement('w:tblHeader');trpr.append(e)
 for i,c in enumerate(row.cells):
  if c._tc in seen:continue
  seen.add(c._tc);c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
  pr=c._tc.get_or_add_tcPr();b=OxmlElement('w:tcBorders')
  for edge in ['top','bottom','left','right']:
   e=OxmlElement('w:'+edge);e.set(qn('w:val'),'single');e.set(qn('w:sz'),'4');e.set(qn('w:color'),'D9D9D9');b.append(e)
  pr.append(b)
  if j<2:e=OxmlElement('w:shd');e.set(qn('w:fill'),'E7E6E6');pr.append(e)
  margin=OxmlElement('w:tcMar')
  for edge,val in [('top','85'),('bottom','85'),('left','85'),('right','85')]:
   e=OxmlElement('w:'+edge);e.set(qn('w:w'),val);e.set(qn('w:type'),'dxa');margin.append(e)
  pr.append(margin)
  for p in c.paragraphs:
   p.paragraph_format.line_spacing=1.05;p.paragraph_format.space_after=Pt(3);p.paragraph_format.space_before=Pt(3)
   p.alignment=WD_ALIGN_PARAGRAPH.LEFT if i==0 and j>=2 else WD_ALIGN_PARAGRAPH.CENTER
   for run in p.runs:run.font.name='Times New Roman';run.font.size=Pt(11);run.bold=j<2
target._p.addprevious(t._tbl)
p=d.add_paragraph(style='List Paragraph');p.paragraph_format.space_before=Pt(12);p.add_run('Nhận xét: ').bold=True
p.add_run('Macro-F1 và F1-toxic của tất cả mô hình đều tăng ở V2. Tuy nhiên, Recall-toxic của TF-IDF + SVM giảm từ 54,22% xuống 44,44%, cho thấy điểm tổng hợp cao hơn chưa chắc đồng nghĩa phát hiện được nhiều toxic hơn. Hai phiên bản sử dụng tập xác thực khác nhau nên bảng mang tính đối chiếu; chưa thể quy toàn bộ thay đổi cho việc tăng dữ liệu huấn luyện.')
target._p.addprevious(p._p)
out=r/'Chuong_3_NLP_CO_BANG_SO_SANH_V1_V2.docx';d.save(out)
c=Document(out);assert len(c.tables)==1 and len(c.tables[0].rows)==8 and len(c.inline_shapes)==12
print(out)
