from django.db import models, transaction
from django.contrib.auth.models import User


class YearGroup(models.Model):
    class Meta:
        verbose_name = 'Поток'
        verbose_name_plural = 'Потоки'

    name = models.CharField('Название', max_length=32)
    studying_year = models.PositiveSmallIntegerField('Учебный год')
    is_main = models.BooleanField('Сделать основным', default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.is_main:
            return super(YearGroup, self).save(*args, **kwargs)
        with transaction.atomic():
            YearGroup.objects.filter(is_main=True).update(is_main=False)
            return super(YearGroup, self).save(*args, **kwargs)


class Project(models.Model):
    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    name = models.CharField('Название проекта', max_length=128)
    github_slug = models.CharField('Репозиторий', max_length=128)  # e.g. 'apellpro/vvpd-project'

    year_group = models.ForeignKey('YearGroup', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Student(models.Model):
    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'

    firstname = models.CharField('Имя', max_length=32)
    surname = models.CharField('Фамилия', max_length=32)
    patronymic = models.CharField('Отчество', max_length=32, blank=True)
    education_group = models.CharField('Группа студента', max_length=32)
    education_type = models.CharField('Форма обучения', max_length=32)
    github_username = models.CharField('Имя пользователя GitHub', max_length=32)
    vk_uid = models.CharField('ID пользователя VK', max_length=32)
    is_leader = models.BooleanField('Сделать лидером команды')

    project = models.ForeignKey('Project', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.surname} {self.firstname} {self.patronymic} ' \
               f'{"★" if self.is_leader else ""}'

    def save(self, *args, **kwargs):
        if not self.is_leader:
            return super(Student, self).save(*args, **kwargs)
        with transaction.atomic():
            Student.objects.filter(
                project=self.project, is_leader=True
            ).update(is_leader=False)
            return super(Student, self).save(*args, **kwargs)


class Tag(models.Model):
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    text = models.CharField('Текст тега', max_length=32)
    background_color = models.CharField('Цвет фона', max_length=7)
    text_color = models.CharField('Цвет текста', max_length=7)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    projects = models.ManyToManyField(Project)

    def __str__(self):
        return self.text
