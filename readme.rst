:author: Lukas Turcani

day_logger
==========

Tracks activities done during the day and calculates the total time
spent on a class of activities.

You need to provide a plain text log file of the form::

    05:58 WORK description of stuff done
    08:43 REST
    16:12 WORK some other description

Which is the 24-hour format of the time an activity was started, then
a string which defines the class of the activity and then an optional
note describing the activity. The name of the class can by any
arbitrary string. The program will add up all the times spent on each
class of tasks and print the totals. For example, in the example above,
the total time spent on all ``WORK`` and ``REST``, would be printed.

The software is run with::

    python day_logger.py path/to/log/file
