import random

from datacenter.models import (
    Schoolkid,
    Mark,
    Chastisement,
    Lesson,
    Commendation
) 

from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import MultipleObjectsReturned


def fix_marks(schoolkid):
    bad_marks = Mark.objects.filter(schoolkid=schoolkid, points__lt=4)
    return bad_marks.update(points=5)

 
def remove_chastisements(schoolkid):
    chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    return chastisements.delete()


def create_commendation(schoolkid_name, subject_title):
    commends = [
        'Сказано здорово - просто и ясно!', 'Очень хороший ответ!',
        'Талантливо!', 'Ты сегодня прыгнул выше головы!',
        'Я поражен!', 'Уже существенно лучше!', 'Потрясающе!',
        'Замечательно!', 'Прекрасное начало!', 'Так держать!',
        'Ты на верном пути!', 'Это как раз то, что нужно!',
        'Я тобой горжусь!', 'С каждым разом у тебя получается всё лучше!',
        'Мы с тобой не зря поработали!', 'Я вижу, как ты стараешься!',
        'Ты растешь над собой!', 'Ты многое сделал, я это вижу!',
        'Теперь у тебя точно все получится!'
    ]
    try:
        schoolkid = Schoolkid.objects.get(
            full_name__contains=schoolkid_name,
        )
    except (ObjectDoesNotExist, MultipleObjectsReturned) as error:
        print(f'Error: {error}')
        exit(1)
    lessons = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
        subject__title=subject_title
    )
    if not lessons.exists():
        print("Error: Wrong lesson's name or lesson does not exist")
        exit(1)
    random_lesson = lessons.order_by('?').first()
    commend = Commendation.objects.create(
        text = random.choice(commends),
        created = random_lesson.date,
        schoolkid = schoolkid,
        subject = random_lesson.subject,
        teacher = random_lesson.teacher
    )
    return commend


# scripts.create_commendation('Фролов Иван', 'Музыка')