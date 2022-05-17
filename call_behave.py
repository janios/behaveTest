from datetime import datetime as dt
import os
import sys


def main():
    print("adding directory to path python")
    sys.path.insert(0, '/root/.local/bin')
    print("Calling Behave")
    time = dt.now()
    report_name = time.strftime("%m-%d-%y-%H-%M") + "-report" + ".html"
    command = "behave -f html > " + report_name
    os.system(command)
    command = "behave"
    os.system(command)
    print("Behave Finished")


if __name__ == '__main__':
    main()
