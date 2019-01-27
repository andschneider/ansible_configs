import argparse
from configparser import ConfigParser
from datetime import datetime, timedelta
from pathlib import Path, PurePath
from subprocess import Popen

import boto3


def read_cli():
    parser = argparse.ArgumentParser()
    # use the mutually exclusive group to force only one argument being used
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument("-t", "--today", action="store_true", default=False,
                       help="Find a backup from today in s3 to download.")

    group.add_argument("-p", "--past", metavar="DAYS", nargs="?", type=int, default=0,
                       help="Find a backup from the specified amount of days ago.")

    group.add_argument("-l", "--latest", action="store_true", default=False,
                       help="Find the latest file in s3 to download.")

    parser.add_argument("-r", "--restore", action="store_true", default=False,
                        help="Automatically restore downloaded backup.")

    parser.add_argument("--drop", action="store_true", default=False,
                        help="Force restore by dropping the old database first.")

    parser.add_argument("--quiet", action="store_true", default=False,
                        help="Runs the mongorestore in quiet mode to limit the output.")

    args = vars(parser.parse_args())

    return args["today"], args["past"], args["latest"], args["restore"], args["drop"], args["quiet"]


def connect_to_bucket(configuration):
    settings = configuration["aws"]
    s3 = boto3.resource("s3")

    return s3.Bucket(settings["bucket"]), settings["backup_file_name"]


def get_available_files(s3_bucket, file_name):
    """Gets the available MongoDB .archive files that match the desired backup name.

    Parameters
    ----------
    s3_bucket : s3.Bucket
        Boto3 authenticated s3 bucket.
    file_name : str
        The name of the desired backups. Assumes files in s3 follow the pattern of "date_name.archive"

    Returns
    -------
    file_map : dict
        Dictionary of available files with the date as key and the full file name as value.

    """
    # get all .archive files from the s3 bucket
    s3_files = [t.key for t in s3_bucket.objects.all() if t.key.split(".")[1] == "archive"]

    # create a dictionary of {datetime: str}
    file_dict = {}
    for archive in s3_files:
        date_string, name = archive.split("_", maxsplit=1)
        name = name.split(".")[0]
        # only get desired files
        if name == file_name:
            date = datetime.strptime(date_string, "%Y-%m-%d")
            file_dict[date] = archive

    return file_dict


def get_backup(file_dict, days):
    """Finds a backup from a specific number of days ago.

    Parameters
    ----------
    file_dict : dict
        The dictionary of dates: file_name to search.
    days : int
        The number of days in the past to search. Use 0 to get today's date.

    Returns
    -------
    file_name : str, None
        The file name if it exists, otherwise None.

    """
    today_date = datetime.today()
    # stripping the hours, minutes, and seconds to match the format of the date in the file name
    today_date = datetime(today_date.year, today_date.month, today_date.day)
    date = today_date - timedelta(days=days)

    return file_dict.get(date, None)


def find_latest_file(file_dict):
    """Finds the latest backup available.

    Parameters
    ----------
    file_dict : dict
        The dictionary of {dates: file_name} to search.

    Returns
    -------
    file_name : str or None
        The file name if it exists, otherwise None.

    """
    file_dates = list(file_dict.keys())
    file_dates.sort(reverse=True)
    return file_dict[file_dates[0]]


def download_file(s3_bucket, file_name):
    """Downloads a given file from s3 if it exists."""
    if file_name is None:
        raise FileNotFoundError("There is no backup from that day.")

    try:
        s3_bucket.download_file(Key=file_name, Filename=file_name)
        print("Download successful.")
    except Exception as e:
        raise e


def restore_from_archive(configuration, downloaded_backup, force, silent):
    """Runs the mongorestore program to load data from the downloaded .archive.

    Assumes there is a mongod process running and it requires authentication.

    Parameters
    ----------
    configuration : ConfigParser
        Settings to authenticate the mongod process.
    downloaded_backup: str
        The file name that was just downloaded.
    force : bool, default=False
        If True, will use --drop when restoring, which removes the old database first.
    silent : bool, default=False
        If True, uses the --quiet option to limit the output from the mongorestore program.

    """
    settings = configuration["mongo"]
    port = settings["port"]
    mongo_un = settings["mongo_admin_user"]
    mongo_pw = settings["mongo_admin_password"]

    args = ["mongorestore",
            "--port", port, "--sslAllowInvalidCertificates", "--ssl",
            "-u", mongo_un, "-p", mongo_pw, "--authenticationDatabase", "admin",
            "--archive=" + downloaded_backup, "--gzip"
            ]

    if force:
        args.append("--drop")
    if silent:
        args.append("--quiet")

    print("Starting restore...")

    restore_proc = Popen(args)
    status = restore_proc.wait()  # wait until finished, and get return code

    if status == 0:
        print("Restore successful.")
    else:
        raise ChildProcessError("Restore failed.")


if __name__ == '__main__':
    # read command line arguments
    today, past, latest, restore, drop, quiet = read_cli()

    # read in configuration
    current_dir = Path(__file__).parent
    config_file = PurePath(current_dir / "restore.ini")
    config = ConfigParser()
    config.read(config_file)

    # pull file names from s3
    bucket, backup_name = connect_to_bucket(config)
    files = get_available_files(bucket, backup_name)

    # download file from s3
    if today:
        file = get_backup(files, 0)
        print("Found {} from today. Downloading...".format(file)) if file else None
    elif past:
        file = get_backup(files, past)
        print("Found {} from {} days ago. Downloading...".format(file, past)) if file else None
    elif latest:
        file = find_latest_file(files)
        print("The latest file is {}. Downloading...".format(file)) if file else None

    download_file(bucket, file)

    # restore downloaded file into db
    restore_from_archive(config, file, drop, quiet)
