from django.shortcuts import render, render_to_response
from django.http import JsonResponse, HttpResponseRedirect
import excel.models as common
from django.http import HttpResponse
import requests
import json
import yaml
import pandas as pd
from django import forms
from django.conf import settings
from django.core.files.storage import FileSystemStorage
# Create your views here.
ip = common.url()
header = common.header()
params=common.params()
data=common.data()
f = requests.Session()
r = f.post(ip, params=params, headers=header, data=json.dumps(data), verify=False)
books = r.json()
#books_list = {'books': books}

def index(request):
    return render(request, 'excel/index.html')

def excel(request):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="PythonExport.xlsx"'
    writer = pd.ExcelWriter(response, engine='xlsxwriter')
    dff = pd.DataFrame(books['DATA'])
    dff.to_excel(writer, 'Sheet1')
    writer.save()
    return response

def emp(request):
    if request.method == 'GET':
        response = r.content.decode("utf-8")
        return HttpResponse(response)

def excelfilter(request):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="filter.xlsx"'
    filter_data = yaml.load((request.GET['Main']))
    writer = pd.ExcelWriter(response, engine='xlsxwriter')
    dff = pd.DataFrame(filter_data)
    dff.to_excel(writer,header=False,startcol=0,startrow=5,index=False)
    worksheet = writer.sheets['Sheet1']
    worksheet.merge_range('C3:E3','Vsolv Summary')
    worksheet.set_column('A:F',20)
    # worksheet.write_string(3, 3, 'Vsolv Summary')
    writer.save()
    return response


def upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="filter.xlsx"'
        writer = pd.ExcelWriter(response, engine='xlsxwriter')
        df = pd.read_excel(myfile, sheetname='Sheet1')
        dff = df.filter(["customer_name", "employee_name", "fetsoutstanding_status"])
        dff.to_excel(writer, index=False)
        worksheet = writer.sheets['Sheet1']
        worksheet.set_column('A:F', 20)
        writer.save()
        return response
    return render(request, 'excel/upload.html')


def upload_file(request):
    if len(request.FILES) !=0:
        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            for count, x in enumerate(request.FILES.getlist("myfile")):
                def process(f):
                    for chunk in f.chunks():
                        filename = fs.save(myfile.name, myfile)

                process(x)
            return HttpResponseRedirect("/excel/")
    else:
        return HttpResponseRedirect("/excel/")
        # uploaded_file_url = fs.url(filename)
        # return render(request, 'excel/index.html', {
        #     'uploaded_file_url': uploaded_file_url
        # })
    # return render(request, 'excel/index.html')

