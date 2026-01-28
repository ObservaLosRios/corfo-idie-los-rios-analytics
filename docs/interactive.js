document.addEventListener('DOMContentLoaded', () => {
	initNavigation();
	initFinanciamientoLineChart();
	initFinanciamientoBarChart();
	initProyectosLineChart();
});

function getExportingOptions() {
	return {
		enabled: true,
		buttons: {
			contextButton: {
				menuItems: [
					'viewFullscreen',
					'printChart',
					'separator',
					'downloadPNG',
					'downloadJPEG',
					'downloadSVG',
					'separator',
					'downloadCSV',
					'downloadXLS',
					'viewData'
				]
			}
		}
	};
}

function initNavigation() {
	const navLinks = document.querySelectorAll('.nav-link');
	const sections = document.querySelectorAll('.section');

	const activateSection = targetId => {
		sections.forEach(section => {
			section.classList.toggle('active', section.id === targetId);
		});
		navLinks.forEach(link => {
			link.classList.toggle('active', link.dataset.section === targetId);
		});
	};

	navLinks.forEach(link => {
		link.addEventListener('click', () => activateSection(link.dataset.section));
	});

	const initialSection = navLinks[0]?.dataset.section;
	if (initialSection) {
		activateSection(initialSection);
	}
}

function triggerReloadEffect(container) {
	if (!container) return;
	container.classList.add('chart-loaded');
	container.classList.remove('reload-pulse');
	void container.offsetWidth; // force reflow for animation restart
	container.classList.add('reload-pulse');
	setTimeout(() => container.classList.remove('reload-pulse'), 600);
}

function initFinanciamientoBarChart() {
	if (typeof Highcharts === 'undefined') return;
	const containerId = 'financiamiento-bar-chart';
	const containerEl = document.getElementById(containerId);
	if (!containerEl) return;

	const targetRegion = 'Región de Los Ríos';
	const highlightColor = '#C0392B';
	const economistPalette = ['#17415F', '#2E5A74', '#698494', '#A9B4BE'];
	const data = [
		{ name: 'Región del Biobío', value: 49332.45 },
		{ name: 'Región de los Lagos', value: 40442.98 },
		{ name: 'Región de La Araucanía', value: 19769.51 },
		{ name: 'Región de Los Ríos', value: 13448.13 }
	];

	const chart = Highcharts.chart(containerId, {
		chart: {
			type: 'column',
			backgroundColor: 'transparent',
			style: {
				fontFamily: 'Inter, system-ui, -apple-system, BlinkMacSystemFont, sans-serif'
			}
		},
		title: { text: 'Financiamiento Innova por región (MM CLP)' },
		xAxis: {
			type: 'category',
			title: { text: 'Región', style: { fontWeight: 'bold' } },
			labels: { rotation: -35, style: { fontSize: '0.9rem' } }
		},
		yAxis: {
			allowDecimals: false,
			title: { text: 'Financiamiento (MM CLP)' }
		},
		legend: { enabled: false },
		tooltip: { valueSuffix: ' MM CLP' },
		plotOptions: {
			column: {
				borderRadius: 6,
				pointPadding: 0.15,
				dataLabels: {
					enabled: true,
					format: '{point.y:.1f}',
					style: { fontWeight: '600' }
				}
			}
		},
		series: [{
			data: data.map((point, index) => ({
				name: point.name,
				y: point.value,
				color: point.name === targetRegion ? highlightColor : economistPalette[index % economistPalette.length]
			}))
		}],
		exporting: getExportingOptions(),
		credits: { enabled: false }
	});
	triggerReloadEffect(containerEl);
}

