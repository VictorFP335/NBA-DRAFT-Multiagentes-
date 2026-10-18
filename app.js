/**
 * NBA DRAFT WAR ROOM - WEB APPLICATION LOGIC
 * High-performance vanilla JS engine for filtering, modal dossiers, and comparison
 */

(function () {
  'use strict';

  // Application State
  const state = {
    prospects: [],
    filteredProspects: [],
    year: 'all',          // 'all', '2018', '2017'
    originType: 'all',    // 'all', 'International', 'NCAA', 'High School'
    position: 'all',      // 'all', 'PG', 'SG', 'SF', 'PF', 'C'
    tier: 'all',          // 'all', 'tier-1', 'tier-2', 'tier-3', 'tier-4'
    sortBy: 'gm_score_desc',
    search: '',
    selectedPlayer: null,
    duelPlayerA: null,
    duelPlayerB: null
  };

  // DOM Elements
  const elements = {
    prospectsGrid: document.getElementById('prospectsGrid'),
    resultsCount: document.getElementById('resultsCount'),
    searchInput: document.getElementById('searchInput'),
    clearSearchBtn: document.getElementById('clearSearchBtn'),
    positionSelect: document.getElementById('positionSelect'),
    tierSelect: document.getElementById('tierSelect'),
    sortSelect: document.getElementById('sortSelect'),
    yearTabs: document.querySelectorAll('.draft-year-tabs .tab-btn'),
    originTabs: document.querySelectorAll('.origin-tabs .origin-tab-btn'),
    
    // Modal
    dossierModal: document.getElementById('dossierModal'),
    modalCloseBtn: document.getElementById('modalCloseBtn'),
    modalPortrait: document.getElementById('modalPortrait'),
    modalPlayerTitle: document.getElementById('modalPlayerTitle'),
    modalBadges: document.getElementById('modalBadges'),
    modalOriginBanner: document.getElementById('modalOriginBanner'),
    modalBiometrics: document.getElementById('modalBiometrics'),
    modalTabBtns: document.querySelectorAll('.modal-tab-btn'),
    modalTabPanels: document.querySelectorAll('.modal-tab-panel'),
    warRoomPanel: document.getElementById('warRoomPanel'),
    statsPanel: document.getElementById('statsPanel'),
    realityPanel: document.getElementById('realityPanel'),
    modalCompareBtn: document.getElementById('modalCompareBtn'),
    modalSimulateLiveBtn: document.getElementById('modalSimulateLiveBtn'),
    liveSimulationContainer: document.getElementById('liveSimulationContainer'),
    liveSimStatusText: document.getElementById('liveSimStatusText'),
    simMessagesStream: document.getElementById('simMessagesStream'),

    // Comparison Modal
    compareModal: document.getElementById('compareModal'),
    compareCloseBtn: document.getElementById('compareCloseBtn'),
    compareLauncherBtn: document.getElementById('compareLauncherBtn'),
    heroCompareBtn: document.getElementById('heroCompareBtn'),
    presetMatchupBtns: document.querySelectorAll('.preset-btn'),
    selectPlayerA: document.getElementById('selectPlayerA'),
    selectPlayerB: document.getElementById('selectPlayerB'),
    compareDuelGrid: document.getElementById('compareDuelGrid'),
    compareBarsList: document.getElementById('compareBarsList')
  };

  // Preset Iconic Matchups
  const PRESET_MATCHUPS = {
    'luka-bagley': ['Luka Dončić', 'Marvin Bagley III'],
    'tatum-fultz': ['Jayson Tatum', 'Markelle Fultz'],
    'trae-sexton': ['Trae Young', 'Collin Sexton'],
    'mitchell-ntilikina': ['Donovan Mitchell', 'Frank Ntilikina'],
    'ayton-jjj': ['Deandre Ayton', 'Jaren Jackson Jr.']
  };

  // Initialize
  async function init() {
    loadData();
    setupEventListeners();
  }

  // Load Prospects Data
  function loadData() {
    if (window.PROSPECTS_DATA && Array.isArray(window.PROSPECTS_DATA)) {
      state.prospects = window.PROSPECTS_DATA;
      finishDataLoad();
    } else {
      fetch('data/enriched_prospects.json')
        .then(res => res.json())
        .then(data => {
          state.prospects = data;
          finishDataLoad();
        })
        .catch(err => {
          console.error('Failed to load prospects data:', err);
          elements.prospectsGrid.innerHTML = `
            <div style="grid-column: 1/-1; text-align: center; padding: 60px 20px; color: #ef4444;">
              <h3>Erro ao carregar dados dos prospectos</h3>
              <p>Verifique o arquivo data/enriched_prospects.json ou data/prospects_data.js</p>
            </div>`;
        });
    }
  }

  function finishDataLoad() {
    updateOriginCounters();
    populateCompareSelects();
    applyFilters();
  }

  // Update Counters in Filter Tabs
  function updateOriginCounters() {
    const counts = {
      all: state.prospects.length,
      International: 0,
      NCAA: 0,
      'High School': 0
    };

    state.prospects.forEach(p => {
      const type = p.origin_type || 'NCAA';
      if (counts[type] !== undefined) {
        counts[type]++;
      }
    });

    document.querySelectorAll('[data-origin-type]').forEach(btn => {
      const type = btn.getAttribute('data-origin-type');
      const counter = btn.querySelector('.tab-counter');
      if (counter && counts[type] !== undefined) {
        counter.textContent = counts[type];
      }
    });
  }

  // Setup Event Listeners
  function setupEventListeners() {
    // Search input
    elements.searchInput.addEventListener('input', e => {
      state.search = e.target.value.trim().toLowerCase();
      elements.clearSearchBtn.classList.toggle('visible', state.search.length > 0);
      applyFilters();
    });

    elements.clearSearchBtn.addEventListener('click', () => {
      elements.searchInput.value = '';
      state.search = '';
      elements.clearSearchBtn.classList.remove('visible');
      applyFilters();
    });

    // Year Tabs
    elements.yearTabs.forEach(btn => {
      btn.addEventListener('click', () => {
        elements.yearTabs.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        state.year = btn.getAttribute('data-year');
        applyFilters();
      });
    });

    // Origin Category Tabs
    elements.originTabs.forEach(btn => {
      btn.addEventListener('click', () => {
        elements.originTabs.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        state.originType = btn.getAttribute('data-origin-type');
        applyFilters();
      });
    });

    // Dropdowns
    elements.positionSelect.addEventListener('change', e => {
      state.position = e.target.value;
      applyFilters();
    });

    elements.tierSelect.addEventListener('change', e => {
      state.tier = e.target.value;
      applyFilters();
    });

    elements.sortSelect.addEventListener('change', e => {
      state.sortBy = e.target.value;
      applyFilters();
    });

    // Modal Events
    elements.modalCloseBtn.addEventListener('click', closeModal);
    elements.dossierModal.addEventListener('click', e => {
      if (e.target === elements.dossierModal) closeModal();
    });

    document.addEventListener('keydown', e => {
      if (e.key === 'Escape') {
        closeModal();
        closeCompareModal();
      }
    });

    // Modal Tabs
    elements.modalTabBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        elements.modalTabBtns.forEach(b => b.classList.remove('active'));
        elements.modalTabPanels.forEach(p => p.classList.remove('active'));
        btn.classList.add('active');
        const tabKey = btn.getAttribute('data-tab');
        document.getElementById(`${tabKey}Panel`).classList.add('active');
      });
    });

    // Live Simulation Button in Modal
    if (elements.modalSimulateLiveBtn) {
      elements.modalSimulateLiveBtn.addEventListener('click', () => {
        if (state.selectedPlayer) {
          runLiveWarRoomSimulation(state.selectedPlayer);
        }
      });
    }

    // Modal Compare Launcher
    elements.modalCompareBtn.addEventListener('click', () => {
      if (state.selectedPlayer) {
        // Compare with default rival (e.g. if Luka, compare with Bagley)
        let rival = 'Marvin Bagley III';
        if (state.selectedPlayer.player === 'Marvin Bagley III' || state.selectedPlayer.player === 'Deandre Ayton') {
          rival = 'Luka Dončić';
        } else if (state.selectedPlayer.player === 'Jayson Tatum') {
          rival = 'Markelle Fultz';
        } else if (state.selectedPlayer.player === 'Markelle Fultz') {
          rival = 'Jayson Tatum';
        }
        closeModal();
        openCompareModal(state.selectedPlayer.player, rival);
      }
    });

    // Comparison Modal Events
    if (elements.compareLauncherBtn) {
      elements.compareLauncherBtn.addEventListener('click', () => {
        openCompareModal('Luka Dončić', 'Marvin Bagley III');
      });
    }

    if (elements.heroCompareBtn) {
      elements.heroCompareBtn.addEventListener('click', () => {
        openCompareModal('Luka Dončić', 'Marvin Bagley III');
      });
    }

    elements.compareCloseBtn.addEventListener('click', closeCompareModal);
    elements.compareModal.addEventListener('click', e => {
      if (e.target === elements.compareModal) closeCompareModal();
    });

    // Preset matchup buttons
    elements.presetMatchupBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        elements.presetMatchupBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const matchKey = btn.getAttribute('data-matchup');
        const pair = PRESET_MATCHUPS[matchKey];
        if (pair) {
          elements.selectPlayerA.value = pair[0];
          elements.selectPlayerB.value = pair[1];
          renderComparison(pair[0], pair[1]);
        }
      });
    });

    elements.selectPlayerA.addEventListener('change', e => {
      renderComparison(e.target.value, elements.selectPlayerB.value);
    });

    elements.selectPlayerB.addEventListener('change', e => {
      renderComparison(elements.selectPlayerA.value, e.target.value);
    });
  }

  // Filter & Sort Logic
  function applyFilters() {
    let list = [...state.prospects];

    // Year Filter
    if (state.year !== 'all') {
      const yr = parseInt(state.year);
      list = list.filter(p => p.class_year === yr);
    }

    // Origin Type Filter
    if (state.originType !== 'all') {
      list = list.filter(p => p.origin_type === state.originType);
    }

    // Position Filter
    if (state.position !== 'all') {
      list = list.filter(p => p.position && p.position.includes(state.position));
    }

    // Tier Filter
    if (state.tier !== 'all') {
      list = list.filter(p => {
        const tierStr = (p.war_room && p.war_room.gm_tier) ? p.war_room.gm_tier.toLowerCase() : '';
        if (state.tier === 'tier-1') return tierStr.includes('tier 1') || (p.war_room && p.war_room.gm_score >= 9.0);
        if (state.tier === 'tier-2') return tierStr.includes('tier 2') || (p.war_room && p.war_room.gm_score >= 8.0 && p.war_room.gm_score < 9.0);
        if (state.tier === 'tier-3') return tierStr.includes('tier 3') || (p.war_room && p.war_room.gm_score >= 6.8 && p.war_room.gm_score < 8.0);
        if (state.tier === 'tier-4') return tierStr.includes('tier 4') || (p.war_room && p.war_room.gm_score < 6.8);
        return true;
      });
    }

    // Search Query
    if (state.search) {
      list = list.filter(p => {
        const pName = (p.player || '').toLowerCase();
        const pOrigin = (p.origin || '').toLowerCase();
        const pClub = (p.origin_club_full || '').toLowerCase();
        const pCountry = (p.origin_country || '').toLowerCase();
        const pTeam = (p.target_team_and_pick || '').toLowerCase();
        return pName.includes(state.search) ||
               pOrigin.includes(state.search) ||
               pClub.includes(state.search) ||
               pCountry.includes(state.search) ||
               pTeam.includes(state.search);
      });
    }

    // Sort
    list.sort((a, b) => {
      const scoreA = (a.war_room && a.war_room.gm_score) ? a.war_room.gm_score : 0;
      const scoreB = (b.war_room && b.war_room.gm_score) ? b.war_room.gm_score : 0;
      const pickA = a.pick || 999;
      const pickB = b.pick || 999;
      const ptsA = (a.stats && a.stats.PTS) ? a.stats.PTS : 0;
      const ptsB = (b.stats && b.stats.PTS) ? b.stats.PTS : 0;
      const tsA = (a.stats && a.stats['TS%']) ? a.stats['TS%'] : 0;
      const tsB = (b.stats && b.stats['TS%']) ? b.stats['TS%'] : 0;
      const bpmA = (a.stats && a.stats.BPM_est) ? a.stats.BPM_est : 0;
      const bpmB = (b.stats && b.stats.BPM_est) ? b.stats.BPM_est : 0;

      switch (state.sortBy) {
        case 'gm_score_desc':
          return scoreB - scoreA;
        case 'pick_asc':
          return pickA - pickB;
        case 'pts_desc':
          return ptsB - ptsA;
        case 'ts_desc':
          return tsB - tsA;
        case 'bpm_desc':
          return bpmB - bpmA;
        case 'name_asc':
          return a.player.localeCompare(b.player);
        default:
          return scoreB - scoreA;
      }
    });

    state.filteredProspects = list;
    renderGrid();
  }

  // Render Cards Grid
  function renderGrid() {
    elements.resultsCount.innerHTML = `Exibindo <strong>${state.filteredProspects.length}</strong> de <strong>${state.prospects.length}</strong> atletas pré-draft`;

    if (state.filteredProspects.length === 0) {
      elements.prospectsGrid.innerHTML = `
        <div style="grid-column: 1/-1; text-align: center; padding: 80px 20px;">
          <div style="font-size: 3rem; margin-bottom: 14px;">🔍</div>
          <h3 style="font-size: 1.3rem; margin-bottom: 8px;">Nenhum prospecto encontrado</h3>
          <p style="color: var(--text-muted); font-size: 0.9rem;">Tente ajustar seus filtros ou termo de busca.</p>
        </div>`;
      return;
    }

    const cardsHtml = state.filteredProspects.map(p => createCardHtml(p)).join('');
    elements.prospectsGrid.innerHTML = cardsHtml;

    // Attach card click handlers
    elements.prospectsGrid.querySelectorAll('.prospect-card').forEach(card => {
      card.addEventListener('click', e => {
        const playerName = card.getAttribute('data-player');
        const prospect = state.prospects.find(x => x.player === playerName);
        if (prospect) {
          openModal(prospect);
        }
      });
    });
  }

  // Create Card HTML
  function createCardHtml(p) {
    const isInternational = p.origin_type === 'International';
    const gmScore = (p.war_room && p.war_room.gm_score) ? p.war_room.gm_score : 7.0;
    
    // Tier classification
    let tierClass = 'tier-3';
    let tierLabel = 'TIER 3: ROTATION';
    if (gmScore >= 9.0) {
      tierClass = 'tier-1';
      tierLabel = 'TIER 1: CORNERSTONE';
    } else if (gmScore >= 8.0) {
      tierClass = 'tier-2';
      tierLabel = 'TIER 2: ALL-STAR';
    } else if (gmScore < 6.8) {
      tierClass = 'tier-4';
      tierLabel = 'TIER 4: BUST RISK';
    }

    const quantScore = p.multiagent_debate?.quant?.score ?? p.war_room?.quant_score ?? '-';
    const tacticalScore = p.multiagent_debate?.tactical?.score ?? p.war_room?.tactical_score ?? '-';
    const fitScore = p.multiagent_debate?.fit?.score ?? p.war_room?.fit_score ?? '-';

    const flag = p.country_flag || '🇺🇸';
    const originBadgeHtml = p.team_badge ? `
      <div class="team-crest-badge" title="${escapeHtml(p.origin)}">
        <img src="${p.team_badge}" alt="${escapeHtml(p.origin)}" onerror="this.style.display='none'">
      </div>` : '';

    const realityVerdict = p.historical_reality?.historical_verdict || p.historical_reality?.career_arc || '';

    return `
      <div class="prospect-card ${isInternational ? 'international-card' : ''}" data-player="${escapeHtml(p.player)}">
        <div class="card-media">
          <img class="player-img" src="${p.local_image || 'assets/players/default_player.svg'}" 
               alt="${escapeHtml(p.player)}" 
               loading="lazy"
               onerror="this.src='assets/players/default_player.svg'">
          
          <div class="card-top-badges">
            <span class="pick-badge">${p.class_year} • Pick #${p.pick}</span>
            <span class="tier-badge ${tierClass}">${tierLabel}</span>
          </div>

          <div class="card-media-bottom-left">
            <span class="origin-tag-pill ${isInternational ? 'euro' : ''}">
              ${flag} ${escapeHtml(p.origin_league || p.origin_type)}
            </span>
          </div>

          ${originBadgeHtml}
        </div>

        <div class="card-content">
          <div class="player-header-meta">
            <h3 class="player-name">${escapeHtml(p.player)}</h3>
            <span class="player-pos-badge">${p.position || 'G/F'}</span>
          </div>

          <div class="player-origin-detail">
            <strong>${escapeHtml(p.origin)}</strong> • ${p.age_at_draft || '?'} anos
          </div>

          <div class="stats-strip">
            <div class="stat-item">
              <span class="stat-lbl">PTS</span>
              <span class="stat-val">${p.stats?.PTS ?? '-'}</span>
            </div>
            <div class="stat-item">
              <span class="stat-lbl">REB</span>
              <span class="stat-val">${p.stats?.REB ?? '-'}</span>
            </div>
            <div class="stat-item">
              <span class="stat-lbl">AST</span>
              <span class="stat-val">${p.stats?.AST ?? '-'}</span>
            </div>
            <div class="stat-item">
              <span class="stat-lbl">TS%</span>
              <span class="stat-val" style="color: ${p.stats?.['TS%'] >= 60 ? 'var(--accent-emerald)' : '#fff'};">${p.stats?.['TS%'] ? p.stats['TS%'] + '%' : '-'}</span>
            </div>
          </div>

          <div class="war-room-mini-scores">
            <div class="war-room-title-bar">
              <span>🏛️ War Room Deliberação</span>
              <span class="gm-final-score">GM: ${gmScore}</span>
            </div>
            <div class="agents-score-pills">
              <div class="agent-pill" title="Dr. Marcus Vance (Quant)">
                <span class="agent-code">QUANT</span>
                <span class="agent-num" style="color: var(--accent-blue);">${quantScore}</span>
              </div>
              <div class="agent-pill" title="Coach Frank Sullivan (Tático)">
                <span class="agent-code">TÁTICO</span>
                <span class="agent-num" style="color: var(--accent-emerald);">${tacticalScore}</span>
              </div>
              <div class="agent-pill" title="Elena Rostova (Fit/Modern NBA)">
                <span class="agent-code">FIT</span>
                <span class="agent-num" style="color: var(--accent-purple);">${fitScore}</span>
              </div>
            </div>
          </div>

          ${realityVerdict ? `
            <div class="reality-snapshot">
              <strong>Realidade NBA:</strong> ${escapeHtml(realityVerdict)}
            </div>` : ''}

          <button type="button" class="view-dossier-btn">
            <span>Ver Dossiê Pré-Draft & Parecer</span> →
          </button>
        </div>
      </div>`;
  }

  // Open Modal Dossier
  function openModal(prospect) {
    state.selectedPlayer = prospect;

    elements.modalPortrait.src = prospect.local_image || 'assets/players/default_player.svg';
    elements.modalPlayerTitle.textContent = prospect.player;

    const gmScore = prospect.war_room?.gm_score ?? 7.0;
    const isInternational = prospect.origin_type === 'International';
    const flag = prospect.country_flag || '🇺🇸';

    // Badges in Header
    elements.modalBadges.innerHTML = `
      <span class="pick-badge">${prospect.class_year} • Pick #${prospect.pick} (${escapeHtml(prospect.target_team_and_pick || '')})</span>
      <span class="tier-badge ${gmScore >= 9.0 ? 'tier-1' : gmScore >= 8.0 ? 'tier-2' : gmScore < 6.8 ? 'tier-4' : 'tier-3'}">
        GM Score: ${gmScore}
      </span>
      <span class="origin-tag-pill ${isInternational ? 'euro' : ''}">
        ${flag} ${escapeHtml(prospect.origin_type)}
      </span>
      <span class="player-pos-badge">${prospect.position}</span>`;

    // Origin Banner
    const crestImg = prospect.team_badge ? `<img class="modal-team-crest-mini" src="${prospect.team_badge}" alt="Crest">` : '';
    elements.modalOriginBanner.innerHTML = `
      ${crestImg}
      <span><strong>Antigo Clube / Time Pré-Draft:</strong> ${escapeHtml(prospect.origin_club_full || prospect.origin)} (${escapeHtml(prospect.origin_league || '')}) • ${flag} ${escapeHtml(prospect.origin_country || 'EUA')}</span>`;

    // Biometrics
    const bio = prospect.biometrics || {};
    elements.modalBiometrics.innerHTML = `
      <div class="bio-chip">
        <span class="bio-label">Altura</span>
        <span class="bio-val">${bio.height || '-'}</span>
      </div>
      <div class="bio-chip">
        <span class="bio-label">Envergadura</span>
        <span class="bio-val">${bio.wingspan || '-'}</span>
      </div>
      <div class="bio-chip">
        <span class="bio-label">Dif. Envergadura</span>
        <span class="bio-val" style="color: var(--accent-gold);">${bio.wingspan_differential || '-'}</span>
      </div>
      <div class="bio-chip">
        <span class="bio-label">Peso</span>
        <span class="bio-val">${bio.weight || '-'}</span>
      </div>
      <div class="bio-chip">
        <span class="bio-label">Salto Vertical</span>
        <span class="bio-val">${bio.vertical_max || '-'}</span>
      </div>
      <div class="bio-chip">
        <span class="bio-label">Idade no Draft</span>
        <span class="bio-val">${prospect.age_at_draft || '-'} anos</span>
      </div>`;

    // Render Tab 1: War Room Multi-Agent Evaluation
    renderWarRoomPanel(prospect);

    // Render Tab 2: Stats & Scout Reports
    renderStatsPanel(prospect);

    // Render Tab 3: Historical Reality
    renderRealityPanel(prospect);

    // Reset to first tab
    elements.modalTabBtns[0].click();

    // Show modal
    elements.dossierModal.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  function closeModal() {
    elements.dossierModal.classList.remove('active');
    if (elements.liveSimulationContainer) {
      elements.liveSimulationContainer.classList.remove('active');
      elements.simMessagesStream.innerHTML = '';
    }
    document.body.style.overflow = '';
  }

  function runLiveWarRoomSimulation(p) {
    if (!elements.liveSimulationContainer) return;
    
    // Reset messages stream
    elements.simMessagesStream.innerHTML = '';
    elements.liveSimulationContainer.classList.add('active');
    elements.liveSimStatusText.textContent = 'Conectando Especialistas...';
    
    elements.liveSimulationContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

    const debate = p.multiagent_debate || {};
    const quant = debate.quant || {};
    const tactical = debate.tactical || {};
    const fit = debate.fit || {};
    const gm = debate.gm_consensus || {};

    const steps = [
      {
        role: 'quant',
        name: 'Dr. Marcus Vance',
        title: 'Quant Agent • Head of Advanced Analytics & Biometrics',
        msg: `Iniciando auditoria métrica de ${p.player} (${p.origin}):\n"${quant.verdict || 'Avaliando dados'}"\nNota Quantitativa: ${quant.score}/10. Envergadura relativa: ${p.biometrics?.wingspan_differential || 'N/A'}.`
      },
      {
        role: 'tactical',
        name: 'Coach Frank Sullivan',
        title: 'Tactical Scout • Film Study & Tape de Ginásio',
        msg: `Dr. Vance, os dados brutos não captam a biomecânica fina! Pelo tape em ${p.origin}:\n"${tactical.verdict || 'Análise de fundamentos e vídeo'}"\nNota Tática: ${tactical.score}/10.`
      },
      {
        role: 'fit',
        name: 'Elena Rostova',
        title: 'VP of Roster Strategy • Pace & Space / Modern NBA',
        msg: `Avaliando a escalabilidade moderna de ${p.player} e troca defensiva:\n"${fit.verdict || 'Análise de encaixe posicional contemporâneo'}"\nNota de Fit Posicional: ${fit.score}/10.`
      },
      {
        role: 'gm',
        name: 'GM Brad Stevens Archetype',
        title: 'Decision Consensus Chair • Deliberação Vinculante',
        msg: `Atenção à mesa. Ponderando o teto atlético contra os trade-offs de risco:\n"${gm.consensus_verdict || 'Veredito final aprovado'}"\n⭐ NOTA FINAL CONSOLIDADA: ${gm.final_score || p.war_room?.gm_score} • BOARD: ${gm.draft_board_tier || p.war_room?.gm_tier}`
      }
    ];

    let currentStep = 0;

    function renderNextBubble() {
      if (currentStep >= steps.length) {
        elements.liveSimStatusText.textContent = '✅ Consenso Vinculante Finalizado!';
        return;
      }

      const item = steps[currentStep];
      elements.liveSimStatusText.textContent = `Em deliberação: ${item.name}...`;

      const typingEl = document.createElement('div');
      typingEl.className = 'sim-typing-indicator';
      typingEl.innerHTML = `<span>${item.name} elaborando parecer...</span> <div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div>`;
      elements.simMessagesStream.appendChild(typingEl);
      elements.simMessagesStream.scrollTop = elements.simMessagesStream.scrollHeight;

      setTimeout(() => {
        typingEl.remove();

        const bubble = document.createElement('div');
        bubble.className = `sim-bubble ${item.role}`;
        bubble.innerHTML = `
          <div class="sim-speaker-row">
            <div>
              <span class="sim-speaker-name ${item.role}">${item.name}</span>
              <div class="sim-speaker-role">${item.title}</div>
            </div>
          </div>
          <div class="sim-text">${escapeHtml(item.msg).replace(/\n/g, '<br/>')}</div>
        `;
        elements.simMessagesStream.appendChild(bubble);
        elements.simMessagesStream.scrollTop = elements.simMessagesStream.scrollHeight;

        currentStep++;
        setTimeout(renderNextBubble, 1000);
      }, 900);
    }

    renderNextBubble();
  }

  // Render War Room Deliberation Panel
  function renderWarRoomPanel(p) {
    const debate = p.multiagent_debate || {};
    const quant = debate.quant || {};
    const tactical = debate.tactical || {};
    const fit = debate.fit || {};
    const gm = debate.gm_consensus || {};

    const quantBullets = (quant.metric_highlights || []).map(b => `<li>${escapeHtml(b)}</li>`).join('');
    const tacticalBullets = (tactical.tape_observations || []).map(b => `<li>${escapeHtml(b)}</li>`).join('');
    const fitBullets = (fit.strategic_arguments || []).map(b => `<li>${escapeHtml(b)}</li>`).join('');

    elements.warRoomPanel.innerHTML = `
      <div class="agents-dossier-grid">
        <!-- Dr. Marcus Vance -->
        <div class="agent-eval-card quant">
          <div class="agent-header">
            <div>
              <div class="agent-name">Dr. Marcus Vance</div>
              <div class="agent-role">Quant Agent • Métricas Avançadas</div>
            </div>
            <div class="agent-score-bubble quant">${quant.score ?? '-'}</div>
          </div>
          <div class="agent-verdict-quote">"${escapeHtml(quant.verdict || 'Análise de dados quantitativos')}"</div>
          <ul class="agent-bullets">
            ${quantBullets}
          </ul>
        </div>

        <!-- Coach Frank Sullivan -->
        <div class="agent-eval-card tactical">
          <div class="agent-header">
            <div>
              <div class="agent-name">Coach Frank Sullivan</div>
              <div class="agent-role">Scout Tático • Vídeo & Fundamentos</div>
            </div>
            <div class="agent-score-bubble tactical">${tactical.score ?? '-'}</div>
          </div>
          <div class="agent-verdict-quote">"${escapeHtml(tactical.verdict || 'Análise tática de film study')}"</div>
          <ul class="agent-bullets">
            ${tacticalBullets}
          </ul>
        </div>

        <!-- Elena Rostova -->
        <div class="agent-eval-card fit">
          <div class="agent-header">
            <div>
              <div class="agent-name">Elena Rostova</div>
              <div class="agent-role">Fit & Upside • NBA Moderna</div>
            </div>
            <div class="agent-score-bubble fit">${fit.score ?? '-'}</div>
          </div>
          <div class="agent-verdict-quote">"${escapeHtml(fit.verdict || 'Análise de valor de reposição posicional')}"</div>
          <ul class="agent-bullets">
            ${fitBullets}
          </ul>
        </div>
      </div>

      <!-- GM Consensus -->
      <div class="gm-consensus-box">
        <div class="gm-consensus-header">
          <div class="gm-title">
            <span>👔</span> ${escapeHtml(gm.war_room_chair || 'General Manager Consensus')}
          </div>
          <div class="gm-tier-badge">
            ${escapeHtml(gm.draft_board_tier || p.war_room?.gm_tier || 'TIER 3')} (Nota: ${gm.final_score || p.war_room?.gm_score || '-'})
          </div>
        </div>
        <div class="gm-verdict-text">
          <strong>Veredito Oficial:</strong> ${escapeHtml(gm.consensus_verdict || '')}
        </div>
        ${gm.tension_analysis ? `
          <div class="gm-tension-block">
            <strong>⚡ Resolução de Conflitos da War Room:</strong> ${escapeHtml(gm.tension_analysis)}
          </div>` : ''}
      </div>`;
  }

  // Render Stats Panel
  function renderStatsPanel(p) {
    const stats = p.stats || {};
    const scout = p.scout_reports || {};
    const strengths = (scout.strengths || []).map(s => `<li>${escapeHtml(s)}</li>`).join('');
    const concerns = (scout.concerns || []).map(c => `<li>${escapeHtml(c)}</li>`).join('');

    elements.statsPanel.innerHTML = `
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 12px; margin-bottom: 28px;">
        <div class="summary-pill"><span class="label">Pontos (PTS)</span><span class="val gold">${stats.PTS ?? '-'}</span></div>
        <div class="summary-pill"><span class="label">Rebotes (REB)</span><span class="val">${stats.REB ?? '-'}</span></div>
        <div class="summary-pill"><span class="label">Assistências (AST)</span><span class="val">${stats.AST ?? '-'}</span></div>
        <div class="summary-pill"><span class="label">Roubos (STL)</span><span class="val">${stats.STL ?? '-'}</span></div>
        <div class="summary-pill"><span class="label">Tocos (BLK)</span><span class="val">${stats.BLK ?? '-'}</span></div>
        <div class="summary-pill"><span class="label">True Shooting (TS%)</span><span class="val green">${stats['TS%'] ? stats['TS%'] + '%' : '-'}</span></div>
        <div class="summary-pill"><span class="label">Uso Ofensivo (USG%)</span><span class="val">${stats['USG%'] ? stats['USG%'] + '%' : '-'}</span></div>
        <div class="summary-pill"><span class="label">3P% (Tentativas)</span><span class="val">${stats['3P%'] ? stats['3P%'] + '%' : '-'} (${stats['3PA'] ?? '-'})</span></div>
        <div class="summary-pill"><span class="label">Lance Livre (FT%)</span><span class="val gold">${stats['FT%'] ? stats['FT%'] + '%' : '-'} (${stats['FTA'] ?? '-'})</span></div>
        <div class="summary-pill"><span class="label">AST / TO Ratio</span><span class="val">${stats.AST_TO ?? '-'}</span></div>
        <div class="summary-pill"><span class="label">BPM Projetado</span><span class="val blue">${stats.BPM_est ? (stats.BPM_est > 0 ? '+' : '') + stats.BPM_est : '-'}</span></div>
      </div>

      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
        <div style="background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.25); border-radius: var(--radius-md); padding: 18px;">
          <h4 style="color: #34d399; font-size: 0.95rem; margin-bottom: 10px; display: flex; align-items: center; gap: 6px;">
            <span>✅</span> Pontos Fortes do Scout (Pré-Draft)
          </h4>
          <ul class="agent-bullets" style="color: #e2e8f0;">${strengths || '<li>Informação padrão de fundamentos.</li>'}</ul>
        </div>
        <div style="background: rgba(239, 68, 68, 0.08); border: 1px solid rgba(239, 68, 68, 0.25); border-radius: var(--radius-md); padding: 18px;">
          <h4 style="color: #f87171; font-size: 0.95rem; margin-bottom: 10px; display: flex; align-items: center; gap: 6px;">
            <span>⚠️</span> Preocupações & Red Flags
          </h4>
          <ul class="agent-bullets" style="color: #e2e8f0;">${concerns || '<li>Nenhuma restrição grave reportada.</li>'}</ul>
        </div>
      </div>`;
  }

  // Render Reality Panel
  function renderRealityPanel(p) {
    const h = p.historical_reality || {};

    elements.realityPanel.innerHTML = `
      <div class="modal-reality-section">
        <span class="reality-tag">Verificação Histórica da Escolha</span>
        <h4 style="font-size: 1.25rem; font-weight: 800; color: #fff; margin-bottom: 10px;">
          ${escapeHtml(h.nba_pick || 'Draft Pick')} • ${escapeHtml(h.historical_verdict || '')}
        </h4>
        <div style="font-size: 0.92rem; color: #cbd5e1; line-height: 1.6; margin-bottom: 18px;">
          ${escapeHtml(h.career_arc || 'Sem histórico registrado')}
        </div>
        <div style="display: flex; gap: 16px; flex-wrap: wrap;">
          <div class="summary-pill">
            <span class="label">All-Star Appearances</span>
            <span class="val gold">${h.all_star_appearances ?? 0} ⭐</span>
          </div>
          <div class="summary-pill">
            <span class="label">Veredito da War Room IA vs Realidade</span>
            <span class="val green">${p.war_room?.gm_score >= 8.5 ? '🎯 Projeção Certeira' : '📊 Calibrado'}</span>
          </div>
        </div>
      </div>`;
  }

  // Comparison Tool
  function populateCompareSelects() {
    const options = state.prospects
      .slice()
      .sort((a, b) => a.player.localeCompare(b.player))
      .map(p => `<option value="${escapeHtml(p.player)}">${escapeHtml(p.player)} (${p.class_year} - ${escapeHtml(p.origin)})</option>`)
      .join('');

    elements.selectPlayerA.innerHTML = options;
    elements.selectPlayerB.innerHTML = options;
  }

  function openCompareModal(nameA, nameB) {
    elements.selectPlayerA.value = nameA;
    elements.selectPlayerB.value = nameB;
    renderComparison(nameA, nameB);
    elements.compareModal.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  function closeCompareModal() {
    elements.compareModal.classList.remove('active');
    document.body.style.overflow = '';
  }

  function renderComparison(nameA, nameB) {
    const pA = state.prospects.find(p => p.player === nameA) || state.prospects[0];
    const pB = state.prospects.find(p => p.player === nameB) || state.prospects[1];

    state.duelPlayerA = pA;
    state.duelPlayerB = pB;

    // Render Duel Fighter Cards
    elements.compareDuelGrid.innerHTML = `
      <div class="duel-fighter-card">
        <div class="duel-portrait">
          <img src="${pA.local_image || 'assets/players/default_player.svg'}" 
               alt="${escapeHtml(pA.player)}" 
               onerror="this.src='assets/players/default_player.svg'">
        </div>
        <h3 style="font-size: 1.25rem; font-weight: 800; color: #fff;">${escapeHtml(pA.player)}</h3>
        <p style="color: var(--accent-gold); font-size: 0.82rem; font-weight: 700; margin-bottom: 6px;">
          ${escapeHtml(pA.origin)} (${pA.origin_country || 'EUA'})
        </p>
        <span class="tier-badge ${pA.war_room?.gm_score >= 9 ? 'tier-1' : pA.war_room?.gm_score >= 8 ? 'tier-2' : pA.war_room?.gm_score < 6.8 ? 'tier-4' : 'tier-3'}">
          GM: ${pA.war_room?.gm_score ?? '-'}
        </span>
      </div>

      <div class="duel-vs-circle">VS</div>

      <div class="duel-fighter-card">
        <div class="duel-portrait">
          <img src="${pB.local_image || 'assets/players/default_player.svg'}" 
               alt="${escapeHtml(pB.player)}" 
               onerror="this.src='assets/players/default_player.svg'">
        </div>
        <h3 style="font-size: 1.25rem; font-weight: 800; color: #fff;">${escapeHtml(pB.player)}</h3>
        <p style="color: var(--accent-blue); font-size: 0.82rem; font-weight: 700; margin-bottom: 6px;">
          ${escapeHtml(pB.origin)} (${pB.origin_country || 'EUA'})
        </p>
        <span class="tier-badge ${pB.war_room?.gm_score >= 9 ? 'tier-1' : pB.war_room?.gm_score >= 8 ? 'tier-2' : pB.war_room?.gm_score < 6.8 ? 'tier-4' : 'tier-3'}">
          GM: ${pB.war_room?.gm_score ?? '-'}
        </span>
      </div>`;

    // Render Metrics Comparison
    const metrics = [
      { name: 'War Room GM Score', keyA: pA.war_room?.gm_score, keyB: pB.war_room?.gm_score, max: 10, unit: '' },
      { name: 'Dr. Vance (Quant)', keyA: pA.war_room?.quant_score, keyB: pB.war_room?.quant_score, max: 10, unit: '' },
      { name: 'Coach Sullivan (Tático)', keyA: pA.war_room?.tactical_score, keyB: pB.war_room?.tactical_score, max: 10, unit: '' },
      { name: 'Elena Rostova (Fit NBA)', keyA: pA.war_room?.fit_score, keyB: pB.war_room?.fit_score, max: 10, unit: '' },
      { name: 'Pontos (PTS)', keyA: pA.stats?.PTS, keyB: pB.stats?.PTS, max: 30, unit: '' },
      { name: 'Assistências (AST)', keyA: pA.stats?.AST, keyB: pB.stats?.AST, max: 10, unit: '' },
      { name: 'Rebotes (REB)', keyA: pA.stats?.REB, keyB: pB.stats?.REB, max: 14, unit: '' },
      { name: 'True Shooting (TS%)', keyA: pA.stats?.['TS%'], keyB: pB.stats?.['TS%'], max: 70, unit: '%' },
      { name: 'Lance Livre (FT%)', keyA: pA.stats?.['FT%'], keyB: pB.stats?.['FT%'], max: 95, unit: '%' },
      { name: 'Projeção BPM', keyA: pA.stats?.BPM_est, keyB: pB.stats?.BPM_est, max: 16, unit: '' }
    ];

    const barsHtml = metrics.map(m => {
      const vA = m.keyA ?? 0;
      const vB = m.keyB ?? 0;
      const pctA = Math.min(100, Math.max(5, (vA / m.max) * 100));
      const pctB = Math.min(100, Math.max(5, (vB / m.max) * 100));
      const winnerA = vA > vB;
      const winnerB = vB > vA;

      return `
        <div class="compare-bar-row">
          <div class="bar-val-left ${winnerA ? 'winner' : ''}">${vA}${m.unit}</div>
          <div class="bar-track-left">
            <div class="bar-fill-left" style="width: ${pctA}%;"></div>
          </div>
          <div class="bar-metric-name">${m.name}</div>
          <div class="bar-track-right">
            <div class="bar-fill-right" style="width: ${pctB}%;"></div>
          </div>
          <div class="bar-val-right ${winnerB ? 'winner' : ''}">${vB}${m.unit}</div>
        </div>`;
    }).join('');

    elements.compareBarsList.innerHTML = barsHtml;
  }

  // Helper Escape HTML
  function escapeHtml(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  // Run on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
