blackbox
========

more functional Transmission RPC Client written on django

requirements
============

 * python (>=2.7)
 * django framework (>=1.5)
 * MySQL database (>= 5.1)
 * python-south
 * python-transmissionrpc 0.11+

notice
------
The dependencies defined above it is the software testing with this application and works fine. As we use django framework we can use every database it supports but they are all untested.

How to install
==============

	git clone git://github.com/teran/blackbox.git
	cd blackbox
	./manage.py syncdb
	./manage.py migrate transmission
	./manage.py runserver

In later plans is to run application with uwsgi now it is possible with manually written uwsgi configuration file.
