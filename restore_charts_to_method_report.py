from pathlib import Path
from docx import Document
from docx.shared import Cm,Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
R=Path('E:/BT1/output/word');A=R/'figures_results'
d=Document(R/'Chuong_3_MO_TA_CACH_LAM_BANG_LOI.docx')
def add(before,file,caption,comment):
 target=next(p for p in d.paragraphs if p.text==before)
 p=d.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER
 p.paragraph_format.space_before=Pt(10);p.paragraph_format.keep_with_next=True
 p.add_run().add_picture(str(A/file),width=Cm(16));target._p.addprevious(p._p)
 p=d.add_paragraph(caption,style='Caption');p.alignment=WD_ALIGN_PARAGRAPH.CENTER
 p.paragraph_format.keep_with_next=True;target._p.addprevious(p._p)
 p=d.add_paragraph(style='List Bullet');p.add_run('Nhận xét: ').bold=True;p.add_run(comment)
 target._p.addprevious(p._p)
add('3.5 Thực nghiệm V2','v1_metrics.png','So sánh các chỉ số trên tập xác thực V1',
 'Hình đối chiếu các baseline với nhánh SVM cải tiến và PhoBERT. Hai nhánh cuối có Macro-F1 gần nhau, nhưng Recall-toxic khác nhau; cần xem cả khả năng phát hiện và số báo nhầm thay vì chỉ nhìn cột cao nhất.')
add('3.5 Thực nghiệm V2','v1_cm.png','Ma trận nhầm lẫn của SVM cải tiến và PhoBERT trên tập xác thực V1',
 'PhoBERT báo nhầm ít hơn SVM 10 câu nhưng phát hiện đúng ít hơn 3 câu toxic. Ma trận này thuộc thí nghiệm SVM cải tiến bổ sung, không phải một trong bốn baseline của bảng trước.')
add('3.6 Thực nghiệm V3','v2_metrics.png','So sánh các chỉ số trên tập xác thực V2',
 'Word+Char SVM đạt Macro-F1 cao hơn các baseline, trong khi kết quả của mô hình này và PhoBERT gần tương đương. Các chỉ số trong hình được tính trên cùng 824 bình luận xác thực.')
add('3.6 Thực nghiệm V3','v2_cm.png','Ma trận nhầm lẫn của hai mô hình trên tập xác thực V2',
 'PhoBERT phát hiện đúng 33 trong 54 câu toxic, nhiều hơn SVM 1 câu, nhưng đồng thời báo nhầm thêm 2 câu non-toxic. Tổng bốn ô của mỗi ma trận bằng 824 bình luận.')
add('3.6 Thực nghiệm V3','v2_loss.png','Diễn biến loss trong quá trình huấn luyện PhoBERT V2',
 'Loss huấn luyện tiếp tục giảm, trong khi loss xác thực tăng sau lượt thứ 2. Nhóm vẫn chọn mô hình ở lượt thứ 4 theo Macro-F1, bởi loss và F1 phản ánh những khía cạnh khác nhau của dự đoán.')
add('3.6 Thực nghiệm V3','v2_tau.png','Ảnh hưởng của ngưỡng đến kết quả phân loại PhoBERT V2',
 'Khi tăng ngưỡng, điều kiện gán toxic chặt hơn nên mô hình có thể giảm báo nhầm nhưng bỏ sót thêm. Ngưỡng 0,90 cho Macro-F1 cao nhất trong các giá trị đã khảo sát trên tập xác thực này.')
add('3.6.4 Kiểm tra và chuẩn bị đánh giá cuối','v3_fold.png','Macro-F1 của SVM và PhoBERT qua năm lượt đánh giá V3',
 'PhoBERT cao hơn ở cả năm lượt đã chạy, nhưng khoảng cách thay đổi theo nhóm bài viết. Ở lượt thứ tư, tương ứng fold 3 trên hình, hai mô hình gần như ngang nhau.')
add('3.6.4 Kiểm tra và chuẩn bị đánh giá cuối','v3_oof.png','So sánh các chỉ số trên dự đoán ngoài mẫu V3',
 'PhoBERT có Macro-F1 và Recall-toxic cao hơn SVM kết hợp. Các điểm trong hình được tính trên toàn bộ dự đoán ngoài mẫu; với PhoBERT, nhãn được tạo sau khi chọn ngưỡng 0,85.')
add('3.6.4 Kiểm tra và chuẩn bị đánh giá cuối','v3_cm.png','Ma trận nhầm lẫn trên dự đoán ngoài mẫu V3',
 'PhoBERT có tổng số toxic phát hiện đúng cao hơn 51 câu, nhưng báo nhầm cũng cao hơn 84 câu so với SVM. Mỗi ma trận được tính trên cùng 7.669 bình luận, gồm 499 câu toxic.')
# Number all figures in reading order, following the five figures in sections 3.1–3.3.
counter=5
for p in d.paragraphs:
 if p.style.name=='Caption' and not p.text.startswith('Bảng '):
  counter+=1;text=p.text
  if text.startswith('Hình '):text=text.split(' ',2)[2]
  p.text=f'Hình 3.{counter} {text}'
  p.alignment=WD_ALIGN_PARAGRAPH.CENTER
for table in d.tables:
 node=table._tbl.getnext()
 while node is not None:
  from docx.oxml.ns import qn
  from docx.text.paragraph import Paragraph
  if node.tag!=qn('w:p'):break
  p=Paragraph(node,d._body)
  if p.text or node.findall('.//'+qn('w:drawing')):
   p.paragraph_format.space_before=Pt(12);break
  node=node.getnext()
out=R/'Chuong_3_CACH_LAM_VA_DAY_DU_BIEU_DO.docx';d.save(out)
check=Document(out)
assert len(check.inline_shapes)==12
assert len(check.tables)==5
assert not any(p.text.startswith('Nguồn:') for p in check.paragraphs)
print(out);print('12 figures: 3 pipelines and 9 restored result charts. All 5 tables retained.')
