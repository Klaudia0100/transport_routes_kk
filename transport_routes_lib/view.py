from tkinter import *
import tkinter.ttk as ttk
import tkintermapview

from model import Company, companies, Employee, employees, get_coordinates

# MAP MARKER
def create_company_marker(company):
    company.marker = map_widget.set_marker(company.coordinates[0], company.coordinates[1], text=company.name)

def create_employee_marker(employee):
    employee.marker = map_widget_employee.set_marker(employee.coordinates[0], employee.coordinates[1], text=f"{employee.name} {employee.surname}")

# SHOW OBJECT ON LIST
def show_companies() -> None:
    listbox_list_object.delete(0, END)

    for idx, company in enumerate(companies):
        listbox_list_object.insert(idx, company.name)

def show_employees() -> None:
    listbox_list_object_employee.delete(0, END)

    for idx, employee in enumerate(employees):
        listbox_list_object_employee.insert(idx, employee.name)

# ADD OBJECT ON LIST
def add_company():
    name = entry_name.get()
    city = entry_city.get()
    street = entry_street.get()

    new_company = Company(name, city, street)
    companies.append(new_company)

    create_company_marker(new_company)
    map_widget.set_position(new_company.coordinates[0], new_company.coordinates[1])

    entry_name.delete(0, END)
    entry_city.delete(0, END)
    entry_street.delete(0, END)

    entry_name.focus()
    show_companies()

def add_employee():
    name = entry_name_employee.get()
    surname = entry_surname_employee.get()
    city = entry_city_employee.get()
    street = entry_street_employee.get()
    company = combobox_company_employee.get()

    selected_company = combobox_company_employee.get()
    if not selected_company:
        print("Błąd: Nie wybrano firmy!")
        return

    new_employee = Employee(name, surname, city, street, company)
    employees.append(new_employee)

    create_employee_marker(new_employee)
    map_widget_employee.set_position(new_employee.coordinates[0], new_employee.coordinates[1])

    entry_name_employee.delete(0, END)
    entry_surname_employee.delete(0, END)
    entry_city_employee.delete(0, END)
    entry_street_employee.delete(0, END)

    combobox_company_employee.set('')
    entry_name_employee.focus()
    show_employees()

def update_company_dropdown():
    company_names = [c.name for c in companies]
    combobox_company_employee['values'] = company_names

#REMOVE OBJECT FROM LIST
def remove_company() -> None:
    i = listbox_list_object.index(ACTIVE)

    company = companies[i]
    if company.marker:
        company.marker.delete()

    companies.pop(i)
    show_companies()

def remove_employee() -> None:
    i = listbox_list_object_employee.index(ACTIVE)

    employee = employees[i]
    if employee.marker:
        employee.marker.delete()

    employees.pop(i)
    show_employees()


#SHOW OBJECT DETAILS
def show_company_details():
    i = listbox_list_object.index(ACTIVE)
    name = companies[i].name
    city = companies[i].city
    street = companies[i].street

    label_name_details_object_value.config(text = name)
    label_city_details_object_value.config(text = city)
    label_street_details_object_value.config(text = street)
    map_widget.set_position(companies[i].coordinates[0], companies[i].coordinates[1])
    map_widget.set_zoom(12)


def show_employee_details():
    i = listbox_list_object_employee.index(ACTIVE)
    name = employees[i].name
    surname = employees[i].surname
    city = employees[i].city
    street = employees[i].street
    company = employees[i].company

    label_name_details_object_value_employee.config(text=name)
    label_surname_details_object_value_employee.config(text=surname)
    label_city_details_object_value_employee.config(text=city)
    label_street_details_object_value_employee.config(text=street)
    label_company_details_object_value_employee.config(text=company)
    map_widget_employee.set_position(employees[i].coordinates[0], employees[i].coordinates[1])
    map_widget_employee.set_zoom(12)

#EDIT OBJECT DETAILS
def edit_company():
    i = listbox_list_object.index(ACTIVE)
    name = companies[i].name
    city = companies[i].city
    street = companies[i].street

    entry_name.insert(0, name)
    entry_city.insert(0, city)
    entry_street.insert(0, street)

    button_add_object.config(text = "Zapisz zmiany", command = lambda: update_company(i))

#UPDATE OBJECT DETAILS
def update_company(i):
    companies[i].name = entry_name.get()
    companies[i].city = entry_city.get()
    companies[i].street = entry_street.get()

    address = f"{companies[i].city}, {companies[i].street}"
    companies[i].coordinates = get_coordinates(address)

    if companies[i].marker:
        companies[i].marker.set_position(companies[i].coordinates[0], companies[i].coordinates[1])
        companies[i].marker.set_text(companies[i].name)

    button_add_object.config(text = "Dodaj firmę", command = add_company)
    entry_name.delete(0, END)
    entry_city.delete(0, END)
    entry_street.delete(0, END)

    entry_name.focus()
    show_companies()

