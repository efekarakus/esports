$(document).ready(function() {

	d3.json("./data/esl_csgo.json", function(error, data) {

		if (error) return console.warn(error);

		var streams = data.streams;

		streams.forEach(function(stream) {
			var streamId = stream.stream_id;

			var chart = segmentedAreaChart();

			d3.select("#esl-one-" + streamId)
				.datum(stream)
				.call(chart);

		});

	});

})