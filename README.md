     ____              _      _ _       _____                        
    |  _ \            | |    (_) |     |  __ \                       
    | |_) | ___   ___ | |     _| |_ ___| |  | |_   _ _ __ ___  _ __  
    |  _ < / _ \ / _ \| |    | | __/ _ \ |  | | | | | '_ ` _ \| '_ \
    | |_) | (_) | (_) | |____| | ||  __/ |__| | |_| | | | | | | |_) |
    |____/ \___/ \___/|______|_|\__\___|_____/ \__,_|_| |_| |_| .__/
                                                              | |    
                                                              |_|    


Boolaz SQLite Dump
==================

The purpose of this tool is initially related to mobile forensic. It is complementary to commercial forensic tools.

Whatever forensic tool you are using (Cellebrite UFED, XRY, Oxygen) to examine mobile phones, they are all capable of extracting SQLite databases from the cellphones. Though, even if they all succeed at doing this, they are all not capable of analyzing each and every type of database that may be stored in the device, since a prior description of the schemas is required.

For instance, if the cellphone is using an application which is not widespread, except in one country (ie: la fourchette in France), it is not worth it for the editor to implement this application in his forensic tool.

Though, as a forensic examiner, it is important sometimes to review all the databases that a device contains since they may comprise information which are crucial for the case.

BooLiteDump is aimed at dumping each and every table from every database in raw text CSV files. It makes it possible to search through them in a straightforward manner with tools like grep.

Requirements
------------

BooLiteDump has been developed in python and has been successfully tested on Linux Ubuntu 14.04 LTS and MacOSX 10.11.6 El Capitan

This tool doesn't require additional python modules to be run. It just needs python 2.7+

Dumping the databases
---------------------

Once you have all the files extracted from the cellphone, your forensic tool should present you with a list of files ordered by type. For instance, Cellebrite UFED stores all the databases extracted from a cellphone in ``files/databases`` folder.

You just have to execute the script with two or more parameters

    $ booLiteDump.py files/databases dst_folder

This commmand will automatically search in the files/databases folder for SQLite database files, and dump all the tables they contain in a bunch of raw text CSV files in the destination folder.

If you are interested in keeping a copy of the initial databases you've just processed, you can add the ``--copy`` option, so that it will create a new subfolder in the destination directory, to store the original files.

Todo list
---------
- Carving residual data in the free lists and unallocated space in SQLite databases
- compiled binary version for windows


Stay tuned for updates and please, feel free to report any bug to the author.
