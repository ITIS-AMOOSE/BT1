from pathlib import Path
import json,csv,math
from PIL import Image,ImageDraw,ImageFont
from docx import Document
from docx.shared import Cm,Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
R=Path('E:/BT1');O=R/'output/word';A=O/'v1_five_models';A.mkdir(exist_ok=True)
data=json.loads((R/'reports/resplit_v1/final_evaluation/results.json').read_text(encoding='utf-8'))
order=[('bow_nb','BoW + Naive Bayes'),('tfidf_nb','TF-IDF + Naive Bayes'),('bow_svm','BoW + SVM'),('tfidf_svm','TF-IDF + SVM')]
records=[]
for key,name in order:
 m=next(x for x in data['models'] if x['model']==key)['validation'];records.append((key,name,[m[x] for x in ['tn','fp','fn','tp']]))
records.append(('phobert','PhoBERT V1 tại ngưỡng 0,52',[1138,56,46,37]))
def metrics(cm):
 tn,fp,fn,tp=cm;p=tp/(tp+fp);r=tp/(tp+fn);f=2*tp/(2*tp+fp+fn);f0=2*tn/(2*tn+fp+fn)
 return [(tn+tp)/sum(cm),p,r,f,(f+f0)/2]
def ft(n):return ImageFont.truetype('C:/Windows/Fonts/arial.ttf',n)
def center(dr,x,y,text,n=30,color='#18344D'):
 box=dr.textbbox((0,0),text,font=ft(n));dr.text((x-(box[2]-box[0])/2,y),text,font=ft(n),fill=color)
for key,name,cm in records:
 assert sum(cm)==1277 and cm[0]+cm[1]==1194 and cm[2]+cm[3]==83
 im=Image.new('RGB',(1350,1050),'white');dr=ImageDraw.Draw(im)
 center(dr,675,28,name,40);center(dr,675,88,'Validation V1 | 1.277 bình luận | 83 toxic',28)
 center(dr,780,157,'Nhãn dự đoán',30)
 for k,lab in enumerate(['Non-toxic (0)','Toxic (1)']):
  center(dr,530+360*k,210,lab,29);center(dr,140,430+360*k,lab,27)
 for i in range(2):
  for j in range(2):
   value=cm[i*2+j];ratio=value/1194;x=350+j*360;y=280+i*300
   rgb=(int(235-180*ratio),int(243-130*ratio),int(251-85*ratio))
   dr.rectangle((x,y,x+360,y+300),fill=rgb,outline='white',width=5)
   color='white' if ratio>.65 else '#18344D'
   center(dr,x+180,y+85,str(value),65,color);center(dr,x+180,y+175,[['TN','FP'],['FN','TP']][i][j],33,color)
 center(dr,675,930,'Hàng là nhãn thật; cột là nhãn dự đoán.',28)
 center(dr,675,980,'Các ô hiển thị số bình luận; cùng thang màu cho năm mô hình.',25)
 # True-label row names aligned to the cell centers.
 # Remove the earlier row-label positions and redraw on a white margin.
 dr.rectangle((0,275,340,900),fill='white')
 center(dr,160,410,'Non-toxic (0)',27);center(dr,160,710,'Toxic (1)',27)
 im.save(A/(key+'_cm.png'),dpi=(220,220))
# Reuse the validated chart layout, limiting its series to these five models.
namespace={}
code=(R/'add_result_figures.py').read_text(encoding='utf-8').split("v1=j(")[0]
exec(code,namespace)
namespace['A']=A
vals=[metrics(c) for _,_,c in records]
chart=namespace['bars']('v1_five_models.png','V1 So sánh bốn baseline và PhoBERT','Cùng tập xác thực 1.277 câu | PhoBERT dùng ngưỡng 0,52',
 ['BoW\nNaive Bayes','TF-IDF\nNaive Bayes','BoW\nSVM','TF-IDF\nSVM','PhoBERT'],
 [('Macro-F1',[m[4]*100 for m in vals]),('F1-toxic',[m[3]*100 for m in vals]),('Recall-toxic',[m[2]*100 for m in vals])])
