$(document).ready(function() {

	d3.json("./data/esl_csgo.json", function(error, data) {

		if (error) return console.warn(error);

		// draw the segmented area chart
		var streams = data.streams.reverse();
		var selectedIdx = 0;
		var chart = segmentedAreaChart();
		var parsedIndices = {0: true, 1: false, 2: false, 3: false}

		d3.select("#esl-one-chart")
			.datum(streams[selectedIdx])
			.call(chart);

		// draw the arrows
		var previousArrow = leftArrow();
		d3.select(".left.arrow")
			.datum({
				titles: streams.map(function(s) { return s.day; })
			})
			.call(previousArrow);
		previousArrow.turnInvisible();

		var nextArrow = rightArrow();
		d3.select(".right.arrow")
			.datum({
				titles: streams.map(function(s) { return s.day; })
			})
			.call(nextArrow);

		// click functions for arrows

		previousArrow.onClick(function() {
			nextArrow.prev();
			selectedIdx -= 1;

			if (parsedIndices[selectedIdx]) chart.formatDate(false);

			d3.select("#esl-one-chart").select("svg").remove();
			
			d3.select("#esl-one-chart")
				.datum(streams[selectedIdx])
				.call(chart);
		})

		nextArrow.onClick(function() {
			previousArrow.next();
			selectedIdx += 1;
			if (!parsedIndices[selectedIdx]) {
				chart.formatDate(true);
				parsedIndices[selectedIdx] = true;
			}
			d3.select("#esl-one-chart").select("svg").remove();
			
			d3.select("#esl-one-chart")
				.datum(streams[selectedIdx])
				.call(chart);
		});

		// draw the retention chart
		var retentionChart = segmentedAreaChart()
								.margin({top: 10, right: 30, bottom: 0, left: 50})
								.width(280)
								.height(200)
								.showTitle(false)
								.formatDate(false);
		d3.select("#retention-chart")
			.datum({
				areas: [streams[0].areas[4]]
			})
			.call(retentionChart);
	});


	// draw the legend

	var legend = d3.selectAll(".legend")
		.append("svg")
			.attr("width", 1200)
			.attr("height", 20);

	legend.append("rect")
		.attr("x", 800)
		.attr("y", 0)
		.attr("width", 20)
		.attr("height", 20)
		.attr("class", "game");

	legend.append("text")
		.attr("x", 825)
		.attr("y", 14)
		.text("Game");

	legend.append("rect")
		.attr("x", 890)
		.attr("y", 0)
		.attr("width", 20)
		.attr("height", 20)
		.attr("class", "analysis");

	legend.append("text")
		.attr("x", 915)
		.attr("y", 14)
		.text("Analysis");

	legend.append("rect")
		.attr("x", 980)
		.attr("y", 0)
		.attr("width", 20)
		.attr("height", 20)
		.attr("class", "break");

	legend.append("text")
		.attr("x", 1005)
		.attr("y", 14)
		.text("Break");
})