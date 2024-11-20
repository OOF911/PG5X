# Phantom Grid 5X
import pickle
import pdb
import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import time, random
# pdb.set_trace()

def home():
    global p1n, p2n, mode, players, buttons
    for w in root.winfo_children():
        w.destroy()
    try:
        p1n, p2n, mode = namode()
        buttons = [[None for _ in range(5)] for _ in range(5)]
        players = [p1n, p2n]
        create_gui()
    except tk.TclError:
        exit()

def create_board():
    return [[' ' for _ in range(5)] for _ in range(5)]

def disable_buttons():
    for x in range(5):
        for y in range(5):
            buttons[x][y].config(image=symbol_images[2])
            buttons[x][y]["command"] = 0

def is_winner(board, player):
    # Check rows for 4 consecutive symbols
    for row in range(5):
        for col in range(2):
            if board[row][col] == board[row][col+1] == board[row][col+2] == board[row][col+3] == player:
                return True
    
    # Check columns for 4 consecutive symbols
    for col in range(5):
        for row in range(2):
            if board[row][col] == board[row+1][col] == board[row+2][col] == board[row+3][col] == player:
                return True
    
    # Check diagonals (top-left to bottom-right) for 4 consecutive symbols
    for row in range(2):
        for col in range(2):
            if board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3] == player:
                return True

    # Check diagonals (top-right to bottom-left) for 4 consecutive symbols
    for row in range(2):
        for col in range(3, 5):
            if board[row][col] == board[row+1][col-1] == board[row+2][col-2] == board[row+3][col-3] == player:
                return True
    
    return False

def is_tie(board):
    return all(board[i][j] != ' ' for i in range(5) for j in range(5))

def update_board(row, col):
    global winner
    global current_player
    winner = None
    if board[row][col] == ' ':
        board[row][col] = symbols[current_player]
        if mode == "Phantom":
            for x in range(5):
                for y in range(5):
                    buttons[x][y].config(image=random.choice(symbol_images))
        elif mode == "Normal":
            buttons[row][col].config(image=symbol_images[current_player])

        if is_winner(board, symbols[current_player]):
            winner = current_player
            disable_buttons()
            status_label.config(text=f"{players[current_player]} WINS!")
            for x in range(5):
                for y in range(5):
                    buttons[x][y].config(image=symbol_images[symbols.index(board[x][y])])
                    buttons[x][y]["command"] = 0
                    root.update()
                    if board[x][y] != ' ':
                        time.sleep(0.2)
            messagebox.showinfo("Game Over", f"{players[current_player]} WINS!")
            update_winner()
            restart = tk.Button(root, image=r_image, width=50, height=50, highlightthickness=0, bd=0, borderwidth=0, command=create_gui)
            restart.grid(row=6, column=0)
            # root.quit()
        elif is_tie(board):
            winner = None
            disable_buttons()
            status_label.config(text="It's a tie!")
            for x in range(5):
                for y in range(5):
                    buttons[x][y].config(image=symbol_images[symbols.index(board[x][y])])
                    buttons[x][y]["command"] = 0
                    root.update()
                    if board[x][y] != ' ':
                        time.sleep(0.2)
            messagebox.showinfo("Game Over", "It's a tie!")
            update_winner()
            restart = tk.Button(root, image=r_image, width=40, height=40, command=create_gui)
            restart.grid(row=6, column=0)
            # root.quit()
        else:
            current_player = (current_player + 1) % 2
            status_label.config(text=f"{players[current_player]}'S TURN")
    else:
        messagebox.showwarning("Invalid Move", "Spot already occupied. Choose another spot.")