(A/'verified_metrics.json').write_text(json.dumps([{'model':n,'tn':c[0],'fp':c[1],'fn':c[2],'tp':c[3],'accuracy':m[0],'precision_toxic':m[1],'recall_toxic':m[2],'f1_toxic':m[3],'macro_f1':m[4],'basis':'REPORT V1 confusion counts' if k=='phobert' else 'V1 validation metrics in final_evaluation/results.json'} for (k,n,c),m in zip(records,vals)],ensure_ascii=False,indent=2),encoding='utf-8')
d=Document(O/'Chuong_3_CO_GIOI_THIEU_MO_HINH.docx')
def find(prefix):return next(p for p in d.paragraphs if p.text.startswith(prefix))
def text(p,value):
 for run in list(p.runs):run._element.getparent().remove(run._element)
 if ': ' in value:
  a,b=value.split(': ',1);p.add_run(a+': ').bold=True;p.add_run(b)
 else:p.add_run(value)
text(find('3.4.4 '),'3.4.4 Chọn cấu hình và ngưỡng phân loại')
text(find('Chuyển điểm thành nhãn:'),'Chọn ngưỡng phân loại: SVM giữ ranh giới quyết định mặc định bằng 0. Với PhoBERT V1, nhóm khảo sát các ngưỡng trên tập xác thực và chọn 0,52 theo Macro-F1. Ngưỡng này được giữ để tạo nhãn trong bước đánh giá.')
text(find('Theo dõi huấn luyện:'),'Theo dõi và đánh giá huấn luyện: Với bốn baseline, nhóm đánh giá trên tập xác thực sau khi huấn luyện xong mỗi cấu hình. PhoBERT được huấn luyện tối đa 5 lượt; sau mỗi lượt, nhóm đánh giá và lưu trạng thái có Macro-F1 tốt nhất. Năm lượt học là quá trình cùng mô hình học tiếp trên dữ liệu, không phải năm mô hình độc lập.')
ev=find('Bước 6 – Đối chiếu kết quả:')
extra=d.add_paragraph(style='List Bullet');text(extra,'Tạo nhãn dự đoán: Dùng các cấu hình đã chọn để dự đoán tập xác thực. Naive Bayes chọn lớp có xác suất ước lượng cao hơn; SVM phân loại theo ranh giới điểm 0; PhoBERT gán toxic khi điểm từ 0,52 trở lên. Sau đó ghép dự đoán với nhãn thật của đúng bình luận.')
ev._p.addprevious(extra._p)
text(ev,'Tính và trình bày kết quả: Từ nhãn thật và nhãn dự đoán, nhóm tính Accuracy, Precision, Recall, F1-toxic và Macro-F1 cho bốn baseline và PhoBERT. Kết quả được trình bày trong một bảng, một biểu đồ so sánh chung và năm ma trận nhầm lẫn riêng.')
# Replace only the V1 results table; other versions retain their tables.
old=d.tables[0];t=d.add_table(rows=1,cols=6);t.autofit=False
heads=['Mô hình','Accuracy','Precision toxic','Recall toxic','F1 toxic','Macro-F1']
tablevals=[[name.replace(' tại ngưỡng 0,52','')]+[f'{x*100:.2f}'.replace('.',',') for x in m] for (_,name,_),m in zip(records,vals)]
for row,values in [(t.rows[0],heads)]+[(t.add_row(),v) for v in tablevals]:
 for i,(c,v) in enumerate(zip(row.cells,values)):
  c.width=Cm(4.7 if i==0 else 2.36);c.text=v
  for p in c.paragraphs:
   p.paragraph_format.line_spacing=1.05;p.paragraph_format.space_before=Pt(5);p.paragraph_format.space_after=Pt(5)
   if i:p.alignment=WD_ALIGN_PARAGRAPH.CENTER
   for run in p.runs:run.font.size=Pt(10)
  pr=c._tc.get_or_add_tcPr();bo=OxmlElement('w:tcBorders')
  for ed in ['top','bottom','left','right']:
   e=OxmlElement('w:'+ed);e.set(qn('w:val'),'single');e.set(qn('w:sz'),'4');e.set(qn('w:color'),'D9D9D9');bo.append(e)
  pr.append(bo)
for c in t.rows[0].cells:
 e=OxmlElement('w:shd');e.set(qn('w:fill'),'E7E6E6');c._tc.get_or_add_tcPr().append(e)
 for run in c.paragraphs[0].runs:run.bold=True
