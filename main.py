from tkinter import *
from transport_routes_lib.view import start_app

def check_login(root_login, entry_user, entry_pass, login_error):
    if entry_user.get() == "admin" and entry_pass.get() == "1234":
        root_login.destroy()
        start_app()
    else:
        login_error.config(text="Błędne dane!", fg="red")

def main():
    root_login = Tk()
    root_login.title("Logowanie")
    root_login.geometry("300x150")

    Label(root_login, text="Login:").pack()
    entry_user = Entry(root_login)
    entry_user.pack()

    Label(root_login, text="Hasło:").pack()
    entry_pass = Entry(root_login, show="*")
    entry_pass.pack()

    login_error = Label(root_login, text="", fg="red")
    login_error.pack(pady=5)

    Button(root_login, text="Zaloguj",
           command=lambda: check_login(root_login, entry_user, entry_pass, login_error)).pack(pady=5)

    root_login.mainloop()

if __name__ == "__main__":
    main()