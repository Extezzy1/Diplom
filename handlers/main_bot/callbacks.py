from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
import FSM
from database import Stores, Categories, Promocodes, Products
from polling_manager import add_bot, stop_bot
from dispatchers import dp_new_bot, polling_manager
import markups.admin_markup as admin_markup

callbacks_router = Router()


@callbacks_router.callback_query(lambda c: c.data.startswith("store_"))
async def show_store(callback: CallbackQuery):
    store_id = callback.data.split("_")[-1]
    await callback.message.edit_text("Управление магазином", reply_markup=admin_markup.create_markup_manage_store(store_id))


@callbacks_router.callback_query(lambda c: c.data == "back_to_list_stores")
async def back_to_list_stores(callback: CallbackQuery, session: AsyncSession):
    request = await session.execute(select(Stores))
    stores = request.fetchall()
    await callback.message.edit_text("Ваши магазины", reply_markup=admin_markup.create_markup_stores(stores))


@callbacks_router.callback_query(lambda c: c.data.startswith("categories_"))
async def show_markup_categories(callback: CallbackQuery, session: AsyncSession):
    store_id = callback.data.split("_")[-1]
    request = await session.execute(select(Categories).where(Categories.store_id == int(store_id)))
    categories = request.fetchall()
    if len(categories) > 0:
        msg = "<b>Управление категориями</b>\n\nТекущие категории:\n\n"
        for index, category in enumerate(categories, 1):
            msg += f"{index}. {category[0].category_title}\n"
    else:
        msg = "<b>Управление категориями</b>"
    await callback.message.edit_text(msg, parse_mode="HTML", reply_markup=admin_markup.create_markup_categories(store_id))


@callbacks_router.callback_query(lambda c: c.data.startswith("main_menu_"))
async def main_menu_(callback: CallbackQuery):
    store_id = callback.data.split("_")[-1]
    await callback.message.edit_text("Управление магазином", reply_markup=admin_markup.create_markup_manage_store(store_id))


@callbacks_router.callback_query(lambda c: c.data.startswith("add_category"))
async def add_category(callback: CallbackQuery, state: FSMContext):
    store_id = callback.data.split("_")[-1]
    await state.set_state(FSM.FSMAdmin.get_category_name)
    await state.set_data({"store_id": store_id})
    await callback.message.answer("Пришлите наименование категории")


