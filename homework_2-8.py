import sqlite3

class BankSystem:
    def __init__(self):
        self.conn = sqlite3.connect("bank_system.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS accounts(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            age INTEGER,
            address TEXT,
            email TEXT,
            balance REAL DEFAULT 0.0
        )""")
        self.conn.commit()

    def open_account(self):
        first_name = input("Введите имя: ")
        last_name = input("Введите фамилию: ")
        age = int(input("Введите возраст: "))
        address = input("Введите адрес: ")
        email = input("Введите email: ")

        self.cursor.execute("""INSERT INTO accounts 
            (first_name, last_name, age, address, email) 
            VALUES (?, ?, ?, ?, ?)""", (first_name, last_name, age, address, email))
        self.conn.commit()
        print("Счет успешно открыт.")

    def deposit(self, account_id, amount):
        self.cursor.execute("SELECT balance FROM accounts WHERE id=?", (account_id,))
        current_balance = self.cursor.fetchone()[0]
        new_balance = current_balance + amount
        self.cursor.execute("UPDATE accounts SET balance=? WHERE id=?", (new_balance, account_id))
        self.conn.commit()
        print("Средства успешно зачислены.")

    def withdraw(self, account_id, amount):
        self.cursor.execute("SELECT balance FROM accounts WHERE id=?", (account_id,))
        current_balance = self.cursor.fetchone()[0]
        if amount > current_balance:
            print("Ошибка: недостаточно средств на счете.")
        else:
            new_balance = current_balance - amount
            self.cursor.execute("UPDATE accounts SET balance=? WHERE id=?", (new_balance, account_id))
            self.conn.commit()
            print("Средства успешно сняты.")

    def check_balance(self, account_id):
        self.cursor.execute("SELECT balance FROM accounts WHERE id=?", (account_id,))
        balance = self.cursor.fetchone()[0]
        print(f"Текущий баланс: {balance}")

    def close_account(self, account_id):
        self.cursor.execute("DELETE FROM accounts WHERE id=?", (account_id,))
        self.conn.commit()
        print("Счет успешно закрыт.")

    def close_connection(self):
        self.conn.close()

    def main(self):
        while True:
            print("\nВыберите действие:")
            print("1. Открыть счет")
            print("2. Пополнить счет")
            print("3. Снять средства")
            print("4. Проверить баланс")
            print("5. Закрыть счет")
            print("6. Выйти из программы")
            choice = input("Введите номер действия: ")

            if choice == "1":
                self.open_account()
            elif choice == "2":
                account_id = int(input("Введите номер счета: "))
                amount = float(input("Введите сумму для пополнения: "))
                self.deposit(account_id, amount)
            elif choice == "3":
                account_id = int(input("Введите номер счета: "))
                amount = float(input("Введите сумму для снятия: "))
                self.withdraw(account_id, amount)
            elif choice == "4":
                account_id = int(input("Введите номер счета: "))
                self.check_balance(account_id)
            elif choice == "5":
                account_id = int(input("Введите номер счета для закрытия: "))
                self.close_account(account_id)
            elif choice == "6":
                self.close_connection()
                break
            else:
                print("Ошибка: неверный выбор.")

bank_system = BankSystem()
bank_system.main()
