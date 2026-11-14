from pathlib import Path
from docx import Document
r=Path('E:/BT1/output/word')
d=Document(r/'Chuong_3_V1_DU_5_MO_HINH_VA_CONFUSION_MATRIX.docx')
def before(prefix,label,body):
 target=next(p for p in d.paragraphs if p.text.startswith(prefix))
 p=d.add_paragraph(style='List Bullet');p.add_run(label+': ').bold=True;p.add_run(body)
 target._p.addprevious(p._p)
before('Nhánh PhoBERT: Văn bản đã tách từ',
 'Thử nghiệm bổ sung với SVM',
 'Bên cạnh bốn baseline, nhóm thử chuẩn hóa một số từ viết tắt và kết hợp TF-IDF theo từ với TF-IDF theo ký tự để huấn luyện SVM. Nhóm khảo sát độ dài cụm từ, việc loại từ dừng có chọn lọc và ngưỡng phân loại; các cấu hình được đối chiếu trên tập xác thực.')
before('3.4.5 Đánh giá và kiểm tra đầu ra',
 'Cấu hình SVM cải tiến',
 'Cấu hình được chọn dùng cụm từ từ một đến ba từ, kết hợp đặc trưng ký tự và loại một danh sách từ dừng nhỏ ở nhánh từ. Ngưỡng được chọn từ dự đoán ngoài mẫu trên tập huấn luyện, khoảng −0,00295; ngưỡng này khác ngưỡng mặc định 0 của SVM baseline.')
before('3.5 Thực nghiệm V2',
 'Kết quả SVM cải tiến ở V1',
 'Thí nghiệm bổ sung đạt Macro-F1 68,86%, F1-toxic 42,33% và Recall-toxic 48,19%. So với baseline TF-IDF + SVM, Macro-F1 tăng khoảng 1,76 điểm phần trăm, nhưng Recall-toxic giảm từ 54,22% xuống 48,19%. PhoBERT đạt Macro-F1 68,88%, gần tương đương SVM cải tiến. Đây là kết quả bổ sung, tách khỏi bảng và hình của bốn baseline cùng PhoBERT ở trên.')
out=r/'Chuong_3_BO_SUNG_NGAN_SVM_CAI_TIEN_V1.docx';d.save(out)
c=Document(out)
assert len(c.inline_shapes)==16 and len(c.tables)==5
assert any(p.text.startswith('Kết quả SVM cải tiến ở V1:') for p in c.paragraphs)
print(out)
