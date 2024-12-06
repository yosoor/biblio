import json
import subprocess
import os
import time

# Функция для выгрузки книг из файла


def load_data():
    with open('database.json', 'r', encoding='utf-8') as database_file:
        list_of_books = json.load(database_file)
        return list_of_books

# Функция для загрузки книг в файл


def dump_data(list_of_books: list):  
    with open('database.json', 'w', encoding='utf-8') as database_file:
        json.dump(list_of_books, database_file, ensure_ascii=False)
    pass

# Функция для добавления книги


def book_add(title: str, author: str, year: str):
    list_of_books = load_data()
    # если year состоит не только из цифр, возвращаем False
    try:
        int(year)
    except ValueError:
        return False
    if len(list_of_books) == 0:
        list_of_books = [{'id': 0, 'title': title, 'author': author, 'year': year, 'status': 'в наличии'}]
        dump_data(list_of_books)
        print('Книга добавлена.')
    else:
        # Проверка на то, есть ли уже книга в библиотеке
        flag = False
        for book in list_of_books:
            if title in book.values() and author in book.values():
                flag = True
                print('Эта книга уже добавлена.')
                break
        if flag is False:
            list_of_books.append({'id': list_of_books[-1]['id'] + 1, 'title': title, 'author': author, 'year': year, 'status': 'в наличии'})
            dump_data(list_of_books)
            print('Книга добавлена.')
    pass

# Функция для удаления книги


def book_delete(book_id: str):
    list_of_books = load_data()
    # если book_id состоит не только из цифр, возвращаем False
    try:
        int(book_id)
    except ValueError:
        return False
    if len(list_of_books) == 0:
        print('Библиотека пуста.')
    else:
        flag = True
        for book in list_of_books:
            if int(book_id) in book.values():
                flag = False
                list_of_books.pop(list_of_books.index(book))
                dump_data(list_of_books)
                
                print('Книга удалена.')
                break
        if flag == True:
            print('Нет книги с таким id.')
            return False
    pass           

# Функция для поиска книги


def book_search(search_value: str):
    list_of_books = load_data()
    if len(list_of_books) == 0:
        print('Библиотека пуста.')
    results_of_search = 0
    for i in list_of_books:
        if search_value in i.values():
            results_of_search += 1
            print(f"""
Название книги: {i['title']}
Автор: {i['author']}
Год: {i['year']}
            """)
    if results_of_search == 0:
        print('\nНет результатов.')     
    pass


# Функция вывод списка книг


def show_list_of_books():
    list_of_books = load_data()
    if len(list_of_books) == 0:
        print('Библиотека пуста.')
    else:
        # Форматирование строк за счет указания размеров полей, чтобы при выводе в консоль ничего не съезжало
        print('%-10s %-20s %-20s %-20s %-20s' % ('ID', 'TITLE', 'AUTHOR', 'YEAR', 'STATUS'))
        print()
        for i in list_of_books:
            print('%-10s %-20s %-20s %-20s %-20s' % (i['id'], i['title'], i['author'], i['year'], i['status']))
            print()
    pass


# Функция для смены статуса книги


def do_new_status(book_id: str, new_status: str):
    list_of_books = load_data()
    # если year состоит не только из цифр, возвращаем False
    try:
        int(book_id)

    except ValueError:
        return False
    if new_status not in ('выдана', 'в наличии'):
        return False
    
    elif len(list_of_books) == 0:
        print('Библиотека пуста.')
    else:
        flag = False
        for i in list_of_books:
            if int(book_id) == i['id']:
                flag = True
                i['status'] = new_status
                dump_data(list_of_books)
                print('\nСтатус изменен.')
        if flag is False:
            print('\nКниги с таким id нет.')
            return False      
    pass

# Навигационный блок
# Бесконечный цикл был создан для того, чтобы после реализации одной из функций у пользователя была возможность вернуться главное меню


while True:
    user_chouse = input(
    """
Выберите действие:
                
1. Добавление книги
2. Удаление книги
3. Поиск книги
4. Отображение всех книг
5. Изменение статуса книги
6. Выйти из приложения

    """)
    
    # subprocess в данном случае производит очистку консоли(чтобы выбранная цифра вместе с меню исчезала)
    subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)
    if user_chouse == "1":
        title = input('Введите название книги: ')
        author = input('Введите ФИО автора в формате "Фамилия И.О.": ')
        year = input('Введите год издания: ')

        # Если функция вернула False, значит в year  не только цифры
        while book_add(title, author, year) is False:
            year = input('Год издания должен состоять из цифр, попробуйте еще раз: ')
        time.sleep(3)
        subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)
        
    
    if user_chouse == '2':
        book_id = input('Введите id книги: ')

        # Если функция вернула False, значит book_id состоит не только из цифр или нет книги с таким id
        while book_delete(book_id) == False:
            subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)
            print('Данные введены некорректно.')
            book_id = input('Ввдите id книги: ')
        time.sleep(3)
        subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)
        
        
    if user_chouse == '3':
        value_of_search = input('Введите или название книги, или имя автора или год ее издания: ')
        book_search(value_of_search)
        main_menu = input('\n\nНажмите Enter, чтобы выйти в главное меню')
        subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)
        
    if user_chouse == '4':
        show_list_of_books()
        main_menu = input('\n\nНажмите Enter, чтобы выйти в главное меню')
        subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)

    if user_chouse == '5':
        new_status = input('Введите новый статус ("в наличии", "выдана"): ')
        book_id = input('Введите id книги: ')
        #Если функция вернула False, значит book_id состоит не только из цифр или нет книги с таким id или неправильно введен new_status
        while do_new_status(book_id, new_status) == False:
            subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)
            print('Данные введены некорректно.')
            new_status = input('Введите новый статус ("в наличии", "выдана"): ')
            book_id = input('Введите id книги: ')
        time.sleep(3)
        subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)  

    if user_chouse == '6':
        break
    
        
