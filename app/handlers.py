from aiogram.types import Message, CallbackQuery
from aiogram import Router, F, Bot, Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
import joblib

import app.keyboards as kb
from app.searcher import SemanticSearch
from app.states import AskQuestion


router = Router()

async def init_models():
    model = joblib.load('save_model/franchise_model.pkl')
    print('Модель загружена')
    searcher = SemanticSearch('app/data/franchise_dataset.csv')
    print('Модель поисковика загружена')
    return model, searcher

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    username = message.from_user.username
    await message.answer(
            f'Здравствуйте, {username}.\n\n'
            f'Вы находитесь в системе поддержки по вопросам, связанным с франчайзингом.\n'
            f'Вы можете задать интересующий вас вопрос — система попытается определить его категорию и предоставить ответ. '
            f'При необходимости запрос будет передан специалисту соответствующего отдела.',
            reply_markup=kb.main
    )

@router.callback_query(F.data == 'question')
async def ask_question(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await callback.message.answer('Пожалуйста, введите ваш вопрос:')
    await state.set_state(AskQuestion.question)

@router.message(F.text)
async def get_question(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(question = message.text)
    model = getattr(bot, "model", None)
    searcher = getattr(bot, "searcher", None)
    question = message.text.strip()
    print(question)
    category = model.predict([question])[0]
    print(category)
    searching_in_db = searcher.search(question, category=category, top_k=1)
    if not searching_in_db:
        await message.answer("К сожалению, не удалось найти подходящий ответ на ваш вопрос.")
        return
    first_result = searching_in_db[0]
    question_in_db = first_result['question']
    answer_in_db = first_result['answer']
    await message.answer(f'Ваш вопрос относится к категории - {category}\n'
                         f'Нашел похожий вопрос: \n{question_in_db}\n'
                         f'Ответ на вопрос:\n{answer_in_db}')
    await message.answer(f'Ваш вопрос отнесён к категории: {category.capitalize()}.\n'
                         f'При необходимости могу передать его профильному специалисту. Продолжить?',
                         reply_markup=kb.call_to_operator)

@router.callback_query(F.data == 'call_operator')
async def call_operator(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.clear()
    await callback.message.answer('Запрос будет передан оператору. Ожидайте ответа в этом чате.\n\n'
        '(Демонстрационный режим: оператор не подключится.)', reply_markup=kb.back_to_menu)

@router.callback_query(F.data == 'about')
async def call_operator(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text(
        'О компании\n\n'
        'Мы предоставляем комплексные решения для запуска и развития бизнеса по франшизе. '
        'Консультации, поддержка, сопровождение и инструменты — всё в одном месте.',
        reply_markup=kb.back_to_menu)

@router.callback_query(F.data == 'back_to_menu')
async def call_operator(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text(f'Вы находитесь в системе поддержки по вопросам, связанным с франчайзингом.\n'
            f'Вы можете задать интересующий вас вопрос — система попытается определить его категорию и предоставить ответ. '
            f'При необходимости запрос будет передан специалисту соответствующего отдела.', reply_markup=kb.main)