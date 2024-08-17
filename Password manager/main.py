from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def gen_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    code_letter = [choice(letters) for _ in range(randint(8, 10))]
    code_number = [choice(numbers) for _ in range(randint(2, 4))]
    code_symbol = [choice(symbols) for _ in range(randint(2, 4))]

    password_list = code_letter + code_number + code_symbol

    shuffle(password_list)

    password = "".join(password_list)

    password_input.insert(0, password)
    pyperclip.copy(password)
# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_password():
    web_input = website_input.get()
    mail_input = email_input.get()
    pass_input = password_input.get()
    new_data = {
        web_input: {
            "Email/Username": mail_input,
            "Password": pass_input,
        }
    }

    if len(web_input) == 0 or len(pass_input) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any area empty.")
    else:

        this_is_ok = messagebox.askokcancel(title=web_input, message=f"These are the details entered: "
                                                                     f"\nEmail: {mail_input}"
                                                        f"\nPassword: {pass_input} \nIs it ok to save?")
        if this_is_ok:
            try:
                with open("your_pass.json", mode='r') as file:
                    # Reading the old data
                    data = json.load(file)
            except FileNotFoundError:
                with open("your_pass.json", "w") as file:
                    # Saving the updated data
                    json.dump(new_data, file, indent=4)
            else:
                # Updating the old data with new data
                data.update(new_data)
                with open("your_pass.json", "w") as file:
                    # Saving the updated data
                    json.dump(data, file, indent=4)
            finally:
                website_input.delete(0, END)
                password_input.delete(0, END)

# ------------------------ DATA SEARCHING MECHANISM -------------------- #


def data_search():
    search_input = website_input.get()
    try:
        with open("your_pass.json") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found")
    else:
        if search_input in data:
            email = data[search_input]['Email/Username']
            password = data[search_input]['Password']
            messagebox.showinfo(title=search_input, message=f"Email: {email}\nPassword: {password}")
            pyperclip.copy(password)
        else:
            messagebox.showinfo(title="Error", message=f"No details for {search_input} exists.")

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

canvas = Canvas(height=200, width=200)
logo = PhotoImage(file="bisonpng01.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(column=2, row=0)

website_label = Label(text='Website:')
website_label.grid(column=1, row=1)

website_input = Entry(width=34)
website_input.grid(column=2, row=1)


email_label = Label(text='E-mail/Username:')
email_label.grid(column=1, row=2)


email_input = Entry(width=45)
email_input.grid(column=2, row=2, columnspan=2)
email_input.insert(0, "wuislord@gmail.com")


password_label = Label(text="Password:")
password_label.grid(column=1, row=3)

password_input = Entry(width=34)
password_input.grid(column=2, row=3)

generate_button = Button(text="Generate", width=8, height=1, command=gen_password)
generate_button.grid(column=3, row=3)


add_button = Button(text="Add", width=38, command=save_password)
add_button.grid(row=4, column=2, columnspan=2)

search_button = Button(text="search", width=8, command=data_search)
search_button.grid(row=1, column=3)


window.mainloop()