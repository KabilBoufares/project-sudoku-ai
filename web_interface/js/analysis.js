/**
 * Analysis Module
 * Handles the generation of automated analysis
 */

const AnalysisGenerator = {
  /**
   * Generate and display analysis from results
   * @param {Array} results - Array of algorithm results
   */
  generateAnalysis(results) {
    const container = document.getElementById('analysis-container');
    container.innerHTML = '';
    
    // Add cards for different analyses
    this.addBestPerformerAnalysis(container, results);
    this.addCategoryComparisonAnalysis(container, results);
    this.addSuccessRateAnalysis(container, results);
    this.addIterationAnalysis(container, results);
  },
  
  /**
   * Create an analysis card
   * @param {String} title - Title for the analysis
   * @param {String} content - HTML content for the analysis
   * @param {String} icon - Emoji icon for the analysis
   * @param {String} type - Type of analysis (success, warning, error, or none)
   * @returns {HTMLElement} - The created analysis card
   */
  createAnalysisCard(title, content, icon, type = '') {
    const card = document.createElement('div');
    card.className = `analysis-card ${type}`;
    
    const titleElement = document.createElement('div');
    titleElement.className = 'analysis-title';
    
    const iconElement = document.createElement('span');
    iconElement.className = 'analysis-icon';
    iconElement.textContent = icon;
    
    titleElement.appendChild(iconElement);
    titleElement.appendChild(document.createTextNode(title));
    
    const contentElement = document.createElement('div');
    contentElement.className = 'analysis-content';
    contentElement.innerHTML = content;
    
    card.appendChild(titleElement);
    card.appendChild(contentElement);
    
    return card;
  },
  
  /**
   * Add best performer analysis
   * @param {HTMLElement} container - The analysis container
   * @param {Array} results - Array of algorithm results
   */
  addBestPerformerAnalysis(container, results) {
    // Find the fastest successful algorithm
    const successfulResults = results.filter(r => r.taux_succes);
    
    if (successfulResults.length === 0) {
      container.appendChild(
        this.createAnalysisCard(
          'No Successful Solutions',
          'None of the algorithms successfully solved this puzzle. This indicates the puzzle may be extremely difficult or unsolvable.',
          '⚠️',
          'error'
        )
      );
      return;
    }
    
    const fastestAlgorithm = successfulResults.reduce((fastest, current) => {
      return current.temps < fastest.temps ? current : fastest;
    }, successfulResults[0]);
    
    // Find the second fastest for comparison
    successfulResults.sort((a, b) => a.temps - b.temps);
    const secondFastest = successfulResults.length > 1 ? successfulResults[1] : null;
    
    let content = `
      <p>The <span class="highlight">${fastestAlgorithm.algorithme}</span> algorithm provided the fastest solution at 
      <span class="highlight">${fastestAlgorithm.temps.toFixed(3)}</span> seconds.</p>
    `;
    
    if (secondFastest) {
      const speedDifference = ((secondFastest.temps - fastestAlgorithm.temps) / secondFastest.temps * 100).toFixed(1);
      content += `
        <p>This is <span class="highlight">${speedDifference}%</span> faster than the second-fastest algorithm 
        (${secondFastest.algorithme} at ${secondFastest.temps.toFixed(3)} seconds).</p>
      `;
    }
    
    // Add category context
    const categoryName = this.getCategoryName(fastestAlgorithm.categorie);
    content += `
      <p>This algorithm belongs to the <span class="highlight">${categoryName}</span> category, which is 
      characterized by ${this.getCategoryDescription(fastestAlgorithm.categorie)}</p>
    `;
    
    container.appendChild(
      this.createAnalysisCard(
        'Best Performing Algorithm',
        content,
        '🏆',
        'success'
      )
    );
  },
  
  /**
   * Add category comparison analysis
   * @param {HTMLElement} container - The analysis container
   * @param {Array} results - Array of algorithm results
   */
  addCategoryComparisonAnalysis(container, results) {
    // Group results by category
    const categories = {};
    results.forEach(r => {
      if (!categories[r.categorie]) {
        categories[r.categorie] = [];
      }
      categories[r.categorie].push(r);
    });
    
    // Calculate average time by category
    const categoryAverages = {};
    for (const category in categories) {
      const successfulAlgos = categories[category].filter(r => r.taux_succes);
      if (successfulAlgos.length > 0) {
        categoryAverages[category] = successfulAlgos.reduce((sum, r) => sum + r.temps, 0) / successfulAlgos.length;
      }
    }
    
    // Find the most efficient category
    let bestCategory = null;
    let bestAverage = Infinity;
    
    for (const category in categoryAverages) {
      if (categoryAverages[category] < bestAverage) {
        bestAverage = categoryAverages[category];
        bestCategory = category;
      }
    }
    
    if (!bestCategory) {
      container.appendChild(
        this.createAnalysisCard(
          'Category Comparison',
          'No category had successful algorithms for meaningful comparison.',
          '📊',
          'warning'
        )
      );
      return;
    }
    
    // Generate content
    let content = `
      <p>The <span class="highlight">${this.getCategoryName(bestCategory)}</span> category performed best overall
      with an average time of <span class="highlight">${bestAverage.toFixed(3)}</span> seconds.</p>
      <p>Performance by category:</p>
      <ul>
    `;
    
    for (const category in categoryAverages) {
      const avgTime = categoryAverages[category].toFixed(3);
      const successRate = (categories[category].filter(r => r.taux_succes).length / categories[category].length * 100).toFixed(0);
      content += `
        <li>${this.getCategoryName(category)}: ${avgTime}s (${successRate}% success rate)</li>
      `;
    }
    
    content += '</ul>';
    
    container.appendChild(
      this.createAnalysisCard(
        'Category Performance Analysis',
        content,
        '📊',
        ''
      )
    );
  },
  
  /**
   * Add success rate analysis
   * @param {HTMLElement} container - The analysis container
   * @param {Array} results - Array of algorithm results
   */
  addSuccessRateAnalysis(container, results) {
    const totalAlgorithms = results.length;
    const successfulAlgorithms = results.filter(r => r.taux_succes).length;
    const successRate = (successfulAlgorithms / totalAlgorithms * 100).toFixed(0);
    
    let title, content, icon, type;
    
    if (successRate >= 75) {
      title = 'High Success Rate';
      icon = '✅';
      type = 'success';
      content = `
        <p><span class="highlight">${successRate}%</span> of algorithms successfully solved this puzzle (${successfulAlgorithms} out of ${totalAlgorithms}), 
        indicating this is a well-structured puzzle with multiple viable solution approaches.</p>
      `;
    } else if (successRate >= 50) {
      title = 'Moderate Success Rate';
      icon = '🔍';
      type = '';
      content = `
        <p><span class="highlight">${successRate}%</span> of algorithms successfully solved this puzzle (${successfulAlgorithms} out of ${totalAlgorithms}). 
        This suggests a moderately challenging puzzle that requires appropriate algorithm selection.</p>
      `;
    } else if (successRate > 0) {
      title = 'Low Success Rate';
      icon = '⚠️';
      type = 'warning';
      content = `
        <p>Only <span class="highlight">${successRate}%</span> of algorithms successfully solved this puzzle (${successfulAlgorithms} out of ${totalAlgorithms}). 
        This is a difficult puzzle that requires specialized solution approaches.</p>
      `;
    } else {
      title = 'No Successful Solutions';
      icon = '❌';
      type = 'error';
      content = `
        <p>None of the algorithms successfully solved this puzzle. This indicates the puzzle may be extremely difficult, 
        contain contradictions, or be unsolvable with the current algorithm implementations.</p>
      `;
    }
    
    container.appendChild(
      this.createAnalysisCard(title, content, icon, type)
    );
  },
  
  /**
   * Add iteration analysis
   * @param {HTMLElement} container - The analysis container
   * @param {Array} results - Array of algorithm results
   */
  addIterationAnalysis(container, results) {
    // Filter results with iteration data
    const resultsWithIterations = results.filter(r => r.iterations && r.taux_succes);
    
    if (resultsWithIterations.length < 2) {
      return; // Not enough data for comparison
    }
    
    // Sort by iterations
    resultsWithIterations.sort((a, b) => a.iterations - b.iterations);
    
    const mostEfficient = resultsWithIterations[0];
    const leastEfficient = resultsWithIterations[resultsWithIterations.length - 1];
    
    const content = `
      <p>The <span class="highlight">${mostEfficient.algorithme}</span> algorithm was the most efficient, 
      requiring only <span class="highlight">${mostEfficient.iterations}</span> iterations to find a solution.</p>
      
      <p>In contrast, <span class="highlight">${leastEfficient.algorithme}</span> required 
      <span class="highlight">${leastEfficient.iterations}</span> iterations, making it 
      ${Math.round(leastEfficient.iterations / mostEfficient.iterations)}x less efficient in terms of computation.</p>
      
      <p>This suggests that ${this.getCategoryName(mostEfficient.categorie)} approaches may be more 
      computation-efficient for this type of puzzle.</p>
    `;
    
    container.appendChild(
      this.createAnalysisCard(
        'Computational Efficiency',
        content,
        '⚙️',
        ''
      )
    );
  },
  
  /**
   * Get a human-readable category name
   * @param {String} category - Category identifier
   * @returns {String} - Human-readable category name
   */
  getCategoryName(category) {
    const names = {
      'recherche_aveugle': 'Blind Search',
      'recherche_informee': 'Informed Search',
      'recherche_locale': 'Local Search',
      'recherche_csp': 'Constraint Satisfaction'
    };
    
    return names[category] || category;
  },
  
  /**
   * Get a description for a category
   * @param {String} category - Category identifier
   * @returns {String} - Category description
   */
  getCategoryDescription(category) {
    const descriptions = {
      'recherche_aveugle': 'methodical exploration without heuristic guidance.',
      'recherche_informee': 'using domain-specific knowledge to guide the search.',
      'recherche_locale': 'iterative improvement from an initial state.',
      'recherche_csp': 'using constraint propagation and backtracking.'
    };
    
    return descriptions[category] || '';
  }
};