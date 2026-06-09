# (1) Phân tích và thiết kế giải pháp

# Biến toàn cục (Global variables):
# - atm_vault_balance: Quản lý tổng lượng tiền mặt vật lý đang có trong két của cây ATM (mặc định ban đầu là 50,000,000 VND).
# - user_account_balance: Quản lý số dư tài khoản số của người dùng hiện tại (mặc định ban đầu là 10,000,000 VND).
# Khi các hàm cần chỉnh sửa giá trị trực tiếp của hai biến này, ta bắt buộc sử dụng từ khóa 'global'.
#
# Biến cục bộ & Cơ chế truyền tham số (Arguments vs Global Variables):
# - Hàm display_balances(): Thao tác đọc trực tiếp từ 2 biến Global để hiển thị dữ liệu mà không cần nhận tham số đầu vào.
# - Hàm deposit_money(amount): Nhận tham số 'amount' (số tiền nạp) từ main. Do tiền nạp trực tiếp làm tăng cả số dư tài khoản lẫn tiền mặt vật lý trong két máy, hàm này cần can thiệp trực tiếp lên 2 biến Global.
# - Hàm check_withdrawal_rules(amount): Nhận tham số 'amount' (số tiền muốn rút) từ main. Hàm chỉ thực hiện kiểm tra logic (tính toán phí 'fee = 1100' nội bộ, kiểm tra bội số, kiểm tra ranh giới số dư của tài khoản và số dư của két ATM) nên chỉ đọc dữ liệu từ các biến Global chứ không chỉnh sửa. Do đó, hàm này trả về (return) các mã trạng thái chuỗi định danh.
# - Hàm execute_withdrawal(total_deduction, amount_to_dispense): Nhận các kết quả đã tính toán từ main để thực hiện cập nhật ghi giảm trực tiếp vào 2 biến Global tương ứng (trừ tài khoản và trừ két ATM).
#
# Giải pháp & Luồng xử lý nghiệp vụ:
# - Tạo hàm main() quản lý vòng lặp vô hạn 'while True' cùng cấu trúc điều hướng rẽ nhánh 'match...case'.
# - Sử dụng phương thức '.isdigit()' kiểm tra dữ liệu đầu vào để bẫy lỗi kiểu dữ liệu (chữ, ký tự đặc biệt, chuỗi trống) và bẫy lỗi số tiền không hợp lệ (nhỏ hơn hoặc bằng 0) trước khi đẩy vào hàm nghiệp vụ.
# - Áp dụng các điều kiện logic lọc lỗi biên cho chức năng rút tiền (bội số của 50,000, lỗi vượt hạn mức tài khoản, lỗi vượt quá lượng tiền mặt trong cây) thông qua mã phản hồi từ hàm kiểm tra để đưa ra quyết định xử lý.

atm_vault_balance = 50000000
user_account_balance = 10000000

def display_balances():
    """
    Hiển thị thông tin số dư tài khoản người dùng và số dư tiền mặt của máy ATM.
    
    Hàm này truy cập trực tiếp vào hai biến toàn cục 'user_account_balance' 
    và 'atm_vault_balance' để in dữ liệu ra màn hình.
    """
    print("--- SỐ DƯ TÀI KHOẢN ---")
    print(f"Tài khoản của bạn: {user_account_balance:,} VND")
    print(f"(Debug) Tiền mặt trong ATM: {atm_vault_balance:,} VND")

def deposit_money(amount):
    """
    Xử lý nạp tiền vào tài khoản người dùng và cập nhật lượng tiền mặt trong máy ATM.
    
    Tham số:
    amount (int): Số tiền người dùng muốn nạp (phải là số nguyên dương).
    
    Giá trị trả về:
    bool: True sau khi thực hiện cập nhật thành công các biến toàn cục.
    """
    global user_account_balance, atm_vault_balance
    user_account_balance += amount
    atm_vault_balance += amount
    return True

