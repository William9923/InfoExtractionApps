"""
    Utility Function:
"""
import sys
import math
from datetime import date
from pprint import pprint
from copy import copy
from kmp import * 
from regex import * 
from bm import *
import re
from flask import Markup

def create_file(files):
    list_of_files = []
    if files is not None:
        for file in files:
            file_read = file.read()
            list_of_files.append({"text": file_read.decode('utf-8'), "filename": file.filename})
        list_of_files = divider(list_of_files)
    return list_of_files

# Buat cari date pertama buat default date
def check_first_date(paragraph): # get the first date on the whole paragrph of news
    return check_nearest_date(paragraph, 0)


def check_date_full_format(text,index_text):
    pattern =  r"\(?\d{1,2}(\/|-)\d{1,2}((\/|-)\d{4})?\)?"
    result = check_nearest(pattern,text,index_text)
    return result

def check_date_month(text,index_text):
    pattern =  re.compile(r"\d{1,2} (?i)(januari|februari|maret|april|mei|juni|juli|agustus|september|oktober|november|desember|jan|feb|mar|apr|mei|jun|jul|agu|sep|okt|nov|des)( \d{4})?")
    result = check_nearest(pattern,text,index_text)
    return result

def check_date_day(text,index_text):
    pattern = re.compile(r"(?i)(senin|selasa|rabu|kamis|jumat|sabtu|minggu)")
    result = check_nearest(pattern,text,index_text)
    return result

def check_date_time(text,index_text):
    pattern = re.compile(r"\d{1,2}(:|\.)\d{2}[^0-9]([A-Z]+)?")
    result = check_nearest(pattern,text,index_text)
    return result

def check_nearest(pattern,text,index_text):
    iter = re.finditer(pattern, text)
    list_index = [m.span() for m in iter]
    min_index_interval = sys.maxsize
    span_index = None
    for index in list_index:
        if (index[0] < index_text):
            diff = abs(index[1] - index_text)
        else :
            diff = abs(index[0] - index_text)

        if diff < min_index_interval:
                min_index_interval = diff 
                span_index = index
    if span_index is not None:
        return {"object" : text[span_index[0] : span_index[1]], "index" : span_index}
    return None


def check_nearest_date(text, index_text): # mirip kek cara di bawah aja, tp pake pattern buat date
    list_date_format = [] 
    if check_date_full_format(text, index_text) is not None :
        list_date_format.append(check_date_full_format(text, index_text))
    if check_date_month(text,index_text) is not None :
        list_date_format.append(check_date_month(text,index_text))
    if check_date_day(text,index_text) is not None:
        list_date_format.append(check_date_day(text,index_text))
    if check_date_time(text,index_text) is not None:
        list_date_format.append(check_date_time(text,index_text))
    
    date = []
    while len(list_date_format) > 0 :
        min_index = sys.maxsize
        cur_index = -1
        for i in range(len(list_date_format)):
            if list_date_format[i].get('index')[0] < min_index:
                min_index = list_date_format[i].get('index')[0]
                cur_index = i
        cur_date = list_date_format.pop(cur_index)

        if len(date) == 0 or cur_date.get('index')[0] - date[-1].get('index')[1] < 10:
            date.append(cur_date)
    return date


def check_nearest_digit(text, index_text):
    digit_pattern = re.compile(r" \d+[\.|,]?\d+ ")
    result = check_nearest(digit_pattern,text,index_text)
    if result is not None:
        result['object'] = result['object'].strip()
    return result

def divider(list_of_news):
    for news in list_of_news:
        news['text'] = news.get('text').strip()
        news['text'] = '. '.join(news.get('text').splitlines())
        news['text'] = news.get('text').split('. ')
        news['processed'] = copy(news['text'])
        for i in range(len(news['text'])):
            news['processed'][i] = preprocessing(news['text'][i])
    return list_of_news


def preprocessing(text):
    return Markup(text.strip().lower().replace('\n','')).striptags()


def create_answer(algo, keyword,list_of_files):
    list_of_answers = []
    list_of_processed_answer = []
    for news in list_of_files:
        list_of_answers.extend(get_text_match_pattern(algo, keyword, news))
    for answer in list_of_answers:
        list_of_processed_answer.append(process_output(answer))
    return list_of_processed_answer


def validate(keyword,algo, files):
    list_algo = ['kmp','bm','regex']
    check1 = len(keyword) > 0
    check2 = algo in list_algo
    check3 = len(files) > 0
    return check1 and check2 and check3

def get_text_match_pattern(algo, keyword, news):
    texts = news['processed']
    keyword_processed = keyword.lower()
    list_of_answer = []
    for i in range(len(texts)):
        if algo == 'kmp' :
            indexes = knuth_morris_prath(keyword_processed, texts[i])
        elif algo == 'bm' :
            indexes = boyer_moore(keyword_processed, texts[i])
        else :
            indexes = regex_function(keyword_processed, texts[i])

        if (len(indexes) > 0):
            for index in indexes:
                digit = check_nearest_digit(texts[i],index)
                list_of_answer.append(
                    {"keyword" : keyword, 
                        "text": news['text'][i], 
                        "digit" :  check_nearest_digit(texts[i],index) if digit is not None else {'index' : (-1,-1), 'object' : "No Digit Found"},
                        "date" : check_nearest_date(news['text'][i], index) if len(check_nearest_date(texts[i], index)) > 0 else check_first_date('. '.join(news['text'])), 
                        "index" : index,
                        "filename" : news['filename'],
                        "contains_date" : True if len(check_nearest_date(texts[i], index)) > 0 else False}
                    )
    return list_of_answer

def get_color(case):
    return {
        'date' : 'light-green',
        'key' : 'purple-text',
        'digit' : 'cyan-text'
    }.get(case)

def connect_date(date_list, index):
    pass 

def change_color(answer):
    # change the digit color:
    if answer['digit'] is not None:
        answer['text'] = Markup(answer['text'].replace(f" {answer['digit']['object']} ",f'<span class="{get_color("digit")}"> {answer["digit"]["object"]} </span>'))
    if answer["contains_date"]:
        for date in answer['date']:
            answer['text'] = Markup(re.sub(f' (?i){date["object"]} ',f'<span class="{get_color("date")}"> {date["object"]} </span>', answer['text']))
    answer['text'] = Markup(re.sub(f'(?i){answer["keyword"]}',f'<span class="{get_color("key")}">{answer["keyword"]}</span>', answer['text']))
    return answer


"""
    Adding the span class for output 
"""
def process_output(answer):
    answer = change_color(answer)
    return {
        "digit" : answer['digit'].get('object'),
        "text" : answer['text'],
        "date" : ' '.join([i.get('object') for i in answer['date']]),
        "filename" : answer['filename'].split('/')[1]
    }


