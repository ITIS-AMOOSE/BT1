from pathlib import Path
src=Path('E:/BT1/build_pipeline_report.py').read_text(encoding='utf-8')
exec(src.split("h('Quy trình thực nghiệm từ V1 đến V3',0)")[0])
h('Quy trình thực nghiệm từ V1 đến V3',0)
p('Nhóm thực hiện ba giai đoạn để lần lượt xây dựng kết quả ban đầu, khảo sát một cách chia dữ liệu mới và đánh giá qua nhiều nhóm bài viết. Phần dưới trình bày thứ tự thực hiện của từng giai đoạn, từ chuẩn bị dữ liệu đến lựa chọn mô hình, đánh giá và kiểm tra kết quả.')
h('3.4 Thực nghiệm V1')
h('3.4.1 Chuẩn bị dữ liệu và quy trình tổng thể',2)
b('Đầu vào','Nhóm sử dụng bộ bình luận đã gán nhãn và tiền xử lý như trình bày tại mục 3.2. Mỗi bình luận được giữ thông tin về bài viết gốc để chia tập và đối chiếu kết quả về sau.')
pipeline('v1_bang_loi','Hình 3.6 Quy trình thực nghiệm V1',[
'1. Chuẩn bị đầu vào\nDữ liệu đã gán nhãn\nTiền xử lý theo mục 3.2',
'2. Chia theo bài viết\nHuấn luyện 70%\nXác thực và kiểm tra 30%',
'3. Biểu diễn văn bản\nBoW hoặc TF-IDF\nMã hóa cho PhoBERT',
'4. Huấn luyện mô hình\nHọc trên tập huấn luyện\nThử các cấu hình',
'5. Lựa chọn và phân loại\nĐánh giá trên xác thực\nChọn mô hình và ngưỡng',
'6. Kiểm tra kết quả\nĐối chiếu nhãn thật\nLưu mô hình và dự đoán'])
b('Bước 1 – Chia dữ liệu','Toàn bộ bình luận của cùng một bài viết được đưa vào một tập. Nhóm khảo sát các cách phân bố bài viết để số mẫu và tỷ lệ nhãn trong mỗi tập gần với mục tiêu 70/15/15; không chọn cách chia theo điểm mô hình.')
b('Kết quả chia tập','Tập huấn luyện gồm 6.000 bình luận, tập xác thực gồm 1.277 bình luận và tập kiểm tra gồm 1.318 bình luận. Tập huấn luyện dùng để học; tập xác thực dùng chọn cấu hình; tập kiểm tra dành cho đánh giá sau khi chốt lựa chọn.')
b('Bước 2 – Kiểm tra sau chia','Đối chiếu để bảo đảm không có bài viết xuất hiện ở nhiều tập, không thiếu hoặc lặp mẫu và nhãn của từng bình luận được giữ nguyên. Tổng số mẫu của ba tập phải bằng 8.595.')

