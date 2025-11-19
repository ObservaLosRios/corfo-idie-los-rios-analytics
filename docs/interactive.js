document.addEventListener('DOMContentLoaded', () => {
	initNavigation();
	initFinanciamientoBarChart();
	initFinanciamientoLineChart();
	initProyectosLineChart();
});

const baseThemes = {
	light: {
		text: '#0f172a',
		muted: '#4b5563',
		grid: '#d1d5db',
		tooltipBg: 'rgba(255,255,255,0.95)',
		tooltipBorder: '#d1d5db'
	},
	dark: {
		text: '#f3f4f6',
		muted: '#cbd5f5',
		grid: '#475569',
		tooltipBg: 'rgba(15,23,42,0.9)',
		tooltipBorder: '#475569'
	}
};

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

function updateToggleIcon(button, theme) {
	if (!button) return;
	const isLight = theme === 'light';
	button.textContent = isLight ? '🌙' : '☀️';
	button.setAttribute('aria-pressed', String(!isLight));
}

function initFinanciamientoBarChart() {
	if (typeof Highcharts === 'undefined') return;
	const containerId = 'financiamiento-bar-chart';
	const containerEl = document.getElementById(containerId);
	const toggleButton = document.getElementById('financiamiento-bar-toggle');
	const card = toggleButton ? toggleButton.closest('.chart-card') : null;
	if (!containerEl || !toggleButton || !card) return;

	const targetRegion = 'Región de Los Ríos';
	const highlightColor = '#C0392B';
	const economistPalette = ['#17415F', '#2E5A74', '#698494', '#A9B4BE'];
	const data = [
		{ name: 'Región del Biobío', value: 43457.46 },
		{ name: 'Región de los Lagos', value: 36105.10 },
		{ name: 'Región de La Araucanía', value: 18621.40 },
		{ name: 'Región de Los Ríos', value: 11263.68 }
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
		subtitle: { text: 'Fuente: ETL CORFO - elaboración propia' },
		xAxis: {
			type: 'category',
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
		credits: { enabled: false }
	});

	let currentTheme = 'light';

	const applyTheme = theme => {
		const palette = baseThemes[theme];
		card.setAttribute('data-theme', theme);
		chart.update({
			title: { style: { color: palette.text } },
			subtitle: { style: { color: palette.muted } },
			tooltip: {
				backgroundColor: palette.tooltipBg,
				borderColor: palette.tooltipBorder,
				style: { color: palette.text }
			},
			plotOptions: {
				column: {
					dataLabels: {
						style: { color: palette.text }
					}
				}
			}
		}, false);

		chart.xAxis[0].update({
			labels: { style: { color: palette.text } },
			lineColor: palette.grid,
			tickColor: palette.grid
		}, false);

		chart.yAxis[0].update({
			labels: { style: { color: palette.text } },
			title: { style: { color: palette.text } },
			gridLineColor: palette.grid
		}, false);

		chart.redraw();
		updateToggleIcon(toggleButton, theme);
	};

	toggleButton.addEventListener('click', () => {
		currentTheme = currentTheme === 'light' ? 'dark' : 'light';
		applyTheme(currentTheme);
	});

	applyTheme(currentTheme);
	triggerReloadEffect(containerEl);
}

