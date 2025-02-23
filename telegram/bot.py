from datetime import datetime
import os
from importlib.resources import files
from os import getenv
from django.core.files import File
import django
from aiogram.types import Message, ReplyKeyboardRemove, InputFile, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from rest_framework.status import is_client_error

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

from main.models import Survey, Answer, Client, Question, Mark

from aiogram.types import ReplyKeyboardMarkup

from aiogram import Bot, Dispatcher
from aiogram.utils import executor
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()
storage = MemoryStorage()
bot = Bot(token=getenv('BOT_TOKEN'))
dp = Dispatcher(bot, storage=storage)

# Состояния
class UserForm(StatesGroup):
    name = State()
    phone = State()
    email = State()

class QuestionForm(StatesGroup):
    waiting_for_answer = State()

is_client_created = False
is_client_end_asking = False
dead_buttons = []


def marking(que):
    menu_marking = ReplyKeyboardMarkup(resize_keyboard=True)
    if que.type_q == 'yes_or_no':
        menu_marking.add('Да').add('Нет')
    elif que.type_q == 'one_of_some':
        marks = Mark.objects.filter(que=que)
        for i in marks:
            if i.mark_text not in dead_buttons:
                menu_marking.add(i.mark_text)
        menu_marking.add('Далее')
    else:
        return ReplyKeyboardRemove()
    return menu_marking


@dp.message_handler(commands=['start'])
async def get_message(message: Message):
    global is_client_created
    my_chat = message.chat.id
    if Survey.objects.filter(active=True).exists():
        now_survey = Survey.objects.get(active=True)
        hello_text = now_survey.hello_text
    if not is_client_created:
        await bot.send_message(chat_id=message.chat.id, text=hello_text)
    try:
        now_client = Client.objects.get(acc_tg=message.from_user.username)
        my_text = 'Готов пройти опрос?'
        button1 = 'Готов'
        button2 = 'Нет, спасибо, позже'
        menu = ReplyKeyboardMarkup(resize_keyboard=True).add(button1, button2)
        await bot.send_message(chat_id=message.chat.id, text=my_text, reply_markup=menu)
        is_client_created = False
    except Client.DoesNotExist:
        is_client_created = True
        await bot.send_message(chat_id=message.chat.id, text="Мы не знакомы, познакомимся?", reply_markup=ReplyKeyboardRemove())
        await start(message)
        return


@dp.message_handler(text='Готов')
async def asking(message: Message, state: FSMContext):
    if not Survey.objects.filter(active=True).exists():
        await bot.send_message(chat_id=message.chat.id, text="На данный момент нет активных опросов.", reply_markup=ReplyKeyboardRemove())
        return

    now_survey = Survey.objects.get(active=True)
    await state.update_data(survey_id=now_survey.id, current_question=1)
    await ask_survey(message, state)


async def ask_survey(message: Message, state: FSMContext):
    user_data = await state.get_data()
    survey_id = user_data.get("survey_id")
    current_question = user_data.get("current_question")

    now_survey = Survey.objects.get(id=survey_id)
    total_questions = now_survey.counting

    if current_question > total_questions:
        '''if os.path.exists(file_path):
            file = InputFile(file_path)
            await bot.send_document(chat_id=message.chat.id, document=file)
        # else:
        #    await message.reply("Файл не найден. Пожалуйста, проверьте путь к файлу.")'''
        await bot.send_message(chat_id=message.chat.id, text="Спасибо за участие в опросе!", reply_markup=ReplyKeyboardRemove())
        await state.finish()
        return

    now_question = Question.objects.filter(survey=now_survey, numb=current_question).first()
    if now_question:
        que_text = now_question.que_text
        if que_text:
            if now_question.file:
                file_path = now_question.file.path
                try:
                    file = InputFile(file_path)
                    if now_question.kind_file == 'photo':
                        await bot.send_photo(
                            chat_id=message.chat.id,
                            photo=file,
                            caption=que_text,
                            reply_markup=marking(now_question)
                        )
                    elif now_question.kind_file == 'video':
                        await bot.send_video(
                            chat_id=message.chat.id,
                            video=file,
                            caption=que_text,
                            reply_markup=marking(now_question)
                        )
                    elif now_question.kind_file == 'audio':
                        await bot.send_audio(
                            chat_id=message.chat.id,
                            audio=file,
                            caption=que_text,
                            reply_markup=marking(now_question)
                        )
                    else:
                        await bot.send_document(
                            chat_id=message.chat.id,
                            document=file,
                            caption=que_text,
                            reply_markup=marking(now_question)
                        )
                except FileNotFoundError:
                    await bot.send_message(chat_id=message.chat.id, text="Документ не найдено.")
            else:
                await bot.send_message(chat_id=message.chat.id, text=que_text, reply_markup=marking(now_question))
            if now_question.wait_answer:
                await QuestionForm.waiting_for_answer.set()
            else:
                await state.update_data(current_question=current_question + 1)
                await ask_survey(message, state)
        else:
            await message.answer("Ошибка: текст вопроса отсутствует.")
            await state.finish()
    else:
        await message.answer("Ошибка: вопрос не найден.")
        await state.finish()


