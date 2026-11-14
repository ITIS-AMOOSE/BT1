from pathlib import Path
from copy import deepcopy
import csv,json,hashlib,zipfile
from lxml import etree
from docx import Document
from docx.shared import Cm,Pt,RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from PIL import Image,ImageDraw,ImageFont
R=Path('E:/BT1');O=R/'output/word';T=R/'tmp/continue_chapter3';A=O/'chapter3_continuation_figures'
T.mkdir(parents=True,exist_ok=True);A.mkdir(exist_ok=True)
reference=Path('C:/Users/Admin/Documents/Chương 3 NLP.docx')
d=Document(reference);original=deepcopy(list(d._element.body)[:-1]);original_text=[p.text for p in d.paragraphs]
(T/'artifact.md').write_text('''# Continuation contract
Reference: C:/Users/Admin/Documents/Chương 3 NLP.docx
SHA256: '''+hashlib.sha256(reference.read_bytes()).hexdigest()+'''
Scope: append sections 3.5–3.9 only. Preserve every existing V1 body element, all three images, all text, headings and paragraph properties. Preserve styles, numbering, page system and headers/footers.
Page system: one A4 portrait section, left 2.5 cm, right 2 cm; all margins retained directly from source. Body Times New Roman 12 pt inherited. Body uses List Paragraph with bold lead-ins and nested bullets, followed by figures and shared comments.
Components: use source Heading 1/2 styles; cloned List Paragraph properties for bullet levels; Caption centered. No new source footnotes or code descriptions. New chart captions continue at Figure 3.9. New sections use the same six-step sequence as V1 and retain separate traditional-ML and PhoBERT branches.
Slots: original body preserve-only; all new paragraphs and images appended before the existing final section properties. Image/chart counts checked after saving.
Render limitation: packaged render attempted; if LibreOffice unavailable, disclose visual QA limitation. New source data must be validated independently of layout.
''',encoding='utf-8')
def read(p):
 with open(R/p,encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def f(n):return ImageFont.truetype('C:/Windows/Fonts/arial.ttf',n)
def center(dr,x,y,text,n=32,color='#18344D'):
 b=dr.textbbox((0,0),text,font=f(n));dr.text((x-(b[2]-b[0])/2,y),text,font=f(n),fill=color)
def matrices(name,title,models,total,toxic):
 count=len(models);im=Image.new('RGB',(2700,1610),'white');dr=ImageDraw.Draw(im)
 center(dr,1350,22,title,46);center(dr,1350,87,f'{total:,} bình luận | {toxic} toxic | Hàng: nhãn thật; cột: nhãn dự đoán'.replace(',','.'),31)
 positions=[(15,160),(915,160),(1815,160),(465,850),(1365,850)] if count==5 else [(465,160),(1365,160),(465,850),(1365,850)]
 for (model,cm),(x,y) in zip(models,positions):
  assert sum(cm)==total and cm[2]+cm[3]==toxic
  center(dr,x+435,y,model,34);center(dr,x+435,y+55,'Nhãn dự đoán',27)
  gx=x+200;gy=y+145;size=225
  for j,lab in enumerate(['Non-toxic (0)','Toxic (1)']):center(dr,gx+size*(j+.5),y+100,lab,27)
  for i,lab in enumerate(['Non-toxic (0)','Toxic (1)']):dr.text((x+8,gy+size*(i+.5)-15),lab,font=f(25),fill='#18344D')
  for i in range(2):
   for j in range(2):
    value=cm[i*2+j];ratio=value/(total-toxic);rgb=tuple(int(a-b*ratio) for a,b in [(235,180),(243,130),(251,85)])
    xx=gx+j*size;yy=gy+i*size;dr.rectangle((xx,yy,xx+size,yy+size),fill=rgb,outline='white',width=5)
    color='white' if ratio>.65 else '#18344D'
    center(dr,xx+size/2,yy+57,str(value),56,color);center(dr,xx+size/2,yy+130,[['TN','FP'],['FN','TP']][i][j],30,color)
 center(dr,1350,1540,'Các ô là số bình luận; các mô hình trong cùng hình dùng chung thang màu.',29)
 path=A/name;im.save(path,dpi=(300,300));return path
v2=read('reports/resplit_v2/improvements/validation_comparison.csv');by={x['model']:x for x in v2}
keys=['bow_nb','tfidf_nb','bow_svm','tfidf_svm'];names=['BoW + Naive Bayes','TF-IDF + Naive Bayes','BoW + SVM','TF-IDF + SVM']
cms=[(name,[int(by[k][z]) for z in ['tn','fp','fn','tp']]) for k,name in zip(keys,names)]+[('PhoBERT (ngưỡng 0,90)',[748,22,21,33])]
cm2=matrices('v2_5_matrices.png','MA TRẬN NHẦM LẪN CỦA NĂM MÔ HÌNH V2',cms,824,54)
svm3=read('reports/kfold_v3/svm/kfold_svm_comparison.csv')
cm3=matrices('v3_4_matrices.png','MA TRẬN NHẦM LẪN NGOÀI MẪU V3',[(name,[int(x[z]) for z in ['TN','FP','FN','TP']]) for name,x in zip(['BoW + SVM','TF-IDF + SVM','SVM từ + ký tự'],svm3)]+[('PhoBERT (ngưỡng 0,85)',[6921,249,275,224])],7669,499)
# Reuse existing deterministic chart helpers without running their authoring body.
ns={};exec((R/'add_result_figures.py').read_text(encoding='utf-8').split('v1=j(')[0],ns);ns['A']=A
metrics2=ns['bars']('v2_compare.png','V2 So sánh các chỉ số trên tập xác thực','824 bình luận | PhoBERT dùng ngưỡng 0,90',
 ['BoW\nNB','TF-IDF\nNB','BoW\nSVM','TF-IDF\nSVM','Word+Char\nSVM','PhoBERT'],
 [('Macro-F1',[float(by[k]['macro_f1'])*100 for k in keys]+[78.826811541,78.878218312]),('F1-toxic',[float(by[k]['f1_toxic'])*100 for k in keys]+[60.37735849,60.550458716]),('Recall-toxic',[float(by[k]['recall_toxic'])*100 for k in keys]+[59.259259259,61.111111111])])
# All new paragraph properties derive from the supplied document.
bullet_proto=deepcopy(d.paragraphs[15]._p.pPr);nested_proto=deepcopy(d.paragraphs[5]._p.pPr)
def bullet(text,nested=False):
 p=d.add_paragraph();p._p.insert(0,deepcopy(nested_proto if nested else bullet_proto))
 p.paragraph_format.keep_with_next=False;p.paragraph_format.space_after=Pt(6)
 if ': ' in text:
  a,b=text.split(': ',1);p.add_run(a+': ').bold=True;p.add_run(b)
 else:p.add_run(text)
 return p
def h(text,l=2):
 p=d.add_paragraph(text,style='Heading '+str(l));p.paragraph_format.keep_with_next=True
 for run in p.runs:run.font.color.rgb=RGBColor(0,0,0)
 return p
fig_no=8
def figure(path,caption):
 global fig_no
 fig_no+=1;p=d.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.paragraph_format.space_before=Pt(10);p.paragraph_format.keep_with_next=True
 p.add_run().add_picture(str(path),width=Cm(16))
 p=d.add_paragraph(f'Hình 3.{fig_no} {caption}',style='Caption');p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.paragraph_format.space_after=Pt(12)
def page():d.add_page_break()

page();h('3.5 Thực nghiệm V2',1)
h('3.5.1 Mục tiêu và các mô hình sử dụng')
bullet('Mục tiêu: Sau thực nghiệm V1, nhóm nhận thấy các mô hình vẫn bỏ sót nhiều bình luận toxic. Vì vậy, nhóm thực hiện V2 để khảo sát kết quả khi tăng phần dữ liệu dành cho huấn luyện, đồng thời tiếp tục xem xét cách biểu diễn văn bản.')
bullet('Các mô hình được sử dụng: Nhóm giữ bốn baseline và PhoBERT như ở V1 để làm cơ sở đối chiếu. Nhánh SVM kết hợp từ và ký tự tiếp tục được khảo sát trên bộ chia mới; các tham số được lựa chọn lại theo kết quả xác thực V2.')
bullet('Lý do giữ các mô hình: Việc giữ các loại mô hình giúp nhóm theo dõi kết quả khi thay đổi thiết lập dữ liệu. Tuy nhiên, do thành phần các tập cũng thay đổi nên không thể xem đây là thí nghiệm chỉ thay đổi riêng số lượng mẫu huấn luyện.')
bullet('Quy trình thực hiện: Nhóm lần lượt chia lại dữ liệu theo bài viết, xây dựng lại bộ biểu diễn, huấn luyện các cấu hình, lựa chọn cấu hình và ngưỡng, sau đó đối chiếu dự đoán với nhãn thật theo pipeline dưới đây.')
figure(O/'pipeline_figures/v2_bang_loi.png','Quy trình thực nghiệm V2')
h('3.5.2 Chuẩn bị và chia tập dữ liệu')
bullet('Đầu vào: Nhóm tiếp tục sử dụng bộ 8.595 bình luận đã được gán nhãn và tiền xử lý như trình bày tại mục 3.2. Nhãn của các bình luận được giữ nguyên, không bổ sung một bộ dữ liệu mới ở bước này.')
bullet('Bước 1 – Chia dữ liệu: Các bình luận của cùng một bài viết tiếp tục được đưa vào chung một tập. Nhóm thay tỷ lệ chia mục tiêu thành 80/10/10 và lựa chọn cách phân bố bài viết để số lượng mẫu và tỷ lệ nhãn gần với mục tiêu. Vì phải giữ nguyên từng bài viết, tỷ lệ thực tế có thể lệch nhẹ so với tỷ lệ đặt ra.')
bullet('Kết quả chia tập: Tập huấn luyện gồm 6.845 bình luận, trong đó có 445 toxic; tập xác thực gồm 824 bình luận với 54 toxic; tập kiểm tra gồm 926 bình luận với 60 toxic.')
bullet('Bước 2 – Kiểm tra sau khi chia: Nhóm đối chiếu để bảo đảm các tập không dùng chung bài viết, không thiếu hoặc lặp bình luận và không thay đổi nhãn đã gán. Tổng số mẫu của ba tập phải bằng 8.595.')
h('3.5.3 Biểu diễn văn bản và huấn luyện mô hình')
bullet('Bước 3 – Biểu diễn văn bản và huấn luyện mô hình: Nhóm sử dụng lại cách chuẩn hóa và tách từ ở mục 3.2, sau đó chuyển văn bản sang dạng đầu vào phù hợp với từng nhánh. Bộ biểu diễn được xây dựng lại từ tập huấn luyện V2.')
bullet('Nhánh học máy truyền thống:')
bullet('Với bốn baseline, văn bản được chuyển thành vector bằng BoW hoặc TF-IDF. Từ vựng và trọng số được xây dựng từ tập huấn luyện V2, sau đó dùng lại để biểu diễn tập xác thực.',True)
bullet('Nhóm lần lượt huấn luyện các cấu hình của Naive Bayes và SVM trên tập huấn luyện, rồi ghi lại kết quả dự đoán trên tập xác thực. Bộ từ vựng đã học từ V1 không được dùng để thay cho bước xây dựng biểu diễn ở V2.',True)
bullet('Thử nghiệm SVM kết hợp: Nhóm tạo hai phần đặc trưng, gồm TF-IDF theo từ từ văn bản đã tách từ và TF-IDF theo ký tự từ văn bản đã chuẩn hóa. Hai phần được ghép lại để huấn luyện SVM. Cách làm này giúp mô hình có thêm thông tin về cụm từ và các biến thể cách viết.')
bullet('Nhánh PhoBERT:')
bullet('Các bình luận đã chuẩn hóa và tách từ được chuyển thành dãy mã số bằng bộ mã hóa của PhoBERT. Những bình luận dài hơn giới hạn được cắt theo cùng cấu hình đã đặt khi huấn luyện.',True)
bullet('Mô hình được huấn luyện tối đa 5 lượt trên tập huấn luyện V2. Trong mỗi lượt, mô hình lần lượt nhận các nhóm bình luận, dự đoán nhãn, so với nhãn thật và điều chỉnh tham số dựa trên mức sai lệch.',True)
bullet('Bước 4 – Theo dõi kết quả huấn luyện:')
bullet('Nhánh học máy truyền thống: Sau khi học xong mỗi cấu hình, nhóm đánh giá trên tập xác thực và ghi lại các chỉ số để đối chiếu.',True)
bullet('Nhánh PhoBERT: Sau mỗi lượt học, nhóm tính Macro-F1 trên tập xác thực và lưu trạng thái có kết quả tốt nhất. Nhờ đó, mô hình được giữ lại dựa trên kết quả xác thực thay vì chỉ dựa vào mức giảm lỗi trên tập huấn luyện.',True)
figure(O/'figures_results/v2_loss.png','Diễn biến loss trong quá trình huấn luyện PhoBERT V2')
bullet('Nhận xét về quá trình học: Loss huấn luyện giảm từ khoảng 0,7704 xuống 0,5101. Loss xác thực thấp nhất ở lượt thứ 2 rồi tăng trở lại, trong khi Macro-F1 tại ngưỡng 0,50 cao nhất ở lượt thứ 4. Loss còn phụ thuộc độ lớn xác suất, còn F1 được tính từ nhãn sau khi áp ngưỡng nên hai chỉ số không nhất thiết thay đổi cùng hướng.')
h('3.5.4 Lựa chọn cấu hình và ngưỡng phân loại')
bullet('Bước 5 – Chọn cấu hình và ngưỡng phân loại: Nhóm đối chiếu các cấu hình trên tập xác thực V2 và ưu tiên Macro-F1. Khi cần xem xét thêm, nhóm dùng F1 và Recall của lớp toxic để hiểu sự khác nhau giữa phát hiện đúng và bỏ sót.')
bullet('Với SVM kết hợp: Cấu hình được chọn sử dụng cụm từ một đến hai từ kết hợp đoạn ký tự dài ba đến năm ký tự. Nhóm đặt trọng số phạt lỗi của lớp toxic cao hơn lớp non-toxic để hạn chế xu hướng chỉ dự đoán lớp chiếm đa số.')
bullet('Với PhoBERT: Trạng thái sau lượt học thứ 4 được giữ lại. Tại ngưỡng mặc định 0,50, mô hình đạt Macro-F1 khoảng 77,26%.')
bullet('Ngưỡng của SVM: Các cấu hình SVM trong V2 giữ ranh giới quyết định mặc định bằng 0. Khác với nhánh SVM tối ưu V1, ngưỡng này không được học từ dự đoán ngoài mẫu.')
bullet('Ngưỡng của PhoBERT: Nhóm thử các ngưỡng từ 0,10 đến 0,90, mỗi lần tăng 0,02 trên tập xác thực của trạng thái đã chọn. Ngưỡng 0,90 cho Macro-F1 cao nhất trong phạm vi khảo sát. Bình luận có điểm toxic từ 0,90 trở lên được gán toxic, thấp hơn được gán non-toxic.')
figure(O/'figures_results/v2_tau.png','Ảnh hưởng của ngưỡng đến các chỉ số của PhoBERT V2')
bullet('Nhận xét về ngưỡng: Khi tăng ngưỡng từ 0,50 lên 0,90, số báo nhầm giảm từ 41 xuống 22, nhưng số toxic được phát hiện đúng cũng giảm từ 39 xuống 33. Việc giảm báo nhầm giúp Macro-F1 tăng lên 78,88%, đồng thời mô hình phải chấp nhận bỏ sót thêm một số câu toxic.')
h('3.5.5 Đánh giá và kiểm tra đầu ra')
bullet('Bước 6 – Đối chiếu kết quả: Nhóm dùng các cấu hình và ngưỡng đã chọn để tạo nhãn dự đoán, rồi ghép với nhãn thật của đúng bình luận. Từ đó, xác định số dự đoán đúng, số non-toxic bị báo nhầm và số toxic bị bỏ sót.')
bullet('Tính các chỉ số đánh giá: Nhóm tính Accuracy, Precision, Recall, F1-toxic và Macro-F1 cho các mô hình, sau đó biểu diễn bằng biểu đồ chung. Ma trận nhầm lẫn của bốn baseline và PhoBERT được ghép trong cùng một hình để thuận tiện đối chiếu như ở V1.')
bullet('Kiểm tra kết quả: Mỗi bình luận phải có đúng một nhãn dự đoán. Tổng các ô trong từng ma trận phải bằng 824, trong đó có 770 non-toxic và 54 toxic thật. Đây là kết quả xác thực V2, không phải kết quả trên tập kiểm tra 926 bình luận.')
bullet('Lưu kết quả: Nhóm lưu mô hình, cấu hình, ngưỡng, lịch sử huấn luyện và dự đoán để phục vụ phân tích. Trước bàn giao, cần tải lại mô hình và đối chiếu với kết quả đã lưu để xác nhận khả năng sử dụng lại.')
figure(metrics2,'So sánh các chỉ số trên tập xác thực V2')
figure(cm2,'Ma trận nhầm lẫn của năm mô hình ở V2')
bullet('Nhận xét chung về ma trận: Hai baseline SVM phát hiện đúng 24–25 trong 54 câu toxic. PhoBERT phát hiện được 33 câu và báo nhầm 22 câu non-toxic. TF-IDF + Naive Bayes chỉ phát hiện đúng 7 câu toxic dù có ít báo nhầm, cho thấy mô hình vẫn nghiêng về dự đoán non-toxic.')
h('3.5.6 Nhận xét về thực nghiệm V2')
bullet('Về dữ liệu: Phần huấn luyện tăng lên 6.845 bình luận nhưng tập xác thực giảm còn 824 bình luận và chỉ có 54 toxic. Vì số toxic ít, thay đổi dự đoán của một vài câu cũng có thể làm các chỉ số biến động đáng kể.')
bullet('Về các baseline: BoW + SVM đạt Macro-F1 75,82%, cao nhất trong bốn baseline. TF-IDF không luôn tốt hơn BoW; hiệu quả còn phụ thuộc dữ liệu và cấu hình được sử dụng.')
bullet('Về SVM kết hợp và PhoBERT: SVM kết hợp đạt Macro-F1 78,83%, còn PhoBERT đạt 78,88%. PhoBERT phát hiện đúng nhiều hơn SVM kết hợp 1 câu toxic nhưng cũng báo nhầm nhiều hơn 2 câu, nên mức chênh giữa hai mô hình còn nhỏ.')
bullet('Về đối chiếu với V1: Điểm xác thực V2 cao hơn V1, nhưng cả tập huấn luyện, tập xác thực và một số cấu hình đều thay đổi. Vì vậy, chưa thể quy toàn bộ mức tăng cho việc dành thêm dữ liệu huấn luyện hoặc xem V2 là kết quả tốt hơn trên mọi dữ liệu.')
bullet('Hướng thực nghiệm tiếp theo: Nhóm tiếp tục đánh giá qua nhiều nhóm bài viết ở V3 để xem các mô hình có giữ được kết quả khi thay đổi phần dữ liệu đánh giá hay không.')

page();h('3.6 Thực nghiệm V3',1)
h('3.6.1 Mục tiêu và các mô hình sử dụng')
bullet('Mục tiêu: V3 được thực hiện để quan sát kết quả qua nhiều nhóm bài viết, thay vì chỉ dựa vào một tập xác thực cố định. Nhóm muốn xem cả điểm trung bình và mức dao động của từng mô hình.')
bullet('Các mô hình được sử dụng: Nhóm tập trung vào BoW + SVM, TF-IDF + SVM, SVM kết hợp từ với ký tự và PhoBERT. V3 không huấn luyện lại hai baseline Naive Bayes trong lượt kiểm định này, nên phần kết quả chỉ đối chiếu bốn mô hình đã chạy.')
bullet('Lý do sử dụng cùng cách chia: Các mô hình được huấn luyện và đánh giá trên cùng các nhóm bài viết ở từng lượt. Điều này giúp mức chênh lệch được quan sát trong cùng điều kiện dữ liệu.')
bullet('Quy trình thực hiện: Nhóm gộp phần huấn luyện và xác thực, chia thành năm phần theo bài viết, lần lượt huấn luyện trên bốn phần và dự đoán phần còn lại. Sau năm lượt, các dự đoán được ghép về đúng bình luận để tổng hợp kết quả.')
figure(O/'pipeline_figures/v3_bang_loi.png','Quy trình thực nghiệm V3')
h('3.6.2 Chuẩn bị và chia tập dữ liệu')
bullet('Đầu vào: Nhóm gộp tập huấn luyện và xác thực V2 thành 7.669 bình luận thuộc 95 bài viết, gồm 499 toxic. Tập kiểm tra V2 với 926 bình luận được giữ riêng, không đưa vào phần dữ liệu này.')
bullet('Bước 1 – Chia dữ liệu: Phần dữ liệu phát triển được chia thành năm phần bằng phương pháp kiểm định chéo theo nhóm có xét phân bố nhãn. Bình luận cùng bài viết luôn thuộc cùng một phần; tỷ lệ toxic giữa các phần được cân đối ở mức có thể nhưng không bảo đảm bằng nhau hoàn toàn.')
bullet('Cách sử dụng các phần: Ở mỗi lượt, nhóm lấy một phần để đánh giá và bốn phần còn lại để huấn luyện. Sau đó thay đổi phần đánh giá cho đến khi thực hiện đủ năm lượt.')
bullet('Bước 2 – Kiểm tra sau khi chia: Bảo đảm mỗi bình luận thuộc đúng một phần, các phần không dùng chung bài viết và không trùng bài với tập kiểm tra. Cùng một bảng phân chia được dùng cho cả SVM và PhoBERT.')
h('3.6.3 Biểu diễn văn bản và huấn luyện mô hình')
bullet('Bước 3 – Biểu diễn văn bản và huấn luyện mô hình: Ở mỗi lượt, nhóm chỉ sử dụng bốn phần huấn luyện để xây bộ biểu diễn và học mô hình. Phần còn lại được dành cho dự đoán và đánh giá của lượt đó.')
bullet('Nhánh học máy truyền thống:')
bullet('Nhóm tạo lại bộ từ vựng và trọng số từ phần huấn luyện của từng lượt, sau đó chuyển đổi phần đánh giá bằng chính bộ biểu diễn đó. Các mô hình được học riêng cho từng lượt, không học tiếp từ mô hình của lượt trước.',True)
bullet('Ba cấu hình SVM gồm BoW, TF-IDF theo từ và TF-IDF kết hợp từ với ký tự. Các cấu hình được giữ cố định trong lần kiểm định để quan sát sự thay đổi kết quả theo dữ liệu.',True)
bullet('Nhánh PhoBERT:')
bullet('Mỗi lượt bắt đầu từ mô hình tiền huấn luyện và được điều chỉnh bằng bốn phần huấn luyện tương ứng. Văn bản được mã hóa theo cùng cách xử lý, giúp các lượt khác nhau về dữ liệu nhưng thống nhất về cách tạo đầu vào.',True)
bullet('Sau mỗi lượt học bên trong một lần chia, nhóm đánh giá trên phần đã giữ lại và lưu trạng thái có Macro-F1 tốt nhất. Trạng thái đó tạo ra điểm dự đoán cho các bình luận thuộc phần đánh giá.',True)
bullet('Bước 4 – Theo dõi kết quả huấn luyện:')
bullet('Nhánh học máy truyền thống: Sau mỗi lần chia, nhóm ghi lại các chỉ số và lưu điểm cùng nhãn dự đoán của ba mô hình SVM trên phần đánh giá.',True)
bullet('Nhánh PhoBERT: Nhóm lưu trạng thái được chọn, các chỉ số và điểm dự đoán của từng phần. Có năm mô hình tương ứng năm lần chia, khác với năm lượt học liên tiếp của cùng một mô hình ở V1 hoặc V2.',True)
figure(O/'figures_results/v3_fold.png','Macro-F1 qua năm phần đánh giá ở V3')
bullet('Nhận xét về từng phần: PhoBERT đạt Macro-F1 cao hơn SVM kết hợp trong cả năm phần đã chạy, nhưng mức chênh không đồng đều. Ở phần đánh giá thứ tư, tương ứng fold 3 trên hình, hai mô hình gần như ngang nhau.')
h('3.6.4 Lựa chọn cấu hình và ngưỡng phân loại')
bullet('Bước 5 – Tổng hợp dự đoán và chọn ngưỡng: Nhóm ghép dự đoán của từng phần về đúng bình luận ban đầu. Mỗi bình luận có một dự đoán từ lượt mô hình không dùng bình luận đó để huấn luyện; đây là dự đoán ngoài mẫu.')
bullet('Với SVM: Nhóm giữ ranh giới quyết định mặc định bằng 0 để chuyển điểm thành nhãn. Ba cấu hình được đối chiếu theo điểm từng phần và kết quả gộp ngoài mẫu.')
bullet('Với PhoBERT: Nhóm thử ngưỡng trên các điểm ngoài mẫu từ 0,20 đến dưới 0,95, mỗi lần tăng 0,05 và chọn giá trị 0,85. Sau đó dùng ngưỡng này để tạo nhãn ngoài mẫu cuối cùng.')
bullet('Phạm vi lựa chọn: Phần đánh giá đã được dùng chọn trạng thái PhoBERT và bảng ngoài mẫu được dùng chọn ngưỡng. Do đó, điểm gộp vẫn chịu ảnh hưởng của quá trình lựa chọn, chưa phải một phép đánh giá cuối hoàn toàn độc lập.')
h('3.6.5 Đánh giá và kiểm tra đầu ra')
bullet('Bước 6 – Đối chiếu kết quả: Nhóm ghép nhãn dự đoán ngoài mẫu với nhãn thật của từng bình luận, rồi tính Accuracy, Precision, Recall, F1-toxic, Macro-F1 và ma trận nhầm lẫn.')
bullet('Hai cách tổng hợp: Nhóm tính trung bình và độ lệch chuẩn của chỉ số qua năm phần để xem mức biến động, đồng thời tính chỉ số một lần trên toàn bộ dự đoán ngoài mẫu. Với PhoBERT, điểm từng phần dùng ngưỡng mặc định còn điểm ngoài mẫu cuối dùng ngưỡng 0,85 nên không được coi là cùng một cách tính.')
bullet('Kiểm tra kết quả: Bảng ngoài mẫu phải có đủ 7.669 bình luận, mỗi bình luận xuất hiện một lần, đúng nhãn thật và đúng phần đánh giá. Tổng các ô của mỗi ma trận phải bằng 7.669, gồm 7.170 non-toxic và 499 toxic.')
bullet('Lưu kết quả: Nhóm lưu mô hình theo từng phần, cách phân chia, cấu hình, ngưỡng và dự đoán ngoài mẫu. Cần tải lại mô hình để đối chiếu khả năng tái tạo dự đoán trước khi xác nhận bàn giao đầy đủ.')
figure(O/'figures_results/v3_oof.png','So sánh các chỉ số trên dự đoán ngoài mẫu V3')
figure(cm3,'Ma trận nhầm lẫn của bốn mô hình ở V3')
bullet('Nhận xét chung về ma trận: PhoBERT phát hiện đúng 224/499 câu toxic và báo nhầm 249 câu non-toxic. SVM kết hợp phát hiện đúng 173 câu và báo nhầm 165 câu. Như vậy, PhoBERT có tổng số phát hiện đúng cao hơn 51 câu, nhưng cũng tạo thêm 84 cảnh báo nhầm.')
h('3.6.6 Nhận xét về thực nghiệm V3')
bullet('Về dữ liệu: Việc thay đổi phần đánh giá cho thấy hiệu năng có dao động theo nhóm bài viết. Dữ liệu toxic vẫn ít và phân bố không đều nên cần xem kết quả của nhiều phần thay vì chỉ dựa vào một lần chia.')
bullet('Về các mô hình SVM: SVM kết hợp đạt Macro-F1 trung bình 68,94%, cao hơn BoW + SVM 64,70% và TF-IDF + SVM 66,30%. Điều này cho thấy đặc trưng kết hợp có ích trong lần kiểm định đã thực hiện.')
bullet('Về PhoBERT: Macro-F1 trung bình đạt 71,16%, cao hơn SVM kết hợp khoảng 2,22 điểm phần trăm. Tuy nhiên, độ lệch chuẩn của PhoBERT là 2,39 điểm phần trăm, lớn hơn 1,42 của SVM kết hợp, cho thấy kết quả PhoBERT dao động nhiều hơn trong các phần đã khảo sát.')
bullet('Về báo nhầm và bỏ sót: PhoBERT có Recall-toxic ngoài mẫu 44,89%, cao hơn 34,67% của SVM kết hợp, nhưng Precision-toxic thấp hơn, 47,36% so với 51,18%. Mô hình vẫn bỏ sót 275/499 câu toxic, nên chưa đáp ứng việc phát hiện đầy đủ bình luận độc hại.')
bullet('Về đánh giá cuối: Kết quả ngoài mẫu chưa thay thế đánh giá trên tập kiểm tra 926 câu. Nhóm cần chốt mô hình, cách kết hợp nếu có và ngưỡng trước khi dùng tập này để đánh giá lựa chọn cuối.')

page();h('3.7 Tổng hợp và đánh giá chung',1)
h('3.7.1 Kết quả đạt được')
bullet('Về quá trình thực hiện: V1 tạo được mốc ban đầu; V2 khảo sát một bộ chia có nhiều dữ liệu huấn luyện hơn; V3 đánh giá qua nhiều nhóm bài viết. Mỗi giai đoạn đều có các bước chuẩn bị dữ liệu, biểu diễn, huấn luyện, lựa chọn và đối chiếu kết quả.')
bullet('Về đặc trưng: Kết hợp thông tin từ và ký tự giúp SVM có thêm tín hiệu từ các cụm từ và biến thể cách viết. Trong V2, cấu hình kết hợp đạt Macro-F1 78,83%, cao hơn baseline BoW + SVM khoảng 3,00 điểm phần trăm trên cùng tập xác thực.')
bullet('Về mô hình: PhoBERT đạt Macro-F1 cao hơn các baseline trong V1 và V2, đồng thời cao hơn SVM kết hợp về trung bình năm phần của V3. Tuy vậy, ở V1 và V2, chênh lệch giữa PhoBERT và SVM cải tiến nhỏ nên không nên kết luận một mô hình vượt trội ở mọi điều kiện.')
h('3.7.2 Ưu điểm và những hạn chế còn lại')
bullet('Ưu điểm về dữ liệu và đánh giá: Chia theo bài viết hạn chế việc bình luận cùng ngữ cảnh xuất hiện ở cả phần huấn luyện và đánh giá. Các mô hình trong mỗi giai đoạn được đối chiếu trên cùng phần dữ liệu; V3 bổ sung thông tin về độ biến động qua nhiều nhóm bài.')
bullet('Ưu điểm của PhoBERT: Trong V3, mô hình phát hiện được nhiều toxic hơn theo tổng số và có Macro-F1 cao hơn. Đây là lợi thế nếu mục tiêu là chuyển thêm trường hợp nghi ngờ cho người kiểm duyệt rà soát.')
bullet('Ưu điểm của SVM kết hợp: Trong kết quả ngoài mẫu V3, mô hình có Precision-toxic cao hơn và ít báo nhầm hơn PhoBERT. Vì vậy, SVM vẫn đáng cân nhắc khi cần hạn chế số cảnh báo phải kiểm tra lại.')
bullet('Hạn chế về dữ liệu: Số toxic còn ít, một số câu khó xác định khi thiếu nội dung bài viết hoặc hội thoại. Dữ liệu thuộc cộng đồng sinh viên PTIT nên chưa thể đại diện cho mọi nhóm hay mọi thời điểm.')
bullet('Hạn chế về cách so sánh: V1, V2 và V3 khác nhau về thành phần tập đánh giá và cách tổng hợp. Điểm V2 cao hơn V3 không chứng minh V2 tốt hơn; tăng tỷ lệ huấn luyện cũng chưa được tách riêng khỏi ảnh hưởng của thay đổi bộ chia và cấu hình.')
bullet('Hạn chế về khả năng phát hiện: Cả SVM và PhoBERT vẫn bỏ sót nhiều toxic. Việc tăng số phát hiện đúng còn đi kèm báo nhầm, nên chỉ nhìn Macro-F1 là chưa đủ để quyết định cách sử dụng thực tế.')
h('3.7.3 Hướng lựa chọn và kiểm tra trước khi bàn giao')
bullet('Lựa chọn theo mục tiêu: Nếu ưu tiên phát hiện thêm để rà soát, có thể cân nhắc PhoBERT theo kết quả V3. Nếu ưu tiên giảm cảnh báo nhầm, SVM kết hợp là lựa chọn đối chiếu phù hợp. Quyết định cuối cần dựa thêm vào kết quả kiểm tra sau khi đã chốt cấu hình.')
bullet('Kiểm tra đầu ra: Các dự đoán phải đủ mẫu, đúng bình luận và nhãn thật; chỉ số phải khớp ma trận nhầm lẫn. Mô hình cần được lưu cùng cách xử lý đầu vào và ngưỡng để có thể sử dụng lại.')
bullet('Kiểm tra khả năng sử dụng lại: Nhóm cần tải lại mô hình và đối chiếu dự đoán trên cùng dữ liệu. Những kiểm tra chưa có kết quả xác nhận phải được thực hiện bổ sung trước khi xem là nghiệm thu hoàn tất.')

page();h('3.8 Dashboard và demo',1)
h('3.8.1 Mục đích và quy trình sử dụng')
bullet('Mục đích: Demo minh họa cách một bình luận đi qua các bước xử lý để nhận nhãn dự đoán. Các câu thử giúp quan sát hành vi mô hình, còn chất lượng chung được đánh giá bằng các tập có nhãn ở phần thực nghiệm.')
bullet('Bước 1 – Chuẩn bị mô hình: Nạp mô hình đã chọn cùng cách biểu diễn hoặc bộ mã hóa và ngưỡng tương ứng. Khi người dùng nhập một câu mới, mô hình chỉ dự đoán, không học thêm từ câu đó.')
bullet('Bước 2 – Nhận và xử lý đầu vào: Kiểm tra câu nhập không rỗng, sau đó chuẩn hóa và tách từ theo đúng cách đã dùng khi huấn luyện. Văn bản được chuyển thành vector với SVM hoặc dãy mã số với PhoBERT.')
bullet('Bước 3 – Dự đoán và hậu xử lý: Mô hình trả về điểm; hệ thống so điểm với ngưỡng để gán toxic hoặc non-toxic. Điểm SVM không phải xác suất, còn điểm softmax PhoBERT cũng không tự bảo đảm tỷ lệ dự đoán đúng của câu đang xét.')
bullet('Bước 4 – Hiển thị kết quả: Giao diện trình bày nhãn, điểm và ngưỡng để người xem đối chiếu được quy tắc phân loại. Nếu thay ngưỡng trên cùng câu và cùng mô hình, điểm không đổi nhưng nhãn có thể đổi.')
h('3.8.2 Kiểm tra demo')
bullet('Các trường hợp thử: Nhóm sử dụng câu bình thường, câu công kích rõ và câu khó hoặc dự đoán sai. Với mỗi câu, cần giải thích được văn bản sau xử lý, điểm đầu ra và lý do điểm đó dẫn đến nhãn được hiển thị.')
bullet('Kiểm tra tính nhất quán: Cùng một câu, mô hình và ngưỡng cần cho kết quả phù hợp với dự đoán ngoài giao diện. Trước khi trình bày, cần xác nhận mô hình đã được tải và đang chạy đúng; lỗi suy luận không được xem như một dự đoán hợp lệ.')
bullet('Phạm vi kết luận: Một số câu demo đúng chưa chứng minh mô hình tốt trên toàn bộ dữ liệu. Nếu hai mô hình cùng nhãn, chỉ kết luận chúng đồng thuận ở câu đó; chưa suy ra độ tin cậy rất cao.')
h('3.9 Hạn chế và hướng phát triển',1)
bullet('Về dữ liệu: Bổ sung có chọn lọc toxic và những câu non-toxic dễ bị báo nhầm, đồng thời rà soát trường hợp thiếu ngữ cảnh. Có thể bố trí gán nhãn chồng lấn để xem xét sự thống nhất giữa các thành viên.')
bullet('Về đánh giá: Tách bước chọn trạng thái mô hình và ngưỡng khỏi phần chấm cuối để giảm ảnh hưởng của lựa chọn. Sau khi cố định phương pháp, kiểm tra thêm trên bài viết ở thời điểm mới hoặc nguồn khác.')
bullet('Về ứng dụng: Tiếp tục hướng tới hỗ trợ người kiểm duyệt. Ngưỡng cần được lựa chọn theo mức chấp nhận báo nhầm và bỏ sót của người sử dụng, thay vì áp một giá trị cho mọi tình huống.')

out=O/'Chuong_3_NLP_VIET_TIEP_THEO_V1.docx';d.save(out)
c=Document(out)
assert [p.text for p in c.paragraphs[:len(original_text)]]==original_text
for a,b0 in zip(original,list(c._element.body)[:len(original)]):
 assert etree.tostring(a,method='c14n',exclusive=True)==etree.tostring(b0,method='c14n',exclusive=True),'Original V1 changed'
assert len(c.inline_shapes)==12,(len(c.inline_shapes))
assert len(c.tables)==0
assert hashlib.sha256(reference.read_bytes()).hexdigest()=='3056ea16f257a9573a05509b2b8b2c1c55f91a5524c4adeef1260cb2a5f083c7'
print(out);print('Original V1 preserved. Added sections 3.5–3.9, 9 figures, total 12 figures; no new tables.')
