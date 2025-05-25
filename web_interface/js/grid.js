/**
 * Grid Rendering Module
 * Handles the rendering of Sudoku grids
 */

const GridRenderer = {
  /**
   * Renders a Sudoku grid
   * @param {HTMLElement} container - The container element
   * @param {Array} grid - 2D array representing the Sudoku grid
   * @param {Boolean} isInitial - Whether this is the initial grid
   * @param {Boolean} success - Whether the solution was successful
   */
  renderGrid(container, grid, isInitial = false, success = true) {
    // Clear the container
    container.innerHTML = '';
    
    // Create each cell
    for (let row = 0; row < 9; row++) {
      for (let col = 0; col < 9; col++) {
        const value = grid[row][col];
        const cell = document.createElement('div');
        cell.className = 'cell';
        
        // Add appropriate classes
        if (isInitial && value !== 0) {
          cell.classList.add('initial');
        } else if (!isInitial && value !== 0) {
          cell.classList.add('solution');
        }
        
        // If there's a conflict in the solution
        if (!success && !isInitial && value !== 0) {
          cell.classList.add('conflict');
        }
        
        // Set cell content
        cell.textContent = value !== 0 ? value : '';
        
        // Add to grid
        container.appendChild(cell);
      }
    }
    
    // Add animation to show grid
    container.style.animation = 'fadeIn 0.8s ease-out';
  },
  
  /**
   * Renders the initial grid
   * @param {Array} grid - 2D array representing the initial Sudoku grid
   */
  renderInitialGrid(grid) {
    const container = document.getElementById('initial-grid');
    this.renderGrid(container, grid, true, true);
  },
  
  /**
   * Creates a result grid for an algorithm
   * @param {Object} result - Algorithm result object
   * @param {Boolean} isActive - Whether this should be the active result
   * @returns {HTMLElement} - The created result container
   */
  createResultGrid(result, isActive = false) {
    const { algorithme, grille_resolue, taux_succes, cases_fausses } = result;
    
    // Create container
    const resultContainer = document.createElement('div');
    resultContainer.className = `algorithm-result ${isActive ? 'active' : ''}`;
    resultContainer.dataset.algorithm = algorithme;
    
    // Create grid
    const gridContainer = document.createElement('div');
    gridContainer.className = 'sudoku-grid';
    this.renderGrid(gridContainer, grille_resolue, false, taux_succes);
    
    // Add performance metrics
    const metricsContainer = document.createElement('div');
    metricsContainer.className = 'performance-metrics';
    
    // Add standard metrics
    this.addMetric(metricsContainer, result.temps.toFixed(3), 'Time (seconds)');
    this.addMetric(metricsContainer, result.iterations || 0, 'Iterations');
    
    // Add category-specific metrics
    if (result.categorie === 'recherche_aveugle') {
      this.addMetric(metricsContainer, result.nb_backtracks || 0, 'Backtracks');
      this.addMetric(metricsContainer, result.profondeur_max || 0, 'Max Depth');
    } else if (result.categorie === 'recherche_informee') {
      this.addMetric(metricsContainer, result.conflits_heuristique || 0, 'Conflicts');
      this.addMetric(metricsContainer, result.etats_explores || 0, 'States Explored');
    } else if (result.categorie === 'recherche_locale') {
      this.addMetric(metricsContainer, result.conflits_finaux || 0, 'Final Conflicts');
      this.addMetric(metricsContainer, result.nb_restarts || 0, 'Restarts');
    } else if (result.categorie === 'recherche_csp') {
      this.addMetric(metricsContainer, result.nb_assignations || 0, 'Assignments');
      this.addMetric(metricsContainer, result.taille_max_domaine || 0, 'Max Domain Size');
    }
    
    // Add status banner
    const statusBanner = document.createElement('div');
    statusBanner.className = `status-badge ${taux_succes ? 'success' : 'error'}`;
    statusBanner.textContent = taux_succes ? 'Success' : `Failed (${cases_fausses} errors)`;
    
    // Assemble the result
    resultContainer.appendChild(gridContainer);
    resultContainer.appendChild(metricsContainer);
    resultContainer.appendChild(statusBanner);
    
    return resultContainer;
  },
  
  /**
   * Adds a metric card to the container
   * @param {HTMLElement} container - The metrics container
   * @param {any} value - The metric value
   * @param {String} label - The metric label
   */
  addMetric(container, value, label) {
    const metricCard = document.createElement('div');
    metricCard.className = 'metric-card';
    
    const metricValue = document.createElement('div');
    metricValue.className = 'metric-value';
    metricValue.textContent = value;
    
    const metricLabel = document.createElement('div');
    metricLabel.className = 'metric-label';
    metricLabel.textContent = label;
    
    metricCard.appendChild(metricValue);
    metricCard.appendChild(metricLabel);
    container.appendChild(metricCard);
  },
  
  /**
   * Creates algorithm tabs
   * @param {Array} results - Array of algorithm results
   */
  createAlgorithmTabs(results) {
    const tabsContainer = document.getElementById('algorithm-tabs');
    const resultsContainer = document.getElementById('results-container');
    
    // Clear containers
    tabsContainer.innerHTML = '';
    resultsContainer.innerHTML = '';
    
    // Create a tab and result grid for each algorithm
    results.forEach((result, index) => {
      // Create tab
      const tab = document.createElement('button');
      tab.className = `tab ${index === 0 ? 'active' : ''} ${result.taux_succes ? 'success' : 'failure'}`;
      tab.dataset.algorithm = result.algorithme;
      
      const statusIcon = document.createElement('span');
      statusIcon.className = 'status-icon';
      statusIcon.textContent = result.taux_succes ? '✓' : '✗';
      
      const tabText = document.createTextNode(result.algorithme);
      
      tab.appendChild(statusIcon);
      tab.appendChild(tabText);
      tabsContainer.appendChild(tab);
      
      // Create result grid
      const resultGrid = this.createResultGrid(result, index === 0);
      resultsContainer.appendChild(resultGrid);
      
      // Add click event
      tab.addEventListener('click', () => {
        // Update active tab
        document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        
        // Update active result
        document.querySelectorAll('.algorithm-result').forEach(r => r.classList.remove('active'));
        resultGrid.classList.add('active');
      });
    });
  }
};