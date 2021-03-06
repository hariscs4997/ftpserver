from django.shortcuts import render, redirect, reverse
from ftplib import FTP
import os
from .models import Camera_One_Image, Camera_Two_Image, StateModel
import tempfile
from django.core import files
from datetime import datetime
from dateutil import parser
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserLoginForm
import pysftp




#Download functions
def download_file(filename=None,camera_one = True,ydir=None,mdir=None,ddir=None,idir=None,time=None):
    #lf = tempfile.NamedTemporaryFile()
    #ftp.retrbinary("RETR " + filename, lf.write, 8*1024)
    if camera_one:
        c = Camera_One_Image()
    else:
        c = Camera_Two_Image()
    c.name = filename
    #c_d = ftp.pwd().lstrip("/Kurpark/")
    if camera_one:
        im_url = "https://archiv.dominikketz.de/ac-cc-8e-7a-4b-0d/archive/" + ydir + '/' + mdir + '/' + ddir + '/' + idir + '/' + filename
    else:
        im_url = "https://archiv.dominikketz.de/ac-cc-8e-7a-4c-f5/archive/" + ydir + '/' + mdir + '/' + ddir + '/' + idir + '/' + filename
    c.image_url = im_url
    if int(ddir) < 10:
        if not ddir.startswith('0'):
            date_d = '0' + ddir
        else:
            date_d = ddir
    else:
        date_d = ddir
    if int(mdir) < 10:
        if not mdir.startswith('0'):
            date_m = '0' + mdir
        else:
            date_m = mdir
    else:
        date_m = mdir
    n_date = "{} {} {}".format(date_d,date_m,ydir)
    n_time = time
    print("Assigning time: ",n_time)
    c.down_time = n_time
    c.down_date = n_date
    c.save()
    print('Saved')
    

ext = ('.jpg','.png','.jpeg')

cnopts = pysftp.CnOpts()
cnopts.hostkeys = None

sftp = pysftp.Connection(host='home16953969.1and1-data.host',username='p6684723-timelapse',password="DiesesLiedistwunderschön,aber?8",cnopts=cnopts)



a1 = '/Kurpark/ac-cc-8e-7a-4b-0d/archive/'
a2 = '/Kurpark/ac-cc-8e-7a-4c-f5/archive/'



def start_operation(a,camera_one=True):
    state = StateModel.objects.latest('id')
    sftp.cwd(a)
    year_dirs = sftp.listdir()
#    year_dirs = ftp.nlst(a)[2:]
    for ydir in year_dirs:
        if ydir.startswith('.'):
            continue
        print("Year Dir:",ydir)
        np = a + '/' + ydir
        sftp.cwd(np)
        month_dirs = sftp.listdir()
#        month_dirs = ftp.nlst(ydir)[2:]
        for mdir in month_dirs:
            if mdir.startswith('.'):
                continue
            print("Month Dir:",mdir)
            np = a + '/' + ydir + '/' + mdir
            sftp.cwd(np)
            day_dirs = sftp.listdir()
#            day_dirs = ftp.nlst(mdir)[2:]
            for ddir in day_dirs:
                if ddir.startswith('.'):
                    continue
                print("Day Dir:",ddir)
                np = a + '/' + ydir + '/' + mdir + '/' + ddir
                sftp.cwd(np)
                internal_dirs = sftp.listdir()
#                internal_dirs = ftp.nlst(ddir)[2:]
                for idir in internal_dirs:
                    if idir.startswith('.'):
                        continue
                    print("Internal Dir:",idir)
                    np = a + '/' + ydir + '/' + mdir + '/' + ddir + '/' + idir
                    sftp.cwd(np)
                    list_files = sftp.listdir()
                    for file in list_files:
                        if file.startswith('.'):
                            continue
                        print(file)
                        t1 = str(sftp.lstat(file))
                        t2 = t1.split(' ')
                        time = t2[-2]
                        if camera_one == True:
                            print("Saving: ",file)
                            download_file(filename=file,ydir=ydir,mdir=mdir,ddir=ddir,idir=idir,time=time)
                            state.camera_one = file
                        else:
                            print("Saving: ",file)
                            download_file(filename=file,camera_one=False,ydir=ydir,mdir=mdir,ddir=ddir,idir=idir,time=time)
                            state.camera_two = file
                        state.save()


#                    ftp.cwd(idir)
                    # listing = []
                    # ftp.retrlines('LIST',listing.append)
                    # for list in listing:
                    #     words = list.split(None,8)
                    #     filename = words[-1].lstrip()
                    #     if filename.endswith(ext):
                    #         if camera_one == True:
                    #             print("Downloading: ",filename)
                    #             download_file(filename)
                    #             state.camera_one = filename
                    #         else:
                    #             print("Downloading: ",filename)
                    #             download_file(filename,camera_one=False)
                    #             state.camera_two = filename
                    #         state.save()
    print("Completed")
    # print("Year Dirs Later: ",year_dirs_later)
    # print("Month Dirs Later:", month_dirs_later)
    # print("Day Dirs Later:", day_dirs_later)
    # print("Internal Dirs Later:", internal_dirs_later)




