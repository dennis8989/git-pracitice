import datetime
import hashlib
import os
import re
import time

from colorama import init, Fore
from requests import get

from tkinter import *
from tkinter import filedialog
init(autoreset=True)
#Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
root = Tk()
root.withdraw()


def again(selection, model):

    os.system("cls")
    if selection == "B":
        main(model)
    elif selection == "S":
        main()
    else:
        exit()
def check_md5(path):
    MD5 = path + "\\" + "MD5.txt"
    CODES = ['UTF-8', 'UTF-16', 'GB18030', 'BIG5']
    for code in CODES:
        try:
            with open(MD5, "r", encoding=code) as f:
                md5 = f.read()
                break
        except:
            pass
    list_file = os.listdir(path)

    for file in list_file:
        if file != "MD5.txt":
            print(file + "...", end="", flush=True)
            file_path = path + "\\" + file
            with open(file_path, "rb") as f:
                m = hashlib.md5()
                buf = f.read()
                m.update(buf)
                h = m.hexdigest()
                # print(re.search(h, md5).group())
            if re.search(h, md5, re.I):
                print("...PASS")
            else:
                print(Fore.RED+'\r' + f'{file}......CHECKSUM FAIL')
                print(Fore.RED+f"can't find CHECKSUM {h.upper()}")
    print("\n")


def download(url, filename, filesize, path):
    # start =time.time()
    r = get(url, stream=True, timeout=3000)
    if int(filesize) > 0:
        with open(path + filename, 'wb') as f:
            iter = 0
            total = int(filesize)
            block = 1 if total < 50 else int(total / 100)
            length = 20
            try:
                for data in r.iter_content(block):
                    f.write(data)
                    iter += 1
                    if iter * block / total > 0.99:
                        percent = 1
                    else:
                        percent = iter * block / total
                    print('\r' + f'{filename[:30]}...' + '[Progress]:[%s%s]%d%%' % (
                        '*' * round(length * percent), ' ' * round((length * (1 - percent))),
                        round(100 * percent)), end='')
                if percent !=1:
                    print('\r' + f'{filename}......download fail')
                elif percent == 1:
                    print('\r' + ' '*80, end='')
                    print('\r' + f'{filename}......' + '[SUCCESS]:%d%%' % (round(100 * percent)))
            except:
                print('\r' + ' ' * 80, end='')
                print(Fore.RED+'\r' + f'{filename}......download fail')
    else:
        # print(filename)
        with open(path + filename, 'wb') as f:
            f.write(r.content)
        print('\r' + f'{filename}......' + '[SUCCESS]:%d%%' % (100))
    # end = time.time()
    # print(end-start)


def get_dict_category(product):
    url = f"https://apis-corp.advantech.com/api/v1/search/documents/support?q={product}&lang=zh-TW&use_fuzzy=false"
    page_content = get(url)
    dict_download_page = page_content.json()
    dict_download_page_doc = dict_download_page['documents']
    dict_category = {}
    for item in dict_download_page_doc:
        if not dict_category.get(item["typeSecond"]):
            dict_category[item["typeSecond"]] = [item]
        else:
            dict_category[item["typeSecond"]] = dict_category.get(item["typeSecond"]) + [item]
    return dict_category


def show_download_item(dict_category):
    item_number = 0
    list_item_values = []
    list_item_show = ["Driver", "Software API", "Datasheet", "Manual"]
    for item_key, list_item_value in dict_category.items():
        if item_key in list_item_show:
            item_number += 1
            list_item_values.append(list_item_value)
            print(f"{item_number}. {item_key}")
    return list_item_values, item_number



def find_solutions(list_item_value):
    list_solutions = []
    for dict_item_value in list_item_value:
        id = dict_item_value["id"]
        dict_driver_data = get('https://apis-corp.advantech.com/api/support/documentdetail?document_id=' + id).json()
        for solution in dict_driver_data['solutions']:
            list_solutions.append(solution)
    return list_solutions
