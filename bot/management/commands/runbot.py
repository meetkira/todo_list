import datetime

from django.core.management.base import BaseCommand

from bot.models import TgUser
from bot.tg.client import TgClient
from goals.models import Goal, GoalCategory
from todo_list.settings import TELEGRAM_TOKEN


class Command(BaseCommand):
    help = 'Starts telegram bot'

    def handle(self, *args, **kwargs):
        offset = 0
        tg_client = TgClient(TELEGRAM_TOKEN)
        print(TELEGRAM_TOKEN)
        while True:
            res = tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                tg_user = TgUser.objects.filter(telegram_user_id=item.message.from_.id).first()
                if tg_user:
                    if tg_user.user is None:
                        tg_client.new_verification_code()
                        tg_user.verification_code = tg_client.verification_code
                        tg_user.save()
                        text = f"Подтвердите, пожалуйста, свой аккаунт. " \
                               f"Для подтверждения необходимо ввести код: {tg_user.verification_code} на сайте"
                    else:
                        text = "неизвестная команда"
                        if item.message.text == "/goals":
                            goals = Goal.objects.filter(is_deleted=False,
                                                        category__board__participants__user=tg_user.user)
                            goals_list = [f"Goal {goal.id} - {goal.title}" for goal in goals]
                            text = "\n".join(goals_list)
                        elif item.message.text == "/create":
                            categories = GoalCategory.objects.filter(is_deleted=False,
                                                                     board__participants__user=tg_user.user)
                            categories_list = [cat.title for cat in categories]
                            text = "\n".join(categories_list)
                            tg_client.send_message(chat_id=item.message.chat.id, text="Выберите категорию\n " + text)
                            res = tg_client.get_updates(offset=offset, timeout=30)
                            offset += 1
                            category = GoalCategory.objects.filter(title=res.result[0].message.text).first()
                            if not category:
                                text = "нет такой категории"
                            else:
                                tg_client.send_message(chat_id=item.message.chat.id, text="Выберите заголовок")
                                res = tg_client.get_updates(offset=offset, timeout=30)
                                offset += 1
                                goal = Goal.objects.create(title=res.result[0].message.text, category=category,
                                                    user=tg_user.user, due_date=datetime.date.today())
                                text = f"Создана цель {goal.id} - {goal.title}"
                else:
                    tg_client.new_verification_code()
                    TgUser.objects.create(telegram_user_id=item.message.from_.id, telegram_chat_id=item.message.chat.id,
                                          verification_code=tg_client.verification_code)

                    text = f"Приветствую! Код верификации: {tg_client.verification_code}"
                tg_client.send_message(chat_id=item.message.chat.id, text=text)
