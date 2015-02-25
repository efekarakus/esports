function flow() {
	var margin = {top: 0, right: 0, bottom: 0, left: 0},
		width = 400,
		height = 800;

	function chart(selection) {

		var linkd = function(d) {
			// The curves are taken by Jason Davies's Sankey library
			// https://github.com/d3/d3-plugins/blob/master/sankey/sankey.js

			var curvature = 0.05;
			var x0 = d.x0,
				y0 = d.y0,

				x1 = d.x1,
				y1 = d.y1,

				x2 = d.x2,
				y2 = d.y2,

				x3 = d.x3,
				y3 = d.y3;

			var xi = d3.interpolateNumber(x0, x1);
			var xii = d3.interpolateNumber(x2, x3);


			return "M" + x0 + "," + y0
				+ "C" + xi(curvature) + "," + y0
				+ " " + xi(1 - curvature) + "," + y1
				+ " " + x1 + "," + y1
				+ "M" + x0 + "," + y0
				+ "L" + x2 + "," + y2
				+ "C" + xii(curvature) + "," + y2
				+ " " + xii(1 - curvature) + "," + y3
				+ " " + x3 + "," + y3
				+ "L" + x2 + "," + y2;
		}

		selection.each(function(data) {
			var logos = d3.select(this)
				.selectAll(".logo");

			var svg = d3.select(this)
				.select(".c.c2")
				.append("svg")
				.attr("width", width)
				.attr("height", height);

			var rect = svg.selectAll("rect.bar")
				.data(data.nodes)
				.enter()
				.append("rect");

			rect.attr("x", function(d) { return d.x; })
				.attr("y", function(d) { return d.y; })
				.attr("width", function(d) { return d.width; })
				.attr("height", function(d) { return d.height; })
				.attr("class", "bar");

			/*
			var link = svg.selectAll("path.link")
				.data(data.links)
				.enter()
				.append("path");

			link.attr("d", function(d) { return linkd(d); })
				.attr("class", "link");
			*/


			logos
				.on("mouseover", function() {
					var team = d3.select(this)
						.attr("data-team");

					var season = d3.select(this)
						.attr("data-season");


					rect.attr("class", function(d) {
						return d.team === team && d.season == season ? team : "bar";
					})
					/*
					link.attr("class", function(d) {
						if (season === "4" && d.from === team) {

						console.log(d);
							return team;
						} else if (season === "5" && d.to === team) {
							return team;
						} else {
							return "link";
						}
					})
					*/
				})
				.on("mouseout", function() {
					var team = d3.select(this)
						.attr("data-team");

					var season = d3.select(this)
						.attr("data-season");

					rect.attr("class", "bar");
					//link.attr("class", "link");
				})


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