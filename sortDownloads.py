import datetime
import time
import os
import re
import pathlib
import ntpath
import calendar
import getpass

from modules.dirclean import dirclean

script_name = os.path.splitext(ntpath.basename(__file__))[0]
logs_dir = f'D:\\automationScripts\\logs\\{script_name}'

def start_log(d, logs_dir, script_name):
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    log_name = os.path.join(logs_dir, script_name + d.strftime("%Y-%m-%d_%H-%M") + '.txt')
    return open(log_name, 'w', encoding='utf-8')


log = None
cleaner = None

downloads_folder = r"C:\Users\\"+getpass.getuser()+"\Downloads"
def remove_html_files():
    list_of_files = os.listdir(downloads_folder)

    # in minutes
    min_existence_time = 20

    full_path = [(downloads_folder + r'/{0}'.format(x)) for x in list_of_files]
    html_files = list(filter(lambda file: pathlib.Path(file).suffix == ".html", full_path))
    printed_something = False
    for file in html_files:
        minutes_since_creation = int((time.time() - os.path.getmtime(file))/60)
        # if file is older than x minutes
        if minutes_since_creation >= min_existence_time:
            html_file_folder = os.path.splitext(file)[0] + "_files"

            log.write(f"Removing outdated ({minutes_since_creation} minutes old) HTML file and its folder:\n")
            printed_something = True

            log.write(cleaner.pure_posix_path(file) + "\n")
            cleaner.completely_remove(file)

            log.write(cleaner.pure_posix_path(html_file_folder) + "\n")
            cleaner.completely_remove(html_file_folder)

    if printed_something:
        log.write("\n")


def sort_work_timetables(min_existence_time = 45):
    timetables_folder = r'D:\work_timetables'

    timetables = list(filter(lambda file: re.search("Maksym.*\d\.xlsx$", file), os.listdir(downloads_folder)))
    timetables = [(downloads_folder + r'/{0}'.format(x)) for x in timetables]
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
            if minutes_since_creation >= min_existence_time:
                destination_year = os.path.join(timetables_folder, str(day.year))
                destination_month = os.path.join(destination_year, calendar.month_name[int(day.month)])

                log.write(f'Moving timetable:\n')
                final_destination = os.path.join(destination_month, ntpath.basename(file))
                log.write(f'{cleaner.pure_posix_path(file)} => {cleaner.pure_posix_path(final_destination)}\n')

                cleaner.move(file, destination_month)

    if printed_something:
        log.write("\n")

    # manage rest of the timetables
    rest_of_timetables = list(filter(lambda file: re.search("Maksym.*\)\.xlsx$", file), os.listdir(downloads_folder)))
    rest_of_timetables = [(downloads_folder + r'/{0}'.format(x)) for x in rest_of_timetables]
    printed_something = False
    for file in rest_of_timetables:
        minutes_since_creation = int((time.time() - os.path.getmtime(file))/60)
        # if file is older than x minutes
        if minutes_since_creation >= min_existence_time:
            printed_something = True
            log.write(f"Moving timetable to recycle bin:\n")
            if os.path.isfile(file):
                log.write(cleaner.pure_posix_path(file) + "\n")
                cleaner.to_recycle_bin(cleaner.pure_windows_path(file))
            else:
                log.write(f"Error::timetable is not file: " + file + "\n")

    if printed_something:
        log.write("\n")
def sort_work_invoices():
    list_of_files = os.listdir(downloads_folder)

    # in minutes
    min_existence_time = 45

    invoices_folder = r'D:\work_invoices'

    full_path = [(downloads_folder + r'/{0}'.format(x)) for x in list_of_files]
    timetables = list(filter(lambda file: re.search("invoice.*\d+\.docx$", ntpath.basename(file)), full_path))
    printed_something = False
    for file in timetables:
        minutes_since_creation = int((time.time() - os.path.getmtime(file)) / 60)
        # if file is older than x minutes
        if minutes_since_creation >= min_existence_time:
            month = re.search("_(.*)\d+\.docx", ntpath.basename(file)).group(1)
            destination = os.path.join(invoices_folder, month)
            log.write(f'Moving invoice:\n')
            printed_something = True
            final_destination = os.path.join(destination, ntpath.basename(file))
            log.write(f'{cleaner.pure_posix_path(file)} => {cleaner.pure_posix_path(final_destination)}\n')

            cleaner.move(file, destination)

    if printed_something:
        log.write("\n")

    # manage rest of the timetables
    rest_of_invoices = list(filter(lambda file: re.search("invoice.*\)\.docx$", ntpath.basename(file)), full_path))
    printed_something = False
    for file in rest_of_invoices:
        minutes_since_creation = int((time.time() - os.path.getmtime(file))/60)
        # if file is older than x minutes
        if minutes_since_creation >= min_existence_time:
            log.write(f"Moving invoice to recycle bin:\n")
            printed_something = True
            if os.path.isfile(file):
                log.write(cleaner.pure_posix_path(file) + "\n")
                cleaner.to_recycle_bin(cleaner.pure_windows_path(file))
            else:
                log.write(f"Error::invoice is not file: " + file + "\n")

    if printed_something:
        log.write("\n")
