"""
Tạo biểu đồ Master Chart: So sánh tổng hợp trực quan toàn bộ 3 Phiên bản (v1, v2, v3) giữa SVM và PhoBERT
"""
import os
import matplotlib.pyplot as plt
import numpy as np

OUTPUT_DIR = "E:/BT1/figures_chuong_3"
os.makedirs(OUTPUT_DIR, exist_ok=True)

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#b0bec5'
plt.rcParams['axes.linewidth'] = 1.2

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.8))

versions = ['Phiên bản v1\n(70/15/15 - Cơ sở)', 'Phiên bản v2\n(80/10/10 - Mở rộng)', 'Phiên bản v3\n(5-Fold CV - Toàn diện)']
x = np.arange(len(versions))
width = 0.35

# -------------------------------------------------------------
# SUBPLOT 1: SO SÁNH MACRO-F1 QUA 3 PHIÊN BẢN
# -------------------------------------------------------------
svm_f1 = [68.86, 78.83, 68.98]  # v1 Val, v2 Val, v3 OOF
phobert_f1 = [68.88, 78.88, 71.22]

r1 = ax1.bar(x - width/2, svm_f1, width, label='SVM Tốt nhất (Word+Char)', color='#ffb74d', edgecolor='#e65100', linewidth=1.5)
r2 = ax1.bar(x + width/2, phobert_f1, width, label='PhoBERT v2 (Deep Learning)', color='#e53935', edgecolor='#b71c1c', linewidth=1.5)

for i in range(len(versions)):
    ax1.text(x[i] - width/2, svm_f1[i] + 0.8, f"{svm_f1[i]:.2f}%", ha='center', va='bottom', fontsize=9.5, fontweight='bold', color='#e65100')
    ax1.text(x[i] + width/2, phobert_f1[i] + 0.8, f"{phobert_f1[i]:.2f}%", ha='center', va='bottom', fontsize=9.5, fontweight='bold', color='#b71c1c')

# Chú thích tăng vọt ở v2
ax1.annotate('Tăng vọt +10% F1\nnhờ mở rộng tập Train!',
             xy=(1, 78.88), xytext=(0.8, 87),
             arrowprops=dict(facecolor='#1565c0', shrink=0.08, width=1.5, headwidth=6),
             ha='center', fontsize=9, fontweight='bold', color='#1565c0',
             bbox=dict(boxstyle="round,pad=0.3", facecolor="#e3f2fd", edgecolor="#90caf9"))

ax1.set_ylabel('Macro-F1 Score (%)', fontsize=11, fontweight='bold')
ax1.set_title('A. Diễn tiến Macro-F1 qua 3 Phiên bản (v1 ➔ v2 ➔ v3)', fontsize=11, fontweight='bold', pad=12)
ax1.set_xticks(x)
ax1.set_xticklabels(versions, fontsize=10, fontweight='bold')
ax1.set_ylim(55, 92)
ax1.grid(axis='y', linestyle='--', alpha=0.5)
ax1.legend(loc='upper left', fontsize=9.5, framealpha=0.9)

# -------------------------------------------------------------
# SUBPLOT 2: SO SÁNH ĐỘ NHẠY BẮT TOXIC (RECALL-TOXIC)
# -------------------------------------------------------------
svm_recall = [48.19, 59.26, 34.67]
phobert_recall = [44.58, 61.11, 44.89]

b1 = ax2.bar(x - width/2, svm_recall, width, label='SVM Tốt nhất', color='#ffb74d', edgecolor='#e65100', linewidth=1.5)
b2 = ax2.bar(x + width/2, phobert_recall, width, label='PhoBERT v2', color='#e53935', edgecolor='#b71c1c', linewidth=1.5)

for i in range(len(versions)):
    ax2.text(x[i] - width/2, svm_recall[i] + 0.8, f"{svm_recall[i]:.1f}%", ha='center', va='bottom', fontsize=9.5, fontweight='bold')
    ax2.text(x[i] + width/2, phobert_recall[i] + 0.8, f"{phobert_recall[i]:.1f}%", ha='center', va='bottom', fontsize=9.5, fontweight='bold', color='#b71c1c')

# Chú thích PhoBERT bắt thêm ở v3
ax2.annotate('PhoBERT bắt thêm +51 toxic\n(+10.2% Recall) trên toàn bộ dữ liệu',
             xy=(2 + width/2, 44.89), xytext=(2 - 0.2, 60),
             arrowprops=dict(facecolor='#b71c1c', shrink=0.08, width=1.5, headwidth=6),
             ha='center', fontsize=9, fontweight='bold', color='#b71c1c',
             bbox=dict(boxstyle="round,pad=0.3", facecolor="#ffebee", edgecolor="#ef5350"))

ax2.set_ylabel('Recall-Toxic - Khả năng dò quét (%)', fontsize=11, fontweight='bold')
ax2.set_title('B. Khả năng phát hiện bình luận Toxic (Recall-Toxic)', fontsize=11, fontweight='bold', pad=12)
ax2.set_xticks(x)
ax2.set_xticklabels(versions, fontsize=10, fontweight='bold')
ax2.set_ylim(20, 75)
ax2.grid(axis='y', linestyle='--', alpha=0.5)
ax2.legend(loc='upper right', fontsize=9.5, framealpha=0.9)

plt.suptitle('HÌNH 3.14: ĐỐI CHIẾU TOÀN DIỆN KẾT QUẢ 3 PHIÊN BẢN (V1, V2, V3) GIỮA SVM VÀ PHOBERT', fontsize=12, fontweight='bold', y=0.98)
plt.tight_layout()

save_path = os.path.join(OUTPUT_DIR, "Hinh_3_14_Doi_chieu_toan_dien_3_phien_ban_v1_v2_v3.png")
plt.savefig(save_path, dpi=300)
plt.close()

print(f"🎉 Đã tạo thành công Master Chart v1-v2-v3: {save_path}")

