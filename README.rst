Inkai
=====

inkai is a tool for data sourcing a database from excel-like spreadsheet.

It is very easy to generate a template from your database:

        $ inkai template mysql://localhost:port/database/ -u user -p -r table -o file.xlsx

Uploading an excel to the database is even easier:

        $ inkai load mysql://localhost:port/database/ -u user -p file.xlsx

Features
--------

With inkai your database project will avoid:

- creating a specific app just for data feeding  
- provide database traininig to your users

Installation
------------

Install inkai by running:

        install inkai

Contribute
----------

- Issue Tracker:
github.com/spadial-science/inkai/issues

- Source Code:
github.com/spadial-science/inkai

Support
-------

If you are having issues, please let us know.


License
-------

The project is licensed under the EUPL license.
