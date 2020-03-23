import base64
from io import BytesIO
from flask import Flask
import plot_barchart

app = Flask(__name__)


@app.route("/")
def show_barchart():
    # Generate the figure **without using pyplot**.
    fig = plot_barchart.plot()

    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")

    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")

    return f"<img src='data:image/png;base64,{data}'/>"


if __name__ == "__main__":
    app.run()
