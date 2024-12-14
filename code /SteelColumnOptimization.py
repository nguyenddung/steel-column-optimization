import tkinter as tk
from tkinter import messagebox
from math import *
import random

# === Các thông số kỹ thuật mặc định ===
default_values = {
    "f": 3250 ,  # Cường độ chịu kéo tính toán (daN/cm2)
    "fy": 3450,  # Cường độ chảy tiêu chuẩn (daN/cm2)
    "fv": 1885,  # Cường độ chịu cắt/trượt (daN/cm2)
    "gamma_c": 0.95,  # Hệ số an toàn vật liệu
    "E": 2100000,  # Mô đun đàn hồi của thép (daN/cm2)
}


def compute_alpha(phi,A,f ,gamma_c,N):
    alpha = N / (phi * f * gamma_c * A) * 100
    return alpha 
def compute_Ix(bf,hc,tw,tf):
    Ix = bf * hc**3 / 12 - (bf - tw) * (hc - 2 * tf)**3 / 12
    return Ix
def compute_Iy(bf,hw,tw,tf):
    Iy = (2 * tf * bf**3 + hw * tw**3) / 12
    return Iy
def compute_rx(Ix,Ac):
    rx = (Ix / Ac)**0.5 
    return rx
def compute_ry(Iy,Ac):
    ry = (Iy / Ac)**0.5 
    return ry
def compute_lambdacp(alpha):
    lambdacp = 180 - 60 * alpha
    return lambdacp
def compute_A(bf,tf,hw,tw):
    Ac = bf * tf * 2 + hw * tw 
    return Ac
def compute_lambda_Ngang(lambda_X ,lambda_Y, f , E):
    lambda_ = min(lambda_X,lambda_Y) * sqrt(f/E)
    return lambda_
def compute_lambda_X(Lx,rx):
    lambda_X = Lx / rx
    return lambda_X
def compute_lambda_Y(Ly,ry):
    lambda_Y = Ly / ry
    return lambda_Y
def compute_phi(lambda_ngang,f,E):
    if lambda_ngang> 0 and lambda_ngang <= 2.5:
        phi = 1 - (0.073 - 5.53 *f / E) * lambda_ngang ** 1.5
    elif lambda_ngang <= 4.5 :
        phi = 1.47 - 13 * f / E - (0.371 - 27.3 * f / E) * lambda_ngang + (0.0275-5.53 * f/ E) * lambda_ngang**2
    else:
        phi = 332 / (lambda_ngang**2 * (51-lambda_ngang) )
    return phi
def compute_Sy(bf,tf,hw):
    Sy = 0.5 * bf * tf * (tf + hw)
    return Sy
def compute_Sx(Sy,tw,hw):
    Sx = Sy + (tw * hw**2 / 8)
    return Sx
def compute_tau(V , Sx ,Ix , tw):
    tau = abs(V * Sx )/ (Ix * tw) *100
    return tau 
def compute_Wx(Ix,hc):
    Wx = 2 * Ix / hc
    return Wx
def compute_Wy(Iy,bf):
    Wy = 2 * Iy /bf
    return Wy
def compute_sigmaX(N,phi,A):
    sigmaX = N / (phi *A) * 100
    return sigmaX 