def check_withdrawal_rules(amount):
    """
    Kiểm tra các quy định và điều kiện ràng buộc trước khi thực hiện giao dịch rút tiền.
    
    Tham số:
    amount (int): Số tiền khách hàng yêu cầu rút.
    
    Giá trị trả về:
    str: Mã trạng thái kết quả kiểm tra bao gồm:
         - "INVALID_MULTIPLIER": Nếu số tiền không phải là bội số của 50,000.
         - "INSUFFICIENT_FUNDS": Nếu tổng tiền (tiền rút + phí) vượt quá số dư tài khoản.
         - "ATM_OUT_OF_CASH": Nếu số tiền khách rút vượt quá tiền mặt vật lý trong cây ATM.
         - "OK": Nếu thỏa mãn tất cả các điều kiện hợp lệ.
    """
    if amount % 50000 != 0:
        return "INVALID_MULTIPLIER"
        
    fee = 1100
    total_deduction = amount + fee
    
    if total_deduction > user_account_balance:
        return "INSUFFICIENT_FUNDS"
        
    if amount > atm_vault_balance:
        return "ATM_OUT_OF_CASH"
        
    return "OK"

def execute_withdrawal(total_deduction, amount_to_dispense):
    """
    Thực hiện trừ tiền trên hệ thống toàn cục và in hóa đơn biên lai rút tiền thành công.
    
    Tham số:
    total_deduction (int): Tổng số tiền bị trừ khỏi tài khoản người dùng (bao gồm phí).
    amount_to_dispense (int): Số tiền gốc khách hàng nhận được từ máy ATM.
    """
    global user_account_balance, atm_vault_balance
    user_account_balance -= total_deduction
    atm_vault_balance -= amount_to_dispense
    
    print(f"Bạn đã rút thành công {amount_to_dispense:,} VND.")
    print(f"Số dư tài khoản còn lại: {user_account_balance:,} VND.")

def main():
    while True:
        print("============= SMART ATM =============")
        print("1. Xem số dư\n"
              "2. Nạp tiền\n"
              "3. Rút tiền\n"
              "4. Kết thúc giao dịch")
        print("=====================================")
        
        choice = input("Vui lòng chọn giao dịch (1-4): ").strip()
        
        match choice:
            case "1":
                print()
                display_balances()
                print()
                
            case "2":
                print("\n--- NẠP TIỀN ---")
                str_amount = input("Nhập số tiền muốn nạp: ").strip()
                
                if not str_amount.isdigit():
                    print("Số tiền không hợp lệ.")
                    print()
                    continue
                    
                amount = int(str_amount)
                if amount <= 0:
                    print("Số tiền không hợp lệ.")
                    print()
                    continue
                    
                if deposit_money(amount):
                    print(f"Giao dịch thành công! Số dư tài khoản hiện tại: {user_account_balance:,} VND.")
                print()
                
            case "3":
                print("\n--- RÚT TIỀN ---")
                str_amount = input("Nhập số tiền cần rút: ").strip()
                
                if not str_amount.isdigit():
                    print("Số tiền không hợp lệ.")
                    print()
                    continue
                    
                amount = int(str_amount)
                if amount <= 0:
                    print("Số tiền không hợp lệ.")
                    print()
                    continue
                
                rule_status = check_withdrawal_rules(amount)
                
                match rule_status:
                    case "INVALID_MULTIPLIER":
                        print("Số tiền rút phải là bội số của 50,000.")
                    case "INSUFFICIENT_FUNDS":
                        print("Giao dịch thất bại: Số dư tài khoản của bạn không đủ.")
                    case "ATM_OUT_OF_CASH":
                        print("Giao dịch thất bại: Máy ATM không đủ tiền mặt để phục vụ.")
                    case "OK":
                        print("Giao dịch đang xử lý...")
                        fee = 1100
                        print(f"Phí giao dịch: {fee:,} VND")
                        total_deduction = amount + fee
                        execute_withdrawal(total_deduction, amount)
                print()
                
            case "4":
                print("\nCảm ơn quý khách đã sử dụng dịch vụ!")
                break
                
            case _:
                print("Lựa chọn không hợp lệ! Vui lòng chọn lại từ 1 đến 4.\n")

if __name__ == "__main__":
    main()