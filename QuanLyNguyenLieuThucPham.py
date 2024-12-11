import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from tkcalendar import DateEntry

# Global Data Lists
danh_sach_nhan_vien = []
item_list = []
invoice_list = []


# main
def main_window():
    root = tk.Tk()

    root.title("Giao Diện Quản Lý Cửa Hàng Nguyên Liệu Thực Phẩm")
    root.geometry('1200x900')

    # Main Frames
    button_frame = tk.Frame(root, width=300, height=700, bg="#1E90FF")
    button_frame.pack(side="left", fill="y")

    HienThi_frame = tk.Frame(root, width=700, height=630)
    HienThi_frame.pack(side="right", fill="both", expand=True)

    # Buttons
    # Thêm chiều cao, chiều rộng và căn chỉnh trái phải cho các nút
    tk.Button(button_frame, text="Nhân Viên", width=20, height=2, bg="#FFFF00",
              command=lambda: hien_thi_nhan_vien(HienThi_frame)).pack(padx=20, pady=10, fill='x')
    tk.Button(button_frame, text="Danh Sách Nguyên Liệu", width=20, height=2, bg="#FFD700",
              command=lambda: hien_thi_nguyen_lieu(HienThi_frame)).pack(padx=20, pady=10, fill='x')
    tk.Button(button_frame, text="Hoá Đơn", width=20, height=2, bg="#FFA500",
              command=lambda: hien_thi_hoa_don(HienThi_frame)).pack(padx=20, pady=10, fill='x')
    tk.Button(button_frame, text="Tính Doanh Thu", width=20, height=2, bg="#FF8C00",
              command=lambda: hien_thi_doanh_thu(HienThi_frame)).pack(padx=20, pady=10, fill='x')

    root.mainloop()
    # Clear Frame


def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()


# Nhân Viên
def xoa_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()


