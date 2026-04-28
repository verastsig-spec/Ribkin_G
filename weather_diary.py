import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
from datetime import datetime

class WeatherDiaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Diary")
        self.file_path = "weather_data.json"
        self.data = self.load_data()

        # Поля ввода
        tk.Label(root, text="Дата (ДД.ММ.ГГГГ):").grid(row=0, column=0, padx=5, pady=5)
        self.entry_date = tk.Entry(root)
        self.entry_date.insert(0, datetime.now().strftime("%d.%m.%Y"))
        self.entry_date.grid(row=0, column=1)

        tk.Label(root, text="Температура (°C):").grid(row=1, column=0)
        self.entry_temp = tk.Entry(root)
        self.entry_temp.grid(row=1, column=1)

        tk.Label(root, text="Описание:").grid(row=2, column=0)
        self.entry_desc = tk.Entry(root)
        self.entry_desc.grid(row=2, column=1)

        self.var_precip = tk.BooleanVar()
        tk.Checkbutton(root, text="Осадки", variable=self.var_precip).grid(row=3, columnspan=2)

        # Кнопки
        tk.Button(root, text="Добавить запись", command=self.add_entry).grid(row=4, columnspan=2, pady=5)
        
        # Фильтры
        tk.Label(root, text="Фильтр (темп > X):").grid(row=5, column=0)
        self.entry_filter_temp = tk.Entry(root)
        self.entry_filter_temp.grid(row=5, column=1)
        tk.Button(root, text="Применить фильтр", command=self.apply_filter).grid(row=6, columnspan=2)

        # Таблица
        self.tree = ttk.Treeview(root, columns=("Date", "Temp", "Desc", "Precip"), show='headings')
        self.tree.heading("Date", text="Дата")
        self.tree.heading("Temp", text="Темп.")
        self.tree.heading("Desc", text="Описание")
        self.tree.heading("Precip", text="Осадки")
        self.tree.grid(row=7, columnspan=2, padx=10, pady=10)

        self.refresh_table(self.data)

    def validate(self):
        try:
            datetime.strptime(self.entry_date.get(), "%d.%m.%Y")
            float(self.entry_temp.get())
            if not self.entry_desc.get().strip():
                raise ValueError("Описание пустое")
            return True
        except ValueError as e:
            messagebox.showerror("Ошибка ввода", f"Проверьте данные: {e}")
            return False

    def add_entry(self):
        if self.validate():
            new_entry = {
                "date": self.entry_date.get(),
                "temp": float(self.entry_temp.get()),
                "desc": self.entry_desc.get(),
                "precip": "Да" if self.var_precip.get() else "Нет"
            }
            self.data.append(new_entry)
            self.save_data()
            self.refresh_table(self.data)

    def apply_filter(self):
        try:
            limit = float(self.entry_filter_temp.get())
            filtered = [row for row in self.data if row['temp'] > limit]
            self.refresh_table(filtered)
        except ValueError:
            self.refresh_table(self.data)

    def refresh_table(self, display_data):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for row in display_data:
            self.tree.insert("", "end", values=(row['date'], row['temp'], row['desc'], row['precip']))

    def save_data(self):
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def load_data(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherDiaryApp(root)
    root.mainloop()
