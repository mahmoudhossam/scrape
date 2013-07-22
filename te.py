#!/usr/bin/env python
import requests
import sys
from furl import furl
from bs4 import BeautifulSoup as bs

def get_form_url():
    r = requests.get('http://billing.telecomegypt.com.eg')
    return r.url

def make_bill_url(url):
    f = furl(url)
    f.path.segments.pop()
    f.path.segments.append('customer_bill_status.aspx')
    return str(f)

def get_bill_page(url, area_code, tel_no):
    data = {
        "LoginSource": "Tel",
        "LoginSourceRadio": "Tel",
        "AreaCode": area_code,
        "TelNo": tel_no}
    args = {
        "New": 1,
        "From": "TelNo"}
    r = requests.post(url, data=data, params=args)
    r.encoding = 'utf-8'
    return r.content

def get_amount(page):
    soup = bs(page)
    table = soup.find_all('table', class_='tableBorder')[6]
    return table.find_all('font', class_='Values')[-1:][0]('b')[0].string

def main():
    tel_no = sys.argv[1]
    form_url = get_form_url()
    url = make_bill_url(form_url)
    p = get_bill_page(url, 02, tel_no)
    print(get_amount(p))

if __name__ == '__main__':
    main()

