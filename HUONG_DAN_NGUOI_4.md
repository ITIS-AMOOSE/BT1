# 📘 HƯỚNG DẪN NGHIỆM THU ĐÁNH GIÁ TẬP TEST TOÀN DIỆN CẢ 3 GIAI ĐOẠN (V1, V2, V3) DÀNH CHO NGƯỜI 4

> **Tài liệu bàn giao nghiệm thu độc lập cho Người 4 (Evaluation Lead & Báo cáo)**  
> **Đề tài BTL I:** Phân loại bình luận của sinh viên PTIT bằng học máy và PhoBERT  
> **Nhóm thực hiện:** Nhóm 12 — Lớp 01 (GVHD: TS. Nguyễn Thị Mai Trang)  
> **Thành viên phụ trách:** Người 4 (Chạy đánh giá trên tập Test, lập bảng phân tích và làm Báo cáo)  
> *(Cập nhật theo Báo cáo chính thức: Đã loại bỏ hoàn toàn Dummy Classifier khỏi các bảng số liệu nghiệm thu)*

---

## 🎯 1. BẢN CHẤT VAI TRÒ CỦA NGƯỜI 4 TRONG ĐỀ TÀI

Theo phân công nhiệm vụ (Bảng 0.1 của Báo cáo):
* **Người 1:** Gộp file, tiền xử lý và chia tập dữ liệu theo `post_id` (chống rò rỉ dữ liệu).
* **Người 2:** Trích chọn đặc trưng (BoW, TF-IDF từ, n-gram ký tự), huấn luyện các mô hình Machine Learning (Naive Bayes, Linear SVM).
* **Người 3:** Thiết lập môi trường và fine-tune mô hình học sâu ngôn ngữ lớn PhoBERT (`vinai/phobert-base-v2`).
* **Người 4 (Bạn):** 
  1. **"Giám khảo độc lập" (Blind Test):** Nắm giữ tập dữ liệu kiểm tra độc lập (`Test set`), không để Người 2 và Người 3 nhìn thấy dữ liệu test trong quá trình huấn luyện hay tinh chỉnh tham số/ngưỡng.
  2. **Nghiệm thu từng giai đoạn (V1, V2, V3):** Chạy kiểm tra độc lập và đối chiếu số liệu thực tế để hoàn thiện các mục trong Báo cáo:
     * **Mục 3.4:** Đánh giá nghiệm thu giai đoạn V1 (Bộ chia cố định 70/15/15 — 1.318 câu test).
     * **Mục 3.5:** Đánh giá nghiệm thu giai đoạn V2 (Bộ chia cố định 80/10/10 — 926 câu test).
     * **Mục 3.6:** Đánh giá nghiệm thu giai đoạn V3 (Kiểm định chéo 5-Fold StratifiedGroupKFold theo `post_id` — 7.669 câu OOF).
     * **Mục 3.7:** Bảng tổng hợp Master Table cả 3 giai đoạn và nhận xét ưu nhược điểm.
     * **Mục 3.8:** Bảng điều khiển Streamlit Dashboard và ứng dụng demo thực tế.

---

## ⚙️ 2. LỆNH CHẠY NGHIỆM THU TỰ ĐỘNG DÀNH CHO NGƯỜI 4