# Quản Lý Nhân Viên
def hien_thi_nhan_vien(HienThi_frame):
    xoa_frame(HienThi_frame)
    tk.Label(HienThi_frame, text="Quản Lý Nhân Viên", font=("Arial", 17, "bold"), fg="#7B68EE", bg="lightyellow",
             relief="groove", bd=9).grid(row=0, column=0, columnspan=4, pady=10)

    MaNV = tk.Entry(HienThi_frame)
    TenNV = tk.Entry(HienThi_frame)
    SdtNV = tk.Entry(HienThi_frame)
    Calam = tk.Entry(HienThi_frame)
    TimNV = tk.Entry(HienThi_frame)

    tk.Label(HienThi_frame, text="Mã Nhân Viên:", relief="solid", bd=2).grid(row=1, column=0, pady=5)
    MaNV.grid(row=1, column=1, pady=5)

    tk.Label(HienThi_frame, text="Họ Tên Nhân Viên:", relief="solid", bd=2).grid(row=2, column=0, pady=5)
    TenNV.grid(row=2, column=1, pady=5)

    tk.Label(HienThi_frame, text="Số Điện Thoại:", relief="solid", bd=2).grid(row=3, column=0, pady=5)
    SdtNV.grid(row=3, column=1, pady=5)

    tk.Label(HienThi_frame, text="Nhập Ca Làm:", relief="solid", bd=2).grid(row=4, column=0, pady=5)
    Calam.grid(row=4, column=1, pady=5)

    tk.Label(HienThi_frame, text="Nhập Mã Nhân Viên để tìm:", relief="solid", bd=2).grid(row=5, column=0, pady=5)
    TimNV.grid(row=5, column=1, pady=5)

    danh_sach_nhan_vien_listbox = tk.Listbox(HienThi_frame, width=150, height=20)
    danh_sach_nhan_vien_listbox.grid(row=6, column=0, columnspan=4, pady=10)

    def cap_nhat_danh_sach_nhan_vien(Nhap_Vao=""):
        danh_sach_nhan_vien_listbox.delete(0, tk.END)
        for nhan_vien in danh_sach_nhan_vien:
            thong_tin_nhan_vien = f"Mã NV-: {nhan_vien['Mã Nhân Viên']} | Tên Nhân Viên-: {nhan_vien['Tên Nhân Viên']} | " \
                                  f"SĐT-: {nhan_vien['Số Điện Thoại']} | Ca Làm-: {nhan_vien['Ca Làm']} | Số Lượng Bán-: {nhan_vien['Số Lượng Bán']}"
            if Nhap_Vao.lower() in thong_tin_nhan_vien.lower():
                danh_sach_nhan_vien_listbox.insert(tk.END, thong_tin_nhan_vien)

    def them_nhan_vien():
        if not MaNV.get() or not TenNV.get() or not SdtNV.get() or not Calam.get():
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin nhân viên!")
            return

        try:
            int(SdtNV.get())
        except ValueError:
            messagebox.showerror("Lỗi", "Phần số điện thoại vừa nhập có kí tự không hợp lệ!")
            return

        danh_sach_nhan_vien.append({
            "Mã Nhân Viên": MaNV.get(),
            "Tên Nhân Viên": TenNV.get(),
            "Số Điện Thoại": SdtNV.get(),
            "Ca Làm": Calam.get(),
            "Số Lượng Bán": 0})
        cap_nhat_danh_sach_nhan_vien()
        messagebox.showinfo("Thành Công", "Nhân Viên đã được thêm!")

    def xoa_nhan_vien():
        nv_chon_xoa = danh_sach_nhan_vien_listbox.curselection()
        if nv_chon_xoa:
            nhan_vien_cho_chon = danh_sach_nhan_vien[nv_chon_xoa[0]]
            danh_sach_nhan_vien.remove(nhan_vien_cho_chon)
            cap_nhat_danh_sach_nhan_vien()
            messagebox.showinfo("Thành Công", "Nhân viên đã được xóa!")
        else:
            messagebox.showerror("Lỗi", "Vui lòng chọn nhân viên để xóa!")

    def sua_nhan_vien():
        nv_chon_sua = danh_sach_nhan_vien_listbox.curselection()
        if nv_chon_sua:
            nhan_vien_cho_chon = danh_sach_nhan_vien[nv_chon_sua[0]]
            nhan_vien_cho_chon['Mã Nhân Viên'] = MaNV.get()
            nhan_vien_cho_chon['Tên Nhân Viên'] = TenNV.get()
            nhan_vien_cho_chon['Số Điện Thoại'] = SdtNV.get()
            nhan_vien_cho_chon['Ca Làm'] = Calam.get()
            cap_nhat_danh_sach_nhan_vien()
            messagebox.showinfo("Thành Công", "Nhân viên đã được sửa!")
        else:
            messagebox.showerror("Lỗi", "Vui lòng chọn nhân viên để sửa!")

    def tim_kiem_nhan_vien():
        Tim_NV = TimNV.get()
        danh_sach_nhan_vien_khop = [nhan_vien for nhan_vien in danh_sach_nhan_vien if
                                    Tim_NV.lower() in nhan_vien['Mã Nhân Viên'].lower()]

        if not danh_sach_nhan_vien_khop:
            messagebox.showinfo("Thông Báo", "Mã Nhân Viên không tồn tại!")
        else:
            cap_nhat_danh_sach_nhan_vien(Tim_NV)

    def tinh_luong_nhan_vien():
        nv_chon_tl = danh_sach_nhan_vien_listbox.curselection()
        if nv_chon_tl:
            nhan_vien_cho_chon = danh_sach_nhan_vien[nv_chon_tl[0]]
            so_luong_ban = nhan_vien_cho_chon['Số Lượng Bán']
            luong_co_ban = 6000000
            thuong = 100000 if so_luong_ban > 100 else 0
            tong_luong = luong_co_ban + thuong
            messagebox.showinfo("Lương Nhân Viên",
                                f"Lương của {nhan_vien_cho_chon['Tên Nhân Viên']} là: {tong_luong:,} VND")
        else:
            messagebox.showerror("Lỗi", "Vui lòng chọn nhân viên để tính lương!")

    tk.Button(HienThi_frame, text="Thêm Nhân Viên", command=them_nhan_vien, width=20, height=2, bg="#00FFFF").grid(row=3, column=2, padx=10, pady=10, sticky="nsew")
    tk.Button(HienThi_frame, text="Xóa Nhân Viên", command=xoa_nhan_vien, width=20, height=2, bg="#7CFC00").grid(row=7,column=0,padx=10,pady=10,sticky="nsew")
    tk.Button(HienThi_frame, text="Sửa Nhân Viên", command=sua_nhan_vien, width=20, height=2, bg="#7CFC00").grid(row=7,column=1,padx=10,pady=10,sticky="nsew")
    tk.Button(HienThi_frame, text="Tìm Kiếm", command=tim_kiem_nhan_vien, width=20, height=2, bg="#7CFC00").grid(row=7,column=2,padx=10,pady=10,sticky="nsew")
    tk.Button(HienThi_frame, text="Tính Lương", command=tinh_luong_nhan_vien, width=20, height=2, bg="#7CFC00").grid(row=7, column=3, padx=10, pady=10, sticky="nsew")

    cap_nhat_danh_sach_nhan_vien()


