function flow() {
	var margin = {top: 0, right: 0, bottom: 0, left: 0},
		width = 700,
		height = 800;

	var colors = {
		"TSM": "#FFF",
		"CLG": "#FFF",
		"C9": "#00A0E6",
		"DIG": "#F5C451",
		"CRS": "#FD5F12",
		"EG": "#274A6B",
		"LMQ": "#24A7DE",
		"COL": "#980A0C",
		"TL": "#00A7DB",
		"WFX": "#615D8A",
		"GV": "#EB1B23",
		"T8": "#008DC0",
		"TIP": "#FF1045",
		"CST": "#1950A8",
		"FNC": "#F5AB17",
		"ALL": "#D0D0D1",
		"GMB": "#EF080C",
		"SK": "#FFF",
		"SHC": "#FF8900",
		"ROC": "#359DD2",
		"MIL": "#5F4CA0",
		"CW": "#D3932B",
		"UOL": "#D3536C",
		"EL": "#228478",
		"H2K": "#3894D1",
		"GIA": "#1997D5",
		"MYM": "#2E6AA6",
		"NS": "#FFF"
	}

	function chart(selection) {

		selection.each(function(data) {
			var svg = d3.select(this)
				.select(".c.c2")
				.append("svg")
				.attr("width", width)
				.attr("height", height);

			var sankey = d3.sankey()
				.nodeWidth(20)
				.nodePadding(25)
				.width(width)
				.height(height)
				.size([width, height]);

			var path = sankey.link();

			sankey
				.nodes(data.nodes)
				.links(data.links)
				.layout(32);

			var link = svg.append("g").selectAll(".link")
				.data(data.links)
				.enter()
					.append("path")
					.attr("class", "link")
					.attr("d", path)
					.style("stroke-width", function(d) { return Math.max(1, d.dy); })
					.sort(function(a, b) { return b.dy - a.dy; });

			var node = svg.append("g").selectAll(".node")
				.data(data.nodes)
				.enter()
					.append("g")
					.attr("class", "node")
					.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });

			node.append("rect")
				.attr("height", function(d) { return d.dy; })
				.attr("width", sankey.nodeWidth())
				.attr("class", "node")
				.style("fill", function(d) { return colors[d.name]; })
				.style("fill-opacity", 1.0);

			node.append("text")
				.attr("x", -6)
				.attr("y", function(d) { return d.dy / 2; })
				.attr("dy", ".35em")
				.attr("text-anchor", "end")
				.attr("transform", null)
				.text(function(d) { return d.name; })
				.filter(function(d) { return d.x < width / 2; })
				.attr("x", 6 + sankey.nodeWidth())
				.attr("text-anchor", "start");


			node.on("mouseover", function(d) {
				var name = d.name;
				var season = d.season;

				link
					.style("stroke", function(d) {
						if (season === 4 && name === d.source.name) return colors[name];
						else if (season === 5 && name === d.target.name) return colors[name];
						else return "#FFF";
					})
					.style("stroke-opacity", function(d) {
						if (season === 4 && name === d.source.name) return 1.0;
						else if (season === 5 && name === d.target.name) return 1.0;
						else return 0.1;
					});
			});


			// draw logos
			width = 100;
			svg = d3.select(this)
				.select(".c.c1")
				.append("svg")
				.attr("width", width)
				.attr("height", height);

			

		});
	}

	chart.margin = function(_) {
		if (!arguments.length) return margin;
		margin = _;
		return chart;
	}

	chart.width = function(_) {
		if (!arguments.length) return width;
		width = _;
		return chart;
	}

	chart.height = function(_) {
		if (!arguments.length) return height;
		height = _;
		return chart;
	}

	return chart;
}