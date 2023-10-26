import tkinter as tk
from tkinter import messagebox, scrolledtext
import db_helper 

class MainApp(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Менеджер заметок")
        self.geometry("400x300")

        self.add_note_button = tk.Button(self, text="Добавить заметку", command=self.add_note)
        self.add_note_button.pack(pady=20)

        self.view_notes_button = tk.Button(self, text="Просмотреть заметки", command=self.view_notes)
        self.view_notes_button.pack(pady=20)

        self.search_notes_button = tk.Button(self, text="Поиск заметки", command=self.search_notes)
        self.search_notes_button.pack(pady=20)

    def add_note(self):
        AddNoteWindow(self)
        self.withdraw()

    def view_notes(self):
        ViewNotesWindow(self)
        self.withdraw()

    def search_notes(self):
        SearchNotesWindow(self)
        self.withdraw()

    def on_closing(self, child_window):
        child_window.destroy()
        self.deiconify()

class BaseNoteWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def back(self):
        self.parent.on_closing(self)

class AddNoteWindow(BaseNoteWindow):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Добавить заметку")
        self.geometry("300x250")

        self.title_label = tk.Label(self, text="Заголовок")
        self.title_label.pack(pady=5)
        self.title_entry = tk.Entry(self)
        self.title_entry.pack(pady=5)

        self.content_label = tk.Label(self, text="Содержание")
        self.content_label.pack(pady=5)
        self.content_text = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=30, height=10)
        self.content_text.pack(pady=5)

        self.add_button = tk.Button(self, text="Добавить", command=self.add_note)
        self.add_button.pack(pady=10)
        self.back_button = tk.Button(self, text="Назад", command=self.back)
        self.back_button.pack(pady=5)

    def add_note(self):
        title = self.title_entry.get()
        content = self.content_text.get(1.0, tk.END)

        if not title.strip() or not content.strip():
            messagebox.showwarning("Ошибка", "Заголовок и содержание не могут быть пустыми!")
            return

        db_helper.add_note(title, content)
        self.back()

class ViewNotesWindow(BaseNoteWindow):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Просмотр заметок")
        self.geometry("300x300")

        self.notes_listbox = tk.Listbox(self)
        self.notes_listbox.pack(pady=20, fill=tk.BOTH, expand=True)

        for note in db_helper.get_all_notes():
            self.notes_listbox.insert(tk.END, note[0])

        self.view_button = tk.Button(self, text="Просмотреть заметку", command=self.view_selected)
        self.view_button.pack(pady=10)
        self.delete_button = tk.Button(self, text="Удалить заметку", command=self.delete_selected)
        self.delete_button.pack(pady=10)
        self.back_button = tk.Button(self, text="Назад", command=self.back)
        self.back_button.pack(pady=5)

    def view_selected(self):
        selected_title = self.get_selected_note()
        if selected_title:
            content = db_helper.get_note_content(selected_title)  
            messagebox.showinfo(selected_title, content[0])

    def delete_selected(self):
        selected_title = self.get_selected_note()
        if selected_title:
            db_helper.delete_note(selected_title) 
            self.notes_listbox.delete(self.notes_listbox.curselection())

    def get_selected_note(self):
        try:
            return self.notes_listbox.get(self.notes_listbox.curselection())
        except tk.TclError:
            messagebox.showwarning("Ошибка", "Выберите заметку для выполнения этого действия!")
            return None

class SearchNotesWindow(BaseNoteWindow):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Поиск заметок")
        self.geometry("300x300")

        self.keyword_label = tk.Label(self, text="Ключевое слово для поиска")
        self.keyword_label.pack(pady=10)
        self.keyword_entry = tk.Entry(self)
        self.keyword_entry.pack(pady=10)

        self.search_button = tk.Button(self, text="Поиск", command=self.search_notes)
        self.search_button.pack(pady=10)
        self.notes_listbox = tk.Listbox(self)
        self.notes_listbox.pack(pady=20, fill=tk.BOTH, expand=True)
        self.back_button = tk.Button(self, text="Назад", command=self.back)
        self.back_button.pack(pady=5)

    def search_notes(self):
        keyword = self.keyword_entry.get()
        self.notes_listbox.delete(0, tk.END)

        for note in db_helper.search_notes(keyword):
            self.notes_listbox.insert(tk.END, note[0])