page();h('3.4.2 Biểu diễn văn bản và huấn luyện',2)
b('Bước 3 – Chuẩn bị đầu vào','Nhóm dùng văn bản đã chuẩn hóa và tách từ theo mục 3.2. Quy tắc xử lý được giữ thống nhất giữa lúc huấn luyện và lúc dự đoán, tránh để cùng một câu bị xử lý theo hai cách khác nhau.')
b('Nhánh học máy truyền thống','Văn bản được chuyển thành vector bằng BoW hoặc TF-IDF. Từ vựng và trọng số chỉ được xây dựng từ tập huấn luyện; tập xác thực được chuyển đổi bằng bộ biểu diễn đã xây dựng đó.')
b('Bước 4 – Huấn luyện baseline','Nhóm kết hợp hai cách biểu diễn với Naive Bayes và SVM để tạo bốn baseline. Mỗi cấu hình được học trên tập huấn luyện rồi dự đoán tập xác thực. Các tham số được thử lần lượt để tìm cấu hình phù hợp cho từng mô hình.')
b('Nhánh PhoBERT','Văn bản đã tách từ được mã hóa thành các đơn vị đầu vào của PhoBERT, với độ dài tối đa theo cấu hình. Mô hình đã tiền huấn luyện được điều chỉnh bằng các bình luận có nhãn, theo từng nhóm mẫu nhỏ trong mỗi lượt học.')
b('Theo dõi huấn luyện','Sau mỗi lượt học, nhóm đánh giá PhoBERT trên tập xác thực và lưu trạng thái có Macro-F1 tốt nhất. Việc này giúp lựa chọn mô hình dựa trên khả năng dự đoán ngoài tập huấn luyện.')
h('3.4.3 Lựa chọn mô hình và hậu xử lý',2)
b('Bước 5 – Chọn cấu hình','Nhóm ưu tiên Macro-F1 trên tập xác thực; nếu cần phân biệt thêm thì xem F1 và Recall của lớp toxic. Với PhoBERT V1, mô hình được chọn ở lượt học thứ 5.')
b('Chuyển điểm thành nhãn','SVM phân loại dựa trên điểm so với ranh giới quyết định. Với PhoBERT, nhóm khảo sát các ngưỡng trên tập xác thực và chọn 0,52. Câu có điểm toxic từ ngưỡng này trở lên được gán toxic, các câu còn lại được gán non-toxic.')
b('Bước 6 – Đối chiếu kết quả','Ghép nhãn dự đoán với nhãn thật của đúng bình luận, sau đó tính các chỉ số và lập ma trận nhầm lẫn. Số dự đoán phải bằng số mẫu được đánh giá và tổng bốn ô trong ma trận phải khớp số mẫu đó.')
b('Lưu và kiểm tra đầu ra','Lưu mô hình đã chọn, cách xử lý đầu vào, ngưỡng và bảng dự đoán. Trước bàn giao, cần tải lại mô hình và kiểm tra khả năng tạo lại kết quả trên cùng dữ liệu; chỉ xác nhận hoàn tất khi đã có kết quả đối chiếu.')
table('Bảng 3.2 Kết quả bốn baseline V1 đơn vị phần trăm',['Mô hình','Accuracy','F1-toxic','Recall-toxic','Macro-F1'],[
['BoW + NB','93,19','32,56','25,30','64,49'],['BoW + SVM','92,64','36,49','32,53','66,29'],['TF-IDF + NB','93,50','2,35','1,20','49,50'],['TF-IDF + SVM','89,43','40,00','54,22','67,10']],[5,2.8,2.8,3,2.9])
b('Nhận xét','TF-IDF + SVM có Macro-F1 cao nhất trong bốn baseline, đạt 67,10%. PhoBERT được báo cáo đạt 68,88% sau chọn ngưỡng. Kết quả này còn phụ thuộc một lần chia và khả năng phát hiện toxic vẫn cần cải thiện.')

page();h('3.5 Thực nghiệm V2')
h('3.5.1 Mục tiêu và chuẩn bị dữ liệu',2)
b('Lý do thay đổi','Sau V1, nhóm tiếp tục khảo sát việc dành thêm dữ liệu cho huấn luyện. V2 vẫn dùng bộ 8.595 bình luận đã chốt, nhưng điều chỉnh tỷ lệ chia mục tiêu thành 80/10/10.')
pipeline('v2_bang_loi','Hình 3.7 Quy trình thực nghiệm V2',[
'1. Giữ dữ liệu đã chốt\n8.595 bình luận\nGiữ nguyên nhãn',
'2. Chia lại theo bài viết\nTăng phần huấn luyện\nMục tiêu 80/10/10',
'3. Chuẩn bị đầu vào\nKế thừa tiền xử lý\nXây lại bộ biểu diễn',
'4. Huấn luyện lại\nBốn baseline\nSVM kết hợp và PhoBERT',
'5. Lựa chọn cấu hình\nDùng tập xác thực V2\nChọn ngưỡng phân loại',
'6. Đánh giá và kiểm tra\nĐối chiếu 824 dự đoán\nGiữ riêng tập kiểm tra'])
b('Bước 1 – Chia lại dữ liệu','Nhóm tiếp tục giữ nguyên các bình luận thuộc cùng bài viết trong một tập, đồng thời lựa chọn cách phân bố gần tỷ lệ mục tiêu và phân bố nhãn chung. Thành phần của từng tập vì vậy khác V1.')
table('Bảng 3.3 Dữ liệu sau chia ở V2',['Tập dữ liệu','Tổng số','Non-toxic','Toxic'],[['Huấn luyện','6.845','6.400','445'],['Xác thực','824','770','54'],['Kiểm tra','926','866','60']],[5,3.8,3.8,3.9])
b('Bước 2 – Kiểm tra','Đối chiếu số mẫu, nhãn và bài viết giữa các tập như V1. Kết quả kiểm tra bộ chia V2 ghi nhận không dùng chung bài viết giữa các tập và bảo toàn các bình luận của bộ dữ liệu ban đầu.')

