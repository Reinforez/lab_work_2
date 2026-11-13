Файлы исправлений рассчитаны на исходный проект FoodBook из этого архива.

Применение из корня проекта:
  git apply patches/fix_idor.diff
  git apply patches/fix_xss.diff

После применения замените catalog/tests.py файлом tests_after_patch.py из каталога patches.
Сам сайт в основном архиве оставлен с неисправленными демонстрационными маршрутами.
