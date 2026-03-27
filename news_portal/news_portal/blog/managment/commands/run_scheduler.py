import logging
from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from news.models import Article, Subscriber  # модели статей и подписчиков
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone

logger = logging.getLogger(__name__)

def send_new_articles_notifications():
    """
    Отправляет уведомления подписчикам о новых статьях, опубликованных за последний час.
    """
    # Получаем время час назад
    one_hour_ago = timezone.now() - timezone.timedelta(hours=1)

    # Находим новые статьи за последний час
    new_articles = Article.objects.filter(
        created_at__gte=one_hour_ago
    ).order_by('-created_at')

    if not new_articles.exists():
        logger.info("Новых статей за последний час нет.")
        return

    logger.info(f"Найдены новые статьи: {new_articles.count()} штук")

    # Получаем активных подписчиков
    subscribers = Subscriber.objects.filter(is_active=True)
    emails = [s.email for s in subcribers]

    if not emails:
        logger.info("Нет активных подписчиков.")
        return

    # Отправляем уведомления для каждой новой статьи
    for article in new_articles:
        # Рендерим HTML‑шаблон письма
        html_message = render_to_string('news/email/new_article.html', {
            'article': article,
            'unsubscribe_url': f"{settings.BASE_URL}/unsubscribe/"
        })

        try:
            sent_count = send_mail(
                subject=f"Новая статья: {article.title}",
                message=f"Заголовок: {article.title}\n\n{article.content[:200]}...\n\nЧитать полностью: {settings.BASE_URL}/article/{article.id}/",
                from_email=settings.NEWS_LETTER_FROM_EMAIL,
                recipient_list=emails,
                html_message=html_message,
                fail_silently=False,
            )
            logger.info(f"Отправлено {sent_count} писем для статьи '{article.title}'")
        except Exception as e:
            logger.error(f"Ошибка отправки для статьи '{article.title}': {e}")

def delete_old_job_executions(max_age=604_800):
    """Удаляет старые записи о выполнении задач старше max_age секунд."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Запускает планировщик задач для рассылки уведомлений о новых статьях"

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # Добавляем задачу рассылки уведомлений — каждые 30 минут
        scheduler.add_job(
            send_new_articles_notifications,
            trigger=CronTrigger(minute="*/30"),  # каждые 30 минут
            id="send_article_notifications",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Добавлена задача рассылки уведомлений о новых статьях.")

        # Добавляем задачу очистки старых записей — раз в неделю по понедельникам в 00:00
        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Добавлена еженедельная задача очистки старых записей.")

        try:
            logger.info("Запуск планировщика...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Остановка планировщика...")
            scheduler.shutdown()
            logger.info("Планировщик успешно остановлен!")