page();h('3.5.2 Huấn luyện và lựa chọn mô hình V2',2)
b('Bước 3 – Chuẩn bị biểu diễn','Quy tắc tiền xử lý được kế thừa từ mục 3.2. Nhóm xây dựng lại bộ biểu diễn bằng tập huấn luyện V2, thay vì dùng lại bộ đã học từ cách chia V1.')
b('Bước 4 – Huấn luyện lại baseline','Bốn baseline được học lại trên 6.845 bình luận và lựa chọn cấu hình theo tập xác thực mới. Nhờ đó, các mô hình trong V2 được đối chiếu trên cùng dữ liệu đánh giá.')
b('Nhánh SVM kết hợp','Văn bản được biểu diễn theo cả cụm từ và đoạn ký tự, sau đó nối hai phần để huấn luyện SVM. Nhánh từ dùng văn bản đã tách từ, còn nhánh ký tự dùng văn bản đã chuẩn hóa. Các cấu hình được thử và lựa chọn bằng kết quả xác thực.')
b('Nhánh PhoBERT','Nhóm mã hóa và huấn luyện như V1, đồng thời đánh giá sau từng lượt học. Lượt thứ 4 được chọn vì có Macro-F1 cao nhất trên tập xác thực tại ngưỡng mặc định.')
b('Kiểm tra bổ sung','Với nhánh SVM cải tiến, kiểm định theo nhóm trên phần huấn luyện được thực hiện sau khi đã chọn cấu hình bằng xác thực. Kết quả này dùng xem xét độ ổn định bổ sung, không thay thế đánh giá cuối.')
h('3.5.3 Hậu xử lý và kiểm tra kết quả V2',2)
b('Bước 5 – Chọn ngưỡng','SVM giữ ranh giới quyết định mặc định. Với PhoBERT đã chọn, nhóm thay đổi ngưỡng từ 0,10 đến 0,90, mỗi lần tăng 0,02, rồi tính lại Macro-F1 trên xác thực. Ngưỡng 0,90 được chọn trong phạm vi khảo sát này.')
b('Bước 6 – Đánh giá','Dùng ngưỡng đã chọn để chuyển điểm thành nhãn, ghép với nhãn thật và tính chỉ số. Với PhoBERT, 824 dự đoán gồm 748 non-toxic đúng, 22 báo nhầm, 21 toxic bị bỏ sót và 33 toxic được phát hiện đúng.')
b('Nghiệm thu đầu ra','Kiểm tra đủ 824 dự đoán, đúng bình luận và đúng nhãn đối chiếu; tổng số mẫu trong ma trận phải khớp dữ liệu. Lưu mô hình, ngưỡng, lịch sử học và bảng dự đoán; việc tải lại để kiểm tra kết quả cần được xác nhận trước bàn giao.')
table('Bảng 3.4 Kết quả bốn baseline V2 đơn vị phần trăm',['Mô hình','Accuracy','F1-toxic','Recall-toxic','Macro-F1'],[['BoW + NB','94,42','51,06','44,44','74,05'],['BoW + SVM','94,90','54,35','46,30','75,82'],['TF-IDF + NB','93,93','21,88','12,96','59,36'],['TF-IDF + SVM','94,66','52,17','44,44','74,67']],[5,2.8,2.8,3,2.9])
b('Nhận xét','SVM kết hợp đạt Macro-F1 78,83%, PhoBERT đạt 78,88%. Mặc dù điểm V2 cao hơn V1, không thể quy toàn bộ mức tăng cho việc tăng dữ liệu huấn luyện vì tập xác thực và cấu hình cũng thay đổi.')

