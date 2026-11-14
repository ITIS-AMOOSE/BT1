from pathlib import Path
import csv,json,math
from PIL import Image,ImageDraw,ImageFont
from docx import Document
from docx.shared import Cm,Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

R=Path('E:/BT1');O=R/'output/word';A=O/'figures_results';A.mkdir(exist_ok=True)
def read(p):
 with open(R/p,encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def j(p):return json.loads((R/p).read_text(encoding='utf-8-sig'))
def font(n=30):return ImageFont.truetype('C:/Windows/Fonts/arial.ttf',n)
colors=['#2563A6','#29915E','#D77A16','#8B55A2']
def canvas(title,sub,height=920):
 im=Image.new('RGB',(1800,height),'white');dr=ImageDraw.Draw(im)
 dr.text((55,25),title,font=font(37),fill='#172B40');dr.text((55,80),sub,font=font(27),fill='#4A5568');return im,dr
def center(dr,x,y,t,n=27,fill='black'):
 box=dr.textbbox((0,0),t,font=font(n));dr.text((x-(box[2]-box[0])/2,y),t,font=font(n),fill=fill)
def save(im,name):im.save(A/name,dpi=(220,220));return A/name
def bars(name,title,sub,labels,series):
 im,dr=canvas(title,sub);x0,y0,x1,y1=150,170,1730,730
 for val in range(0,101,20):
  y=y1-val/100*(y1-y0);dr.line((x0,y,x1,y),fill='#DDE3EB',width=2);dr.text((70,y-15),str(val),font=font(25),fill='black')
 dr.text((55,125),'Điểm (%)',font=font(25),fill='black')
 step=(x1-x0)/len(labels);bw=min(65,step/(len(series)+1))
 for i,lab in enumerate(labels):
  cx=x0+step*(i+.5)
  for k,(key,vals) in enumerate(series):
   x=cx+(k-len(series)/2)*bw;v=vals[i];y=y1-v/100*(y1-y0)
   dr.rectangle((x,y,x+bw-8,y1),fill=colors[k]);center(dr,x+bw/2-4,y-35,f'{v:.1f}',23)
  for k,line in enumerate(lab.split('\n')):center(dr,cx,750+k*31,line,25)
 for k,(key,_) in enumerate(series):
  x=270+k*420;dr.rectangle((x,860,x+25,885),fill=colors[k]);dr.text((x+38,853),key,font=font(27),fill='black')
 return save(im,name)
def lines(name,title,sub,xs,series,xlabel,yr=(0,100),mark=None):
 im,dr=canvas(title,sub);l,t,r,b=155,185,1710,730
 def pos(x,y):return (l+(x-min(xs))/(max(xs)-min(xs))*(r-l),b-(y-yr[0])/(yr[1]-yr[0])*(b-t))
 for i in range(6):
  v=yr[0]+i*(yr[1]-yr[0])/5;y=pos(xs[0],v)[1];dr.line((l,y,r,y),fill='#DFE5EB',width=2);dr.text((45,y-15),f'{v:.2f}' if yr[1]<=1 else f'{v:.0f}',font=font(25),fill='black')
 ticks=xs if len(xs)<=6 else [min(xs)+(max(xs)-min(xs))*i/8 for i in range(9)]
 for x in ticks:
  px=pos(x,yr[0])[0];center(dr,px,745,f'{x:g}' if len(xs)<=6 else f'{x:.2f}',24)
 for k,(key,vals) in enumerate(series):
  pts=[pos(x,y) for x,y in zip(xs,vals)];dr.line(pts,fill=colors[k],width=6)
  if len(xs)<=6:
   for xx,yy in pts:dr.ellipse((xx-7,yy-7,xx+7,yy+7),fill=colors[k])
 if mark is not None:
  xx=pos(mark,yr[0])[0]
  for yy in range(t,b,20):dr.line((xx,yy,xx,yy+10),fill='#A62A28',width=3)
  center(dr,xx-80,140,f'Ngưỡng {mark:.2f}',25,fill='#A62A28')
 center(dr,930,790,xlabel,28)
 for k,(key,_) in enumerate(series):
  x=110+k*420;dr.line((x,865,x+40,865),fill=colors[k],width=6);dr.text((x+50,846),key,font=font(26),fill='black')
 return save(im,name)
def cm(name,title,sub,mats):
 im,dr=canvas(title,sub,height=890)
 for k,(label,counts) in enumerate(mats):
  left=230+k*820;top=290;size=240
  center(dr,left+240,155,label,31);center(dr,left+240,220,'Nhãn dự đoán',27)
  for i,lab in enumerate(['Non-toxic (0)','Toxic (1)']):
   center(dr,left+size*(i+.5),255,lab,25)
   dr.text((left-175,top+size*(i+.5)-15),lab,font=font(22),fill='black')
  for i in range(2):
   for z in range(2):
    value=counts[i*2+z];ratio=value/max(counts);color=(int(235-180*ratio),int(243-130*ratio),int(251-85*ratio))
    x=left+z*size;y=top+i*size;dr.rectangle((x,y,x+size,y+size),fill=color,outline='white',width=4)
    center(dr,x+size/2,y+75,str(value),43,fill='white' if ratio>.65 else '#142D45')
    center(dr,x+size/2,y+135,[['TN','FP'],['FN','TP']][i][z],26,fill='white' if ratio>.65 else '#142D45')
 center(dr,900,810,'Hàng: nhãn thật | Cột: nhãn dự đoán | Ô hiển thị số bình luận',27)
 return save(im,name)

v1=j('reports/resplit_v1/final_evaluation/results.json')
lab=['BoW\nNB','TF-IDF\nNB','BoW\nSVM','TF-IDF\nSVM','SVM\ncải tiến','PhoBERT']
models={m['model']:m['validation'] for m in v1['models']}
met=[models[x] for x in ['bow_nb','tfidf_nb','bow_svm','tfidf_svm']]+[{'macro_f1':.688595814,'f1_toxic':.423280423,'recall_toxic':.481927711},{'macro_f1':.6888,'f1_toxic':.4205,'recall_toxic':.4458}]
f1=bars('v1_metrics.png','V1 So sánh kết quả validation','1.277 bình luận | 83 toxic | PhoBERT tại ngưỡng 0,52',lab,[(n,[m[key]*100 for m in met]) for n,key in [('Macro-F1','macro_f1'),('F1-toxic','f1_toxic'),('Recall-toxic','recall_toxic')]])
f2=cm('v1_cm.png','V1 Ma trận nhầm lẫn trên validation','Số liệu SVM từ manifest; PhoBERT từ REPORT V1',[('SVM cải tiến',[1128,66,43,40]),('PhoBERT tau 0,52',[1138,56,46,37])])
f3=bars('v2_metrics.png','V2 So sánh kết quả validation','824 bình luận | 54 toxic | So sánh trên cùng tập đánh giá',['BoW\nNB','TF-IDF\nNB','BoW\nSVM','TF-IDF\nSVM','Word+Char\nSVM','PhoBERT'],[('Macro-F1',[74.05,59.36,75.82,74.67,78.83,78.88]),('F1-toxic',[51.06,21.88,54.35,52.17,60.38,60.55]),('Recall-toxic',[44.44,12.96,46.30,44.44,59.26,61.11])])
f4=cm('v2_cm.png','V2 Ma trận nhầm lẫn trên validation','824 bình luận | 770 non-toxic và 54 toxic',[('Word+Char SVM',[750,20,22,32]),('PhoBERT tau 0,90',[748,22,21,33])])
hist=read('reports/phobert_v2/training_history.csv');xs=[float(z['epoch']) for z in hist]
f5=lines('v2_loss.png','V2 Diễn biến loss của PhoBERT','Checkpoint chọn bằng Macro-F1; không chọn chỉ bằng loss',xs,[(n,[float(z[key]) for z in hist]) for n,key in [('Train loss','train_loss'),('Validation loss','val_loss')]],'Epoch',yr=(.45,.85))
th=read('reports/phobert_v2/threshold_search.csv')
f6=lines('v2_tau.png','V2 Các chỉ số theo ngưỡng PhoBERT','Validation 824 câu | checkpoint epoch 4',[float(z['threshold']) for z in th],[(n,[float(z[key])*100 for z in th]) for n,key in [('Macro-F1','macro_f1'),('Precision-toxic','precision_toxic'),('Recall-toxic','recall_toxic')]],'Ngưỡng xác suất tau',mark=.9)
sv=read('reports/kfold_v3/svm/svm_fold_details.csv');ph=read('reports/kfold_v3/phobert/kfold_results.csv')[:5]
f7=lines('v3_fold.png','V3 Macro-F1 theo từng fold','Cùng bảng chia nhóm theo post_id | PhoBERT dùng ngưỡng mặc định',list(range(5)),[('Word+Char SVM',[float(next(q for q in sv if q['model']=='word_char_svm' and int(q['fold'])==i)['macro_f1'])*100 for i in range(5)]),('PhoBERT',[float(q['macro_f1'])*100 for q in ph])],'Fold',yr=(60,80))
f8=bars('v3_oof.png','V3 Kết quả gộp dự đoán OOF','7.669 bình luận | PhoBERT được chọn ngưỡng 0,85 trên OOF',['BoW\nSVM','TF-IDF\nSVM','Word+Char\nSVM','PhoBERT'],[('Macro-F1',[64.96,66.44,68.98,71.22]),('F1-toxic',[33.14,36.12,41.34,46.09]),('Recall-toxic',[23.45,26.85,34.67,44.89])])
f9=cm('v3_cm.png','V3 Ma trận nhầm lẫn OOF','7.669 bình luận | 499 toxic | Hai mô hình có cùng tập đánh giá',[('Word+Char SVM',[7005,165,326,173]),('PhoBERT tau 0,85',[6921,249,275,224])])

d=Document(O/'Chuong_3_tu_3_4_ban_ngan_gon.docx')
def anchor(text):return next(p for p in d.paragraphs if p.text==text)
def insert(before,path,title,source,bullets):
 target=anchor(before)
 par=d.add_paragraph();par.alignment=WD_ALIGN_PARAGRAPH.CENTER;par.paragraph_format.keep_with_next=True
 par.add_run().add_picture(str(path),width=Cm(16));target._p.addprevious(par._p)
 par=d.add_paragraph(title,style='Caption');par.alignment=WD_ALIGN_PARAGRAPH.CENTER;target._p.addprevious(par._p)
 par=d.add_paragraph('Nguồn: '+source)
 for run in par.runs:run.font.size=Pt(9);run.italic=True
 target._p.addprevious(par._p)
 for label,text in bullets:
  par=d.add_paragraph(style='List Bullet');par.add_run(label+': ').bold=True;par.add_run(text);target._p.addprevious(par._p)
insert('3.4.3 Ưu điểm và nhược điểm',f1,'Hình 3.1 So sánh các chỉ số validation V1','results.json baseline V1; manifest steps23_v2; REPORT PhoBERT V1.',[('Nhận xét','SVM cải tiến và PhoBERT gần nhau về Macro-F1; chưa đủ cơ sở tuyên bố PhoBERT vượt trội ở V1.')])
insert('3.4.3 Ưu điểm và nhược điểm',f2,'Hình 3.2 Confusion matrix của hai mô hình V1','models/current_run.json cho SVM V1; reports/phobert/REPORT.md cho PhoBERT V1.',[('Đánh đổi','PhoBERT báo nhầm ít hơn 10 câu nhưng phát hiện đúng ít hơn 3 câu toxic so với SVM.')])
insert('3.5.3 Huấn luyện và ngưỡng quyết định',f3,'Hình 3.3 So sánh các chỉ số validation V2','validation_report.md cải tiến resplit_v2; best_metrics.json PhoBERT V2.',[('Nhận xét','Word+Char SVM có Macro-F1 cao hơn các baseline trong hình; hai mô hình cuối có kết quả gần tương đương.')])
insert('3.5.3 Huấn luyện và ngưỡng quyết định',f4,'Hình 3.4 Confusion matrix của hai mô hình V2','validation_report.md SVM V2; REPORT và best_metrics.json PhoBERT V2.',[('Đánh đổi','PhoBERT phát hiện đúng thêm 1 toxic, đồng thời báo nhầm thêm 2 non-toxic.')])
insert('3.5.4 So sánh V1 và V2',f5,'Hình 3.5 Train loss và validation loss PhoBERT V2','reports/phobert_v2/training_history.csv.',[('Nhận xét','Train loss tiếp tục giảm còn validation loss tăng sau epoch 2; cần theo dõi overfitting.')])
insert('3.5.4 So sánh V1 và V2',f6,'Hình 3.6 Ảnh hưởng của ngưỡng đến các chỉ số V2','reports/phobert_v2/threshold_search.csv.',[('Cách giải thích','Tăng ngưỡng làm số cảnh báo không tăng và Recall không tăng; giảm báo nhầm có thể giúp Macro-F1 tăng.'),('Giới hạn','0,90 tốt nhất trong các ngưỡng đã khảo sát trên validation này, không phải ngưỡng tối ưu cho mọi dữ liệu.')])
insert('3.6.3 Kết quả OOF và phân tích lỗi',f7,'Hình 3.7 Macro-F1 theo năm fold trong V3','svm_fold_details.csv; phobert/kfold_results.csv trong reports/kfold_v3.',[('Nhận xét','PhoBERT cao hơn trong năm fold, nhưng mức chênh thay đổi; fold 3 gần như ngang nhau.')])
insert('3.7 Tổng hợp và đánh giá cuối',f8,'Hình 3.8 So sánh chỉ số OOF V3','kfold_svm_comparison.csv; phobert/kfold_summary.json.',[('Nhận xét','PhoBERT có Macro-F1 và Recall-toxic cao hơn; đây là điểm OOF sau chọn ngưỡng, khác điểm trung bình từng fold.')])
insert('3.7 Tổng hợp và đánh giá cuối',f9,'Hình 3.9 Confusion matrix OOF V3','Bảng dự đoán OOF của SVM và PhoBERT trong reports/kfold_v3.',[('Đánh đổi','PhoBERT giảm tổng FN 51 câu, nhưng tăng FP 84 câu. Cần cân nhắc chi phí kiểm duyệt nhầm.')])
# Replace old figure caption to keep numbering unique.
for p in d.paragraphs:
 if p.text=='Hình 3.1 Diễn biến huấn luyện PhoBERT V2 tại ngưỡng 0,50':
  p.text='Diễn biến các độ đo qua epoch của PhoBERT V2 tại ngưỡng 0,50'
  # Existing figure repeats loss; remove it and its caption to retain only newly sourced charts.
  prev=p._p.getprevious()
  if prev is not None:prev.getparent().remove(prev)
  p._p.getparent().remove(p._p)
d.save(O/'Chuong_3_tu_3_4_co_bieu_do.docx')
print('Created',len(d.inline_shapes),'figures; ',len(d.tables),'tables')