e=OxmlElement('w:tblHeader');t.rows[0]._tr.get_or_add_trPr().append(e)
old._tbl.addprevious(t._tbl);old._tbl.getparent().remove(old._tbl)
text(find('Bảng 3.2 Kết quả'),'Bảng 3.2 Kết quả bốn baseline và PhoBERT V1 đơn vị phần trăm')
# Remove the former V1 chart/matrix and their comments; keep every figure from V2/V3.
start=find('Hình 3.7 ');prev=start._p.getprevious();assert prev.findall('.//'+qn('w:drawing'))
end=find('3.5 Thực nghiệm V2')._p
node=prev
while node is not end:
 nxt=node.getnext();node.getparent().remove(node);node=nxt
target=find('3.5 Thực nghiệm V2')
def figure(path,caption,comment):
 p=d.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.paragraph_format.space_before=Pt(10);p.paragraph_format.keep_with_next=True
 p.add_run().add_picture(str(path),width=Cm(16));target._p.addprevious(p._p)
 p=d.add_paragraph(caption,style='Caption');p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.paragraph_format.keep_with_next=True;target._p.addprevious(p._p)
 p=d.add_paragraph(style='List Bullet');p.add_run('Nhận xét: ').bold=True;p.add_run(comment);target._p.addprevious(p._p)
figure(chart,'So sánh kết quả của bốn baseline và PhoBERT trên tập xác thực V1',
 'PhoBERT đạt Macro-F1 khoảng 68,88%, cao nhất trong năm mô hình của hình. TF-IDF + SVM có Recall-toxic 54,22%, cao hơn PhoBERT 44,58%, nhưng tạo nhiều báo nhầm hơn. Vì vậy, cần đọc đồng thời các chỉ số.')
comments=[
'Mô hình phát hiện đúng 21 trong 83 câu toxic, bỏ sót 62 câu và báo nhầm 25 câu non-toxic. Recall-toxic thấp cho thấy mô hình còn bỏ qua nhiều toxic.',
'Mô hình chỉ phát hiện đúng 1 trong 83 câu toxic, dù Accuracy đạt khoảng 93,50%. Kết quả minh họa việc dự đoán chủ yếu non-toxic có thể tạo Accuracy cao trên dữ liệu mất cân bằng.',
'Mô hình phát hiện đúng 27 câu toxic, bỏ sót 56 câu và báo nhầm 38 câu non-toxic. So với BoW + Naive Bayes, số phát hiện đúng tăng nhưng báo nhầm cũng tăng.',
'Mô hình phát hiện đúng 45 câu toxic, cao nhất trong năm mô hình, nhưng báo nhầm 97 câu non-toxic. Recall cao hơn đi kèm Precision thấp hơn.',
'Tại ngưỡng 0,52, mô hình phát hiện đúng 37 câu toxic, bỏ sót 46 câu và báo nhầm 56 câu non-toxic. Hình được dựng từ ma trận ghi trong báo cáo V1, không dùng bảng dự đoán V2 hiện nằm trong thư mục PhoBERT.']
for (key,name,cm),comment in zip(records,comments):
 figure(A/(key+'_cm.png'),'Ma trận nhầm lẫn '+name+' trên tập xác thực V1',comment)
# Match an explicit old V1 summary now that all five models are tabulated.
for p in d.paragraphs:
 if p.text.startswith('Nhận xét: TF-IDF + SVM có Macro-F1 cao nhất trong bốn baseline'):
  text(p,'Nhận xét: TF-IDF + SVM có Macro-F1 cao nhất trong bốn baseline, đạt 67,10%. PhoBERT đạt 68,88% theo số liệu V1. Các hình dưới đây trình bày cả kết quả tổng hợp lẫn số báo nhầm và bỏ sót của từng mô hình.')
n=5
for p in d.paragraphs:
 if p.style.name=='Caption' and not p.text.startswith('Bảng '):
  n+=1;cap=p.text
  if cap.startswith('Hình '):cap=cap.split(' ',2)[2]
  p.text=f'Hình 3.{n} {cap}';p.alignment=WD_ALIGN_PARAGRAPH.CENTER
out=O/'Chuong_3_V1_DU_5_MO_HINH_VA_CONFUSION_MATRIX.docx';d.save(out)
check=Document(out)
assert len(check.inline_shapes)==16,(len(check.inline_shapes))
assert len(check.tables[0].rows)==6
assert len(check.tables[0].columns)==6
print(out);print('16 figures preserved/updated. V1: five models, six metrics columns, five individual matrices and one comparison chart.')
