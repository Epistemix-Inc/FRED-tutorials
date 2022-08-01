School Closure Model
====================

Overview
--------

This model studies the effects of school closures in Jefferson County,
PA. The ``main.fred`` file includes three components:

-  Influenza condition
-  ``school.fred``: a condition for group agents to close the school according
   to case numbers in their school or county as well as normally
   scheduled holiday closure dates. This condition also keeps track of
   students whose schools are closed.
-  ``parameters.fred`` : a file written into by the ``METHODS`` script
   to modify the school closure policies and other variables.

Normal Closures
~~~~~~~~~~~~~~~

The schools are given a school schedule that closes the schools during
summer, winter, and spring break. There are states for each break:
``WinterBreak``, ``SpringBreak``, and\ ``SummerBreak``. In these states,
school administrators (represented by ``group agents``) close their schools and wait until the end of the break period.
They pass into these states from the ``CheckCalendar`` state:

.. code:: fred

       state CheckCalendar {
           wait(0)
           if (date_range(Dec-20,Jan-02)) then next(WinterBreak) 
           if (date_range(Mar-10,Mar-15)) then next(SpringBreak)
           if (date_range(Jun-15,Aug-25)) then next(SummerBreak)
           default(Open)
       }

Group agents go to the break states by checking the current date with
``date_range()``. The group agents only pass into this check state if their
school is not already affected by flu closures. No flu closures will
take place if ``school_closure_policy`` is set equal to ``NO_CLOSURE``.

School Closure due to Flu
~~~~~~~~~~~~~~~~~~~~~~~~~

The schools are also setup to actively check the number of cases of flu
either in their school or in their county and close schools if the
number passes a threshold set by one of the variables:
``local_closure_trigger`` or ``global_closure_trigger``. After deciding
to close due to the flu, the admin goes to the ``Close`` state, and the
school remains closed for a time period set by the variable
``days_closed``.

Global Flu Closure
^^^^^^^^^^^^^^^^^^

The ``GLOBAL_CLOSURE``, ``LOCAL_CLOSURE``, and ``NO_CLOSURE`` variables
are set to arbitrary but unique integers to get around the inability to
assign strings to variables. The global closure option is selected by
setting ``school_closure_policy = GLOBAL_CLOSURE``. This variable passes
group agents from the ``CheckEpidemic`` state in the ``SCHOOL`` condition to
the ``CheckGlobalEpidemic`` state:

.. code:: fred

       state CheckGlobalEpidemic {
           wait(0)
           if (global_closure_trigger <= current_count(INF.Is)) then next(Close)
           default(CheckCalendar)
       }

This state checks the county flu count against the global threshold,
``local_closure_trigger``. If the threshold is reached, then all group agents
go to ``Close`` state.


Local Flu Closure
^^^^^^^^^^^^^^^^^

The local closure option is selected by setting
``school_closure_policy = LOCAL_CLOSURE``. This variable passes group agents
from the ``CheckEpidemic`` state in the ``SCHOOL`` condition to the
``CheckLocalEpidemic`` state:

.. code:: fred

       state CheckLocalEpidemic {
           wait(0)
           if (local_closure_trigger <= current_count(INF.Is, School)) then next(Close)
           default(CheckCalendar)
       }

In this state, each admin checks if the number of infected agents in
their own school is greater than the threshold set by
``local_closure_trigger``. If the number is greater or equal, then the
admin goes to the ``Close`` state and closes the school, otherwise they
pass to the ``check_calendar`` state.

Student Tracking
^^^^^^^^^^^^^^^^

The ``StudentSchoolOpen`` and ``StudentSchoolOpen`` states are included
in the ``SCHOOL`` condition to keep track of how many students have
their school closed/open over the course of time. Students are filtered
into ``StudentSchoolOpen`` from the ``Start`` state with the conditional
``if (is_member(School) & age < 18)``. The students then switch between the two
states by checking if their school has been closed by an admin using the
``is_temporarily_closed(<group>)`` predicate. ##Results

Plotting Flu Cases
~~~~~~~~~~~~~~~~~~

The following plots show the effectiveness of the different policies in
limiting the number of total and daily infections as a percent of the
county population.

===== =====
|tot| |inc|
===== =====
===== =====

Plotting School Closures
~~~~~~~~~~~~~~~~~~~~~~~~

The plots below show the number of schools closed and number of students
out of school over time. Because the threshold for school closure is the
same regardless of school size, the larger schools are more likely to
close under the local closure policy. This results in a higher
percentage of students out of school than percentage of schools closed
for the local policy.

======== ==========
|closed| |students|
======== ==========
======== ==========

Modifying Closure Variables
---------------------------

FRED variables are modified in the :filename:`METHODS` script for this model,
which overwrites various combinations the ``school_closure_policy``,
``days_closed``, ``global_closure_trigger``, and ``local_closure_trigger`` variables.
For each combination of interest, the changes are written into the
``parameters.fred`` file and then ``fred_job`` is called to execute the model
with the modified parameters. This produces a
range of results as captured in the following figures.

In each figure, the modified variable values are shown in the legend for
the figure. The other variables not represented in a figure use the
following default values:

-  ``global_closure_trigger = 1000``

-  ``local_closure_trigger = 20``

-  ``days_closed = 28``

Changing the ``global_closure_trigger`` Variable
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

================== ==================
|global_trigs_tot| |global_trigs_new|
================== ==================
================== ==================

Changing the ``local_closure_trigger`` Variable
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

================= =================
|local_trigs_tot| |local_trigs_new|
================= =================
================= =================

Changing the ``days_closed`` Variable Under Global Closure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

======================== ========================
|global_days_closed_tot| |global_days_closed_new|
======================== ========================
======================== ========================

Changing the ``days_closed`` Variable Under Local Closure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

======================= =======================
|local_days_closed_tot| |local_days_closed_new|
======================= =======================
======================= =======================

.. |tot| image:: figures/tot.png
.. |inc| image:: figures/inc.png
.. |closed| image:: figures/closed.png
.. |students| image:: figures/students.png
.. |global_trigs_tot| image:: figures/global_trigs_tot.png
.. |global_trigs_new| image:: figures/global_trigs_new.png
.. |local_trigs_tot| image:: figures/local_trigs_tot.png
.. |local_trigs_new| image:: figures/local_trigs_new.png
.. |global_days_closed_tot| image:: figures/global_days_closed_tot.png
.. |global_days_closed_new| image:: figures/global_days_closed_new.png
.. |local_days_closed_tot| image:: figures/local_days_closed_tot.png
.. |local_days_closed_new| image:: figures/local_days_closed_new.png
