import datetime
import time
import os
import re
import shutil
import pathlib
import calendar

d = datetime.datetime.now().replace(microsecond=0)

scriptname = re.search(".*\\\(.*)\.", __file__).group(1)
logsdir = os.path.join(r"D:\automationScripts\logs", scriptname)
if not os.path.exists(logsdir):
    os.mkdir(logsdir)

logname = logsdir + "\\" + scriptname + d.strftime("%Y-%m-%d_%H-%M") + '.txt'
log = None

testing = True

#sortfolder = r"C:\Users\yagni\Downloads"
sortfolder = r"D:\automationScriptsTestFiles"
def pure_path(p):
    return pathlib.PureWindowsPath(p).as_posix()
def remove_outdated_logs():
    list_of_files = os.listdir(logsdir)

    max_logs_amount = 8

    printed_something = False
    while len(list_of_files) > max_logs_amount:
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
    max_existance_time = 10

    full_path = [(sortfolder + r'/{0}'.format(x)) for x in list_of_files]
    html_files = list(filter(lambda file: pathlib.Path(file).suffix == ".html", full_path))
    printed_something = False
    for file in html_files:
        minutes_since_creation = int((time.time() - os.path.getmtime(file))/60)
        # if file is older than x minutes
        if minutes_since_creation >= max_existance_time:
            html_file_folder = re.search("(.*)\.", file).group(1) + "_files"
            log.write(f"Removing outdated ({minutes_since_creation} minutes old) HTML file and its folder:\n")
            printed_something = True
            if os.path.isfile(file):
                if not testing:
                    os.remove(file)
                log.write(pure_path(file) + "\n")
            if os.path.isdir(html_file_folder):
                if not testing:
                    shutil.rmtree(html_file_folder)
                log.write(pure_path(html_file_folder) + "\n")
    if printed_something:
        log.write("\n")


def move_work_timetables():
    list_of_files = os.listdir(sortfolder)
    # 60 minutes
    max_existance_time = 45

    timetabes_folder = r'D:\work\timetables'

    full_path = [(sortfolder + r'/{0}'.format(x)) for x in list_of_files]
    timetables = list(filter(lambda file: re.search("Maksym.*\d\.xlsx$", file), full_path))
    printed_something = False
    for file in timetables:
        printed_something = True
        try:
            day = datetime.datetime.strptime(file[-13:-5], "%Y%m%d")
        except:
            log.write("Problems converting timetable date: " + file + "\n\n")
            return
        if day.weekday() != 0:
            log.write(f'Given file is not starting on monday => {file}\n\n')
        else:
            minutes_since_creation = int((time.time() - os.path.getmtime(file)) / 60)
            # if file is older than x minutes
            if minutes_since_creation >= max_existance_time:
                destination_year = os.path.join(timetabes_folder, str(day.year))
                if not os.path.exists(destination_year):
                    os.mkdir(destination_year)
                destination_month = os.path.join(destination_year, calendar.month_name[int(day.month)])
                if not os.path.exists(destination_month):
                    os.mkdir(destination_month)
                filename = re.search(".*/(.*\.xlsx)$", file).group(1)
                final_destination = os.path.join(destination_month, filename)
                if not testing:
                    shutil.move(file, final_destination)
                log.write(f'Moving timetable:\n')
                log.write(f'{pure_path(file)} => {pure_path(final_destination)}\n')

    if printed_something:
        log.write("\n")

    # manage rest of the timetables
    rest_of_timetables = list(filter(lambda file: re.search("Maksym.*\)\.xlsx$", file), full_path))
    printed_something = False
    for file in rest_of_timetables:
        minutes_since_creation = int((time.time() - os.path.getmtime(file))/60)
        # if file is older than x minutes
        if minutes_since_creation >= max_existance_time:
            printed_something = True
            log.write(f"Removing duplicate timetable:\n")
            if os.path.isfile(file):
                if not testing:
                    os.remove(file)
                log.write(pure_path(file) + "\n")

    if printed_something:
        log.write("\n")

if __name__ == '__main__':
    log = open(logname, 'w', encoding='utf-8')

    log.write(f'Started download folder sorting on {d}\n\n')

    remove_outdated_logs()

    remove_html_files()

    move_work_timetables()

    log.write(f'Finished download folder sorting.\n')
    log.close()