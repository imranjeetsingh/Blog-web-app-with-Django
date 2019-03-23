import datetime
import re, math

from django.utils.html import strip_tags

def count_words(html_string):
    word_string = strip_tags(html_string)
    count = len(re.findall(r'\w+', word_string))
    return count

def get_read_time(html_string):
    count = count_words(html_string)
    read_time_min = math.ceil(count/200)
    # read_time_sec = 60*read_time_min
    # read_time = str(datetime.timedelta(seconds=read_time_sec))
    return read_time_min