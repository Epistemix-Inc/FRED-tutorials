# Flu with Vaccine Model

## TODO

- do `flu_delay` and the meta-agent assignments need to be made in `main.fred`?

## Introduction

This example builds on the the Flu with Behavior model (see `../flu-with-behavior`) by adding an `INFLUENZA_VACCINE` condition that allows agents to be exposed to a vaccine that probabilistically protects the agent from influenza by setting `INFLUENZA.sus = 0`.

## Review of code implementing the model

The code that implements the Flu with Vaccine model is contained in five `.fred` files:

- `main.fred`
- `simpleflu.fred`
- `stayhome.fred`
- `vaccine.fred`
- `parameters.fred`

### `main.fred`

This `main.fred` contains four basic components.
The first two will be familiar from the Simple Flu and Flu with Behavior models.
The simulation block defines the dates and physical location of the simulation.
A series of `include` statement refer to other `.fred` files to reference conditions, states, and variables necessary to run the simulation.

The Flu with Vaccine `main.fred` also directly defines a global variable.

```fred
variables {
    global flu_delay
    flu_delay = 90
}
```

In this case, it is the number of days to wait after the initial infections before introducing the vaccination to the first agents.

The next code chunk modifies the `INFLUENZA` condition.
Specifically, it directs a meta-agent to start in the `ImportDelay` state and transition to `Import` after the delay.

### `simpleflu.fred`



### `stayhome.fred`



### `vaccine.fred`

`vaccine.fred` defines the variables, condition, and states (for both agents and the meta-agent) required to simulate basic vaccination behavior in our population.


### `parameters.fred`



