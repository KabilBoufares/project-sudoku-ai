let currentDifficulty = 'expert';
let algorithmData = null;

/**
 * Initialise l'application
 */
function initApp() {
  setupEventListeners();
  loadData();
  initParticles();
}

/**
 * Gestion des événements
 */
function setupEventListeners() {
  const difficultySelect = document.getElementById('difficulty');
  difficultySelect.addEventListener('change', (e) => {
    currentDifficulty = e.target.value.toLowerCase();
    loadData();
  });

  const runLevelButton = document.getElementById('run-level');
  runLevelButton.addEventListener('click', () => {
    runLevel(currentDifficulty);
  });

  const runAllButton = document.getElementById('run-all');
  runAllButton.addEventListener('click', runAllLevels);
}

/**
 * Charge les résultats depuis le fichier JSON selon la difficulté
 */
function loadData() {
  showLoadingState();

  const filePath = `./data/results_${currentDifficulty}.json`;
  fetch(filePath)
    .then(res => {
      if (!res.ok) throw new Error(`Fichier non trouvé : ${filePath}`);
      return res.json();
    })
    .then(json => {
      algorithmData = json;
      renderData(algorithmData);
    })
    .catch(err => {
      console.error("Erreur de chargement JSON:", err);
      showErrorState("Impossible de charger les données : " + err.message);
    });
}

/**
 * Affiche les placeholders de chargement
 */
function showLoadingState() {
  document.getElementById('initial-grid').innerHTML = '<div class="loading-spinner">Loading...</div>';
  document.getElementById('algorithm-tabs').innerHTML = '<div class="loading-spinner">Loading algorithms...</div>';
  document.getElementById('results-container').innerHTML = '';
  document.getElementById('comparison-body').innerHTML = '<tr><td colspan="8" class="loading-spinner">Loading comparison data...</td></tr>';
  document.getElementById('analysis-container').innerHTML = '<div class="loading-spinner">Generating analysis...</div>';
}

/**
 * Affiche un message d'erreur en cas de souci
 */
function showErrorState(message) {
  const errorHTML = `<div class="error-message">${message}</div>`;
  document.getElementById('initial-grid').innerHTML = errorHTML;
  document.getElementById('algorithm-tabs').innerHTML = errorHTML;
  document.getElementById('results-container').innerHTML = errorHTML;
  document.getElementById('comparison-body').innerHTML = `<tr><td colspan="8">${errorHTML}</td></tr>`;
  document.getElementById('analysis-container').innerHTML = errorHTML;
}

/**
 * Rend toutes les données à l'écran
 */
function renderData(data) {
  if (!data || !data.length) {
    showErrorState('Aucune donnée disponible');
    return;
  }

  GridRenderer.renderInitialGrid(data[0].grille_initiale);
  GridRenderer.createAlgorithmTabs(data);
  ComparisonGenerator.generateComparisonTable(data);
  ChartRenderer.renderCharts(data);
  AnalysisGenerator.generateAnalysis(data);
}

/**
 * Lance la génération des résultats pour un niveau
 */
function runLevel(difficulty) {
  const runBtn = document.getElementById('run-level');
  runBtn.disabled = true;
  runBtn.innerHTML = '<span class="button-icon">⏳</span> Running...';

  fetch(`/run?difficulty=${difficulty}`)
    .then(res => {
      if (!res.ok) throw new Error('Erreur serveur');
      return res.json();
    })
    .then(data => {
      if (data.success) {
        setTimeout(() => {
          loadData();
          runBtn.disabled = false;
          runBtn.innerHTML = '<span class="button-icon">🔄</span> Run Level';
        }, 1000);
      } else {
        showErrorState(data.error || "Erreur inconnue.");
        runBtn.disabled = false;
      }
    })
    .catch(err => {
      showErrorState("Erreur réseau : " + err.message);
      runBtn.disabled = false;
      runBtn.innerHTML = '<span class="button-icon">🔄</span> Run Level';
    });
}

/**
 * Simule un run pour tous les niveaux (extension future)
 */
function runAllLevels() {
  const runAllBtn = document.getElementById('run-all');
  runAllBtn.disabled = true;
  runAllBtn.innerHTML = '<span class="button-icon">⏳</span> Running All...';

  // À compléter si tu veux exécuter tous les niveaux
  setTimeout(() => {
    loadData();
    runAllBtn.disabled = false;
    runAllBtn.innerHTML = '<span class="button-icon">🚀</span> Run All';
  }, 2000);
}

/**
 * Anime le fond avec des particules
 */
function initParticles() {
  const container = document.querySelector('.particles-background');
  if (!container) return;

  for (let i = 0; i < 50; i++) {
    const particle = document.createElement('div');
    particle.className = 'particle';
    particle.style.left = `${Math.random() * 100}%`;
    particle.style.top = `${Math.random() * 100}%`;
    const size = `${Math.random() * 5 + 2}px`;
    particle.style.width = size;
    particle.style.height = size;
    particle.style.opacity = Math.random() * 0.5 + 0.1;
    particle.style.background = `rgba(${Math.random()*255}, ${Math.random()*255}, ${Math.random()*255}, 0.8)`;
    particle.style.borderRadius = '50%';
    particle.style.position = 'absolute';
    particle.style.animation = `float ${Math.random() * 20 + 10}s linear infinite`;
    particle.style.animationDelay = `${Math.random() * 5}s`;
    container.appendChild(particle);
  }
}

// 📦 Lancement
document.addEventListener('DOMContentLoaded', initApp);
