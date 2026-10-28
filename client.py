from customtkinter import *
import socket
import threading
from pygame import mixer
from PIL import Image, ImageTk
from tkinter import filedialog
import io
import binascii
import base64

mixer.init()
send_sound = mixer.Sound('matthewvakaliuk73627-message-send-292621.mp3')

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("localhost", 8080))

win = CTk()
win.geometry("600x600")
win.title("looktiktok")

menu = CTkFrame(win, width=340)
menu.pack(side="left", fill="y")


def set_theme(theme):
    if theme == "dark":
        set_appearance_mode("dark")
    elif theme == "green":
        set_appearance_mode("dark")
        textbox.configure(fg_color="#115e0a")
        stiker_frame.configure(fg_color="#177a0d")
        text_smail.configure(fg_color="#10520a")
        text_smail_cat.configure(fg_color="#10520a")
        text_smail_angre.configure(fg_color="#10520a")
        text_smail_happy.configure(fg_color="#10520a")
        text_smail_genius.configure(fg_color="#10520a")
        menu_buton.configure(fg_color="#10520a")
        text_button.configure(fg_color="#10520a")
        openn.configure(fg_color="#10520a")
        buton_stiker.configure(fg_color="#10520a")
    else:
        set_appearance_mode("light")


openn = CTkOptionMenu(menu, width=140, command=set_theme, values=["dark", "light", "green"])
openn.pack(pady=10)
main_frame = CTkFrame(win, fg_color="transparent")
main_frame.pack(side="right", expand=True, fill="both", padx=10, pady=10)


def togle_menu():
    if menu.winfo_ismapped():
        menu.pack_forget()
    else:
        menu.pack(side="left", fill="y")


menu_buton = CTkButton(main_frame, width=50, height=50, command=togle_menu, text="☰")
menu_buton.pack(anchor="w", padx=10, pady=10)

textbox = CTkScrollableFrame(main_frame)
textbox.pack(padx=10, pady=10, expand=True, fill="both")

name = CTkLabel(menu, text="ваше ім'я")
name.pack(padx=10, pady=10)
name_entry = CTkEntry(menu)
name_entry.pack(padx=10, pady=10)
name_entry.insert("0", "67")


def mesage():
    mesag = text_entry.get()
    if not mesag.strip():
        return
    name = name_entry.get()
    full_mesage = f"{name}: {mesag}\n"
    sock.sendall(full_mesage.encode('utf-8'))
    lbl = CTkLabel(textbox, text=f"Я: {mesag}", font=("Segoe UI Emoji", 14), justify="left", anchor="w")
    lbl.pack(anchor="w", padx=5, pady=2, fill="x")

    text_entry.delete(0, "end")
    send_sound.play()

def emoji():
    text_entry.insert("end", "☺️")

def emoji_cat():
    text_entry.insert("end", "😹")

def emoji_angre():
    text_entry.insert("end", "😡")

def emoji_happy():
    text_entry.insert("end", "🤣")

def emoji_genius():
    text_entry.insert("end", "🧠")


text_frame = CTkFrame(main_frame, fg_color="transparent")
text_frame.pack(fill="x")
text_entry = CTkEntry(text_frame, placeholder_text="ваше повідомлення...", height=50, font=("Segoe UI Emoji", 16))
text_entry.pack(padx=10, pady=10, expand=True, fill="x", side="left")
text_button = CTkButton(text_frame, width=50, height=50, text=">", command=mesage)
text_button.pack(padx=10, pady=10, side="right")

stiker_frame = CTkFrame(win, fg_color="transparent", height=150, width=200)
is_visible = False


def open_emoji():
    global is_visible
    if is_visible:
        stiker_frame.place_forget()
        is_visible = False
    else:
        stiker_frame.place(x=1400, y=430)
        is_visible = True


text_smail = CTkButton(stiker_frame, width=50, height=50, text="😄", font=("Segoe UI Emoji", 24), command=emoji)
text_smail.pack(padx=10, pady=10, side="left")

text_smail_cat = CTkButton(stiker_frame, width=50, height=50, text="😹", font=("Segoe UI Emoji", 24), command=emoji_cat)
text_smail_cat.pack(padx=10, pady=10, side="top")

text_smail_angre = CTkButton(stiker_frame, width=50, height=50, text="😡", font=("Segoe UI Emoji", 24),command=emoji_angre)
text_smail_angre.pack(padx=10, pady=10, side="top")

text_smail_happy = CTkButton(stiker_frame, width=50, height=50, text="😂", font=("Segoe UI Emoji", 24), command=emoji_happy)
text_smail_happy.pack(padx=10, pady=10, side="top")

text_smail_genius = CTkButton(stiker_frame, width=50, height=50, text="🧠", font=("Segoe UI Emoji", 24), command=emoji_genius)
text_smail_genius.pack(padx=10, pady=10, side="top")

buton_stiker = CTkButton(text_frame, width=50, height=50, text="😹", command=open_emoji)
buton_stiker.pack(padx=10, pady=10, side="left")


def open_images():
    fille = filedialog.askopenfilename()
    if not fille:
        return
    name = name_entry.get()
    img = Image.open(fille)
    img.thumbnail((150, 150))
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    full_mesage = f"{name} [PHOTO]{img_str}\n"
    sock.sendall(full_mesage.encode('utf-8'))

    send_photos(img, "Я:")


def send_photos(pl, info):
    if not hasattr(win, "chat_images"):
        win.chat_images = []

    lbl_info = CTkLabel(textbox, text=info, font=("Segoe UI Emoji", 14), justify="left", anchor="w")
    lbl_info.pack(anchor="w", padx=5, pady=2, fill="x")

    tk_image = ImageTk.PhotoImage(pl)
    win.chat_images.append(tk_image)

    lbl_img = CTkLabel(textbox, text="", image=tk_image)
    lbl_img.pack(anchor="w", padx=5, pady=2)


image_button = CTkButton(text_frame, height=50, width=50, text="📎", command=open_images)
image_button.pack(padx=10, pady=10, side="right")


def recive():
    buffer = ""
    while True:
        data = sock.recv(65536)
        if not data:
            break
        buffer += data.decode('utf-8', errors='ignore')

        while "\n" in buffer:
            line, buffer = buffer.split("\n", 1)
            if not line.strip():
                continue

            if "[PHOTO]" in line:
                parts = line.split("[PHOTO]")
                info = parts[0].strip() + ":"
                try:
                    img_data = base64.b64decode(parts[1].strip())
                    img = Image.open(io.BytesIO(img_data))
                    img.thumbnail((150, 150))
                    win.after(0, lambda p=img, i=info: send_photos(p, i))
                except Exception as e:
                    print("Помилка декодування фото:", e)
            else:
                win.after(0, lambda l=line: (
                    CTkLabel(textbox, text=l, font=("Segoe UI Emoji", 14), justify="left", anchor="w").pack(
                        anchor="w", padx=5, pady=2, fill="x")
                ))


threading.Thread(target=recive, daemon=True).start()

win.mainloop()

