from telebot import TeleBot, types
from datetime import datetime

TOKEN = ''
bot = TeleBot(TOKEN)
tasks = []


class Task:

    def __init__(self, descr, deadline=None):
        self.descr = descr
        self.deadline = deadline


@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_1 = types.KeyboardButton('Создать новую задачу')
    button_2 = types.KeyboardButton('Открыть список задач')
    button_3 = types.KeyboardButton('Задача выполнена')
    markup.add(button_1, button_2, button_3)

    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}! '
                                      f'Я - {bot.get_me().first_name}, бот по управлению задачами. '
                                      f'Используйте команды на клавиатуре.', parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(message.chat.id, 'Доступные команды:\n'
                                      '/start - начать взаимодействие\n'
                                      '/help - показать справочную информацию\n'
                                      'Создать новую задачу - добавить новую задачу\n'
                                      'Открыть список задач - просмотреть список задач\n'
                                      'Задача выполнена - отметить задачу как выполненную')


@bot.message_handler(func=lambda message: message.text == 'Создать новую задачу')
def add_task(message):
    bot.send_message(message.chat.id, 'Введите новую задачу')
    bot.register_next_step_handler(message, insert_task)


@bot.message_handler(func=lambda message: message.text == 'Задача выполнена')
def lists_of_tasks(message):
    if not tasks:
        bot.send_message(message.chat.id, 'Задач еще нету')
    else:
        list_of_tasks = ''
        str(list_of_tasks)
        for i in range(len(tasks)):
            if tasks[i].deadline is None:
                tasks[i].deadline = ''
            list_of_tasks += (str(i + 1) + '. ' + tasks[i].descr + ' ' + str(tasks[i].deadline) + '\n')
        bot.send_message(message.chat.id, f'Ваш список задач:\n{list_of_tasks}')
        bot.register_next_step_handler(message, task_completed)
        bot.send_message(message.chat.id, 'Какая задача выполнена? Введите цифру')


def task_completed(message):
    if message.text.isdigit():
        if 0 <= int(message.text) <= len(tasks):
            inx = int(message.text) - 1
            bot.send_message(message.chat.id, f'Задача {tasks[inx].descr} выполнена')
            tasks.pop(inx)
        else:
            bot.send_message(message.chat.id, 'Неверное значение. Введите номер задачи')
            bot.register_next_step_handler(message, task_completed)
    else:
        if message.text == 'Создать новую задачу' or message.text == 'Открыть список задач' \
                or message.text == 'Задача выполнена':
            if message.text == 'Создать новую задачу':
                bot.send_message(message.chat.id, 'Введите новую задачу')
                bot.register_next_step_handler(message, insert_task)
            elif message.text == 'Открыть список задач':
                list_of_tasks = ''
                for i in range(len(tasks)):
                    if tasks[i].deadline is None:
                        tasks[i].deadline = ''
                        list_of_tasks += (str(i + 1) + '. ' + tasks[i].descr + ' ' + str(tasks[i].deadline) + '\n')
                        bot.send_message(message.chat.id, f'Ваш список задач:\n{list_of_tasks}')
                        bot.send_message(message.chat.id, 'Чтобы редактировать, введите номер задачи')
                        bot.register_next_step_handler(message, print_number)
            elif message.text == 'Задача выполнена':
                list_of_tasks = ''
                str(list_of_tasks)
                for i in range(len(tasks)):
                    if tasks[i].deadline is None:
                        tasks[i].deadline = ''
                    list_of_tasks += (str(i + 1) + '. ' + tasks[i].descr + ' ' + str(tasks[i].deadline) + '\n')
                bot.send_message(message.chat.id, f'Ваш список задач:\n{list_of_tasks}')
                bot.register_next_step_handler(message, task_completed)
                bot.send_message(message.chat.id, 'Какая задача выполнена? Введите порядковый номер задачи')
        else:
            bot.send_message(message.chat.id, 'Неверное значение. Введите номер задачи')
            bot.register_next_step_handler(message, task_completed)


def insert_task(message):
    if message.text == 'Создать новую задачу' or message.text == 'Открыть список задач' \
            or message.text == 'Задача выполнена':
        bot.send_message(message.chat.id, 'Эту задачу не надо добавлять)')
    else:
        if message.chat.id not in tasks:
            task = Task(descr=message.text)
            tasks.append(task)
        bot.send_message(message.chat.id, f'Задача {message.text} добавлена')
        bot.send_message(message.chat.id, 'Вы будете ставить дедлайн на эту задачу?', reply_markup=yes_or_no_keyboard())
        if message.text == 'Создать новую задачу' or message.text == 'Открыть список задач' \
                or message.text == 'Задача выполнена':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button_1 = types.KeyboardButton('Создать новую задачу')
            button_2 = types.KeyboardButton('Открыть список задач')
            button_3 = types.KeyboardButton('Задача выполнена')
            markup.add(button_1, button_2, button_3)
            bot.send_message(message.chat.id, '', reply_markup=markup)


