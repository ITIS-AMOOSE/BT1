from pathlib import Path
import json
from docx import Document
from docx.shared import Cm,Pt,RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from PIL import Image,ImageDraw,ImageFont
R=Path('E:/BT1');O=R/'output/word';A=O/'pipeline_figures';A.mkdir(parents=True,exist_ok=True)
d=Document();s=d.sections[0];s.page_width=Cm(21);s.page_height=Cm(29.7)
s.top_margin=s.bottom_margin=Cm(2);s.left_margin=Cm(2.5);s.right_margin=Cm(2)
for name in ['Normal','Title','Heading 1','Heading 2','List Bullet','Caption']:
 st=d.styles[name];st.font.name='Times New Roman';st.font.color.rgb=RGBColor(0,0,0)
 st.font.size=Pt(12 if name in ['Normal','List Bullet'] else 14)
 st.paragraph_format.line_spacing=1.15;st.paragraph_format.space_after=Pt(6)
for name in ['Heading 1','Heading 2']:d.styles[name].paragraph_format.keep_with_next=True
def h(t,l=1):d.add_heading(t,l)
def p(t):d.add_paragraph(t)
def b(title,t):
 z=d.add_paragraph(style='List Bullet');z.add_run(title+': ').bold=True;z.add_run(t)
def page():d.add_page_break()
def table(title,heads,data,widths=None):
 z=d.add_paragraph(title,style='Caption');z.paragraph_format.keep_with_next=True
 t=d.add_table(rows=1,cols=len(heads));t.autofit=False
 widths=widths or [16.5/len(heads)]*len(heads)
 for row,values in [(t.rows[0],heads)]+[(t.add_row(),a) for a in data]:
  for i,(c,v) in enumerate(zip(row.cells,values)):
   c.width=Cm(widths[i]);c.text=str(v)
   pr=c._tc.get_or_add_tcPr();border=OxmlElement('w:tcBorders')
   for edge in ['top','bottom','left','right']:
    e=OxmlElement('w:'+edge);e.set(qn('w:val'),'single');e.set(qn('w:sz'),'4');e.set(qn('w:color'),'D9D9D9');border.append(e)
   pr.append(border)
   for par in c.paragraphs:
    par.paragraph_format.line_spacing=1.05;par.paragraph_format.space_before=Pt(5);par.paragraph_format.space_after=Pt(5)
    for run in par.runs:run.font.size=Pt(10.5)
 for c in t.rows[0].cells:
  e=OxmlElement('w:shd');e.set(qn('w:fill'),'E7E6E6');c._tc.get_or_add_tcPr().append(e)
  for run in c.paragraphs[0].runs:run.bold=True
 e=OxmlElement('w:tblHeader');t.rows[0]._tr.get_or_add_trPr().append(e)
 z=d.add_paragraph();z.paragraph_format.space_after=Pt(2)
def pipeline(name,caption,steps):
 im=Image.new('RGB',(1600,760),'white');dr=ImageDraw.Draw(im);ft=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',29)
 for i,lines in enumerate(steps):
  col=i%3;row=i//3;x=30+col*530;y=30+row*365
  dr.rounded_rectangle((x,y,x+470,y+255),radius=12,fill='#F2F5F8',outline='#385A75',width=3)
  for n,line in enumerate(lines.split('\n')):
   box=dr.textbbox((0,0),line,font=ft);dr.text((x+235-(box[2]-box[0])/2,y+30+n*49),line,font=ft,fill='#142C40')
  if col<2:
   dr.line((x+480,y+125,x+515,y+125),fill='#385A75',width=5);dr.polygon([(x+515,y+125),(x+502,y+117),(x+502,y+133)],fill='#385A75')
 dr.text((35,704),'Đọc theo thứ tự bước 1–6; mỗi nhánh dùng dữ liệu huấn luyện tương ứng.',font=ft,fill='#334155')
 path=A/(name+'.png');im.save(path,dpi=(200,200))
 z=d.add_paragraph();z.alignment=WD_ALIGN_PARAGRAPH.CENTER;z.paragraph_format.keep_with_next=True;z.add_run().add_picture(str(path),width=Cm(16))
 z=d.add_paragraph(caption,style='Caption');z.alignment=WD_ALIGN_PARAGRAPH.CENTER

