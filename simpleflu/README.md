# Simple Flu

## Introduction

This example introduces the **Simple Flu** model, which is a standalone model of flu infection and the basis for the `../flu-with-behavior`, `../school-closure`, and `../vaccine` tutorials.
This model defines a condition, `INFLUENZA`, which agents can contract via contract with the meta agent (to create initial infections) or via other agents.
Having contracted the condition, agents either do or do not develop symptoms and then recover, at which point they can no longer contract `INFLUENZA`.

## Review of code implementing the model

The code that implements the **Simple Flu** model is contained in two `.fred` files:

- `main.fred`
- `simpleflu.fred`

### main.fred

This file does not influence the `INFLUENZA` model itself.
Instead, the `main.fred` file defines the location and time period of a particular run of simulations and imports the FRED model that defines `INFLUENZA`.

The `simulation` block handles the first part of this.
This block is required to define what location and time period will be simulated.
This instance also specifies that weekly outputs will be generated with `weekly_data = 1`.

```fred
simulation {
    locations = Jefferson_County_PA 
    start_date = 2020-Jan-01
    end_date = 2020-May-01
    weekly_data = 1
}
```

The only additional content in this file is the line `include simpleflu.fred`, which imports the `INFLUENZA` condition from `simpleflu.fred`.

### simpleflu.fred

This file does all of the definition of the `INFLUENZA` condition and its initial conditions.
`INFLUENZA` is a condition that can be passed by coming into contact with other agents (`transmission_mode = proximity`).
Agents all begin in the `Susceptible` state, where they have their susceptibility set to 1 and wait indefinitely to be `exposed`.
Exposure, either via the meta agent or another agent, moves a given agent to `Exposed`.

```fred
state Susceptible {
    INFLUENZA.sus = 1
    wait()
    next()
}
```

Once in `Exposed`, an agent loses its susceptibility to `INFLUENZA`.
The agent then waits through an incubation period and moves to a symptomatic infection state (`InfectiousSymptomatic`) with a probability of .33 and otherwise moves to an asymptomatic infectious state (`InfectiousAsymptomatic`).

```fred
state Exposed {
    INFLUENZA.sus = 0
    wait(24*lognormal(1.9,1.23))
    next(InfectiousAsymptomatic) with prob(0.33)
    default(InfectiousSymptomatic)
}
```

Both infectious states work roughly the same.
Once entering one of the infectious state after the wait period in `Exposed`, agents gain a non-zero transmissibility and wait through an infectious period before recovering.
Asymptomatic infections are half as transmissible as infectious ones, according to this model.

```fred
state InfectiousSymptomatic {
    INFLUENZA.trans = 1          # this value is .5 for InfectiousAsymptomatic
    wait(24* lognormal(5.0,1.5))
    next(Recovered)
}
```

Once the infectious period is over, agents move to the `Recovered` condition.
This condition reduces transmissibility of `INFLUENZA` to zero and continues indefinitely.

```fred
state Recovered {
    INFLUENZA.trans = 0
    wait()
    next()
}
```

The only remaining state in `simpleflu.fred` is the `Import` condition, which is the starting state for the meta agent.
This state prompts the meta agent to infect ten agents and then wait indefinitely.

```fred
state Import {
    import_count(10)
    wait()
    next()
}
```

## Sample Model Outputs



## Summary



