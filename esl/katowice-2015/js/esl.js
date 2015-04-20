$(document).ready(function() {

	d3.json("./data/esl_csgo.json", function(error, data) {

		if (error) return console.warn(error);

		var streams = data.streams.reverse();

		var streamId = streams[0].stream_id;

		var chart = segmentedAreaChart();

		d3.select("#esl-one-chart")
			.datum(streams[0])
			.call(chart);


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