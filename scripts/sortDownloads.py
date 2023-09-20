import datetime
import time
import os
import re
import shutil
import pathlib
import calendar
import send2trash
import ntpath

d = datetime.datetime.now().replace(microsecond=0)

scriptname = os.path.splitext(ntpath.basename(__file__))[0]
logsdir = os.path.join(r"D:\automationScripts\logs", scriptname)
if not os.path.exists(logsdir):
    os.mkdir(logsdir)

logname = os.path.join(logsdir, scriptname + d.strftime("%Y-%m-%d_%H-%M") + '.txt')
log = None

testing = False

#sortfolder = r"C:\Users\yagni\Downloads"
sortfolder = r"D:\automationScriptsTestFiles"
def pure_posix_path(p):
    return pathlib.PureWindowsPath(p).as_posix()
def pure_windows_path(p):
    return pathlib.PureWindowsPath(p)

def completely_remove(p):
    if not testing:
        try:
            if os.path.isdir(p):
                shutil.rmtree(p)
            elif os.path.isfile(p):
                os.remove(p)
            else:
                log.write("\nError::unknown file type: " + p + "\n")
        except:
            log.write("\nError::problem when deleting: " + p + "\n")
def to_recycle_bin(p):
    if not testing:
        try:
            send2trash.send2trash(pure_windows_path(p))
        except:
            log.write("\nError::problem when deleting: " + p + "\n")

def move(src_file, dest_folder):
    filename = ntpath.basename(src_file)
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    if not testing:
        # copy and then move to recycle bin
        shutil.copy(src_file, os.path.join(dest_folder, filename))
        to_recycle_bin(src_file)
def remove_outdated_logs():
    list_of_files = os.listdir(logsdir)

    max_logs_amount = 8

    printed_something = False
    while len(list_of_files) > max_logs_amount:
        full_path = [logsdir + r'/{0}'.format(x) for x in list_of_files]
        oldest_file = min(full_path, key=os.path.getctime)
        oldest_file_name = ntpath.basename(oldest_file)

        log.write(f"Removing outdated log file => {oldest_file_name}\n")
        printed_something = True

        completely_remove(oldest_file)
        list_of_files.remove(oldest_file_name)

    if printed_something:
        log.write("\n")

def remove_html_files():
    list_of_files = os.listdir(sortfolder)

    # in minutes
    max_existance_time = 10

    full_path = [(sortfolder + r'/{0}'.format(x)) for x in list_of_files]
    html_files = list(filter(lambda file: pathlib.Path(file).suffix == ".html", full_path))
    printed_something = False
    for file in html_files:
        minutes_since_creation = int((time.time() - os.path.getmtime(file))/60)
        # if file is older than x minutes
        if minutes_since_creation >= max_existance_time:
            html_file_folder = os.path.splitext(file)[0] + "_files"

            log.write(f"Removing outdated ({minutes_since_creation} minutes old) HTML file and its folder:\n")
            printed_something = True

            log.write(pure_posix_path(file) + "\n")
            completely_remove(file)

            log.write(pure_posix_path(html_file_folder) + "\n")
            completely_remove(html_file_folder)

    if printed_something:
        log.write("\n")


def sort_work_timetables():
    list_of_files = os.listdir(sortfolder)

    # in minutes
    max_existance_time = 45

    timetabes_folder = r'D:\work_timetables'

    full_path = [(sortfolder + r'/{0}'.format(x)) for x in list_of_files]
    timetables = list(filter(lambda file: re.search("Maksym.*\d\.xlsx$", ntpath.basename(file)), full_path))
    printed_something = False
    for file in timetables:
        printed_something = True
        try:
            day = datetime.datetime.strptime(file[-13:-5], "%Y%m%d")
        except:
            log.write("Error::problems when converting timetable date: " + file + "\n\n")
            return
        if day.weekday() != 0:
            log.write(f'Error::timetable is not starting on monday => {file}\n\n')
        else:
            minutes_since_creation = int((time.time() - os.path.getmtime(file)) / 60)
            # if file is older than x minutes
            if minutes_since_creation >= max_existance_time:
                destination_year = os.path.join(timetabes_folder, str(day.year))
                destination_month = os.path.join(destination_year, calendar.month_name[int(day.month)])

                log.write(f'Moving timetable:\n')
                final_destination = os.path.join(destination_month, ntpath.basename(file))
                log.write(f'{pure_posix_path(file)} => {pure_posix_path(final_destination)}\n')

                move(file, destination_month)

    if printed_something:
        log.write("\n")

    # manage rest of the timetables
    rest_of_timetables = list(filter(lambda file: re.search("Maksym.*\)\.xlsx$", ntpath.basename(file)), full_path))
    printed_something = False
    for file in rest_of_timetables:
        minutes_since_creation = int((time.time() - os.path.getmtime(file))/60)
        # if file is older than x minutes
        if minutes_since_creation >= max_existance_time:
            printed_something = True
            log.write(f"Removing duplicate timetable:\n")
            if os.path.isfile(file):
                log.write(pure_posix_path(file) + "\n")
                to_recycle_bin(pure_windows_path(file))
            else:
                log.write(f"Error::timetable is not file: " + file + "\n")

    if printed_something:
        log.write("\n")
        
def sort_work_invoices():
    pass

if __name__ == '__main__':
    log = open(logname, 'w', encoding='utf-8')

    log.write(f'Started download folder sorting on {d}\n\n')

    remove_outdated_logs()

    remove_html_files()

    sort_work_timetables()

    log.write(f'Finished download folder sorting.\n')
    log.close()