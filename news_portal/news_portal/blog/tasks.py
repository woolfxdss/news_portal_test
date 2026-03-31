from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Subscriber, News

@shared_task
def send_new_news_notification(news_id):
    """
    Асинхронная задача для отправки уведомлений о новой новости подписчикам
    """
    try:
        news = News.objects.get(id=news_id)
        subscribers = Subscriber.objects.filter(is_active=True)
        emails = [s.email for s in subscribers]

        if not emails:
            return 0

        # Рендерим HTML‑шаблон письма
        html_message = render_to_string('news/email/new_news.html', {
            'news': news,
            'unsubscribe_url': 'http://yourdomain.com/unsubscribe/'  # замените на реальный URL
        })

        # Отправляем письма
        sent_count = send_mail(
            subject=f'Новая новость: {news.title}',
            message=f'Новая новость: {news.title}\n\n{news.content[:200]}...\n\nЧитать полностью: http://yourdomain.com/news/{news.id}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=emails,
            html_message=html_message,
            fail_silently=False,
        )

        return sent_count
    except News.DoesNotExist:
        return 0