# APPLICATION WINDOW
root = Tk()
root.title("Aplikacja Zarządzania Firmami i Trasami")
root.geometry("1024x760")

# SWITCH
selected_view = StringVar()

def switch_view(event=None):
    view = selected_view.get()
    if view == "Firma":
        frame_company.grid(row=1, column=0, columnspan=2)
        frame_employee.grid_forget()
    elif view == "Pracownicy":
        frame_employee.grid(row=1, column=0, columnspan=2)
        frame_company.grid_forget()
        update_company_dropdown()

combobox_view = ttk.Combobox(root, textvariable=selected_view, values=["Firma", "Pracownicy"], state="readonly")
combobox_view.set("Firma")
combobox_view.grid(row=0, column=0, sticky=W, padx=10, pady=10)
combobox_view.bind("<<ComboboxSelected>>", switch_view)


# FRAME COMPANY
frame_company = Frame(root)
frame_company.grid(row=1, column=0, columnspan=2)

frame_list_object = Frame(frame_company)
frame_form = Frame(frame_company)
frame_details_object = Frame(frame_company)
frame_map = Frame(frame_company)

frame_list_object.grid(row=0, column=0, padx=50)
frame_form.grid(row=0, column=1)
frame_details_object.grid(row=1, column=0, columnspan=2, padx=50, pady=20)
frame_map.grid(row=2, column=0, columnspan=2)


# RAMKA LISTA OBIEKTÓW COMPANY
label_list_object = Label(frame_list_object, text="Lista firm: ")
listbox_list_object = Listbox(frame_list_object)

button_show_object_details = Button(frame_list_object, text="Pokaż szczegóły", command = show_company_details)
button_delete_object = Button(frame_list_object, text="Usuń", command = remove_company)
button_edit_object = Button(frame_list_object, text="Edytuj", command = edit_company)

label_list_object.grid(row=0, column=0)
listbox_list_object.grid(row=1, column=0)
button_show_object_details.grid(row=2, column=0)
button_delete_object.grid(row=2, column=1)
button_edit_object.grid(row=2, column=2)


# RAMKA FORMULARZ COMPANY
label_form = Label(frame_form, text="Formularz: ")
label_name = Label(frame_form, text="Nazwa: ")
label_city = Label(frame_form, text="Miasto: ")
label_street = Label(frame_form, text="Ulica: ")

label_form.grid(row=0, column=0, columnspan=2)
label_name.grid(row=1, column=0, sticky=W)
label_city.grid(row=2, column=0, sticky=W)
label_street.grid(row=3, column=0, sticky=W)

entry_name = Entry(frame_form)
entry_city = Entry(frame_form)
entry_street = Entry(frame_form)

entry_name.grid(row=1, column=1)
entry_city.grid(row=2, column=1)
entry_street.grid(row=3, column=1)

button_add_object = Button(frame_form, text="Dodaj firmę", command=add_company)
button_add_object.grid(row=5, column=0, columnspan=2)


# SZCZEGÓŁY OBIEKTU COMPANY
label_details_object_title = Label(frame_details_object, text="Szczegóły firmy")

label_name_details_object = Label(frame_details_object, text="Nazwa:")
label_name_details_object_value = Label(frame_details_object, text="...")

label_city_details_object = Label(frame_details_object, text="Miasto:")
label_city_details_object_value = Label(frame_details_object, text="...")

label_street_details_object = Label(frame_details_object, text="Ulica:")
label_street_details_object_value = Label(frame_details_object, text="...")

label_details_object_title.grid(row=0, column=0, columnspan=2)

label_name_details_object.grid(row=1, column=0, sticky=W)
label_name_details_object_value.grid(row=1, column=1, sticky=W)

label_city_details_object.grid(row=1, column=2, sticky=W)
label_city_details_object_value.grid(row=1, column=3, sticky=W)

label_street_details_object.grid(row=1, column=4, sticky=W)
label_street_details_object_value.grid(row=1, column=5, sticky=W)

# RAMKA MAPA COMPANY
map_widget = tkintermapview.TkinterMapView(frame_map, width=1024, height=600, corner_radius=4)
map_widget.set_zoom(6)
map_widget.set_position(52.2, 21.0)

map_widget.grid(row=0, column=0)


# FRAME EMPLOYEE
frame_employee = Frame(root)

frame_list_object_employee = Frame(frame_employee)
frame_form_employee = Frame(frame_employee)
frame_details_object_employee = Frame(frame_employee)
frame_map_employee = Frame(frame_employee)
frame_list_object_employee.grid(row=0, column=0, padx=50)
frame_form_employee.grid(row=0, column=1)
frame_details_object_employee.grid(row=1, column=0, columnspan=2, padx=50, pady=20)
frame_map_employee.grid(row=2, column=0, columnspan=2)