#dict_solutions
{'documentId': '99ba157e-9a07-42cd-8233-10a77c5ba506', 'documentNo': '99ba157e-9a07-42cd-8233-10a77c5ba506',
 'documentType': 'Download', 'documentCategory': 'Datasheet', 'abstract': 'AIMB-787_DS(081821).pdf',
 'createDate': '2021-08-19T10:44:18.27', 'updateDate': '2021-08-19T10:44:18.27', 'os': [], 'partNo': [], 'solutions': [
    {'name': 'AIMB-787_DS(081821).pdf', 'description': None, 'files': [
        {'fileId': None, 'fileName': 'AIMB-787_DS(081821).pdf', 'fileExt': None, 'fileDescription': None,
         'fileSize': 0.0, 'displayName': 'AIMB-787_DS(081821).pdf.',
         'primaryUrl': 'https://downloadt.advantech.com/download/downloadlit.aspx?LIT_ID=99ba157e-9a07-42cd-8233-10a77c5ba506',
         'secondaryUrl': None, 'releaseDate': '0001-01-01T00:00:00', 'createDate': '0001-01-01T00:00:00'}]}]}

def ask_download_solution(list_item_value):
    list_solutions = [] #os
    for dict_item_value in list_item_value:
        id = dict_item_value["id"]
        dict_solutions = get('https://apis-corp.advantech.com/api/support/documentdetail?document_id=' + id).json()
        list_solutions.append(dict_solutions)
        # for solution in dict_driver_data['solutions']:
        #     list_solutions.append(solution)
    n = 0
    solutions = []
    for dict_solutions in list_solutions:
        for solution in dict_solutions['solutions']:
            solutions.append(solution)
            n += 1
            name = solution['name']
            print(f"{n}. {name}")
    print(Fore.CYAN+'\n[A]download all. [B]Back to main menu. [S]Search other model. [E]Exit.\n'+Fore.WHITE)
    return list_solutions, solutions





def download_driver(model, type, solutions_select, path_source):
    # print('Plese select download folder')
    # root = Tk()
    # root.withdraw()
    # path_source = filedialog.askdirectory()

    path_source.replace('/',r'\\')
    for solution in solutions_select:
        if type in ['Datasheet', 'Manual']:
            name_os =  type
        else:
            name_os = solution['name']
            name_os = re.sub(r"\/", "_", name_os)
        # name_os = "{osname}".format(osname=solution['name'])
        # print(name_os[-3:])
        # path = f".\\{model}\\{name_os}\\" if name_os[-3:] == r".pdf" else f".\\{model}\\DS and UMN\\"
        path = f".\\{model}\\{name_os}\\"
        path = f"{path_source}\\{model}\\{name_os}\\"
        # path = r".\\{model}\\{name_os}\\".format(model=model,name_os=name_os)
        if not os.path.isdir(path): os.makedirs(path)
        print(Fore.YELLOW+f"Start to download {name_os}")
        list_files = solution['files']
        for file in list_files:
            url = file['primaryUrl']
            # print(file)
            # print(url)
            # if name_os[-4:] == ".pdf":
            #     filename = name_os
            # else:
            #     filename = re.sub(" ", "_", file['displayName']).rsplit("_", maxsplit=1)[0]
            # print(path)
            if name_os in ['Datasheet', 'Manual']:
                filename =  file['fileName'] if file['fileName'][-3:] == 'pdf' else file['fileName'] + '.pdf'
            else:
                filename = file['fileName']+"." + file['fileExt']
            filesize = int(file['fileSize'])
            download(url, filename, filesize, path)
        if os.path.isfile(path + "MD5.txt"):
            print("\nstart to check MD5")
            check_md5(path)
        else:
            pass


