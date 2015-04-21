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

})