Basics
==============

Running
--------------

Basically you want to execute

    fab -H host_name -i /path/to/key -u username run_through_test:sysname='SYSNAME',enterprise=True if you want to install enterprise packages

Where sysname is one of
* rhel7
* rhel6
* rhel5
* ...