h('Quy trình thực nghiệm từ V1 đến V3',0)
p('Phần này trình bày cách nhóm tổ chức từng giai đoạn thực nghiệm, từ dữ liệu đầu vào đến mô hình và kết quả được lưu. Ở mỗi giai đoạn, các bước được mô tả theo đầu vào, cách thực hiện, đầu ra và tiêu chí kiểm tra. Kết quả được đặt sau quy trình để làm rõ chúng được tạo ra như thế nào.')
h('3.4 Quy trình thực nghiệm V1')
h('3.4.1 Mục tiêu và pipeline tổng thể',2)
b('Mục tiêu','Xây dựng mốc đối chiếu ban đầu bằng bốn baseline BoW/TF-IDF kết hợp Naive Bayes hoặc SVM, cùng nhánh PhoBERT. Các thí nghiệm bổ sung được tách khỏi bảng baseline.')
pipeline('v1','Hình 3.6 Pipeline thực nghiệm V1',[
'1. Chuẩn bị dữ liệu\nĐọc CSV bằng pandas\nKiểm tra ID và nhãn',
'2. Chia theo bài viết\nNhóm bằng post_id\nMục tiêu 70/15/15',
'3. Tạo đầu vào\nChuẩn hóa và tách từ\nGiữ ID để đối chiếu',
'4. Huấn luyện hai nhánh\nBoW/TF-IDF → NB/SVM\nTokenizer → PhoBERT',
'5. Chọn và hậu xử lý\nValidation chọn cấu hình\nĐiểm → ngưỡng → nhãn',
'6. Đánh giá và lưu\nChỉ số, ma trận lỗi\nMô hình và dự đoán'])
h('3.4.2 Dữ liệu đầu vào và cách chia tập',2)
b('Đầu vào','Bình luận đã gán nhãn, có id, post_id, text, text_clean, text_tokenized và label. pandas đọc CSV; bước kiểm tra từ chối nhãn ngoài 0/1 hoặc bản ghi thiếu trường bắt buộc.')
b('Cách chia','Script chia nhóm tổng hợp số mẫu và số toxic theo post_id, thử các thứ tự nhóm rồi gán nguyên bài vào train, validation hoặc test. Phương án được chọn theo mức lệch tỷ lệ mẫu và phân bố nhãn, không theo điểm mô hình.')
b('Đầu ra','Ba tập gồm 6.000 train, 1.277 validation và 1.318 test. Do chia nguyên bài viết, số mẫu thực tế không nhất thiết đúng tuyệt đối tỷ lệ mục tiêu 70/15/15.')

