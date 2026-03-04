import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import urllib.parse
import pyperclip  # для работы с буфером обмена


class URLEncoderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("URL Encoder")
        self.root.geometry("700x600")
        self.root.resizable(True, True)

        # Настройка стилей
        self.setup_styles()

        # Создание виджетов
        self.create_widgets()

    def setup_styles(self):
        """Настройка стилей для виджетов"""
        self.bg_color = "#f0f0f0"
        self.text_bg = "#ffffff"
        self.button_color = "#e1e1e1"
        self.highlight_color = "#0078d4"

        self.root.configure(bg=self.bg_color)

    def create_widgets(self):
        """Создание элементов интерфейса"""

        # Верхняя панель с инструкцией
        instruction_frame = tk.Frame(self.root, bg=self.bg_color)
        instruction_frame.pack(pady=10, fill=tk.X)

        instruction = tk.Label(
            instruction_frame,
            text="Введите текст для кодирования в URL формат (UTF-8):",
            bg=self.bg_color,
            font=("Arial", 10)
        )
        instruction.pack()

        # Поле для ввода текста
        input_frame = tk.Frame(self.root, bg=self.bg_color)
        input_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        input_label = tk.Label(
            input_frame,
            text="Исходный текст:",
            bg=self.bg_color,
            anchor="w",
            font=("Arial", 9, "bold")
        )
        input_label.pack(anchor="w")

        self.input_text = scrolledtext.ScrolledText(
            input_frame,
            height=8,
            wrap=tk.WORD,
            font=("Consolas", 10),
            bg=self.text_bg,
            relief=tk.SUNKEN,
            borderwidth=1
        )
        self.input_text.pack(fill=tk.BOTH, expand=True, pady=(0, 5))

        # Кнопки управления
        button_frame = tk.Frame(self.root, bg=self.bg_color)
        button_frame.pack(pady=10)

        self.encode_button = tk.Button(
            button_frame,
            text="Кодировать текст",
            command=self.encode_text,
            bg=self.button_color,
            font=("Arial", 10),
            padx=20,
            pady=5,
            cursor="hand2",
            relief=tk.RAISED,
            borderwidth=1
        )
        self.encode_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = tk.Button(
            button_frame,
            text="Очистить все",
            command=self.clear_all,
            bg=self.button_color,
            font=("Arial", 10),
            padx=20,
            pady=5,
            cursor="hand2",
            relief=tk.RAISED,
            borderwidth=1
        )
        self.clear_button.pack(side=tk.LEFT, padx=5)

        # Поле для вывода результата
        output_frame = tk.Frame(self.root, bg=self.bg_color)
        output_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        output_label_frame = tk.Frame(output_frame, bg=self.bg_color)
        output_label_frame.pack(fill=tk.X)

        output_label = tk.Label(
            output_label_frame,
            text="Закодированный результат:",
            bg=self.bg_color,
            anchor="w",
            font=("Arial", 9, "bold")
        )
        output_label.pack(side=tk.LEFT)

        self.copy_button = tk.Button(
            output_label_frame,
            text="Копировать",
            command=self.copy_to_clipboard,
            bg=self.button_color,
            font=("Arial", 8),
            padx=10,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.copy_button.pack(side=tk.RIGHT)

        self.output_text = scrolledtext.ScrolledText(
            output_frame,
            height=8,
            wrap=tk.WORD,
            font=("Consolas", 10),
            bg="#fafafa",
            relief=tk.SUNKEN,
            borderwidth=1
        )
        self.output_text.pack(fill=tk.BOTH, expand=True, pady=(0, 5))

        # Статус бар
        self.status_bar = tk.Label(
            self.root,
            text="Готов к работе",
            bg="#dddddd",
            anchor="w",
            padx=10,
            font=("Arial", 8)
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Привязка горячих клавиш
        self.root.bind('<Control-Return>', lambda e: self.encode_text())
        self.root.bind('<Control-q>', lambda e: self.root.quit())

    def encode_text(self):
        """Кодирование текста"""
        # Получаем текст из поля ввода
        input_text = self.input_text.get("1.0", tk.END).rstrip('\n')

        if not input_text:
            messagebox.showwarning("Предупреждение", "Введите текст для кодирования!")
            return

        try:
            # Кодируем текст
            encoded = urllib.parse.quote(input_text, safe='', encoding='utf-8')

            # Очищаем поле вывода и вставляем результат
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", encoded)

            # Активируем кнопку копирования
            self.copy_button.config(state=tk.NORMAL)

            # Обновляем статус
            original_len = len(input_text)
            encoded_len = len(encoded)
            self.status_bar.config(
                text=f"✓ Текст закодирован. Исходный размер: {original_len} симв., "
                     f"закодированный: {encoded_len} симв."
            )

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при кодировании:\n{str(e)}")
            self.status_bar.config(text="✗ Ошибка кодирования")

    def clear_all(self):
        """Очистка всех полей"""
        self.input_text.delete("1.0", tk.END)
        self.output_text.delete("1.0", tk.END)
        self.copy_button.config(state=tk.DISABLED)
        self.status_bar.config(text="Поля очищены")

    def copy_to_clipboard(self):
        """Копирование результата в буфер обмена"""
        result = self.output_text.get("1.0", tk.END).rstrip('\n')

        if result:
            try:
                pyperclip.copy(result)
                self.status_bar.config(text="✓ Результат скопирован в буфер обмена")

                # Визуальный feedback
                self.copy_button.config(bg="#90EE90")
                self.root.after(200, lambda: self.copy_button.config(bg=self.button_color))

            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось скопировать в буфер обмена:\n{str(e)}")
        else:
            messagebox.showwarning("Предупреждение", "Нет данных для копирования!")


def main():
    root = tk.Tk()
    app = URLEncoderApp(root)

    # Центрирование окна на экране
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

    root.mainloop()


if __name__ == "__main__":
    main()