#==== condition =======
########################
def check_technical(hc, bf, tf, tw, N, V, Mx, My, L0,params,D) :
    f, fy, fv, gamma_c, E = params.values() # lay cac thong so ki thuat

    # kiem tra dieu kien o 2.1.3.2
    if tw > tf :
        return False
    if bf > 30 * tf:
        return False
    if bf/tf > sqrt(E/f):
        return False
    
    hw  = hc - 2 * tf
    # kiem tra dieu kien o 2.1.3.1
    h = hw + 2 * tf
    if h > D-200:
        return False
    if bf > D - 200:
        return False
    
    if hw < 0:
        return False  # Chiều cao bản bụng không hợp lệ
    Ac = compute_A(bf, tf ,hw , tw)  # dien tich cot trong tam
    if Ac <= 0:
        return False  # Diện tích không hợp lệ
    Lx = 0.7 * L0
    Ly = 0.7 * L0

    Ix = compute_Ix(bf,hc,tw,tf)
    Iy = compute_Iy(bf,hw,tw,tf)

    rx = compute_rx(Ix,Ac)
    ry = compute_ry(Iy,Ac)

    lambdaX = compute_lambda_X(Lx,rx)
    lambdaY = compute_lambda_Y(Ly,ry)

    lambda_ngang = compute_lambda_Ngang(lambdaX,lambdaY ,f , E )
    phi = compute_phi( lambda_ngang,f , E)
    alpha = compute_alpha(phi , Ac ,f ,gamma_c,N)
    lamdacp = compute_lambdacp(alpha)
    # ====check do manh cot ====#
    if lambdaX > lamdacp - 1  or lambdaY > lamdacp - 1 :
        return False
    
    # ====check kiem tra do chiu cat===== #
    Sy = compute_Sy(bf,tf,hw)
    Sx = compute_Sx(Sy,tw,hw)
    tau = compute_tau(V,Sx,Ix,tw)
    if tau > (fv * gamma_c / 10) - 1: 
        return False
    
    # check do ben chiu uon nen :
    Wx = compute_Wx(Ix,hc)
    Wy = compute_Wy(Iy,bf)
    if N/Ac  + My / Wy + Mx / Wx  > 0.95 *f:
        return False
    
    # check dieu kien on dinh tong the cot chiu nen :
    sigma_X = compute_sigmaX(N,phi,Ac)
    if sigma_X  > 0.95 * f / 10 - 1 :
        return False
    
    return True

# === Hàm tạo phương án ngẫu nhiên ===
def generate_random_solution(ranges):
    return tuple(random.uniform(ranges[param][0], ranges[param][1]) for param in ranges)

# === Thuật toán DE ===
def differential_evolution(ranges, L0, max_iterations, F, Cr, params, N, V, Mx, My, D):
    population = []
    while len(population) < max_iterations:
        solution = generate_random_solution(ranges)
        # Chỉ thêm vào population nếu solution hợp lệ
        if check_technical(*solution, N, V, Mx, My, L0, params, D) == True:
            population.append(solution)

    tolerance = 1e-3  # Ngưỡng hội tụ

    for gen in range(max_iterations):
        for i in range(len(population)):
            current = population[i]
            a, b, c = random.sample(population, 3)

            # Sinh vector thử nghiệm
            trial = [
                a[k] + F * (b[k] - c[k]) if random.random() < Cr else a[k]
                for k in range(len(a))
            ]

            # Giới hạn giá trị trong phạm vi ranges
            trial = [
                max(min(trial[k], ranges[param][1]), ranges[param][0])
                for k, param in enumerate(ranges)
            ]
            
            # Kiểm tra tính hợp lệ của vector thử nghiệm
            if check_technical(*trial, N, V, Mx, My, L0, params, D) == True:
                # So sánh với phương án hiện tại, chỉ thay thế nếu tốt hơn
                current_objective = 2 * current[1] * current[2] + (current[0] - 2 * current[2]) * current[3]
                trial_objective = 2 * trial[1] * trial[2] + (trial[0] - 2 * trial[2]) * trial[3]
                if trial_objective < current_objective:
                    population[i] = trial  # Cập nhật vector tốt hơn

        # Kiểm tra hội tụ
        objective_values = [2 * optimal[1] * optimal[2] + (optimal[0] - 2 * optimal[2]) * optimal[3] for optimal in population]
        if max(objective_values) - min(objective_values) < tolerance:
            break

    # Trả về vector có giá trị tốt nhất
    
    return min(
        population,
        key=lambda optimal: 2 * optimal[1] * optimal[2] + (optimal[0] - 2 * optimal[2]) * optimal[3],
    )


# === Các thông số kỹ thuật mặc định ===
default_values = {
    "f": 3250,  # Cường độ chịu kéo tính toán (daN/cm2)
    "fy": 3450,  # Cường độ chảy tiêu chuẩn (daN/cm2)
    "fv": 1885,  # Cường độ chịu cắt/trượt (daN/cm2)
    "gamma_c": 0.95,  # Hệ số an toàn vật liệu
    "E": 2100000,  # Mô đun đàn hồi của thép (daN/cm2)
}