page();h('3.4.3 Xử lý đầu vào và huấn luyện V1',2)
table('Bảng 3.2 Luồng xử lý của hai nhánh V1',['Bước','Cách thực hiện','Đầu ra'],[
['Chuẩn hóa','Dùng các hàm tiền xử lý đã trình bày ở 3.2: NFC, khoảng trắng, URL/mention; giữ thông tin có thể thể hiện thái độ.','text_clean'],
['Tách từ','Dùng underthesea.word_tokenize; giữ liên kết với id và label.','text_tokenized'],
['Tạo đặc trưng baseline','CountVectorizer hoặc TfidfVectorizer trong Pipeline của scikit-learn; fit trên train, transform validation bằng bộ đã fit.','Vector đặc trưng thưa'],
['Huấn luyện baseline','ParameterGrid tạo các cấu hình; Pipeline.fit học bộ biểu diễn và MultinomialNB hoặc LinearSVC trên train.','Pipeline cho từng cấu hình'],
['Tạo đầu vào PhoBERT','Tokenizer của checkpoint mã hóa câu đã tách từ; thêm token đặc biệt theo cấu hình; cắt/padding tối đa 128 token.','input_ids và attention_mask'],
['Fine-tune PhoBERT','PyTorch và Transformers xử lý theo batch, tính loss, lan truyền ngược và cập nhật bằng AdamW; đánh giá sau epoch.','Checkpoint và lịch sử học']],[3.1,9.2,4.2])
b('Lưới baseline','Khảo sát n-gram từ 1–1 hoặc 1–2, min_df bằng 1 hoặc 2; alpha của NB là 0,1/0,5/1,0; C của SVM là 0,1/1,0/10,0, cùng lựa chọn trọng số lớp trong cấu hình.')
b('Thiết lập PhoBERT','Dùng vinai/phobert-base-v2; batch size 32; learning rate 2×10⁻⁵; weight decay 0,01; warmup 10%; label smoothing 0,05. Văn bản được xử lý thống nhất khi train và suy luận.')
h('3.4.4 Chọn mô hình và hậu xử lý V1',2)
b('Baseline','Mỗi cấu hình dự đoán validation. Nhóm ưu tiên Macro-F1, sau đó F1-toxic và Recall-toxic; pipeline được chọn được lưu bằng joblib. LinearSVC dùng ngưỡng quyết định mặc định 0.')
b('PhoBERT','Chọn checkpoint epoch 5 theo kết quả validation được ghi trong báo cáo V1. Xác suất toxic được so với các ngưỡng khảo sát; ngưỡng cuối là 0,52. Điểm từ 0,52 trở lên được gán nhãn 1.')
b('Nhánh SVM tối ưu riêng','Nếu trình bày kết quả 68,86%, cần nêu thêm luồng chuẩn hóa viết tắt, TF-IDF từ/ký tự và hiệu chỉnh ngưỡng bằng OOF trên train. Đây là thí nghiệm bổ sung, không phải một trong bốn baseline.')

page();h('3.4.5 Đánh giá và kiểm tra đầu ra V1',2)
b('Tạo bảng dự đoán','Giữ id và nhãn thật của từng bình luận, bổ sung nhãn dự đoán và điểm nếu có. Sau đó dùng các hàm đánh giá của scikit-learn để tính chỉ số và confusion matrix.')
b('Kiểm tra dữ liệu','Đối chiếu giao của post_id giữa các tập, ID trùng và văn bản đầu vào trùng theo quy tắc chuẩn hóa. Tổng mẫu sau chia phải bằng 8.595; nhãn của mỗi ID phải được bảo toàn.')
b('Kiểm tra kết quả','Đủ 1.277 dự đoán validation; không thiếu hoặc lặp ID; tổng TN, FP, FN và TP bằng 1.277. Mỗi giá trị trong bảng kết quả phải truy được về đúng lượt chạy và tập đánh giá.')
b('Tái lập mô hình','Với pipeline đã lưu, kiểm tra tải lại và chạy trên cùng đầu vào. Các lượt SVM tối ưu có ghi nhận kiểm tra tái lập; những kiểm tra chưa có biên bản không được xem là đã nghiệm thu hoàn tất.')
b('Sản phẩm cần bàn giao','Pipeline hoặc checkpoint, cấu hình được chọn, bảng dự đoán, chỉ số đánh giá và lịch sử huấn luyện nếu có. Tên phiên bản dữ liệu phải đi kèm kết quả.')
table('Bảng 3.3 Kết quả bốn baseline trên validation V1 đơn vị phần trăm',['Mô hình','Accuracy','F1-toxic','Recall-toxic','Macro-F1'],[
['BoW + NB','93,19','32,56','25,30','64,49'],['BoW + SVM','92,64','36,49','32,53','66,29'],['TF-IDF + NB','93,50','2,35','1,20','49,50'],['TF-IDF + SVM','89,43','40,00','54,22','67,10']],[5,2.8,2.8,3,2.9])
h('3.4.6 Nhận xét sau V1',2)
b('Kết quả quan sát','Trong bốn baseline, TF-IDF + SVM có Macro-F1 cao nhất, đạt 67,10%. PhoBERT được báo cáo đạt 68,88% sau chọn ngưỡng 0,52; đây vẫn là điểm validation dùng trong lựa chọn.')
b('Hạn chế','Các mô hình còn bỏ sót toxic và kết quả mới phản ánh một lần chia cố định. V2 được thực hiện để khảo sát một thiết lập có nhiều dữ liệu train hơn.')
b('Phạm vi sử dụng kết quả','Các bảng dự đoán và lịch sử PhoBERT hiện nằm trong thư mục V1 có dấu hiệu đã được thay bằng V2. Khi bổ sung hình V1 cần dùng đúng bản lưu của lượt V1; không lấy lịch sử 824 câu để minh họa validation 1.277 câu.')

