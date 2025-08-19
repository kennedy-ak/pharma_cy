import csv
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from app.models import Drug
from decimal import Decimal, InvalidOperation


class Command(BaseCommand):
    help = 'Import drugs from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
        
        try:
            with open(csv_file_path, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                
                imported_count = 0
                skipped_count = 0
                
                for row in csv_reader:
                    try:
                        # Extract data from CSV row
                        name = row['name'].strip()
                        description = row['description'].strip() if row['description'] else ''
                        price = Decimal(str(row['price']))
                        stock_quantity = int(row['stock_quantity'])
                        
                        # Check if drug already exists
                        existing_drug = Drug.objects.filter(name=name).first()
                        
                        if existing_drug:
                            self.stdout.write(
                                self.style.WARNING(f'Drug "{name}" already exists. Skipping.')
                            )
                            skipped_count += 1
                            continue
                        
                        # Create new drug instance
                        drug = Drug(
                            name=name,
                            description=description,
                            price=price,
                            stock_quantity=stock_quantity,
                            minimum_stock_level=1,  # Default value
                            created_at=timezone.now(),  # Use today's datetime
                            updated_at=timezone.now()   # Use today's datetime
                        )
                        
                        drug.save()
                        imported_count += 1
                        
                        self.stdout.write(
                            self.style.SUCCESS(f'Successfully imported: {name}')
                        )
                        
                    except (ValueError, InvalidOperation, KeyError) as e:
                        self.stdout.write(
                            self.style.ERROR(f'Error processing row {csv_reader.line_num}: {e}')
                        )
                        skipped_count += 1
                        continue
                
                # Summary
                self.stdout.write(
                    self.style.SUCCESS(
                        f'\nImport completed!\n'
                        f'Successfully imported: {imported_count} drugs\n'
                        f'Skipped: {skipped_count} drugs'
                    )
                )
                
        except FileNotFoundError:
            raise CommandError(f'CSV file "{csv_file_path}" not found.')
        except Exception as e:
            raise CommandError(f'Error reading CSV file: {e}')