def create_gui():
    global status_label, board
    for w in root.winfo_children():
        w.destroy()

    label = tk.Label(root, text=f"{players[0]}: X    {players[1]}: O", font=("bahnschrift" if os.name=="nt" else "bahnschrift" if os.name == "nt" else "copperplate", 18), fg='#00ffff')
    label.grid(row=0, columnspan=5, pady=10)
    label.configure(bg='black')

    status_label = tk.Label(root, text=f"{players[current_player]}'S TURN", font=("bahnschrift" if os.name=="nt" else "bahnschrift" if os.name == "nt" else "copperplate", 18), bg='black', fg='#ff66ff')
    status_label.grid(row=6, columnspan=5, pady=10)

    e = tk.Button(root, image=e_image, width=50, height=50, command=quit, bd=0, highlightthickness=0, borderwidth=0)
    e.grid(row=0, column=4, padx=0, pady=0)

    home_button = tk.Button(root, image=h_image, width=50, height=50, bd=0, highlightthickness=0, borderwidth=0, command=home)
    home_button.grid(row=0, column=0, padx=0, pady=0)

    board = create_board()

    for i in range(5):
        for j in range(5):
            button = tk.Button(root, image=blank_image, width=80, height=80, command=lambda row=i, col=j: update_board(row, col))
            button.grid(row=i+1, column=j, padx=3, pady=3)
            buttons[i][j] = button

def i1():
    with open("Info/r1.txt") as f:
        messagebox.showinfo(f.readline(), f.read())
def i2():
    with open("Info/r2.txt") as f:
        messagebox.showinfo(f.readline(), f.read())
def i3():
    with open("Info/r3.txt") as f:
        messagebox.showinfo(f.readline(), f.read())
def stop():
    global p1nv, p2nv
    sv.set(" ")
    p1nv.set(" ")
    p2nv.set(" ")
    # sv.destroy()
    # p1n.destroy()
    # p2n.destroy()
    root.destroy()

# Initialize game data
board = create_board()
symbols = ['X', 'O', " "]
current_player = 0

# Initialize GUI
root = tk.Tk()
root.title("Phantom Grid 5X")
root.configure(bg='black')

# Load images
x_image = Image.open("Images/X.jpeg")
o_image = Image.open("Images/O.jpeg")
blank_image = Image.open("Images/Blank.jpeg")
n_image = Image.open("Images/normal.jpeg")
b_image = Image.open("Images/blind.jpeg")
p_image = Image.open("Images/pg5x.jpeg")
q_image = Image.open("Images/q.jpeg")
e_image = Image.open("Images/close.jpeg")
r_image = Image.open("Images/restart.jpeg")
h_image = Image.open("Images/home.jpeg")
x_image = ImageTk.PhotoImage(x_image.resize((95, 95), Image.LANCZOS))
o_image = ImageTk.PhotoImage(o_image.resize((95, 95), Image.LANCZOS))
blank_image = ImageTk.PhotoImage(blank_image.resize((95, 95), Image.LANCZOS))
n_image = ImageTk.PhotoImage(n_image.resize((133, 58), Image.LANCZOS))
b_image = ImageTk.PhotoImage(b_image.resize((133, 58), Image.LANCZOS))
p_image = ImageTk.PhotoImage(p_image.resize((133, 58), Image.LANCZOS))
q_image = ImageTk.PhotoImage(q_image.resize((50, 50), Image.LANCZOS))
e_image = ImageTk.PhotoImage(e_image.resize((50, 50), Image.LANCZOS))
r_image = ImageTk.PhotoImage(r_image.resize((50, 50), Image.LANCZOS))
h_image = ImageTk.PhotoImage(h_image.resize((50, 50), Image.LANCZOS))

symbol_images = [x_image, o_image, blank_image]

