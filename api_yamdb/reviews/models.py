from api.validators import my_year_validator
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import CustomUser
from django.core.validators import MaxValueValidator, MinValueValidator
from reviews.validators import validate_year

<<<<<<< HEAD
User = get_user_model()


class Category(models.Model):
    """Модель категорий"""

    name = models.CharField(
        verbose_name='Категория',
        max_length=100
    )
    slug = models.SlugField(
        verbose_name='Ссылка',
        max_length=30,
        unique=True
    )

    class Meta:
        ordering = ['id', ]
        verbose_name_plural = 'Категории'
        verbose_name = 'Категория'
=======

class Category(models.Model):
    name = models.CharField(
        verbose_name='Категория',
        help_text='Название категории',
        max_length=150,
        unique=True
    )
    slug = models.SlugField(
        unique=True
    )
>>>>>>> origin/developreviews

    def __str__(self):
        return self.name

<<<<<<< HEAD

class Genre(models.Model):
    """Модель жанров"""

    name = models.CharField(
        max_length=50,
        verbose_name='Жанр'
    )
    slug = models.SlugField(
        unique=True,
        max_length=30,
        verbose_name='Ссылка'
    )

    class Meta:
        ordering = ['id', ]
        verbose_name_plural = 'Жанры'
        verbose_name = 'Жанр'
=======
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Жанр',
        help_text='Название жанра',
        max_length=150,
        unique=True
    )
    slug = models.SlugField(
        unique=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)
>>>>>>> origin/developreviews


class Title(models.Model):
    name = models.CharField(
<<<<<<< HEAD
        verbose_name='Произведение',
        max_length=100
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='Год выпуска',
        null=True,
        blank=True,
        validators=[my_year_validator, ]
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True,
        blank=True,
        verbose_name='Категория'
    )
    description = models.TextField()
    genre = models.ManyToManyField(
        Genre,
        through='TitleGenre'
    )

    class Meta:
        ordering = ['id', ]
        verbose_name_plural = 'Произведения'
        verbose_name = 'Произведение'
=======
        verbose_name='Наименование',
        help_text='Наименование произведения',
        max_length=500
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        help_text='Жанр произведения',
        related_name='titles',
        blank=True,
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        help_text='Категория выбранного произведения',
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True
    )
    year = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        db_index=True,
        validators=(validate_year,),
        verbose_name='Дата публикации'
    )
    description = models.CharField(
        verbose_name='Описание',
        help_text='Описание произведения',
        max_length=200,
        blank=True,
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)
>>>>>>> origin/developreviews

    def __str__(self):
        return self.name


<<<<<<< HEAD
class TitleGenre(models.Model):
    """Модель жанров произведений"""

    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE
    )


class Review(models.Model):
    """Модель отзыва"""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации отзыва',
        auto_now_add=True,
        db_index=True
    )
    score = models.IntegerField(
        validators=[
            MinValueValidator(1, 'Минимальная оценка - 1'),
            MaxValueValidator(10, 'Максимальная оценка - 10')
        ]
    )

    class Meta:
        ordering = ['pub_date', ]
=======
class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        help_text='Произведение к которому относится отзыв',
        related_name='review',
        verbose_name='Произведение'
    )
    score = models.IntegerField(
        validators=[
            MaxValueValidator(10, 'Максимальная оценка - 10'),
            MinValueValidator(1, 'Минимальная оценка - 1')
        ],
        verbose_name='Оценка произведения',
    )
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    text = models.TextField(
        help_text='Текст нового отзывы',
        verbose_name='Текст отзыва'
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ('score',)
>>>>>>> origin/developreviews
        constraints = (
            models.UniqueConstraint(
                fields=('title', 'author'),
                name='uniq_author',
            ),
        )

    def __str__(self):
<<<<<<< HEAD
        return self.text


class Comment(models.Model):
    """Модель комментария"""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации комментария',
        auto_now_add=True,
        db_index=True
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
=======
        return self.text[:15]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        help_text='Произведение к которому относится коментарий',
        related_name='comments',
        verbose_name='Произведение'
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
        help_text='Автор который оставил коментарий',
    )
    text = models.TextField(
        help_text='Текст нового коментария',
        verbose_name='Коментарий'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        help_text='Дата добавления нового коментария',
        verbose_name='Дата'
    )

    class Meta:
        ordering = ('pub_date',)

    def __str__(self):
        return self.text[:15]
>>>>>>> origin/developreviews
