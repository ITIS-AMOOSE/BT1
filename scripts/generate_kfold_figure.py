"""
Tạo biểu đồ kết quả kiểm định 5-Fold GroupKFold (v3) chuẩn 300 DPI cho báo cáo Chương 3
"""
import os
import matplotlib.pyplot as plt
import numpy as np

OUTPUT_DIR = "E:/BT1/figures_chuong_3"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Thiết lập font chữ & thẩm mỹ
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#b0bec5'
plt.rcParams['axes.linewidth'] = 1.2

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.8), gridspec_kw={'width_ratios': [1.3, 1]})

# -------------------------------------------------------------
# SUBPLOT 1: SO SÁNH MACRO-F1 QUA 5 FOLD ĐỐI ĐẦU TRỰC DIỆN
# -------------------------------------------------------------
folds = ['Fold 0', 'Fold 1', 'Fold 2', 'Fold 3', 'Fold 4']
x = np.arange(len(folds))
width = 0.20

bow_svm = [64.90, 61.09, 65.47, 69.73, 62.29]
tfidf_svm = [67.39, 64.88, 65.47, 69.40, 64.33]
word_char_svm = [70.62, 66.63, 69.77, 69.61, 68.06]
phobert = [75.04, 69.78, 71.91, 69.64, 69.41]

r1 = ax1.bar(x - 1.5*width, bow_svm, width, label='BoW + SVM (TB: 64.70%)', color='#90caf9', edgecolor='#1565c0')
r2 = ax1.bar(x - 0.5*width, tfidf_svm, width, label='TF-IDF + SVM (TB: 66.30%)', color='#80cbc4', edgecolor='#00695c')
r3 = ax1.bar(x + 0.5*width, word_char_svm, width, label='Word+Char SVM Tốt nhất (TB: 68.94%)', color='#ffb74d', edgecolor='#e65100')
r4 = ax1.bar(x + 1.5*width, phobert, width, label='PhoBERT v2 SOTA (TB: 71.16%)', color='#e53935', edgecolor='#b71c1c')

# Annotate PhoBERT scores on top
for i in range(len(folds)):
    ax1.text(x[i] + 1.5*width, phobert[i] + 0.8, f"{phobert[i]:.1f}%", ha='center', va='bottom', fontsize=8.5, fontweight='bold', color='#b71c1c')

ax1.set_ylabel('Macro-F1 Score (%)', fontsize=11, fontweight='bold')
ax1.set_title('A. Đối đầu Macro-F1 qua 5 Folds độc lập (PhoBERT thắng 5/5 Folds)', fontsize=11, fontweight='bold', pad=12)
ax1.set_xticks(x)
ax1.set_xticklabels(folds, fontsize=10, fontweight='bold')
ax1.set_ylim(55, 80)
ax1.grid(axis='y', linestyle='--', alpha=0.5)
ax1.legend(loc='lower left', fontsize=9, framealpha=0.9)

# -------------------------------------------------------------
# SUBPLOT 2: ĐỐI ĐẦU CHỈ SỐ OUT-OF-FOLD (OOF) TRÊN TOÀN BỘ 7.669 CÂU
# -------------------------------------------------------------
metrics = ['Macro-F1\nOOF', 'F1-Toxic\nOOF', 'Recall-Toxic\n(Độ nhạy)', 'Precision\nToxic']
x2 = np.arange(len(metrics))
w2 = 0.35

svm_oof = [68.98, 41.34, 34.67, 51.18]
phobert_oof = [71.22, 46.09, 44.89, 47.36]

b_svm = ax2.bar(x2 - w2/2, svm_oof, w2, label='Word+Char SVM (Tốt nhất ML)', color='#ffb74d', edgecolor='#e65100')
b_pho = ax2.bar(x2 + w2/2, phobert_oof, w2, label='PhoBERT v2 (Deep Learning)', color='#e53935', edgecolor='#b71c1c')

for i in range(len(metrics)):
    ax2.text(x2[i] - w2/2, svm_oof[i] + 0.8, f"{svm_oof[i]:.1f}%", ha='center', va='bottom', fontsize=8.5, fontweight='bold')
    ax2.text(x2[i] + w2/2, phobert_oof[i] + 0.8, f"{phobert_oof[i]:.1f}%", ha='center', va='bottom', fontsize=8.5, fontweight='bold', color='#b71c1c')

# Highlight Recall difference (+51 toxic comments)
ax2.annotate('PhoBERT bắt thêm\n+51 câu toxic (+10.2%)!',
             xy=(2 + w2/2, 44.89), xytext=(2 - 0.2, 58),
             arrowprops=dict(facecolor='#b71c1c', shrink=0.08, width=1.5, headwidth=6),
             ha='center', fontsize=8.5, fontweight='bold', color='#b71c1c',
             bbox=dict(boxstyle="round,pad=0.3", facecolor="#ffebee", edgecolor="#ef5350"))

ax2.set_ylabel('Điểm số (%)', fontsize=11, fontweight='bold')
ax2.set_title('B. Chỉ số Out-Of-Fold (OOF) tổng hợp trên toàn bộ 7.669 câu', fontsize=11, fontweight='bold', pad=12)
ax2.set_xticks(x2)
ax2.set_xticklabels(metrics, fontsize=9.5, fontweight='bold')
ax2.set_ylim(20, 78)
ax2.grid(axis='y', linestyle='--', alpha=0.5)
ax2.legend(loc='upper right', fontsize=9, framealpha=0.9)

plt.suptitle('HÌNH 3.13: KẾT QUẢ KIỂM ĐỊNH CHÉO 5-FOLD GROUPKFOLD (PHIÊN BẢN V3) GIỮA SVM VÀ PHOBERT', fontsize=12, fontweight='bold', y=0.98)
plt.tight_layout()

save_path = os.path.join(OUTPUT_DIR, "Hinh_3_13_Ket_qua_kiem_dinh_5_Fold_GroupKFold_v3.png")
plt.savefig(save_path, dpi=300)
plt.close()

print(f"🎉 Đã tạo thành công ảnh kiểm định K-Fold v3 chuẩn 300 DPI: {save_path}")

