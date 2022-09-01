import tkinter.filedialog
from tkinter.ttk import Notebook
from tkinter.filedialog import askopenfilename
from tkinter import messagebox as mb
from tkinter import ttk
import tkinter as tk
from tkinter import *
from tkinter import messagebox as mb
from pandas import DataFrame
import pandas as pd
import numpy
import numpy as np
import warnings
import _thread as thread
import numpy as np
import csv
import os
from os import listdir
from os.path import isfile
import itertools
import xmltodict
import subprocess as sp
from subprocess import PIPE
import csv
import math
from PIL import ImageTk, Image
import time
import subprocess
import HMDB
import restart_
import psutil
import KEGG
import matplotlib.pyplot as plt
#####make a start window:
Thewindow = tk.Tk()
style = ttk.Style()
style.theme_use('vista')
Thewindow.resizable(False, False)
Thewindow.title('SASA')
Thewindow.iconbitmap('SASAico.ico')

Thewindow.geometry("600x550")

# add logo
Label(Thewindow, text='_'*200).place(x=0, y=380)
Label(Thewindow, text='_'*80).place(x=0, y=400)
Label(Thewindow, text='This project is supported and powered by:').place(x=350, y=405)


img = ImageTk.PhotoImage(Image.open("IM1.png"))
imglabel = Label(Thewindow, image=img).place(x=0, y=425)

img2 = ImageTk.PhotoImage(Image.open("SASAlogo.png"))

img3 = ImageTk.PhotoImage(Image.open("IM2.png"))
imglabel = Label(Thewindow, image=img3).place(x=150, y=495)

img5 = ImageTk.PhotoImage(Image.open("IM4.png"))
imglabel = Label(Thewindow, image=img5).place(x=300, y=495)

img4 = ImageTk.PhotoImage(Image.open("IM3.png"))
imglabel = Label(Thewindow, image=img4).place(x=0, y=495)

img_true = PhotoImage(file = "True.png")
img_true = img_true.subsample(2, 2)

# about text on gui
Label(Thewindow, text="SASA  ( SWATH-Auto System Analyzer ), is a software for SWATH analysis.\n "
                      "Developed at Proteomics and Metabolomics Unit at 57357 Children’s Cancer Hospital, Egypt.\n "
                      "Version 1.0.0").place(x=40, y=10)
Label(Thewindow, text='Citation: ').place(x=10, y=330)

# take a project nanme

def Old_project():
    global ProjectName
    ProjectName = filedialog.askdirectory()
    Label(Thewindow, image=img_true).place(x=210, y=175)
    mb.showinfo(title='OutPut Folder',message='Your OutPut Folder is: ' + ProjectName)

def find_path(path):
    return os.path.isfile(path)
    
def import_your_path():
    set_path = Toplevel(Thewindow)

    Label(set_path, text=" Set the MasterView Path ").grid(row=0, column=0)
    MV = ttk.Entry(set_path)
    MV.grid(row=0, column=1)
    Label(set_path, text=" e.g.: C:\Program Files\MasterView ").grid(row=0, column=2)

    Label(set_path, text=" Set the MultiQuant Path ").grid(row=1, column=0)
    MQ = ttk.Entry(set_path)
    MQ.grid(row=1, column=1)
    Label(set_path, text=" e.g.: C:\Program Files\MultiQuant ").grid(row=1, column=2)

    def Ok():
        with open("MVpath.txt",'w') as MV_path:
            MV_path.write(str(MV.get()))
        with open("MQpath.txt",'w') as MQ_path:
            MQ_path.write(str(MQ.get()))
        Label(Thewindow, image=img_true).place(x=210, y=105)
        set_path.destroy()

    ttk.Button(set_path, text="Ok", command=Ok).grid(row=2, column=2)
    Label(Thewindow, text=' ' * 76).place(x=55, y=150)

def Auto_Check():
    Label(Thewindow, text='Searching for the requirements, Please Wait').place(x=55, y=155)

    MV = find_path(r"C:\Program Files\AB SCIEX\PeakView 2\bin\PeakView.exe")
    MQ = find_path(r"C:\Program Files\AB SCIEX\MultiQuant 3.0\bin\MultiQuant.exe")

    if MV == True and MQ == True:

        with open("MVpath.txt","w") as MV:
            MV.write("C:\\Program Files\AB SCIEX\\PeakView 2\\bin\\PeakView.exe")
        with open("MQpath.txt","w") as MQ:
            MQ.write(r"C:\\Program Files\\AB SCIEX\\MultiQuant 3.0\\bin\\MultiQuant.exe")
            
        Label(Thewindow, image=img_true).place(x=210, y=116)

    else:
        mb.showinfo(title='Check requirements', message='Please make sure that MasterView and MultiQuant are installed on C:\Program Files or enter a new paths for it!!')
        thread.start_new_thread(import_your_path, ())


def TH_Auto_Check():
    thread.start_new_thread(Auto_Check, ())
def About():
    about = Toplevel(Thewindow)
    about.geometry("900x250")
    Label(about, image=img2).place(x=735, y=40)

    whatever_about = "SASA  ( SWATH-Auto System Analyzer ), is a software for SWATH analysis.\n" \
                     "Developed at Proteomics and Metabolomics Unit at 57357 Children’s Cancer Hospital, Egypt.\n" \
                     "SASA Tool was developed using python 3.7 and it can run as an executable file on windows platform. Each function in the script is made to run on a separate thread and used arrays and data frames ( numpy and pandas), hence more speed and efficient processing for the data.\n" \
                     "Version 1.0.0\n____________________\nCopyright (C) 2019  Proteomics and Metabolomics Unit at 57357 Children’s Cancer Hospital"

    msg = tk.Message(about, text = whatever_about)
    msg.config(anchor="n",aspect = 400,font = ('times', 14))
    msg.place(x=10, y=10)

### see if everything is okay before start the main tool
def everything_is_okay():
    #first for MW and MQ
    MV = open("MVpath.txt", "r")
    MQ = open("MQpath.txt", "r")
    if MV.read() != "" and MQ.read() != "":
        try:
            ProjectName_file = ProjectName
            Start_the_software()
        except:
            mb.showerror(title='Erorr.2',message='No output folder available, please choose one. See the documentation file.!!')

    else:
        mb.showerror(title='Erorr.1', message='MasterView or/and MultiQuant paths are not available, please insert them. See the documentation file.!!')


