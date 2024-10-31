
import os 
from django.core.management.base import BaseCommand
from fuel_app.models import Station


class Command(BaseCommand):
    help = "Populate districts from StationDistrict.txt"

    def handle(self, *args, **kwargs):
        file_path = os.path.join("data", "StationDistrict.txt")
        with open(file_path, "r", encoding="utf-8") as file:
            districts = file.readlines()
            for district in districts:
                Station.objects.get_or_create(city=district.strip())
            self.stdout.write(self.style.SUCCESS("Districts populated successfully"))