page();h('3.6 Thực nghiệm V3')
h('3.6.1 Chuẩn bị dữ liệu và chia năm phần',2)
b('Mục tiêu','V3 được thực hiện để quan sát kết quả qua nhiều nhóm bài viết, giảm sự phụ thuộc vào một lần chia xác thực cố định. Các mô hình được đánh giá trên cùng cách chia để thuận tiện đối chiếu.')
pipeline('v3_bang_loi','Hình 3.8 Quy trình thực nghiệm V3',[
'1. Gộp phần phát triển\nHuấn luyện và xác thực\n7.669 bình luận',
'2. Chia thành năm phần\nGiữ nguyên nhóm bài\nXét thêm phân bố nhãn',
'3. Luân phiên đánh giá\nHọc trên bốn phần\nDự đoán phần còn lại',
'4. Huấn luyện từng lượt\nKhởi tạo mô hình riêng\nLưu dự đoán từng phần',
'5. Gom dự đoán\nĐúng từng bình luận\nChọn ngưỡng PhoBERT',
'6. Tổng hợp kết quả\nĐiểm và độ biến động\nKiểm tra trước bàn giao'])
b('Bước 1 – Tạo phần dữ liệu phát triển','Gộp tập huấn luyện và xác thực V2 thành 7.669 bình luận thuộc 95 bài viết, trong đó có 499 toxic. Tập kiểm tra 926 bình luận được giữ riêng.')
b('Bước 2 – Chia năm phần','Nhóm sử dụng kiểm định chéo theo nhóm có xét phân bố nhãn. Bình luận cùng bài nằm trong cùng một phần; phương pháp cố gắng giữ tỷ lệ nhãn tương đối cân bằng nhưng không bảo đảm bằng nhau tuyệt đối.')
b('Kiểm tra sau chia','Đối chiếu để mỗi bình luận thuộc đúng một phần, không có bài viết dùng chung giữa các phần và không trùng bài với tập kiểm tra. Cùng cách chia này được dùng cho cả SVM và PhoBERT.')

page();h('3.6.2 Huấn luyện và tạo dự đoán ngoài mẫu',2)
b('Bước 3 – Tổ chức mỗi lượt','Lần lượt chọn một phần để đánh giá và dùng bốn phần còn lại để huấn luyện. Sau năm lượt, mọi bình luận trong phần dữ liệu phát triển đều đã có một lần được đưa ra ngoài tập huấn luyện để dự đoán.')
b('Nhánh SVM','Ở mỗi lượt, nhóm xây mới bộ biểu diễn từ bốn phần huấn luyện, sau đó học mô hình và dự đoán phần còn lại. Ba cấu hình được đối chiếu là BoW + SVM, TF-IDF + SVM và SVM kết hợp từ với ký tự.')
b('Nhánh PhoBERT','Mô hình được khởi tạo và huấn luyện riêng cho từng lượt. Trong mỗi lượt, nhóm theo dõi Macro-F1 trên phần đánh giá để chọn trạng thái mô hình, sau đó lưu điểm dự đoán của phần đó.')
b('Bước 4 – Gom dự đoán','Đưa dự đoán của từng lượt về đúng bình luận ban đầu. Mỗi bình luận cần có đúng một dự đoán từ mô hình không dùng bình luận đó để huấn luyện; đây là bảng dự đoán ngoài mẫu của toàn bộ phần phát triển.')
h('3.6.3 Hậu xử lý và tổng hợp kết quả',2)
b('Bước 5 – Tạo nhãn cuối','SVM dùng ranh giới quyết định mặc định. Với PhoBERT, nhóm khảo sát ngưỡng trên điểm ngoài mẫu, từ 0,20 đến dưới 0,95, mỗi lần tăng 0,05; ngưỡng 0,85 được chọn để tạo nhãn và tính kết quả tổng hợp.')
b('Bước 6 – Tổng hợp hai cách','Tính trung bình và độ lệch chuẩn từ điểm của năm lượt để quan sát mức biến động. Đồng thời, tính chỉ số trên toàn bộ dự đoán ngoài mẫu để xem tổng số phát hiện đúng, bỏ sót và báo nhầm.')
b('Lưu ý khi đánh giá','Phần đánh giá còn được dùng chọn trạng thái PhoBERT và dự đoán ngoài mẫu được dùng chọn ngưỡng. Vì vậy, kết quả vẫn chịu ảnh hưởng của việc lựa chọn, chưa thay thế bước đánh giá cuối độc lập.')
table('Bảng 3.5 Kết quả tổng hợp V3',['Nội dung','SVM kết hợp','PhoBERT'],[['Macro-F1 qua năm lượt (%)','68,94 ± 1,42','71,16 ± 2,39'],['Macro-F1 ngoài mẫu (%)','68,98','71,22'],['Recall-toxic ngoài mẫu (%)','34,67','44,89'],['Báo nhầm / bỏ sót','165 / 326','249 / 275']],[6.5,5,5])
b('Nhận xét','PhoBERT phát hiện đúng nhiều hơn về tổng số nhưng cũng tạo thêm cảnh báo nhầm. Kết quả cho thấy cần cân nhắc cả khả năng phát hiện và khối lượng rà soát khi lựa chọn mô hình.')

