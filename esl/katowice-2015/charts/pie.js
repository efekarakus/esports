function pie() 
{
	var width = 300,
		height = 300;

	var radius = 100;

	var pie = d3.layout.pie()
		.sort(null)
		.value(function(d) { return d.total; });

	function chart(selection) {
		selection.each(function(data) {
			
			data.forEach(function(d) {
				d.total = (+d.hours)*3600 + (+d.minutes)*60 + (+d.seconds);
			});


			var arc = d3.svg.arc()
				.outerRadius(radius)
				.innerRadius(radius - 70);

			var svg = d3.select(this)
				.append("svg")
					.attr("width", width)
					.attr("height", height)
				.append("g")
					.attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

			var g = svg.selectAll(".arc")
				.data(pie(data))
				.enter()
					.append("g")
						.attr("class", "arc");

			g.append("path")
				.attr("d", arc)
				.attr("class", function(d) { return d.data.type; });

		})
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