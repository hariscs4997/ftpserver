from django.shortcuts import render
from ftplib import FTP
import os
from .models import Camera_One_Image, Camera_Two_Image, StateModel
import tempfile
from django.core import files
from datetime import datetime
from dateutil import parser


#Download functions
def download_file(filename,camera_one = True):
    #lf = tempfile.NamedTemporaryFile()
    #ftp.retrbinary("RETR " + filename, lf.write, 8*1024)
    if camera_one:
        c = Camera_One_Image()
    else:
        c = Camera_Two_Image()
    c.name = filename
    c_d = ftp.pwd().lstrip("/Kurpark/")
    im_url = "https://archiv.dominikketz.de/" + c_d + "/" + filename
    c.image_url = im_url
    cmd_str = "MDTM " + filename
    timestamp = ftp.voidcmd(cmd_str)[4:].strip()
    time = parser.parse(timestamp)
    n_time = time.strftime("%H:%M") 
    n_date = time.strftime("%d %m %Y")
    c.down_time = n_time
    c.down_date = n_date
    c.save()
    

ext = ('.jpg','.png','.jpeg')

ftp = FTP('home16953969.1and1-data.host','p6684723-timelapse','Wr7-k7z-Jox-DPy')
a1 = '/Kurpark/ac-cc-8e-7a-4b-0d/archive/'
a2 = '/Kurpark/ac-cc-8e-7a-4c-f5/archive/'


def start_operation(a,camera_one=True):
    state = StateModel.objects.latest('id')
    year_dirs = ftp.nlst(a)[2:]
    for ydir in year_dirs:
        print("Year Dir:",ydir)
        month_dirs = ftp.nlst(ydir)[2:]
        for mdir in month_dirs:
            print("Month Dir:",mdir)
            day_dirs = ftp.nlst(mdir)[2:]
            for ddir in day_dirs:
                print("Day Dir:",ddir)
                internal_dirs = ftp.nlst(ddir)[2:]
                for idir in internal_dirs:
                    print("Internal Dir:",idir)
                    ftp.cwd(idir)
                    listing = []
                    ftp.retrlines('LIST',listing.append)
                    for list in listing:
                        words = list.split(None,8)
                        filename = words[-1].lstrip()
                        if filename.endswith(ext):
                            if camera_one == True:
                                print("Downloading: ",filename)
                                download_file(filename)
                                state.camera_one = filename
                            else:
                                print("Downloading: ",filename)
                                download_file(filename,camera_one=False)
                                state.camera_two = filename
                            state.save()
    print("Completed")
    # print("Year Dirs Later: ",year_dirs_later)
    # print("Month Dirs Later:", month_dirs_later)
    # print("Day Dirs Later:", day_dirs_later)
    # print("Internal Dirs Later:", internal_dirs_later)




def regular_operation(a,fn,camera_one=True):
    state = StateModel.objects.latest('id')
    year_dirs = ftp.nlst(a)[2:]
    year_dirs.reverse()
    #use this counter to end the state saving process after executing one time
    cntr = 0
    for ydir in year_dirs:
        print("Reverse Year Dir:", ydir)
        month_dirs = ftp.nlst(ydir)[2:]
        month_dirs.reverse()
        for mdir in month_dirs:
            print("Reverse Month Dir:", mdir) 
            day_dirs = ftp.nlst(mdir)[2:]
            day_dirs.reverse()
            for ddir in day_dirs:
                print("Reverse Day Dir:", ddir)
                internal_dirs = ftp.nlst(ddir)[2:]
                internal_dirs.reverse()
                for idir in internal_dirs:
                    print("Reverse Internal Dir:",idir)
                    ftp.cwd(idir)
                    listing = []
                    ftp.retrlines('LIST',listing.append)
                    listing.reverse()
                    for list in listing:
                        words = list.split(None,8)
                        filename = words[-1].lstrip()
                        if filename.endswith(ext):
                            if filename == fn:
                                print("File already exists")
                                return "Out"
                            else:
                                if camera_one:
                                    print("Downloading: ",filename)
                                    download_file(filename)
                                    if cntr ==0:
                                        state.camera_one = filename
                                        cntr +=1
                                        state.save()
                                else:
                                    print("Downloading: ",filename)
                                    download_file(filename,camera_one=False)
                                    if cntr ==0:
                                        state.camera_two = filename
                                        cntr +=1
                                        state.save()
                                
                            #infile.write(filename + '\n')
    print("Reverse Complete")

def camera_two_get():
    s = StateModel.objects.latest('id')
    s_camera2 = s.camera_two
    if s_camera2 == 'empty':
        print("First Operation c2")
        start_operation(a2,camera_one=False)
    else:
        print("Regular Operation c2")
        regular_operation(a2,s_camera2,camera_one=False)
    print("Process completed.")

def main_process():
    state_filter = StateModel.objects.all()
    if len(state_filter) == 0:
        new_state = StateModel()
        new_state.save()
    s = StateModel.objects.latest('id')
    s_camera1 = s.camera_one 
    s_camera2 = s.camera_two 
    if s_camera1 == 'empty':
        print("First Operation c1")
        start_operation(a1)
    else:
        print("Regular Operation c1")
        regular_operation(a1,s_camera1)
    if s_camera2 == 'empty':
        print("First Operation c2")
        start_operation(a2,camera_one = False)
    else:
        print("Regular Operation c2")
        regular_operation(a2,s_camera2,camera_one = False)
    print("Process Completed.")

    



from django.http import HttpResponse
# Create your views here.


def handle_camera1(request):
    if request.method == 'POST':
        year = request.POST['up_year']
        month = request.POST['up_month']
        date = request.POST['up_date']
        if int(date) < 10:
            date = '0' + date
        if int(month) < 10:
            month = '0' + month
        search_filter = '{} {} {}'.format(date,month,year)
        images = Camera_One_Image.objects.filter(down_date = search_filter)
        return render(request,'camera1.html',{'images':images})
    now = datetime.now()
    query = now.strftime("%d %m %Y")
    images = Camera_One_Image.objects.filter(down_date = query)
    return render(request,'camera1.html',{'images':images})

def handle_camera2(request):
    if request.method == 'POST':
        year = request.POST['up_year']
        month = request.POST['up_month']
        date = request.POST['up_date']
        if int(date) < 10:
            date = '0' + date
        if int(month) < 10:
            month = '0' + month
        search_filter = '{} {} {}'.format(date,month,year)
        images = Camera_Two_Image.objects.filter(down_date = search_filter)
        return render(request,'camera2.html',{'images':images})
    
    now = datetime.now() 
    query = now.strftime("%d %m %Y")
    images = Camera_Two_Image.objects.filter(down_date = query)
    return render(request,'camera2.html',{'images':images})
