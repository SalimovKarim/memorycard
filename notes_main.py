from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QRadioButton, QMessageBox, QGroupBox, QButtonGroup, QTextEdit, QListWidget, QLineEdit, QInputDialog

import json

notes = {
    'Добро пожаловать!': {
        'текст': 'Это самое лучшее приложение для заметок в мире!',
        'теги':   ['добро', 'инструкция']},
        
    'Рахим итегес!': {
        'текст': 'это самое лучшее приложение для заметок в мире!',
        'теги': ['добро', 'инструкция']}
        
}
with open ('notes_data.json', 'w') as file:
    json.dump(notes, file)


app = QApplication([])
main_win = QWidget()
main_win.setWindowTitle('Умные заметки')
main_win.resize(700, 400)

main_hline = QHBoxLayout()#глав. гориз. линии

#вертик. линии
left_line = QVBoxLayout()
right_line = QVBoxLayout()


TextEdit = QTextEdit()

left_line.addWidget(TextEdit)

main_hline.addLayout(left_line)

list_notes = QListWidget()
list_notes_ladel = QLabel('Создать заметку')

right_line.addWidget(list_notes_ladel)
right_line.addWidget(list_notes)

button_create = QPushButton('Создать заметку')
button_del = QPushButton('Удалить заметку')
button_save = QPushButton('Сохранить заметку')

hline = QHBoxLayout()
hline.addWidget(button_create)
hline.addWidget(button_del)


right_line.addLayout(hline)
right_line.addWidget(button_save)




list_notes1 = QListWidget()
list_notes_ladel1 = QLabel('Список тегов')

right_line.addWidget(list_notes_ladel1)
right_line.addWidget(list_notes1)

line_edit = QLineEdit()
line_edit.setPlaceholderText('Введите текст...')

right_line.addWidget(line_edit)

hline1 = QHBoxLayout()


button_teg_create = QPushButton('Добавить к заметке')
button_teg_del = QPushButton('Открепить от заметки')
button_tag_search = QPushButton('Искать заметку по тегу')


hline1.addWidget(button_teg_create)
hline1.addWidget(button_teg_del)

right_line.addLayout(hline1)
right_line.addWidget(button_tag_search)




main_hline.addLayout(right_line)

#ставим на окно главюгоризю линию
main_win.setLayout(main_hline)


def show_notes():
    key = list_notes.selectedItems()[0].text()
    print(key)
    TextEdit.setText(notes[key]['текст'])
    list_notes1.clear()
    list_notes1.addItems(notes[key]['теги'])

list_notes.itemClicked.connect(show_notes)

def add_notes():
    note_name, ok = QInputDialog.getText(main_win, 'Добавить заметку', 'Название заметки:')
    if ok and note_name != '':
        notes[note_name] = {'текст' : '', 'теги' : []}
        list_notes.addItem(note_name)
        list_notes1.addItems(notes[note_name]['теги'])
        print(notes)
button_create.clicked.connect(add_notes)

list_notes.addItems(notes)


# сохранение заметки в поле заметок
def save_note():             
    if list_notes.selectedItems():# если в списке заметок выбрана заметка то:
        key = list_notes.selectedItems()[0].text()#
        notes[key]['текст'] = TextEdit.toPlainText()
        with open ('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys = True)
        print(notes) # добавить заметку
    else:
        print('Заметка для сохранения не выбрана!')
        pass
button_save.clicked.connect(save_note)

def del_note ():
    if list_notes.selectedItems():# если в списке заметок выбрана заметка то:
        key  = list_notes.selectedItems()[0].text()
        del notes [key]#удаление
        list_notes.clear()#отчистка заметок
        list_notes1.clear()#отчистка тегов
        TextEdit.clear()#отчистка текста
        list_notes.addItems(notes) 
        with open ('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys = True)
        print(notes)
    else:
        print('Заметка для удаления не выбрана!')
button_del.clicked.connect(del_note)


def add_tag():
    if list_notes.selectedItems():# если в списке заметок выбрана заметка то:
        key = list_notes.selectedItems()[0].text()
        tag = line_edit.text()
        if not tag in notes[key]['теги']:
            notes [key]['теги'].append(tag)
            list_notes1.addItem(tag)
            line_edit.clear()#очищение текста из линии введите тег
        with open ('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys = True)
        print(notes)
    else:
        print('Заметка для добавления тега не выбрана!')
button_teg_create.clicked.connect(add_tag)


def del_tag():
    if list_notes1.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_notes1.selectedItems()[0].text()
        notes [key]['теги'].remove(tag)
        list_notes1.clear()
        list_notes1.addItems(notes[key]['теги'])
        with open ('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys = True)
    else:
        print('Тег для удаления не выбран!')
button_teg_del.clicked.connect(del_tag)


def search_tag():
    print(button_tag_search.text())
    tag = line_edit.text()
    if button_tag_search.text() == 'Искать заметку по тегу' and tag:
        print(tag)
        notes_filtered = {}
        # тут будут заметки с выделенным тегом
        for note in notes:
            if tag in notes[note]['теги']:
                notes_filtered[note] = notes[note]
        button_tag_search.setText('Сбросить поиск')
        list_notes.clear()
        list_notes1.clear()
        list_notes.addItems(notes_filtered)
        print(button_tag_search.text())
    elif button_tag_search.text() == 'Сбросить поиск':
        line_edit.clear()
        list_notes.clear()
        list_notes1.clear()
        list_notes.addItems(notes)
        button_tag_search.setText('Искать заметки по тегу')
        print(button_tag_search.text())
    else:
        pass
button_tag_search.clicked.connect(search_tag)




main_win.show()
app.exec()