page();h('3.5 Quy trình thực nghiệm V2')
h('3.5.1 Mục tiêu và những bước thay đổi',2)
b('Mục tiêu','Khảo sát kết quả khi tăng tỷ lệ train. Nhóm vẫn sử dụng 8.595 bình luận đã gán nhãn, nhưng chia lại theo mục tiêu 80/10/10.')
pipeline('v2','Hình 3.7 Pipeline thực nghiệm V2',[
'1. Giữ corpus đã chốt\n8.595 bình luận\nKhông thay nhãn',
'2. Chia lại theo post_id\nMục tiêu 80/10/10\nKiểm tra không trùng bài',
'3. Tạo đầu vào V2\nDùng lại tiền xử lý\nFit mới bộ đặc trưng',
'4. Huấn luyện lại\nBaseline và Word+Char\nFine-tune PhoBERT',
'5. Chọn trên validation\nSVM dùng ngưỡng 0\nPhoBERT chọn 0,90',
'6. Đánh giá và lưu\n824 dự đoán validation\nGiữ riêng test 926 câu'])
table('Bảng 3.4 Phân bố nhãn của bộ chia V2',['Tập','Số mẫu','Non-toxic','Toxic'],[['Train','6.845','6.400','445'],['Validation','824','770','54'],['Test','926','866','60']],[5,3.8,3.8,3.9])
b('Cách chọn bộ chia','Manifest V2 ghi seed 42 và 500 ứng viên chia. Bộ chia được kiểm tra về tỷ lệ mẫu, phân bố nhãn và ràng buộc nhóm; không lựa chọn theo mô hình nào đạt điểm cao nhất.')
b('Kiểm tra sau chia','Manifest ghi nhận không trùng post_id giữa các tập, bảo toàn toàn bộ ID và không có văn bản trùng giữa các tập theo kiểm tra đã dùng. Đây là kiểm tra dữ liệu, chưa phải đánh giá mô hình.')