# Nguyên liệu thực phẩm
def hien_thi_nguyen_lieu(HienThi_frame):
    xoa_frame(HienThi_frame)
    tk.Label(HienThi_frame, text="Quản Lý Nguyên Liệu", font=("Arial", 17, "bold"), fg="#7B68EE", bg="lightyellow",
             relief="groove", bd=9).grid(row=0, column=0, columnspan=4, pady=10)

    MaN = tk.Entry(HienThi_frame)
    TenN = tk.Entry(HienThi_frame)
    KHangN = tk.Entry(HienThi_frame)
    GiaN = tk.Entry(HienThi_frame)
    TimMaN = tk.Entry(HienThi_frame)  # Thêm ô tìm kiếm mã nguyên liệu

    tk.Label(HienThi_frame, text="Mã Nguyên Liệu:", relief="solid", bd=2).grid(row=1, column=0, pady=5)
    MaN.grid(row=1, column=1, pady=5)

    tk.Label(HienThi_frame, text="Tên Nguyên Liệu:", relief="solid", bd=2).grid(row=2, column=0, pady=5)
    TenN.grid(row=2, column=1, pady=5)

    tk.Label(HienThi_frame, text="Khối lượng nguyên liệu (Dạng: g hoặc ml):", relief="solid", bd=2).grid(row=3,column=0,pady=5)
    KHangN.grid(row=3, column=1, pady=5)

    tk.Label(HienThi_frame, text="Giá Nguyên Liệu  (VNĐ):", relief="solid", bd=2).grid(row=4, column=0, pady=5)
    GiaN.grid(row=4, column=1, pady=5)

    tk.Label(HienThi_frame, text="Nhập Mã Nguyên Liệu Để Tìm:", relief="solid", bd=2).grid(row=5, column=0, pady=5)
    TimMaN.grid(row=5, column=1, pady=5)

    danh_sach_nguyen_lieu = tk.Listbox(HienThi_frame, width=150, height=20)
    danh_sach_nguyen_lieu.grid(row=6, column=0, columnspan=5, pady=10)

    def cap_nhat_danh_sach_nguyen_lieu():
        danh_sach_nguyen_lieu.delete(0, tk.END)  # Xóa các mục cũ
        for nguyen_lieu in item_list:
            danh_sach_nguyen_lieu.insert(tk.END,
                                         f"Mã Nguyên Liệu: {nguyen_lieu['Mã Nguyên Liệu']}| Tên Nguyên Liệu: {nguyen_lieu['Tên Nguyên Liệu']}| Khối lượng Nguyên Liệu: {nguyen_lieu['Khối lượng Nguyên Liệu']}| Giá Nguyên Liệu: {nguyen_lieu['Giá Nguyên Liệu(VNĐ)']}")

    def them_nguyen_lieu():
        if not MaN.get() or not TenN.get() or not KHangN.get() or not GiaN.get():
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin của nguyên liệu!")
            return
        # Kiểm tra giá trị nhập vào không phải số âm
        try:
            gia_tri = int(GiaN.get())
            if gia_tri < 0:
                raise ValueError("Giá nguyên liệu không thể là số âm.")
        except ValueError as e:
            messagebox.showerror("Lỗi", f"Giá nguyên liệu không hợp lệ: {e}. Vui lòng nhập lại giá trị hợp lệ.")
            GiaN.delete(0, tk.END)
            GiaN.focus()
            return

        item_list.append({
            "Mã Nguyên Liệu": MaN.get(),
            "Tên Nguyên Liệu": TenN.get(),
            "Khối lượng Nguyên Liệu": KHangN.get(),
            "Giá Nguyên Liệu(VNĐ)": GiaN.get()
        })
        cap_nhat_danh_sach_nguyen_lieu()
        messagebox.showinfo("Thành Công", "Nguyên Liệu đã được thêm!")

    def xoa_nguyen_lieu():
        selected_index = danh_sach_nguyen_lieu.curselection()
        if selected_index:
            selected_drink = item_list[selected_index[0]]
            item_list.remove(selected_drink)
            cap_nhat_danh_sach_nguyen_lieu()
            messagebox.showinfo("Thành Công", "Nguyên Liệu đã được xóa!")
        else:
            messagebox.showerror("Lỗi", "Vui lòng chọn nguyên liệu để xóa!")

    def sua_nguyen_lieu():
        selected_index = danh_sach_nguyen_lieu.curselection()
        if selected_index:
            selected_item = item_list[selected_index[0]]
            selected_item['Mã Nguyên Liệu'] = MaN.get()
            selected_item['Tên Nguyên Liệu'] = TenN.get()
            selected_item['Khối lượng Nguyên Liệu'] = KHangN.get()
            selected_item['Giá Nguyên Liệu(VNĐ)'] = GiaN.get()
            cap_nhat_danh_sach_nguyen_lieu()
            messagebox.showinfo("Thành Công", "Nguyên liệu đã được sửa!")
        else:
            messagebox.showerror("Lỗi", "Vui lòng chọn nguyên liệu để sửa!")

    def tim_kiem_nguyen_lieu():
        filter_text = TimMaN.get()
        nguyen_lieu_khop = [nguyen_lieu for nguyen_lieu in item_list if
                            filter_text.lower() in nguyen_lieu['Mã Nguyên Liệu'].lower()]

        if not nguyen_lieu_khop:
            messagebox.showinfo("Thông Báo", "Mã Nguyên Liệu không tồn tại!")
        else:
            danh_sach_nguyen_lieu.delete(0, tk.END)
            for nguyen_lieu in nguyen_lieu_khop:
                danh_sach_nguyen_lieu.insert(tk.END,
                                             f"Mã Nguyên Liệu: {nguyen_lieu['Mã Nguyên Liệu']}| Tên Nguyên Liệu: {nguyen_lieu['Tên Nguyên Liệu']}")

    # Gọi các hàm mà không có dấu ngoặc đơn để tránh việc gọi ngay lập tức
    tk.Button(HienThi_frame, text="Thêm Nguyên Liệu", command=them_nguyen_lieu, width=20, height=2, bg="#00FFFF").grid(row=3, column=2, padx=10, pady=10, sticky="e")
    tk.Button(HienThi_frame, text="Xóa Nguyên Liệu", command=xoa_nguyen_lieu, width=20, height=2, bg="#7CFC00").grid(row=8, column=0, padx=10, pady=10, sticky="e")
    tk.Button(HienThi_frame, text="Sửa Nguyên Liệu", command=sua_nguyen_lieu, width=20, height=2, bg="#7CFC00").grid(row=8, column=1, padx=10, pady=10, sticky="e")
    tk.Button(HienThi_frame, text="Tìm Kiếm Nguyên Liệu", command=tim_kiem_nguyen_lieu, width=20, height=2,bg="#7CFC00").grid(row=8, column=2, padx=10, pady=10, sticky="e")

    cap_nhat_danh_sach_nguyen_lieu()

