let data;
let currentAlgorithmIndex = 0;
let execChart, iterChart, confChart, falseChart;

function showLoader(show=true) {
  document.getElementById('loader').style.display = show ? 'flex' : 'none';
}

function loadResults() {
  showLoader(true);
  const difficulty = document.getElementById('difficulty').value;
  const resultsFile = `./data/results_${difficulty}.json`;

  fetch(resultsFile)
    .then(res => {
      if (!res.ok) throw new Error(`Erreur chargement JSON: ${res.status}`);
      return res.json();
    })
    .then(json => {
      data = json;
      renderInitialGrid(data[0].grille_initiale);
      renderAlgorithmTabs(data);
      renderAllGrids(data);
      renderStatsTable(data);
      renderCharts(data);
      showLoader(false);
    })
    .catch(err => {
      showLoader(false);
      alert("❌ Erreur de chargement des résultats : " + err.message);
    });
}

function renderInitialGrid(grid) {
  const container = document.getElementById('initial-grid');
  container.innerHTML = '';
  grid.flat().forEach(value => {
    const cell = document.createElement('div');
    cell.className = 'cell initial';
    cell.textContent = value !== 0 ? value : '';
    container.appendChild(cell);
  });
}

function renderAlgorithmTabs(results) {
  const tabs = document.getElementById('algorithm-tabs');
  tabs.innerHTML = '';
  results.forEach((algo, i) => {
    const btn = document.createElement('button');
    btn.className = 'tab' + (i === 0 ? ' active' : '') + (algo.succes ? ' success' : ' failure');
    btn.textContent = `${algo.algorithme} ${algo.succes ? '✅' : '❌'}`;
    btn.onclick = () => switchTab(i);
    tabs.appendChild(btn);
  });
}

function renderAllGrids(results) {
  const container = document.getElementById('algorithm-results');
  container.innerHTML = '';

  results.forEach((algo, i) => {
    const div = document.createElement('div');
    div.className = 'algorithm-result' + (i === 0 ? ' active' : '') + (algo.succes ? ' success' : ' failure');

    const grid = document.createElement('div');
    grid.className = 'sudoku-grid';
    algo.grille_resolue.flat().forEach(val => {
      const cell = document.createElement('div');
      cell.className = 'cell solution';
      cell.textContent = val !== 0 ? val : '';
      grid.appendChild(cell);
    });

    const perf = document.createElement('div');
    perf.className = 'algorithm-performance';
    perf.innerHTML = `
      <div class="performance-metrics">
        <div class="metric">
          <div class="metric-value">${algo.temps.toFixed(2)}</div>
          <div class="metric-label">Temps (s)</div>
        </div>
        <div class="metric">
          <div class="metric-value">${algo.iterations}</div>
          <div class="metric-label">Itérations</div>
        </div>
        <div class="metric">
          <div class="metric-value">${algo.conflicts}</div>
          <div class="metric-label">Conflits</div>
        </div>
        <div class="metric">
          <div class="metric-value">${algo.cases_fausses}</div>
          <div class="metric-label">Cases fausses</div>
        </div>
      </div>
    `;

    div.appendChild(grid);
    div.appendChild(perf);
    container.appendChild(div);
  });
}

function switchTab(index) {
  currentAlgorithmIndex = index;
  document.querySelectorAll('.tab').forEach((t, i) => t.classList.toggle('active', i === index));
  document.querySelectorAll('.algorithm-result').forEach((r, i) => r.classList.toggle('active', i === index));
}

function renderStatsTable(results) {
  const tbody = document.getElementById('stats-table-body');
  tbody.innerHTML = '';
  results.forEach(algo => {
    const row = document.createElement('tr');
    row.className = algo.succes ? 'success' : 'failure';
    row.innerHTML = `
      <td>${algo.algorithme}</td>
      <td>${algo.temps.toFixed(2)}</td>
      <td>${algo.iterations}</td>
      <td>${algo.conflicts}</td>
      <td>${algo.cases_fausses}</td>
      <td>${algo.succes ? '✅' : '❌'}</td>
    `;
    tbody.appendChild(row);
  });
}

function renderCharts(results) {
  const labels = results.map(r => r.algorithme);
  const times = results.map(r => r.temps);
  const iterations = results.map(r => r.iterations);
  const conflicts = results.map(r => r.conflicts);
  const fausses = results.map(r => r.cases_fausses);

  const config = (label, data, color) => ({
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: label,
        data: data,
        backgroundColor: color,
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false }
      },
      scales: {
        y: { beginAtZero: true }
      }
    }
  });

  // Destroy previous charts to avoid overlap
  if (execChart) execChart.destroy();
  if (iterChart) iterChart.destroy();
  if (confChart) confChart.destroy();
  if (falseChart) falseChart.destroy();

  execChart = new Chart(document.getElementById('execution-time-chart'), config('Temps (s)', times, '#4d8bff'));
  iterChart = new Chart(document.getElementById('iterations-chart'), config('Itérations', iterations, '#22c55e'));
  confChart = new Chart(document.getElementById('conflicts-chart'), config('Conflits', conflicts, '#ef4444'));
  falseChart = new Chart(document.getElementById('false-cells-chart'), config('Cases fausses', fausses, '#f59e0b'));
}

// Bouton pour relancer les solveurs depuis Flask
document.getElementById('run-btn').addEventListener('click', () => {
  const difficulty = document.getElementById('difficulty').value;
  showLoader(true);
  fetch(`http://localhost:5000/run?difficulty=${difficulty}`)
    .then(response => {
      showLoader(false);
      if (response.ok) {
        alert("Résolution terminée. Rafraîchissement automatique...");
        setTimeout(() => location.reload(), 1200);
      } else {
        alert("Échec de la génération des résultats.");
      }
    })
    .catch(err => {
      showLoader(false);
      alert("Erreur réseau ou serveur : " + err);
    });
});

// Mise à jour des résultats à chaque changement de difficulté
document.getElementById('difficulty').addEventListener('change', loadResults);

// Chargement initial
window.addEventListener('DOMContentLoaded', loadResults);
