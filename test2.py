import re
from util import *


text = "Aku ingin memakan pisang 100 biji 200 12/22/2000 20 Mei 2020 minggu senin SelAsa 05:06 WIT 20:07 WIB"
pattern = re.compile(r"\(?\d{1,2}(\/|-)\d{1,2}((\/|-)\d{4})?\)?")
pattern2 = re.compile(r"\d{1,2} (?i)(januari|februari|maret|april|mei|juni|juli|agustus|september|oktober|november|desember|jan|feb|mar|apr|mei|jun|jul|agu|sep|okt|nov|des)( \d{4})?")
pattern3 = re.compile(r"(?i)(senin|selasa|rabu|kamis|jumat|sabtu|minggu)")
pattern4 = re.compile(r"\d{1,2}(:|\.)\d{2}[^0-9]([A-Z]+)?")

iter = re.finditer(pattern4, text)
list_index = [m.span() for m in iter]
print(list_index)
print(text[list_index[0][0]:list_index[0][1]])   # cara cari

print(check_date_time(text,0))