def sort_sql_files():
    list_of_files = os.listdir(downloads_folder)

    # in minutes
    min_existence_time = 20

    folder = r"D:\work\database"

    full_path = [(downloads_folder + r'/{0}'.format(x)) for x in list_of_files]
    sql_files = list(filter(lambda file: pathlib.Path(file).suffix == ".sql", full_path))
    printed_something = False
    for file in sql_files:
        minutes_since_creation = int((time.time() - os.path.getmtime(file)) / 60)
        # if file is older than x minutes
        if minutes_since_creation >= min_existence_time:
            log.write(f'Moving sql into work folder:\n')
            printed_something = True
            final_destination = os.path.join(folder, ntpath.basename(file))
            log.write(f'{cleaner.pure_posix_path(file)} => {cleaner.pure_posix_path(final_destination)}\n')

            cleaner.move(file, folder)

    if printed_something:
        log.write("\n")

    folder = r"D:\work\database\zipped"

    sql_gz_files = list(filter(lambda file: re.search(".*\.sql\.gz$", ntpath.basename(file)), full_path))
    printed_something = False
    for file in sql_gz_files:
        minutes_since_creation = int((time.time() - os.path.getmtime(file)) / 60)
        # if file is older than x minutes
        if minutes_since_creation >= min_existence_time:
            log.write(f'Moving sql archive into work folder:\n')
            printed_something = True
            final_destination = os.path.join(folder, ntpath.basename(file))
            log.write(f'{cleaner.pure_posix_path(file)} => {cleaner.pure_posix_path(final_destination)}\n')

            cleaner.move(file, folder)

    if printed_something:
        log.write("\n")


def group_type(extension=None):
    list_of_files = os.listdir(downloads_folder)

    # in minutes
    min_existence_time = 10

    sorted_downloads_folder = r"D:\sorted_downloads"
    ignored_extentions = []
    if extension is None:
        sorted_downloads_folder = os.path.join(sorted_downloads_folder, "unknown_extensions")
        ignored_extentions = [".crdownload"]
    elif extension == "png" or extension == "jpg":
        sorted_downloads_folder = os.path.join(sorted_downloads_folder, "png_jpg")
    elif extension == "gz" or extension == "zip":
        sorted_downloads_folder = os.path.join(sorted_downloads_folder, "zip_gz")
    elif extension == "exe" or extension == "msi":
        sorted_downloads_folder = os.path.join(sorted_downloads_folder, "exe_msi")
    else:
        sorted_downloads_folder = os.path.join(sorted_downloads_folder, extension)

    full_path = [(downloads_folder + r'/{0}'.format(x)) for x in list_of_files]

    if extension is not None:
        files = list(filter(lambda file: pathlib.Path(file).suffix == "."+extension, full_path))
    else:
        files = list(filter(lambda file: os.path.isfile(file), full_path))
        extension = "unknown"

    printed_something = False
    for file in files:
        minutes_since_creation = int((time.time() - os.path.getmtime(file)) / 60)
        # if file is older than x minutes
        if minutes_since_creation >= min_existence_time and pathlib.Path(file).suffix not in ignored_extentions:
            log.write(f'Grouping {extension}:\n')
            printed_something = True
            final_destination = os.path.join(sorted_downloads_folder, ntpath.basename(file))
            log.write(f'{cleaner.pure_posix_path(file)} => {cleaner.pure_posix_path(final_destination)}\n')

            cleaner.move(file, sorted_downloads_folder)

    if printed_something:
        log.write("\n")


if __name__ == '__main__':
    d = datetime.datetime.now().replace(microsecond=0)

    log = start_log(d=d, logs_dir=logs_dir, script_name=script_name)

    log.write(f'Started download folder sorting on {d}\n\n')

    cleaner = dirclean(testing=False, log=log, logs_dir=logs_dir)

    cleaner.remove_outdated_logs(8)

    remove_html_files()

    sort_work_timetables()

    sort_work_invoices()

    sort_sql_files()

    group_type("gz")
    group_type("zip")
    group_type("exe")
    group_type("msi")
    group_type("pdf")
    group_type("docx")
    group_type("txt")
    group_type("jpg")
    group_type("png")

    # rest of the files
    group_type()

    log.write(f'Finished download folder sorting.\n')
    log.close()
