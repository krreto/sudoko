import tkinter as tk
import os
from gtts import gTTS

def start_game(level):
    # تحويل رسالة الترحيب إلى كلام
    message = f"لنبدأ لعبة سودوكو على مستوى {level}."
    speech = gTTS(text=message, lang="ar", slow=False)
    speech.save("welcome.mp3")
    os.system("mpg321 welcome.mp3")

    # يمكنك وضع كود اللعبة هنا
    pass

def choose_level():
    level_window = tk.Toplevel(root)
    level_window.title("اختر مستوى الصعوبة")
    level_window.geometry("200x150")
    
    beginner_button = tk.Button(level_window, text="مبتدئ", command=lambda: start_game("مبتدئ"))
    beginner_button.pack(pady=5)

    intermediate_button = tk.Button(level_window, text="متوسط", command=lambda: start_game("متوسط"))
    intermediate_button.pack(pady=5)

    hard_button = tk.Button(level_window, text="صعب", command=lambda: start_game("صعب"))
    hard_button.pack(pady=5)

    expert_button = tk.Button(level_window, text="خبير", command=lambda: start_game("خبير"))
    expert_button.pack(pady=5)

def print_board(board):
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - -")

        for j in range(len(board[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == 8:
                print(board[i][j])
            else:
                print(str(board[i][j]) + " ", end="")

def find_empty_location(board, l):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                l[0] = row
                l[1] = col
                return True
    return False

def is_valid(board, row, col, num):
    for x in range(9):
        if board[row][x] == num or board[x][col] == num:
            return False

    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[i + start_row][j + start_col] == num:
                return False

    return True

def solve_sudoku(board):
    l = [0, 0]

    if not find_empty_location(board, l):
        return True

    row, col = l[0], l[1]

    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num

            if solve_sudoku(board):
                return True

            board[row][col] = 0

    return False

def draw_grid(root, entries):
    for i in range(9):
        for j in range(9):
            entry = tk.Entry(root, width=3, font=('Arial', 14))
            entry.grid(row=i, column=j)
            entry.grid(padx=1, pady=1)
            entry.insert(0, "")  # لا قيم افتراضية
            entries[i][j] = entry

def highlight_duplicates(board, entries):
    for i in range(9):
        for j in range(9):
            num = board[i][j]
            if num != 0:
                for x in range(9):
                    if x != j and board[i][x] == num:
                        entries[i][j].config(bg="red")  # إبراز التكرار في الصف
                        entries[i][x].config(bg="red")  # إبراز التكرار في الصف
                    if x != i and board[x][j] == num:
                        entries[i][j].config(bg="red")  # إبراز التكرار في العمود
                        entries[x][j].config(bg="red")  # إبراز التكرار في العمود

# مثال للوحة سودوكو، 0 تعني مكان فارغ
board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

root = tk.Tk()
root.title("لعبة سودوكو")
root.configure(bg="white")

entries = [[None]*9 for _ in range(9)]
draw_grid(root, entries)

start_button = tk.Button(root, text="بدء اللعبة", command=lambda: start_game("مبتدئ"))
start_button.grid(row=9, column=0, columnspan=9, pady=10)

level_button = tk.Button(root, text="تحديد المستوى", command=choose_level)
level_button.grid(row=10, column=0, columnspan=9, pady=10)

highlight_duplicates(board, entries)

root.mainloop()

if solve_sudoku(board):
    print_board(board)
else:
    print("لا توجد حلول")