def yes_or_no_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    button_1 = types.InlineKeyboardButton('Да', callback_data='Yes')
    button_2 = types.InlineKeyboardButton('Нет', callback_data='No')
    markup.add(button_1, button_2)
    return markup


def write_deadline(message):
    try:
        current_task = tasks[-1]
        task_deadline = str(datetime.strptime(message.text, '%Y:%m:%d').date())
        current_task.deadline = task_deadline
        bot.send_message(message.chat.id, f'Дедлайн для задачи {current_task.descr}'
                                          f' установлен на {task_deadline}\nЗадача добавлена в список')

    except ValueError:
        bot.send_message(message.chat.id, 'Некорректный формат даты. Попробуйте снова.')
        bot.send_message(message.chat.id, 'Напишите дату дедлайна в формате: год(xxxx):месяц(xx):день(xx)')
        bot.register_next_step_handler(message, write_deadline)


@bot.message_handler(func=lambda message: message.text == 'Открыть список задач')
def show_tasks(message):
    if not tasks:
        bot.send_message(message.chat.id, 'Задач еще нету')
    else:
        list_of_tasks = ''
        for i in range(len(tasks)):
            if tasks[i].deadline is None:
                tasks[i].deadline = ''
            list_of_tasks += (str(i+1) + '. ' + tasks[i].descr + ' ' + str(tasks[i].deadline) + '\n')
        bot.send_message(message.chat.id, f'Ваш список задач:\n{list_of_tasks}')
        bot.send_message(message.chat.id, 'Чтобы редактировать, введите номер задачи')
        bot.register_next_step_handler(message, print_number)


def print_number(message):
    if message.text.isdigit():
        if 0 <= int(message.text) <= len(tasks):
            markup = types.InlineKeyboardMarkup()
            button_1 = types.InlineKeyboardButton('Назад', callback_data='back')
            button_2 = types.InlineKeyboardButton('Удалить задачу', callback_data='delete')
            button_3 = types.InlineKeyboardButton('Изменить дедлайн', callback_data='deadline')
            markup.add(button_1, button_2, button_3)
            bot.send_message(message.chat.id, message.text, reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'Неверное значение')
            bot.send_message(message.chat.id, 'Чтобы редактировать, введите номер задачи')
            bot.register_next_step_handler(message, print_number)
    else:
        if message.text == 'Создать новую задачу':
            bot.send_message(message.chat.id, 'Введите новую задачу')
            bot.register_next_step_handler(message, insert_task)
        elif message.text == 'Открыть список задач':
            list_of_tasks = ''
            for i in range(len(tasks)):
                if tasks[i].deadline is None:
                    tasks[i].deadline = ''
                    list_of_tasks += (str(i + 1) + '. ' + tasks[i].descr + ' ' + str(tasks[i].deadline) + '\n')
                    bot.send_message(message.chat.id, f'Ваш список задач:\n{list_of_tasks}')
                    bot.send_message(message.chat.id, 'Чтобы редактировать, введите номер задачи')
                    bot.register_next_step_handler(message, print_number)
        elif message.text == 'Задача выполнена':
            list_of_tasks = ''
            str(list_of_tasks)
            for i in range(len(tasks)):
                if tasks[i].deadline is None:
                    tasks[i].deadline = ''
                list_of_tasks += (str(i + 1) + '. ' + tasks[i].descr + ' ' + str(tasks[i].deadline) + '\n')
            bot.send_message(message.chat.id, f'Ваш список задач:\n{list_of_tasks}')
            bot.register_next_step_handler(message, task_completed)
            bot.send_message(message.chat.id, 'Какая задача выполнена? Введите цифру')
        else:
            bot.send_message(message.chat.id, 'Неверное значение. Чтобы редактировать, введите номер задачи')
            bot.register_next_step_handler(message, print_number)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == 'No':
            bot.send_message(call.message.chat.id, 'У этой задачи не будет дедлайна. Задача добавлена в список')
        elif call.data == 'Yes':
            bot.send_message(call.message.chat.id, 'Напишите дату дедлайна в формате: год(xxxx):месяц(xx):день(xx)')
            bot.register_next_step_handler(call.message, write_deadline)
        if call.data == 'back':
            bot.send_message(call.message.chat.id, 'Возврат в список задач')
            show_tasks(call.message)
        elif call.data == 'delete':
            bot.send_message(call.message.chat.id, call.message.text)
            task_completed(call.message)


bot.polling(none_stop=True)