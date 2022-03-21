from django.db import models


class Project(models.Model):

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    name = models.CharField('Название проекта', max_length=30)
    github_link = models.CharField('Ссылка на GitHib проекта', max_length=300)
    check_statistic = models.FloatField('Статистика с момента последней проверки')
    new_commits_num = models.PositiveIntegerField('Количество новых коммитов')
    open_tasks_num = models.PositiveIntegerField('Количество открытых задач')
    tasks_in_progress_num = models.PositiveIntegerField('Количество задач в работе')
    closed_tasks_num = models.PositiveIntegerField('Количество закрытых задач')
    last_release_num = models.PositiveIntegerField('Номер последнего релиза', default='')
    rating = models.DecimalField('Рейтинг проекта', decimal_places=2, max_digits=2)
    week_lines_progress = models.IntegerField('Количество удалений и добавлений строк за неделю')

    def __str__(self):
        return self.name


class Student(models.Model):

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'

    project = models.OneToOneField(Project, on_delete=models.CASCADE)
    name = models.CharField('Имя студента', max_length=30)
    surname = models.CharField('Фамилия студента', max_length=60)
    patronymic = models.CharField('Отчество студента', max_length=60)
    is_team_lead = models.BooleanField(default=False)
    group = models.CharField('Группа студента', max_length=20)
    form_of_education = models.CharField('Форма обучения', max_length=40)
    vk_link = models.CharField('Ссылка на VK студента', max_length=300)
    github_link = models.CharField('Ссылка на GitHib студента', max_length=300)

    def __str__(self):
        return self.name


class YearGroup(models.Model):

    class Meta:
        verbose_name = 'Поток'
        verbose_name_plural = 'Потоки'

    name = models.CharField('Учебный год', max_length=30)
    studying_year = models.IntegerField('Учебный год')
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return self.name
