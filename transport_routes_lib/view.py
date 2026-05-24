from tkinter import *
import tkintermapview

from model import Company, companies, get_coordinates

def create_company_marker(company):
    company.marker = map_widget.set_marker(
        company.coordinates[0],
        company.coordinates[1],
        text=company.name
    )

def show_companies() -> None:
    listbox_list_object.delete(0, END)

    for idx, company in enumerate(companies):
        listbox_list_object.insert(idx, company.name)


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


def remove_company() -> None:
    i = listbox_list_object.index(ACTIVE)

    company = companies[i]
    if company.marker:
        company.marker.delete()

    companies.pop(i)
    show_companies()

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

def edit_company():
    i = listbox_list_object.index(ACTIVE)
    name = companies[i].name
    city = companies[i].city
    street = companies[i].street

    entry_name.insert(0, name)
    entry_city.insert(0, city)
    entry_street.insert(0, street)

    button_add_object.config(text = "Zapisz zmiany", command = lambda: update_company(i))


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

root = Tk()
root.title("Aplikacja Zarządzania Firmami i Trasami")
root.geometry("1024x760")

# FRAME
frame_list_object = Frame(root)
frame_form = Frame(root)
frame_details_object = Frame(root)
frame_map = Frame(root)

frame_list_object.grid(row=0, column=0, padx=50)
frame_form.grid(row=0, column=1)
frame_details_object.grid(row=1, column=0, columnspan=2, padx=50, pady=20)
frame_map.grid(row=2, column=0, columnspan=2)


# RAMKA LISTA OBIEKTÓW
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


# RAMKA FORMULARZ
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


# SZCZEGÓŁY OBIEKTU
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

# RAMKA MAPA
map_widget = tkintermapview.TkinterMapView(frame_map, width=1024, height=600, corner_radius=4)
map_widget.set_zoom(6)
map_widget.set_position(52.2, 21.0)

map_widget.grid(row=0, column=0)


root.mainloop()