# Hoá Đơn
def hien_thi_hoa_don(HienThi_frame):
    clear_frame(HienThi_frame)
    tk.Label(HienThi_frame, text="Quản Lý Hoá Đơn", font=("Arial", 17, "bold"), fg="#7B68EE", bg="lightyellow", relief="groove", bd=9).grid(row=0, column=0, columnspan=4, pady=10)

    ten_khach_hang = tk.Entry(HienThi_frame)
    tk.Label(HienThi_frame, text="Tên Khách Hàng:", relief="solid", bd=2).grid(row=1, column=0, pady=5)
    ten_khach_hang.grid(row=1, column=1, pady=5)

    nhan_vien_combobox = ttk.Combobox(HienThi_frame, values=[nv["Mã Nhân Viên"] for nv in danh_sach_nhan_vien])
    tk.Label(HienThi_frame, text="Chọn Nhân Viên:", relief="solid", bd=2).grid(row=2, column=0, pady=5)
    nhan_vien_combobox.grid(row=2, column=1, pady=5)

    # Cập nhật lên Listbox để có nhiều lựa chọn nguyên liệu
    nguyen_lieu_listbox = tk.Listbox(HienThi_frame, selectmode=tk.MULTIPLE, height=5)
    for nguyen_lieu in item_list:
        nguyen_lieu_listbox.insert(tk.END, nguyen_lieu["Tên Nguyên Liệu"])

    tk.Label(HienThi_frame, text="Chọn Nguyên Liệu:", relief="solid", bd=2).grid(row=3, column=0, pady=5)
    nguyen_lieu_listbox.grid(row=3, column=1, pady=5)

    # Phần nhập số lượng cho từng thành phần đã chọn
    quantity_entries = {}

    def update_quantity_entries():  # Chọn số lượng nguyên liệu đã chọn
        selected_nguyen_lieu = [nguyen_lieu_listbox.get(i) for i in nguyen_lieu_listbox.curselection()]
        for widget in frame_quantity.winfo_children():
            widget.grid_forget()

        for idx, nguyen_lieu in enumerate(selected_nguyen_lieu):
            tk.Label(frame_quantity, text=f"Số lượng {nguyen_lieu}:").grid(row=idx, column=0, padx=5, pady=5)
            quantity_entries[nguyen_lieu] = tk.Entry(frame_quantity)
            quantity_entries[nguyen_lieu].grid(row=idx, column=1, padx=5, pady=5)

    frame_quantity = tk.Frame(HienThi_frame)
    frame_quantity.grid(row=4, column=0, columnspan=4, pady=10)

    nguyen_lieu_listbox.bind("<<ListboxSelect>>", lambda event: update_quantity_entries())

    ngay_hoa_don = DateEntry(HienThi_frame, date_pattern="yyyy-mm-dd")
    tk.Label(HienThi_frame, text="Ngày Lập Hóa Đơn:", relief="solid").grid(row=5, column=0, pady=5)
    ngay_hoa_don.grid(row=5, column=1, pady=5)

    ma_giam_gia = ["GIAM10", "GIAM20", "GIAM30"]
    ma_giam_gia_combobox = ttk.Combobox(HienThi_frame, values=ma_giam_gia)
    ma_giam_gia_combobox.set("Chọn mã giảm giá")  # Giá trị mặc định
    tk.Label(HienThi_frame, text="Mã Giảm Giá:", relief="solid", bd=2).grid(row=6, column=0, pady=5)
    ma_giam_gia_combobox.grid(row=6, column=1, pady=5)

    # thêm nút mới để chọn loại thanh toán
    loai_thanh_toan = tk.StringVar()
    loai_thanh_toan.set("Thanh Toán Ngay")  # Giá trị mặc định

    tk.Radiobutton(HienThi_frame, text="Đặt Trước Nguyên Liệu", variable=loai_thanh_toan, value="Đặt Trước Nguyên Liệu").grid(row=7, column=0, pady=5)
    tk.Radiobutton(HienThi_frame, text="Thanh Toán Ngay", variable=loai_thanh_toan, value="Thanh Toán Ngay").grid(row=7, column=1, pady=5)

    danh_sach_hoa_don_listbox = tk.Listbox(HienThi_frame, width=150, height=20)
    danh_sach_hoa_don_listbox.grid(row=8, column=0, columnspan=4, pady=10)

    def cap_nhat_danh_sach_hoa_don():
        danh_sach_hoa_don_listbox.delete(0, tk.END)
        for hoa_don in invoice_list:
            # Định dạng số tiền với dấu chấm ngăn cách hàng nghìn
            tong_tien_dinh_dang = "{:,.0f}".format(hoa_don['Tổng Tiền']).replace(",", ".")
            danh_sach_hoa_don_listbox.insert(
                tk.END,
                f"Khách Hàng: {hoa_don['Tên Khách Hàng']} | NV: {hoa_don['Nhân Viên']} | "
                f"Nguyên Liệu: {hoa_don['Nguyên Liệu']} | SL: {hoa_don['Số Lượng']} | "
                f"Tổng Tiền : {tong_tien_dinh_dang} VNĐ | Giảm Giá: {hoa_don['Giảm Giá']}% | "
                f"Loại Hóa đơn : {hoa_don['Loại Thanh Toán']} | "
                f"Ngày Lập: {hoa_don['Ngày Lập']}"
            )

    def them_hoa_don():
        khach_hang = ten_khach_hang.get()
        nhan_vien = nhan_vien_combobox.get()

        # Lấy các thành phần đã chọn từ hộp danh sách
        selected_nguyen_lieu = [nguyen_lieu_listbox.get(i) for i in nguyen_lieu_listbox.curselection()]
        ma_giam = ma_giam_gia_combobox.get()
        ngay = ngay_hoa_don.get()

        # ghi số lượng cho từng thành phần đã chọn
        so_luong = {}
        for nguyen_lieu in selected_nguyen_lieu:
            quantity = quantity_entries.get(nguyen_lieu, tk.Entry()).get()
            if not quantity.isdigit():
                messagebox.showerror("Lỗi", f"Số lượng không hợp lệ cho {nguyen_lieu}")
                return
            so_luong[nguyen_lieu] = int(quantity)

        if khach_hang and nhan_vien and selected_nguyen_lieu and all(so_luong.values()):
            # Tính tổng giá dựa trên thành phần và số lượng đã chọn
            gia_nguyen_lieu_list = [
                next((int(nl["Giá Nguyên Liệu(VNĐ)"]) for nl in item_list if nl["Tên Nguyên Liệu"] == nguyen_lieu), 0)
                for nguyen_lieu in selected_nguyen_lieu
            ]
            tong_tien = sum(gia_nguyen_lieu * so_luong[nguyen_lieu] for nguyen_lieu, gia_nguyen_lieu in zip(selected_nguyen_lieu, gia_nguyen_lieu_list))

            # Xử lý mã giảm giá
            phan_tram_giam_gia = 0
            if ma_giam in ma_giam_gia:
                phan_tram_giam_gia = int(ma_giam.replace("GIAM", ""))

            gia_sau_giam = tong_tien * (1 - phan_tram_giam_gia / 100)

            # Cập nhật doanh thu của nhân viên
            for nv in danh_sach_nhan_vien:
                if nv["Mã Nhân Viên"] == nhan_vien:
                    nv["Số Lượng Bán"] += sum(so_luong.values())

            # Thêm hóa đơn với loại thanh toán
            invoice_list.append({
                "Tên Khách Hàng": khach_hang,
                "Nhân Viên": nhan_vien,
                "Nguyên Liệu": ", ".join(selected_nguyen_lieu),
                "Số Lượng": sum(so_luong.values()),
                "Tổng Tiền": round(gia_sau_giam),
                "Giảm Giá": phan_tram_giam_gia,
                "Ngày Lập": ngay,
                "Loại Thanh Toán": loai_thanh_toan.get()
            })
            cap_nhat_danh_sach_hoa_don()
            messagebox.showinfo("Thành Công", f"Hoá đơn đã được thêm!\nTổng Tiền: {round(gia_sau_giam):,} VNĐ")
        else:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")

    def xoa_hoa_don():
        chi_so_chon = danh_sach_hoa_don_listbox.curselection()
        if chi_so_chon:
            hoa_don_chon = invoice_list[chi_so_chon[0]]
            invoice_list.remove(hoa_don_chon)
            cap_nhat_danh_sach_hoa_don()
            messagebox.showinfo("Thành Công", "Hoá đơn đã được xóa!")
        else:
            messagebox.showerror("Lỗi", "Vui lòng chọn hoá đơn để xóa!")

    def in_hoa_don():
        chi_so_chon = danh_sach_hoa_don_listbox.curselection()
        if chi_so_chon:
            hoa_don_chon = invoice_list[chi_so_chon[0]]
            filename = f"HoaDon_{hoa_don_chon['Tên Khách Hàng']}.pdf"

            # Tạo đối tượng canvas để tạo PDF
            c = canvas.Canvas(filename, pagesize=letter)

            c.setFont("Times-Roman", 16)
            c.drawString(200, 750, "HÓA ĐƠN MUA HÀNG")

            # Thông tin khách hàng và nhân viên
            c.setFont("Times-Roman", 12)
            c.drawString(30, 720, f"Tên Khách Hàng: {hoa_don_chon['Tên Khách Hàng']}")
            c.drawString(30, 705, f"Nhân Viên: {hoa_don_chon['Nhân Viên']}")
            c.drawString(30, 690, f"Ngày Lập: {hoa_don_chon['Ngày Lập']}")
            c.drawString(30, 675, f"Loại Thanh Toán: {hoa_don_chon['Loại Thanh Toán']}")  # Payment type

            y_position = 660
            c.drawString(30, y_position, "Chi Tiết Nguyên Liệu:")
            y_position -= 20

            for nguyen_lieu in hoa_don_chon['Nguyên Liệu'].split(", "):
                c.drawString(30, y_position, f"{nguyen_lieu}")
                y_position -= 20

            # Tổng tiền và giảm giá
            y_position -= 20
            c.drawString(30, y_position, f"Tổng Tiền: {hoa_don_chon['Tổng Tiền']:,} VNĐ")
            y_position -= 20
            c.drawString(30, y_position, f"Giảm Giá: {hoa_don_chon['Giảm Giá']}%")

            c.save()

            messagebox.showinfo("In Hóa Đơn", f"Hóa đơn đã được in thành công ra file {filename}!")
        else:
            messagebox.showerror("Lỗi", "Vui lòng chọn hoá đơn để in!")

    tk.Button(HienThi_frame, text="Thêm Hoá Đơn", command=them_hoa_don, width=20, height=2, bg="#00FFFF").grid(row=3,column=2,padx=5,pady=10,sticky="e")
    tk.Button(HienThi_frame, text="Xóa Hoá Đơn", command=xoa_hoa_don, width=20, height=2, bg="#7CFC00").grid(row=9,column=0,padx=5,pady=10,sticky="e")
    tk.Button(HienThi_frame, text="In Hoá Đơn", command=in_hoa_don, width=20, height=2, bg="#7CFC00").grid(row=9,column=1,padx=5,pady=10,sticky="e")

    cap_nhat_danh_sach_hoa_don()

