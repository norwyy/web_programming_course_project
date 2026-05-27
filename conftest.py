# Корневой conftest: гарантирует загрузку Django до сбора тестов (для discovery в VS Code)
import os
import sys

# Добавляем корень проекта в path, если его ещё нет
_root = os.path.dirname(os.path.abspath(__file__))
if _root not in sys.path:
    sys.path.insert(0, _root)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

import django
django.setup()
