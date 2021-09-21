import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()
from datacenter.models import Schoolkid, Mark, Lesson, Commendation, Chastisement, Subject
import random
import argparse


commendations = ['Молодец!', 'Отлично!', 'Хорошо!', 'Гораздо лучше, чем я ожидал!', 
                 'Ты меня приятно удивил!', 'Великолепно!', 'Прекрасно!', 'Ты меня очень обрадовал!', 
                 'Именно этого я давно ждал от тебя!', 'Сказано здорово – просто и ясно!', 
                 'Ты, как всегда, точен!', 'Очень хороший ответ!', 'Талантливо!',
                 'Ты сегодня прыгнул выше головы!', 'Я поражен!', 'Уже существенно лучше!', 'Потрясающе!',
                 'Замечательно!', 'Прекрасное начало!', 'Так держать!', 'Ты на верном пути!', 'Здорово!',
                 'Это как раз то, что нужно!', 'Я тобой горжусь!', 'С каждым разом у тебя получается всё лучше!',
                 'Мы с тобой не зря поработали!', 'Я вижу, как ты стараешься!', 'Ты растешь над собой!',
                 'Ты многое сделал, я это вижу!', 'Теперь у тебя точно все получится!']


def get_child(schoolkid):
    child = Schoolkid.objects.get(full_name__contains=schoolkid, year_of_study=6, group_letter='А')
    return child


def fix_marks(schoolkid):
    child = get_child(schoolkid)
    marks = Mark.objects.filter(schoolkid=child, points__lt=4)
    for mark in marks:
        mark.points = 5
        mark.save()


def remove_chastisements(schoolkid):
    child = get_child(schoolkid)
    notes = Chastisement.objects.filter(schoolkid=child)
    notes.delete()


def create_commendation(schoolkid, subject):
    child = get_child(schoolkid)
    text = random.choice(commendations)
    lesson = Lesson.objects.filter(year_of_study=6, group_letter='А', subject__title=subject).order_by('?').first()
    Commendation.objects.create(text=text, created=lesson.date, schoolkid=child, subject=lesson.subject, teacher=lesson.teacher)


def main():
    parser = argparse.ArgumentParser(description='Improve rating of student')
    parser.add_argument('surname', help='Введите фамилию ученика')
    parser.add_argument('subject', help='Введите название предмета')
    args = parser.parse_args()
    schoolkid = args.surname.title()
    subject = args.subject.title()


    try:
        get_child(schoolkid)
        Subject.objects.get(title=subject, year_of_study=6)
        fix_marks(schoolkid)
        remove_chastisements(schoolkid)
        create_commendation(schoolkid, subject)
    except Schoolkid.DoesNotExist:
        exit('Неправильно введена фамилия, перезапустите программу и попробуйте еще раз')
    except Subject.DoesNotExist:
        exit('Неправильно введено название предмета, перезапустите программу и попробуйте еще раз')
    except Schoolkid.MultipleObjectsReturned:
        exit('Таких учеников несколько, уточните фамилию и попробуйте еще раз')


if __name__ == '__main__':
    main()

