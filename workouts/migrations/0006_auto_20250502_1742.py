# workouts/migrations/0006_auto_20250502_1742.py

from django.db import migrations
from django.utils.text import slugify

def fill_slugs(apps, schema_editor):
    Workout = apps.get_model('workouts', 'Workout')
    for w in Workout.objects.filter(slug__isnull=True):
        w.slug = slugify(w.title)
        w.save()

class Migration(migrations.Migration):

    dependencies = [
        # Замените '0005_auto_20250501_1105' на имя вашего предыдущего файла миграции
        ('workouts', '0005_alter_groupworkout_max_participants_and_more'),
    ]

    operations = [
        migrations.RunPython(fill_slugs, reverse_code=migrations.RunPython.noop),
    ]
