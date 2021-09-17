import os
import django
import random

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

from datacenter.models import Schoolkid, Mark, Lesson, Commendation, Chastisement, Subject

schoolkid = input("Введите ФИО ученика ")
schoolkid = schoolkid.title()

from django.core.exceptions import ObjectDoesNotExist
try:
    child = Schoolkid.objects.get(full_name__contains=schoolkid)
except ObjectDoesNotExist:
    print("Неправильно введены ФИО, перезапустите программу и попробуйте еще раз")
    exit()

subject = input("Введите название предмета ")
subject = subject.title()

try:
    lesson_subject = Subject.objects.get(title=subject, year_of_study = 6)
except ObjectDoesNotExist:
    print("Неправильно введено название предмета, перезапустите программу и попробуйте еще раз")
    exit()

def fix_marks(schoolkid):
    marks = Mark.objects.filter(schoolkid=child, points__lt=4)
    for mark in marks:
        mark.points = 5
        mark.save()
fix_marks(schoolkid)


def remove_chastisements(schoolkid):
    notes = Chastisement.objects.filter(schoolkid=child)
    notes.delete()
remove_chastisements(schoolkid)

commendations = ['Молодец!', 'Отлично!', 'Хорошо!', 'Гораздо лучше, чем я ожидал!', 'Ты меня приятно удивил!',
                 'Великолепно!', 'Прекрасно!', 'Ты меня очень обрадовал!', 'Именно этого я давно ждал от тебя!',
                 'Сказано здорово – просто и ясно!', 'Ты, как всегда, точен!', 'Очень хороший ответ!', 'Талантливо!',
                 'Ты сегодня прыгнул выше головы!', 'Я поражен!', 'Уже существенно лучше!', 'Потрясающе!',
                 'Замечательно!', 'Прекрасное начало!', 'Так держать!', 'Ты на верном пути!', 'Здорово!',
                 'Это как раз то, что нужно!', 'Я тобой горжусь!', 'С каждым разом у тебя получается всё лучше!',
                 'Мы с тобой не зря поработали!', 'Я вижу, как ты стараешься!', 'Ты растешь над собой!',
                 'Ты многое сделал, я это вижу!', 'Теперь у тебя точно все получится!']

def create_commendation(schoolkid, subject):
    text = random.choice(commendations)
    lesson = Lesson.objects.filter(year_of_study=6, group_letter='А', subject__title=subject).last()
    Commendation.objects.create(text = text, created = lesson.date, schoolkid=child, subject = lesson.subject, teacher=lesson.teacher)
create_commendation(schoolkid, subject)