@dp.message_handler(state=QuestionForm.waiting_for_answer)
async def handle_answer(message: Message, state: FSMContext):
    global is_client_end_asking
    global dead_buttons
    if message.text == 'Далее':
        is_client_end_asking = True
        dead_buttons = []
    user_data = await state.get_data()
    survey_id = user_data.get("survey_id")
    current_question = user_data.get("current_question")
    now_client = Client.objects.get(acc_tg=message.from_user.username)
    now_survey = Survey.objects.get(id=survey_id)
    now_question = Question.objects.filter(survey=now_survey, numb=current_question).first()
    if (is_client_end_asking and now_question) and now_question.type_q == 'one_of_some':
        is_client_end_asking = False
        await state.update_data(current_question=current_question + 1)
        await ask_survey(message, state)
    elif now_question:
        # if message.text == 'Далее':
         #   await bot.send_message(chat_id=message.chat.id, text="Пожалуйста, выберете один из вариантов")
        #else:
        Answer.objects.create(
            client_tg_acc=message.from_user.username,
            que=now_question,
            ans=message.text,
            date=datetime.now(),
            client_id=now_client
        )
        if now_question.type_q == 'one_of_some':
            is_client_end_asking = False
            dead_buttons.append(message.text)
            await state.update_data(current_question=current_question)
            await ask_survey(message, state)
        else:
            is_client_end_asking = False
            await state.update_data(current_question=current_question + 1)
            await ask_survey(message, state)
    else:
        await message.answer("Ошибка: текущий вопрос не найден.")
        await state.finish()


@dp.message_handler()
async def start(message: Message):
    if is_client_created:
        await UserForm.name.set()
        await message.answer('Напишите, пожалуйста ваше имя.')


@dp.message_handler(state=UserForm.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Спасибо! Теперь напишите ваш номер телефона.")
    await UserForm.phone.set()

@dp.message_handler(state=UserForm.phone)
async def process_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer("Отлично! Теперь введите вашу почту.")
    await UserForm.email.set()

@dp.message_handler(state=UserForm.email)
async def process_email(message: Message, state: FSMContext):
    email = message.text.strip()
    if not email or "@" not in email:
        await message.answer("Пожалуйста, введите корректный email.")
        return

    await state.update_data(email=email)
    user_data = await state.get_data()
    Client.objects.create(
        name=user_data.get("name"),
        acc_tg=message.from_user.username,
        phone=user_data.get("phone"),
        email=email,
        tg_id=message.from_user.id
    )
    start_botton = ReplyKeyboardMarkup(resize_keyboard=True).add('/start')
    await bot.send_message(chat_id=message.chat.id, text="Спасибо! Вы зарегистрированы. Теперь введите /start для начала опроса."
                           , reply_markup=start_botton)
    await state.finish()




#executor.start_polling(dp)
async def main():
    # Запуск бота
    try:
        await dp.start_polling()
    finally:
        await bot.close()