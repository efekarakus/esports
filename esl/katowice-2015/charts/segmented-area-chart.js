function segmentedAreaChart()
{
	var margin = {top: 20, right: 0, bottom: 30, left: 50},
		width = 1000 - margin.left - margin.right,
		height = 300 - margin.top - margin.bottom;

	var parseDate = d3.time.format("%Y-%m-%d %H:%M:%S");

	var x = d3.time.scale()
		.range([0, width]);

	var y = d3.scale.linear()
		.range([height, 0]);

	var xAxis = d3.svg.axis()
		.scale(x)
		.orient("bottom");

	var yAxis = d3.svg.axis()
		.scale(y)
		.orient("left");

	var area = d3.svg.area()
		.x(function(d) {return x(d.timestamp);})
		.y0(height)
		.y1(function(d) {return y(d.count);});


	function chart(selection) {
		selection.each(function(data) {

			var day = data.day;
			var areas = data.areas

			var maxCount = 0;
			var minDate = new Date(2999, 12, 12);
			var maxDate = new Date(0, 1, 1);

			areas.forEach(function(area) {
				var points = area.points;
				points.forEach(function(point) {
					point.count  = +point.count;
					point.timestamp = parseDate.parse(point.timestamp);

					maxCount = maxCount < point.count ? point.count : maxCount;
					minDate = minDate > point.timestamp ? point.timestamp : minDate;
					maxDate = maxDate < point.timestamp ? point.timestamp : maxDate;
				})
			});

			x.domain([minDate, maxDate]);
			y.domain([0, maxCount]);

			var svg =  d3.select(this)
				.append("svg")
					.attr("width", width + margin.left + margin.right)
					.attr("height", height + margin.top + margin.bottom)
				.append("g")
					.attr("transform", "translate(" + margin.left + ", " + margin.top + ")");

			areas.forEach(function(a) {
				svg.append("path")
					.datum(a.points)
					.attr("class", "area " + a.type)
					.attr("d", area);
			});

			svg.append("g")
					.attr("class", "x axis")
					.attr("transform", "translate(0," + height + ")")
					.call(xAxis);

			svg.append("g")
					.attr("class", "y axis")
					.call(yAxis)
				.append("text")
					.attr("transform", "rotate(-90)")
					.attr("y", 6)
					.attr("dy", ".71em")
					.style("text-anchor", "end")
					.text("Viewers");

			svg.append("g")
				.append("text")
					.attr("x", 40)
					.attr("class", "title")
					.text(day);

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