# RAMKA LISTA OBIEKTÓW EMPLOYEE
label_list_object_employee = Label(frame_list_object_employee, text="Lista pracowników: ")
listbox_list_object_employee = Listbox(frame_list_object_employee)
button_show_object_details_employee = Button(frame_list_object_employee, text="Pokaż szczegóły", command = show_employee_details)
button_delete_object_employee = Button(frame_list_object_employee, text="Usuń", command = remove_employee)
button_edit_object_employee = Button(frame_list_object_employee, text="Edytuj")
label_list_object_employee.grid(row=0, column=0)
listbox_list_object_employee.grid(row=1, column=0)
button_show_object_details_employee.grid(row=2, column=0)
button_delete_object_employee.grid(row=2, column=1)
button_edit_object_employee.grid(row=2, column=2)


# RAMKA FORMULARZ EMPLOYEE
label_form_employee = Label(frame_form_employee, text="Formularz: ")
label_name_employee = Label(frame_form_employee, text="Imię: ")
label_surname_employee = Label(frame_form_employee, text="Nazwisko: ")
label_company_employee = Label(frame_form_employee, text="Firma: ")
label_city_employee = Label(frame_form_employee, text="Miasto: ")
label_street_employee = Label(frame_form_employee, text="Ulica: ")

label_form_employee.grid(row=0, column=0, columnspan=2)
label_name_employee.grid(row=1, column=0, sticky=W)
label_surname_employee.grid(row=2, column=0, sticky=W)
label_company_employee.grid(row=5, column=0, sticky=W)
label_city_employee.grid(row=3, column=0, sticky=W)
label_street_employee.grid(row=4, column=0, sticky=W)

entry_name_employee = Entry(frame_form_employee)
entry_surname_employee = Entry(frame_form_employee)
combobox_company_employee = ttk.Combobox(frame_form_employee, state = "readonly")
entry_city_employee = Entry(frame_form_employee)
entry_street_employee = Entry(frame_form_employee)

entry_name_employee.grid(row=1, column=1)
entry_surname_employee.grid(row=2, column=1)
combobox_company_employee.grid(row=5, column=1)
entry_city_employee.grid(row=3, column=1)
entry_street_employee.grid(row=4, column=1)

button_add_object_employee = Button(frame_form_employee, text = "Dodaj pracownika", command = add_employee)
button_add_object_employee.grid(row=6, column=0, columnspan=2)


# SZCZEGÓŁY OBIEKTU EMPLOYEE
label_details_object_title_employee = Label(frame_details_object_employee, text="Szczegóły pracownika")
label_name_details_object_employee = Label(frame_details_object_employee, text="Imię:")
label_name_details_object_value_employee = Label(frame_details_object_employee, text="...")
label_surname_details_object_employee = Label(frame_details_object_employee, text="Nazwisko:")
label_surname_details_object_value_employee = Label(frame_details_object_employee, text="...")
label_city_details_object_employee = Label(frame_details_object_employee, text="Miasto:")
label_city_details_object_value_employee = Label(frame_details_object_employee, text="...")
label_street_details_object_employee = Label(frame_details_object_employee, text="Ulica:")
label_street_details_object_value_employee = Label(frame_details_object_employee, text="...")
label_company_details_object_employee = Label(frame_details_object_employee, text="Firma:")
label_company_details_object_value_employee = Label(frame_details_object_employee, text="...")


label_details_object_title_employee.grid(row=0, column=0, columnspan=2)

label_name_details_object_employee.grid(row=1, column=0, sticky=W)
label_name_details_object_value_employee.grid(row=1, column=1, sticky=W)

label_surname_details_object_employee.grid(row=1, column=2, sticky=W)
label_surname_details_object_value_employee.grid(row=1, column=3, sticky=W)

label_city_details_object_employee.grid(row=1, column=4, sticky=W)
label_city_details_object_value_employee.grid(row=1, column=5, sticky=W)

label_street_details_object_employee.grid(row=1, column=6, sticky=W)
label_street_details_object_value_employee.grid(row=1, column=7, sticky=W)

label_company_details_object_employee.grid(row=1, column=8, sticky=W)
label_company_details_object_value_employee.grid(row=1, column=9, sticky=W)


# RAMKA MAPA EMPLOYEE
map_widget_employee = tkintermapview.TkinterMapView(frame_map_employee, width=1024, height=600, corner_radius=4)
map_widget_employee.set_zoom(6)
map_widget_employee.set_position(52.2, 21.0)
map_widget_employee.grid(row=0, column=0)

# APP START
frame_company.grid(row=1, column=0, columnspan=2)
frame_employee.grid_forget()

switch_view()
root.mainloop()