import datetime
import time
import os
import re
import shutil
import pathlib
import calendar

d = datetime.datetime.now().replace(microsecond=0)

scriptname = re.search(".*\\\(.*)\.", __file__).group(1)
logsdir = os.path.join(r"D:\automation\logs", scriptname)
if not os.path.exists(logsdir):
    os.mkdir(logsdir)

logname = logsdir + "\\" + scriptname + d.strftime("%Y-%m-%d_%H-%M") + '.txt'
log = None

#sortfolder = r"C:\Users\yagni\Downloads"
sortfolder = r"D:\automation\test"

def pure_path(p):
    return pathlib.PureWindowsPath(p).as_posix()
def remove_outdated_logs(threshold):
    list_of_files = os.listdir(logsdir)

    printed_something = False
    while len(list_of_files) > threshold:
        full_path = [logsdir + r'/{0}'.format(x) for x in list_of_files]
        oldest_file = min(full_path, key=os.path.getctime)
        os.remove(oldest_file)
        oldest_file_name = re.search("/(.*$)", oldest_file).group(1)
        list_of_files.remove(oldest_file_name)
        log.write(f"Removing outdated log => {pure_path(oldest_file_name)}\n")
        printed_something = True
    if printed_something:
        log.write("\n")

def remove_html_files():
    list_of_files = os.listdir(sortfolder)
    # 10 minutes
    max_existance_time = 0

    print(list_of_files)
    full_path = [(sortfolder + r'/{0}'.format(x)) for x in list_of_files]
    html_files = list(filter(lambda file: pathlib.Path(file).suffix == ".html", full_path))
    for file in html_files:
        minutes_since_creation = int((time.time() - os.path.getmtime(file))/60)
        print (minutes_since_creation)
        # if file is older than x minutes
        if minutes_since_creation > max_existance_time:
            html_file_folder = re.search("(.*)\.", file).group(1) + "_files"
            log.write(f"Removing outdated ({minutes_since_creation} minutes old) HTML file and its folder:\n")

            if os.path.isfile(file):
                os.remove(file)
                log.write(pure_path(file) + "\n")
            if os.path.isdir(html_file_folder):
                shutil.rmtree(html_file_folder)
                log.write(pure_path(html_file_folder) + "\n\n")


def move_work_timetables():
    list_of_files = os.listdir(sortfolder)
    # 60 minutes
    max_existance_time = 45

    timetabes_folder = r'D:\work\timetables'

    full_path = [(sortfolder + r'/{0}'.format(x)) for x in list_of_files]
    xlsx_files = list(filter(lambda file: re.search("Maksym.*\d\.xlsx$", file), full_path))
    for file in xlsx_files:
        day = datetime.datetime.strptime(file[-13:-5], "%Y%m%d")
        if day.weekday() != 0:
            log.write(f'Given file is not starting on monday => {file}\n\n')
        else:
            destination_year = os.path.join(timetabes_folder, str(day.year))
            if not os.path.exists(destination_year):
                os.mkdir(destination_year)
            destination_month = os.path.join(destination_year, calendar.month_name[int(day.month)])
            if not os.path.exists(destination_month):
                os.mkdir(destination_month)
            filename = re.search(".*/(.*\.xlsx)$", file).group(1)
            final_destination = os.path.join(destination_month, filename)
            shutil.move(file, final_destination)
            log.write(f'Moved timetable:\n')
            log.write(f'{pure_path(file)} => {pure_path(final_destination)}\n\n')

if __name__ == '__main__':
    log = open(logname, 'w', encoding='utf-8')

    log.write(f'Started download folder sorting on {d}\n\n')

    # Keep max 24 files
    remove_outdated_logs(8)

    remove_html_files()

    move_work_timetables()

    log.close()