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

		var highlight = function(d, link) {
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

		}

		selection.each(function(data) {
			var svg = d3.select(this)
				.select(".c.c2")
				.append("svg")
				.attr("width", width)
				.attr("height", height);

			var sankey = d3.sankey()
				.nodeWidth(20)
				.nodePadding(40)
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

			node.on("mouseover", function(d) { highlight(d, link); })
				.on("mouseout", function() { link.style("stroke", "#FFF").style("stroke-opacity", .3); });

			function drawLogos(season, root) {
				root = season === 4 ? root.select(".c.c1") : root.select(".c.c3");

				var w = 100;
				var logoSize = 50;

				var svg = root.append("svg")
					.attr("width", w)
					.attr("height", height + logoSize);

				var logo = svg.selectAll(".logos")
					.data(data.nodes.filter(function(a) { return a.season === season && a.name !== "NS"; }))
					.enter()
						.append("image");

				logo
					.attr("xlink:href", function(d) { return "./images/" + d.name + ".png"; })
					.attr("x", function() { return season === 4 ? w - logoSize : 0; })
					.attr("y", function(d) { return d.y + d.dy/2 - logoSize/2; })
					.attr("width", logoSize)
					.attr("height", logoSize)
					.attr("class", "logo")
					.on("mouseover", function(d) { highlight(d, link); })
					.on("mouseout", function() { link.style("stroke", "#FFF").style("stroke-opacity", .3); });

			}

			drawLogos(4, d3.select(this));
			drawLogos(5, d3.select(this));

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