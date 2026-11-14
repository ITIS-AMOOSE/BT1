"""
Capture high-resolution screenshots of the Streamlit dashboard using Playwright with local Chrome.
"""
import time
from playwright.sync_api import sync_playwright

def capture():
    with sync_playwright() as p:
        print("Đang khởi động Chrome...")
        browser = p.chromium.launch(channel="chrome", headless=True)
        context = browser.new_context(viewport={"width": 1600, "height": 1050}, device_scale_factor=2)
        page = context.new_page()
        
        print("Đang mở http://localhost:8501...")
        page.goto("http://localhost:8501", wait_until="networkidle", timeout=30000)
        time.sleep(4)  # Đợi Streamlit websocket và Plotly load hoàn toàn
        
        # 1. Chụp màn hình Tab 1: Demo & Dashboard chính (Hình 3.12)
        target_path_12 = "E:/BT1/figures_chuong_3/Hinh_3_12_Giao_dien_dashboard_va_demo.png"
        page.screenshot(path=target_path_12, full_page=False)
        print(f"✅ Đã lưu Hình 3.12 chính: {target_path_12}")
        
        # 2. Chụp Tab 2: Thống kê Dữ liệu
        try:
            tab2 = page.locator('button[role="tab"]:has-text("Thống kê Dữ liệu")')
            if tab2.count() > 0:
                tab2.click()
                time.sleep(3)
                target_path_tab2 = "E:/BT1/figures_chuong_3/Hinh_3_12b_Giao_dien_thong_ke_du_lieu.png"
                page.screenshot(path=target_path_tab2, full_page=False)
                print(f"✅ Đã lưu ảnh phụ Thống kê: {target_path_tab2}")
                
            # 3. Chụp Tab 3: Benchmark & Ma trận
            tab3 = page.locator('button[role="tab"]:has-text("So sánh Mô hình")')
            if tab3.count() > 0:
                tab3.click()
                time.sleep(3)
                target_path_tab3 = "E:/BT1/figures_chuong_3/Hinh_3_12c_Giao_dien_so_sanh_mo_hinh.png"
                page.screenshot(path=target_path_tab3, full_page=False)
                print(f"✅ Đã lưu ảnh phụ Benchmark: {target_path_tab3}")
        except Exception as e:
            print(f"Lưu ý khi click tab: {e}")
            
        browser.close()
        print("🎉 HOÀN TẤT CHỤP MÀN HÌNH DASHBOARD STREAMLIT!")

if __name__ == "__main__":
    capture()
