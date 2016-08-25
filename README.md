     ____              _      _ _       _____                        
    |  _ \            | |    (_) |     |  __ \                       
    | |_) | ___   ___ | |     _| |_ ___| |  | |_   _ _ __ ___  _ __  
    |  _ < / _ \ / _ \| |    | | __/ _ \ |  | | | | | '_ ` _ \| '_ \
    | |_) | (_) | (_) | |____| | ||  __/ |__| | |_| | | | | | | |_) |
    |____/ \___/ \___/|______|_|\__\___|_____/ \__,_|_| |_| |_| .__/
                                                              | |    
                                                              |_|    


SQLite Dump
===========

The purpose of this tool is initially related to mobile forensic. It is complementary to commercial forensic tools.

Whatever forensic tool you are using (Cellebrite UFED, XRY, Oxygen) to examine mobile phones, they are all capable of extracting SQLite databases from the cellphones. Though, even if they all succeed in doing this, they are all not capable of analyzing each and every type of database that may appear in the device, since a prior implementation (description) of the schema is required.

For instance, if the cellphone is using an application which is not widespread worldwide, except in one country (ie: la fourchette in France), it is not worth it for the editor to implement this application in his forensic tool. As an example, if you examine a french smartphone with UFED, the database file for "la fourchette" will be extracted successfully but the data won't be analyzed by Cellebrite.

Though, as a forensic examiner, it is important sometimes to review all the databases that a device contains since they may comprise information which are crucial for the case.

BooLiteDump is aimed at dumping each and every table that contains data, from every database file, into raw text CSV files. It makes it possible to search through them in a straightforward manner with tools like grep or simply a spreadsheet software (should I say libreoffice :-) ?

It also produces a CSV file, to summarize the number of records in each table so that you can easily focus on the most important ones without wasting your time opening every database with SQLiteBrowser and examining each table content.

Prerequisites
------------

BooLiteDump has been developed in python and has been successfully tested on Linux Ubuntu 14.04 LTS, MacOSX 10.11.6 El Capitan and Windows 8.1 64 bits

This tool doesn't require any additional python modules to be run. It just needs python 2.7+

An executable windows binary file is also available for download.

Dumping the databases
---------------------

Once you have all the files extracted from your cellphone, your forensic tool should present you with a list of files ordered by type. For instance, Cellebrite UFED stores all the databases extracted from a cellphone in the ``files/databases`` folder.

You just have to execute the script with two or more parameters

    $ booLiteDump.py files/databases dst_folder

This commmand will automatically search in the "files/databases" folder for SQLite database files, and dump all the tables they contain in a bunch of raw text CSV/TSV files in the destination folder. By default the files created by booLiteDump are Tab Separated Files so that they can be easily processed with common linux tools (awk, sed, cut...) or a spreadsheet software.

    $ ./booLiteDump.py ./Database/ ./boolitedump

    /-----------------------/
    /  SEARCHING FOR FILES  /
    /-----------------------/
    234 files found

    /----------------------------------------/
    /  SEARCHING FOR SQLITE HEADER IN FILES  /
    /----------------------------------------/
    234 SQLite files found

    /----------------------------/
    /  DUMPING NON-EMPTY TABLES  /
    /----------------------------/
    ./Database/accounts.db
    ./Database/admined_pages_db
    ./Database/alarms.db
    ./Database/all.db
    ./Database/analytics_db2
    ./Database/analytics_db2_1
    ...
    ./Database/youtube_upload_service
    Extracted tables: 626

    /-----------------------/
    /  CREATING SUMMARY...  /
    /-----------------------/
    Created file : dst_folder/booLitedump/tables.tsv

If you are interested in keeping a copy of the initial databases you've just processed, you can add the ``--copy`` option, so that it will create a new subfolder in the destination directory, to store the original files.

Eventually you will get a CSV file (tab separated) for each SQLite database and one additional CSV file for the summary.

    DB num  DB file Table   Records
    1       ./Database/accounts.db       android_metadata        1
    1       ./Database/accounts.db       accounts        3
    1       ./Database/accounts.db       sqlite_sequence 3
    1       ./Database/accounts.db       authtokens      41
    1       ./Database/accounts.db       grants  0
    1       ./Database/accounts.db       extras  98
    1       ./Database/accounts.db       meta    0
    2       ./Database/admined_pages_db  android_metadata        1
    2       ./Database/admined_pages_db  _shared_version 4
    2       ./Database/admined_pages_db  admined_pages_table     0
    3       ./Database/alarms.db android_metadata        1
    3       ./Database/alarms.db alarms  2
    3       ./Database/alarms.db ringtone        0
    4       ./Database/all.db    countries       10707
    ...

Todo list
---------
- Carving residual data in the free lists and unallocated space in SQLite databases


Stay tuned for updates and please, feel free to report any bug to the author.
