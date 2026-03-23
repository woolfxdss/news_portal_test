from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Subscriber, Post


def send_new_post_notification(Post):
    """
    Отправляет уведомление о новой статье всем подписчикам
    """
    subscribers = Subscriber.objects.filter(is_active=True)
    emails = [s.email for s in subscribers]

    if not emails:
        return 0

    # Рендерим HTML‑шаблон письма
    html_message = render_to_string('news/email/new_post.html', {
        'Post': Post,
        'unsubscribe_url': 'http://yourdomain.com/unsubscribe/'  # замените на реальный URL
    })

    # Отправляем письма
    sent_count = send_mail(
        subject=settings.NEWS_LETTER_SUBJECT,
        message=f'Новая статья: {Post.title}\n\n{Post.content[:200]}...\n\nЧитать полностью: http://yourdomain.com/post/{Post.id}',
        from_email=settings.NEWS_LETTER_FROM_EMAIL,
        recipient_list=emails,
        html_message=html_message,
        fail_silently=False,
    )

    return sent_count
