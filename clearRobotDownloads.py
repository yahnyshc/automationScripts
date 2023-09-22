import datetime
import os
import ntpath
import time

from modules.dirclean import dirclean

d = datetime.datetime.now().replace(microsecond=0)

script_name = os.path.splitext(ntpath.basename(__file__))[0]
logs_dir = f'D:\\automationScripts\\logs\\{script_name}'

if not os.path.exists(logs_dir):
    os.mkdir(logs_dir)

logname = os.path.join(logs_dir, script_name + d.strftime("%Y-%m-%d_%H-%M") + '.txt')
log = None

sortfolders = [r"C:\Documents\Download\webrobot",
               r"C:\Documents\Download\webrobot\proxyagent",
               r"C:\Documents\Download\webrobot\errors"]

cleaner = None
def remove_html_files():
    # in hours
    min_existence_time = 72

    for sortfolder in sortfolders:
        list_of_files = os.listdir(sortfolder)
        directories = [(sortfolder + r'/{0}'.format(x)) for x in list_of_files]
        printed_something = False

        for dir in directories:
            if str(cleaner.pure_windows_path(dir)) in sortfolders:
                continue
            minutes_since_creation = int((time.time() - os.path.getmtime(dir))/3600)
            # if file is older than x hours
            if minutes_since_creation >= min_existence_time:
                log.write(f"Removing outdated ({minutes_since_creation} hours old) robot downloads folder:\n")
                printed_something = True

                log.write(cleaner.pure_posix_path(dir) + "\n")
                cleaner.completely_remove(dir)

    if printed_something:
        log.write("\n")

if __name__ == "__main__":
    log = open(logname, 'w', encoding='utf-8')

    log.write(f'Started robot\'s download folder sorting on {d}\n\n')

    cleaner = dirclean(testing=False, log=log, logs_dir=logs_dir)

    cleaner.remove_outdated_logs(4)

    remove_html_files()

    log.write(f'Finished robot\'s download folder sorting.\n')
    log.close()
