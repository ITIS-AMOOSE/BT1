from pathlib import Path
from docx import Document
from docx.shared import Cm,Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from PIL import Image,ImageDraw,ImageFont
R=Path('E:/BT1/output/word')
d=Document(R/'Chuong_3_CACH_LAM_VA_DAY_DU_BIEU_DO.docx')
def replace(p,text,boldlead=False):
 for run in list(p.runs):run._element.getparent().remove(run._element)
 if boldlead and ': ' in text:
  a,b=text.split(': ',1);p.add_run(a+': ').bold=True;p.add_run(b)
 else:p.add_run(text)
def find(prefix):return next(p for p in d.paragraphs if p.text.startswith(prefix))
def before(target,text,style='List Bullet'):
 p=d.add_paragraph(style=style);replace(p,text,style=='List Bullet');target._p.addprevious(p._p);return p
replace(find('3.4.1 '),'3.4.1 Mục tiêu và các mô hình sử dụng')
inp=find('Đầu vào:')
for text in [
 'Mục tiêu: V1 được thực hiện để xây dựng kết quả ban đầu, làm cơ sở đối chiếu các phương pháp và xác định những điểm cần cải thiện ở các giai đoạn sau.',
 'Các mô hình truyền thống: Nhóm kết hợp hai cách biểu diễn BoW và TF-IDF với Naive Bayes và SVM, tạo thành bốn baseline: BoW + Naive Bayes, TF-IDF + Naive Bayes, BoW + SVM và TF-IDF + SVM.',
 'Nhánh PhoBERT: Nhóm sử dụng mô hình tiếng Việt đã được tiền huấn luyện, sau đó điều chỉnh bằng dữ liệu có nhãn của đề tài để phân loại toxic và non-toxic.',
 'Lý do lựa chọn: Bốn baseline giúp so sánh ảnh hưởng của cách biểu diễn văn bản và thuật toán phân loại. PhoBERT bổ sung cách tiếp cận dựa trên ngữ cảnh, qua đó cho phép đối chiếu với các mô hình truyền thống trên cùng tập xác thực.',
 'Quy trình thực hiện: Sau khi xác định các mô hình, nhóm lần lượt chuẩn bị và chia dữ liệu, biểu diễn văn bản, huấn luyện, chọn cấu hình và ngưỡng, rồi đánh giá và kiểm tra đầu ra như sơ đồ dưới đây.'
]:before(inp,text)
# Place data preparation after the overview diagram.
step1=find('Bước 1 – Chia dữ liệu:')
before(step1,'3.4.2 Chuẩn bị và chia dữ liệu',style='Heading 2')
step1._p.addprevious(inp._p)
replace(find('3.4.2 Biểu diễn'),'3.4.3 Biểu diễn văn bản và huấn luyện')
replace(find('Bước 3 – Chuẩn bị đầu vào:'),
 'Bước 3 – Biểu diễn văn bản: Từ các tập dữ liệu đã chuẩn bị, nhóm chuyển văn bản thành dạng phù hợp với từng mô hình. Các bước chuẩn hóa và tách từ được kế thừa từ mục 3.2, không thực hiện lại một quy trình tiền xử lý khác.',True)
replace(find('3.4.3 Lựa chọn'),'3.4.4 Lựa chọn mô hình và hậu xử lý')
before(find('Bước 6 – Đối chiếu kết quả:'),'3.4.5 Đánh giá và kiểm tra đầu ra',style='Heading 2')
# Add the model scope before execution in later versions too.
before(find('Bước 1 – Chia lại dữ liệu:'),
 'Các mô hình sử dụng: V2 giữ bốn baseline và nhánh PhoBERT của V1, đồng thời khảo sát thêm SVM kết hợp đặc trưng từ và ký tự. Nhóm huấn luyện lại các mô hình trên bộ chia mới để so sánh trong cùng điều kiện đánh giá.')
before(find('Bước 1 – Tạo phần dữ liệu phát triển:'),
 'Các mô hình sử dụng: V3 tập trung đối chiếu BoW + SVM, TF-IDF + SVM, SVM kết hợp từ với ký tự và PhoBERT. Tất cả dùng chung cách chia năm phần để kết quả từng lượt có thể so sánh trực tiếp.')
# Update the V1 diagram so that its first step matches the new introduction.
im=Image.new('RGB',(1600,760),'white');dr=ImageDraw.Draw(im);ft=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',29)
steps=['1. Xác định mô hình\nBốn baseline truyền thống\nNhánh PhoBERT',
'2. Chuẩn bị và chia tập\nKế thừa dữ liệu mục 3.2\nChia theo bài 70/15/15',
'3. Biểu diễn văn bản\nBoW hoặc TF-IDF\nMã hóa cho PhoBERT',
'4. Huấn luyện mô hình\nHọc trên tập huấn luyện\nThử các cấu hình',
'5. Lựa chọn và phân loại\nĐánh giá trên xác thực\nChọn mô hình và ngưỡng',
'6. Kiểm tra kết quả\nĐối chiếu nhãn thật\nLưu mô hình và dự đoán']
for i,text in enumerate(steps):
 x=30+(i%3)*530;y=30+(i//3)*365
 dr.rounded_rectangle((x,y,x+470,y+255),radius=12,fill='#F2F5F8',outline='#385A75',width=3)
 for n,line in enumerate(text.split('\n')):
  box=dr.textbbox((0,0),line,font=ft);dr.text((x+235-(box[2]-box[0])/2,y+30+n*49),line,font=ft,fill='#142C40')
 if i%3<2:
  dr.line((x+480,y+125,x+515,y+125),fill='#385A75',width=5)
  dr.polygon([(x+515,y+125),(x+502,y+117),(x+502,y+133)],fill='#385A75')
# Connect step 3 to step 4 through the gap between rows.
dr.line([(1565,155),(1585,155),(1585,340),(15,340),(15,520),(30,520)],fill='#385A75',width=3)
dr.polygon([(30,520),(20,513),(20,527)],fill='#385A75')
dr.text((35,704),'Trình tự từ bước 1 đến bước 6; các nhánh dùng chung cách chia dữ liệu.',font=ft,fill='#334155')
path=R/'pipeline_figures/v1_gioi_thieu_mo_hinh.png';im.save(path,dpi=(200,200))
imagepar=next(p for p in d.paragraphs if p._p.findall('.//'+qn('w:drawing')))
for run in list(imagepar.runs):run._element.getparent().remove(run._element)
imagepar.add_run().add_picture(str(path),width=Cm(16))
out=R/'Chuong_3_CO_GIOI_THIEU_MO_HINH.docx';d.save(out)
c=Document(out)
assert len(c.inline_shapes)==12 and len(c.tables)==5
assert not any('Bước 3 – Chuẩn bị đầu vào:' in p.text for p in c.paragraphs)
assert len([p for p in c.paragraphs if p.text.startswith('3.4.2 ')])==1
print(out);print('Preserved 12 images and 5 tables. New model introduction and V1 sections 3.4.1–3.4.5.')
