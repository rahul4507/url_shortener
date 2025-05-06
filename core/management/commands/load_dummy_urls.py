# myapp/management/commands/load_dummy_urls.py
import random
import string

from django.core.management.base import BaseCommand
from django.db import IntegrityError, transaction
from django.utils import timezone

from core.models import URL  # ← replace with your actual app name


class Command(BaseCommand):
    help = "Bulk-insert 1,000,000 dummy URL records with random 6-char shortcodes."

    BASE_URL = "https://music.youtube.com/watch?v=rK2d3wwb63M&list=RDAMVMm87B0ulgN64"
    TOTAL_RECORDS = 1_000_000
    BATCH_SIZE = 10_000
    CODE_LENGTH = 6
    CHARSET = string.ascii_letters + string.digits

    def generate_batch_codes(self, existing_codes, batch_size):
        """
        Yield a list of `batch_size` new, unique codes not in existing_codes.
        """
        new_codes = set()
        while len(new_codes) < batch_size:
            code = "".join(random.choices(self.CHARSET, k=self.CODE_LENGTH))
            if code not in existing_codes and code not in new_codes:
                new_codes.add(code)
        return list(new_codes)

    def handle(self, *args, **options):
        self.stdout.write("Starting bulk insert of URL records…")
        now = timezone.now()

        # Keep track of all codes generated so far (to avoid duplicates)
        seen_codes = set()

        for offset in range(0, self.TOTAL_RECORDS, self.BATCH_SIZE):
            batch_size = min(self.BATCH_SIZE, self.TOTAL_RECORDS - offset)
            codes = self.generate_batch_codes(seen_codes, batch_size)
            seen_codes.update(codes)

            objs = [
                URL(
                    original_url=self.BASE_URL,
                    short_code=code,
                    created_at=now,
                    updated_at=now,
                )
                for code in codes
            ]

            # Wrap in a transaction for integrity; bulk_create is still one SQL per batch
            with transaction.atomic():
                URL.objects.bulk_create(objs, batch_size)

            self.stdout.write(f"  • Inserted {offset + batch_size:,} / {self.TOTAL_RECORDS:,}")

        self.stdout.write(self.style.SUCCESS("✅ Finished inserting 1,000,000 URLs."))