# === Hàm tính toán tối ưu (sử dụng nội dung bạn cung cấp) ===
def run_de():
    try:
        N = float(N_var.get()) 
        V = float(V_var.get()) 
        Mx = float(Mx_var.get()) 
        My = float(My_var.get())
        L0 = float(L0_var.get()) * 1000  # Đổi từ m sang mm
        F = float(F_var.get())
        Cr = float(Cr_var.get())
        D = float(D_var.get())
        max_iterations = int(pop_size_var.get())

        # Lấy các thông số kỹ thuật từ người dùng
        params = {
            "f": float(f_var.get()),
            "fy": float(fy_var.get()),  # Thêm fy vào đây
            "fv": float(fv_var.get()),
            "gamma_c": float(gamma_c_var.get()),
            "E": float(E_var.get())
        }

        # Định nghĩa phạm vi cho các biến thiết kế
        ranges = {
            'hc': (100, D - 200),
            'bf': (181, D - 200),
            'tf': (8, 40),
            'tw': (8, 16),
        }
       
        # Gọi thuật toán tối ưu
        optimal = differential_evolution(ranges, L0, max_iterations, F, Cr, params, N, V, Mx, My, D)

        # Tính diện tích tiết diện
        Ac = 2 * optimal[1] * optimal[2] + (optimal[0] - 2 * optimal[2]) * optimal[3]

        # Hiển thị kết quả
        result.set(
            f"Phương án tối ưu:\n"
            f"Hc: {optimal[0]:.4f} mm\n"
            f"Bf: {optimal[1]:.4f} mm\n"
            f"Tf: {optimal[2]:.4f} mm\n"
            f"Tw: {optimal[3]:.4f} mm\n"
            f"Diện tích tiết diện: {Ac:.4f} mm²"
        )
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi trong quá trình tính toán: {e}")

        


# === Tạo giao diện Tkinter ===
root = tk.Tk()
root.title("Tối ưu tiết diện cột thép")
root.geometry("800x700")

# Tạo các biến lưu giá trị nhập liệu
N_var = tk.StringVar(value="10000")
V_var = tk.StringVar(value="500")
Mx_var = tk.StringVar(value="10000")
My_var = tk.StringVar(value="5000")
D_var = tk.StringVar(value="1200")
L0_var = tk.StringVar(value="20")
F_var = tk.StringVar(value="0.5")
Cr_var = tk.StringVar(value="0.9")
pop_size_var = tk.StringVar(value="100")

f_var = tk.StringVar(value=str(default_values["f"]))
fy_var = tk.StringVar(value=str(default_values["fy"]))
fv_var = tk.StringVar(value=str(default_values["fv"]))
gamma_c_var = tk.StringVar(value=str(default_values["gamma_c"]))
E_var = tk.StringVar(value=str(default_values["E"]))

# === Hàm tạo một dòng nhập liệu ===
def create_input_row(parent, label_text, variable):
    frame = tk.Frame(parent)
    frame.pack(fill="x", padx=5, pady=5)
    tk.Label(frame, text=label_text, width=30, anchor="w").pack(side="left")
    tk.Entry(frame, textvariable=variable).pack(side="left", fill="x", expand=True)

# Các trường nhập liệu
create_input_row(root, "Lực dọc N (daN):", N_var)
create_input_row(root, "Lực cắt V (daN):", V_var)
create_input_row(root, "Momen Mx (daN.cm):", Mx_var)
create_input_row(root, "Momen My (daN.cm):", My_var)
create_input_row(root, "Đường kính cọc khoan D(>200mm):", D_var)
create_input_row(root, "Chiều dài cột L0 (m):", L0_var)
create_input_row(root, "Hệ số khuếch đại F:", F_var)
create_input_row(root, "Chỉ số lai ghép Cr:", Cr_var)
create_input_row(root, "Số vòng lặp:", pop_size_var)
create_input_row(root, "Cường độ chịu kéo (f)((daN/cm2)):", f_var)
create_input_row(root, "Cường độ chảy (fy)(daN/cm2):", fy_var)
create_input_row(root, "Cường độ chịu cắt (fv)(daN/cm2):", fv_var)
create_input_row(root, "Hệ số an toàn (gamma_c):", gamma_c_var)
create_input_row(root, "Mô đun đàn hồi (E)(daN/cm2):", E_var)

# Nút chạy và hiển thị kết quả
result = tk.StringVar()
tk.Button(root, text="Tính toán", command=run_de).pack(pady=10)
tk.Label(root, textvariable=result, fg="blue").pack(pady=10)

root.mainloop()
# #test alpha 
# phi = 0.161 
# A = 12616
# f = 3250
# gamma_c = 0.95 
# N = 10000
# alpha = compute_alpha(phi,A,f,gamma_c,N)
# print('alpha = ',alpha)

#test sigma_x