page();h('3.5.2 Tạo đặc trưng và huấn luyện V2',2)
b('Kế thừa từ V1','Nhóm dùng lại quy tắc tiền xử lý ở mục 3.2. Bộ biểu diễn và mô hình được fit lại trên train V2; không dùng bộ từ vựng đã fit trên một bộ chia khác.')
b('Bốn baseline','Chạy lại các Pipeline BoW/TF-IDF kết hợp NB/SVM, khảo sát tham số và chọn bằng validation V2. Bảng kết quả chính chỉ giữ bốn baseline theo phạm vi trình bày.')
b('Word+Char SVM','ColumnTransformer tạo TF-IDF từ trên text_tokenized và TF-IDF char_wb 3–5 trên text_clean, sau đó ghép hai ma trận. LinearSVC học trên đặc trưng đã ghép.')
b('Chọn cấu hình cải tiến','Script thử lưới cấu hình và chọn theo validation. Cấu hình Word+Char được chọn có C=0,1 và trọng số lớp {0:1, 1:8}. Kiểm tra ba fold trên train được chạy sau lựa chọn, dùng để chẩn đoán bổ sung.')
b('Fine-tune PhoBERT','Tạo đầu vào bằng tokenizer rồi huấn luyện theo batch như V1. Sau mỗi epoch, tính Macro-F1 trên validation ở ngưỡng mặc định; lưu checkpoint tốt nhất, tương ứng epoch 4 trong V2.')
h('3.5.3 Hậu xử lý và đánh giá V2',2)
b('SVM','Lấy decision score và gán toxic khi điểm nằm phía toxic của ngưỡng 0. Không mô tả cấu hình này là dùng ngưỡng học từ OOF.')
b('PhoBERT','Áp softmax lên logits để lấy điểm toxic. Quét ngưỡng từ 0,10 đến 0,90, bước 0,02 trên validation của checkpoint đã chọn; ngưỡng 0,90 cho Macro-F1 cao nhất trong lưới khảo sát.')
b('Kiểm tra đầu ra','Bảng dự đoán phải có 824 mẫu, gồm 54 toxic thật. Với PhoBERT, confusion matrix có TN=748, FP=22, FN=21, TP=33; tổng bốn ô bằng 824.')
b('Đầu ra bàn giao','Lưu pipeline SVM, checkpoint/tokenizer PhoBERT, tham số/ngưỡng, lịch sử học, bảng quét ngưỡng và dự đoán validation. Test 926 câu được giữ cho bước đánh giá sau khi chốt lựa chọn.')
table('Bảng 3.5 Kết quả bốn baseline trên validation V2 đơn vị phần trăm',['Mô hình','Accuracy','F1-toxic','Recall-toxic','Macro-F1'],[['BoW + NB','94,42','51,06','44,44','74,05'],['BoW + SVM','94,90','54,35','46,30','75,82'],['TF-IDF + NB','93,93','21,88','12,96','59,36'],['TF-IDF + SVM','94,66','52,17','44,44','74,67']],[5,2.8,2.8,3,2.9])
b('Kết quả bổ sung','Word+Char SVM đạt Macro-F1 78,83%; PhoBERT đạt 78,88%. Hai kết quả gần nhau. V2 cao hơn V1 trên validation, nhưng chưa tách được tác động của tăng train vì tập đánh giá và cấu hình cũng đổi.')

page();h('3.6 Quy trình thực nghiệm V3')
h('3.6.1 Tạo pool và chia năm fold',2)
b('Mục tiêu','Quan sát độ biến động giữa các nhóm bài viết, đồng thời so sánh SVM và PhoBERT trên cùng các fold.')
pipeline('v3','Hình 3.8 Pipeline kiểm định chéo V3',[
'1. Gộp train + validation\npandas.concat\n7.669 câu; 95 bài',
'2. Gán fold theo nhóm\nStratifiedGroupKFold\n5 fold; seed 42',
'3. Lặp fold k = 0…4\nTrain: fold khác k\nĐánh giá: fold k',
'4. Fit riêng từng lượt\nSVM và PhoBERT\nLưu mô hình mỗi fold',
'5. Ghép OOF theo ID\nMỗi mẫu một dự đoán\nChọn ngưỡng PhoBERT',
'6. Tổng hợp và kiểm tra\nĐiểm fold; điểm OOF\nKhông gộp test vào pool'])
b('Đầu vào','Gộp train và validation V2 thành pool 7.669 câu, trong đó có 499 toxic. Test V2 gồm 926 câu được giữ riêng; pool có 95 bài viết.')
b('Công cụ và cách chia','Dùng StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=42), truyền label để xét phân bố lớp và post_id làm nhóm. Cột fold lưu số 0–4 cho từng mẫu.')
b('Kiểm tra đã có trong script','So sánh giao post_id giữa mọi cặp fold và giữa pool với test. Script dừng bằng assertion nếu phát hiện trùng bài.')
b('Đầu ra','Một bảng dữ liệu chứa id, post_id, nội dung, nhãn và fold, cùng manifest thống kê/hash. SVM và PhoBERT cùng đọc bảng chia này để tránh so sánh trên các fold khác nhau.')