def main(model=None):
    time.sleep(0.5)
    os.system("cls")
    print("ADV_GetDriver V1.4")
    # path_source = filedialog.askdirectory()


    if not model:
        model = input("Please input model name\n")

    deadline = datetime.datetime(2022, 8, 31) # -------------------------------------------------deadline
    today = datetime.datetime.today()
    if today > deadline:
        print(Fore.YELLOW+'Can\' find the product')
        input("please enter any key to exit")
        exit()
    # --------------------------------------------------------------------------------------check if model can be found
    while True:
        dict_category = get_dict_category(model) # get download category
        if dict_category != {}:
            break
        else:
            print(Fore.YELLOW+"can't find the model")
            os.system("cls")
            main()
    #-------------------------------------------------------------------------------------------------------------------

    #------------------------------------ask category-------------------------------------------------------------------
    os.system("cls")
    print(Fore.YELLOW+f"Result for {model}")
    list_item_values, item_number = show_download_item(dict_category) # show category ["Driver", "Software API", "Datasheet", "Manual"]
    #list_item_value
    [{'id': '1-216IJ4E', 'typeTop': 'TechnicalDownloads', 'typeSecond': 'Software API', 'language': 'en-us',
      'title': 'SUSI for ASMB-787', 'highlightTitle': '', 'abstract': None, 'highlightAbstract': None,
      'description': None, 'highlightDescription': None, 'url': '/support/details/software-api?id=1-216IJ4E',
      'imageUrl': '', 'lastUpdate': '2021-01-28T05:11:13', 'properties': None},
     {'id': '1-1YM2PJD', 'typeTop': 'TechnicalDownloads', 'typeSecond': 'Software API', 'language': 'en-us',
      'title': 'SUSI for AIMB-787', 'highlightTitle': '', 'abstract': None, 'highlightAbstract': None,
      'description': None, 'highlightDescription': None, 'url': '/support/details/software-api?id=1-1YM2PJD',
      'imageUrl': '', 'lastUpdate': '2021-03-10T05:57:37', 'properties': None},
     {'id': '1-21WF2RP', 'typeTop': 'TechnicalDownloads', 'typeSecond': 'Software API', 'language': 'en-us',
      'title': 'iBMC and DeviceOn', 'highlightTitle': '', 'abstract': None, 'highlightAbstract': None,
      'description': None, 'highlightDescription': None, 'url': '/support/details/software-api?id=1-21WF2RP',
      'imageUrl': '', 'lastUpdate': '2021-03-23T02:42:20', 'properties': None}]
    while True:  # ask  answer for download category ["Driver", "Software API", "Datasheet", "Manual"]
        selection = input('Please select download item.'+Fore.CYAN+'\n\n[B]Back to main menu. [S]Search other model. ['
                                        'E]Exit.\n'+Fore.WHITE)
        if selection.isnumeric() and int(selection) in range(1, item_number + 1):
            list_item_value = list_item_values[int(selection) - 1]
            break
        elif re.match("B|S|E", selection, re.I):
            again(selection, model)
#----------------------------------------------------------------------------------------------------------------------
#---------------------------------ask OS ------------------------------------------------------------------------------
    # list_solutions = find_solutions(list_item_value)
    # print(list_solutions)
    os.system("cls")
    list_solutions, solutions = ask_download_solution(list_item_value)
    while True:
        selection = input("Which one you want to download?\n")
        if selection.isnumeric() and int(selection) in range(1, len(solutions) + 1):
            # list_solution_select = [list_solutions[int(selection) - 1]]
            solutions_select = [solutions[int(selection) - 1]]
            break
        elif selection == "A":
            # list_solution_select = list_solutions
            solutions_select = solutions
            break

        else:
            again(selection, model)
            break
    os.system("cls")

#------------------------------download driver--------------------------------------------------------------------------
    type = list_solutions[0]['documentCategory']
    time.sleep(0.5)
    try:
        path_source = filedialog.askdirectory()
    except:
        path_source = '.'
    os.system("cls")
    print(path_source)
    download_driver(model, type, solutions_select, path_source)

    while True:
        selection = input(Fore.CYAN+'\n[B]Back to main menu. [S]Search other model. [E]Exit.\n'+Fore.WHITE)
        if re.match("B|S|E", selection, re.I):
            again(selection, model)
#----------------------------------------------------------------------------------------------------------------------
def start():
    try:

        main()
    except Exception as e:
        print(e)
        x = input("press any key to continue")
        model = ""
        start()
start()


#pyinstaller -F --name ADV_GetDriver getdriver_by_requests.py
