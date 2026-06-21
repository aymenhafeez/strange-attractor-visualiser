# Strange attractor visualiser

<table>
  <tr>
    <td><img src="media/image_1.png" /></td>
    <td><img src="media/image_2.png" /></td>
  </tr>
  <tr>
    <td><img src="media/image_3.png" /></td>
    <td><img src="media/image_4.png" /></td>
  </tr>
</table>

Streamlit app to visually explore and learn about [strange
attractors](https://en.wikipedia.org/wiki/Attractor). View the app live
[here](https://strangeattractors.streamlit.app/)


## Features and usage

* View various strange attractors
* Alter parameter values to see how it affects the shape of the attractor
* Density colouring to show point distribution
* Background on each attractor with information on how each parameter affects it's
  shape
* Preset parameter values to generate interesting shapes
* Trajectory animation


## Running locally

```python
git clone https://github.com/aymenhafeez/strange-attractor-visualiser
cd strange-attractor-visualiser/

python -m venv .venv
source .venv/bin/activate

pip install -e .

streamlit run main.py
```
