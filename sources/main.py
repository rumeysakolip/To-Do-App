import tkinter as tk
import json
import os

root = tk.Tk()
root.title("Görev Listesi")
root.geometry("600x700")
root.configure(bg="#002b2e")

# Görev listesi ve silme durumu
tasks = []
selected_for_delete = set()
delete_mode = False

# Renk ve stil
COLOR_BG = "#002b2e"
COLOR_BOX = "#114344"
COLOR_SELECTED = "#226666"
COLOR_TEXT = "white"
FONT = ("Consolas", 14)

# Kaydet
def save_tasks():
    data = [{"text": t[1], "completed": t[0].get()} for t in tasks]
    with open("todo_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Görev oluştur
def create_task(text, completed=False):
    var = tk.BooleanVar(value=completed)
    frame = tk.Frame(task_frame, bg=COLOR_BOX, bd=2, relief="solid")
    frame.pack(fill="x", pady=4, padx=10)

    cb = tk.Checkbutton(
        frame, text=text, variable=var,
        font=FONT, bg=COLOR_BOX, fg=COLOR_TEXT,
        selectcolor=COLOR_BOX, activebackground=COLOR_BOX,
        anchor="w", width=40, command=save_tasks
    )
    cb.pack(side="left", padx=10, pady=5)

    def toggle_selection(event):
        if delete_mode:
            if frame in selected_for_delete:
                frame.config(bg=COLOR_BOX)
                selected_for_delete.remove(frame)
            else:
                frame.config(bg=COLOR_SELECTED)
                selected_for_delete.add(frame)

    frame.bind("<Button-1>", toggle_selection)
    cb.bind("<Button-1>", lambda e: e)  # checkbox'a tıklama davranışı kalsın

    tasks.append((var, text, frame, cb))
    save_tasks()
    filter_tasks()

# Görev ekle
def add_task():
    text = entry_task.get().strip()
    if text:
        create_task(text)
        entry_task.delete(0, tk.END)

# Seçimleri temizle
def clear_selections():
    for t in tasks:
        t[2].config(bg=COLOR_BOX)
    selected_for_delete.clear()

# Silme modunu iptal et
def cancel_delete_mode():
    global delete_mode
    delete_mode = False
    delete_button.config(text="Sil")
    cancel_button.pack_forget()
    clear_button.pack_forget()
    clear_selections()

# Seçileni sil
def confirm_delete():
    global delete_mode
    global tasks
    new_tasks = []
    for t in tasks:
        if t[2] not in selected_for_delete:
            new_tasks.append(t)
        else:
            t[2].destroy()
    tasks = new_tasks
    selected_for_delete.clear()
    delete_mode = False
    delete_button.config(text="Sil")
    cancel_button.pack_forget()
    clear_button.pack_forget()
    save_tasks()

# Sil tuşu tıklanınca
def on_delete_click():
    global delete_mode
    if delete_mode:
        confirm_delete()
    else:
        delete_mode = True
        delete_button.config(text="Seçileni Sil")
        cancel_button.pack(pady=5)
        clear_button.pack(pady=5)

# Arama
def filter_tasks(*args):
    q = search_entry.get().lower()
    for _, text, frame, _ in tasks:
        if q in text.lower():
            frame.pack(fill="x", pady=4, padx=10)
        else:
            frame.pack_forget()

# Yükleme
def load_tasks():
    if os.path.exists("todo_data.json"):
        with open("todo_data.json", "r", encoding="utf-8") as f:
            try:
                for item in json.load(f):
                    create_task(item["text"], item.get("completed", False))
            except:
                pass

# Üst giriş alanı
top = tk.Frame(root, bg=COLOR_BG)
top.pack(pady=10)

tk.Label(top, text="Görev :", font=FONT, fg=COLOR_TEXT, bg=COLOR_BG).grid(row=0, column=0, padx=5)
entry_task = tk.Entry(top, font=FONT, width=30, bg=COLOR_BOX, fg=COLOR_TEXT, insertbackground="white")
entry_task.grid(row=0, column=1, padx=5)
tk.Button(top, text="Ekle", font=FONT, command=add_task, bg=COLOR_BOX, fg=COLOR_TEXT).grid(row=0, column=2, padx=5)

# Arama + sil alanı
search = tk.Frame(root, bg=COLOR_BG)
search.pack()

tk.Label(search, text="🔍", font=("Arial", 14), bg=COLOR_BG, fg=COLOR_TEXT).grid(row=0, column=0, padx=5)

search_entry = tk.Entry(search, font=FONT, width=35, bg=COLOR_BOX, fg=COLOR_TEXT, insertbackground="white")
search_entry.grid(row=0, column=1, padx=5)
search_entry.bind("<KeyRelease>", filter_tasks)

delete_button = tk.Button(search, text="Sil", font=FONT, command=on_delete_click, bg=COLOR_BOX, fg=COLOR_TEXT)
delete_button.grid(row=0, column=2, padx=5)

# Bu 2 buton sadece silme modunda görünür
cancel_button = tk.Button(search, text="İptal", font=FONT, command=cancel_delete_mode, bg="darkred", fg="white")
clear_button = tk.Button(search, text="Seçimleri Temizle", font=FONT, command=clear_selections, bg="#004444", fg="white")

# Görevler listesi
task_frame = tk.Frame(root, bg=COLOR_BG)
task_frame.pack(pady=10, fill="both", expand=True)

# Başlat
load_tasks()
root.mainloop()