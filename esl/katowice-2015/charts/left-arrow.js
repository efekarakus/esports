function leftArrow() {
	var width = 100,
		height = 300;

	var sideLength = width/2;
	var svg;

	var titles = [],
		titleIndex = -1;

	function chart(selection) {
		selection.each(function(data) {
			titles = data.titles;

			svg = d3.select(this)
				.append("svg")
					.attr("width", width)
					.attr("height", height);

			var arrow = svg.append("g")
					.attr("class", "visible");


			var triangleHeight = Math.sqrt(sideLength*sideLength - (sideLength/2)*(sideLength/2));

			var positions = [
				{x: (width/2 + sideLength/2), y: (height/2 - sideLength/2)},
				{x: (width/2 + sideLength/2), y: (height/2 + sideLength/2)},
				{x: (width/2 + sideLength/2) - triangleHeight, y: height/2}
			]

			arrow.append("path")
				.attr("d",	"M " + positions[0].x + " " + positions[0].y + " " +
							"L " + positions[1].x + " " + positions[1].y + " " +
							"L " + positions[2].x + " " + positions[2].y + " " +
							"L " + positions[0].x + " " + positions[0].y);

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

	chart.sideLength = function(_) {
		if (!arguments.length) return sideLength;
		sideLength = _;
		return chart;
	}

	chart.turnInvisible = function() {
		svg.select("g.visible")
				.attr("class", "invisible");
	}

	chart.turnVisible = function() {
		svg.select("g.invisible")
				.attr("class", "visible");
	}

	chart.prev = function() {
		if (titleIndex === 0 || titleIndex === -1) {
			titleIndex = -1;
			chart.turnInvisible();
		} else {
			titleIndex -= 1;
			// TODO update tooltip
		}
	}

	chart.next = function() {
		if (titleIndex === -1) {
			chart.turnVisible();
		}

		if (titleIndex !== titles.length) {
			titleIndex += 1;
			// TODO update tooltip
		}
	}

	chart.onClick = function(f) {
		var arrow = svg.select("g");

		arrow.on("click", function() {
			f();
			chart.prev();
		});
	}

	return chart;
}