page();h('3.6.2 Huấn luyện trong từng fold',2)
table('Bảng 3.6 Các thao tác trong một lượt kiểm định V3',['Bước','Cách thực hiện','Sản phẩm'],[
['Lấy dữ liệu lượt k','Chọn fold khác k cho train, fold bằng k cho validation; giữ lại ID và vị trí dòng.','Train/validation của lượt k'],
['Fit SVM','Tạo pipeline mới; fit vectorizer và LinearSVC trên train của lượt k; dự đoán validation.','Nhãn và decision score'],
['Fine-tune PhoBERT','Khởi tạo mô hình cho lượt học riêng; huấn luyện trên train, theo dõi Macro-F1 của fold đánh giá để chọn checkpoint.','Checkpoint và xác suất fold'],
['Lưu kết quả','Lưu mô hình, chỉ số fold và dự đoán tại các vị trí validation tương ứng.','Artifact theo fold'],
['Lặp lại','Thực hiện đủ năm lượt, mỗi fold lần lượt làm phần đánh giá.','Năm bộ mô hình và dự đoán']],[3.2,9.1,4.2])
b('Cấu hình SVM kết hợp','Trong script V3, nhánh từ dùng TF-IDF 1–2, nhánh char_wb dùng 3–5; C=0,1, trọng số lớp {0:1, 1:8}. Các bộ đặc trưng được fit mới trong từng lượt.')
b('Lưu ý về checkpoint','Fold đánh giá cũng được dùng để chọn checkpoint PhoBERT. Vì vậy, việc mẫu không nằm trong train chưa có nghĩa kết quả hoàn toàn độc lập với bước lựa chọn.')
h('3.6.3 Ghép OOF và hậu xử lý',2)
b('Ghép dự đoán','Đưa điểm của fold đánh giá về đúng vị trí của từng mẫu trong pool. Sau năm lượt, mỗi mẫu cần có đúng một dự đoán từ lượt không dùng mẫu đó để huấn luyện.')
b('Ngưỡng SVM','Nhãn OOF được lấy từ pipeline.predict, tương ứng ngưỡng decision score mặc định 0.')
b('Ngưỡng PhoBERT','Quét xác suất OOF từ 0,20 đến dưới 0,95, bước 0,05. Ngưỡng được chọn là 0,85; áp dụng ngưỡng này để tạo nhãn và tính điểm OOF cuối.')
b('Hai cách tổng hợp','Tính mean ± độ lệch chuẩn từ các chỉ số từng fold; đồng thời tính chỉ số một lần trên toàn bộ nhãn OOF. Điểm fold PhoBERT và OOF cuối còn khác nhau về ngưỡng sử dụng.')

