from pathlib import Path
from docx import Document
from docx.shared import Pt
r=Path('E:/BT1/output/word');d=Document(r/'Chuong_3_DA_BO_MUC_3_8_2.docx')
revisions={
2:'Mục đích: Ở lần thực nghiệm đầu tiên, nhóm xây dựng các mô hình ban đầu để có cơ sở so sánh và xác định những điểm cần cải thiện.',
3:'Dữ liệu huấn luyện: Nhóm sử dụng 6.000 bình luận cho train, 1.277 bình luận cho validation và 1.318 bình luận cho test, tương ứng tỷ lệ chia mục tiêu 70/15/15.',
4:'Cách chia dữ liệu: Các bình luận được chia theo post_id. Toàn bộ bình luận của một bài viết chỉ nằm trong một tập để hạn chế sự trùng lặp ngữ cảnh giữa các tập.',
5:'Các mô hình sử dụng: Nhóm thử nghiệm BoW và TF-IDF kết hợp với Naive Bayes hoặc SVM, đồng thời sử dụng PhoBERT và mô hình đối chứng Dummy để đối chiếu kết quả.',
6:'Lựa chọn mô hình: Nhóm dựa vào Macro-F1 trên validation để chọn cấu hình. Với PhoBERT, checkpoint được chọn ở epoch 5, sau đó áp dụng ngưỡng quyết định 0,52.',
9:'Kết quả chính: SVM cải tiến đạt Macro-F1 68,86%, trong khi PhoBERT đạt 68,88%. Hai kết quả gần như tương đương; mức chênh 0,02 điểm phần trăm chưa cho thấy sự khác biệt rõ rệt.',
10:'Khả năng phát hiện toxic: SVM cải tiến có Recall-toxic 48,19%, cao hơn mức 44,58% của PhoBERT. Như vậy, mô hình có Macro-F1 cao hơn chưa chắc phát hiện được nhiều bình luận toxic hơn.',
11:'Về chỉ số Accuracy: Dummy đạt 93,50% dù không phát hiện được câu toxic nào. Vì vậy, nhóm xem thêm Macro-F1 và các chỉ số của lớp toxic khi đánh giá mô hình.',
14:'Nhận xét: Khoảng cách giữa SVM cải tiến và PhoBERT ở V1 rất nhỏ. Kết quả này cho thấy cần xem thêm các loại lỗi, thay vì chỉ dựa vào thứ hạng Macro-F1.',
17:'Báo nhầm và bỏ sót: So với SVM, PhoBERT giảm được 10 trường hợp báo nhầm nhưng cũng phát hiện đúng ít hơn 3 câu toxic. Mỗi mô hình vì thế có một lợi thế khác nhau.',
19:'Ưu điểm: V1 tạo được cơ sở đối chiếu giữa các phương pháp trên cùng tập validation. Việc chia theo bài viết cũng giúp hạn chế sự trùng lặp ngữ cảnh khi đánh giá.',
20:'Nhược điểm: Cả SVM cải tiến và PhoBERT vẫn bỏ sót hơn một nửa số câu toxic. Bên cạnh đó, kết quả mới phản ánh một lần chia dữ liệu nên chưa cho thấy mức biến động ở các nhóm bài viết khác.',
24:'Lý do thay đổi: Sau V1, khả năng phát hiện toxic còn hạn chế. Nhóm tiếp tục thử nghiệm V2 để tìm hiểu liệu việc dành thêm dữ liệu cho huấn luyện có mang lại kết quả khả quan hơn hay không.',
25:'Dữ liệu huấn luyện: V2 sử dụng 6.845 bình luận cho train, 824 bình luận cho validation và 926 bình luận cho test, theo tỷ lệ chia mục tiêu 80/10/10.',
26:'Thay đổi về dữ liệu: Nhóm chia lại bộ 8.595 bình luận hiện có. Trong đó, validation V2 gồm 54 câu toxic và 770 câu non-toxic; thành phần tập đánh giá vì vậy cũng khác V1.',
27:'Cấu hình SVM được chọn: Nhóm kết hợp TF-IDF theo từ và ký tự, sử dụng C=0,1, trọng số lớp {0:1, 1:8} và ngưỡng decision score bằng 0.',
28:'Cấu hình PhoBERT được chọn: Các tham số huấn luyện chính được giữ như trước. Trên validation V2, nhóm chọn checkpoint ở epoch 4 và ngưỡng quyết định 0,90.',
31:'Hiệu quả của đặc trưng kết hợp: Word+Char SVM đạt Macro-F1 78,83%, cao hơn BoW + SVM khoảng 3,00 điểm phần trăm. Kết quả cho thấy việc bổ sung nhánh ký tự có ích trong thiết lập này.',
32:'Thay đổi về lỗi của SVM: Khi chuyển từ BoW sang đặc trưng kết hợp, số câu toxic bị bỏ sót giảm từ 29 xuống 22. Tuy nhiên, số câu non-toxic bị báo nhầm tăng từ 13 lên 20.',
33:'Kết quả PhoBERT: Mô hình đạt Macro-F1 78,88% và phát hiện đúng 33 trong 54 câu toxic, trong khi SVM phát hiện được 32 câu.',
34:'So sánh hai mô hình: PhoBERT cao hơn khoảng 0,05 điểm phần trăm Macro-F1. Với mức chênh nhỏ như vậy, chưa thể xem đây là ưu thế rõ rệt so với SVM.',
38:'Nhận xét: Word+Char SVM đạt Macro-F1 cao hơn các baseline trong hình và tiến gần kết quả của PhoBERT. Vì vậy, đặc trưng kết hợp là một lựa chọn đáng chú ý trong nhóm mô hình truyền thống.',
41:'Báo nhầm và bỏ sót: PhoBERT phát hiện đúng thêm 1 câu toxic so với Word+Char SVM, nhưng đồng thời báo nhầm thêm 2 câu non-toxic. Lợi thế về phát hiện đi kèm với việc tăng cảnh báo nhầm.',
43:'Train loss: Qua năm epoch, train loss giảm từ 0,7704 xuống 0,5101, cho thấy mô hình ngày càng khớp hơn với dữ liệu huấn luyện.',
44:'Validation loss: Giá trị thấp nhất xuất hiện ở epoch 2 rồi tăng trở lại. Diễn biến này là dấu hiệu cần xem xét khả năng overfitting khi tiếp tục huấn luyện.',
45:'Lý do chọn epoch 4: Tại ngưỡng 0,50, Macro-F1 đạt cao nhất ở epoch 4 với 77,26%. Do đã chọn Macro-F1 làm tiêu chí chính, nhóm lưu checkpoint này dù validation loss không thấp nhất.',
46:'Sự khác nhau giữa loss và F1: Loss còn phụ thuộc vào độ lớn xác suất dự đoán, còn F1 được tính từ nhãn sau khi áp dụng ngưỡng. Vì vậy, hai chỉ số có thể thay đổi theo những hướng khác nhau.',
47:'Ảnh hưởng của việc tăng ngưỡng: Khi nâng ngưỡng lên 0,90, FP giảm từ 41 xuống 22 và TP giảm từ 39 xuống 33. Việc giảm báo nhầm giúp Macro-F1 tăng từ 77,26% lên 78,88%, dù mô hình bỏ sót thêm một số câu toxic.',
50:'Nhận xét: Train loss tiếp tục giảm trong khi validation loss tăng sau epoch 2. Do đó, cần theo dõi kết quả validation khi chọn thời điểm dừng, thay vì chỉ nhìn vào mức giảm loss trên train.',
53:'Ảnh hưởng của ngưỡng: Khi tăng ngưỡng, mô hình cần điểm cao hơn mới gán nhãn toxic, nên số cảnh báo có thể giảm và Recall không tăng. Nếu số báo nhầm giảm đủ nhiều, Macro-F1 vẫn có thể được cải thiện.',
54:'Phạm vi kết luận: Trong các ngưỡng đã khảo sát trên validation V2, 0,90 cho kết quả tốt nhất. Giá trị này cần được kiểm tra lại nếu thay mô hình hoặc dữ liệu đánh giá.',
57:'Ưu điểm của V2: Nhóm có thêm dữ liệu để huấn luyện và thu được điểm validation cao hơn V1. Đây là kết quả khả quan để tiếp tục khảo sát ở giai đoạn sau.',
58:'Nhược điểm: Validation V2 chỉ có 54 câu toxic và đã được dùng để chọn cấu hình, ngưỡng. Vì vậy, kết quả trên tập này có thể cao hơn mức đạt được trên dữ liệu mới.',
59:'Lưu ý khi so sánh: V1 và V2 khác nhau cả về train, validation và cấu hình. Do đó, chưa thể cho rằng toàn bộ mức tăng điểm là do tăng tỷ lệ dữ liệu huấn luyện.',
63:'Mục đích: Với V3, nhóm muốn quan sát kết quả qua nhiều nhóm bài viết, từ đó đánh giá mức biến động và so sánh các mô hình trên cùng cách chia fold.',
64:'Dữ liệu sử dụng: Pool train và validation gồm 7.669 bình luận thuộc 95 bài viết, trong đó có 499 câu toxic. Tập test V2 gồm 926 bình luận được giữ riêng.',
65:'Cách chia dữ liệu: Nhóm dùng StratifiedGroupKFold với năm fold theo post_id. Ở mỗi lượt, mô hình được huấn luyện trên bốn fold và đánh giá trên fold còn lại.',
66:'Các cấu hình SVM: Nhóm đối chiếu BoW + SVM, TF-IDF + SVM và Word+Char SVM. Toàn bộ pipeline được fit lại trên train của từng lượt trước khi dự đoán fold đánh giá.',
67:'Huấn luyện PhoBERT: Mô hình được fine-tune riêng cho từng fold. Checkpoint được chọn theo Macro-F1 trên fold đánh giá tại ngưỡng mặc định.',
68:'Lựa chọn ngưỡng OOF: Sau khi gom xác suất ngoài mẫu từ năm fold, nhóm khảo sát các ngưỡng trên pool OOF và chọn giá trị 0,85.',
71:'Kết quả chính: PhoBERT đạt Macro-F1 trung bình 71,16%, cao hơn mức 68,94% của Word+Char SVM khoảng 2,22 điểm phần trăm.',
72:'Mức biến động: Độ lệch chuẩn của PhoBERT là 2,39 điểm phần trăm, còn SVM là 1,42 điểm phần trăm. SVM có kết quả ít dao động hơn giữa các fold trong lần thực nghiệm này.',
73:'Nhận xét: PhoBERT đạt điểm cao hơn ở cả năm fold, nhưng mức chênh dao động từ khoảng 0,03 đến 4,42 điểm phần trăm. Lợi thế của mô hình vì vậy không đồng đều ở mọi nhóm bài viết.',
74:'Giới hạn đánh giá: Fold đánh giá còn được dùng để chọn checkpoint, còn OOF được dùng chọn ngưỡng. Quy trình này chưa phải nested CV độc lập nên kết quả có thể chịu ảnh hưởng của việc lựa chọn cấu hình.',
78:'Nhận xét: Đường Macro-F1 của PhoBERT nằm trên SVM ở cả năm fold, nhưng hai mô hình gần như ngang nhau ở fold 3. Điều này cho thấy thành phần bài viết trong mỗi fold có ảnh hưởng đến mức chênh lệch.',
81:'So sánh số lỗi: PhoBERT có tổng số câu toxic phát hiện đúng cao hơn SVM 51 câu, nhưng cũng báo nhầm nhiều hơn 84 câu.',
82:'Ý nghĩa của kết quả: PhoBERT phát hiện được nhiều toxic hơn nhưng tạo thêm cảnh báo đối với non-toxic. Điều này giải thích vì sao Macro-F1 cao hơn trong khi Accuracy lại thấp hơn SVM.',
83:'Hạn chế còn lại: PhoBERT vẫn bỏ sót 275 trong 499 câu toxic, tương đương khoảng 55,11%. Với kết quả này, mô hình phù hợp hơn với vai trò hỗ trợ rà soát thay vì tự quyết định mọi trường hợp.',
85:'Cách đọc ma trận: Các hàng thể hiện nhãn thật, các cột thể hiện nhãn dự đoán. Do non-toxic chiếm đa số, cần chú ý thêm các ô FN và FP để đánh giá khả năng phát hiện và mức báo nhầm.',
86:'Các trường hợp cần rà soát: Nhóm cần xem kỹ những câu dùng tiếng lóng, câu quá ngắn, câu công kích phụ thuộc ngữ cảnh và câu thể hiện cảm xúc tiêu cực nhưng không công kích ai.',
90:'Nhận xét: PhoBERT đạt Macro-F1 và Recall-toxic cao hơn SVM. Các điểm trong hình được tính trên dự đoán OOF sau khi chọn ngưỡng, nên cần phân biệt với trung bình điểm từng fold.',
93:'Báo nhầm và bỏ sót: PhoBERT giảm tổng số bỏ sót 51 câu nhưng tăng số báo nhầm 84 câu. Khi sử dụng thực tế, cần cân nhắc cả số cảnh báo mà người kiểm duyệt phải xem lại.',
97:'Ở giai đoạn V1: Nhóm xây dựng được mốc đối chiếu ban đầu và nhận ra hạn chế của Accuracy khi dữ liệu mất cân bằng. SVM cải tiến và PhoBERT có Macro-F1 gần tương đương, khoảng 68,9%.',
98:'Ở giai đoạn V2: Trên cùng validation, Word+Char SVM đạt Macro-F1 78,83%, cao hơn BoW + SVM khoảng 3,00 điểm phần trăm. Số bỏ sót giảm 7 câu, nhưng số báo nhầm cũng tăng 7 câu.',
99:'Ở giai đoạn V3: PhoBERT đạt Macro-F1 trung bình 71,16%, so với 68,94% của Word+Char SVM. Mô hình đạt điểm cao hơn trong cả năm fold, với mức chênh trung bình khoảng 2,22 điểm phần trăm.',
100:'Nhìn lại ba giai đoạn: V1 cung cấp kết quả ban đầu, V2 khảo sát một cách chia mới, còn V3 cho thấy kết quả thay đổi thế nào giữa các nhóm bài viết. Đóng góp của V3 nằm ở việc mở rộng đánh giá, chứ không chỉ ở mức điểm đạt được.',
102:'Có cơ sở đối chiếu: Các baseline và mô hình Dummy giúp nhóm đánh giá mức cải thiện so với cách dự đoán đơn giản. Việc xem thêm Macro-F1 và Recall-toxic cũng làm rõ chất lượng trên lớp ít mẫu.',
103:'Hạn chế trùng lặp ngữ cảnh: Chia dữ liệu theo bài viết giúp tránh đưa bình luận cùng bài vào cả train và tập đánh giá. Cách làm này phù hợp hơn với mục tiêu xử lý bình luận từ các bài viết chưa gặp.',
104:'Tận dụng hai loại đặc trưng: Nhánh từ giữ các cụm từ cục bộ, còn nhánh ký tự khai thác những đoạn chữ trong các biến thể cách viết. Kết quả V2 và các cấu hình SVM V3 cho thấy việc kết hợp hai nhánh có ích.',
105:'PhoBERT phát hiện được nhiều toxic hơn trong V3: Recall-toxic OOF đạt 44,89%, so với 34,67% của SVM, và tổng số phát hiện đúng cao hơn 51 câu. Đây là điểm thuận lợi nếu mục tiêu là đưa thêm trường hợp nghi ngờ đến người kiểm duyệt.',
106:'SVM có lợi thế về báo nhầm: Precision-toxic OOF đạt 51,18%, cao hơn mức 47,36% của PhoBERT; số FP cũng thấp hơn, 165 so với 249. Ngoài ra, Macro-F1 của SVM ít biến động hơn giữa các fold đã khảo sát.',
110:'Vẫn còn nhiều câu toxic bị bỏ sót: PhoBERT bỏ sót 275/499 câu, tương đương 55,11%, còn SVM bỏ sót 326/499 câu. Vì vậy, cả hai mô hình vẫn cần được cải thiện nếu muốn phát hiện đầy đủ hơn.',
111:'Phát hiện thêm đi kèm báo nhầm: PhoBERT có tổng TP cao hơn 51 câu nhưng FP cũng cao hơn 84 câu. Mức tăng Macro-F1 cần được xem cùng khối lượng cảnh báo nhầm phát sinh.',
112:'Mỗi mô hình có thế mạnh riêng: PhoBERT cao hơn về Macro-F1 và Recall-toxic, trong khi SVM cao hơn về Precision-toxic và Accuracy OOF. Việc lựa chọn cần gắn với mục tiêu sử dụng cụ thể.',
113:'Khó tách riêng tác động giữa V1 và V2: Cả train, validation và cấu hình đều thay đổi. Vì vậy, điểm V2 cao hơn chưa đủ để kết luận rằng tăng tỷ lệ train là nguyên nhân duy nhất hoặc V2 là lựa chọn tốt nhất.',
114:'Kết quả V3 còn chịu ảnh hưởng của lựa chọn: Fold đánh giá tham gia chọn checkpoint PhoBERT và OOF tham gia chọn ngưỡng. Cần có bước đánh giá độc lập hơn để kiểm tra mức cải thiện trên dữ liệu mới.',
115:'Chưa đánh giá riêng từng hiện tượng ngôn ngữ: Các chỉ số chung chưa cho biết mô hình xử lý mỉa mai hay công kích ngầm tốt đến đâu. Muốn kết luận về từng loại, cần có nhóm mẫu được xác định và đánh giá riêng.',
116:'Phạm vi dữ liệu còn hẹp: Mẫu toxic ít và phân bố không đều giữa các bài; một số câu cũng khó gán nhãn khi thiếu ngữ cảnh. Kết quả trong cộng đồng PTIT vì thế chưa thể đại diện cho mọi nhóm hoặc thời điểm.',
118:'Nếu ưu tiên phát hiện để rà soát: Có thể cân nhắc PhoBERT dựa trên Macro-F1 và Recall-toxic của V3. Đổi lại, người sử dụng cần chấp nhận và xử lý nhiều cảnh báo nhầm hơn.',
119:'Nếu ưu tiên hạn chế báo nhầm: Word+Char SVM là lựa chọn đáng cân nhắc, do có Precision-toxic cao hơn và ít FP hơn trong kết quả OOF đã quan sát.',
120:'Cách sử dụng phù hợp: Mô hình nên hỗ trợ sàng lọc và chuyển các trường hợp nghi ngờ cho người kiểm duyệt. Với chất lượng hiện tại, dự đoán chưa nên là căn cứ duy nhất cho quyết định xử lý.',
121:'Trước khi chốt mô hình: Nhóm cần cố định checkpoint, cách ensemble nếu có và ngưỡng, rồi mới đánh giá trên test 926 câu. Quyết định cuối nên dựa vào mục tiêu sử dụng cùng kết quả đánh giá này.',
122:'Nhận xét chung: Đặc trưng kết hợp giúp cải thiện baseline trong V2, còn PhoBERT đạt Macro-F1 cao hơn trong V3. Tuy vậy, kết quả vẫn cho thấy sự đánh đổi giữa báo nhầm và bỏ sót. Qua ba giai đoạn, nhóm có thêm cơ sở để hiểu thế mạnh và giới hạn của từng lựa chọn.',
126:'Mục đích của demo: Giao diện giúp người dùng thử phân loại một bình luận và quan sát cách xử lý của mô hình. Kết quả thử từng câu được dùng để minh họa, còn chất lượng chung vẫn được đánh giá trên tập có nhãn.',
127:'Luồng xử lý: Sau khi người dùng nhập câu, hệ thống chuẩn hóa và tách từ, tạo đầu vào phù hợp rồi gọi mô hình. Điểm đầu ra được so với ngưỡng để trả về nhãn toxic hoặc non-toxic.',
128:'Các chức năng chính: Giao diện gồm phân loại trực tiếp, thống kê dữ liệu, so sánh mô hình, khảo sát cải tiến và phân tích lỗi, giúp theo dõi cả kết quả dự đoán lẫn kết quả thực nghiệm.',
129:'Điểm của SVM: Mô hình trả về decision score để xác định vị trí so với ngưỡng phân loại. Đưa score qua sigmoid chưa đủ để xem đó là xác suất đã được hiệu chỉnh.',
130:'Điểm của PhoBERT: Softmax tạo điểm cho từng lớp. Điểm toxic bằng 0,90 thể hiện đầu ra của mô hình với câu đang xét, chưa đồng nghĩa dự đoán đó có độ chính xác thực tế 90%.',
131:'Khi thay đổi ngưỡng: Với cùng câu và checkpoint, điểm đầu ra vẫn giữ nguyên. Nhãn dự đoán có thể đổi do điều kiện gán nhãn toxic thay đổi.',
132:'Cách trình bày demo: Nhóm thử một câu bình thường, một câu công kích rõ và một câu khó hoặc dự đoán sai. Với mỗi trường hợp, phần trình bày tập trung vào kết quả tiền xử lý, điểm đầu ra và ngưỡng quyết định.',
134:'Về dữ liệu: Cần bổ sung có chọn lọc các mẫu toxic và kiểm tra kết quả trên nguồn hoặc thời điểm mới, do dữ liệu hiện còn ít toxic và tập trung theo bài viết.',
135:'Về gán nhãn: Với những câu mơ hồ hoặc thiếu ngữ cảnh, nên bố trí gán nhãn chồng lấn và trao đổi khi có bất đồng. Nếu có đủ dữ liệu gán chồng lấn, nhóm có thể đo thêm độ đồng thuận.',
136:'Về đánh giá: Cần tách bước chọn checkpoint và ngưỡng khỏi tập dùng chấm cuối. Có thể sử dụng validation nội bộ hoặc nested CV để hạn chế ảnh hưởng của quá trình lựa chọn.',
137:'Về ứng dụng: Nên tiếp tục hướng đến việc hỗ trợ con người rà soát. Ngưỡng quyết định cần được lựa chọn theo mức độ chấp nhận bỏ sót và báo nhầm của người sử dụng.',
138:'Hướng hoàn thiện: Kết quả V3 cho thấy PhoBERT có Macro-F1 cao hơn SVM nhưng cũng tạo nhiều cảnh báo nhầm hơn. Bước tiếp theo là kiểm tra bằng đánh giá cuối và hoàn thiện demo để phù hợp với mục tiêu sử dụng.'
}
for i,text in revisions.items():
 p=d.paragraphs[i]
 # Replace text without changing paragraph style or spacing.
 for run in list(p.runs):run._element.getparent().remove(run._element)
 lead,body=text.split(': ',1);p.add_run(lead+': ').bold=True;p.add_run(body)
# Remove a duplicated continuation heading; the following heading identifies the content.
for p in list(d.paragraphs):
 if p.text=='3.7 Tổng hợp và đánh giá cuối tiếp theo':p._p.getparent().remove(p._p)
out=r/'Chuong_3_VAN_PHONG_TU_NHIEN.docx';d.save(out)
c=Document(out)
assert len(c.tables)==7 and len(c.inline_shapes)==9
assert not any(p.text.startswith(('3.8.2','Nguồn:','Lưu ý về OOF:','SVM cải tiến:','PhoBERT: Checkpoint','Hướng tiếp theo:','Lý do làm V3:')) for p in c.paragraphs)
for t in c.tables[:2]:assert len(t.rows)==5
print('Reworded',len(revisions),'paragraphs; retained tables, images and paragraph spacing.');print(out)
