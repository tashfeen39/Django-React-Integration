import axios from "axios";
import React from "react";
import Plot from "react-plotly.js";

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      data1: [],
      data2: [],
    };
  }

  componentDidMount() {
    axios
      .get("http://127.0.0.1:8000/scrape/")
      .then((response) => {
        const { data1, data2 } = response.data;

        if (data1 && data2) {
          this.setState({
            data1: data1,
            data2: data2,
          });
        } else {
          console.error("Error");
        }
      })
      .catch((error) => {
        console.error(error);
      });
  }

  render() {
    const { data1, data2 } = this.state;

    const dataPrices1 = data1.map((item) => item.Price);
    const dataSizes1 = data1.map((item) => item.Size);
    const dataPrices2 = data2.map((item) => item.Price);
    const dataSizes2 = data2.map((item) => item.Size);

    const plotData = [
      {
        x: dataSizes1,
        y: dataPrices1,
        type: "bar",
        name: "Multan",
      },
      {
        x: dataSizes2,
        y: dataPrices2,
        type: "bar",
        name: "Lahore",
      },
    ];

    const plotLayout = {
      barmode: "group",
      xaxis: {
        title: "Sizes",
      },
      yaxis: {
        title: "Prices",
      },
    };

    return (
      <div>
        <h1>Data from Backend</h1>
        <div>
          <Plot data={plotData} layout={plotLayout} />
        </div>
      </div>
    );
  }
}

export default App;
