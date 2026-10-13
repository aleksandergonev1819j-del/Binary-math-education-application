import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image, ImageTk
import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class BinaryEduApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Binary Math Educator")
        self.root.geometry("950x750")

        self.original_image = Image.open(resource_path("background1.jpg"))
        self.bg_copy = self.original_image.copy()
        self.background_image = ImageTk.PhotoImage(self.original_image)
        self.background_label = tk.Label(self.root, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.root.bind('<Configure>', self.resizer)
        self.current_frame = None

        self.show_main_menu()

    def resizer(self, event):
        # FIX: Ensure we only resize when the main window is the one triggering the event
        if event.widget == self.root:
            new_width = event.width
            new_height = event.height
            # Prevent errors if window is minimized (width/height = 0)
            if new_width > 0 and new_height > 0:
                image = self.bg_copy.resize((new_width, new_height))
                self.background_image = ImageTk.PhotoImage(image)
                self.background_label.config(image=self.background_image)

    def clear_screen(self):
        """Removes all widgets from the current screen and creates a centered frame."""
        if self.current_frame:
            self.current_frame.destroy()

        # FIX: Removed conflicting pack() and place(). Kept only place for perfect centering.
        # Added padding so it looks like a nice centered block.
        self.current_frame = tk.Frame(self.background_label, padx=30, pady=30)
        self.current_frame.place(relx=0.5, rely=0.5, anchor="center")

    def show_main_menu(self):
        self.clear_screen()

        tk.Label(self.current_frame, text="Choose an Exercise to Practice!", font=("Arial", 32, "bold")).pack(pady=20)

        exercises = [
            (1, "1. Binary to Decimal (Integer)"),
            (2, "2. Decimal to Binary (Integer)"),
            (3, "3. Decimal to Binary (Floating)"),
            (4, "4. Binary to Decimal (Floating)"),
            (5, "5. Straight Code"),
            (6, "6. Inverse Code"),
            (7, "7. Additional Code"),
            (8, "8. Modified Straight Code (Addition)"),
            (9, "9. Modified Additional Code (Addition)"),
            (10, "10. Inverse Code (Addition)")  # НОВО: Добавено упражнение за събиране в обратен код
        ]

        for ex_num, text in exercises:
            btn = tk.Button(self.current_frame, text=text, width=40, font=("Arial", 14),
                            command=lambda n=ex_num: self.start_exercise(n))
            btn.pack(pady=5)

    # НОВО: Функцията от твоя скрийншот, добавена като метод в класа
    def binary_add_ones_complement(self, code1, code2):
        # Премахваме точката, за да работим с битовете като цели числа
        c1_clean = code1.replace(".", "")
        c2_clean = code2.replace(".", "")
        num_bits = len(c1_clean)

        # Извършваме стандартно двоично събиране
        sum_int = int(c1_clean, 2) + int(c2_clean, 2)
        sum_bin = bin(sum_int)[2:]  # Превръщаме в стрингова репрезентация

        # Проверка за цикличен пренос (ако дължината е по-голяма от оригиналната)
        if len(sum_bin) > num_bits:
            # Взимаме прелялата единица и я добавяме към останалата част
            overflow = sum_bin[:-num_bits]
            remainder = sum_bin[-num_bits:]
            final_sum_int = int(remainder, 2) + int(overflow, 2)
            final_sum_bin = bin(final_sum_int)[2:].zfill(num_bits)
        else:
            final_sum_bin = sum_bin.zfill(num_bits)

        # Форматираме резултата обратно с точка след знаковия бит
        result = f"{final_sum_bin[0]}.{final_sum_bin[1:]}"
        return result

    def start_exercise(self, ex_num):
        self.clear_screen()

        btn_back = tk.Button(self.current_frame, text="< Back to Main Menu", font=("Arial", 12),
                             command=self.show_main_menu)
        btn_back.pack(anchor="nw", side="top", pady=(0, 15))

        self.correct_answer = None
        self.correct_flags = None

        # --- EXERCISE 1 ---
        if ex_num == 1:
            binary_range = random.randint(4, 10)
            binary_str = "".join([str(random.randint(0, 1)) for _ in range(binary_range)])

            total_decimal = 0
            for index, char in enumerate(binary_str):
                digit = int(char)
                power = binary_range - index
                if digit == 1:
                    total_decimal += 2 ** (power - 1)
            self.correct_answer = str(total_decimal)

            tk.Label(self.current_frame, text="Binary to Decimal", font=("Arial", 20, "bold")).pack(pady=10)
            tk.Label(self.current_frame, text=f"Convert this binary number to decimal:\n{binary_str}",
                     font=("Arial", 16)).pack(pady=10)

            self.entry_answer = tk.Entry(self.current_frame, font=("Arial", 18), justify="center", width=20)
            self.entry_answer.pack(pady=10)

            tk.Button(self.current_frame, text="Submit Answer", font=("Arial", 14), width=15,
                      command=lambda: self.check_single_answer(ex_num)).pack(pady=10)

        # --- EXERCISE 2 ---
        elif ex_num == 2:
            decimal_number = random.randint(1, 9999)
            original_number = decimal_number

            binary_result = ""
            while decimal_number > 0:
                binary_result = str(decimal_number % 2) + binary_result
                decimal_number //= 2

            self.correct_answer = binary_result

            tk.Label(self.current_frame, text="Decimal to Binary (Integer)",
                     font=("Arial", 20, "bold")).pack(pady=15)
            tk.Label(self.current_frame, text=f"Convert this decimal number to binary:\n{original_number}",
                     font=("Arial", 16)).pack(pady=15)

            self.entry_answer = tk.Entry(self.current_frame, font=("Arial", 18), justify="center", width=20)
            self.entry_answer.pack(pady=15)

            tk.Button(self.current_frame, text="Submit Answer", font=("Arial", 14), width=15,
                      command=lambda: self.check_single_answer(ex_num)).pack(pady=5)

        # --- EXERCISE 3 ---
        elif ex_num == 3:
            decimal_number = round(random.uniform(0.1, 0.9), 4)
            original = decimal_number

            binary_result = "0."
            precision = 12

            while decimal_number > 0 and len(binary_result) < precision:
                decimal_number *= 2
                bit = int(decimal_number)
                binary_result += str(bit)
                decimal_number -= bit

            self.correct_answer = binary_result

            tk.Label(self.current_frame, text="Decimal to Binary (Floating)",
                     font=("Arial", 20, "bold")).pack(pady=15)
            tk.Label(self.current_frame, text=f"Convert this decimal number to binary:\n{original}",
                     font=("Arial", 16)).pack(pady=15)

            self.entry_answer = tk.Entry(self.current_frame, font=("Arial", 18), justify="center", width=20)
            self.entry_answer.pack(pady=10)

            tk.Button(self.current_frame, text="Submit Answer", font=("Arial", 14), width=15,
                      command=lambda: self.check_single_answer(ex_num)).pack(pady=5)

        # --- EXERCISE 4 ---
        elif ex_num == 4:
            binary_range = random.randint(4, 8)
            fractional = "".join(str(random.randint(0, 1)) for _ in range(binary_range))
            binary_str = "0." + fractional

            total_decimal = 0
            for i, bit in enumerate(fractional):
                if bit == "1":
                    total_decimal += 2 ** (-(i + 1))

            self.correct_answer = str(total_decimal)

            tk.Label(self.current_frame, text="Binary to Decimal (Floating)",
                     font=("Arial", 20, "bold")).pack(pady=15)
            tk.Label(self.current_frame, text=f"Convert this binary number to decimal:\n{binary_str}",
                     font=("Arial", 16)).pack(pady=15)

            self.entry_answer = tk.Entry(self.current_frame, font=("Arial", 18), justify="center", width=20)
            self.entry_answer.pack(pady=10)

            tk.Button(self.current_frame, text="Submit Answer", font=("Arial", 14), width=15,
                      command=lambda: self.check_single_answer(ex_num)).pack(pady=5)

        # --- EXERCISE 5 ---
        elif ex_num == 5:
            sign = random.choice(['+', '-'])
            bits = "".join(str(random.randint(0, 1)) for _ in range(random.randint(4, 8)))

            if sign == '+':
                result = "0." + bits
            else:
                result = "1." + bits

            self.correct_answer = result

            tk.Label(self.current_frame, text="Straight Code", font=("Arial", 20, "bold")).pack(pady=15)
            tk.Label(self.current_frame, text=f"Convert to straight code:\n{sign}0.{bits}", font=("Arial", 16)).pack(
                pady=15)

            self.entry_answer = tk.Entry(self.current_frame, font=("Arial", 18), justify="center", width=20)
            self.entry_answer.pack(pady=10)

            tk.Button(self.current_frame, text="Submit Answer", font=("Arial", 14), width=15,
                      command=lambda: self.check_single_answer(ex_num)).pack(pady=5)

        # --- EXERCISE 6 ---
        elif ex_num == 6:
            sign = random.choice(['+', '-'])
            bits = "".join(str(random.randint(0, 1)) for _ in range(random.randint(4, 8)))

            if sign == '+':
                result = "0." + bits
            else:
                inverted = "".join('1' if b == '0' else '0' for b in bits)
                result = "1." + inverted

            self.correct_answer = result

            tk.Label(self.current_frame, text="Inverse Code", font=("Arial", 20, "bold")).pack(pady=15)
            tk.Label(self.current_frame, text=f"Convert to inverse code:\n{sign}0.{bits}", font=("Arial", 16)).pack(
                pady=15)

            self.entry_answer = tk.Entry(self.current_frame, font=("Arial", 18), justify="center", width=20)
            self.entry_answer.pack(pady=10)

            tk.Button(self.current_frame, text="Submit Answer", font=("Arial", 14), width=15,
                      command=lambda: self.check_single_answer(ex_num)).pack(pady=5)

        # --- EXERCISE 7 ---
        elif ex_num == 7:
            sign = random.choice(['+', '-'])
            bits = "".join(str(random.randint(0, 1)) for _ in range(random.randint(4, 8)))

            if sign == '+':
                result = "0." + bits
            else:
                inverted = "".join('1' if b == '0' else '0' for b in bits)
                plus_one = bin(int(inverted, 2) + 1)[2:].zfill(len(bits))
                result = "1." + plus_one[-len(bits):]

            self.correct_answer = result

            tk.Label(self.current_frame, text="Additional Code", font=("Arial", 20, "bold")).pack(pady=15)
            tk.Label(self.current_frame, text=f"Convert to additional code:\n{sign}0.{bits}", font=("Arial", 16)).pack(
                pady=15)

            self.entry_answer = tk.Entry(self.current_frame, font=("Arial", 18), justify="center", width=20)
            self.entry_answer.pack(pady=10)

            tk.Button(self.current_frame, text="Submit Answer", font=("Arial", 14), width=15,
                      command=lambda: self.check_single_answer(ex_num)).pack(pady=5)

        # --- EXERCISE 8 ---
        elif ex_num == 8:
            binary_range = random.randint(4, 10)
            x_sign, y_sign = random.choice(['+', '-']), random.choice(['+', '-'])
            x_bits = "".join([str(random.randint(0, 1)) for _ in range(binary_range)])
            y_bits = "".join([str(random.randint(0, 1)) for _ in range(binary_range)])

            def to_mok(sign, bits):
                if sign == "+":
                    return "00" + bits
                else:
                    return "11" + "".join(['1' if b == '0' else '0' for b in bits])

            x_mok_str, y_mok_str = to_mok(x_sign, x_bits), to_mok(y_sign, y_bits)
            sum_int = int(x_mok_str, 2) + int(y_mok_str, 2)
            max_len = len(x_mok_str)

            carry = 1 if sum_int >= (2 ** max_len) else 0
            if carry: sum_int = (sum_int - (2 ** max_len)) + 1

            res_binary = bin(sum_int)[2:].zfill(max_len)
            s1, s2 = res_binary[0], res_binary[1]

            z_pk_sign = '0' if s1 == '0' else '1'
            z_pk_bits = res_binary[2:] if s1 == '0' else "".join(['1' if b == '0' else '0' for b in res_binary[2:]])

            self.correct_answer = f"{z_pk_sign}.{z_pk_bits}"
            self.correct_flags = {
                "Z": "1" if s1 == '0' else "0",
                "C": str(carry),
                "N": "1" if s1 == '1' else "0",
                "OV": "1" if s1 != s2 else "0"
            }

            self.breakdown = f"X(mok): {x_mok_str[:2]}.{x_mok_str[2:]}\nY(mok): {y_mok_str[:2]}.{y_mok_str[2:]}\nZ(mok): {s1}{s2}.{res_binary[2:]}"

            tk.Label(self.current_frame, text="Modified Straight Code", font=("Arial", 20, "bold")).pack(
                pady=15)
            tk.Label(self.current_frame, text=f"Perform addition:\n{x_sign}0.{x_bits}  +  {y_sign}0.{y_bits}",
                     font=("Arial", 16)).pack(pady=10)

            tk.Label(self.current_frame, text="Z(pk) result:", font=("Arial", 14)).pack()
            self.entry_answer = tk.Entry(self.current_frame, font=("Arial", 18), justify="center", width=20)
            self.entry_answer.pack(pady=10)

            tk.Label(self.current_frame, text="Enter Flags (0 or 1):", font=("Arial", 14)).pack(pady=10)
            flags_frame = tk.Frame(self.current_frame)
            flags_frame.pack()

            font_flags = ("Arial", 14)
            tk.Label(flags_frame, text="Z:", font=font_flags).grid(row=0, column=0)
            self.entry_z = tk.Entry(flags_frame, width=5, font=font_flags, justify="center")
            self.entry_z.grid(row=0, column=1, padx=5)

            tk.Label(flags_frame, text="C:", font=font_flags).grid(row=0, column=2)
            self.entry_c = tk.Entry(flags_frame, width=5, font=font_flags, justify="center")
            self.entry_c.grid(row=0, column=3, padx=5)

            tk.Label(flags_frame, text="N:", font=font_flags).grid(row=0, column=4)
            self.entry_n = tk.Entry(flags_frame, width=5, font=font_flags, justify="center")
            self.entry_n.grid(row=0, column=5, padx=5)

            tk.Label(flags_frame, text="OV:", font=font_flags).grid(row=0, column=6)
            self.entry_ov = tk.Entry(flags_frame, width=5, font=font_flags, justify="center")
            self.entry_ov.grid(row=0, column=7, padx=5)

            tk.Button(self.current_frame, text="Submit Answer", font=("Arial", 14), width=15,
                      command=lambda: self.check_complex_answer(ex_num)).pack(pady=15)

        # --- EXERCISE 9 ---
        elif ex_num == 9:
            binary_range = random.randint(4, 8)
            x_sign, y_sign = random.choice(['+', '-']), random.choice(['+', '-'])
            x_bits = "".join(str(random.randint(0, 1)) for _ in range(binary_range))
            y_bits = "".join(str(random.randint(0, 1)) for _ in range(binary_range))

            def to_mdk(sign, bits):
                if sign == '+':
                    return "00" + bits
                else:
                    inverted = "".join('1' if b == '0' else '0' for b in bits)
                    plus_one = bin(int(inverted, 2) + 1)[2:].zfill(len(bits))
                    return "11" + plus_one

            x_mdk = to_mdk(x_sign, x_bits)
            y_mdk = to_mdk(y_sign, y_bits)

            sum_int = int(x_mdk, 2) + int(y_mdk, 2)
            max_len = len(x_mdk)

            carry = 1 if sum_int >= 2 ** max_len else 0
            sum_int %= 2 ** max_len

            res_binary = bin(sum_int)[2:].zfill(max_len)
            s1, s2 = res_binary[0], res_binary[1]

            overflow = "1" if s1 != s2 else "0"
            negative = "1" if s1 == '1' else "0"
            is_zero = "1" if s1 == '0' else "0"

            self.correct_answer = f"{s1}.{res_binary[2:]}"
            self.correct_flags = {
                "Z": is_zero,
                "C": str(carry),
                "N": negative,
                "OV": overflow
            }

            self.breakdown = f"X(MDK): {x_mdk[:2]}.{x_mdk[2:]}\nY(MDK): {y_mdk[:2]}.{y_mdk[2:]}\nZ(MDK): {s1}{s2}.{res_binary[2:]}"

            tk.Label(self.current_frame, text="Modified Additional Code", font=("Arial", 20, "bold")).pack(
                pady=15)
            tk.Label(self.current_frame, text=f"Perform addition:\n{x_sign}0.{x_bits}  +  {y_sign}0.{y_bits}",
                     font=("Arial", 16)).pack(pady=10)

            tk.Label(self.current_frame, text="Z(dk) result:", font=("Arial", 14)).pack()
            self.entry_answer = tk.Entry(self.current_frame, font=("Arial", 18), justify="center", width=20)
            self.entry_answer.pack(pady=10)

            tk.Label(self.current_frame, text="Enter Flags (0 or 1):", font=("Arial", 14)).pack(pady=5)
            flags_frame = tk.Frame(self.current_frame)
            flags_frame.pack()

            font_flags = ("Arial", 14)
            tk.Label(flags_frame, text="Z:", font=font_flags).grid(row=0, column=0)
            self.entry_z = tk.Entry(flags_frame, width=5, font=font_flags, justify="center")
            self.entry_z.grid(row=0, column=1, padx=5)

            tk.Label(flags_frame, text="C:", font=font_flags).grid(row=0, column=2)
            self.entry_c = tk.Entry(flags_frame, width=5, font=font_flags, justify="center")
            self.entry_c.grid(row=0, column=3, padx=5)

            tk.Label(flags_frame, text="N:", font=font_flags).grid(row=0, column=4)
            self.entry_n = tk.Entry(flags_frame, width=5, font=font_flags, justify="center")
            self.entry_n.grid(row=0, column=5, padx=5)

            tk.Label(flags_frame, text="OV:", font=font_flags).grid(row=0, column=6)
            self.entry_ov = tk.Entry(flags_frame, width=5, font=font_flags, justify="center")
            self.entry_ov.grid(row=0, column=7, padx=5)

            tk.Button(self.current_frame, text="Submit Answer", font=("Arial", 14), width=15,
                      command=lambda: self.check_complex_answer(ex_num)).pack(pady=10)

        # --- EXERCISE 10: Inverse Code (Addition) (НОВО) ---
        elif ex_num == 10:
            binary_range = random.randint(4, 6)
            sign1 = random.choice(['+', '-'])
            sign2 = random.choice(['+', '-'])

            # Генериране на случайни битове за двете числа
            bits1 = "".join([str(random.randint(0, 1)) for _ in range(binary_range)])
            bits2 = "".join([str(random.randint(0, 1)) for _ in range(binary_range)])

            bits_1 = "".join([str(random.randint(0, 1)) for _ in range(1)])
            bits_2 = "".join([str(random.randint(0, 1)) for _ in range(1)])

            # Логика за превръщане в обратен код (Inverse Code)
            def get_inverse_code(sign, bits):
                if sign == "+":
                    return f"0.{bits}"
                else:
                    inverted_bits = "".join(['1' if b == '0' else '0' for b in bits])
                    return f"1.{inverted_bits}"

            inverse_code1 = get_inverse_code(sign1, bits1)
            inverse_code2 = get_inverse_code(sign2, bits2)

            # Изпълнение на събирането с помощта на новата функция
            self.correct_answer = self.binary_add_ones_complement(inverse_code1, inverse_code2)

            tk.Label(self.current_frame, text="Inverse Code Addition", font=("Arial", 20, "bold")).pack(
                pady=15)
            tk.Label(self.current_frame,
                     text=f"Add these binary numbers using inverse code:\n{sign1}{bits_1}.{bits1}  +  {sign2}{bits_2}.{bits2}\n\n",
                     font=("Arial", 14)).pack(pady=15)

            self.entry_answer = tk.Entry(self.current_frame, font=("Arial", 18), justify="center", width=20)
            self.entry_answer.pack(pady=10)

            tk.Button(self.current_frame, text="Submit Answer", font=("Arial", 14), width=15,
                      command=lambda: self.check_single_answer(ex_num)).pack(pady=5)

        # FIX: Set text to " " (space) instead of "" to avoid the white dash visual glitch
        self.lbl_feedback = tk.Label(self.current_frame, text=" ", font=("Arial", 14))
        self.lbl_feedback.pack(pady=10)

    def check_single_answer(self, ex_num):
        user_ans = self.entry_answer.get().strip()
        if user_ans == self.correct_answer:
            self.lbl_feedback.config(text="You are right! The answer is correct!", fg="green")
            self.show_try_again_button(ex_num)
        else:
            self.lbl_feedback.config(text=f"You are wrong! The right answer is: {self.correct_answer}", fg="red")
            self.show_try_again_button(ex_num)

    def check_complex_answer(self, ex_num):
        user_ans = self.entry_answer.get().strip()
        z, c, n, ov = self.entry_z.get().strip(), self.entry_c.get().strip(), self.entry_n.get().strip(), self.entry_ov.get().strip()

        is_ans_correct = (user_ans == self.correct_answer)
        are_flags_correct = (z == self.correct_flags["Z"] and c == self.correct_flags["C"] and
                             n == self.correct_flags["N"] and ov == self.correct_flags["OV"])

        if is_ans_correct and are_flags_correct:
            self.lbl_feedback.config(text="You are right! Both code and flags are correct!", fg="green")
        else:
            error_msg = "You are wrong!\n"
            if not is_ans_correct:
                error_msg += f"Correct Z: {self.correct_answer}\n{self.breakdown}\n"
            if not are_flags_correct:
                error_msg += f"Correct Flags: Z={self.correct_flags['Z']}, C={self.correct_flags['C']}, N={self.correct_flags['N']}, OV={self.correct_flags['OV']}"
            self.lbl_feedback.config(text=error_msg, fg="red")

        self.show_try_again_button(ex_num)

    def show_try_again_button(self, ex_num):
        for widget in self.current_frame.winfo_children():
            if isinstance(widget, tk.Button) and widget['text'] == "Try Again":
                return
        btn_retry = tk.Button(self.current_frame, text="Try Again", font=("Arial", 14, "bold"), width=15,
                              command=lambda: self.start_exercise(ex_num), bg="#d9edf7")
        btn_retry.pack(pady=10)
if __name__ == "__main__":
    root = tk.Tk()
    app = BinaryEduApp(root)
    root.mainloop()