page();h('3.6.4 Kiểm tra đầu ra và kết quả V3',2)
b('Tiêu chí kiểm tra bảng OOF','Có đủ 7.669 ID, không lặp ID và không thiếu dự đoán. Nhãn thật phải khớp dữ liệu nguồn; mỗi dòng mang đúng fold đánh giá và đúng dự đoán tương ứng.')
b('Tiêu chí kiểm tra so sánh','SVM và PhoBERT dùng cùng ID, nhãn và fold. Tổng các ô confusion matrix phải bằng 7.669, trong đó có 499 mẫu toxic thật.')
b('Kiểm tra mô hình lưu','Cần đủ cấu hình và artifact cho năm lượt. Trước khi nghiệm thu, tải lại checkpoint/pipeline bằng đúng bộ tiền xử lý và đối chiếu với dự đoán đã lưu; đây là tiêu chí cần xác nhận, không mặc định đã hoàn thành cho mọi artifact.')
table('Bảng 3.7 Tổng hợp kết quả V3',['Nội dung','Word+Char SVM','PhoBERT'],[['Macro-F1 theo fold (%)','68,94 ± 1,42','71,16 ± 2,39'],['Macro-F1 OOF (%)','68,98','71,22'],['Recall-toxic OOF (%)','34,67','44,89'],['TN / FP','7.005 / 165','6.921 / 249'],['FN / TP','326 / 173','275 / 224']],[6.5,5,5])
b('Nhận xét','PhoBERT có Macro-F1 trung bình cao hơn 2,22 điểm phần trăm. Trên OOF, tổng TP cao hơn 51 câu nhưng FP cũng cao hơn 84 câu; khả năng phát hiện tăng đi kèm nhiều cảnh báo nhầm hơn.')
h('3.6.5 Ensemble và đánh giá cuối',2)
b('Luồng ensemble','Với một câu mới, áp dụng cùng tiền xử lý và tokenizer, lấy xác suất toxic từ năm mô hình rồi tính trung bình. So điểm trung bình với ngưỡng để trả nhãn cuối.')
b('Phân biệt với OOF','Một mẫu OOF được dự đoán bởi mô hình của lượt giữ mẫu đó ngoài train; không lấy trung bình năm mô hình trên chính pool để gọi là OOF, vì các mô hình khác có thể đã học mẫu đó.')
b('Bước đánh giá còn cần thực hiện','Chốt mô hình hoặc ensemble và ngưỡng trước khi chấm test 926 câu. Điểm OOF hiện có không phải kết quả test của ensemble; cần kiểm tra riêng việc dùng ngưỡng OOF cho ensemble.')

page();h('3.7 Tổng hợp và nghiệm thu quy trình')
h('3.7.1 Những điểm đạt được',2)
b('Về cách tổ chức','Mỗi lượt thực nghiệm có dữ liệu đầu vào, cấu hình, mô hình và bảng dự đoán tương ứng. Nhờ đó, kết quả có thể được đối chiếu ngược về các bước đã thực hiện.')
b('Về dữ liệu','Chia nguyên bài viết giúp hạn chế việc dùng chung ngữ cảnh giữa train và tập đánh giá. V3 dùng chung bảng fold cho các mô hình nên việc so sánh theo fold rõ ràng hơn.')
b('Về mô hình','Đặc trưng từ/ký tự bổ sung cho nhau trong các thí nghiệm SVM. PhoBERT có Macro-F1 cao hơn trong V3, còn SVM tạo ít cảnh báo nhầm hơn ở kết quả OOF đã quan sát.')
h('3.7.2 Những giới hạn cần ghi nhận',2)
b('Khác nhau giữa các phiên bản','V1 và V2 đổi cả dữ liệu trong từng tập và cấu hình. Vì vậy, chưa thể quy toàn bộ chênh lệch điểm cho việc tăng tỷ lệ train.')
b('Ảnh hưởng của việc lựa chọn','Validation được dùng chọn nhiều cấu hình; trong V3, fold đánh giá được dùng chọn checkpoint và OOF được dùng chọn ngưỡng. Cần đánh giá độc lập hơn trước khi kết luận về dữ liệu mới.')
b('Chất lượng phát hiện','PhoBERT vẫn bỏ sót 275/499 toxic trong OOF; chưa phù hợp để tự động xử lý mọi bình luận. Mô hình nên hỗ trợ con người rà soát.')
h('3.7.3 Tiêu chí nghiệm thu trước bàn giao',2)
table('Bảng 3.8 Nội dung cần xác nhận khi nghiệm thu',['Hạng mục','Điều kiện kiểm tra'],[['Dữ liệu','Đúng phiên bản, đúng số mẫu, không trùng bài giữa các phần cần tách.'],['Cấu hình','Ghi rõ bộ chia, tham số, checkpoint, cách tiền xử lý và ngưỡng.'],['Dự đoán','Đủ ID, đúng nhãn thật; confusion matrix và bảng chỉ số khớp nhau.'],['Mô hình lưu','Nạp được bằng đúng môi trường; dự đoán tải lại khớp kết quả tham chiếu.'],['Đánh giá cuối','Chốt lựa chọn trước khi chấm; phân biệt validation, OOF và test.']],[4.2,12.3])
p('Các kiểm tra rò rỉ dữ liệu đã có trong script/manifest cần được giữ cùng sản phẩm bàn giao. Những tiêu chí chưa có log hoặc biên bản xác nhận phải được kiểm tra bổ sung trước khi gọi là đã nghiệm thu.')

