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
# Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
root = Tk()
root.withdraw()


class advGetDriver():
    def __init__(self, model) -> None:
        self.model = model.strip()
        self.dict_category = {}
        self.list_item_values = []
        self.list_solutions = []
        self.ask_download_directory = False

    def run(self):
        self.deadline().get_dict_category(
            self.model).show_download_item().ask_download_solution()
        # self.get_dict_category(self.model)
        # print(self.dict_category)
        # self.show_download_item()
        # self.ask_download_solution()

    def deadline(self):
        # -------------------------------------------------deadline
        deadline = datetime.datetime(2022, 8, 31)
        today = datetime.datetime.today()
        if today > deadline:
            print(Fore.YELLOW+'Can\' find the product')
            input("please enter any key to exit")
            exit()
        return self

    def get_dict_category(self, product):
        while True:
            url = f"https://apis-corp.advantech.com/api/v1/search/documents/support?q={product}&lang=zh-TW&use_fuzzy=false"
            page_content = get(url)
            dict_download_page = page_content.json()
            dict_download_page_doc = dict_download_page['documents']
            self.dict_category = {}
            for item in dict_download_page_doc:
                if not self.dict_category.get(item["typeSecond"]):
                    self.dict_category[item["typeSecond"]] = [item]
                else:
                    self.dict_category[item["typeSecond"]] = self.dict_category.get(
                        item["typeSecond"]) + [item]
            if self.dict_category != {}:
                break
            else:
                print(Fore.YELLOW+"can't find the model")
                time.sleep(2)
                os.system("cls")
                main()
        return self

    def show_download_item(self):
        os.system("cls")
        print(Fore.YELLOW + f"Result for {self.model}")

        list_item_show = ["Driver", "Software API", "Datasheet", "Manual"]
        item_number = 0
        for item_key, list_item_value in self.dict_category.items():
            if item_key in list_item_show:
                item_number += 1
                self.list_item_values.append(list_item_value)
                print(f"{item_number}. {item_key}")
        # ask  answer for download category ["Driver", "Software API", "Datasheet", "Manual"]
        while True:
            selection = ''
            selection = input(
                'Please select download item.' + Fore.CYAN +
                '\n\n[B]Back to main menu. [S]Search other model. ['
                'E]Exit.\n' + Fore.WHITE)
            if selection.isnumeric() and int(selection) in range(1, item_number + 1):
                self.list_item_value = self.list_item_values[int(
                    selection) - 1]
                break
            else:
                self.again(selection)
                # self.item_number = 0
                # self.show_download_item()
        return self

    def find_solutions(list_item_value):
        list_solutions = []
        for dict_item_value in list_item_value:
            id = dict_item_value["id"]
            dict_driver_data = get(
                'https://apis-corp.advantech.com/api/support/documentdetail?document_id=' + id).json()
            for solution in dict_driver_data['solutions']:
                list_solutions.append(solution)
        return list_solutions

    def ask_download_solution(self):
        os.system("cls")
        list_solutions = []  # os
        for dict_item_value in self.list_item_value:
            id = dict_item_value["id"]
            try:
                dict_solutions = get(
                    'https://apis-corp.advantech.com/api/support/documentdetail?document_id=' + id).json()
                list_solutions.append(dict_solutions)
            except:
                pass
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
        print(
            Fore.CYAN+'\n[A]download all. [B]Back to main menu. [S]Search other model. [E]Exit.\n'+Fore.WHITE)
        while True:
            selection = input("Which one you want to download?\n")
            if selection.isnumeric() and int(selection) in range(1, len(solutions) + 1):
                # list_solution_select = [list_solutions[int(selection) - 1]]
                solutions_select = [solutions[int(selection) - 1]]
                break
            elif selection.upper() == "A":
                # list_solution_select = list_solutions
                solutions_select = solutions
                break

            else:
                self.again(selection)
                n = 0
                self.ask_download_solution()
        os.system("cls")

        type = list_solutions[0]['documentCategory']
        time.sleep(0.5)

        if self.ask_download_directory is True:
            try:
                path_source = filedialog.askdirectory()
            except:
                path_source = '.'
        else:
            path_source = '.'
        os.system("cls")
        # print(path_source)
        self.download_driver(type, solutions_select, path_source)
        return self

    def download_driver(self, type, solutions_select, path_source):
        path_source.replace('/', r'\\')
        for solution in solutions_select:
            if type in ['Datasheet', 'Manual']:
                name_os = type
            else:
                name_os = solution['name']
                name_os = re.sub(r"\/", "_", name_os)
                name_os = name_os.strip()

            # name_os = "{osname}".format(osname=solution['name'])
            # print(name_os[-3:])
            # path = f".\\{model}\\{name_os}\\" if name_os[-3:] == r".pdf" else f".\\{model}\\DS and UMN\\"
            # path = f".\\{self.model}\\{name_os}\\"
            path = f"{path_source}\\{self.model}\\{name_os}\\"
            # print(path)
            # path = r".\\{model}\\{name_os}\\".format(model=model,name_os=name_os)
            if not os.path.isdir(path):
                os.makedirs(path)
            print(Fore.YELLOW+f"Start to download {name_os}")
            list_files = solution['files']
            for file in list_files:
                url = file['primaryUrl']
                if name_os in ['Datasheet', 'Manual']:
                    filename = file['fileName'] if file['fileName'][-3:
                                                                    ] == 'pdf' else file['fileName'] + '.pdf'
                else:
                    filename = file['fileName']+"." + file['fileExt']
                filesize = int(file['fileSize'])
                self.download(url, filename, filesize, path)
            if os.path.isfile(path + "MD5.txt"):
                print("\nstart to check MD5")
                self.check_md5(path)
            else:
                pass
        while True:
            selection = input(
                Fore.CYAN + '\n[B]Back to main menu. [S]Search other model. [E]Exit.\n' + Fore.WHITE)
            
            self.again(selection)
            # self.download_driver(type, solutions_select, path_source)

    def check_md5(self, path):
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

    def download(self, url, filename, filesize, path):
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
                            '*' * round(length * percent), ' ' *
                            round((length * (1 - percent))),
                            round(100 * percent)), end='')
                    if percent != 1:
                        print('\r' + f'{filename}......download fail')
                    elif percent == 1:
                        print('\r' + ' '*80, end='')
                        print('\r' + f'{filename}......' +
                              '[SUCCESS]:%d%%' % (round(100 * percent)))
                except:
                    print('\r' + ' ' * 80, end='')
                    print(Fore.RED+'\r' + f'{filename}......download fail')
        else:
            # print(filename)
            with open(path + filename, 'wb') as f:
                f.write(r.content)
            print('\r' + f'{filename}......' + '[SUCCESS]:%d%%' % (100))

    def again(self, selection):
        # os.system("cls")
        if selection.upper() == "B":
            os.system("cls")
            advGetDriver(self.model).run()
        elif selection.upper() == "S":
            os.system("cls")
            main()
        elif selection.upper() == "E":
            os._exit(0)
        else:
            pass


def main(model=None):

    time.sleep(0.5)
    # os.system("cls")
    print("ADV_GetDriver V1.6")
    # path_source = filedialog.askdirectory()
    model = ''
    while True:
        model = input("Please input model name\n")
        if not model or len(model) < 2:
            print("At least 3 words!")
        else:
            break

    # advGetDriver1 = advGetDriver(model)
    try:
        advGetDriver(model).run()
    except Exception as e:
        print(e)
        x = input("press any key to continue")


main()
#pyinstaller -F --name ADV_GetDriver ADV_GetDriver_classMode.py