Nhóm đã tối ưu sẵn bộ script tự động [`scripts/run_evaluation_member4.py`](file:///E:/BT1/scripts/run_evaluation_member4.py). Script tự động nhận diện mô hình trên máy, nạp dữ liệu và xuất trực tiếp ra bảng số liệu chuẩn Markdown/CSV.

### 🌟 Cách 1: Chạy toàn bộ cả 3 Version cùng lúc (Khuyên dùng)
Mở Terminal (PowerShell / CMD) tại thư mục `E:\BT1` và gõ:
```bash
python -X utf8 scripts/run_evaluation_member4.py --all
```
*(Script sẽ tự động chạy tuần tự V1 $\rightarrow$ V2 $\rightarrow$ V3 chỉ trong vài giây và xuất ngay bảng Master Table).*

### 🔹 Cách 2: Chạy nghiệm thu từng Version riêng biệt
* **Chạy riêng giai đoạn V1:**
  ```bash
  python -X utf8 scripts/run_evaluation_member4.py --version v1
  ```
* **Chạy riêng giai đoạn V2:**
  ```bash
  python -X utf8 scripts/run_evaluation_member4.py --version v2
  ```
* **Chạy riêng giai đoạn V3:**
  ```bash
  python -X utf8 scripts/run_evaluation_member4.py --version v3
  ```

---

## 📊 3. SỐ LIỆU NGHIỆM THU CHÍNH THỨC ĐỂ ĐƯA VÀO BÁO CÁO (ĐÃ BỎ DUMMY)

### 🔹 MỤC 3.4 BÁO CÁO — NGHIỆM THU GIAI ĐOẠN V1 (TEST SET V1: 1.318 CÂU - 70/15/15)
*File lưu số liệu:* [`reports/final_evaluation/v1_test_evaluation_results.csv`](file:///E:/BT1/reports/final_evaluation/v1_test_evaluation_results.csv)  
*Ảnh minh họa tương ứng trong báo cáo:* Hình 3.7 (So sánh chỉ số V1) và Hình 3.8 (Ma trận nhầm lẫn V1).

| Mô hình | Accuracy | Recall-Toxic | F1-Toxic | **Macro-F1** | TP (Bắt đúng) | FP (Báo nhầm) | FN (Bỏ sót) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **BoW + Naive Bayes** | 93.47% | 47.56% | 47.56% | **72.04%** | 39 | 43 | 43 |
| **TF-IDF + Naive Bayes** | **94.31%** | 8.54% | 15.73% | 56.39% | 7 | **0** | 75 |
| **BoW + Linear SVM** | 92.79% | 48.78% | 45.71% | 70.93% | 40 | 53 | 42 |
| **TF-IDF + Linear SVM** | 87.71% | **56.10%** | 36.22% | 64.71% | **46** | 126 | 36 |
| **PhoBERT v1 (Deep Learning)** | 92.41% | 50.00% | 45.05% | **70.80%** | 41 | 59 | 41 |

* **Nhận xét của Người 4 viết vào Mục 3.4:**
  - Ở V1, tập Train chỉ có 6.000 câu (394 câu toxic) nên mô hình bị thiếu dữ liệu huấn luyện, đặc biệt là các biến thể teencode và từ lóng hiếm gặp.
  - TF-IDF + Naive Bayes gần như chỉ đoán Non-toxic, bỏ sót tới 75/82 câu toxic (Recall chỉ 8.54%).
  - TF-IDF + SVM có Recall cao nhất (56.10%, bắt 46/82 câu) nhưng lại báo nhầm quá nhiều câu Non-toxic (126 ca FP), kéo Macro-F1 xuống 64.71%.
  - PhoBERT v1 và BoW + Naive Bayes đạt Macro-F1 cân bằng nhất (~71% - 72%).

---

### 🔹 MỤC 3.5 BÁO CÁO — NGHIỆM THU GIAI ĐOẠN V2 (TEST SET V2: 926 CÂU - 80/10/10)
*File lưu số liệu:* [`reports/final_evaluation/v2_test_evaluation_results.csv`](file:///E:/BT1/reports/final_evaluation/v2_test_evaluation_results.csv)  
*Ảnh minh họa tương ứng trong báo cáo:* Hình 3.12 (So sánh chỉ số V2) và Hình 3.13 (Ma trận nhầm lẫn V2).

| Mô hình | Accuracy | Recall-Toxic | F1-Toxic | **Macro-F1** | TP (Bắt đúng) | FP (Báo nhầm) | FN (Bỏ sót) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **BoW + Naive Bayes** | 92.98% | 31.67% | 36.89% | 66.59% | 19 | 24 | 41 |
| **TF-IDF + Naive Bayes** | 93.74% | 10.00% | 17.14% | 56.94% | 6 | **4** | 54 |
| **BoW + Linear SVM** | 94.38% | 26.67% | 38.10% | 67.58% | 16 | 8 | 44 |
| **TF-IDF + Linear SVM** | 94.49% | 28.33% | 40.00% | 68.56% | 17 | 8 | 43 |
| **Word+Char SVM Tốt nhất (v2)** | 94.60% | **41.67%** | **50.00%** | **73.57%** | **25** | 15 | 35 |
| **PhoBERT v2 (Tau = 0.90 SOTA)** | **94.82%** | 40.00% | **50.00%** | 🏆 **73.63%** | 24 | 12 | 36 |

* **Nhận xét của Người 4 viết vào Mục 3.5:**
  - Tăng tỷ lệ tập Train lên 80% (6.845 câu, 445 toxic) giúp các mô hình cải thiện khả năng học mẫu câu độc hại.
  - Mô hình cải tiến **Word+Char SVM** (kết hợp n-gram từ [1,2] và n-gram ký tự [3,5]) vượt trội so với các baseline truyền thống, tăng **+5.01%** Macro-F1 so với TF-IDF SVM thông thường (73.57% so với 68.56%), bắt đúng 25/60 câu toxic.
  - **PhoBERT v2** áp dụng ngưỡng tối ưu $\tau = 0.90$ trên Validation dẫn đầu toàn diện với Macro-F1 **73.63%**, kiểm soát báo nhầm rất tốt (chỉ 12 ca FP).

---

### 🔹 MỤC 3.6 BÁO CÁO — NGHIỆM THU KIỂM ĐỊNH CHÉO V3 (5-FOLD GROUPKFOLD & OOF 7.669 CÂU)
*File lưu số liệu:* [`reports/final_evaluation/v3_oof_evaluation_results.csv`](file:///E:/BT1/reports/final_evaluation/v3_oof_evaluation_results.csv)  
*Ảnh minh họa tương ứng trong báo cáo:* Hình 3.15 (Macro-F1 qua 5 fold), Hình 3.16 (So sánh chỉ số OOF V3), Hình 3.17 (Ma trận nhầm lẫn V3).

| Mô hình | Accuracy | Recall-Toxic | F1-Toxic | **Macro-F1 (OOF)** | TP (Bắt đúng) | FP (Báo nhầm) | FN (Bỏ sót) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **BoW + Linear SVM** | **93.85%** | 23.45% | 33.14% | 64.96% *(TB Fold: 64.70% $\pm$ 2.99%)* | 117 | **90** | 382 |
| **TF-IDF + Linear SVM** | 93.82% | 26.85% | 36.12% | 66.44% *(TB Fold: 66.30% $\pm$ 1.86%)* | 134 | 109 | 365 |
| **Word+Char SVM (OOF 5 Folds)** | 93.60% | 34.67% | 41.34% | **68.98%** *(TB Fold: 68.94% $\pm$ 1.42%)* | 173 | 165 | 326 |
| **PhoBERT v2 (OOF 5 Folds SOTA)** | 93.17% | 🏆 **44.89%** | 🏆 **46.09%** | 🏆 **71.22%** *(TB Fold: 71.16% $\pm$ 2.39%)* | 🏆 **224** | 249 | 🏆 **275** |

* **Nhận xét của Người 4 viết vào Mục 3.6:**
  - Đánh giá kiểm định chéo trên toàn bộ pool 7.669 câu loại bỏ hoàn toàn yếu tố may rủi khi chia một tập cố định.
  - **PhoBERT v2** vượt trội hơn Word+Char SVM ở cả 5 fold (+2.22% Macro-F1 trung bình). PhoBERT phát hiện đúng **224/499 câu toxic**, bắt thêm được **+51 câu toxic** so với SVM (Recall đạt 44.89% so với 34.67%).
  - Tuy nhiên, PhoBERT có độ lệch chuẩn lớn hơn (2.39% so với 1.42%), cho thấy mô hình học sâu nhạy cảm hơn với phân phối dữ liệu giữa các cụm bài viết. Word+Char SVM ổn định hơn và ít báo nhầm hơn (165 ca FP so với 249 ca của PhoBERT).

---

### 🌟 MỤC 3.7 BÁO CÁO — BẢNG MASTER TEST TABLE TỔNG HỢP CẢ 3 GIAI ĐOẠN (ĐÃ BỎ DUMMY)
*File lưu số liệu:* [`reports/final_evaluation/master_test_evaluation_all_versions.csv`](file:///E:/BT1/reports/final_evaluation/master_test_evaluation_all_versions.csv)  
*Ảnh minh họa tương ứng:* 🖼️ [`figures_chuong_3/Hinh_3_14_Doi_chieu_toan_dien_3_phien_ban_v1_v2_v3.png`](file:///E:/BT1/figures_chuong_3/Hinh_3_14_Doi_chieu_toan_dien_3_phien_ban_v1_v2_v3.png)

Người 4 copy nguyên văn bảng sau vào Mục 3.7 để so sánh bức tranh tổng thể:

| Giai đoạn | Mô hình | Accuracy | Recall-Toxic | F1-Toxic | **Macro-F1** | TP | FP | FN |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **V1 (70/15/15)** | BoW + Naive Bayes | 93.47% | 47.56% | 47.56% | 72.04% | 39 | 43 | 43 |
| | TF-IDF + Naive Bayes | 94.31% | 8.54% | 15.73% | 56.39% | 7 | 0 | 75 |
| | BoW + Linear SVM | 92.79% | 48.78% | 45.71% | 70.93% | 40 | 53 | 42 |
| | TF-IDF + Linear SVM | 87.71% | **56.10%** | 36.22% | 64.71% | 46 | 126 | 36 |
| | PhoBERT v1 (Deep Learning) | 92.41% | 50.00% | 45.05% | **70.80%** | 41 | 59 | 41 |
| **V2 (80/10/10)** | BoW + Naive Bayes | 92.98% | 31.67% | 36.89% | 66.59% | 19 | 24 | 41 |
| | TF-IDF + Naive Bayes | 93.74% | 10.00% | 17.14% | 56.94% | 6 | 4 | 54 |
| | BoW + Linear SVM | 94.38% | 26.67% | 38.10% | 67.58% | 16 | 8 | 44 |
| | TF-IDF + Linear SVM | 94.49% | 28.33% | 40.00% | 68.56% | 17 | 8 | 43 |
| | **Word+Char SVM Tốt nhất (v2)** | 94.60% | **41.67%** | **50.00%** | **73.57%** | 25 | 15 | 35 |
| | **PhoBERT v2 (Tau = 0.90 SOTA)** | **94.82%** | 40.00% | **50.00%** | 🏆 **73.63%** | 24 | **12** | 36 |
| **V3 (5-Fold CV)**| BoW + Linear SVM | 93.85% | 23.45% | 33.14% | 64.96% | 117 | 90 | 382 |
| | TF-IDF + Linear SVM | 93.82% | 26.85% | 36.12% | 66.44% | 134 | 109 | 365 |
| | Word+Char SVM (OOF 5 Folds) | **93.60%** | 34.67% | 41.34% | **68.98%** | 173 | **165** | 326 |
| | **PhoBERT v2 (OOF 5 Folds SOTA)** | 93.17% | 🏆 **44.89%** | 🏆 **46.09%** | 🏆 **71.22%** | 🏆 **224** | 249 | 🏆 **275** |

---

## 🧩 4. MẪU DỮ LIỆU PHÂN TÍCH LỖI (ERROR ANALYSIS DÀNH CHO MỤC 3.6 / 3.7)

File chi tiết các ca lỗi: [`reports/final_evaluation/v2_test_error_cases.csv`](file:///E:/BT1/reports/final_evaluation/v2_test_error_cases.csv). Người 4 trích 4 trường hợp tiêu biểu đưa vào bảng phân tích lỗi:

| STT | Nội dung bình luận | Nhãn thật | SVM đoán | PhoBERT đoán | Loại lỗi & Bản chất |
| :---: | :--- | :---: | :---: | :---: | :--- |
| 1 | *"Thầy cô dạy có tâm ghê, thi xong trượt sạch cả lớp"* | Toxic (1) | Non-toxic (0) | Non-toxic (0) | **FN (Bỏ sót do mỉa mai ngầm):** Chứa các từ tích cực bề mặt ("có tâm ghê") nhưng mang hàm ý chỉ trích châm biếm. Cả ML và DL đều bị đánh lừa. |
| 2 | *"đm m học ngu như bò mà cứ thích thể hiện clgv"* | Toxic (1) | Toxic (1) | Toxic (1) | **TP (Bắt đúng nhờ n-gram ký tự & ngữ cảnh):** Teencode chửi bới ("đm", "clgv", "ngu như bò") được xử lý tốt. |
| 3 | *"Thằng này bắn đi cho đỡ rác việc"* | Toxic (1) | Toxic (1) | Toxic (1) | **TP (Bắt đúng ngôn từ đe dọa / bạo lực):** Ngữ nghĩa tiêu cực rõ rệt. |
| 4 | *"Môn này khó vãi chưởng, học muốn nổ não luôn á"* | Non-toxic (0) | Toxic (1) | Non-toxic (0) | **FP ở SVM (Báo nhầm cảm thán):** Chứa từ cảm thán mạnh ("vãi chưởng", "nổ não") khiến SVM gắn cờ nhầm, trong khi PhoBERT hiểu ngữ cảnh than thở học tập nên đoán đúng. |

---

## 🖥️ 5. MỤC 3.8 BÁO CÁO — CHẠY DASHBOARD STREAMLIT DEMO

1. **Khởi chạy ứng dụng:**
   ```bash
   streamlit run app.py
   ```
2. Trình duyệt tự mở tại: `http://localhost:8501`.
3. Ảnh chụp giao diện độ phân giải cao sẵn có: [`figures_chuong_3/Hinh_3_12_Giao_dien_dashboard_va_demo.png`](file:///E:/BT1/figures_chuong_3/Hinh_3_12_Giao_dien_dashboard_va_demo.png).

---

## 📁 6. DANH MỤC TÀI NGUYÊN ĐÃ SẴN SÀNG TRONG REPO

| Tài nguyên | Đường dẫn | Ý nghĩa |
| :--- | :--- | :--- |
| **Script chạy nghiệm thu** | [`scripts/run_evaluation_member4.py`](file:///E:/BT1/scripts/run_evaluation_member4.py) | Chạy tự động xuất bảng điểm cho Người 4 |
| **Thư viện phụ thuộc** | [`requirements.txt`](file:///E:/BT1/requirements.txt) | Cài đặt môi trường một dòng lệnh |
| **Dashboard Demo** | [`app.py`](file:///E:/BT1/app.py) | Web app Streamlit phân loại trực tiếp |
| **14 Biểu đồ chuẩn 300 DPI** | [`figures_chuong_3/`](file:///E:/BT1/figures_chuong_3) | Đầy đủ hình từ 3.1 đến 3.17 chèn vào Word/LaTeX |
| **Dữ liệu báo cáo CSV** | [`reports/final_evaluation/`](file:///E:/BT1/reports/final_evaluation) | Lưu trữ vĩnh viễn kết quả nghiệm thu cả 3 ver |