page();h('3.8 Luồng triển khai và kiểm tra demo')
p('Demo sử dụng mô hình đã huấn luyện để minh họa quá trình từ câu nhập đến nhãn dự đoán. Luồng nghiệm thu dưới đây xác định những bước cần đối chiếu khi chạy ứng dụng; không mặc định mọi chức năng hiện tại đã đáp ứng đầy đủ.')
table('Bảng 3.9 Pipeline suy luận trên demo',['Bước','Cách thực hiện','Đầu ra cần quan sát'],[['1. Nạp tài nguyên','Nạp pipeline SVM hoặc checkpoint/tokenizer PhoBERT và cấu hình ngưỡng.','Tên mô hình và trạng thái nạp'],['2. Nhận đầu vào','Đọc câu người dùng nhập, kiểm tra câu rỗng hoặc không hợp lệ.','Văn bản đầu vào hợp lệ'],['3. Tiền xử lý','Dùng lại các hàm và quy tắc tương ứng khi huấn luyện.','Văn bản chuẩn hóa/tách từ'],['4. Suy luận','SVM gọi decision_function/predict; PhoBERT chạy ở chế độ đánh giá, không cập nhật gradient.','Decision score hoặc điểm softmax'],['5. Hậu xử lý','So điểm với ngưỡng của mô hình; chuyển thành nhãn 0/1.','Toxic hoặc non-toxic'],['6. Kiểm tra hiển thị','Đối chiếu nhãn, điểm và ngưỡng; phân biệt lỗi chạy với kết quả phân loại.','Kết quả có thể giải thích và đối chiếu']],[3.2,9.1,4.2])
b('Kiểm tra bằng câu mẫu','Dùng câu bình thường, câu công kích rõ và câu khó. Nếu có nhãn tham chiếu, đối chiếu với dự đoán; một vài câu demo không thay thế độ đo trên tập đánh giá.')
b('Kiểm tra ngưỡng','Giữ nguyên câu và mô hình rồi đổi ngưỡng. Điểm phải giữ nguyên nếu đường suy luận không thay đổi; nhãn chỉ đổi khi điều kiện so ngưỡng thay đổi.')
b('Kiểm tra nhất quán','Cùng đầu vào và cùng cấu hình cần cho kết quả phù hợp với lượt suy luận ngoài giao diện. Nếu nạp hoặc suy luận lỗi, phải nhận biết được trạng thái đó trước khi giới thiệu kết quả là đầu ra của mô hình.')
h('3.9 Hướng hoàn thiện',1)
b('Ưu tiên đánh giá','Hoàn tất kiểm tra tải lại mô hình và chấm test cho lựa chọn cuối. Với V3, có thể dùng validation nội bộ để chọn checkpoint/ngưỡng, tách khỏi fold chấm ngoài.')
b('Ưu tiên dữ liệu','Bổ sung có chọn lọc toxic, rà soát câu mơ hồ và đánh giá trên bài viết ở thời điểm mới. Sau mỗi thay đổi, giữ giao thức cố định để xác định tác động rõ hơn.')
f=s.footer.paragraphs[0];f.alignment=WD_ALIGN_PARAGRAPH.CENTER;e=OxmlElement('w:fldSimple');e.set(qn('w:instr'),'PAGE');f._p.append(e)
out=O/'Chuong_3_PIPELINE_V1_V2_V3.docx';d.save(out)
print(out);print('Tables',len(d.tables),'Diagrams',len(d.inline_shapes))