function initFinanciamientoLineChart() {
	if (typeof Highcharts === 'undefined') return;
	const containerId = 'financiamiento-line-chart';
	const containerEl = document.getElementById(containerId);
	if (!containerEl) return;

	const palette = {
		losRios: '#1DA0FF',
		biobio: '#6F52ED',
		lagos: '#16C47F',
		araucania: '#FF7B39'
	};

	const seriesData = [
		{
			name: 'Región del Biobío',
			color: palette.biobio,
			marker: { symbol: 'diamond' },
			data: [760.91, 1871.37, 1982.01, 2808.48, 624.45, 1667.64, 5299.00, 5443.20, 4922.88, 2088.35, 3300.90, 1187.01, 2311.04, 2917.03, 4358.26, 4877.75, 2912.18]
		},
		{
			name: 'Región de los Lagos',
			color: palette.lagos,
			marker: { symbol: 'square' },
			data: [4000.67, 1009.35, 2441.03, 3146.14, 1527.42, 2182.44, 2596.22, 3340.47, 3679.56, 3283.38, 2357.93, 1215.47, 1649.61, 1691.51, 2404.96, 3257.02, 659.81]
		},
		{
			name: 'Región de La Araucanía',
			color: palette.araucania,
			marker: { symbol: 'triangle' },
			data: [596.51, 1852.06, 2565.90, 2288.24, 1058.12, 990.15, 1347.63, 1202.58, 660.64, 1753.35, 649.42, 500.37, 488.87, 356.84, 1867.95, 959.77, 631.10]
		},
		{
			name: 'Región de Los Ríos',
			color: palette.losRios,
			lineWidth: 4,
			marker: { enabled: true, radius: 5, symbol: 'circle' },
			data: [402.82, 279.14, 2127.86, 1000.61, 582.98, 1083.99, 994.78, 826.04, 537.24, 467.28, 357.41, 176.29, 397.77, 783.23, 910.09, 1816.51, 704.09]
		}
	];

	const chart = Highcharts.chart(containerId, {
		chart: {
			backgroundColor: 'transparent',
			style: {
				fontFamily: 'Inter, system-ui, -apple-system, BlinkMacSystemFont, sans-serif'
			}
		},
		title: {
			text: 'Crecimiento del financiamiento Innova por región',
			align: 'left'
		},
		yAxis: {
			title: { text: 'Monto (MM CLP)' }
		},
		xAxis: {
			title: { text: 'Año de Adjudicación', style: { fontWeight: 'bold' } },
			accessibility: { rangeDescription: 'Cobertura 2009-2025' }
		},
		legend: {
			layout: 'vertical',
			align: 'right',
			verticalAlign: 'middle'
		},
		tooltip: {
			shared: true,
			valueSuffix: ' MM CLP'
		},
		plotOptions: {
			series: {
				label: { connectorAllowed: false },
				marker: {
					enabled: true,
					radius: 4,
					lineWidth: 1,
					lineColor: '#ffffff'
				},
				pointStart: 2009
			}
		},
		series: seriesData,
		exporting: getExportingOptions(),
		credits: { enabled: false },
		responsive: {
			rules: [{
				condition: { maxWidth: 640 },
				chartOptions: {
					legend: {
						layout: 'horizontal',
						align: 'center',
						verticalAlign: 'bottom'
					}
				}
			}]
		}
	});
	triggerReloadEffect(containerEl);
}

function initProyectosLineChart() {
	if (typeof Highcharts === 'undefined') return;
	const containerId = 'proyectos-line-chart';
	const containerEl = document.getElementById(containerId);
	if (!containerEl) return;

	const palette = {
		losRios: '#1DA0FF',
		biobio: '#6F52ED',
		lagos: '#16C47F',
		araucania: '#FF7B39'
	};

	const seriesData = [
		{
			name: 'Región del Biobío',
			color: palette.biobio,
			marker: { symbol: 'diamond' },
			data: [5, 14, 33, 32, 13, 25, 64, 70, 96, 40, 56, 45, 56, 66, 31, 38, 22]
		},
		{
			name: 'Región de los Lagos',
			color: palette.lagos,
			marker: { symbol: 'square' },
			data: [20, 28, 32, 41, 19, 36, 48, 69, 68, 57, 35, 47, 65, 48, 40, 31, 7]
		},
		{
			name: 'Región de La Araucanía',
			color: palette.araucania,
			marker: { symbol: 'triangle' },
			data: [7, 31, 42, 29, 18, 22, 33, 31, 41, 39, 12, 16, 21, 18, 18, 12, 10]
		},
		{
			name: 'Región de Los Ríos',
			color: palette.losRios,
			lineWidth: 4,
			marker: { enabled: true, radius: 5, symbol: 'circle' },
			data: [3, 8, 19, 13, 8, 15, 29, 15, 18, 7, 3, 8, 12, 16, 11, 12, 8]
		}
	];

	const chart = Highcharts.chart(containerId, {
		chart: {
			backgroundColor: 'transparent',
			style: {
				fontFamily: 'Inter, system-ui, -apple-system, BlinkMacSystemFont, sans-serif'
			}
		},
		title: {
			text: 'Conteo de proyectos adjudicados (Top regiones)',
			align: 'left'
		},
		yAxis: {
			title: { text: 'Número de proyectos' },
			allowDecimals: false
		},
		xAxis: {
			title: { text: 'Año de Adjudicación', style: { fontWeight: 'bold' } },
			accessibility: { rangeDescription: 'Cobertura 2009-2025' }
		},
		legend: {
			layout: 'vertical',
			align: 'right',
			verticalAlign: 'middle'
		},
		tooltip: {
			shared: true,
			valueSuffix: ' proyectos'
		},
		plotOptions: {
			series: {
				label: { connectorAllowed: false },
				marker: {
					enabled: true,
					radius: 4,
					lineWidth: 1,
					lineColor: '#ffffff'
				},
				pointStart: 2009
			}
		},
		series: seriesData,
		exporting: getExportingOptions(),
		credits: { enabled: false },
		responsive: {
			rules: [{
				condition: { maxWidth: 640 },
				chartOptions: {
					legend: {
						layout: 'horizontal',
						align: 'center',
						verticalAlign: 'bottom'
					}
				}
			}]
		}
	});
	triggerReloadEffect(containerEl);
}
