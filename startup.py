import sys
from django.core.management import execute_from_command_line

def run():
    try:
        execute_from_command_line(["manage.py", "migrate", "--noinput"])
    except Exception as e:
        print("Migration error:", e)
