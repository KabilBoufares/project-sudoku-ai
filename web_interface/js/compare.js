const ComparisonGenerator = {
  generateComparisonTable(results) {
    const tableBody = document.getElementById('comparison-body');
    tableBody.innerHTML = '';

    const grouped = {
      'recherche_aveugle': [],
      'recherche_informee': [],
      'recherche_locale': [],
      'recherche_csp': []
    };

    results.forEach(res => {
      if (grouped[res.categorie]) {
        grouped[res.categorie].push(res);
      }
    });

    Object.entries(grouped).forEach(([cat, algos]) => {
      if (algos.length === 0) return;

      const block = document.createElement('div');
      block.className = 'category-comparison';

      const title = document.createElement('h3');
      title.textContent = this.getCategoryName(cat);
      block.appendChild(title);

      const table = document.createElement('table');
      table.className = 'comparison-table';

      const thead = document.createElement('thead');
      const headerRow = document.createElement('tr');
      const headers = this.getColumns(cat);
      headers.forEach(h => {
        const th = document.createElement('th');
        th.textContent = h.label;
        headerRow.appendChild(th);
      });
      thead.appendChild(headerRow);
      table.appendChild(thead);

      const tbody = document.createElement('tbody');
      algos.sort((a, b) => b.taux_succes - a.taux_succes || a.temps - b.temps);
      algos.forEach(result => {
        const row = document.createElement('tr');
        row.className = result.taux_succes ? 'success' : 'failure';
        headers.forEach(h => {
          const td = document.createElement('td');
          td.textContent = h.value(result);
          row.appendChild(td);
        });
        tbody.appendChild(row);
      });

      table.appendChild(tbody);
      block.appendChild(table);
      tableBody.appendChild(block);
    });
  },

  getColumns(category) {
    const common = [
      { label: 'Algorithme', value: r => r.algorithme },
      {
        label: 'Succès',
        value: r => r.taux_succes ? '✅' : '❌'
      },
      {
        label: 'Temps (ms)',
        value: r => `${Math.round(r.temps * 1000)} ms`
      },
      {
        label: 'Itérations',
        value: r => r.iterations ?? '-'
      }
    ];

    const metrics = {
        'recherche_aveugle': [
          { label: 'Prof. Max', value: r => r.profondeur_max ?? '-' },
          {
            label: 'Mesures dédiées',
            value: r => {
              const parts = [];
              if (r.nb_backtracks !== undefined) parts.push(`backtracks: ${r.nb_backtracks}`);
              if (r.memoire_max_file !== undefined) parts.push(`mémoire: ${r.memoire_max_file}`);
              return parts.join(', ') || '-';
            }
          }
        ],

      'recherche_informee': [
        {
          label: 'Mesures dédiées',
          value: r => {
            const parts = [];
            if (r.conflits_heuristique !== undefined) parts.push(`conflits: ${r.conflits_heuristique}`);
            if (r.etats_explores !== undefined) parts.push(`explorés: ${r.etats_explores}`);
            return parts.join(', ') || '-';
          }
        }
      ],
      'recherche_locale': [
        {
          label: 'Mesures dédiées',
          value: r => {
            const parts = [];
            if (r.conflits_finaux !== undefined) parts.push(`conflits: ${r.conflits_finaux}`);
            if (r.nb_restarts !== undefined) parts.push(`restarts: ${r.nb_restarts}`);
            return parts.join(', ') || '-';
          }
        }
      ],
      'recherche_csp': [
        {
          label: 'Mesures dédiées',
          value: r => {
            const parts = [];
            if (r.nb_assignations !== undefined) parts.push(`assignations: ${r.nb_assignations}`);
            if (r.nb_backtracks !== undefined) parts.push(`backtracks: ${r.nb_backtracks}`);
            if (r.taille_max_domaine !== undefined) parts.push(`domaine: ${r.taille_max_domaine}`);
            return parts.join(', ') || '-';
          }
        }
      ]
    };

    return [...common, ...(metrics[category] || [])];
  },

  getCategoryName(category) {
    const names = {
      'recherche_aveugle': 'Recherche Aveugle',
      'recherche_informee': 'Recherche Informée',
      'recherche_locale': 'Recherche Locale / Métaheuristique',
      'recherche_csp': 'Recherche par Contraintes'
    };
    return names[category] || category;
  }
};