page();h('3.6.4 Kiểm tra và chuẩn bị đánh giá cuối',2)
b('Đối chiếu bảng dự đoán','Kiểm tra đủ 7.669 bình luận, không lặp hoặc thiếu dự đoán và giữ đúng nhãn thật. Tổng bốn ô của ma trận nhầm lẫn phải bằng 7.669, trong đó có 499 câu toxic thật.')
b('Kiểm tra tính nhất quán','Hai mô hình phải được so sánh trên cùng các bình luận và cùng phần đánh giá. Mô hình đã lưu cần được tải lại với đúng cách xử lý đầu vào để đối chiếu dự đoán trước khi nghiệm thu.')
b('Kết hợp nhiều mô hình','Với một câu mới, có thể lấy điểm toxic từ năm mô hình rồi tính trung bình và so với ngưỡng. Luồng này khác dự đoán ngoài mẫu: mỗi bình luận ngoài mẫu chỉ nhận dự đoán từ lượt không dùng nó để huấn luyện.')
b('Đánh giá còn cần hoàn tất','Chốt mô hình hoặc cách kết hợp cùng ngưỡng trước khi sử dụng tập kiểm tra 926 câu. Việc áp dụng ngưỡng đã chọn cho mô hình kết hợp cũng cần được kiểm tra riêng; chưa xem điểm ngoài mẫu là kết quả kiểm tra cuối.')
h('3.7 Tổng hợp và nghiệm thu quá trình thực nghiệm')
b('Những bước đã làm rõ','V1 tạo mốc ban đầu; V2 thay đổi cách chia và huấn luyện lại; V3 mở rộng đánh giá qua nhiều nhóm bài. Ở mỗi giai đoạn, dữ liệu đi qua các bước biểu diễn, huấn luyện, lựa chọn và đối chiếu với nhãn thật.')
b('Ưu điểm','Giữ nguyên bài viết khi chia giúp hạn chế trùng ngữ cảnh. Xây bộ biểu diễn chỉ từ phần huấn luyện giúp tránh dùng thông tin của phần đánh giá khi học. Việc lưu kết quả từng lượt tạo cơ sở để đối chiếu và tái kiểm tra.')
b('Nhược điểm','Dữ liệu toxic còn ít và mô hình vẫn bỏ sót nhiều câu. Việc dùng xác thực nhiều lần để lựa chọn có thể làm kết quả cao hơn khi gặp dữ liệu mới. Những hạn chế này cần được nêu cùng các chỉ số đạt được.')
table('Bảng 3.6 Các điều kiện cần xác nhận trước nghiệm thu',['Nội dung','Cách kiểm tra'],[['Dữ liệu đầu vào','Đúng bộ dữ liệu và cách chia; đủ mẫu, đúng nhãn, không trùng bài giữa các phần cần tách.'],['Mô hình và cách xử lý','Giữ được cấu hình, cách biểu diễn và ngưỡng để sử dụng lại.'],['Kết quả đánh giá','Đủ dự đoán; ghép đúng bình luận; chỉ số khớp ma trận nhầm lẫn.'],['Khả năng sử dụng lại','Tải lại mô hình và đối chiếu dự đoán trên cùng dữ liệu.'],['Đánh giá cuối','Chốt lựa chọn trước khi dùng tập kiểm tra; phân biệt rõ với xác thực và ngoài mẫu.']],[4.2,12.3])
b('Trạng thái nghiệm thu','Các điều kiện trên là nội dung cần được xác nhận trước bàn giao. Với bước chưa có kết quả đối chiếu, nhóm cần thực hiện bổ sung thay vì mặc định đã hoàn tất.')

