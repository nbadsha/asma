# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 13:00:56 2022

@author: Nayeem191323
"""
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 11:57:17 2022

@author: Nayeem191323
"""

import re


# str_ = """13/02/2020 - present
# 6/05/2018 – 31/05/2019
# Aug 2021 - Present
# July 2017 - July 2019
# MAR2021 – PRESENT
# FEB2016-MAR2021
# 22nd July’19 - Present
# 1 Jun'18 - Present
# 1 Jun'18 - 20 Jul'18
# september 2021
# Dec 2019-Present
# Sep 2018-Dec 2019
# Mar 2019 - Present
# Nov 2021
# Feb 2016 to Nov 2021"""


MONTH = r"((JANUARY|january|January|JAN|jan|Jan)|(FEBRUARY|february|February|FEB|feb|Feb)|(MARCH|march|March|MAR|mar|Mar)|(APRIL|april|April|APR|apr|Apr)|(MAY|may|May|MAY|may|May)|(JUNE|june|June|JUN|jun|Jun)|(JULY|july|July|JUL|jul|Jul)|(AUGUST|august|August|AUG|aug|Aug)|(SEPTEMBER|september|September|SEP|sep|Sep)|(OCTOBER|october|October|OCT|oct|Oct)|(NOVEMBER|november|November|NOV|nov|Nov)|(DECEMBER|december|December|DEC|dec|Dec))"

# Aug 2021
gen_date_1 = r"("+MONTH+"\s*\d{2,4})"
# Jun'18 or July’19
gen_date_2 = f"{MONTH}[’|']\d{'{2}'}"
# present
prsnt = r"(Present|present|PRESENT|Current|current)"

# Match 13/02/2020 - Present
date_ptrn_1 = f"((0?[1-9]{'{1,2}'})(\/|\-|\.|\s*)(\d{'{1,2}'})(\/|\-|\.|\s*)(\d{'{2,4}'})\s*[-|–|']{'{1}'}\s*{prsnt})"

# Match 6/05/2018 – 31/05/2019
date_ptrn_2 = r"((0?[1-9]{1,2})(\/|\-|\.|\s*)(\d{1,2})(\/|\-|\.|\s*)(\d{2,4})\s*[-|–|']{1}\s*(0?[1-9]{1,2})(\/|\-|\.|\s*)(\d{1,2})(\/|\-|\.|\s*)(\d{2,4}))"

# Aug 2021 - Present
date_ptrn_3 = f"({gen_date_1}(\s*[-|–|']\s*{prsnt}))"

# July 2017 - July 2019 or July 2017 to July 2019
date_ptrn_4 = f"({gen_date_1}\s*([-|–|'|-|]|(to)){'{1}'}\s*{gen_date_1})"

# MAR2021 – PRESENT
date_ptrn_5 = f"({MONTH}\d+\s*[-|–|'|-]{'{1}'}\s*{prsnt})"

# FEB2016-MAR2021
date_ptrn_6 = f"({MONTH}\d+[-|–|'|-]{'{1}'}{MONTH}\d+)"

# 22nd July’19 - Present
date_ptrn_7 = f"({gen_date_2}\s*[-|–|'|-]\s*{prsnt})"

# 1 Jun'18 - 20 Jul'18
date_ptrn_8 = f"(\d+\s*{gen_date_2}\s*[-|–|'|-]\s*\d+\s*{gen_date_2})"

#  September 2021
date_ptrn_9 = f"({MONTH}\s*\d+)"

# Dec'17- till Date
date_ptrn_10 = f"({gen_date_2}\s*[-|–|'|-]\s*(till Date|till date))"

# June'15 - Oct'17
date_ptrn_11 = f"({gen_date_2}\s*[-|–|'|-]\s*{gen_date_2})"


ptrn = f"{date_ptrn_1}|{date_ptrn_2}|{date_ptrn_3}|{date_ptrn_3}|{date_ptrn_4}|\
    {date_ptrn_5}|{date_ptrn_6}|{date_ptrn_7}|{date_ptrn_8}|{date_ptrn_9}|{date_ptrn_10}|{date_ptrn_11}"

def match_dates(doc_text):
    return [x[0] for x in [tuple(comp for comp in a if comp) \
            for a in re.findall(ptrn, doc_text)]]
        
if __name__ == '__main__':
    date_str = """Dec'17- till Date
    June'15 - Oct'17"""
    
    print(match_dates(date_str))
    re.findall(ptrn, date_str)