def namode():
    global sv, p1nv, p2nv
    welcome = tk.Label(root, text="WELCOME TO THE GRID", font=("bahnschrift" if os.name == "nt" else "copperplate", 18), fg='#00ffff', bg='#000000')
    welcome.grid(row=0, columnspan=2, pady=10)
    label = tk.Label(root, text="CHOOSE GAME MODE", font=("bahnschrift" if os.name == "nt" else "copperplate", 18), fg='#00ffff', bg='#000000')
    label.grid(row=3, columnspan=2, pady=10)

    p1nv = tk.StringVar()
    p2nv = tk.StringVar()
    a = tk.Label(root, text="Enter Player 1 Name:", font=("bahnschrift" if os.name == "nt" else "copperplate", 16), fg='#ff66ff', bg='#000000')
    a.grid(row=1, column=0, padx=10, pady=10)
    b = tk.Label(root, text="Enter Player 2 Name:", font=("bahnschrift" if os.name == "nt" else "copperplate", 16), fg='#ff66ff', bg='#000000')
    b.grid(row=2, column=0, padx=10, pady=10)
    p1 = tk.Entry(root,font=("bahnschrift" if os.name == "nt" else "copperplate", 16), fg="white", bg="black", textvariable=p1nv, )
    p2 = tk.Entry(root,font=("bahnschrift" if os.name == "nt" else "copperplate", 16), fg="white", bg="black", textvariable=p2nv, )
    p1.grid(row=1, column=1, padx=10, pady=10)
    p2.grid(row=2, column=1, padx=10, pady=10)

    sv = tk.StringVar()
    x = tk.Button(root, image=n_image, width=130, height=50, command=lambda: sv.set("Normal"))
    y = tk.Button(root, image=b_image, width=130, height=50, command=lambda: sv.set("Blind"))
    z = tk.Button(root, image=p_image, width=130, height=50, command=lambda: sv.set("Phantom"))
    r1 = tk.Button(root, image=q_image, width=50, height=50, bd=0, highlightthickness=0, command=i1)
    r2 = tk.Button(root, image=q_image, width=50, height=50, bd=0, highlightthickness=0, command=i2)
    r3 = tk.Button(root, image=q_image, width=50, height=50, bd=0, highlightthickness=0, command=i3)
    e = tk.Button(root, image=e_image, width=50, height=50, command=stop, highlightthickness=0, bd=0, borderwidth=0)

    x.grid(row=5, columnspan=2, pady=10)
    y.grid(row=6, columnspan=2, pady=10)
    z.grid(row=7, columnspan=2, pady=10)
    r1.grid(row=5, column=1, padx=0, pady=0)
    r2.grid(row=6, column=1, padx=0, pady=0)
    r3.grid(row=7, column=1, padx=0, pady=0)
    e.grid(row=0, column=2, padx=0, pady=0)
    
    root.wait_variable(p1nv)
    root.wait_variable(p2nv)
    root.wait_variable(sv)

    # a.destroy()
    # b.destroy()
    # p1.destroy()
    # p2.destroy()
    # label.destroy()
    # welcome.destroy()
    # x.destroy()
    # y.destroy()
    # z.destroy()
    # r1.destroy()
    # r2.destroy()
    # r3.destroy()

    return p1nv.get().upper(), p2nv.get().upper(), sv.get()

try:
    p1n, p2n, mode = namode()
    buttons = [[None for _ in range(5)] for _ in range(5)]
    players = [p1n, p2n]
    create_gui()
except tk.TclError:
    exit()


def update_winner():
    if not os.path.exists(os.path.join(os.getcwd(), "players.dat")):
        with open("players.dat", 'wb') as f:
            pickle.dump({}, f)

    with open("players.dat", "rb+") as f:
        try:
            data = pickle.load(f)
        except EOFError:
            data = {}
        if p1n not in data:
            data[p1n] = 0
        if p2n not in data:
            data[p2n] = 0
        if winner != None:
            data[players[winner]] += 1

        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")
        
        sitems = sorted(data.items(), key=lambda x: x[1], reverse=True)
        spw = max(len(max(sitems, key=lambda x: len(x[0]))[0]), 6) + 2
        spn = max(len(str(max(sitems, key=lambda x: x[1])[1])), 4) + 2
        print(" "*((spw-6)//2),
            "Player",
            " "*((spw-6)//2 if (spw-6)/2==(spw-6)//2 else ((spw-6)//2)+1),
            "|",
            " "*((spn-4)//2 if (spn-4)/2==(spn-4)//2 else ((spn-4)//2)+1),
            "Wins",
            sep=""
            )
        print("-"*spw, "+", "-"*spn, sep="")
        for item in sitems:
            print(" "*((spw-len(item[0]))//2),
            item[0],
            " "*((spw-len(item[0]))//2 if (spw-len(item[0]))/2==(spw-len(item[0]))//2 else ((spw-len(item[0]))//2)+1),
            "|",
            " "*((spn-len(str(item[1])))//2 if (spn-len(str(item[1])))/2==(spn-len(str(item[1])))//2 else ((spn-len(str(item[1])))//2)+1),
            item[1],
            sep=""
            )
        f.seek(0)
        pickle.dump(data, f)


root.mainloop()
