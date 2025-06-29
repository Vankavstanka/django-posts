import requests
from django.core.management.base import BaseCommand
from posts.models import Post

URL = "https://jsonplaceholder.typicode.com/posts"

class Command(BaseCommand):
    help = "Загружает demo-данные с JSONPlaceholder и сохраняет в БД"

    def handle(self, *args, **kwargs):
        self.stdout.write("Скачиваю данные...")
        resp = requests.get(URL, timeout=10)
        resp.raise_for_status()
        payload = resp.json()

        new_posts = []
        for entry in payload:
            if not Post.objects.filter(id=entry["id"]).exists():
                new_posts.append(Post(
                    id=entry["id"],
                    title=entry["title"],
                    body=entry["body"],
                    userId=entry["userId"],
                ))

        Post.objects.bulk_create(new_posts, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS(
            f"Добавлено {len(new_posts)} записей из {len(payload)}"
        ))