# Doanh Thu
def hien_thi_doanh_thu(HienThi_frame):
    clear_frame(HienThi_frame)
    tk.Label(HienThi_frame, text="Tính Doanh Thu", font=("Arial", 17, "bold"), fg="#7B68EE", bg="lightyellow",
             relief="groove", bd=9).grid(row=0, column=0, columnspan=4, pady=10)

    ngay_bat_dau = DateEntry(HienThi_frame, date_pattern="yyyy-mm-dd")
    tk.Label(HienThi_frame, text="Chọn Ngày Bắt Đầu:").grid(pady=5)
    ngay_bat_dau.grid(pady=5)

    ngay_ket_thuc = DateEntry(HienThi_frame, date_pattern="yyyy-mm-dd")
    tk.Label(HienThi_frame, text="Chọn Ngày Kết Thúc:").grid(pady=5)
    ngay_ket_thuc.grid(pady=5)

    def tinh_doanh_thu():
        # Lấy khoảng thời gian từ hóa đơn
        start_date = datetime.strptime(ngay_bat_dau.get(), "%Y-%m-%d")
        end_date = datetime.strptime(ngay_ket_thuc.get(), "%Y-%m-%d")

        # Lọc hóa đơn và tính tiền theo khoảng thời gian
        tinh_tien = sum(hoa_don["Tổng Tiền"] for hoa_don in invoice_list if
                        start_date <= datetime.strptime(hoa_don["Ngày Lập"], "%Y-%m-%d") <= end_date)
        messagebox.showinfo("Doanh Thu", f"Tổng Doanh Thu trong khoảng thời gian: {tinh_tien:,} VNĐ")

    tk.Button(HienThi_frame, text="Tính Doanh Thu", command=tinh_doanh_thu, width=20, height=2, bg="#7CFC00").grid(
        row=6, column=2, padx=5, pady=10)

main_window()
