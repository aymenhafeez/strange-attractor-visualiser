# Strange attractor visualiser

![](media/app.png)

WIP

Streamlit app to visually explore and learn about [strange
attractors](https://en.wikipedia.org/wiki/Attractor)

## Running the app

```python
streamlit run main.py
```

Currently only supports the Lorenz, Rossler, Three-scroll and Dadras attractors. Plans
to add more soon.

## Features and usage

* View various strange attractors
* Alter parameter values to see how it affects the shape of the attractor
* Density colouring to show point distribution
* Trajectory animation

### Learn mode

The toggleable 'Learn mode' shows the equations for the chosen system, as well as some
additional information on the attractor and how to generate some interesting shapes.
