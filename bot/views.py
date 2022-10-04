from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from bot.models import TgUser
from bot.tg.client import TgClient
from todo_list.settings import TELEGRAM_TOKEN


# Create your views here.


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def verify(request):
    if request.method == 'PATCH':
        verification_code = request.data.get("verification_code")
        if not verification_code:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"verification_code": "wrong code"})
        tg_user = TgUser.objects.filter(verification_code=verification_code).first()
        if not tg_user:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"user": "no tguser"})
        tg_user.user_id = request.user.id
        tg_user.save()
        tg_client = TgClient(TELEGRAM_TOKEN)
        tg_client.send_message(chat_id=tg_user.telegram_chat_id, text="Успешная верификация!")
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST, data={"method": "wrong method"})
