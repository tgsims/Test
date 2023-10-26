from note_manager import MainApp
import db_helper

if __name__ == "__main__":
    db_helper.init_db()  # Инициализация базы данных перед запуском приложения
    app = MainApp()
    app.mainloop()
