from celery import shared_task
from django.core.mail import send_mail

from comment.models import Comment
from order.models import Order
from .celery import app



@app.task
def send_order_confirmation_email(order_id):
    # Получите заказ по его ID или каким-либо другим способом
    order = Order.objects.get(id=order_id)

    # Отправьте письмо с подтверждением заказа
    subject = 'Подтверждение заказа'
    message = f'Спасибо за ваш заказ! Номер заказа: {order.id}'
    recipient_list = [order.user.email]
    send_mail(subject, message, 'noreply@example.com', recipient_list)

@app.task
def send_comment_notification_email(comment_id):
    # Получите комментарий по его ID или каким-либо другим способом
    comment = Comment.objects.get(id=comment_id)

    # Отправьте уведомление о комментарии по электронной почте
    subject = 'Уведомление о новом комментарии'
    message = f'Получен новый комментарий от пользователя {comment.user}: {comment.content}'
    recipient_list = [comment.user.email]
    send_mail(subject, message, 'noreply@example.com', recipient_list, fail_silently=False)