def regular_operation(a,fn,camera_one=True):
    state = StateModel.objects.latest('id')
    sftp.cwd(a)
    year_dirs = sftp.listdir()
    #year_dirs = ftp.nlst(a)[2:]
    year_dirs.reverse()
    #use this counter to end the state saving process after executing one time
    cntr = 0
    for ydir in year_dirs:
        if ydir.startswith('.'):
            continue
        print("Reverse Year Dir:", ydir)
        np = a + '/' + ydir
        sftp.cwd(np)
        month_dirs = sftp.listdir()
        #month_dirs = ftp.nlst(ydir)[2:]
        month_dirs.reverse()
        for mdir in month_dirs:
            if mdir.startswith('.'):
                continue
            print("Reverse Month Dir:", mdir) 
            np = a + '/' + ydir + '/' + mdir
            sftp.cwd(np)
            day_dirs = sftp.listdir()
#            day_dirs = ftp.nlst(mdir)[2:]
            day_dirs.reverse()
            for ddir in day_dirs:
                if ddir.startswith('.'):
                    continue
                
                print("Reverse Day Dir:", ddir)
                np = a + '/' + ydir + '/' + mdir + '/' + ddir
                sftp.cwd(np)
                internal_dirs = sftp.listdir()
#                internal_dirs = ftp.nlst(ddir)[2:]
                internal_dirs.reverse()
                for idir in internal_dirs:
                    if idir.startswith('.'):
                        continue
                    print("Reverse Internal Dir:",idir)
                    np = a + '/' + ydir + '/' + mdir + '/' + ddir + '/' + idir
                    sftp.cwd(np)
#                    ftp.cwd(idir)
                    list_files = sftp.listdir()
                    list_files.reverse()
                    for file in list_files:
                        if file.startswith('.'):
                            continue
                        if file == fn:
                            print("File already exists")
                            return "Out"
                        else:
                            t1 = str(sftp.lstat(file))
                            t2 = t1.split(' ')
                            time = t2[-2]
                            if camera_one:
                                print("Saving: ",file)
                                download_file(filename=file,ydir=ydir,mdir=mdir,ddir=ddir,idir=idir,time=time)
                                if cntr ==0:
                                    state.camera_one = file
                                    cntr +=1
                                    state.save()
                            else:
                                print("Saving: ",file)
                                download_file(filename=file,camera_one=False,ydir=ydir,mdir=mdir,ddir=ddir,idir=idir,time=time)
                                if cntr ==0:
                                    state.camera_two = file
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

@login_required(login_url='/login')
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
        images_f = Camera_One_Image.objects.filter(down_date = search_filter)
        images = images_f.order_by('-down_time')
        return render(request,'camera1.html',{'images':images})
    now = datetime.now()
    query = now.strftime("%d %m %Y")
    images_f = Camera_One_Image.objects.filter(down_date = query)
    images = images_f.order_by('-down_time')
    return render(request,'camera1.html',{'images':images})

@login_required(login_url='/login')
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
        images_f = Camera_Two_Image.objects.filter(down_date = search_filter)
        images = images_f.order_by('-down_time')
        return render(request,'camera2.html',{'images':images})
    
    now = datetime.now() 
    query = now.strftime("%d %m %Y")
    images_f = Camera_Two_Image.objects.filter(down_date = query)
    images = images_f.order_by('-down_time')
    return render(request,'camera2.html',{'images':images})

@login_required(login_url='/login')
def overview(request): 
    return render(request,'overview.html')

@login_required(login_url='/login')
def impressum(request): 
    return render(request,'impressum.html')
# def login(request): 
#     return render(request,'login.html')

@login_required(login_url='/login')
def logout(request):
    #Log the user out
    auth.logout(request)
    messages.success(request, "You have successfuly been logged out")
    return redirect(reverse('login'))

def login(request):
    # Return a login page
    if request.user.is_authenticated:
        return redirect(reverse('overview'))
    if request.method == "POST":
        login_form = UserLoginForm(request.POST)
        
        if login_form.is_valid():
            user = auth.authenticate(username=request.POST['username'],
                                     password=request.POST['password'])
            if user:
                auth.login(user=user, request=request)
                
                messages.success(request, "You have successfuly logged in!")
                return redirect(reverse('overview'))
                
            else:
                login_form.add_error(None, "Your username or password is incorrect")
    else:
        login_form = UserLoginForm()
    return render(request, 'login.html', {"login_form": login_form})