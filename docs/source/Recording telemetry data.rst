Recording telemetry data
========================
Huginn has a utility script that you can use to capture telemetry data that
you can use for analysis.

The huginn_telemetry.py script can be called from the console in the following way.

.. code-block:: bash

  huginn_telemetry.py telemetry.csv

The telemetry data will be saved in csv format in *telemetry.csv*. This file
will contain the following data.

=====  ================  =================
Index  Variable          Unit
=====  ================  =================
0      time              seconds
1      dt                seconds
2      latitude          degrees
3      longitude         degrees
4      altitude          meters
5      airspeed          meters/sec
6      heading           degrees
7      x acceleration    meters/sec^2
8      y acceleration    meters/sec^2
9      z acceleration    meters/sec^2
10     roll rate         degrees/sec
11     pitch rate        degrees/sec
12     yaw rate          degrees/sec
13     temperature       kelvin
14     static pressure   pascal
15     dynamic pressure  pascal
16     roll              degrees
17     pitch             degrees
18     engine rpm        rounds per minute
19     engine thrust     newton
20     engine power      hp
21     aileron           -1.0 to 1.0
22     elevator          -1.0 to 1.0
23     rudder            -1.0 to 1.0
24     throttle          0.0 to 1.0
=====  ================  =================