@callbacks_router.callback_query(lambda c: c.data.startswith("delete_categories"))
async def delete_categories(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    store_id = callback.data.split("_")[-1]
    request = await session.execute(select(Categories).where(Categories.store_id == int(store_id)))
    categories = request.fetchall()
    if len(categories) == 0:
        await callback.message.answer("Список категорий пуст!")
        return

    await callback.message.edit_text("Выберите категорию для удаления", reply_markup=admin_markup.create_markup_delete_categories(store_id, categories))


@callbacks_router.callback_query(lambda c: c.data.startswith("delete_category"))
async def delete_category(callback: CallbackQuery, session: AsyncSession):
    category_id = callback.data.split("_")[-1]
    request = await session.execute(select(Categories).where(Categories.category_id == int(category_id)))
    categories = request.fetchmany(1)[0][0]
    store_id = categories.store_id
    await session.execute(delete(Categories).where(Categories.category_id == int(category_id)))
    await session.commit()
    request = await session.execute(select(Categories).where(Categories.store_id == int(store_id)))
    categories = request.fetchall()
    if len(categories) > 0:
        msg = "<b>Категория успешно удалена\n\nУправление категориями</b>\n\nТекущие категории:\n\n"
        for index, category in enumerate(categories, 1):
            msg += f"{index}. {category[0].category_title}\n"
    else:
        msg = "<b>Категория успешно удалена\n\nУправление категориями</b>"
    await callback.message.edit_text(msg, parse_mode="HTML", reply_markup=admin_markup.create_markup_categories(store_id))


@callbacks_router.callback_query(lambda c: c.data.startswith("edit_categories"))
async def edit_categories(callback: CallbackQuery, session: AsyncSession):
    store_id = callback.data.split("_")[-1]
    request = await session.execute(select(Categories).where(Categories.store_id == int(store_id)))
    categories = request.fetchall()
    if len(categories) == 0:
        await callback.message.answer("Список категорий пуст!")
        return

    await callback.message.edit_text("Выберите категорию для редактирования", reply_markup=admin_markup.create_markup_edit_categories(store_id, categories))


@callbacks_router.callback_query(lambda c: c.data.startswith("edit_category"))
async def edit_category(callback: CallbackQuery, session: AsyncSession, state: FSMContext):
    category_id = callback.data.split("_")[-1]
    await state.set_state(FSM.FSMAdmin.get_new_category_name)
    await state.set_data({"category_id": category_id})
    await callback.message.answer("Введите новое наименование категории")


@callbacks_router.callback_query(lambda c: c.data.startswith("back_to_categories_"))
async def back_to_categories_(callback: CallbackQuery, session: AsyncSession):
    store_id = callback.data.split("_")[-1]
    request = await session.execute(select(Categories).where(Categories.store_id == int(store_id)))
    categories = request.fetchall()
    if len(categories) > 0:
        msg = "<b>Управление категориями</b>\n\nТекущие категории:\n\n"
        for index, category in enumerate(categories, 1):
            msg += f"{index}. {category[0].category_title}\n"
    else:
        msg = "<b>Управление категориями</b>"
    await callback.message.edit_text(msg, parse_mode="HTML", reply_markup=admin_markup.create_markup_categories(store_id))


@callbacks_router.callback_query(lambda c: c.data.startswith("promocodes_"))
async def promocodes_(callback: CallbackQuery):
    store_id = callback.data.split("_")[-1]
    await callback.message.edit_text("Управление промокодами")
    await callback.message.edit_reply_markup(reply_markup=admin_markup.create_markup_promocodes(store_id))


@callbacks_router.callback_query(lambda c: c.data.startswith("add_promocode"))
async def add_promocode(callback: CallbackQuery, state: FSMContext):
    store_id = callback.data.split("_")[-1]
    await state.set_state(FSM.FSMAdmin.get_promocode_name)
    await state.set_data({"store_id": store_id})
    await callback.message.answer("Пришлите наименование промокода", reply_markup=admin_markup.create_markup_cancel())


@callbacks_router.callback_query(lambda c: c.data.startswith("delete_promocodes_"))
async def delete_promocodes(callback: CallbackQuery, session: AsyncSession):
    store_id = callback.data.split("_")[-1]
    request = await session.execute(select(Promocodes).where(Promocodes.store_id == int(store_id)))
    current_promocodes = [item[0] for item in request.fetchall()]
    if len(current_promocodes) > 0:
        await callback.message.edit_text("Выберите промокод для удаления")
    else:
        await callback.message.edit_text("Список промокодов пуст!")

    await callback.message.edit_reply_markup(reply_markup=admin_markup.create_markup_delete_promocodes(current_promocodes, store_id))


@callbacks_router.callback_query(lambda c: c.data.startswith("delete_promocode"))
async def delete_promocode(callback: CallbackQuery, session: AsyncSession):
    promocode_id = callback.data.split("_")[-1]

    request = await session.execute(select(Promocodes.store_id).where(Promocodes.promocode_id == int(promocode_id)))
    store_id = request.fetchmany(1)[0][0]

    await session.execute(delete(Promocodes).where(Promocodes.promocode_id == int(promocode_id)))
    await session.commit()

    request = await session.execute(select(Promocodes).where(Promocodes.store_id == int(store_id)))
    current_promocodes = [item[0] for item in request.fetchall()]
    if len(current_promocodes) > 0:
        await callback.message.edit_text("Выберите промокод для удаления")
    else:
        await callback.message.edit_text("Список промокодов пуст!")

    await callback.message.edit_reply_markup(
        reply_markup=admin_markup.create_markup_delete_promocodes(current_promocodes, store_id))


@callbacks_router.callback_query(lambda c: c.data.startswith("back_promocodes_"))
async def back_promocodes(callback: CallbackQuery):
    store_id = callback.data.split("_")[-1]
    await callback.message.edit_text("Управление промокодами")
    await callback.message.edit_reply_markup(reply_markup=admin_markup.create_markup_promocodes(store_id))


@callbacks_router.callback_query(lambda c: c.data.startswith("active_promocodes_"))
async def active_promocodes(callback: CallbackQuery, session: AsyncSession):
    store_id = callback.data.split("_")[-1]
    request = await session.execute(select(Promocodes).where(Promocodes.store_id == int(store_id)))
    promocodes = request.fetchall()
    if len(promocodes) > 0:
        msg = "Активные промокоды:\n\n"
        for index, promocode in enumerate(promocodes, 1):
            msg += f"{index}. <b>{promocode[0].promocode_title}</b>, процент скидки: <b>{promocode[0].discount_percent}</b>\n"
        await callback.message.edit_text(msg)
        await callback.message.edit_reply_markup(reply_markup=admin_markup.create_markup_show_active_promocodes(store_id))

    else:
        await callback.message.answer("Список промокодов пуст!")


@callbacks_router.callback_query(lambda c: c.data.startswith("set_discount_"))
async def set_discount(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    store_id = callback.data.split("_")[-1]
    request = await session.execute(select(Promocodes).where(Promocodes.store_id == int(store_id)))
    current_promocodes = [item[0] for item in request.fetchall()]
    if len(current_promocodes) > 0:
        await callback.message.edit_text("Выберите промокод, в котором хотите поменять процент скидки")
    else:
        await callback.message.edit_text("Список промокодов пуст!")

    await callback.message.edit_reply_markup(reply_markup=admin_markup.create_markup_set_discount_promocode(current_promocodes, store_id))


@callbacks_router.callback_query(lambda c: c.data.startswith("set_promocode_discount"))
async def set_discount_promocode(callback: CallbackQuery, state: FSMContext):
    promocode_id = callback.data.split("_")[-1]
    await callback.message.answer("Введите новый процент скидки", reply_markup=admin_markup.create_markup_cancel())
    await state.set_state(FSM.FSMAdmin.get_new_promocode_discount)
    await state.set_data({"promocode_id": promocode_id})


@callbacks_router.callback_query(lambda c: c.data.startswith("products_"))
async def products_callback(callback: CallbackQuery):
    store_id = callback.data.split("_")[-1]
    await callback.message.edit_text("Управление товарами")
    await callback.message.edit_reply_markup(reply_markup=admin_markup.create_markup_products(store_id))


@callbacks_router.callback_query(lambda c: c.data.startswith("add_product"))
async def add_product(callback: CallbackQuery, state: FSMContext):
    store_id = callback.data.split("_")[-1]
    await state.set_state(FSM.FSMAdmin.get_product_name)
    await state.set_data({"store_id": store_id})
    await callback.message.answer("Пришлите наименование товара")


# @callbacks_router.callback_query(lambda c: c.data.startswith("delete_products"))
# async def delete_products(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
#     store_id = callback.data.split("_")[-1]
#     request = await session.execute(select(Products).where(Products.store_id == int(store_id)))
#     products = request.fetchall()
#     if len(products) == 0:
#         await callback.message.answer("Список продуктов пуст!")
#         return
#
#     await callback.message.edit_text("Выберите продукт для удаления", reply_markup=admin_markup.create_markup_delete_products(store_id, products))
#
#
# @callbacks_router.callback_query(lambda c: c.data.startswith("delete_product"))
# async def delete_product(callback: CallbackQuery, session: AsyncSession):
#     product_id = callback.data.split("_")[-1]
#     request = await session.execute(select(Products).where(Products.product_id == int(product_id)))
#     products = request.fetchmany(1)[0][0]
#     store_id = products.store_id
#     await session.execute(delete(Products).where(Products.product_id == int(product_id)))
#     await session.commit()
#     request = await session.execute(select(Products).where(Products.store_id == int(store_id)))
#     products = request.fetchall()
#     if len(products) > 0:
#         msg = "<b>Товар успешно удален\n\nУправление товарами</b>\n\nТекущие товары:\n\n"
#         for index, product in enumerate(products, 1):
#             msg += f"{index}. {product[0].product_title}\n"
#     else:
#         msg = "<b>Товар успешно удален\n\nУправление товарами</b>"
#     await callback.message.edit_text(msg, parse_mode="HTML", reply_markup=admin_markup.create_markup_products(store_id))
#
#
# @callbacks_router.callback_query(lambda c: c.data.startswith("edit_products"))
# async def edit_products(callback: CallbackQuery, session: AsyncSession):
#     store_id = callback.data.split("_")[-1]
#     request = await session.execute(select(Products).where(Products.store_id == int(store_id)))
#     products = request.fetchall()
#     if len(products) == 0:
#         await callback.message.answer("Список продуктов пуст!")
#         return
#
#     await callback.message.edit_text("Выберите продукт для редактирования", reply_markup=admin_markup.create_markup_edit_products(store_id, products))
#
#
# @callbacks_router.callback_query(lambda c: c.data.startswith("edit_product"))
# async def edit_product(callback: CallbackQuery, session: AsyncSession, state: FSMContext):
#     product_id = callback.data.split("_")[-1]
#     await state.set_state(FSM.FSMAdmin.get_new_product_name)
#     await state.set_data({"product_id": product_id})
#     await callback.message.answer("Введите новое наименование продукта")
#
#
