from tkinter import *
import csv

# добавить вопрос если запись повторяеся, онлайн база

months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
          'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
lbl2_text = []


def exit(self):
    window.destroy()


window = Tk()
window.title("hh stealer")
window.bind("<Escape>", exit)


def delete_db():
    def delete():
        with open('database.csv', 'w') as file:
            file.close()
        delete_window.destroy()

    delete_window = Toplevel(window)
    delete_text = Label(delete_window, text='Вы уверены, что хотите удалить файл?')
    delete_text.grid(column=0, row=0, columnspan=2, padx=30, pady=5)

    yes = Button(delete_window, text='Да', width=10, command=delete)
    yes.grid(column=0, row=1, pady=15)
    yes.bind("<Return>", delete)

    no = Button(delete_window, text='Нет', width=10, command=delete_window.destroy)
    no.grid(column=1, row=1, pady=15)


def how_to():
    instructions = """
    Как пользоваться программой:

        1. Заполните поле "Дата общения"
        2. Скопируйте и вставьте ссылку на резюме,
           которое необходимо скопировать в поле "Ссылка"
                Удобно сделать это так:
                    - нажимаем в браузере Ctrl+L (выделяется вся строка со ссылкой)
                    - нажимаем Ctrl+C (копируем ссылку)
        3. Скопируйте выбранное резюме в браузере
                Удобно сделать это так:
                    - нажимаем в браузере Ctrl+A (выделяется вся страница)
                    - нажимаем Ctrl+C (копируем страницу)
        4. Нажмите кнопку "Сохранить" или Enter


        Результаты сохранения показываются в нижней части окна
    """
    help_window = Toplevel(window)
    help_text = Label(help_window, text=instructions, justify='left')
    help_text.pack(padx=30, pady=30)


def clean_text(text):
    clean = ""
    for x in text:
        if x.isalnum() or x in "():-@., \n":
            clean += x
    return(clean)


def save(event=None, info=lbl2_text):
    try:
        text = window.clipboard_get()
    except:
        text = ""
    if len(text.splitlines()) < 3 or text.splitlines()[2] != 'Резюме':
        result = 'Ошибка копирования'
    else:
        text = clean_text(text)
        text = parse_resume(text, ent.get(), ent2.get())

        with open('database.csv', 'a+', newline='') as file:
            resume_writer = csv.writer(
                file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            resume_writer.writerow(text)
            file.close()
        result = text[0].split()[0] + ': Успешно сохранено'
    if len(info) >= 3:
        info.pop(0)
    info.append(result)
    info = "\n".join(info[::-1])

    lbl2.configure(text=info)
    ent.delete(0, END)
    ent2.delete(0, END)


def parse_resume(text, date, link):

    # finding name
    start = text.find('Был на сайте')
    if start == -1:
        start = text.find('Была на сайте')
    if start == -1:
        name = None
    else:
        start = text.find('\n', start) + 1
        end = text.find('\n', start)
        name = text[start:end].strip()

    # finding e-mail
    middle = text.find('@')
    if middle == -1:
        mail = None
    else:
        while text[middle] != '\n':
            middle -= 1
        else:
            start = middle + 1
            middle += 1
        while text[middle] != '\n' and text[middle] != ' ':
            middle += 1
        else:
            end = middle + 1
        mail = text[start:end].strip()

    # finding phone (fix end)
    start = text.find('(')
    if start == -1:
        phone = None
    else:
        middle = start
        while text[middle] != '\n' and text[middle] != 'п':
            middle += 1
        else:
            end = middle
        phone = '+7' + text[start:end].strip()

    # finding comment
    start = text.find('Комментарии') + 12
    if start == 11:
        comment = None
    else:
        end = text.find('История', start) - 1
        comment = text[start:end].strip()
        if comment == 'Добавить комментарий':
            comment = None
        else:
            comment = comment.splitlines()
            comment = "\n".join(comment[1:len(comment) - 22])

    # find birth
    start = text.find('родил') + 5
    if start == 'с':
        start += 2
    else:
        start += 3
    end = text.find('\n', start)
    birth = text[start:end].strip()

    # finding trips
    middle = text.find('командировкам')
    if middle == -1:
        trips = None
    else:
        end = text.find('\n', middle)
        while text[middle] != ',':
            middle -= 1
        else:
            start = middle + 2
        trips = text[start:end].strip()

    # finding driving license
    start = text.find('Права категории')
    if start == -1:
        driving_license = None
    else:
        end = text.find('\n', start)
    driving_license = text[start:end].strip()

    # finding education
    middle = text.find('образование\n')
    if middle == -1:
        education = None
    else:
        while text[middle] != '\n':
            middle -= 1
        start = middle + 1
        end = text.find('Знание языков')
        if end == -1:
            end = text.find('Гражданство')
        education = text[start:end].strip()

    # finding experience
    start = text.find('\nОпыт работы') + 1
    end = text.find('Ключевые навыки')
    full_experience = text[start:end].strip().replace(
        '\n\n', '\n').splitlines()[1:]
    experience = []
    for x in full_experience:
        if not x.split()[0].isnumeric() and not x.split()[0] in months:
            experience.append(x)
    experience = "\n".join(experience)

    # finding job_name
    middle = text.find('Резюме обновлено')
    start = text.find('\n', middle) + 1
    if text.find('Сопроводительное письмо', start) != -1:
        search = text[start:].split('\n', 7)
        for i in range(len(search)):
            if " " in search[i]:
                search[i] = search[i].split()[0]
            if search[i] in text[text.find('Резюме, похожие на это'):text.find('Комментарии')]:
                job_name = search[i]
    else:
        end = text.find('\n', start)
        job_name = text[start:end]

    # finding income
    middle = text.find('руб.', 0, len(text) // 2)
    if middle == -1:
        income = None
    else:
        while text[middle] != '\n':
            middle -= 1
        start = middle + 1
        end = text.find('\n', start)
        income = text[start:end]

    text = [name, date, link, job_name, birth, mail, phone, comment, trips,
            driving_license, education, experience, income]

    return(text)


lbl = Label(text='Скопируйте резюме')
lbl.grid(column=1, row=0, pady=15)
try:
    text = window.clipboard_get()
except:
    text = ""
if len(text.splitlines()) < 3 or text.splitlines()[2] != 'Резюме':
    lbl.configure(text='Скопируйте резюме', font='Helvetica 12 bold')
else:
    lbl.configure(text='Нажмите Enter')

lbl2 = Label()
lbl2.grid(column=1, row=4)

lbl3 = Label(text='Дата общения:')
lbl3.grid(column=0, row=1, sticky='E')

lbl4 = Label(text='Ссылка на резюме:')
lbl4.grid(column=0, row=2, sticky='E')

ent = Entry()
ent.grid(column=1, row=1)
ent.focus_set()
ent.bind("<Return>", save)

ent2 = Entry()
ent2.grid(column=1, row=2)
ent2.bind("<Return>", save)

btn = Button(text='Сохранить', command=save)
btn.grid(column=1, row=3, pady=10, ipadx=30)
btn.bind("<Return>", save)

btn2 = Button(text='Помощь', command=how_to)
btn2.grid(column=0, row=4, sticky='N', pady=15)

btn3 = Button(text='Удалить базу', command=delete_db)
btn3.grid(column=2, row=4, sticky='N', padx=20, pady=15)

window.mainloop()