page();h('3.8 Quy trình sử dụng mô hình trên demo')
b('Đầu vào','Người dùng nhập một bình luận cần phân loại. Hệ thống kiểm tra câu có nội dung hợp lệ trước khi xử lý.')
b('Bước 1 – Chuẩn bị mô hình','Nạp mô hình đã được chọn cùng cách biểu diễn hoặc bộ mã hóa và ngưỡng tương ứng. Mô hình chỉ được dùng để dự đoán, không học thêm từ câu người dùng vừa nhập.')
b('Bước 2 – Tiền xử lý','Áp dụng đúng quy tắc đã dùng trong huấn luyện như chuẩn hóa và tách từ. Sau đó, chuyển câu thành dạng đầu vào phù hợp với SVM hoặc PhoBERT.')
b('Bước 3 – Dự đoán','Mô hình tạo điểm cho bình luận. Với SVM, đây là điểm so với ranh giới phân loại; với PhoBERT, đây là điểm của lớp toxic sau khi chuyển đổi đầu ra.')
b('Bước 4 – Hậu xử lý','So điểm với ngưỡng đã chọn để trả nhãn toxic hoặc non-toxic. Khi thay ngưỡng trên cùng câu và cùng mô hình, điểm giữ nguyên nhưng nhãn có thể thay đổi.')
b('Bước 5 – Hiển thị','Trình bày nhãn, điểm và ngưỡng để người dùng biết vì sao câu nhận kết quả đó. Điểm đầu ra không đồng nghĩa với tỷ lệ dự đoán đúng thực tế của câu đang xét.')
b('Bước 6 – Kiểm tra demo','Thử câu bình thường, câu công kích rõ và câu khó; đối chiếu với kết quả chạy cùng mô hình ngoài giao diện. Nếu không tải hoặc chạy được mô hình, cần nhận biết tình trạng đó trước khi giới thiệu kết quả.')
h('3.9 Hướng hoàn thiện')
b('Về đánh giá','Hoàn tất kiểm tra tải lại và đánh giá lựa chọn cuối trên tập kiểm tra. Có thể tách riêng phần chọn mô hình khỏi phần chấm điểm trong từng lượt kiểm định để hạn chế ảnh hưởng của lựa chọn.')
b('Về dữ liệu','Bổ sung các câu toxic và những câu dễ bị báo nhầm; rà soát trường hợp thiếu ngữ cảnh. Sau mỗi thay đổi, giữ cách đánh giá nhất quán để biết thay đổi đó có thực sự đem lại cải thiện hay không.')
f=s.footer.paragraphs[0];f.alignment=WD_ALIGN_PARAGRAPH.CENTER;e=OxmlElement('w:fldSimple');e.set(qn('w:instr'),'PAGE');f._p.append(e)
out=O/'Chuong_3_MO_TA_CACH_LAM_BANG_LOI.docx';d.save(out)
print(out);print('Tables:',len(d.tables),'Diagrams:',len(d.inline_shapes))
assert not any('_' in x.text for x in d.paragraphs)
