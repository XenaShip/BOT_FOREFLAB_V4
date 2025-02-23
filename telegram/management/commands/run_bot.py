import asyncio
from django.core.management.base import BaseCommand
from telegram.bot import main

class Command(BaseCommand):
    help = "Запускает Telegram-бота"

    def handle(self, *args, **options):
        self.stdout.write("Запуск Telegram-бота...")
        asyncio.run(main())