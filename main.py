import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()
from datacenter.models import Schoolkid, Mark, Lesson, Commendation, Chastisement, Subject
import random
import argparse


def fix_marks(schoolkid):
    child = Schoolkid.objects.get(full_name__contains=schoolkid, year_of_study=6, group_letter='А')
    marks = Mark.objects.filter(schoolkid=child, points__lt=4)
    for mark in marks:
        mark.points = 5
        mark.save()

def remove_chastisements(schoolkid):
    child = Schoolkid.objects.get(full_name__contains=schoolkid, year_of_study=6, group_letter='А')
    notes = Chastisement.objects.filter(schoolkid=child)
    notes.delete()

commendations = ['Молодец!', 'Отлично!', 'Хорошо!', 'Гораздо лучше, чем я ожидал!', 'Ты меня приятно удивил!',
                 'Великолепно!', 'Прекрасно!', 'Ты меня очень обрадовал!', 'Именно этого я давно ждал от тебя!',
                 'Сказано здорово – просто и ясно!', 'Ты, как всегда, точен!', 'Очень хороший ответ!', 'Талантливо!',
                 'Ты сегодня прыгнул выше головы!', 'Я поражен!', 'Уже существенно лучше!', 'Потрясающе!',
                 'Замечательно!', 'Прекрасное начало!', 'Так держать!', 'Ты на верном пути!', 'Здорово!',
                 'Это как раз то, что нужно!', 'Я тобой горжусь!', 'С каждым разом у тебя получается всё лучше!',
                 'Мы с тобой не зря поработали!', 'Я вижу, как ты стараешься!', 'Ты растешь над собой!',
                 'Ты многое сделал, я это вижу!', 'Теперь у тебя точно все получится!']

def create_commendation(schoolkid, subject):
    child = Schoolkid.objects.get(full_name__contains=schoolkid, year_of_study=6, group_letter='А')
    text = random.choice(commendations)
    lesson = Lesson.objects.filter(year_of_study=6, group_letter='А', subject__title=subject)
    lesson = random.choice(lesson)
    Commendation.objects.create(text = text, created = lesson.date, schoolkid=child, subject = lesson.subject, teacher=lesson.teacher)


def main():
    parser = argparse.ArgumentParser(description='Improve rating of student')
    parser.add_argument('surname', help='Введите фамилию ученика')
    parser.add_argument('subject', help='Введите название предмета')
    args = parser.parse_args()
    schoolkid = args.surname.title()
    subject = args.subject.title()

    from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
    try:
        Schoolkid.objects.get(full_name__contains=schoolkid, year_of_study=6, group_letter='А')
        Subject.objects.get(title=subject, year_of_study=6)
        fix_marks(schoolkid)
        remove_chastisements(schoolkid)
        create_commendation(schoolkid, subject)
    except ObjectDoesNotExist:
        exit('Неправильно введены ФИО и/или название предмета, перезапустите программу и попробуйте еще раз')
    except MultipleObjectsReturned:
        exit('Уточните фамилию ученика')


if __name__ == '__main__':
    main()
