import datetime

from django.core.management.base import BaseCommand

from bot.models import TgUser, TgProcessedUpdate
from bot.tg.client import TgClient
from goals.models import Goal, GoalCategory
from todo_list.settings import TELEGRAM_TOKEN


class Command(BaseCommand):
    help = 'Starts telegram bot'

    def handle(self, *args, **kwargs):
        last_update = TgProcessedUpdate.objects.first()
        tg_client = TgClient(TELEGRAM_TOKEN)
        while True:
            res = tg_client.get_updates(offset=last_update.update_id + 1 if last_update else 0)
            for item in res.result:
                text = "неизвестная команда"
                last_update_id = item.update_id
                tg_user = TgUser.objects.filter(telegram_user_id=item.message.from_.id).first()
                if not tg_user:
                    tg_client.new_verification_code()
                    TgUser.objects.create(telegram_user_id=item.message.from_.id, telegram_chat_id=item.message.chat.id,
                                          verification_code=tg_client.verification_code)

                    text = f"Приветствую! Код верификации: {tg_client.verification_code}"
                else:
                    if tg_user.user is None:
                        tg_client.new_verification_code()
                        tg_user.verification_code = tg_client.verification_code
                        tg_user.save()
                        text = f"Подтвердите, пожалуйста, свой аккаунт. " \
                               f"Для подтверждения необходимо ввести код: {tg_user.verification_code} на сайте"
                    else:

                        if item.message.text == "/goals":
                            goals = Goal.objects.filter(is_deleted=False,
                                                        category__board__participants__user=tg_user.user)
                            goals_list = [f"Goal {goal.id} - {goal.title}" for goal in goals]
                            if goals_list:
                                text = "\n".join(goals_list)
                            else:
                                text = "пусто"
                        if item.message.text == "/create":
                            categories = GoalCategory.objects.filter(is_deleted=False,
                                                                     board__participants__user=tg_user.user)
                            categories_list = [cat.title for cat in categories]
                            if categories_list:
                                text = "\n".join(categories_list)
                                tg_client.send_message(chat_id=item.message.chat.id, text="Выберите категорию\n " + text)
                                last_update_id+=1
                                res_cat = tg_client.get_updates(offset=last_update_id, timeout=30)
                                category = GoalCategory.objects.filter(title=res_cat.result[0].message.text).first()
                                if not category:
                                    text = "нет такой категории"
                                else:
                                    tg_client.send_message(chat_id=item.message.chat.id, text="Выберите заголовок")
                                    last_update_id+=1
                                    res_goal_title = tg_client.get_updates(offset=last_update_id, timeout=30)
                                    goal = Goal.objects.create(title=res_goal_title.result[0].message.text,
                                                               category=category,
                                                               user=tg_user.user, due_date=datetime.date.today())
                                    text = f"Создана цель {goal.id} - {goal.title}"
                            else:
                                text = "пусто"

                tg_client.send_message(chat_id=item.message.chat.id, text=text)

                if last_update_id:
                    TgProcessedUpdate.objects.all().delete()
                    last_update = TgProcessedUpdate.objects.create(update_id=last_update_id)
