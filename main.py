from aiogram import Dispatcher,executor,types,Bot
from config import API_KEY
import database

bot = Bot(token = API_KEY)
dp = Dispatcher(bot)

database.init_db()

@dp.message_handler(commands="start")
async def start(message: types.Message):
    await message.reply("Ку")

@dp.message_handler(commands="add")
async def add(message: types.Message):
    task = message.get_args()
    if task:
        user_id = message.from_user.id
        username = message.from_user.username
        database.add_task(user_id, username, task)
        await message.reply(f"Задача {task} добавлена")
    else:
        await message.reply("Укажите задачу")

@dp.message_handler(commands="list")
async def list(message: types.Message):
    tasks = message.get_args()
    if tasks:
        tasks_list = "\n".join([f"{task[0]}. {task[3]} (Добавлено пользователем {task[2]})" for task in tasks])
        await message.reply(f"Ваши задачи: \n{tasks_list}")
    else:
        await message.reply("Нет задач")

@dp.message_handler(commands="delete")
async def delete(message: types.Message):
    task_id = message.get_args()
    if task_id.isdigit():
        database.delete_task(int(task_id))
        await message.reply(f"Задача {task_id} удалена")
    else:
        await message.reply("Укажите id задачи")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates= True)