from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.db.utils import IntegrityError
from .models import CompareItemJT, CompareItemJD, CompareItem
import sys
import logging
sys.path.append('..')
from src.Compare import Compare

# Create your views here.


def compareView(request):
    return render(request, 'compare.html')


# def showJTView(request):
#     quered_jt = {CompareItemJT.objects.last()}
#     return render(request, 'show_compared_jt.html', {'quered_jt': quered_jt})
#
#
# def addTitle(request):
#     new_item = CompareItemJT(content=request.POST['content'])
#     code, title = compare_jt.process(new_item.content)
#     result = list(zip(code, title))
#     new_item.result_1, new_item.result_2, new_item.result_3 = result[0], result[1], result[2]
#     try:
#         new_item.save()
#     except IntegrityError as ie:
#         logging.exception(repr(ie)+' Duplicated entries')
#     except Exception as e:
#         logging.exception(repr(e) + ' Non Integrity Error')
#
#     return HttpResponseRedirect('/showTitle/')
#     # create a new todo all_items
#     # save
#     # redirect the browser to "/todo/"
#
# def addJD(request):
#     new_item = CompareItemJD(content=request.POST['content'])
#     code, description = compare_jd.process(new_item.content)
#     result = list(zip(code, description))
#     new_item.result_1, new_item.result_2, new_item.result_3 = result[0], result[1], result[2]
#     try:
#         new_item.save()
#     except IntegrityError as ie:
#         logging.exception(repr(ie)+' Duplicated entries')
#     except Exception as e:
#         logging.exception(repr(e) + ' Non Integrity Error')
#     return HttpResponseRedirect('/showJD/')
#
# def showJDView(request):
#     quered_jd = {CompareItemJD.objects.last()}
#     return render(request, 'show_compared_jd.html', {'quered_jd': quered_jd})
#
#
# def addTitleDescr(request):
#     new_item = CompareItemJT(title=request.POST['title'], description=request.POST['description'])
#     code, title = compare_jt.process(new_item.content)
#     result = list(zip(code, title))
#     new_item.result_1, new_item.result_2, new_item.result_3 = result[0], result[1], result[2]
#     try:
#         new_item.save()
#     except IntegrityError as ie:
#         logging.exception(repr(ie)+' Duplicated entries')
#     except Exception as e:
#         logging.exception(repr(e) + ' Non Integrity Error')
#
#     return HttpResponseRedirect('/showTitle/')
#     # create a new todo all_items
#     # save
#     # redirect the browser to "/todo/"


def showJTDView(request):
    quered_jt = {CompareItem.objects.last()}
    return render(request, 'show_compared_jt.html', {'quered_jt': quered_jt})


def addTitleDescription(request):
    new_item = CompareItem(title=request.POST['title'], description=request.POST['description'])
    if not new_item.description:
        compare_service = Compare(type='title')
        text = new_item.title
    elif not new_item.title:
        compare_service = Compare(type='description')
        text = new_item.description
    else:
        compare_service = Compare()
        text = new_item.title + '.' + new_item.description

    code, title, processed_text = compare_service.process(text)
    new_item.processed_text = processed_text
    result = list(zip(code, title))
    new_item.result_1, new_item.result_2, new_item.result_3 = result[0], result[1], result[2]
    try:
        new_item.save()
    except IntegrityError as ie:
        logging.exception(repr(ie)+' Duplicated entries')
    except Exception as e:
        logging.exception(repr(e) + ' Non Integrity Error')

    return HttpResponseRedirect('/show/')
