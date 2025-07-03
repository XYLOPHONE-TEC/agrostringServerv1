# import_coeffs.py

from django.core.management.base import BaseCommand
from django.conf import settings
from carbon.models import Coefficient
import os
import csv

class Command(BaseCommand):
    help = 'Import natural_elements.csv into Coefficient model'

    def handle(self, *args, **kwargs):
        path = os.path.join(settings.BASE_DIR, 'carbon', 'natural_elements.csv')
        if not os.path.exists(path):
            self.stderr.write(f'❌ File not found: {path}')
            return
        with open(path, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                Coefficient.objects.update_or_create(
                    element=row['element'],
                    defaults={'value': float(row['value'])}
                )
        self.stdout.write(self.style.SUCCESS('✅ Coefficients loaded successfully'))
