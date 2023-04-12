from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('music_app_apis', '0009_alter_allsongs_song_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='allsongs',
            name='song_id',
        ),
        migrations.RenameField(
            model_name='allsongs',
            old_name='song_id_new',
            new_name='song_id',
        ),
    ]
