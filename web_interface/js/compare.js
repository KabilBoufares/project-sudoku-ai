/**
 * Comparison Module
 * Handles the generation of comparison tables
 */

const ComparisonGenerator = {
  /**
   * Generate the comparison table
   * @param {Array} results - Array of algorithm results
   */
  generateComparisonTable(results) {
    const tableBody = document.getElementById('comparison-body');
    tableBody.innerHTML = '';
    
    // Sort results by category, then by success (successful first), then by time
    results.sort((a, b) => {
      // First by category
      if (a.categorie !== b.categorie) {
        return a.categorie.localeCompare(b.categorie);
      }
      
      // Then by success (successful first)
      if (a.taux_succes !== b.taux_succes) {
        return b.taux_succes - a.taux_succes;
      }
      
      // Then by time (faster first)
      return a.temps - b.temps;
    });
    
    // Add rows for each algorithm
    results.forEach(result => {
      const row = document.createElement('tr');
      row.className = result.taux_succes ? 'success' : 'failure';
      
      // Algorithm name
      const nameCell = document.createElement('td');
      nameCell.textContent = result.algorithme;
      row.appendChild(nameCell);
      
      // Category
      const categoryCell = document.createElement('td');
      categoryCell.textContent = this.getCategoryName(result.categorie);
      row.appendChild(categoryCell);
      
      // Success
      const successCell = document.createElement('td');
      const successBadge = document.createElement('span');
      successBadge.className = `status-badge ${result.taux_succes ? 'success' : 'error'}`;
      successBadge.textContent = result.taux_succes ? 'Success' : 'Failed';
      successCell.appendChild(successBadge);
      row.appendChild(successCell);
      
      // Time
      const timeCell = document.createElement('td');
      timeCell.textContent = result.temps.toFixed(3) + 's';
      row.appendChild(timeCell);
      
      // Iterations
      const iterationsCell = document.createElement('td');
      iterationsCell.textContent = result.iterations || '-';
      row.appendChild(iterationsCell);
      
      // Max Depth
      const depthCell = document.createElement('td');
      depthCell.textContent = result.profondeur_max || '-';
      row.appendChild(depthCell);
      
      // Memory
      const memoryCell = document.createElement('td');
      memoryCell.textContent = this.getMemoryMetric(result);
      row.appendChild(memoryCell);
      
      // Specific metrics
      const specificCell = document.createElement('td');
      specificCell.textContent = this.getSpecificMetrics(result);
      row.appendChild(specificCell);
      
      tableBody.appendChild(row);
    });
  },
  
  /**
   * Get the appropriate memory metric for an algorithm
   * @param {Object} result - Algorithm result
   * @returns {String} - Formatted memory metric
   */
  getMemoryMetric(result) {
    if (result.memoire_max_file) {
      return `${result.memoire_max_file} states`;
    } else if (result.memoire_max_beam) {
      return `${result.memoire_max_beam} states`;
    } else if (result.taille_max_domaine) {
      return `${result.taille_max_domaine} vals`;
    } else {
      return '-';
    }
  },
  
  /**
   * Get specific metrics based on algorithm category
   * @param {Object} result - Algorithm result
   * @returns {String} - Formatted specific metrics
   */
  getSpecificMetrics(result) {
    switch (result.categorie) {
      case 'recherche_aveugle':
        return result.nb_backtracks ? `${result.nb_backtracks} backtracks` : '-';
        
      case 'recherche_informee':
        const metrics = [];
        if (result.conflits_heuristique !== undefined) {
          metrics.push(`${result.conflits_heuristique} conflicts`);
        }
        if (result.etats_explores !== undefined) {
          metrics.push(`${result.etats_explores} states explored`);
        }
        return metrics.length > 0 ? metrics.join(', ') : '-';
        
      case 'recherche_locale':
        const localMetrics = [];
        if (result.conflits_finaux !== undefined) {
          localMetrics.push(`${result.conflits_finaux} final conflicts`);
        }
        if (result.nb_restarts !== undefined) {
          localMetrics.push(`${result.nb_restarts} restarts`);
        }
        return localMetrics.length > 0 ? localMetrics.join(', ') : '-';
        
      case 'recherche_csp':
        const cspMetrics = [];
        if (result.nb_assignations !== undefined) {
          cspMetrics.push(`${result.nb_assignations} assignments`);
        }
        if (result.nb_backtracks !== undefined) {
          cspMetrics.push(`${result.nb_backtracks} backtracks`);
        }
        return cspMetrics.length > 0 ? cspMetrics.join(', ') : '-';
        
      default:
        return '-';
    }
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
  }
};