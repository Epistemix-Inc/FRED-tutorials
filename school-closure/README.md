TODO:

1. Plot the number of students whose schools are closed.



# School Closure Model

## Overview

This model studies the effects of school closures in Jefferson County.  The `main.fred` file includes three components: 

* Influenza condition
* `school.fred`: a condition for admins to close the school according to case numbers in their school or county as well as normally scheduled holiday closure dates.
* `parameters.fred` : a file written into by the `METHODS` script to modify the school closure policies and other variables.



### Normal Closures

The schools are given a school schedule that closes the schools during summer, winter, and spring break:


```fred
    state Check_Calendar {
        wait(0)
        if (date_range(Dec-20,Jan-02)) then next(WinterBreak) 
        if (date_range(Mar-10,Mar-15)) then next(SpringBreak)
        if (date_range(Jun-15,Aug-25)) then next(SummerBreak)
        default(Open)
    }
```
The admins only pass into this state if their school is not already affected by flu closures.
No flu closures will take place if `school_closure_policy` is set equal to `NO_CLOSURE`.



### School Closure due to Flu

The schools are also setup to actively check the number of cases of flu either in their school or in their county and close schools if the number passes a threshold set by one of the variables `local_closure_trigger` or `global_closure_trigger`.  After deciding to close, the school remains closed for a time period set by the variable `days_closed`.

#### Global Flu Closure

The global closure option is selected by setting `school_closure_policy = GLOBAL_CLOSURE `.  This variable passes admins from the `Check_Epidemic` state in the `SCHOOL` condition to the `Check_Global_Epidemic ` state:


```fred
    state Check_Global_Epidemic {
        wait(0)
		if (global_closure_trigger <= current_count_of_INF.Is) then next(Close)
        default(Check_Calendar)
    }
```


#### Local Flu Closure

The local closure option is selected by setting `school_closure_policy = LOCAL_CLOSURE `.  This variable passes admins from the `Check_Epidemic` state in the `SCHOOL` condition to the `Check_Local_Epidemic ` state:


```fred
    state Check_Local_Epidemic {
        wait(0)
		if (local_closure_trigger <= current_count_of_INF.Is_in_School) then next(Close)
        default(Check_Calendar)
    }
```

In this state, the admin checks if the number of infected agents in their school is greater than the threshold set by `local_closure_trigger `.  If the number is greater, then the admin goes to the `Close` state and closes the school, otherwise they pass to the `check_calendar` state.

Below are results of the the three school closure policies.  

![tot](tot.pdf)
![inc](inc.pdf)
![closed](closed.pdf)
## Modifying Closure Variables
Variables are modified via the `METHODS` script which overwrites various combinations the `school_closure_policy`, `days_closed`, `global_closure_trigger`, and `local_closure_trigger` variables into the `parameters.fred` file to test and plot various scenarios seen below.
 Note that unless stated otherwise, the variables in the simulation represented below are:

* `global_closure_trigger = 1000`
* `local_closure_trigger = 20`
*  `days_closed = 28`.

### Changing the `global_closure_trigger` Variable
![global_trigs_tot](global_trigs_tot.pdf)
![global_trigs_new](global_trigs_new.pdf)
### Changing the `local_closure_trigger` Variable
![local_trigs_tot](local_trigs_tot.pdf)
![local_trigs_new](local_trigs_new.pdf)
### Changing the `days_closed` Variable Under Global Closure
![global_days_closed_tot](global_days_closed_tot.pdf)
![global_days_closed_new](global_days_closed_new.pdf)
### Changing the `days_closed` Variable Under Local Closure
![local_days_closed_tot](local_days_closed_tot.pdf)
![local_days_closed_new](local_days_closed_new.pdf)