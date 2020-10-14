from django.core.management.base import BaseCommand
import os

class Command(BaseCommand):
    help = 'Renames a Django project'
    def add_arguments(self, parser):
        parser.add_argument('old_project_name', type=str)
        parser.add_argument('new_project_name', type=str, help='The new Django project name')
    def handle(self, *args, **options):
        new_project_name = options['new_project_name']
        old_project_name = options['old_project_name']
        files_to_rename = [f'{old_project_name}/setting/base.py', f'{old_project_name}/wsgi.py', 'manage.py']
        # folder_to_rename = old_project_name
        for f in files_to_rename:
            with open(f, 'r') as file:
                filedata = file.read()

            filedata = filedata.replace(old_project_name, new_project_name)

            with open(f, 'w') as file:
                file.write(filedata)

        os.rename(old_project_name, new_project_name)
        # print('name changed')
        self.stdout.write(self.style.SUCCESS('Project has been renamed to %s' % new_project_name))