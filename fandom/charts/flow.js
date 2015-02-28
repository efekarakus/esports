function flow() {
	var margin = {top: 0, right: 0, bottom: 0, left: 0},
		width = 700,
		height = 850,
		pWidth = 35,
		pHeight = 25;

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

		var highlight = function(d, link, percentage) {
			var node = d;
			var name = d.name;
			var season = d.season;

			link
				.transition().duration(400)
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

			percentage.transition().duration(300)
				.select("text")
				.text(function(d) { 
					if (node.season === 4) {
						for (var i = 0; i < node.sourceLinks.length; i++) {
							var l = node.sourceLinks[i];

							if (l.target.name === d.name && d.season === 5) {
								return Math.round(l.value/node.value * 100) + "%";
							}
						}

						return ""; 
					} else {
						for (var i = 0; i < node.targetLinks.length; i++) {
							var l = node.targetLinks[i];

							if (l.source.name === d.name && d.season === 4) {
								return Math.round(l.value/node.value * 100) + "%";
							}
						}
						return "";
					}
				});

			percentage.transition().duration(300)
				.select("rect")
					.style("stroke-opacity", function(d) { return d.season === season ? 0.0 : 1.0; } )
					.style("fill-opacity", function(d) { return d.season === season ? 0.0 : 1.0; });
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
				.size([width, height - 50]);

			var path = sankey.link();

			sankey
				.nodes(data.nodes)
				.links(data.links)
				.layout(10);


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
				.attr("data-name", function(d) { return d.name; })
				.attr("data-season", function(d) { return d.season; })
				.attr("data-fullname", function(d) { return d.fullname; })
				.attr("data-count", function(d) { return d.value; })
				.style("fill", function(d) { return colors[d.name]; })
				.style("fill-opacity", 1.0);

			var percentage = node.append("g");


			percentage.append("rect")
				.attr("x", function(d) { return d.season === 4 ? sankey.nodeWidth() + 10 : -pWidth - 10; })
				.attr("y", function(d) { return d.dy/2 - pHeight/2; })
				.attr("width", pWidth)
				.attr("height", pHeight)
				.attr("rx", 5)
				.attr("ry", 5)
				.style("fill", "#fff")
				.style("stroke", "#000");

			percentage.append("text")
				.attr("x", function(d) {
					return d.season === 4 ? sankey.nodeWidth() + 13 : -pWidth - 5; 
				})
				.attr("y", function(d) { return d.dy/2 + 5; })
				.text(function(d) { return d.percentage + "%"; });


			node.on("mouseover", function(d) { highlight(d, link, percentage); })
				.on("mouseout", function() { 
					link.transition().duration(400)
						.style("stroke", "#FFF")
						.style("stroke-opacity", .3); 

					percentage.transition().duration(300)
						.select("rect")
						.style("stroke-opacity", 1.0)
						.style("fill-opacity", 1.0);

					percentage.transition().duration(300)
						.select("text")
						.text(function(d) { return d.percentage + "%"; });
			});

			// --- LOGOS ---
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
					.attr("data-name", function(d) { return d.name; })
					.attr("data-season", function(d) { return d.season; })
					.attr("data-fullname", function(d) { return d.fullname; })
					.attr("data-count", function(d) { return d.value; })
					.on("mouseover", function(d) { highlight(d, link, percentage); })
					.on("mouseout", function() { 
						link.transition().duration(400)
							.style("stroke", "#FFF")
							.style("stroke-opacity", .3); 

						percentage.transition().duration(300)
							.select("rect")
							.style("stroke-opacity", 1.0)
							.style("fill-opacity", 1.0);

						percentage.transition().duration(300)
							.select("text")
							.text(function(d) { return d.percentage + "%"; });
					});
			}

			drawLogos(4, d3.select(this));
			drawLogos(5, d3.select(this));

			function buildTooltip(elem) {
				var title = "";
				if ($(elem).data("fullname") === "empty") {
					title = "No Support";
				} else {
					title = $(elem).data("fullname") + " (" + $(elem).data("name") + ")";
				}
				var count = $(elem).data("count");
				var season = $(elem).data("season");

				$(elem).qtip({
					content: {
						title: title,
						text: "Count: " + count
					},
					style: {
						classes: "qtip-dark qtip-shadow"
					},
					position: {
						target: "mouse",
						adjust: {x: 10, y: 20}
					}
				});
			}

			// tooltips
			$("image.logo").each(function() {
				buildTooltip(this);
			});

			$("rect.node").each(function() {
				buildTooltip(this);
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