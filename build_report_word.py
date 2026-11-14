from pathlib import Path
import csv,json,statistics
from docx import Document
from docx.shared import Cm,Pt,RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from PIL import Image,ImageDraw,ImageFont

R=Path('E:/BT1'); O=R/'output/word'; O.mkdir(parents=True,exist_ok=True)
def rows(p):
    with open(R/p,encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def js(p):return json.loads((R/p).read_text(encoding='utf-8-sig'))
d=Document(); sec=d.sections[0]; sec.page_width=Cm(21);sec.page_height=Cm(29.7)
sec.top_margin=Cm(2);sec.bottom_margin=Cm(2);sec.left_margin=Cm(2.5);sec.right_margin=Cm(2)
for name in ['Normal','Title','Heading 1','Heading 2','Heading 3','Caption']:
 s=d.styles[name];s.font.name='Times New Roman';s.font.color.rgb=RGBColor(0,0,0)
 s.font.size=Pt(13 if name=='Normal' else 14 if name!='Title' else 18)
 s.paragraph_format.space_after=Pt(6)
d.styles['Normal'].paragraph_format.line_spacing=1.3
d.styles['Normal'].paragraph_format.alignment=WD_ALIGN_PARAGRAPH.JUSTIFY
for name in ['Heading 1','Heading 2','Heading 3']:d.styles[name].paragraph_format.keep_with_next=True
def p(t):return d.add_paragraph(t)
def h(t,lev=1):return d.add_heading(t,lev)
def page():d.add_page_break()
def table(title,heads,data):
 c=d.add_paragraph(title,style='Caption');c.paragraph_format.keep_with_next=True
 t=d.add_table(rows=1, cols=len(heads));t.autofit=False
 widths=[5]+[(16.5-5)/(len(heads)-1)]*(len(heads)-1)
 for row,vals in [(t.rows[0],heads)]+[(t.add_row(),x) for x in data]:
  for i,(cell,val) in enumerate(zip(row.cells,vals)):
   cell.width=Cm(widths[i]);cell.text=str(val)
   for par in cell.paragraphs:
    par.paragraph_format.line_spacing=1.05;par.paragraph_format.space_after=Pt(5);par.paragraph_format.space_before=Pt(5)
    par.alignment=WD_ALIGN_PARAGRAPH.LEFT if i==0 else WD_ALIGN_PARAGRAPH.CENTER
    for run in par.runs:run.font.size=Pt(10.5)
   pr=cell._tc.get_or_add_tcPr();b=OxmlElement('w:tcBorders')
   for edge in ['top','left','bottom','right']:
    z=OxmlElement('w:'+edge);z.set(qn('w:val'),'single');z.set(qn('w:sz'),'4');z.set(qn('w:color'),'D9D9D9');b.append(z)
   pr.append(b)
 for cell in t.rows[0].cells:
  sh=OxmlElement('w:shd');sh.set(qn('w:fill'),'E7E6E6');cell._tc.get_or_add_tcPr().append(sh)
  for run in cell.paragraphs[0].runs:run.bold=True
 hdr=OxmlElement('w:tblHeader');t.rows[0]._tr.get_or_add_trPr().append(hdr)
 p('')
def fig(path,cap):
 par=d.add_paragraph();par.alignment=WD_ALIGN_PARAGRAPH.CENTER;par.paragraph_format.keep_with_next=True
 par.add_run().add_picture(str(path),width=Cm(16))
 c=d.add_paragraph(cap,style='Caption');c.alignment=WD_ALIGN_PARAGRAPH.CENTER
def note(t):
 z=p(t);z.paragraph_format.line_spacing=1.1
 for r in z.runs:r.italic=True;r.font.size=Pt(10)
def chart(file,title,names,values):
 im=Image.new('RGB',(1500,650),'white');dr=ImageDraw.Draw(im)
 ft=ImageFont.truetype('C:/Windows/Fonts/times.ttf',29);sm=ImageFont.truetype('C:/Windows/Fonts/times.ttf',25)
 dr.text((45,18),title,font=ft,fill='black')
 for i,(n,v) in enumerate(zip(names,values)):
  y=100+i*95;dr.text((30,y+10),n,font=sm,fill='black');dr.rectangle((400,y,400+int(v*11),y+45),fill=(48,95,135));dr.text((415+int(v*11),y+7),f'{v:.2f}%',font=sm,fill='black')
 dr.text((400,590),'Macro-F1 (%) - trục bắt đầu tại 0',font=sm,fill='black');im.save(O/file);return O/file

h('Thực nghiệm và kết quả phân loại bình luận toxic',0)
p('Phần báo cáo từ mục 3.4 đến hết trình bày quá trình thực nghiệm qua ba giai đoạn V1, V2 và V3. Nhóm lần lượt khảo sát thiết lập ban đầu, thay đổi tỷ lệ chia dữ liệu và kiểm định chéo theo bài viết. Các kết quả cho thấy đặc trưng từ kết hợp ký tự là một hướng cải tiến hữu ích; PhoBERT đạt Macro-F1 cao hơn SVM trong thiết lập năm fold, nhưng vẫn còn hạn chế khi phát hiện lớp toxic.')
h('3.4 Thực nghiệm V1')
h('3.4.1 Thiết lập và huấn luyện',2)
p('V1 sử dụng bộ chia resplit_v1, gồm 6.000 bình luận train, 1.277 bình luận validation và 1.318 bình luận test. Toàn bộ bình luận thuộc cùng một post_id được xếp trong cùng tập. Validation gồm 83 bình luận toxic và 1.194 bình luận non-toxic. Các mô hình được chọn theo Macro-F1 trên validation; các kết quả validation không được xem là điểm test.')
p('Nhóm xây dựng bốn baseline kết hợp BoW hoặc TF-IDF với Multinomial Naive Bayes hoặc Linear SVM, cùng DummyClassifier làm mốc tham chiếu. Nhánh SVM cải tiến kết hợp TF-IDF từ và ký tự, khảo sát chuẩn hóa viết tắt, n-gram, từ dừng có chọn lọc và ngưỡng quyết định học từ dự đoán ngoài mẫu trên train. Bộ từ vựng và trọng số IDF được học trong phần dữ liệu huấn luyện tương ứng.')
p('Cấu hình SVM được chọn ở bước steps23_v2 là slang_ng3_stop_oof: chuẩn hóa viết tắt, n-gram từ 1–3, nhánh ký tự, danh sách từ dừng có chọn lọc và ngưỡng OOF khoảng −0,00295. Giá trị C bằng 0,1 và class_weight="balanced". Ngưỡng và tham số thuộc cấu hình này không được mặc định áp dụng cho các thí nghiệm khác.')
p('Nhánh học sâu fine-tune checkpoint vinai/phobert-base-v2 cho hai nhãn. Cấu hình gồm max_length=128, batch_size=32, AdamW với learning rate 2×10⁻⁵, weight decay 0,01, warmup 10% và label smoothing 0,05. Checkpoint được lựa chọn bằng validation. Trong báo cáo này, V1/V2/V3 chỉ giai đoạn thực nghiệm; hậu tố base-v2 thuộc tên checkpoint PhoBERT, không phải tên giai đoạn.')
table('Bảng 3.1 Cấu hình và lựa chọn chính của V1',['Thành phần','Giá trị'],[['Train / validation / test','6.000 / 1.277 / 1.318'],['SVM cải tiến','slang_ng3_stop_oof'],['PhoBERT','vinai/phobert-base-v2'],['Checkpoint PhoBERT','Epoch 5'],['Ngưỡng PhoBERT','0,52 trên validation']])
note('Nguồn: reports/resplit_v1/steps23_v2/REPORT.md; reports/phobert/REPORT.md; reports/phobert/run_manifest.json.')
page();h('3.4.2 Kết quả trên validation',2)
v1=js('reports/resplit_v1/final_evaluation/results.json')
data=[]
names={'bow_nb':'BoW + NB','tfidf_nb':'TF-IDF + NB','bow_svm':'BoW + SVM','tfidf_svm':'TF-IDF + SVM','dummy':'Dummy'}
for m in v1['models']:
 q=m['validation'];data.append([names[m['model']]]+[f'{q[k]*100:.2f}' for k in ['accuracy','f1_toxic','recall_toxic','macro_f1']])
data += [['SVM cải tiến','91.46','42.33','48.19','68.86'],['PhoBERT τ=0,52','92.01','42.05','44.58','68.88']]
table('Bảng 3.2 Kết quả validation V1 đơn vị phần trăm',['Mô hình','Accuracy','F1 toxic','Recall toxic','Macro-F1'],data)
p('Dummy đạt Accuracy 93,50% nhưng không phát hiện được bình luận toxic nào. Điều này phản ánh ảnh hưởng của mất cân bằng nhãn và cho thấy Accuracy không thể là tiêu chí lựa chọn duy nhất. TF-IDF + NB có Accuracy tương tự nhưng Recall-toxic chỉ đạt 1,20%, tức phát hiện được 1 trong 83 câu toxic.')
p('Trong bốn baseline, TF-IDF + SVM có Macro-F1 cao nhất, đạt 67,10%. Sau tối ưu, SVM cải tiến đạt 68,86%, tăng khoảng 1,76 điểm phần trăm. PhoBERT đạt 68,88%, gần tương đương SVM cải tiến. Chênh lệch khoảng 0,02 điểm phần trăm chưa đủ để khẳng định một mô hình vượt trội.')
table('Bảng 3.3 Đối chiếu lỗi trên validation V1',['Mô hình','TN','FP','FN','TP'],[['SVM cải tiến',1128,66,43,40],['PhoBERT τ=0,52',1138,56,46,37]])
p('PhoBERT báo nhầm ít hơn SVM 10 câu nhưng cũng phát hiện đúng ít hơn 3 câu toxic. Hai mô hình có sự đánh đổi giữa báo nhầm và bỏ sót; không có mô hình đồng thời tốt hơn ở mọi chỉ số.')
h('3.4.3 Hạn chế và động cơ thực hiện V2',2)
p('Recall-toxic của cả hai mô hình vẫn dưới 50%. Số mẫu toxic dùng học còn ít và kết quả mới phản ánh một lần chia dữ liệu. Nhóm thực hiện V2 để khảo sát thiết lập tăng tỷ lệ dữ liệu dành cho train. Đây là động cơ thực nghiệm, không phải bằng chứng rằng kích thước train là nguyên nhân duy nhất gây ra hạn chế V1.')
note('Nguồn: results.json của baseline V1; manifest mô hình steps23_v2; báo cáo và bảng dự đoán PhoBERT V1. Chênh lệch chỉ số được biểu diễn bằng điểm phần trăm.')
page();h('3.5 Thực nghiệm V2')
h('3.5.1 Mục đích và thay đổi so với V1',2)
p('V2 sử dụng resplit_v2 với tỷ lệ mục tiêu 80/10/10. Số mẫu thực tế là 6.845 train, 824 validation và 926 test. Do chia nguyên theo bài viết, tỷ lệ thực tế có thể lệch nhẹ tỷ lệ mục tiêu. Validation V2 gồm 54 câu toxic và 770 câu non-toxic. Tổng số bình luận vẫn là 8.595; đây là thay đổi cách phân chia, không phải bổ sung một bộ dữ liệu độc lập.')
p('Các nhánh BoW, TF-IDF, Naive Bayes, SVM và PhoBERT tiếp tục được khảo sát. SVM từ kết hợp ký tự được chọn với C=0,1 và trọng số lớp {0:1, 1:8}; ngưỡng decision score giữ ở 0. PhoBERT giữ các tham số huấn luyện chính như V1, chọn checkpoint epoch 4 và quét ngưỡng trên validation, thu được τ=0,90.')
h('3.5.2 Kết quả trên validation',2)
dat=[]
for q in rows('reports/resplit_v2/improvements/validation_comparison.csv'):
 if 'model' in q and 'macro_f1' in q:
  dat.append([names.get(q['model'],q['model'])]+[f'{float(q[k])*100:.2f}' for k in ['accuracy','f1_toxic','recall_toxic','macro_f1']])
if not dat:
 dat=[['Dummy','93.45','0.00','0.00','48.31'],['TF-IDF + NB','93.93','21.88','12.96','59.36'],['BoW + NB','94.42','51.06','44.44','74.05'],['TF-IDF + SVM','94.66','52.17','44.44','74.67'],['BoW + SVM','94.90','54.35','46.30','75.82'],['SVM từ có trọng số','95.15','55.56','46.30','76.49'],['SVM ký tự','95.15','56.52','48.15','76.98'],['SVM từ + ký tự','94.90','60.38','59.26','78.83']]
dat.append(['PhoBERT τ=0,90','94.78','60.55','61.11','78.88'])
table('Bảng 3.4 Kết quả validation V2 đơn vị phần trăm',['Mô hình','Accuracy','F1 toxic','Recall toxic','Macro-F1'],dat)
p('SVM từ kết hợp ký tự đạt Macro-F1 78,83%, cao hơn BoW + SVM khoảng 3,00 điểm phần trăm. Số bỏ sót giảm từ 29 xuống 22, trong khi số báo nhầm tăng từ 13 lên 20. Kết quả cho thấy khả năng phát hiện toxic được cải thiện kèm chi phí tăng cảnh báo nhầm.')
p('PhoBERT đạt Macro-F1 78,88% và Recall-toxic 61,11%. So với SVM từ kết hợp ký tự, PhoBERT phát hiện đúng thêm 1 câu toxic nhưng báo nhầm thêm 2 câu. Chênh lệch Macro-F1 khoảng 0,05 điểm phần trăm là nhỏ, đặc biệt khi validation chỉ có 54 mẫu toxic.')
note('Nguồn: reports/resplit_v2/improvements/validation_report.md; reports/phobert_v2/best_metrics.json và REPORT.md. Tất cả kết quả ở bảng này thuộc validation, không phải test.')
page();h('3.5.3 Diễn biến huấn luyện và lựa chọn ngưỡng',2)
fig(R/'figures_chuong_3/Hinh_3_10_Duong_cong_huan_luyen_PhoBERT.png','Hình 3.1 Diễn biến huấn luyện PhoBERT trong V2 tại ngưỡng 0,50')
p('Train loss giảm từ khoảng 0,7704 xuống 0,5101 qua năm epoch. Validation loss thấp nhất khoảng 0,6993 tại epoch 2 rồi tăng lên. Trong khi đó, Macro-F1 tại ngưỡng 0,50 đạt cao nhất ở epoch 4, khoảng 77,26%. Vì tiêu chí lựa chọn là Macro-F1, nhóm sử dụng checkpoint epoch 4 thay vì chọn epoch có validation loss nhỏ nhất.')
p('Loss đánh giá mức phù hợp của phân phối dự đoán với nhãn, còn F1 đánh giá nhãn sau khi áp dụng ngưỡng. Một số dự đoán sai có độ tự tin tăng có thể khiến loss tăng, trong khi các thay đổi ở những mẫu khác vẫn giúp F1 tăng. Khoảng cách giữa train loss và validation loss là dấu hiệu cần theo dõi overfitting, không thể chỉ dựa vào train loss giảm để kết luận mô hình tốt hơn.')
p('Sau khi quét ngưỡng trên validation của checkpoint epoch 4, τ=0,90 cho Macro-F1 78,88%. Nâng ngưỡng từ 0,50 lên 0,90 làm TP giảm từ 39 xuống 33, FN tăng từ 15 lên 21, nhưng FP giảm từ 41 xuống 22. Nhờ giảm báo nhầm, F1-toxic tăng từ 58,21% lên 60,55%. Ngưỡng 0,90 là lựa chọn thực nghiệm trên tập này, không phải quy tắc chung cho PhoBERT.')
h('3.5.4 Đối chiếu V1 và V2 và hạn chế',2)
table('Bảng 3.5 Đối chiếu hai lần chia cố định',['Chỉ tiêu','V1','V2'],[['Train / validation / test','6.000 / 1.277 / 1.318','6.845 / 824 / 926'],['Toxic trong validation','83','54'],['Macro-F1 SVM cải tiến (%)','68,86','78,83'],['Macro-F1 PhoBERT (%)','68,88','78,88'],['Ngưỡng PhoBERT','0,52','0,90']])
p('V2 có điểm validation cao hơn V1, nhưng đồng thời thành phần train, validation, cấu hình SVM và ngưỡng đã thay đổi. Vì vậy, không thể quy toàn bộ mức tăng cho việc tăng tỷ lệ train. Sự khác biệt giữa các lần chia dẫn đến nhu cầu đánh giá trên nhiều nhóm bài viết ở V3.')
note('Nguồn hình: training_history.csv của PhoBERT V2; các giá trị ngưỡng cuối từ best_metrics.json. Hình phản ánh chỉ số trước quét ngưỡng nên Macro-F1 epoch 4 khác điểm cuối 78,88%.')
page();h('3.6 Thực nghiệm V3')
h('3.6.1 Mục đích và giao thức kiểm định chéo',2)
p('V3 khảo sát biến động hiệu năng qua nhiều nhóm bài viết thay vì chỉ dựa trên một tập validation cố định. Phần phát triển gồm 7.669 bình luận của 95 bài, trong đó 499 bình luận toxic, được chia bằng StratifiedGroupKFold thành năm fold theo post_id. Mỗi lượt sử dụng bốn fold huấn luyện và fold còn lại đánh giá. Tập test 926 câu của cách chia V2 được tách riêng khỏi pool kiểm định chéo.')
p('Các mô hình SVM dùng cùng bảng phân fold với PhoBERT. Ba cấu hình SVM gồm BoW, TF-IDF từ và TF-IDF từ kết hợp ký tự. Trong cấu hình kết hợp, nhánh từ dùng n-gram 1–2, nhánh char_wb dùng n-gram 3–5; C=0,1 và trọng số lớp {0:1, 1:8}. Mỗi lượt fit lại pipeline trên train của fold, sau đó dự đoán fold đánh giá.')
p('PhoBERT được fine-tune riêng cho từng fold. Checkpoint tốt nhất được chọn theo Macro-F1 trên chính fold đánh giá tại ngưỡng mặc định. Xác suất từ các checkpoint được gom thành OOF rồi dùng để chọn ngưỡng 0,85. Vì fold đánh giá còn tham gia chọn checkpoint và bộ OOF tham gia chọn ngưỡng, các điểm này có ảnh hưởng của quá trình lựa chọn; không phải ước lượng nested CV hoàn toàn độc lập.')
h('3.6.2 Kết quả theo từng fold',2)
sv=rows('reports/kfold_v3/svm/svm_fold_details.csv');ph=rows('reports/kfold_v3/phobert/kfold_results.csv')[:5]
ft=[]
for i in range(5):
 a=next(x for x in sv if x['model']=='word_char_svm' and int(x['fold'])==i);b=ph[i]
 ft.append([str(i),f"{float(a['macro_f1'])*100:.2f}",f"{float(b['macro_f1'])*100:.2f}",f"{(float(b['macro_f1'])-float(a['macro_f1']))*100:+.2f}"])
table('Bảng 3.6 Macro-F1 theo fold đơn vị phần trăm',['Fold','SVM từ + ký tự','PhoBERT','Chênh lệch điểm %'],ft+[['Trung bình ± SD','68,94 ± 1,42','71,16 ± 2,39','+2,22']])
p('PhoBERT có Macro-F1 cao hơn SVM trong cả năm fold của thiết lập này. Tuy nhiên, mức chênh lệch dao động từ khoảng 0,03 đến 4,42 điểm phần trăm. SVM có độ lệch chuẩn nhỏ hơn trong kết quả quan sát, còn PhoBERT có điểm trung bình cao hơn. Năm fold chưa đủ để tự động kết luận khác biệt có ý nghĩa thống kê hoặc ưu thế trên mọi miền dữ liệu.')
note('Nguồn: data/kfold_v3/train_pool_5folds.csv; scripts/prepare_kfold_data.py; scripts/train_kfold_svm.py; scripts/generate_kfold_notebook.py; các bảng fold trong reports/kfold_v3. Điểm fold PhoBERT dùng ngưỡng mặc định; điểm OOF sau đây dùng ngưỡng đã chọn 0,85.')
page();h('3.6.3 Kết quả OOF và sự đánh đổi giữa các mô hình',2)
table('Bảng 3.7 Kết quả gộp dự đoán OOF trên 7.669 câu',['Chỉ số','SVM từ + ký tự','PhoBERT τ=0,85'],[['Macro-F1 (%)','68,98','71,22'],['F1-toxic (%)','41,34','46,09'],['Recall-toxic (%)','34,67','44,89'],['Precision-toxic (%)','51,18','47,36'],['Accuracy (%)','93,60','93,17'],['TP / FN','173 / 326','224 / 275'],['FP / TN','165 / 7.005','249 / 6.921']])
fig(chart('oof.png','Kết quả OOF theo giao thức V3',['BoW + SVM','TF-IDF + SVM','Word + Char SVM','PhoBERT tau 0,85'],[64.96,66.44,68.98,71.22]),'Hình 3.2 Macro-F1 OOF của các mô hình trong V3')
p('PhoBERT có tổng số phát hiện đúng toxic cao hơn 51 câu, nhưng đồng thời báo nhầm nhiều hơn 84 câu. Điều này giải thích việc Macro-F1 và Recall-toxic cao hơn trong khi Accuracy thấp hơn SVM. Chênh lệch tổng TP không đồng nghĩa đúng 51 mẫu riêng biệt chỉ được PhoBERT phát hiện; kết luận đó cần đối chiếu dự đoán từng mẫu.')
p('Đặc trưng ký tự có thể bổ sung tín hiệu cho các biến thể cách viết và lỗi chính tả, trong khi biểu diễn theo ngữ cảnh của PhoBERT cung cấp một hướng tiếp cận khác. Tuy nhiên, chỉ số tổng hợp chưa chứng minh riêng khả năng hiểu mỉa mai hay công kích ngầm. Việc đánh giá các hiện tượng này cần tập mẫu được xác định và kiểm tra riêng.')
note('Nguồn: reports/kfold_v3/svm/kfold_svm_comparison.csv; reports/kfold_v3/phobert/kfold_summary.json và oof_predictions.csv. OOF PhoBERT được hiệu chỉnh ngưỡng trên chính pool OOF; không đồng nhất với điểm của ensemble trên test.')
page();h('3.6.4 Ma trận nhầm lẫn và phân tích lỗi',2)
table('Bảng 3.8 Ma trận nhầm lẫn OOF với toxic là lớp dương',['Thực tế và mô hình','Dự đoán non-toxic','Dự đoán toxic'],[['Non-toxic – SVM','7.005 (TN)','165 (FP)'],['Toxic – SVM','326 (FN)','173 (TP)'],['Non-toxic – PhoBERT','6.921 (TN)','249 (FP)'],['Toxic – PhoBERT','275 (FN)','224 (TP)']])
p('Mỗi mô hình được đánh giá trên 7.170 câu non-toxic và 499 câu toxic. Số non-toxic lớn khiến ô TN chiếm ưu thế. Vì vậy, khi đọc ma trận cần xem trực tiếp hàng toxic và số FN thay vì chỉ nhìn ô có màu đậm nhất. PhoBERT vẫn bỏ sót 275/499 câu toxic tại ngưỡng đã chọn, tương đương khoảng 55,11%.')
p('Để minh họa lỗi ở cấp câu, nhóm sử dụng các bản ghi validation V2. Những ví dụ này có nguồn đánh giá khác với ma trận OOF ở trên; chúng chỉ minh họa tình huống lỗi, không được dùng để suy ra tỷ lệ nguyên nhân trên toàn bộ V3. Nội dung đã loại bỏ thông tin nhận diện trong phần trích dẫn.')
table('Bảng 3.9 Ví dụ sai của PhoBERT trên validation V2',['Bình luận','Nhãn thật','Dự đoán','Điểm toxic'],[['Thằng này bắn đi cho đỡ jack việc','1','0','0,6676'],['[MENTION] t biết m luôn tệ mà','1','0','0,2590']])
p('Ở ví dụ thứ nhất, điểm 0,6676 thấp hơn ngưỡng 0,90 nên mô hình trả non-toxic dù nhãn dữ liệu là toxic. Nếu hạ ngưỡng xuống 0,50 thì riêng mẫu này sẽ đổi nhãn; điều đó không bảo đảm toàn tập tốt hơn vì nhiều mẫu non-toxic khác cũng có thể chuyển thành báo nhầm. Ví dụ thứ hai cho thấy việc điều chỉnh ngưỡng đến 0,50 vẫn chưa khắc phục được mọi lỗi.')
p('Các hướng rà soát gồm biến thể tiếng lóng, công kích phụ thuộc hội thoại, câu ngắn và cảm xúc tiêu cực không công kích. Đây là các giả thuyết phân tích cần kiểm tra từng bản ghi. Nếu chưa có quy trình mã hóa nhóm lỗi và thống kê, không gán tỷ lệ phần trăm cho từng nguyên nhân hoặc khẳng định một từ cụ thể đã gây ra dự đoán.')
note('Nguồn: bảng OOF hai mô hình; reports/phobert_v2/validation_error_analysis.csv. Nhãn thật trong bảng là nhãn của bộ dữ liệu nhóm, có thể cần ngữ cảnh để diễn giải.')
page();h('3.7 Tổng hợp kết quả và giới hạn đánh giá')
h('3.7.1 Đối chiếu ba giai đoạn',2)
table('Bảng 3.10 Tổng hợp giao thức và điểm Macro-F1',['Giai đoạn','Tập đánh giá','SVM (%)','PhoBERT (%)'],[['V1','Validation 1.277 câu','68,86','68,88'],['V2','Validation 824 câu','78,83','78,88'],['V3 theo fold','Mean ± SD năm fold','68,94 ± 1,42','71,16 ± 2,39'],['V3 gộp OOF','7.669 câu','68,98','71,22']])
p('V1 thiết lập mốc ban đầu; V2 khảo sát một cách chia có tỷ lệ train lớn hơn; V3 quan sát hiệu năng qua nhiều nhóm bài viết. Không xếp hạng ba giai đoạn chỉ theo độ lớn điểm số vì tập đánh giá và quy trình lựa chọn khác nhau. Điểm V2 cao hơn V3 không chứng minh V3 kém hơn; V3 cung cấp thêm thông tin về mức biến động qua các fold.')
h('3.7.2 Kết quả test của baseline V1',2)
p('Lượt đánh giá baseline V1 có lưu selection_before_test.json và results.json. TF-IDF + SVM được chọn bằng validation trước khi chấm test 1.318 câu, gồm 82 toxic và 1.236 non-toxic. Kết quả của mô hình đã chọn được trình bày dưới đây; không sử dụng thứ hạng test để chọn lại baseline.')
table('Bảng 3.11 Kết quả test đã lưu của TF-IDF SVM baseline V1',['Chỉ số','Giá trị'],[['Accuracy / Macro-F1 (%)','87,71 / 64,71'],['Precision / Recall toxic (%)','26,74 / 56,10'],['F1-toxic (%)','36,22'],['TN / FP / FN / TP','1.110 / 126 / 36 / 46']])
p('Macro-F1 test thấp hơn validation của baseline này, khoảng 67,10% xuống 64,71%, minh họa rằng điểm validation không bảo đảm giữ nguyên trên tập đánh giá khác. Đây là kết quả của baseline V1, không đại diện cho SVM cải tiến, PhoBERT hoặc ensemble V3. Bộ chia thuộc dữ liệu đã được sử dụng trong quá trình phát triển, nên cũng không xem là benchmark hoàn toàn mới, chưa từng được khảo sát.')
p('Đối với V2/V3, đánh giá cuối cần chốt checkpoint hoặc cách ensemble và ngưỡng trước khi sử dụng test 926 câu. Kết quả validation, điểm từng fold và OOF hiện tại không thay thế phép đánh giá này. Khi hoàn tất, cần báo cùng các độ đo, ma trận nhầm lẫn và xác định chính xác mô hình được chấm.')
note('Nguồn: reports/resplit_v1/final_evaluation/selection_before_test.json và results.json. Các lượt test ở những cách chia khác nhau không phải các benchmark độc lập để so sánh trực tiếp.')
page();h('3.8 Dashboard và demo')
h('3.8.1 Mục đích và luồng xử lý',2)
p('Ứng dụng Streamlit được xây dựng để minh họa luồng phân loại bình luận và hỗ trợ quan sát dữ liệu. Người dùng nhập văn bản; hệ thống chuẩn hóa, tách từ, tạo đầu vào tương ứng rồi gọi mô hình. Điểm đầu ra được so với ngưỡng để chuyển thành nhãn toxic hoặc non-toxic. Demo là công cụ quan sát hành vi của mô hình, không thay thế đánh giá trên tập có nhãn.')
p('Các nhóm chức năng trong mã giao diện gồm phân loại trực tiếp, thống kê dữ liệu, so sánh mô hình, khảo sát cải tiến và phân tích lỗi. Thống kê nhãn được đọc từ dữ liệu; một số bảng và thành phần biểu đồ được khai báo trực tiếp trong giao diện. Khi báo cáo kết quả khoa học, các số liệu phải đối chiếu với file dự đoán hoặc báo cáo của lượt chạy tương ứng.')
h('3.8.2 Ý nghĩa điểm số và ngưỡng',2)
p('Linear SVM trả decision score; điểm này không phải xác suất. Việc áp sigmoid lên score chỉ đưa giá trị về khoảng 0–1, chưa tạo xác suất đã hiệu chỉnh. Với PhoBERT, softmax tạo điểm cho hai lớp, nhưng điểm 0,90 cũng không tự chứng minh độ chính xác thực tế 90%. Cần phân biệt điểm của một câu với độ đo trên tập đánh giá.')
p('Khi thay ngưỡng và giữ nguyên câu cùng checkpoint, điểm mô hình không đổi, chỉ quy tắc gán nhãn thay đổi. Ngưỡng cao hơn làm số cảnh báo toxic không tăng; thường giảm báo nhầm nhưng có thể tăng bỏ sót. Ngưỡng 0,90 của V2 và 0,85 của OOF V3 thuộc các thiết lập khác nhau, không được hoán đổi mà không kiểm tra.')
h('3.8.3 Phạm vi sử dụng phiên bản giao diện hiện tại',2)
p('Mã giao diện hiện có cơ chế dự phòng bằng từ khóa khi PhoBERT không nạp hoặc suy luận được. Trong tình huống đó, kết quả không phải đầu ra của PhoBERT. Để demo có thể kiểm chứng, cần hiển thị trạng thái tải mô hình và lỗi, đồng thời dừng dự đoán hoặc công bố rõ cơ chế dự phòng.')
p('Đường cong ngưỡng trong tab Ablation được sinh theo công thức minh họa, không lấy từ dự đoán thực nghiệm; các giá trị độ trễ có hằng số cộng thêm và KPI độ trễ cố định. Những thành phần này không được sử dụng để chứng minh ngưỡng tối ưu hoặc tốc độ mô hình. Lựa chọn BoW + SVM cũng cần gắn đúng pipeline trước khi giới thiệu là một mô hình riêng.')
p('Kịch bản demo phù hợp gồm câu bình thường, câu công kích rõ và câu khó hoặc dự đoán sai. Với mỗi câu, trình bày đầu vào sau tiền xử lý, mô hình thực sự nạp, score và ngưỡng. Nếu hai mô hình đồng thuận, chỉ kết luận chúng trả cùng nhãn; không suy ra độ tin cậy rất cao khi chưa có kiểm định.')
note('Nguồn triển khai: app.py và src/preprocessing.py. Các mô tả hạn chế ở đây phản ánh mã giao diện hiện tại; không sử dụng ảnh demo để thay thế số liệu đánh giá.')
page();h('3.9 Hạn chế và hướng cải thiện')
p('Thứ nhất, lớp toxic chiếm tỷ lệ nhỏ và phân bố theo bài viết không đồng đều. Một lần chia validation có thể cho kết quả thuận lợi hoặc khó hơn lần khác. Kiểm định chéo giúp quan sát biến động nhưng không loại bỏ hết sự phụ thuộc vào dữ liệu và lựa chọn cấu hình.')
p('Thứ hai, nhãn phản ánh quy ước của nhóm. Những trường hợp đùa giỡn, mỉa mai hoặc thiếu hội thoại có thể gây bất đồng. Cần tổ chức gán nhãn chồng lấn cho một phần dữ liệu, ghi lại cách xử lý bất đồng và đo độ đồng thuận nếu muốn định lượng độ tin cậy của nhãn.')
p('Thứ ba, kiểm định chéo PhoBERT còn sử dụng fold đánh giá để chọn checkpoint và sử dụng OOF để chọn ngưỡng. Một hướng đánh giá chặt hơn là dùng tập validation nội bộ trong mỗi train fold để chọn checkpoint/ngưỡng, rồi chỉ chấm outer fold sau khi cố định lựa chọn. Tập test cuối cần được bảo vệ khỏi quá trình điều chỉnh.')
p('Thứ tư, dữ liệu tập trung trong cộng đồng sinh viên PTIT, nên không suy rộng ngay sang mọi nhóm Facebook hoặc mạng xã hội. Cần đánh giá trên bài viết ở thời điểm mới, nguồn khác và các biến thể ngôn ngữ mới. Bổ sung có chọn lọc mẫu toxic và mẫu phê bình không toxic là hướng đáng khảo sát, nhưng phải đánh giá lại bằng giao thức cố định.')
p('Cuối cùng, kết quả hiện tại phù hợp với vai trò hỗ trợ rà soát. Việc lựa chọn ngưỡng cần gắn với chi phí bỏ sót và báo nhầm. Để triển khai, cần đo thời gian suy luận thật trên cấu hình phần cứng được công bố, xác thực đường đi mô hình và bổ sung trạng thái lỗi rõ ràng trong demo.')
h('Tiểu kết phần thực nghiệm',2)
p('Ba giai đoạn cho thấy hiệu năng phụ thuộc vào đặc trưng, cấu hình và tập đánh giá. Trong V2, đặc trưng từ kết hợp ký tự cải thiện Macro-F1 so với baseline BoW + SVM trên cùng validation. Trong V3, PhoBERT đạt Macro-F1 trung bình 71,16%, cao hơn 68,94% của SVM từ kết hợp ký tự; kết quả OOF cũng cho thấy tăng khả năng phát hiện toxic kèm tăng báo nhầm. Các kết luận cần đi cùng giới hạn lựa chọn checkpoint, ngưỡng và phạm vi dữ liệu.')
h('Nguồn số liệu và khả năng đối chiếu',2)
for t in ['V1: reports/resplit_v1/final_evaluation/results.json; reports/resplit_v1/steps23_v2/REPORT.md; models/current_run.json; reports/phobert/REPORT.md.','V2: reports/resplit_v2/improvements/validation_report.md; reports/phobert_v2/best_metrics.json; training_history.csv; validation_error_analysis.csv.','V3: reports/kfold_v3/svm/svm_fold_details.csv; kfold_svm_comparison.csv; reports/kfold_v3/phobert/kfold_results.csv; kfold_summary.json; oof_predictions.csv.','Giao thức và demo: scripts/prepare_kfold_data.py; scripts/train_kfold_svm.py; scripts/generate_kfold_notebook.py; app.py.']:
 note(t)
footer=sec.footer.paragraphs[0];footer.alignment=WD_ALIGN_PARAGRAPH.CENTER
f=OxmlElement('w:fldSimple');f.set(qn('w:instr'),'PAGE');footer._p.append(f)
d.save(O/'Chuong_3_tu_3_4_den_het.docx')
print(O/'Chuong_3_tu_3_4_den_het.docx')
