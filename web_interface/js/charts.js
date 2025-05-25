/**
 * Charts Module
 * Handles the creation and management of performance charts
 */

const ChartRenderer = {
  // Store chart instances for updating
  charts: {
    time: null,
    conflicts: null,
    successRate: null,
    memory: null
  },
  
  // Color schemes for the charts
  colors: {
    time: {
      backgroundColor: 'rgba(108, 92, 231, 0.2)',
      borderColor: 'rgba(108, 92, 231, 1)'
    },
    conflicts: {
      backgroundColor: 'rgba(214, 48, 49, 0.2)',
      borderColor: 'rgba(214, 48, 49, 1)'
    },
    successRate: {
      backgroundColor: 'rgba(0, 184, 148, 0.2)',
      borderColor: 'rgba(0, 184, 148, 1)'
    },
    memory: {
      backgroundColor: 'rgba(253, 121, 168, 0.2)',
      borderColor: 'rgba(253, 121, 168, 1)'
    }
  },
  
  // Chart configuration
  chartConfig: {
  responsive: true,
  maintainAspectRatio: false,
  layout: {
    padding: {
      top: 20,
      bottom: 20,
      left: 10,
      right: 10
    }
  },
  plugins: {
    legend: {
      display: true,
      position: 'top',
      labels: {
        color: '#f5f6fa',
        font: {
          family: 'Poppins',
          size: 12
        }
      }
    },
    tooltip: {
      mode: 'index',
      intersect: false,
      backgroundColor: 'rgba(45, 52, 54, 0.9)',
      titleFont: {
        family: 'Poppins',
        size: 14
      },
      bodyFont: {
        family: 'Poppins',
        size: 13
      }
    },
    title: {
      display: false
    }
  },
  scales: {
    x: {
      ticks: {
        color: '#a29bfe',
        font: {
          family: 'Poppins',
          size: 10
        }
      },
      grid: {
        color: 'rgba(255, 255, 255, 0.05)'
      }
    },
    y: {
      beginAtZero: true,
      ticks: {
        color: '#a29bfe',
        font: {
          family: 'Poppins',
          size: 10
        }
      },
      grid: {
        color: 'rgba(255, 255, 255, 0.05)'
      }
    }
  },
  animation: {
    duration: 1000,
    easing: 'easeOutQuart'
  }
},
  
  /**
   * Create and render all charts
   * @param {Array} results - Array of algorithm results
   */
  renderCharts(results) {
    this.renderTimeChart(results);
    this.renderConflictsChart(results);
    this.renderSuccessRateChart(results);
    this.renderMemoryChart(results);
  },
  
  /**
   * Render the time performance chart
   * @param {Array} results - Array of algorithm results
   */
  renderTimeChart(results) {
    const ctx = document.getElementById('timeChart').getContext('2d');
    const data = {
      labels: results.map(r => r.algorithme),
      datasets: [{
        label: 'Time (seconds)',
        data: results.map(r => r.temps),
        backgroundColor: this.colors.time.backgroundColor,
        borderColor: this.colors.time.borderColor,
        borderWidth: 2,
        tension: 0.3,
        fill: true
      }]
    };
    
    // Destroy existing chart if it exists
    if (this.charts.time) {
      this.charts.time.destroy();
    }
    
    // Create new chart
    this.charts.time = new Chart(ctx, {
      type: 'bar',
      data: data,
      options: { 
        ...this.chartConfig,
        plugins: {
          ...this.chartConfig.plugins,
          title: {
            display: true,
            text: 'Execution Time Comparison',
            color: '#f5f6fa',
            font: {
              family: 'Poppins',
              size: 16,
              weight: 'bold'
            }
          }
        }
      }
    });
  },
  
  /**
   * Render the conflicts chart
   * @param {Array} results - Array of algorithm results
   */
  renderConflictsChart(results) {
    const ctx = document.getElementById('conflictsChart').getContext('2d');
    
    // Get conflicts from different algorithm types
    const data = {
      labels: results.map(r => r.algorithme),
      datasets: [{
        label: 'Conflicts',
        data: results.map(r => {
          if (r.categorie === 'recherche_informee') {
            return r.conflits_heuristique || 0;
          } else if (r.categorie === 'recherche_locale') {
            return r.conflits_finaux || 0;
          } else {
            return 0;
          }
        }),
        backgroundColor: this.colors.conflicts.backgroundColor,
        borderColor: this.colors.conflicts.borderColor,
        borderWidth: 2,
        tension: 0.3,
        fill: true
      }]
    };
    
    // Destroy existing chart if it exists
    if (this.charts.conflicts) {
      this.charts.conflicts.destroy();
    }
    
    // Create new chart
    this.charts.conflicts = new Chart(ctx, {
      type: 'line',
      data: data,
      options: { 
        ...this.chartConfig,
        plugins: {
          ...this.chartConfig.plugins,
          title: {
            display: true,
            text: 'Conflicts by Algorithm',
            color: '#f5f6fa',
            font: {
              family: 'Poppins',
              size: 16,
              weight: 'bold'
            }
          }
        }
      }
    });
  },
  
  /**
   * Render the success rate chart
   * @param {Array} results - Array of algorithm results
   */
  renderSuccessRateChart(results) {
    const ctx = document.getElementById('successRateChart').getContext('2d');
    
    // Group by category
    const categories = {};
    results.forEach(r => {
      if (!categories[r.categorie]) {
        categories[r.categorie] = { total: 0, success: 0 };
      }
      categories[r.categorie].total++;
      if (r.taux_succes) {
        categories[r.categorie].success++;
      }
    });
    
    // Calculate success rate
    const categoryLabels = {
      'recherche_aveugle': 'Blind Search',
      'recherche_informee': 'Informed Search',
      'recherche_locale': 'Local Search',
      'recherche_csp': 'Constraint Satisfaction'
    };
    
    const data = {
      labels: Object.keys(categories).map(c => categoryLabels[c]),
      datasets: [{
        label: 'Success Rate (%)',
        data: Object.values(categories).map(c => Math.round((c.success / c.total) * 100)),
        backgroundColor: this.colors.successRate.backgroundColor,
        borderColor: this.colors.successRate.borderColor,
        borderWidth: 2
      }]
    };
    
    // Destroy existing chart if it exists
    if (this.charts.successRate) {
      this.charts.successRate.destroy();
    }
    
    // Create new chart
    this.charts.successRate = new Chart(ctx, {
      type: 'bar',
      data: data,
      options: { 
        ...this.chartConfig,
        plugins: {
          ...this.chartConfig.plugins,
          title: {
            display: true,
            text: 'Success Rate by Category',
            color: '#f5f6fa',
            font: {
              family: 'Poppins',
              size: 16,
              weight: 'bold'
            }
          }
        },
        scales: {
          ...this.chartConfig.scales,
          y: {
            ...this.chartConfig.scales.y,
            max: 100,
            ticks: {
              color: '#a29bfe',
              callback: function(value) {
                return value + '%';
              }
            }
          }
        }
      }
    });
  },
  
  /**
   * Render the memory usage chart
   * @param {Array} results - Array of algorithm results
   */
  renderMemoryChart(results) {
    const ctx = document.getElementById('memoryChart').getContext('2d');
    
    // Get memory usage from different metrics
    const data = {
      labels: results.map(r => r.algorithme),
      datasets: [{
        label: 'Memory Usage',
        data: results.map(r => {
          return r.memoire_max_file || r.memoire_max_beam || r.taille_max_domaine || 0;
        }),
        backgroundColor: this.colors.memory.backgroundColor,
        borderColor: this.colors.memory.borderColor,
        borderWidth: 2,
        tension: 0.3,
        fill: true
      }]
    };
    
    // Destroy existing chart if it exists
    if (this.charts.memory) {
      this.charts.memory.destroy();
    }
    
    // Create new chart
    this.charts.memory = new Chart(ctx, {
      type: 'line',
      data: data,
      options: { 
        ...this.chartConfig,
        plugins: {
          ...this.chartConfig.plugins,
          title: {
            display: true,
            text: 'Memory Usage Comparison',
            color: '#f5f6fa',
            font: {
              family: 'Poppins',
              size: 16,
              weight: 'bold'
            }
          }
        }
      }
    });
  }
};