#### start the app.
def Start_the_software():
    global themain
    # make the result folder ( project name )

    ProjectName_file = ProjectName

    Thewindow.destroy()

    warnings.simplefilter(action='ignore', category=FutureWarning)

    themain = tk.Tk()
    themain.geometry("1350x650")
    style = ttk.Style()
    style.theme_use('vista')
    themain.resizable(False, False)
    themain.title('SASA')
    themain.iconbitmap('SASAico.ico')


    # themain.state('zoomed')
    ####mpb = loading bar
    mpb = ttk.Progressbar(themain, orient="horizontal", length=160, mode="determinate")
    mpb.place(x=148, y=570, width=1200, height=15)
    mpb["maximum"] = 100
    # forming a label for  the loading bar\
    label = StringVar()
    Label(themain, textvariable=label).place(x=10, y=565)

    ### to text_histroy the image
    ttk.Label(themain, text='History :', font=20).place(x=1100, y=32)
    T = Text(themain, height=30, width=35, wrap=WORD)
    T.place(x=1060, y=55)
    T.insert(END, ">>> The program   started\n")

    # making the menu and making function to open any file ( retrieve any file )
    def TH_retrieve():
        thread.start_new_thread(retrieve, ())

    def TH_wiff_to_mzxml():
        thread.start_new_thread(wiff_to_mzxml, ())

    def TH_addational_formate_converter():
        thread.start_new_thread(addational_formate_converter, ())


    def retrieve():
        file_name_to_retrieve = filedialog.askopenfilenames()
        for i in file_name_to_retrieve:
            os.startfile(i)
            T.insert(END, '>>> The File ' + i + ' opend\n')
    def restart():
        themain.destroy()

        for proc in psutil.process_iter():
            # check whether the process name matches
            if proc.name() == "SASA.exe":
                proc.kill()
            else:
                pass

        restart_.res()

    def quite():
        themain.destroy()
    def Sofa():
        SOFA = os.path.join("sofastats","sofastats.exe")

        T.insert(END, '>>> Calling SOFA...\n')
        os.startfile(SOFA)

    def TH_Sofa():
        thread.start_new_thread(Sofa, ())

    def KEGG_query():
        #try:
        T.insert(END, ">>>Loading KEGG\n")
        label.set("Loading KEGG")
        main_excel_name = askopenfilename()
        main_excel = pd.read_csv(main_excel_name)
        main_excel.drop_duplicates(subset=["Metabolite ID"], keep='first', inplace=True)
        df_all = pd.DataFrame()

        Loading_new = len(main_excel) / 100  # loading bar
        Loading = 0
        for i_formula , i_name in zip ( main_excel["Formula"] , main_excel["Name"] ):
            df = pd.DataFrame()
            Loading += 1  # loading bar
            path_id, path_name = KEGG.KEGG(i_formula,i_name)
            name_path = i_name +"/"+ "pathway name"
            df[name_path] = path_name
            #df_all = df_all.append(df, ignore_index=True, sort=False)
            df_all = pd.concat([df_all, df], axis=1,sort=False, )
            mpb["value"] = math.floor(round(Loading / Loading_new, 0))


        mpb["value"] = 80
        ProjectName_file_new = ProjectName_file + '/' + 'KEGG result.csv'
        df_all.to_csv(ProjectName_file_new, index=False, header=True)


        all_values = []
        for i in list(df_all.columns.values):
            all_values.append(df_all[i].tolist())
        flat_list = [item for sublist in all_values for item in sublist if str(item) != 'nan']

        dic_count = {i:flat_list.count(i) for i in flat_list}
        df_count = pd.DataFrame([dic_count])
        ##graph

        df_count = df_count.transpose()
        ordered_df = df_count.sort_values(by=0)
        my_range = range(1, len(df_count.index) + 1)

        # The vertival plot is made using the hline function
        # I load the seaborn library only to benefit the nice looking feature
        import seaborn as sns
        sns.set_style("darkgrid")
        #plt.figure(figsize=(10, 10))
        plt.hlines(y=my_range, xmin=0, xmax=ordered_df[0], color="skyblue")
        plt.plot(ordered_df[0], my_range, "o")

        # Add titles and axis names
        plt.rc('xtick', labelsize=8)
        plt.rc('ytick', labelsize=8)
        plt.yticks(my_range, ordered_df.index)
        plt.title("KEGG pathways hits", loc='center')
        plt.xlabel('number of hits')
        plt.ylabel('Pathways')
        plt.tight_layout()
        plt.autoscale()
        ProjectName_file_new = ProjectName_file + '/' + 'KEGG pathways plot.png'
        plt.savefig(ProjectName_file_new, dpi = 300)
        plt.show()

        mpb["value"] = 100
        label.set("KEGG Query processed")
        T.insert(END, ">>> KEGG Query processed\n")
        mb.showinfo(title='KEGG', message='Result KEGG is Saved')
    #except:
     #   mb.showerror("Error.30","KEGG failed to connect, check the internet connection and try again.")

    def TH_KEGG_query():
        thread.start_new_thread(KEGG_query, ())

    menu = Menu(themain)
    themain.config(menu=menu)

    filemenu = Menu(menu)
    menu.add_cascade(label="File", menu=filemenu)
    filemenu.add_command(label="Open...", command=TH_retrieve)
    filemenu.add_separator()
    filemenu.add_command(label="Start New Session...", command=restart)
    filemenu.add_separator()
    filemenu.add_command(label="Quite...", command=quite)
    filemenu.add_separator()


    convert = Menu(menu)
    menu.add_cascade(label="converter", menu=convert)
    convert.add_command(label="Convert .wiff to mzXML...", command=TH_wiff_to_mzxml)
    convert.add_separator()
    convert.add_command(label="Convert to mzML,mzXML,mgf...", command=TH_addational_formate_converter)


    stat = Menu(menu)
    menu.add_cascade(label="Tools", menu=stat)
    stat.add_command(label="Open SOFA...", command=TH_Sofa)
    convert.add_separator()
    stat.add_command(label="KEGG query...", command=TH_KEGG_query)

    ####Step.1#######

    def wiff_to_mzxml():
        try:
            mpb["value"] = 0
            wiff_files = filedialog.askopenfilenames()
            path = os.path.realpath(__file__)
            path = path.replace('\\Filter_PV.py', '')
            path_new = path + '\\msconverter'
            mpb["value"] = 30
            ProjectName_file_new = ProjectName_file
            for filename in wiff_files:
                if '.wiff' in filename:
                    with open('WIFF_convert.bat', 'w') as f:
                        f.write(
                            'cd ' + path_new + ' && ' + 'msconvert ' + filename + ' --mzXML -o ' + ProjectName_file_new)
                    Run = path + '\\WIFF_convert.bat'

                    # CMD RUN and realtime print out
                    call = sp.Popen(Run, stdout=sp.PIPE, bufsize=1)

                    label.set("processing...")

                    CMD_RUN_FRAME = Toplevel(themain)
                    CMD_RUN_FRAME.geometry("900x600")
                    ttk.Label(CMD_RUN_FRAME, text='CMD :', font=20).grid(row=0, column=0)
                    CMD = Text(CMD_RUN_FRAME, height=35, width=100, wrap=WORD)
                    CMD.grid(row=1, column=1)
                    for line in iter(call.stdout.readline, ''):
                        CMD.insert(END, '\n')
                        CMD.insert(END, str(line.strip()))
                    call.wait()
                    call.stdout.close()
                    CMD_RUN_FRAME.destroy()
                    if call == 0:
                        label.set("process  done")
                        mb.showinfo(title='Result', message='Result  Saved')
                        T.insert(END, '>>> .wiff file(s) is/are converted to .mzXML \n')
                    else:
                        label.set("ERROR")
                        mb.showinfo(title='Result', message='Error')
                else:
                    mb.showinfo(title='Result', message='The file should be a .wiff formate')
                    T.insert(END, '>>> Error \n')
                    CMD_RUN_FRAME.destroy()
            mpb["value"] = 100
        except:
            mb.showerror(title='Error 3', message='You did not import a file or you did not import the write file. See the documentation file')


    def addational_formate_converter():
        # note you didn't write yet converion code from Waters RAW to any mz data formate.
        try:
            mpb["value"] = 0
            themain5 = Toplevel(themain)
            themain5.title('SASA')
            themain5.iconbitmap('SASAico.ico')
            path = os.path.realpath(__file__)
            path = path.replace('\\Filter_PV.py', '')
            path_new = path + '\\msconverter'
            ProjectName_file_new = ProjectName_file
            ## create Radiobutton
            MODES = [
                ("mzML", "mzML"),
                ("mzXML", "mzXML"),
                ("mgf", "mgf"),
                ("text", "text"),]
            v = StringVar()
            v.set("L")  # initialize

            row = 1
            for text, mode in MODES:
                row += 1
                b = ttk.Radiobutton(themain5, text=text,
                                    variable=v, value=mode).grid(row=row, column=0)
                ttk.Label(themain5,
                          text='convert from: Agilent, \nBruker FID/YEP/BAF, \nThermo RAW and MS2/CMS2/BMS2 to:').grid(
                    row=0, column=0)

            def Run():
                mpb["value"] = 30
                name_files = filedialog.askopenfilenames()
                for filename in name_files:
                    with open('_convert.bat', 'w') as f:
                        if v.get() == 'mzML':
                            f.write(
                                'cd ' + path_new + ' && ' + 'msconvert ' + filename + ' --mzML -o ' + ProjectName_file_new)
                        if v.get() == 'mzXML':
                            f.write(
                                'cd ' + path_new + ' && ' + 'msconvert ' + filename + ' --mzXML -o ' + ProjectName_file_new)
                        if v.get() == 'mgf':
                            f.write(
                                'cd ' + path_new + ' && ' + 'msconvert ' + filename + ' --mgf -o ' + ProjectName_file_new)
                        if v.get() == 'text':
                            f.write(
                                'cd ' + path_new + ' && ' + 'msconvert ' + filename + ' --text -o ' + ProjectName_file_new)

                    Run = path + '\\_convert.bat'

                    # CMD RUN and realtime print out
                    call = sp.Popen('Run', cwd=path, stdout=sp.PIPE, bufsize=1)

                    label.set("processing...")

                    CMD_RUN_FRAME = Toplevel(themain)
                    CMD_RUN_FRAME.geometry("900x600")
                    ttk.Label(CMD_RUN_FRAME, text='CMD :', font=20).grid(row=0, column=0)
                    CMD = Text(CMD_RUN_FRAME, height=35, width=100, wrap=WORD)
                    CMD.grid(row=1, column=1)
                    for line in iter(call.stdout.readline, ''):
                        CMD.insert(END, '\n')
                        CMD.insert(END, str(line.strip()))
                    call.wait()
                    call.stdout.close()

                    if call == 0:
                        label.set("process  done")
                        mb.showinfo(title='Result', message='Result  Saved')
                        T.insert(END, '>>> file(s) is/are converted to' + v.get() + '\n')
                        mpb["value"] = 70
                        CMD_RUN_FRAME.destroy()
                    else:
                        label.set("ERROR")
                        mb.showinfo(title='Result', message='Error')
                mpb["value"] = 100

            ttk.Button(themain5, text="   Run   ", command=Run).grid(row=5, column=1)
        except:
            mb.showerror(title='Error 4',message='You did not import a file or you did not import the write file. See the documentation file')

        #####STEP1.1#################



    #### Step 1.2####convert database txt files to excel
    #############################################################

    def RUN_database_converter_xml():
        try:
            global Name
            mpb["value"] = 0
            theroot2 = Toplevel(themain)
            theroot2.title('SASA')
            theroot2.iconbitmap('SASAico.ico')

            Name = ttk.Entry(theroot2)
            Name.grid(row=0, column=1)
            Label(theroot2, text="   Save File By ").grid(row=0, column=0)

            def TH_Run():
                thread.start_new_thread(Run, ())

            def open_():
                mpb["value"] = 0
                global dir_path
                dir_path = filedialog.askopenfilenames()
                mpb["value"] = 100
                label.set("File(s)  loaded")

            def Run():
                mpb["value"] = 0
                global Name
                Name = Name.get() + '.csv'
                df = pd.DataFrame()
                df_new_first = pd.DataFrame([])
                row = -1
                FINAL_data = pd.DataFrame()
                # make the first part of the xml the main peak

                # for loading bar
                Loading = 0
                for file_name in dir_path:
                    Loading += 1  # loading bar
                    Loading_new = len(dir_path) / 100  # loading bar
                    mpb["value"] = math.floor(round(Loading / Loading_new, 0))  # loading bar

                    new_df_ms = pd.DataFrame()

                    row += 1
                    with open(file_name) as fd:
                        doc = xmltodict.parse(fd.read())

                    try:
                        for i in doc['ms-ms']:
                            if i != 'references' and i != 'ms-ms-peaks':
                                df[i] = [doc['ms-ms'][i]]
                    except:
                        pass

                    try:
                        for i in doc['ms-ms']['references']['reference']:
                            i_new = i + ' //references'
                            df[i_new] = [(doc['ms-ms']['references']['reference'][i])]
                    except:
                        pass



                    # make the F_
                    peaks_num = 0
                    peaks_row = -1
                    row_list = []
                    ALL_RJ_list = []
                    try:
                        for i in doc['ms-ms']['ms-ms-peaks']:
                            for r in doc['ms-ms']['ms-ms-peaks'][i]:

                                col_list = []
                                RJ_list = []
                                peaks_num += 1
                                FF = 'F ' + str(peaks_num)
                                for e in r.keys():
                                    col_list.append(e)
                                for j in r:
                                    RJ_list.append(r[j])
                                ALL_RJ_list.append(RJ_list)
                    except:
                        pass

                    try:
                        new_df_ms = pd.concat([pd.DataFrame([q], columns=col_list) for q in ALL_RJ_list],
                                              ignore_index=True)
                        new_df_ms.rename(columns={'id': 'F_id'}, inplace=True)
                    except:
                        pass
                    F_index = []
                    try:
                        for i in range(len(new_df_ms.index)):
                            i = i + 1
                            i = 'F_' + str(i)
                            F_index.append(i)
                    except:
                        pass
                    try:
                        new_df_ms.insert(0, 'F', F_index)
                        new_df_ms = new_df_ms.convert_objects(convert_numeric=True)
                        new_df_ms['PK$PEAK_int_rel'] = (new_df_ms['intensity'] / new_df_ms['intensity'].max()) * 100
                        new_df_ms = new_df_ms[new_df_ms['PK$PEAK_int_rel'] >= 5]
                    except:
                        pass

                    # append the main part to the F_ part
                    final_df = pd.DataFrame()
                    final_df = pd.concat([df, new_df_ms], axis=1, sort=False, ignore_index=False)

                    FINAL_data = FINAL_data.append(final_df, ignore_index=True, sort=False)
                    FINAL_data = FINAL_data.apply(pd.to_numeric ,  errors='ignore' ,  downcast='float')

                FINAL_data[['database-id',  'id //references']] = FINAL_data[
                    ['database-id','id //references']].fillna(method='ffill')

                FINAL_data.rename(columns={'database-id': 'ACCESSION',
                                           'mass-charge': 'PK$PEAK_m/z', 'intensity': 'PK$PEAK_int',
                                          }, inplace=True)

                new_df_df = pd.DataFrame()

                mpb["value"] = 0
                Loading = 0
                for i in set(FINAL_data["ACCESSION"]):
                    Loading += 1  # loading bar
                    Loading_new = len(set(FINAL_data["ACCESSION"])) / 100  # loading bar
                    mpb["value"] = math.floor(round(Loading / Loading_new, 0))  # loading bar
                    new_df_df__ = pd.DataFrame()
                    Name_, Formula, location = HMDB.HMDB(i)
                    new_df_df__["CH$FORMULA"] = [Formula]
                    new_df_df__["ACCESSION"] = i
                    new_df_df = new_df_df.append(new_df_df__, ignore_index=True,
                                                 sort=False)

                Final_merge = FINAL_data.merge(new_df_df, how='inner', on='ACCESSION')

                mpb["value"] = 70
                ProjectName_file_new = ProjectName_file + '/' + Name + '.csv'
                Final_merge.to_csv(ProjectName_file_new, index=False, header=True)
                label.set("DataBase File is Created")
                mpb["value"] = 95
                mpb["value"] = 100
                mb.showinfo(title='Result', message='Result  Saved')
                T.insert(END, ">>> DataBases is created\n")

                theroot2.destroy()

            ttk.Button(theroot2, text="Open Xml File(s) ", command=open_, width=20).grid(row=1, column=0)
            ttk.Button(theroot2, text="   run   ", command=TH_Run, width=20).grid(row=1, column=1)

        except:
            theroot2.destroy()
            mb.showerror("Error 6","Something going wrong!!.\n OR you did not enter a valid information, please See the documentation")

    def Insert_build_in_database():

        global HMDB_HR_P
        global HMDB_HR_N
        global ReSpect
        global my_DB
        global MAIN_DB
        theroot9 = Toplevel(themain)
        theroot9.title('SASA')
        theroot9.iconbitmap('SASAico.ico')

        DB = IntVar()

        # HMDB_HR

        Label(theroot9, text='HMDB HR').grid(row=0, column=0)

        ttk.Radiobutton(theroot9, text='HMDB HR +ve', variable=DB,value = 1).grid(row=1, column = 0,sticky=W)

        ttk.Radiobutton(theroot9, text='HMDB HR -ve', variable=DB, value=2).grid(row=2, column=0, sticky=W)

        # HMDB_LR

        Label(theroot9, text='HMDB LR').grid(row=0, column=1)

        ttk.Radiobutton(theroot9, text='HMDB LR +ve        ', variable=DB,value = 11).grid(row=1, column = 1,sticky=W)

        ttk.Radiobutton(theroot9, text='HMDB LR -ve         ', variable=DB, value=22).grid(row=2, column=1, sticky=W)

        # ReSpect for Phytochemicals

        # my_DB
        Label(theroot9, text='Other option').grid(row=0, column=3)
        ttk.Radiobutton(theroot9, text='Import a Database', variable=DB, value=3).grid(row=1, column=3, sticky=W)

        def run():
            global MAIN_DB
            if DB.get() == 1:
                MAIN_DB = pd.read_csv('HMDB_HR_P.csv')
            elif DB.get() == 2:
                MAIN_DB = pd.read_csv('HMDB_HR_N.csv')

            elif DB.get() == 11:
                MAIN_DB = pd.read_csv('HMDB_LR_P.csv')
            elif DB.get() == 22:
                MAIN_DB = pd.read_csv('HMDB_LR_N.csv')

            elif DB.get() == 3:
                filename_DB = askopenfilename()
                if '.xlsx' in filename_DB:
                    MAIN_DB = pd.read_excel(filename_DB)
                if '.csv' in filename_DB:
                    MAIN_DB = pd.read_csv(filename_DB,encoding="cp1252",low_memory=False)

            mpb["value"] = 100
            label.set("DataBase is Imported")
            T.insert(END, ">>> DataBase is Imported\n")
            theroot9.destroy()

        ttk.Button(theroot9, text="   OK   ", command=run).grid(row=5, column=0)

    ##step2

    def P_V_Method_File():
        
        try:
            global PPM
            global data_DB
            try:
                data_DB = MAIN_DB
            except:
                mb.showerror(title='Erorr.7',message='No database is available!! please choose a built-in database or import yours.. See the documentation file.!!')
                return False

            global filename
            mpb["value"] = 0
            themain6 = Toplevel(themain)
            themain6.title('SASA')
            themain6.iconbitmap('SASAico.ico')

            Label(themain6, text=" Width (Da) ").grid(row=0, column=0)
            PPM = ttk.Entry(themain6)
            PPM.grid(row=0, column=1)
            PPM.config(foreground='gray')
            PPM.insert(0, "Example: 0.01")



            def TH_Run():
                thread.start_new_thread(Run, ())



            def Open_RULE():
                global filename_rule
                filename_rule = askopenfilename()
                mpb["value"] = 100
                label.set("Adducts File is Loaded")




            def Run():
                global PPM
                global data_DB
                try:
                    data_rule = pd.read_csv(filename_rule)
                except:
                    mb.showerror(title='Error.13', message='Please Enter the Adducts file.')
                    return False
                print (PPM.get())
                #if PPM.get() != "Example: 0.01":
                 #   mb.showerror(title='Erorr.8', message='You did not enter the width (Da)')
                  #  return False
                #else:
                 #   pass

                global filename
                label.set("loading")
                mpb["value"] = 0

                data_DB = data_DB.fillna('')
                List_formula = [i for i in data_DB['CH$FORMULA'] if i != '']
                list_id = [i for i in data_DB['ACCESSION'] if i != '']

                ppm_value = float(PPM.get())

                data_rule = pd.read_csv(filename_rule)
                # Genreate the PV method
                PV_method_with_adducts = pd.DataFrame()
                Loading = 0  # loading bar
                Loading_new = len(data_rule['name']) / 100  # loading bar
                for adu in data_rule['name']:
                    Loading += 1  # loading bar
                    mpb["value"] = math.floor(round(Loading / Loading_new, 0))  # loading bar

                    Find1 = adu.find("+")
                    Find2 = adu.find("]")

                    if "-" in adu:
                        adu = adu[Find1 + 1:Find2]
                        adu = f"-{adu}"

                    else:
                        adu = adu[Find1 + 1:Find2]

                    PV_method_dataframe = pd.DataFrame()

                    # PV_method_dataframe['#']= [ i  for i in range(1,len(List_name)+1)]
                    PV_method_dataframe['Name'] = list_id
                    PV_method_dataframe['Formula'] = List_formula
                    PV_method_dataframe['Include'] = 'TRUE'
                    PV_method_dataframe['Mass(Da)'] = ''
                    PV_method_dataframe['Found At Mass (Da)'] = 0
                    PV_method_dataframe['Control Found At Mass (Da)'] = ''
                    PV_method_dataframe['Width (Da)'] = ppm_value
                    pd.to_numeric(PV_method_dataframe['Width (Da)'])

                    if adu == "M":
                        PV_method_dataframe['Adduct'] = ""
                    else:
                        PV_method_dataframe['Adduct'] = adu

                    PV_method_dataframe['Expected RT (min)'] = 0
                    PV_method_dataframe['RT Width (min)'] = 1
                    PV_method_dataframe['Found At RT (min)'] = 0
                    PV_method_dataframe['Library Score'] = -1
                    PV_method_dataframe['Library Hit'] = ''
                    PV_method_dataframe['Formula Finder Result'] = ''
                    PV_method_dataframe['Intensity'] = 0
                    PV_method_dataframe['Control Intensity'] = ''
                    PV_method_dataframe['Known Concentration'] = ''
                    PV_method_dataframe['Calculated Concentration'] = ''
                    PV_method_dataframe['Area'] = 0
                    PV_method_dataframe['Control Area'] = ''
                    PV_method_dataframe['Isotope'] = 0
                    PV_method_dataframe['Threshold (cps)'] = 100
                    PV_method_dataframe['Threshold (ratio of control)'] = 5
                    PV_method_dataframe['Calculated Concentration'] = ''
                    PV_method_dataframe['Formula Finder Score'] = -1
                    PV_method_dataframe['Int Std'] = 'FALSE'
                    PV_method_dataframe['Combined Score'] = -1
                    PV_method_dataframe['Mass Error Score'] = -1
                    PV_method_dataframe['RT Score'] = -1
                    PV_method_dataframe['Isotope Score'] = -1
                    PV_method_dataframe['Non-Targeted Peak'] = 'FALSE'
                    PV_method_dataframe['S:N'] = ''
                    PV_method_dataframe['Fragment Mass (Da)'] = ''
                    PV_method_dataframe['Comments'] = ''
                    PV_method_dataframe['Extraction Mass (Da)'] = ''
                    PV_method_dataframe['Error (ppm)'] = 0
                    PV_method_dataframe['Control Error (ppm)'] = ''
                    PV_method_dataframe['Error (mDa)'] = 0
                    PV_method_dataframe['Control Error (mDa)'] = ''
                    PV_method_dataframe['RT Delta (min)'] = 0
                    PV_method_dataframe['Control RT Delta (min)'] = ''
                    PV_method_dataframe['RT % Error'] = 0
                    PV_method_dataframe['Control RT % Error'] = ''
                    PV_method_with_adducts = PV_method_with_adducts.append(PV_method_dataframe, ignore_index=True,
                                                                           sort=False)

                    mpb["value"] = 95
                PV_method_with_adducts.drop_duplicates(subset=['Name', 'Adduct'], inplace=True)
                PV_method_with_adducts.insert(loc=0, column='#',
                                              value=range(1, len(PV_method_with_adducts.index.tolist()) + 1))

                ProjectName_file_new = ProjectName_file + '/' + "MasterView.csv"
                PV_method_with_adducts.to_csv(ProjectName_file_new, index=False, header=True)

                mpb["value"] = 100
                label.set("Method Generated")
                T.insert(END, ">>> MasterView Method is Generated\n")
                Label(themain, text='----->').place(x=260, y=150)
                mb.showinfo(title='MasterView', message='MasterView Method is Saved')
                themain6.destroy()


        except:
            mb.showerror(title='Error.9', message='Something going wrong!!, please go back to the documentation.')

        ttk.Button(themain6, text="   Import The Adducts File   ", command=Open_RULE).grid(row=1, column=0)
        ttk.Button(themain6, text="   Run   ", command=TH_Run).grid(row=1, column=2)
        while True:
            if PPM.get() != "Example: 0.01":
                PPM.config(foreground='black')
                break

    def Open_MW():
        try:
            with open ("MVpath.txt",'r') as f:
                f = f.read()
            os.startfile(str(f))
            T.insert(END, ">>> MasterView is Opened\n")
            label.set("MasterView is Opened")
            mpb["value"] = 100
        except:
            mb.showerror(title='Error.10', message='Error, Go back to The documentation')

    def M_Q_Method_FILE():
        try:
            try:
                data_DB = MAIN_DB
            except:
                mb.showerror(title='Error.7',
                            message='No database is available!! please choose a built-in database or import yours.. See the documentation file.!!')
                return False
            def TH_Run():
                thread.start_new_thread(Run, ())

            global shift
            global filename
            global Minimum_m_z
            global m_z_window
            global Maximum_m_z
            mpb["value"] = 0
            themain7 = Toplevel(themain)
            themain7.title('SASA')
            themain7.iconbitmap('SASAico.ico')

            Label(themain7, text=" m/z Shift ").grid(row=0, column=0)
            shift = ttk.Entry(themain7)
            shift.grid(row=0, column=1)
            shift.insert(0, "Example: 20")

            Label(themain7, text=" Start m/z  ").grid(row=1, column=0)
            Minimum_m_z = ttk.Entry(themain7)
            Minimum_m_z.grid(row=1, column=1)
            Minimum_m_z.insert(0, "Example: 50")

            Label(themain7, text=" End m/z  ").grid(row=2, column=0)
            Maximum_m_z = ttk.Entry(themain7)
            Maximum_m_z.grid(row=2, column=1)
            Maximum_m_z.insert(0, "Example: 1100")

            Label(themain7, text=" SWATH Window ").grid(row=3, column=0)
            m_z_window = ttk.Entry(themain7)
            m_z_window.grid(row=3, column=1)
            m_z_window.insert(0, "Example: 50")

            shift.config(foreground='gray')
            Minimum_m_z.config(foreground='gray')
            Maximum_m_z.config(foreground='gray')
            m_z_window.config(foreground='gray')


            # Filteration(): # filter the result from the P V method to find the detected the parents and there fragments to write the MQ method
            def open_PV_result():
                global filename_PV_result
                filename_PV_result = filedialog.askopenfilenames()
                mpb["value"] = 100
                T.insert(END, ">>> MasterView is Imported\n")
                label.set("Method Imported")


            def Run():

                for data_PV_result_i in filename_PV_result:

                    try:
                        data_PV_result = pd.read_csv(data_PV_result_i,low_memory=False)
                    except:
                        mb.showerror(title='Error.12', message='Please import the MasterView result file..')
                        return False

                    #if str(shift.get()) == "Example: 20" or str(Minimum_m_z.get()) == "Example: 50" or str(
                    #        Maximum_m_z.get()) == "Example: 1100" or str(m_z_window.get()) == "Example: 50":
                    #   mb.showerror(title='Error.11', message='Please, enter all the Parameters.')
                    #   return False
                    #else:
                    #    pass

                    global append_dataframe_MQ_Dataframe_mothod_main

                    
                    each_file_name = data_PV_result_i[::-1]
                    each_file_name = each_file_name[:each_file_name.find("/")]
                    each_file_name = each_file_name[::-1]
                    each_file_name = each_file_name.replace(".csv","")

                    
                    ProjectName_file_new = ProjectName_file + '/' + each_file_name + "_" + "MultiQuant.txt"
                    ProjectName_file_new_for_filteration = ProjectName_file + '/'+ each_file_name + "_" + 'MQ_Filteration_method' + '.txt'

                    data_PV_result = pd.read_csv(data_PV_result_i)
                    data_PV_result["Adduct"].fillna("M", inplace=True)

                    # see if the mz range is true
                    # first calculate how many range we have by the window of the mz


                    try:
                        shiftshift = shift.get()
                        Minimum_m_z_float = Minimum_m_z.get()
                        Maximum_m_z_float = Maximum_m_z.get()
                        m_z_window_float = m_z_window.get()
                    except:
                        print(shiftshift , Minimum_m_z_float , Maximum_m_z_float, m_z_window_float)

                    
                    Range_mz = (float(Maximum_m_z_float) - float(Minimum_m_z_float)) / float(m_z_window_float)

                    if (Range_mz - math.floor(Range_mz)) == 0:
                        # filter dabase by formula
                        data_DB = MAIN_DB

                        data_DB.dropna(subset=['PK$PEAK_m/z'], inplace=True)

                        data_DB = data_DB.sort_values(by=['CH$FORMULA'])

                        data_DB.reset_index(drop=True, inplace=True)

                        # filter the PV_result to DB to detect the parent

                        mpb["value"] = 30

                        # List_formula_DB = set(data_DB['CH$FORMULA'])
                        # List_PV_result = set (data_PV_result['Formula'])
                        List_of_common_formula = set(data_PV_result['Name']).intersection(data_DB['ACCESSION'])

                        mpb["value"] = 0
                        set_of_formula_with_adducts = []

                        Loading = 0
                        Loading_new = len(List_of_common_formula) / 100  # loading bar
                        for j in List_of_common_formula:
                            Loading += 1  # loading bar
                            mpb["value"] = math.floor(round(Loading / Loading_new, 0))  # loading bar
                            for i in range(len(data_PV_result['Name'])):
                                if j == data_PV_result['Name'][i]:
                                    if data_PV_result['Adduct'][i] == "M":
                                        formula_adducts = data_PV_result['Name'][i] + "$" + data_PV_result['Formula'][i] + '+' + "M" + '_' + str(data_PV_result['Extraction Mass (Da)'][i]) + '*' + str(data_PV_result['Found At RT (min)'][i]) # to be used in the next step
                                    else:
                                        formula_adducts = data_PV_result['Name'][i] + "$" + data_PV_result['Formula'][i] + '+' + data_PV_result['Adduct'][i] + '_' + str(data_PV_result['Extraction Mass (Da)'][i]) + '*' + str(data_PV_result['Found At RT (min)'][i]) # to be used in the next step

                                    set_of_formula_with_adducts.append(formula_adducts)

                        List_of_formula_with_adducts_with_rt = set(set_of_formula_with_adducts)
                        # Daraframe for MQ method
                        append_dataframe_MQ_Dataframe_mothod_main = pd.DataFrame()
                        # write the MQ method for parents
                        mpb["value"] = 0
                        Loading = 0
                        Loading_new = len(List_of_formula_with_adducts_with_rt) / 100  # loading bar

                        append_MQ_Dataframe_mothod = pd.DataFrame()
                        append_new_MQ_Dataframe_mothod = pd.DataFrame()

                        for i in List_of_formula_with_adducts_with_rt:
                            Loading += 1  # loading bar
                            mpb["value"] = math.floor(round(Loading / Loading_new, 0))  # loading bar

                            formula_extracted_mass_parrent = float(i[i.find('_') + 1:i.find('*')])
                            formula_Ert_parrent = float(i[i.find('*') + 1:])
                            name_with_aduct_parrent = i[:i.find('$')]
                            adducts = i[i.find('+'):i.find('_')]
                            MQ_Dataframe_mothod = pd.DataFrame()
                            new_MQ_Dataframe_mothod = pd.DataFrame()

                            MQ_Dataframe_mothod['Accuracy For QCs Used'] = ['TRUE']
                            MQ_Dataframe_mothod['Accuracy For Stds Used'] = 'TRUE'
                            MQ_Dataframe_mothod['Baseline Sub. Window'] = str(0.1)
                            MQ_Dataframe_mothod['Calc Conc Used'] = 'TRUE'
                            MQ_Dataframe_mothod['Comment'] = ''
                            MQ_Dataframe_mothod['End Mass'] = [formula_extracted_mass_parrent + (((float(shiftshift) / pow(10, 6)) * formula_extracted_mass_parrent))]
                            MQ_Dataframe_mothod['Expected RT'] = [str(formula_Ert_parrent)]
                            MQ_Dataframe_mothod['Experiment'] = str(1)
                            MQ_Dataframe_mothod['Extraction Type'] = 'Scan'
                            MQ_Dataframe_mothod['GroupName'] = name_with_aduct_parrent + adducts + '_A'
                            MQ_Dataframe_mothod['Ion Ratio Tolerance'] = str(20)
                            MQ_Dataframe_mothod['Ion Ratio Used'] = 'TRUE'
                            MQ_Dataframe_mothod['IS'] = 'FALSE'
                            MQ_Dataframe_mothod['Lower Lim Calc Conc'] = ''
                            MQ_Dataframe_mothod['Max Tolerance LLOQ'] = str(20)
                            MQ_Dataframe_mothod['Max Tolerance QC'] = str(15)
                            MQ_Dataframe_mothod['Max Tolerance Stds'] = str(15)
                            MQ_Dataframe_mothod['Min Peak Height'] = str(0)
                            MQ_Dataframe_mothod['Min Peak Width'] = str(4)
                            MQ_Dataframe_mothod['Name'] = name_with_aduct_parrent + adducts  ### why name = formula + ID cuz name of fragments cant be tha same so just to make sure that the names are diffrenet
                            MQ_Dataframe_mothod['Noise Percentage'] = str(100)
                            MQ_Dataframe_mothod['Peak Splitting Factor'] = str(1)
                            MQ_Dataframe_mothod['Period'] = str(1)
                            MQ_Dataframe_mothod['Regression Type'] = 'Linear'
                            MQ_Dataframe_mothod['Report Largest Peak'] = 'TRUE'
                            MQ_Dataframe_mothod['Smoothing Width'] = str(3)
                            MQ_Dataframe_mothod['Start Mass'] = [formula_extracted_mass_parrent - (((float(shiftshift) / pow(10, 6)) * formula_extracted_mass_parrent))]
                            MQ_Dataframe_mothod['Units'] = ''
                            MQ_Dataframe_mothod['Update RT'] = str(0)
                            MQ_Dataframe_mothod['Upper Lim Calc Conc'] = ''
                            MQ_Dataframe_mothod['Use Area'] = 'TRUE'
                            MQ_Dataframe_mothod['PK$PEAK_int_rel'] = ['A_P']

                            # append only the dataframe for the first parent
                            append_MQ_Dataframe_mothod = append_MQ_Dataframe_mothod.append(MQ_Dataframe_mothod,ignore_index=True, sort=False)

                            # append the second parent dataframe in the main dataframe
                            append_dataframe_MQ_Dataframe_mothod_main = append_dataframe_MQ_Dataframe_mothod_main.append(MQ_Dataframe_mothod, ignore_index=True, sort=False)

                            # for the second parent with real exp. number
                            Exper_number = (formula_extracted_mass_parrent - float(Minimum_m_z_float)) / float( m_z_window_float)
                            if Exper_number - math.floor(Exper_number) == 0:
                                real_Exper_number = Exper_number + 1
                            elif Exper_number - math.floor(Exper_number) != 0:
                                real_Exper_number = Exper_number + 2

                            new_MQ_Dataframe_mothod['End Mass'] = [formula_extracted_mass_parrent + (
                            ((float(shiftshift) / pow(10, 6)) * formula_extracted_mass_parrent))]
                            new_MQ_Dataframe_mothod['Expected RT'] = [str(formula_Ert_parrent)]
                            new_MQ_Dataframe_mothod['Experiment'] = [str(int(real_Exper_number))]
                            new_MQ_Dataframe_mothod['GroupName'] = name_with_aduct_parrent + adducts
                            new_MQ_Dataframe_mothod['Name'] = name_with_aduct_parrent + adducts + "_B"  ### why name = formula + ID cuz name of fragments cant be tha same so just to make sure that the names are diffrenet
                            new_MQ_Dataframe_mothod['Start Mass'] = [formula_extracted_mass_parrent - (
                            ((float(shiftshift) / pow(10, 6)) * formula_extracted_mass_parrent))]
                            new_MQ_Dataframe_mothod['PK$PEAK_int_rel'] = ['AA_P']

                            # append only dataframe for second parent
                            append_new_MQ_Dataframe_mothod = append_new_MQ_Dataframe_mothod.append(new_MQ_Dataframe_mothod,
                                                                                                   ignore_index=True,
                                                                                                   sort=False)

                            # append the second parent dataframe in the main dataframe
                            append_dataframe_MQ_Dataframe_mothod_main = append_dataframe_MQ_Dataframe_mothod_main.append(
                                new_MQ_Dataframe_mothod, ignore_index=True, sort=False)
                        # write MQ for fragments
                        Loading = 0
                        mpb["value"] = 0
                        # ID = 0
                        Loading_new = len(append_MQ_Dataframe_mothod['GroupName']) / 100  # loading bar
                        for i_parent in range(len(append_MQ_Dataframe_mothod['GroupName'])):

                            parent_formila = str(append_MQ_Dataframe_mothod['GroupName'][i_parent])
                            parent_formila = parent_formila[:parent_formila.find('+')]
                            parent_formila_with_adducts = str(append_MQ_Dataframe_mothod['GroupName'][i_parent])
                            parent_formila_with_adducts = parent_formila_with_adducts[:parent_formila_with_adducts.find("_")]
                            parent_formila_with_adducts = parent_formila_with_adducts

                            if data_DB['ACCESSION'].str.contains(parent_formila).any() == True:
                                FMZ = pd.DataFrame()
                                FMZ = FMZ.iloc[0:0]

                                end_mass = list(data_DB['ACCESSION'])
                                res = len(end_mass) - 1 - end_mass[::-1].index(parent_formila)

                                MZ = data_DB['PK$PEAK_m/z'][end_mass.index(parent_formila):res + 1]
                                relt_int = data_DB['PK$PEAK_int_rel'][end_mass.index(parent_formila):res + 1]

                                Fragment_exp_number = append_new_MQ_Dataframe_mothod.loc[append_new_MQ_Dataframe_mothod[
                                                                                             'GroupName'] == parent_formila_with_adducts, 'Experiment'].tolist()
                                Fragment_exp_number_real = str(int(Fragment_exp_number[0]))

                                # group name without _A
                                Group_Name = append_MQ_Dataframe_mothod['GroupName'][i_parent].replace('_A', '')

                                FMZ['End Mass'] = MZ + ((float(shiftshift) / pow(10, 6)) * MZ)
                                FMZ['Expected RT'] = append_MQ_Dataframe_mothod['Expected RT'][i_parent]
                                FMZ['Experiment'] = Fragment_exp_number_real 
                                FMZ['Name'] = append_MQ_Dataframe_mothod['Name'][i_parent] + MZ.astype(
                                    str)  ### why name = formula + ID cuz name of fragments cant be tha same so just to make sure that the names are diffrene
                                FMZ['Start Mass'] = MZ - ((float(shiftshift) / pow(10, 6)) * MZ)
                                FMZ['GroupName'] = Group_Name
                                FMZ['PK$PEAK_int_rel'] = relt_int

                                FMZ.reset_index(drop=True, inplace=True)

                                FMZ.drop_duplicates(subset='Name', keep='first', inplace=True)

                                append_dataframe_MQ_Dataframe_mothod_main = append_dataframe_MQ_Dataframe_mothod_main.append(
                                    FMZ, ignore_index=True, sort=False)

                                Loading += 1  # loading bar
                                mpb["value"] = math.floor(round(Loading / Loading_new, 0))  # loading bar

                        append_dataframe_MQ_Dataframe_mothod_main[
                            ['Regression Type', 'Accuracy For QCs Used', 'Accuracy For Stds Used', 'Baseline Sub. Window',
                             'Calc Conc Used', 'Extraction Type', 'Ion Ratio Tolerance', 'Ion Ratio Used', 'IS',
                             'Max Tolerance LLOQ', 'Max Tolerance QC', 'Max Tolerance Stds', 'Min Peak Height',
                             'Min Peak Width', 'Noise Percentage', 'Peak Splitting Factor', 'Period', 'Report Largest Peak',
                             'Smoothing Width', 'Update RT', 'Upper Lim Calc Conc', 'Use Area']] = \
                        append_dataframe_MQ_Dataframe_mothod_main[
                            ['Regression Type', 'Accuracy For QCs Used', 'Accuracy For Stds Used', 'Baseline Sub. Window',
                             'Calc Conc Used', 'Extraction Type', 'Ion Ratio Tolerance', 'Ion Ratio Used', 'IS',
                             'Max Tolerance LLOQ', 'Max Tolerance QC', 'Max Tolerance Stds', 'Min Peak Height',
                             'Min Peak Width', 'Noise Percentage', 'Peak Splitting Factor', 'Period', 'Report Largest Peak',
                             'Smoothing Width', 'Update RT', 'Upper Lim Calc Conc', 'Use Area']].fillna(method='ffill')

                        mpb["value"] = 70
                        append_dataframe_MQ_Dataframe_mothod_main = append_dataframe_MQ_Dataframe_mothod_main[
                            append_dataframe_MQ_Dataframe_mothod_main['End Mass'] >= float(
                                Minimum_m_z_float)]  # make this before sorting
                        append_dataframe_MQ_Dataframe_mothod_main = append_dataframe_MQ_Dataframe_mothod_main[
                            append_dataframe_MQ_Dataframe_mothod_main['End Mass'] <= float(
                                Maximum_m_z_float)]  # make this before sorting

                        append_dataframe_MQ_Dataframe_mothod_main.sort_values(by=['GroupName'], ascending=False,
                                                                              inplace=True)

                        # write MQ_filiteration
                        append_dataframe_MQ_Dataframe_mothod_main.to_csv(ProjectName_file_new_for_filteration, header=True,
                                                                         index=False, sep='\t')

                        # write the main MQ
                        append_dataframe_MQ_Dataframe_mothod_main.drop(columns=['PK$PEAK_int_rel'], inplace=True)

                        append_dataframe_MQ_Dataframe_mothod_main.to_csv(ProjectName_file_new, header=True, index=False,sep='\t')

                        mpb["value"] = 100

                        
                        Label(themain, text='----->').place(x=260, y=250)
                        T.insert(END, ">>> MultiQuant Method is Saved\n")
                        label.set("Method Generated")

                        themain7.destroy()

                        Label(themain, text='----->').place(x=250, y=250)
                    else:
                        mb.showerror("Error", "Please, insert a mz range with suitable window to search with it")
                mb.showinfo(title='Result', message='Result  Saved')
        except:
            mb.showerror(title='Error', message='Error, See The documentation File')

        ttk.Button(themain7, text="   Open The MasterView Result   ", command=open_PV_result).grid(row=5, column=0)
        # ttk.Button(themain7, text="   Open The Database mz file   ", command= Open_fmz_DB).grid(row=5,column=1)
        ttk.Button(themain7, text="   Run   ", command=TH_Run).grid(row=5, column=2)


        """
        count_to_stop = 0
        if count_to_stop == 0:
            while True:

                shift_str = shift.get()
                if str(shift_str) != "Example: 20" :
                    shift_str.config(foreground='black')

                Minimum_m_z_str = Minimum_m_z.get()
                if str(Minimum_m_z_str) != "Example: 50" :
                    Minimum_m_z_str.config(foreground='black')

                Maximum_m_z_str = Maximum_m_z.get()
                if str(Maximum_m_z_str) != "Example: 1100" :
                    Maximum_m_z_str.config(foreground='black')


                m_z_window_str = m_z_window.get()
                if str(m_z_window_str) != "Example: 50":
                    m_z_window_str.config(foreground='black')

                if str(shift_str) != "Example: 20" and str(Minimum_m_z_str) != "Example: 50" and str(
                            Maximum_m_z_str) != "Example: 1100" and str(m_z_window_str) != "Example: 50":
                    count_to_stop = count_to_stop + 1
                    time.sleep(5)
                break
        else:
            pass
        """

    def open_MQ():
        try:
            with open("MQpath.txt", 'r') as f:
                f = f.read()
            os.startfile(str(f))
            Label(themain, text='----->').place(x=500, y=250)
            T.insert(END, ">>> MultiQuant is Opened\n")
            label.set("MultiQuant is Opened")
            mpb["value"] = 100
        except:
            mb.showerror(title='Error.14', message='Error, Go back to The documentation')



    #####STEP 3#################
    #### Filter
    #### step1.3: open excel files

    #### make the filtration excel
    def Generate_excel_for_filtration():
        try:
            def TH_Run():
                thread.start_new_thread(Run, ())

            mpb["value"] = 0
            themain8 = Toplevel(themain)
            themain8.title('SASA')
            themain8.iconbitmap('SASAico.ico')

            def open_MQ():
                global MQ_method_file_list
                MQ_method_file_list = filedialog.askopenfilenames()
                label.set("File opened")
                T.insert(END, ">>> File Imported\n")
                mpb["value"] = 100

            varP = IntVar()
            ttk.Checkbutton(themain8, text='Ionization mode : Positive', variable=varP).grid(row=0, sticky=W)
            varN = IntVar()
            ttk.Checkbutton(themain8, text='Ionization mode : Negative', variable=varN).grid(row=1, sticky=W)

            def Run():

                for MQ_method_file in MQ_method_file_list:
                    try:
                        data_MQ = pd.read_csv(MQ_method_file, delimiter="\t")
                    except:
                        mb.showerror(title='Error.15', message='Please insert the MQ_Filteration_method file, Go back to The documentation')
                        return False

                    label.set("Loading... ")

                    if varP.get() == 1:
                        Ionization_mode = 'Positive'
                    if varN.get() == 1:
                        Ionization_mode = 'Negative'

                    mpb["value"] = 25
                    # open MQ method
                    data_MQ = pd.read_csv(MQ_method_file, delimiter="\t")
                    # exctract only what needed
                    data_MQ = data_MQ[['GroupName', 'End Mass', 'Start Mass', 'Experiment', 'Name', 'PK$PEAK_int_rel']]
                    # give the parent an id number
                    data_MQ.loc[data_MQ['PK$PEAK_int_rel'] == 'A_P', 'PK$PEAK_int_rel'] = 1000
                    data_MQ.loc[data_MQ['PK$PEAK_int_rel'] == 'AA_P', 'PK$PEAK_int_rel'] = 2000

                    # convert all to float
                    data_MQ = data_MQ.apply(pd.to_numeric, errors='ignore', downcast='float')
                    # add ionization mode
                    data_MQ['ionization mode'] = Ionization_mode

                    # D or F ?
                    data_MQ['Transition level (Sympol)'] = np.where(data_MQ['PK$PEAK_int_rel'] >= 75, 'B_D', 'C_F')
                    mpb["value"] = 50
                    # then give the 1000 = P

                    data_MQ.loc[data_MQ['PK$PEAK_int_rel'] == 1000, 'Transition level (Sympol)'] = 'A_P'
                    data_MQ.loc[data_MQ['PK$PEAK_int_rel'] == 2000, 'Transition level (Sympol)'] = 'AA_P'


                    Loading = 0
                    mpb["value"] = 80

                    data_MQ.rename(index=str, columns={"GroupName": "Metabolite ID"}, inplace=True)
                    data_MQ['Metabolite ID'] = data_MQ['Metabolite ID'].str.replace('_A', '')
                    data_MQ = data_MQ.sort_values(by=['Name', 'Transition level (Sympol)'])

                    data_MQ.loc[data_MQ['Transition level (Sympol)'] == 'B_D', 'Transition level (Sympol)'] = 'D'
                    data_MQ.loc[data_MQ['Transition level (Sympol)'] == 'C_F', 'Transition level (Sympol)'] = 'F'
                    data_MQ.loc[data_MQ['Transition level (Sympol)'] == 'A_P', 'Transition level (Sympol)'] = 'P'
                    data_MQ.loc[data_MQ['Transition level (Sympol)'] == 'AA_P', 'Transition level (Sympol)'] = 'P__'


                    ### if you found nan in PK$PEAK_int_rel this line will be the problem
                    data_MQ['PK$PEAK_int_rel'] = data_MQ['PK$PEAK_int_rel'].map({1000: 'P', 2000: 'P__'})


                    data_MQ.reset_index(inplace=True)


                    each_file_name = MQ_method_file[::-1]
                    each_file_name = each_file_name[:each_file_name.find("/")]
                    each_file_name = each_file_name[::-1]
                    each_file_name = each_file_name.replace(".csv","")
                    each_file_name = each_file_name.replace("_MQ_Filteration_method","")
                    
                    ProjectName_file_new = ProjectName_file + '/' + each_file_name + "_" + "Filtration_method.csv"

                    #ProjectName_file_new = ProjectName_file + '/' + 'Filtration_method.csv'
                    data_MQ.to_csv(ProjectName_file_new, index=False, header=True)


                    mpb["value"] = 100
                    label.set("Method Generated")
                    T.insert(END, ">>> Method is Generated\n")
                    label.set("Excel file created")
                    T.insert(END, ">>> Filtration  Method File is Generated\n")

                themain8.destroy()
                mb.showinfo(title='Result', message='Filtration Method Saved')

        except:
            mb.showerror(title='Error.16',
                        message='Something going wrong, Go back to The documentation')
            return False

        ttk.Button(themain8, text="  Import the MQ_Filteration_method  ", command=open_MQ).grid(row=2, column=1)
        ttk.Button(themain8, text="   Run   ", command=TH_Run).grid(row=2, column=2)

    ####
    def open_main_database():
        try:
            mpb["value"] = 0
            global main_excel
            global main_excel_name
            global e_sample_name
            global themain4
            global file_main_excel_name_for_final_result

            main_excel_name = askopenfilename()
            main_excel = pd.read_csv(main_excel_name)

            file_main_excel_name_for_final_result = main_excel_name.rfind("/")
            file_main_excel_name_for_final_result = main_excel_name[file_main_excel_name_for_final_result + 1:]
            file_main_excel_name_for_final_result = file_main_excel_name_for_final_result.replace(".txt_Filtration_method.csv","")
            # open Toplevel(themain)

            mpb["value"] = 100
            T.insert(END, ">>> File is imported\n")
            label.set(" File is imported")
            Label(themain, text='----->').place(x=170, y=400)
        except:
            mb.showerror("Error", "Sorry, you did not enter a valid information, please Go back to the documentation")

    ### step4: RT
    def open_RT():  # txt file
        try:
            main_excel = pd.read_csv(main_excel_name)
        except:
            mb.showerror(title='Error.17',
                        message='Please Import the Filtration method first, Go back to The documentation')
            return False
        try:
            mpb["value"] = 0  # bar
            global RT_file
            global RT_file_no_blank
            filename_RT = filedialog.askopenfilenames()
            if len(filename_RT) == 1:
                filename_RT = filename_RT[0]
                RT_file = pd.read_csv(filename_RT, sep='\t')
                RT_file.drop([0, 1], inplace=True)
            elif len(filename_RT) != 1:
                RT_file = DataFrame()

                for i_path in filename_RT:
                    RT_i = pd.read_csv(i_path, sep='\t')
                    RT_i.drop([0, 1], inplace=True)
                    RT_file = pd.concat([RT_file,RT_i],ignore_index = True, sort = False)


            if "Sample Name" in list(RT_file.columns.values):
                RT_file = RT_file.sort_values(by=['Sample Name'])
            elif "Sample.Name" in list(RT_file.columns.values):
                RT_file = RT_file.sort_values(by=['Sample.Name'])
                
            RT_file_no_blank = RT_file.drop([col for col in RT_file.columns if 'Blank' in col or "blank" in col], axis=1)

            mpb["value"] = 50

            RT_file_no_blank.fillna(0, inplace=True)
            RT_file_no_blank.reset_index(inplace=True)
            RT_file_no_blank.drop(["index"], 1, inplace=True)

            mpb["value"] = 80

            ttk.Button(themain, text="Run RT", command=TH_Run_RT).place(x=430, y=340, width=100, height=30)
            Label(themain, text='----->').place(x=370, y=345)
            mpb["value"] = 100  # bar
            label.set("The RT File is Imported")
            T.insert(END, ">>> The RT File is Imported\n")
        except:
            mb.showerror("Error", "Sorry, you did not enter a valid information, please See the documentation")

    def Run_RT():
        #try:
        global main_excel
        global RT_file
        global RT_file_no_blank
        global RT_file_no_blank_
        RT_file = RT_file.reset_index(drop=True)

        if "Sample Name" in list(RT_file_no_blank.columns.values):
            RT_file_no_blank_ = RT_file_no_blank.drop(["Sample Name"], 1)
        elif "Sample.Name" in list(RT_file_no_blank.columns.values):
            RT_file_no_blank_ = RT_file_no_blank.drop(["Sample.Name"], 1)
            
        RT_file_no_blank_ = RT_file_no_blank_.astype(float)

        mpb["value"] = 30  # bar

        RT_file_no_blank['avr_RT_sample'] = RT_file_no_blank_.mean(axis=1)

        if "Sample Name" in list(RT_file_no_blank.columns.values):
            RT_file_no_blank.rename(columns={'Sample Name': 'Name'}, inplace=True)
        
        elif "Sample.Name" in list(RT_file_no_blank.columns.values):
            
            RT_file_no_blank.rename(columns={"Sample.Name": 'Name'}, inplace=True)


        RT_file_no_blank = RT_file_no_blank[["Name", "avr_RT_sample"]]

        mpb["value"] = 70  # bar

        if "avr_RT_sample" not in main_excel.columns:
            main_excel = main_excel.merge(RT_file_no_blank, on="Name")
        else:
            main_excel.drop(["avr_RT_sample"],1, inplace=True)
            main_excel = main_excel.merge(RT_file_no_blank, on="Name")
            mb.showinfo(title='Note', message='Note!! SASA re-write the old result')

        main_excel.to_csv(main_excel_name, index=False, header=True)
        mpb["value"] = 100  # bar
        label.set("The RT is calculated")
        T.insert(END, ">>> The RT is calculated\n")
        mb.showinfo(title='Result', message='Result  Saved')
        #except:
         #   mb.showerror("Error.18", "Sorry, you did not enter a valid information, please Go back to the documentation")

    def open_width():
        try:
            main_excel = pd.read_csv(main_excel_name)
        except:
            mb.showerror(title='Error.17',
                        message='Please Import the Filtration method first, Go back to The documentation')
            return False
        
        mpb["value"] = 0  # bar
        global width_file
        global width_file_no_blank
        filename_width = filedialog.askopenfilenames()
        
        if len(filename_width) == 1:
            filename_width = filename_width[0]
            width_file = pd.read_csv(filename_width, sep='\t')
            width_file.drop([0, 1], inplace=True)
        
        elif len(filename_width) != 1:
            width_file = DataFrame()

            for i_path in filename_width:
                width_i = pd.read_csv(i_path, sep='\t')
                width_i.drop([0, 1], inplace=True)
                width_file = pd.concat([width_file,width_i],ignore_index = True, sort = False)

        if "Sample Name" in list(width_file.columns.values):
            width_file = width_file.sort_values(by=['Sample Name'])
        elif "Sample.Name" in list(width_file.columns.values):
            width_file = width_file.sort_values(by=['Sample.Name'])
            
        width_file_no_blank = width_file.drop([col for col in width_file.columns if 'Blank' in col], axis=1)
        mpb["value"] = 40
        width_file_no_blank.fillna(0, inplace=True)
        width_file_no_blank.reset_index(inplace=True)
        width_file_no_blank.drop(["index"], 1, inplace=True)
        mpb["value"] = 70
        Label(themain, text='----->').place(x=370, y=400)
        ttk.Button(themain, text="Run Width", command=TH_width_run).place(x=430, y=400, width=100, height=30)

        mpb["value"] = 100  # bar
        label.set("The Width is Imported")
        T.insert(END, ">>> The Width is Imported\n")

    def width_run():
        try:
            global main_excel
            global width_file_no_blank
            global width_file_no_blank_

            if "Sample Name" in list(width_file_no_blank.columns.values):
                width_file_no_blank_ = width_file_no_blank.drop(["Sample Name"], 1)
            elif "Sample.Name" in list(width_file_no_blank.columns.values):
                width_file_no_blank_ = width_file_no_blank.drop(["Sample.Name"], 1)
                
            width_file_no_blank_ = width_file_no_blank_.astype(float)
            mpb["value"] = 30
            width_file_no_blank['avr_width_sample'] = width_file_no_blank_.mean(axis=1)

            if "Sample Name" in list(width_file_no_blank.columns.values):
                width_file_no_blank.rename(columns={'Sample Name': 'Name'}, inplace=True)
            elif "Sample.Name" in list(width_file_no_blank.columns.values):
                width_file_no_blank.rename(columns={'Sample.Name': 'Name'}, inplace=True)
                
            width_file_no_blank = width_file_no_blank[["Name", "avr_width_sample"]]
            mpb["value"] = 70

            if "avr_width_sample" not in main_excel.columns:
                main_excel = main_excel.merge(width_file_no_blank, on="Name")
            else:
                main_excel.drop(["avr_width_sample"],1, inplace=True)
                main_excel = main_excel.merge(width_file_no_blank, on="Name")
                mb.showinfo(title='Note', message='Note!! SASA re-write the old result')

            main_excel.to_csv(main_excel_name, index=False, header=True)
            mpb["value"] = 100  # bar
            mb.showinfo(title='Result', message='Result  Saved')
            label.set("The Width is calculated")
            T.insert(END, ">>> The Width is calculated\n")
        except:
            mb.showerror("Error.19", "Sorry, you did not enter a valid information, please Go back to the documentation")


    def open_Hei():  # txt file
        try:
            main_excel = pd.read_csv(main_excel_name)
        except:
            mb.showerror(title='Error.17',
                        message='Please Import the Filtration method first, Go back to The documentation')
            return False
        try:
            mpb["value"] = 0  # bar
            global Hei_file
            global e_blank
            global themain5

            filename_Hei = filedialog.askopenfilenames()
            
            if len(filename_Hei) == 1:
                filename_Hei = filename_Hei[0]
                Hei_file = pd.read_csv(filename_Hei, sep='\t')
                Hei_file.drop([0, 1], inplace=True)
                Hei_file.fillna(0, inplace=True)

            elif len(filename_Hei) != 1:
                Hei_file = DataFrame()

                for i_path in filename_Hei:
                    Hei_i = pd.read_csv(i_path, sep='\t')
                    Hei_i.drop([0, 1], inplace=True)
                    Hei_i.fillna(0, inplace=True)
                    Hei_file = pd.concat([Hei_file,Hei_i],ignore_index = True, sort = False)

            if "Sample Name" in list(Hei_file.columns.values):
                Hei_file = Hei_file.sort_values(by=['Sample Name'])
            elif "Sample.Name" in list(Hei_file.columns.values):
                Hei_file = Hei_file.sort_values(by=['Sample.Name'])
            
            Hei_file.reset_index(inplace=True)
            Hei_file.drop(["index"], 1, inplace=True)
            mpb["value"] = 30
            Label(themain, text='----->').place(x=345, y=463)
            Label(themain, text="Sample:Blank").place(x=380, y=463)
            e_blank = ttk.Entry(themain)
            mpb["value"] = 60
            e_blank.place(x=465, y=463, width=50)
            Label(themain, text='----->').place(x=525, y=463)
            ttk.Button(themain, text=" RUN Ratio", command=TH_Run_hei).place(x=580, y=460, width=80, height=30)
            mpb["value"] = 100  # bar
            label.set("The Height File is Imported")
            T.insert(END, ">>> The Height ratio is Imported\n")
        except:
            mb.showerror("Error", "Sorry, you did not enter a valid information, please See the documentation")

    def Run_hei():
        #try:
        mpb["value"] = 0  # bar
        ##for sample
        global Hei_file
        global main_excel

        Hei_file_no_blank = Hei_file.drop([col for col in Hei_file.columns if "blank" in col or "Blank" in col], axis=1)

        if "Sample Name" in list(Hei_file_no_blank.columns.values):
            Hei_file_no_blank_ = Hei_file_no_blank.drop(["Sample Name"], 1)
        elif "Sample.Name" in list(Hei_file_no_blank.columns.values):
            Hei_file_no_blank_ = Hei_file_no_blank.drop(["Sample.Name"], 1)
            
        Hei_file_no_blank_.reset_index(inplace=True)
        Hei_file_no_blank_.drop(["index"], 1, inplace=True)
        Hei_file_no_blank_ = Hei_file_no_blank_.astype(float)
        mpb["value"] = 40
        Hei_file['avr_high_sample'] = Hei_file_no_blank_.mean(axis=1)

        ##########for blank
        Hei_file_col = [ i.lower() for i in Hei_file.columns ]
        if "Blank" in ",".join(Hei_file_col) or "blank" in ",".join(Hei_file_col):
            Hei_file_no_sample = Hei_file.drop([col for col in Hei_file.columns if 'blank' not in col], axis=1)
            if len(Hei_file_no_sample.columns) == 0:
                Hei_file_no_sample = Hei_file.drop([col for col in Hei_file.columns if 'Blank' not in col], axis=1)
            else:
                pass
           
            Hei_file_no_sample.reset_index(inplace=True)
            Hei_file_no_sample.drop(["index"], 1, inplace=True)
            Hei_file_no_sample = Hei_file_no_sample.astype(float)

            Hei_file['avr_high_blank'] = Hei_file_no_sample.mean(axis=1)
        else:
            Hei_file['avr_high_blank'] = [""]

        ###Ratio
        Hei_file["Ratio"] = Hei_file['avr_high_sample'] / (Hei_file['avr_high_blank'] + int(e_blank.get()))

        if "Sample Name" in list(Hei_file.columns.values):
            Hei_file.rename(columns={'Sample Name': 'Name'}, inplace=True)
        elif "Sample.Name" in list(Hei_file.columns.values):
            Hei_file.rename(columns={'Sample.Name': 'Name'}, inplace=True)
            
        Hei_file = Hei_file[["Name", "Ratio","avr_high_sample"]]
        if "Ratio" not in  main_excel.columns or "avr_high_sample" not in  main_excel.columns :
            main_excel = main_excel.merge(Hei_file, on="Name")
        else:
            main_excel.drop(["Ratio","avr_high_sample"],1, inplace=True)
            main_excel = main_excel.merge(Hei_file, on="Name")
            mb.showinfo(title='Note', message='Note!! SASA re-write the old result')

        mpb["value"] = 80

        main_excel.to_csv(main_excel_name, index=False, header=True)
        mpb["value"] = 100  # bar
        mb.showinfo(title='Result', message='Result Height ratio  Saved')

        label.set("The Height ratio is calculated")
        T.insert(END, ">>> The Height ratio is calculated\n")
        Label(themain, text='------>').place(x=630, y=402)
        #except:
         #   mb.showerror("Error.20", "Sorry, you did not enter a valid information, please Go back to the documentation")


    def Filter():
        try:
            main_excel = pd.read_csv(main_excel_name)
        except:
            mb.showerror(title='Error.25',message='Please Import the Filtration method first, Go back to The documentation')
            return False

        def TH_Analyse_run():
            thread.start_new_thread(Analyse_run, ())

        themain3 = Toplevel(themain)
        themain3.title('SASA')
        themain3.iconbitmap('SASAico.ico')

        e_RT = ttk.Entry(themain3)
        e_RT.grid(row=0, column=1)
        e_RT.insert(0, "Example: 0.1417")
        Label(themain3, text="   Accepted RT ").grid(row=0, column=0)

        e_width = ttk.Entry(themain3)
        e_width.grid(row=1, column=1)
        e_width.insert(0, "Example: 17.4966")
        Label(themain3, text="   Accepted Width ").grid(row=1, column=0)

        e_height = ttk.Entry(themain3)
        e_height.grid(row=2, column=1)
        e_height.insert(0, "Example: 5")
        Label(themain3, text="   Accepted Height ").grid(row=2, column=0)

        e_RT.config(foreground='gray')
        e_width.config(foreground='gray')
        e_height.config(foreground='gray')

        def Analyse_run():
            #try:
            global filter_dataframe_append

            if str(e_RT.get()) == "Example: 0.1417" or str(e_width.get()) == "Example: 17.4966" or str(e_height.get()) == "Example: 5":
                mb.showerror("Error.21",
                             "Please enter all the parameters , please Go back to the documentation")
                return False
            else:
                pass

            global main_excel
            global main_excel_name

            parent = set(main_excel['Metabolite ID'])

            Loading = 0
            filter_dataframe_append = pd.DataFrame()
            for i_parent in parent:

                Loading += 1  # loading bar
                Loading_new = len(parent) / 100  # loading bar
                mpb["value"] = math.floor(round(Loading / Loading_new, 0))  # loading bar

                filter_dataframe = pd.DataFrame()
                filter_dataframe = main_excel[main_excel['Metabolite ID'] == i_parent]
                filter_dataframe = filter_dataframe.reset_index()

                # parent RT
                for i in range(len(filter_dataframe['Transition level (Sympol)'])):
                    if filter_dataframe['Transition level (Sympol)'][i] == "P":
                        parent_RT = filter_dataframe["avr_RT_sample"][i]

                for i in range(len(filter_dataframe['Transition level (Sympol)'])):
                    if filter_dataframe['Transition level (Sympol)'][i] == "P":
                        parent_width = filter_dataframe["avr_width_sample"][i]


                #parent_RT = filter_dataframe.loc[filter_dataframe['Transition level (Sympol)'] == 'P', 'avr_RT_sample'].iloc[0]
                # parent width                #parent_width = filter_dataframe.loc[filter_dataframe['Transition level (Sympol)'] == 'P', 'avr_width_sample'].iloc[0]

                #scoring
                filter_dataframe["scoring_rt"] = abs  (parent_RT - filter_dataframe['avr_RT_sample'] )
                filter_dataframe["scoring_width"] = abs  (parent_width - filter_dataframe['avr_width_sample'] )

                filter_dataframe["scoring_rt_width"] = abs (filter_dataframe["scoring_rt"] + filter_dataframe["scoring_width"])
                #filter_dataframe["scoring"]  = (filter_dataframe["scoring_rt_width"]  - filter_dataframe["scoring_rt_width"].min()) / (filter_dataframe["scoring_rt_width"].max() - filter_dataframe["scoring_rt_width"].min())

                filter_dataframe["scoring"] = abs(filter_dataframe["scoring_rt_width"] - 1)
                # accepted RT_shift
                filter_dataframe['accepted RT'] = abs( ( (parent_RT - filter_dataframe['avr_RT_sample']) / parent_RT)) * 100

                # accepted _shift
                filter_dataframe['accepted Width'] = abs( ( (parent_width - filter_dataframe['avr_width_sample']) / parent_width)) * 100


                # del not accepted RT
                filter_dataframe = filter_dataframe[filter_dataframe['accepted RT'] < float(e_RT.get())]
                filter_dataframe = filter_dataframe[filter_dataframe['accepted Width'] < float(e_width.get())]
                filter_dataframe = filter_dataframe[filter_dataframe['Ratio'] >= float(e_height.get())]
                # del group with no

                if 'P' in list(set(filter_dataframe['Transition level (Sympol)'])) and 'D' in list(set(filter_dataframe['Transition level (Sympol)'])) :
                    filter_dataframe_append = filter_dataframe_append.append(filter_dataframe, ignore_index=True,sort=False)
                else:
                    pass

            #filter_dataframe_append.reset_index(inplace=True, drop=True)
          

            #filter_dataframe_append.drop(["scoring_rt","scoring_width","scoring_rt_width"], 1, inplace=True)
            #filter_dataframe_append['scoring'].round(decimals=2)

            try:
                filter_dataframe_append.drop(["index"], 1, inplace=True)
                filter_dataframe_append.drop(["level"], 1, inplace=True)
                filter_dataframe_append.drop(["level_0"], 1, inplace=True)
            except:
                pass

            mpb["value"] = 80
            ProjectName_file_new = ProjectName_file + '//' + f"_{file_main_excel_name_for_final_result}_final.csv"
            print(ProjectName_file_new)
            filter_dataframe_append.to_csv(ProjectName_file_new, index=False, header=True)
            mpb["value"] = 100  # bar
            mb.showinfo(title='Result', message='Result  Saved')

            label.set("The Filteration is processed")
            T.insert(END, ">>> The Filteration is processed\n")


            #except:
             #   mb.showerror("Error.22","Something going wrong , please Go back to the documentation")






        ttk.Button(themain3, text="   Run   ", command=TH_Analyse_run).grid(row=2, column=2)

        time.sleep(1)
        while True:
            if str(e_RT.get()) != "Example: 0.1417" :
                e_RT.config(foreground='black')
            if str(e_width.get()) != "Example: 17.4966" :
                e_width.config(foreground='black')
            if str(e_height.get()) != "Example: 5" :
                e_height.config(foreground='black')


            if str(e_RT.get()) != "Example: 0.1417" and str(e_width.get()) != "Example: 17.4966" and str(e_height.get()) != "Example: 5":
                e_height.config(foreground='black')
                break

    def HMDB_Q():
        #try:
        mb.showinfo(title='Note',
                    message='Note!!!,This step will only work if the accession available in HMDB ')
        filename = askopenfilename()
        try:
            final_result = pd.read_csv(filename)
        except:
            mb.showerror(title='Error.25',
                        message='Please Import a File containing the HMDB accessions id, Go back to The documentation')
            return False



        try:
            RT_H_W = final_result[["Metabolite ID", "avr_RT_sample", "avr_width_sample", "avr_high_sample","Transition level (Sympol)"]]
        except:
            RT_H_W = final_result[["Metabolite ID", "avr_RT_sample", "avr_width_sample","Transition level (Sympol)"]]

        Metabolite_ID = final_result["Metabolite ID"]

        
        Metabolite_ID = set(Metabolite_ID)
        df_HMDB = pd.DataFrame()
        Loading = 0
        for i in Metabolite_ID:
            Loading += 1  # loading bar
            Loading_new = len(Metabolite_ID) / 100  # loading bar
            mpb["value"] = math.floor(round(Loading / Loading_new, 0))  # loading bar

            i_with_out_adducts = i[:i.find("+")]
            Adduct = i[i.find("+")+1:]
            Name, Formula, location = HMDB.HMDB(i_with_out_adducts)
            df = pd.DataFrame()
            df["Metabolite ID"] = [i_with_out_adducts + "+" + Adduct]

            df["Name"] =Name
            df["Formula"] = Formula
            df["Location"] = location


            df_HMDB = df_HMDB.append(df, ignore_index=True,sort=False)


        if "avr_RT_sample" not in df_HMDB.columns or "avr_width_sample" not in df_HMDB.columns or "avr_high_sample" not in df_HMDB.columns:
            df_HMDB = df_HMDB.merge(RT_H_W, on="Metabolite ID")


           
        
        else:
            df_HMDB.drop(["avr_RT_sample", "avr_width_sample","avr_high_sample","Transition level (Sympol)"], 1, inplace=True)
            df_HMDB = df_HMDB.merge(RT_H_W, on="Metabolite ID")
            mb.showinfo(title='Note', message='Note!! SASA re-write the old result')

        #scoring
        append_df_scoring = pd.DataFrame()
        for i_id in set(final_result["Metabolite ID"]):

            df_scoring = final_result[final_result['Metabolite ID'] == i_id]
            df_scoring = df_scoring[["Metabolite ID","scoring"]]
            df_scoring["scoring%"] =  ( sum(df_scoring["scoring"])  / len(df_scoring["scoring"]) )  * 100
            df_scoring.drop(["scoring"], axis=1, inplace=True)

            append_df_scoring = append_df_scoring.append(df_scoring, ignore_index=True, sort=False)

        df_HMDB = df_HMDB.merge(append_df_scoring, on="Metabolite ID")

        df_HMDB.drop_duplicates(keep="first",inplace=True)

        mpb["value"] = 80
        ProjectName_file_new = ProjectName_file + '/' + 'HMDB.csv'

        df_HMDB.to_csv(ProjectName_file_new, index=False, header=True)
        mpb["value"] = 100
        label.set("HMDB Query processed")
        T.insert(END, ">>> HMDB Query processed\n")
        mb.showinfo(title='HMDB', message='Final Result HMDB is Saved')
        #except:
         #       mb.showerror("Error.24",
          #               "Something going wrong , please Go back to the documentation")


    ###Thread all the functions###########


    def TH_RUN_database_converter_xml():
        thread.start_new_thread(RUN_database_converter_xml, ())

    def TH_open_main_database():
        thread.start_new_thread(open_main_database, ())

    def TH_open_RT():
        thread.start_new_thread(open_RT, ())

    def TH_Run_RT():
        thread.start_new_thread(Run_RT, ())

    def TH_open_Hei():
        thread.start_new_thread(open_Hei, ())

    def TH_Run_hei():
        thread.start_new_thread(Run_hei, ())

    def TH_open_width():
        thread.start_new_thread(open_width, ())

    def TH_width_run():
        thread.start_new_thread(width_run, ())

    def TH_Filter():
        thread.start_new_thread(Filter, ())

    def TH_P_V_Method_File():
        thread.start_new_thread(P_V_Method_File, ())

    def TH_Open_MW():
        thread.start_new_thread(Open_MW, ())

    def TH_M_Q_Method_FILE():
        thread.start_new_thread(M_Q_Method_FILE, ())

    def TH_open_MQ():
        thread.start_new_thread(open_MQ, ())

    def TH_Generate_excel_for_filtration():
        thread.start_new_thread(Generate_excel_for_filtration, ())

    def TH_Insert_build_in_database():
        thread.start_new_thread(Insert_build_in_database, ())

    def TH_HMDB_Q():
        thread.start_new_thread(HMDB_Q, ())

    # step label
    Label(themain, text='Step 1:').place(x=0, y=55)
    Label(themain, text='Step 2:').place(x=0, y=153)
    Label(themain, text='Step 3:').place(x=0, y=253)
    Label(themain, text='Step 4:').place(x=0, y=395)


    step2_Frame_1 = ttk.Label(themain,text="___________DataBases___________________________________________________________________________________________________________________________________________")
    step2_Frame_1.place(x=0, y=20)


    step3_Frame_1 = ttk.Label(themain,text="___________Parents Detection__________________________________________________________________")
    step3_Frame_1.place(x=0, y=120)


    step33_Frame_1 = ttk.Label(themain,text="___________Fragments Detection_____________________________________________________________________________________________________________________")
    step33_Frame_1.place(x=0, y=220)


    step4_Frame_1 = ttk.Label(themain,text="___________Parents and Fragments Filtration____________________________________________________________________________________________________________________________________________________________________")
    step4_Frame_1.place(x=0, y=320)


    #### for step 1
    ttk.Button(themain, text="Generate Database from HMDB xml files",command=TH_RUN_database_converter_xml).place(x=280, y=50, width=250, height=30)
    Label(themain, text='OR >>> ').place(x=200, y=55)
    ttk.Button(themain, text="Select Database", command=TH_Insert_build_in_database).place(x=50, y=50,width=120, height=30)

    ## step 2
    ttk.Button(themain, text="Generate MasterView method", command=TH_P_V_Method_File).place(x=50, y=150, width=170,height=30)
    ttk.Button(themain, text="Open MasterView", command=TH_Open_MW).place(x=320, y=150, width=150, height=30)

    #step 3
    ttk.Button(themain, text="Generate MultiQuant method", command=TH_M_Q_Method_FILE).place(x=50, y=250, width=170,height=30)
    ttk.Button(themain, text="Open MultiQuant", command=TH_open_MQ).place(x=320, y=250, width=140, height=30)

    # make excel for step 4
    ttk.Button(themain, text="Generate Filtration method", command=TH_Generate_excel_for_filtration).place(x=570, y=250, width=170, height=30)

    #### for step 4
    ttk.Button(themain, text="Import Filtration\nmethod", command=TH_open_main_database).place(x=50, y=390, width=100,height=50)
    ttk.Button(themain, text="1. Import RT", command=TH_open_RT).place(x=230, y=340, width=100, height=30)
    ttk.Button(themain, text="2. Import width", command=TH_open_width).place(x=230, y=400, width=100, height=30)
    ttk.Button(themain, text="3. Import Height", command=TH_open_Hei).place(x=230, y=460, width=100, height=30)
    ttk.Button(themain, text="Filter", command=TH_Filter).place(x=695, y=400, width=100, height=30)
    ttk.Button(themain, text="HMDB Query", command=TH_HMDB_Q).place(x=900, y=400, width=100, height=30)


    ###################
    themain.mainloop()

    #####


#### for start window
tkinter.ttk.Separator(Thewindow, orient=HORIZONTAL).place(x=30, y=100,relwidth=0.9, width=-10, height=-10)

ttk.Button(Thewindow, text="   About   ", command=About).place(x=380, y=120, width=120)


ttk.Button(Thewindow, text="   Open documentation File   ", command=print('documentation')).place(x=355, y=200, width=170)

tkinter.ttk.Separator(Thewindow, orient=VERTICAL).place(x=300, y=100,relheight=0.35, width=-10, height=-10)

ttk.Button(Thewindow, text="1. Check Requirements   ", command=TH_Auto_Check).place(x=55, y=120, width=130)

ttk.Button(Thewindow, text="2. Choose Output Folder   ", command=Old_project).place(x=55, y=180, width=140)

ttk.Button(Thewindow, text="3. Start the software   ", command=everything_is_okay).place(x=55, y=240, width=120)

Thewindow.mainloop()


for proc in psutil.process_iter():
    # check whether the process name matches
    if proc.name() == "SASA.exe":
        proc.kill()
    else:
        pass
