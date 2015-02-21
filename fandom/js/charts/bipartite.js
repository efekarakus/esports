function bipartite() {
	var margin = {top: 0, right: 0, bottom: 10, left: 0},
		width = 1000,
		height = 500;

	var S3_START = 0,
		VIS_START = 200,
		S4_START = 800;

	var BAR_WIDTH = 30;

	function reformat(data, season)
	{
		var collection = [];
		var teams = Object.keys(data[season]);

		teams.forEach(function(team) {
			var values = Object.keys(data[season][team]);
			var entry = {
				"name": team
			}

			values.forEach(function(value) {
				entry[value] = data[season][team][value];
			})

			collection.push(entry);
		});

		collection.sort(function(a, b) {
			return b.count - a.count;
		})

		return collection;
	}

	function scale(data) 
	{
		var max = 0;
		data.forEach(function(d) {
			max += d.count;
		});

		return d3.scale.linear()
			.domain([0, max])
			.range([0, height]);
	}

	function sumTill(data, limit) 
	{
		var sum = 0;
		for (var i = 0; i < data.length; i++) {
			if (i === limit) break;

			sum += data[i].count;
		}
		return sum;
	}

	function className(name) {
		var abbrs = {
			"Counter Logic Gaming": "CLG",
			"Curse": "CRS",
			"Team Dignitas": "DIG",
			"LMQ": "LMQ",
			"Cloud9": "C9",
			"Team SoloMid": "TSM",
			"compLexity Black": "COL",
			"Evil Geniuses": "EG",
			"empty": "EMPTY",
			"Gravity": "GV",
			"Team 8": "T8",
			"Team Impulse": "TIP",
			"Team Liquid": "TL",
			"Winterfox": "WFX",
			"Team Coast": "CST",
			"Alliance": "ALL",
			"Fnatic": "FNC",
			"Supa Hot Crew": "SHC",
			"SK Gaming": "SK",
			"Millenium": "MIL",
			"ROCCAT": "ROC",
			"Copenhagen Wolves": "CW",
			"Gambit Gaming": "GMB",
			"Elements": "EL",
			"GIANTS GAMING": "GIA",
			"H2k": "H2K",
			"Unicorns of Love": "UOL",
			"Meet Your Makers": "MYM"
		}

		return abbrs[name];
	}

	function chart(selection) {
		selection.each(function(data) {
			var svg = d3.select(this)
				.append("svg")
				.attr("width", width)
				.attr("height", height);

			var s4 = reformat(data, "s4");
			var s5 = reformat(data, "s5");

			var s4scale = scale(s4);
			var s5scale = scale(s5);

			// build s4 bars
			var s4bars = svg.selectAll(".s4bars")
				.data(s4)
				.enter()
				.append("rect");

			s4bars.attr("x", VIS_START)
				.attr("y", function(d, i) { return s4scale(sumTill(s4, i)); })
				.attr("width", BAR_WIDTH)
				.attr("height", function(d) { return s4scale(d.count); })
				.attr("class", function(d) { return className(d.name); });

			// build s5 bars
			var s5bars = svg.selectAll(".s5bars")
				.data(s5)
				.enter()
				.append("rect");

			s5bars.attr("x", S4_START - BAR_WIDTH)
				.attr("y", function(d, i) { return s5scale(sumTill(s5, i)); })
				.attr("width", BAR_WIDTH)
				.attr("height", function(d) { return s5scale(d.count); })
				.attr("class", function(d) { return className(d.name); });
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