function initFinanciamientoLineChart() {
	if (typeof Highcharts === 'undefined') return;
	const containerId = 'financiamiento-line-chart';
	const containerEl = document.getElementById(containerId);
	const toggleButton = document.getElementById('financiamiento-line-toggle');
	const card = toggleButton ? toggleButton.closest('.chart-card') : null;
	if (!containerEl || !toggleButton || !card) return;

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
			data: [760.91, 1523.84, 1719.92, 2366.97, 624.45, 1667.64, 5117.76, 5158.2, 4442.28, 1892.58, 3221.4, 1187.01, 2311.04, 2747.18, 2970.02, 2954.09, 2792.18]
		},
		{
			name: 'Región de los Lagos',
			color: palette.lagos,
			marker: { symbol: 'square' },
			data: [3994.67, 873.87, 2267.49, 3087.66, 1444.69, 1988.39, 2440.72, 3151.55, 3336.79, 3031.21, 2219.95, 1205.47, 1625.21, 1501.56, 2126.64, 1356.88, 452.35]
		},
		{
			name: 'Región de La Araucanía',
			color: palette.araucania,
			marker: { symbol: 'triangle' },
			data: [596.51, 1785.56, 2565.9, 2210.91, 1058.12, 954.15, 1262.7, 1188.98, 583.47, 1753.35, 649.42, 337.82, 448.87, 331.88, 1838.55, 502.87, 552.33]
		},
		{
			name: 'Región de Los Ríos',
			color: palette.losRios,
			lineWidth: 4,
			marker: { enabled: true, radius: 5, symbol: 'circle' },
			data: [367.93, 279.14, 1430.88, 1000.61, 582.98, 1018.21, 970.73, 826.04, 487.25, 467.28, 357.41, 176.29, 387.77, 783.23, 829.09, 674.66, 624.19]
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
		subtitle: {
			text: 'Fuente: ETL CORFO - elaboración propia',
			align: 'left'
		},
		yAxis: {
			title: { text: 'Monto (MM CLP)' }
		},
		xAxis: {
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

	let currentTheme = 'light';

	const applyTheme = theme => {
		const palette = baseThemes[theme];
		card.setAttribute('data-theme', theme);

		chart.setTitle(
			{
				text: 'Crecimiento del financiamiento Innova por región',
				style: { color: palette.text }
			},
			{
				text: 'Fuente: ETL CORFO - elaboración propia',
				style: { color: palette.muted }
			},
			false
		);

		chart.xAxis[0].update({
			labels: { style: { color: palette.text } },
			lineColor: palette.grid,
			tickColor: palette.grid
		}, false);

		chart.yAxis[0].update({
			labels: { style: { color: palette.text } },
			title: { style: { color: palette.text } },
			gridLineColor: palette.grid
		}, false);

		chart.update({
			legend: {
				itemStyle: { color: palette.text },
				itemHoverStyle: { color: palette.muted }
			},
			tooltip: {
				backgroundColor: palette.tooltipBg,
				borderColor: palette.tooltipBorder,
				style: { color: palette.text }
			}
		}, false);

		chart.redraw();
		updateToggleIcon(toggleButton, theme);
	};

	toggleButton.addEventListener('click', () => {
		currentTheme = currentTheme === 'light' ? 'dark' : 'light';
		applyTheme(currentTheme);
	});

	applyTheme(currentTheme);
	triggerReloadEffect(containerEl);
}

function initProyectosLineChart() {
	if (typeof Highcharts === 'undefined') return;
	const containerId = 'proyectos-line-chart';
	const containerEl = document.getElementById(containerId);
	const toggleButton = document.getElementById('proyectos-line-toggle');
	const card = toggleButton ? toggleButton.closest('.chart-card') : null;
	if (!containerEl || !toggleButton || !card) return;

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
			data: [5, 12, 29, 29, 13, 25, 63, 67, 88, 38, 54, 45, 56, 63, 23, 33, 19]
		},
		{
			name: 'Región de los Lagos',
			color: palette.lagos,
			marker: { symbol: 'square' },
			data: [19, 27, 29, 39, 18, 33, 43, 64, 60, 50, 34, 46, 64, 44, 37, 26, 4]
		},
		{
			name: 'Región de La Araucanía',
			color: palette.araucania,
			marker: { symbol: 'triangle' },
			data: [7, 28, 42, 28, 18, 21, 31, 29, 39, 39, 12, 14, 19, 17, 17, 10, 8]
		},
		{
			name: 'Región de Los Ríos',
			color: palette.losRios,
			lineWidth: 4,
			marker: { enabled: true, radius: 5, symbol: 'circle' },
			data: [2, 8, 18, 13, 8, 14, 28, 15, 17, 7, 3, 8, 11, 16, 9, 11, 6]
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
		subtitle: {
			text: 'Fuente: ETL CORFO - elaboración propia',
			align: 'left'
		},
		yAxis: {
			title: { text: 'Número de proyectos' },
			allowDecimals: false
		},
		xAxis: {
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

	let currentTheme = 'light';

	const applyTheme = theme => {
		const palette = baseThemes[theme];
		card.setAttribute('data-theme', theme);

		chart.setTitle(
			{
				text: 'Conteo de proyectos adjudicados (Top regiones)',
				style: { color: palette.text }
			},
			{
				text: 'Fuente: ETL CORFO - elaboración propia',
				style: { color: palette.muted }
			},
			false
		);

		chart.xAxis[0].update({
			labels: { style: { color: palette.text } },
			lineColor: palette.grid,
			tickColor: palette.grid
		}, false);

		chart.yAxis[0].update({
			labels: { style: { color: palette.text } },
			title: { style: { color: palette.text } },
			gridLineColor: palette.grid
		}, false);

		chart.update({
			legend: {
				itemStyle: { color: palette.text },
				itemHoverStyle: { color: palette.muted }
			},
			tooltip: {
				backgroundColor: palette.tooltipBg,
				borderColor: palette.tooltipBorder,
				style: { color: palette.text }
			}
		}, false);

		chart.redraw();
		updateToggleIcon(toggleButton, theme);
	};

	toggleButton.addEventListener('click', () => {
		currentTheme = currentTheme === 'light' ? 'dark' : 'light';
		applyTheme(currentTheme);
	});

	applyTheme(currentTheme);
	triggerReloadEffect(containerEl);
}
