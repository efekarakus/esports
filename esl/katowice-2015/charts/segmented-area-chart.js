function segmentedAreaChart()
{
	var margin = {top: 20, right: 0, bottom: 30, left: 50},
		width = 1000 - margin.left - margin.right,
		height = 300 - margin.top - margin.bottom;

	var showTitle = true,
		formatDate = true;

	var parseDate = d3.time.format("%Y-%m-%d %H:%M:%S");

	var teamToImg = {
		"TEAM ENVYUS": "envy",
		"Titan": "titan",
		"LGB eSports": "lgbesports",
		"Natus Vincere": "natusvincere",
		"fnatic": "fnatic",
		"Vox Eminor": "vox",
		"Ninjas in Pyjamas": "nip",
		"Counter Logic Gaming": "clg",
		"Virtus.Pro": "virtuspro",
		"Cloud9 G2A": "cloud9",
		"Keyd Stars": "keydstars",
		"PENTA Sports": "pentasports",
		"TSM Kinguin": "tsm"
	}

	function chart(selection) {
		selection.each(function(data) {
			
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

			var title = data.day;
			var areas = data.areas;

			var maxCount = 0,
				minCount = 999999;

			var minDate = new Date(2999, 12, 12),
				maxDate = new Date(0, 1, 1);

			areas.forEach(function(area) {
				var points = area.points;
				points.forEach(function(point) {

					point.count  = +point.count;
					point.timestamp = formatDate ? parseDate.parse(point.timestamp) : point.timestamp;

					minCount = minCount > point.count ? point.count : minCount;
					maxCount = maxCount < point.count ? point.count : maxCount;
					minDate = minDate > point.timestamp ? point.timestamp : minDate;
					maxDate = maxDate < point.timestamp ? point.timestamp : maxDate;
				})
			});

			x.domain([minDate, maxDate]);
			y.domain([minCount, maxCount]);

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
					.text(showTitle ? title : "");


			var games = areas.filter(function(area) { return area.type === "game"; });
			var ignoreList = [
				{scoreA: 1, scoreB: 0, teamA: "TEAM ENVYUS", teamB: "Natus Vincere"},
				{scoreA: 16, scoreB: 1, teamA: "Virtus.Pro", teamB: "Keyd Stars"},
				{scoreA: 17, scoreB: 19, teamA: "Virtus.Pro", teamB: "Keyd Stars"},
				{scoreA: 16, scoreB: 4, teamA: "Virtus.Pro", teamB: "Keyd Stars"}
			]

			games = games.filter(function(game) {
				for (var i  = 0; i < ignoreList.length; i++) {
					var ignore = ignoreList[i];
					if (game.scoreA === ignore.scoreA 
						&& game.scoreB === ignore.scoreB
						&& game.teamA === ignore.teamA
						&& game.teamB === ignore.teamB)
						return false;
				}
				return true;
			});

			games.forEach(function(game) {
				var points = game.points.slice();
				points.sort(function(a, b) { return b.count - a.count });

				var medianCount = points[Math.floor(points.length/2)].count;
				var medianTime = points[Math.floor(points.length/2)].timestamp;

				var circle = svg.append("circle")
					.attr("cx", x(medianTime))
					.attr("cy", y(medianCount))
					.attr("r", 8)
					.attr("class", "details"); 

				$(circle[0][0]).qtip({
					content: {
						text: 
							"<table>" +
								"<tr><td><img src='./styles/images/team-logos/"+ teamToImg[game.teamA] +".png'>" 
								+"</img></td><td class='title'>" + game.teamA + "</td><td>" + game.scoreA + "</td></tr>" +

								"<tr><td><img src='./styles/images/team-logos/"+ teamToImg[game.teamB] +".png'>" 
								+"</img></td><td class='title'>" + game.teamB + "</td><td>" + game.scoreB + "</td></tr>" +
							"</table>"
					},
					style: {
						classes: "sar-darkblue qtip-shadow",
					},
					position: {
						my: 'bottom center',
						at: 'top center',
						adjust: {
							x: 10,
							y: -3
						}
					}
				})
			});
		});
	}

	chart.margin = function(_) {
		if (!arguments.length) return margin;
		margin = _;
		return chart;
	}

	chart.width = function(_) {
		if (!arguments.length) return width;
		width = _ - margin.left - margin.right;
		return chart;
	}

	chart.height = function(_) {
		if (!arguments.length) return height;
		height = _ - margin.top - margin.bottom;;
		return chart;
	}

	chart.showTitle = function(_) {
		if (!arguments.length) return showTitle;
		showTitle = _;
		return chart;
	}

	chart.formatDate = function(_) {
		if (!arguments.length) return formatDate;
		formatDate = _;
		return chart;
	}

	return chart;
}