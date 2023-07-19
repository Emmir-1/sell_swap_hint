from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify as django_slugify


class Category(models.Model):
    """
    Модель для категорий товаров.

    Аргументы:
    - slug (str): Уникальный идентификатор категории (поле SlugField).
    - name (str): Название категории (поле CharField).
    - parent (Category, optional): Родительская категория (ссылка на себя) (поле ForeignKey).

    Примечание:
    - Категория может иметь родительскую категорию или быть корневой.
    """
    slug = models.SlugField(max_length=50, primary_key=True)  # Уникальный идентификатор категории.
    name = models.CharField(max_length=50, unique=True)  # Название категории.
    parent = models.ForeignKey('self', on_delete=models.SET_NULL,
                               related_name='children', blank=True, null=True)  # Родительская категория.

    def __str__(self):
        """
        Возвращает строковое представление категории.

        Примечание:
        - Если категория имеет родительскую категорию, то возвращается строка "Родитель -> Название".
        - Если категория является корневой (не имеет родительской категории), то возвращается только название.
        """
        return f'{self.parent} -> {self.name}' if self.parent else f'{self.name}'

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'


@receiver(pre_save, sender=Category)
def category_slug_save(sender, instance, *args, **kwargs):
    """
    Обработчик сигнала pre_save для модели Category.

    Аргументы:
    - sender (Model): Модель, которая инициировала сигнал (Category).
    - instance (Category): Экземпляр объекта модели Category, который будет сохранен.

    Примечание:
    - Сигнал pre_save вызывается перед сохранением экземпляра модели Category в базу данных.
    - Метод генерирует уникальный идентификатор (slug) для категории, если его нет.
    """
    if not instance.slug:
        # Словарь для транслитерации русских символов в английские.
        alphabet = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z',
                    'и': 'i', 'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's',
                    'т': 't',
                    'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ы': 'i', 'э': 'e',
                    'ю': 'yu',
                    'я': 'ya'}

        # Генерируем slug на основе названия категории с транслитерацией.
        instance.slug = django_slugify(''.join(alphabet.get(w, w) for w in instance.name.lower()))

# from django.db import models
# from django.db.models.signals import pre_save
# from django.dispatch import receiver
# from django.template.defaultfilters import slugify as django_slugify
#
#
# class Category(models.Model):
#     slug = models.SlugField(max_length=50, primary_key=True)
#     name = models.CharField(max_length=50, unique=True)
#     parent = models.ForeignKey('self', on_delete=models.SET_NULL,
#                                related_name='children', blank=True, null=True)
#
#     def __str__(self):
#         return f'{self.parent} -> {self.name}' if self.parent else f'{self.name}'
#
#     # def get_children(self):
#     #     if self.parent:
#     #         return self.children.all()
#     #     return False
#
#     class Meta:
#         verbose_name = 'category'
#         verbose_name_plural = 'categories'
#
#
# @receiver(pre_save, sender=Category)
# def category_slug_save(sender, instance, *args, **kwargs):
#     # print('***************************************')
#     # print('SIGNAL IS WORKED!')
#     # print('***************************************')
#     if not instance.slug:
#         alphabet = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z',
#                     'и': 'i', 'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's',
#                     'т': 't',
#                     'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ы': 'i', 'э': 'e',
#                     'ю': 'yu',
#                     'я': 'ya'}
#
#         instance.slug = django_slugify(''.join(alphabet.get(w, w) for w in instance.name.lower()))
#
#         # instance.slug = slugify(instance.name)
