// Patient Zero: The Missing Context - 4-Tab Core Application

let appState = {
  patients: [],
  activePatientId: "p0",
  currentPatient: null,
  activeTab: "dashboard",
  chartInstance: null,
  selectedProvenance: null
};

document.addEventListener("DOMContentLoaded", () => {
  initApp();
  setupEventListeners();
});

async function initApp() {
  try {
    const res = await fetch("/api/patients");
    const data = await res.json();
    appState.patients = data.patients || [];
    populatePatientSelector();
    await loadPatient(appState.activePatientId);
  } catch (err) {
    console.error("Failed to initialize:", err);
  }
}

function populatePatientSelector() {
  const sel = document.getElementById("patient-select");
  if (!sel) return;
  sel.innerHTML = "";
  appState.patients.forEach(p => {
    const opt = document.createElement("option");
    opt.value = p.id;
    opt.textContent = `${p.name} (${(p.conditions && p.conditions[0]) || 'General'})`;
    sel.appendChild(opt);
  });

  const addOpt = document.createElement("option");
  addOpt.value = "__new__";
  addOpt.textContent = "+ Add New Patient...";
  sel.appendChild(addOpt);

  sel.value = appState.activePatientId;
}

async function loadPatient(patientId) {
  try {
    appState.activePatientId = patientId;
    const res = await fetch(`/api/patients/${patientId}`);
    if (!res.ok) throw new Error("Failed to fetch patient data");
    appState.currentPatient = await res.json();

    renderCurrentView();
  } catch (err) {
    console.error("Error loading patient:", err);
  }
}

function switchTab(tabName) {
  appState.activeTab = tabName;
  const tabs = ["dashboard", "timeline", "trends", "documents"];
  
  tabs.forEach(t => {
    const pageEl = document.getElementById(`page-${t}`);
    const navBtn = document.getElementById(`nav-${t}`);
    if (pageEl) pageEl.classList.toggle("hidden", t !== tabName);
    if (navBtn) {
      if (t === tabName) {
        navBtn.className = "px-3.5 py-1.5 rounded-lg text-cyan-400 bg-cyan-500/10 border border-cyan-500/30 transition flex items-center gap-1.5";
      } else {
        navBtn.className = "px-3.5 py-1.5 rounded-lg text-slate-400 hover:text-slate-200 transition flex items-center gap-1.5";
      }
    }
  });

  renderCurrentView();
}

function renderCurrentView() {
  if (!appState.currentPatient) return;
  
  if (appState.activeTab === "dashboard") renderDashboard();
  else if (appState.activeTab === "timeline") renderTimeline();
  else if (appState.activeTab === "trends") renderTrends();
  else if (appState.activeTab === "documents") renderDocuments();

  if (window.lucide) lucide.createIcons();
}

/* ==========================================================================
   PAGE 1: DASHBOARD
   ========================================================================== */
function renderDashboard() {
  const p = appState.currentPatient;
  if (!p) return;

  document.getElementById("dash-patient-name").textContent = p.name;
  document.getElementById("dash-patient-summary").textContent = p.summary;
  
  // Count stats
  const docsCount = p.documents ? p.documents.length : 0;
  const medsCount = p.medications ? p.medications.length : 0;
  const visitsCount = p.timeline ? p.timeline.filter(e => e.category === "Consultation" || e.category === "Hospitalization").length : 0;
  const testsCount = p.labs ? p.labs.reduce((acc, l) => acc + l.points.length, 0) : 0;

  document.getElementById("dash-count-docs").textContent = docsCount;
  document.getElementById("dash-count-meds").textContent = medsCount;
  document.getElementById("dash-count-tests").textContent = testsCount;
  document.getElementById("dash-count-visits").textContent = visitsCount;

  // Recent Activity Feed (last 4 events)
  const recentContainer = document.getElementById("dash-recent-activity");
  recentContainer.innerHTML = "";
  const recentEvents = p.timeline ? [...p.timeline].reverse().slice(0, 4) : [];

  if (recentEvents.length === 0) {
    recentContainer.innerHTML = `
      <div class="p-6 rounded-xl bg-slate-900/40 border border-dashed border-slate-800 text-center space-y-2.5">
        <p class="text-xs text-slate-400">No medical encounters or documents ingested yet for <strong>${escapeHtml(p.name)}</strong>.</p>
        <button onclick="openUploadModal()" class="px-4 py-2 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-xs inline-flex items-center gap-2 shadow transition">
          <i data-lucide="upload-cloud" class="w-4 h-4"></i> Upload First Medical Document
        </button>
      </div>
    `;
  } else {
    recentEvents.forEach(ev => {
      const item = document.createElement("div");
      item.className = "p-3 rounded-xl bg-slate-900/70 border border-slate-800/80 hover:border-cyan-500/40 transition flex items-center justify-between gap-3 cursor-pointer";
      item.onclick = () => openProvenance(ev.provenance, ev.title, ev.category);

      const categoryBadge = getCategoryDot(ev.category);

      item.innerHTML = `
        <div class="flex items-center gap-3">
          ${categoryBadge}
          <div>
            <h4 class="text-xs font-bold text-slate-100">${ev.title}</h4>
            <span class="text-[11px] text-slate-400 font-mono">${ev.date} &bull; ${ev.provenance.document_name}</span>
          </div>
        </div>
        <button class="text-xs text-cyan-400 hover:text-cyan-300 font-semibold flex items-center gap-1">
          <span>View</span> &rarr;
        </button>
      `;
      recentContainer.appendChild(item);
    });
  }

  // Spotlight Lab Metric (e.g. Hemoglobin or HbA1c)
  if (p.labs && p.labs.length > 0) {
    const primaryLab = p.labs[0];
    const initial = primaryLab.points[0];
    const latest = primaryLab.points[primaryLab.points.length - 1];
    document.getElementById("dash-hb-initial").textContent = initial.value;
    document.getElementById("dash-hb-latest").textContent = latest.value;
    document.getElementById("dash-spotlight-desc").textContent = primaryLab.trend_interpretation;
  } else {
    document.getElementById("dash-hb-initial").textContent = "--";
    document.getElementById("dash-hb-latest").textContent = "--";
    document.getElementById("dash-spotlight-desc").textContent = "Upload laboratory panel to automatically plot biomarker progression.";
  }
}

/* ==========================================================================
   PAGE 2: TIMELINE (Clean stream with color dots)
   ========================================================================== */
function renderTimeline() {
  const p = appState.currentPatient;
  const container = document.getElementById("timeline-events-container");
  if (!p || !container) return;

  container.innerHTML = "";

  if (!p.timeline || p.timeline.length === 0) {
    container.innerHTML = `
      <div class="p-8 sm:p-12 rounded-2xl bg-slate-900/40 border border-dashed border-slate-800 text-center space-y-3 max-w-lg mx-auto">
        <div class="w-12 h-12 rounded-2xl bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center mx-auto text-cyan-400">
          <i data-lucide="file-plus-2" class="w-6 h-6"></i>
        </div>
        <h3 class="text-base font-bold text-white">Timeline is Empty</h3>
        <p class="text-xs text-slate-400 max-w-sm mx-auto">
          Upload medical files (PDFs, blood reports, prescriptions, scans, or doctor notes) to automatically extract clinical entities and build the chronological timeline.
        </p>
        <button onclick="openUploadModal()" class="px-5 py-2.5 rounded-xl bg-gradient-to-r from-cyan-500 to-teal-400 hover:from-cyan-400 hover:to-teal-300 text-slate-950 font-bold text-xs inline-flex items-center gap-2 shadow-lg shadow-cyan-500/20 transition transform hover:scale-105">
          <i data-lucide="upload-cloud" class="w-4 h-4"></i> Upload Patient Documents Now
        </button>
      </div>
    `;
    return;
  }

  p.timeline.forEach(ev => {
    const card = document.createElement("div");
    card.className = "relative flex items-start gap-4 group";

    const dotConfig = {
      "Laboratory": { color: "bg-blue-500", text: "🔵 Test", border: "border-blue-500/40", glow: "shadow-blue-500/30" },
      "Prescription": { color: "bg-emerald-500", text: "🟢 Medication", border: "border-emerald-500/40", glow: "shadow-emerald-500/30" },
      "Consultation": { color: "bg-purple-500", text: "🟣 Doctor Visit", border: "border-purple-500/40", glow: "shadow-purple-500/30" },
      "Imaging": { color: "bg-amber-500", text: "🟠 Scan", border: "border-amber-500/40", glow: "shadow-amber-500/30" },
      "Hospitalization": { color: "bg-rose-500", text: "🔴 Hospital", border: "border-rose-500/40", glow: "shadow-rose-500/30" },
      "Procedure": { color: "bg-teal-500", text: "🔵 Procedure", border: "border-teal-500/40", glow: "shadow-teal-500/30" }
    };
    const c = dotConfig[ev.category] || dotConfig["Consultation"];

    card.innerHTML = `
      <!-- Color Dot Node -->
      <div class="timeline-node w-5 h-5 rounded-full ${c.color} border-2 border-slate-900 shadow-md ${c.glow} flex-shrink-0 mt-3 -ml-2.5"></div>

      <!-- Content Box -->
      <div class="flex-1 glass-card rounded-xl p-4 hover:border-cyan-500/40 transition cursor-pointer" onclick="openProvenanceForEvent('${ev.id}')">
        <div class="flex items-center justify-between gap-2 mb-1.5 flex-wrap">
          <div class="flex items-center gap-2">
            <span class="text-xs font-mono font-bold text-cyan-400 bg-slate-900/90 px-2 py-0.5 rounded border border-slate-700/60">
              ${formatDate(ev.date)}
            </span>
            <span class="text-[11px] font-semibold text-slate-300">
              ${c.text}
            </span>
          </div>
          <button class="text-xs text-slate-400 group-hover:text-cyan-400 flex items-center gap-1 font-semibold transition">
            <i data-lucide="file-check-2" class="w-3.5 h-3.5"></i>
            <span>View Source</span>
          </button>
        </div>

        <h4 class="text-sm font-bold text-slate-100 group-hover:text-cyan-300 transition">${ev.title}</h4>
        <p class="text-xs text-slate-300 mt-1 leading-relaxed">${ev.summary}</p>

        <!-- Provenance Quote Snippet -->
        <div class="provenance-quote-box text-xs text-slate-400 flex items-center justify-between gap-2 mt-2.5">
          <span class="truncate">"${ev.provenance.verbatim_quote}"</span>
          <span class="font-mono text-[11px] text-cyan-400 flex-shrink-0">📄 ${ev.provenance.document_name}</span>
        </div>
      </div>
    `;

    container.appendChild(card);
  });
}

function openProvenanceForEvent(eventId) {
  const ev = appState.currentPatient.timeline.find(x => x.id === eventId);
  if (!ev) return;
  openProvenance(ev.provenance, ev.title, ev.category);
}

/* ==========================================================================
   PAGE 3: TRENDS (Hemoglobin & Common Tests)
   ========================================================================== */
function renderTrends() {
  const p = appState.currentPatient;
  const select = document.getElementById("trend-metric-select");
  const grid = document.getElementById("trend-cards-grid");
  if (!p || !select || !grid) return;

  select.innerHTML = "";
  grid.innerHTML = "";

  if (!p.labs || p.labs.length === 0) {
    grid.innerHTML = `
      <div class="col-span-full p-8 rounded-2xl bg-slate-900/40 border border-dashed border-slate-800 text-center space-y-3">
        <p class="text-xs text-slate-400">No laboratory test panels documented yet for <strong>${escapeHtml(p.name)}</strong>.</p>
        <button onclick="openUploadModal()" class="px-4 py-2 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-xs inline-flex items-center gap-2 shadow transition">
          <i data-lucide="upload-cloud" class="w-4 h-4"></i> Upload Lab Results
        </button>
      </div>
    `;
    if (appState.chartInstance) {
      appState.chartInstance.destroy();
      appState.chartInstance = null;
    }
    const statRow = document.getElementById("trend-stat-row");
    if (statRow) statRow.innerHTML = "";
    return;
  }

  p.labs.forEach((series, idx) => {
    const opt = document.createElement("option");
    opt.value = idx;
    opt.textContent = `${series.test_name} (${series.unit})`;
    select.appendChild(opt);

    // Render summary card for this test
    const initial = series.points[0];
    const latest = series.points[series.points.length - 1];
    const delta = (latest.value - initial.value).toFixed(1);
    const deltaSign = delta > 0 ? "+" : "";

    const card = document.createElement("div");
    card.className = "glass-card rounded-xl p-4 border border-slate-800 hover:border-cyan-500/40 transition cursor-pointer";
    card.onclick = () => {
      select.value = idx;
      updateTrendChart(series);
    };

    card.innerHTML = `
      <div class="flex items-center justify-between mb-1.5">
        <span class="text-xs font-bold text-cyan-400">${series.test_name}</span>
        <span class="text-[11px] text-slate-400 font-mono">${series.points.length} Tests</span>
      </div>
      <div class="text-xl font-extrabold text-white brand-font my-1">
        ${initial.value} &rarr; <span class="text-emerald-400">${latest.value}</span> <span class="text-xs font-normal text-slate-400">${series.unit}</span>
      </div>
      <div class="text-xs font-semibold text-emerald-400 mb-2">
        Trend: ${deltaSign}${delta} ${series.unit}
      </div>
      <p class="text-[11px] text-slate-300 leading-relaxed line-clamp-2">${series.trend_interpretation}</p>
    `;
    grid.appendChild(card);
  });

  select.onchange = (e) => updateTrendChart(p.labs[e.target.value]);
  updateTrendChart(p.labs[0]);
}

function updateTrendChart(series) {
  const canvas = document.getElementById("trend-chart-canvas");
  if (!canvas || !series) return;

  const ctx = canvas.getContext("2d");
  if (appState.chartInstance) appState.chartInstance.destroy();

  const labels = series.points.map(pt => formatDate(pt.date));
  const values = series.points.map(pt => pt.value);

  appState.chartInstance = new Chart(ctx, {
    type: "line",
    data: {
      labels: labels,
      datasets: [
        {
          label: `${series.test_name} (${series.unit})`,
          data: values,
          borderColor: "#06b6d4",
          backgroundColor: "rgba(6, 182, 212, 0.15)",
          borderWidth: 3,
          fill: true,
          tension: 0.3,
          pointBackgroundColor: "#06b6d4",
          pointBorderColor: "#ffffff",
          pointRadius: 6,
          pointHoverRadius: 9
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { labels: { color: "#e2e8f0", font: { family: "Inter", size: 12 } } },
        tooltip: {
          callbacks: {
            afterBody: (items) => {
              const pt = series.points[items[0].dataIndex];
              return `Reference: ${pt.reference_range}\nClick to inspect source report.`;
            }
          }
        }
      },
      scales: {
        x: { grid: { color: "rgba(255, 255, 255, 0.05)" }, ticks: { color: "#94a3b8" } },
        y: { grid: { color: "rgba(255, 255, 255, 0.05)" }, ticks: { color: "#94a3b8" } }
      },
      onClick: (e, elements) => {
        if (elements.length > 0) {
          const pt = series.points[elements[0].index];
          openProvenance(pt.provenance, `${series.test_name}: ${pt.value} ${pt.unit}`, "Laboratory");
        }
      }
    }
  });

  // Populate stat row below chart
  const statRow = document.getElementById("trend-stat-row");
  if (statRow) {
    const initial = series.points[0];
    const latest = series.points[series.points.length - 1];
    const delta = (latest.value - initial.value).toFixed(1);

    statRow.innerHTML = `
      <div class="bg-slate-900/80 p-3 rounded-xl border border-slate-800">
        <span class="text-slate-400 block text-[11px]">Progression:</span>
        <strong class="text-white text-sm">${initial.value} &rarr; ${latest.value} ${series.unit}</strong>
      </div>
      <div class="bg-slate-900/80 p-3 rounded-xl border border-slate-800">
        <span class="text-slate-400 block text-[11px]">Net Change:</span>
        <strong class="text-emerald-400 text-sm">${delta > 0 ? '+' : ''}${delta} ${series.unit}</strong>
      </div>
      <div class="bg-slate-900/80 p-3 rounded-xl border border-slate-800">
        <span class="text-slate-400 block text-[11px]">Reference Range:</span>
        <strong class="text-slate-200 text-sm">${series.normal_min} - ${series.normal_max} ${series.unit}</strong>
      </div>
    `;
  }
}

/* ==========================================================================
   PAGE 4: DOCUMENTS (Source Vault)
   ========================================================================== */
function renderDocuments() {
  const p = appState.currentPatient;
  const grid = document.getElementById("documents-grid");
  if (!p || !grid) return;

  grid.innerHTML = "";

  if (!p.documents || p.documents.length === 0) {
    grid.innerHTML = `
      <div class="col-span-full p-8 sm:p-12 rounded-2xl bg-slate-900/40 border border-dashed border-slate-800 text-center space-y-3">
        <div class="w-12 h-12 rounded-2xl bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center mx-auto text-cyan-400">
          <i data-lucide="folder-plus" class="w-6 h-6"></i>
        </div>
        <h3 class="text-base font-bold text-white">Document Vault is Empty</h3>
        <p class="text-xs text-slate-400 max-w-sm mx-auto">
          No medical records uploaded for <strong>${escapeHtml(p.name)}</strong> yet. Ingest prescriptions, laboratory reports, or discharge summaries.
        </p>
        <button onclick="openUploadModal()" class="px-4 py-2 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-xs inline-flex items-center gap-2 shadow transition">
          <i data-lucide="upload-cloud" class="w-4 h-4"></i> Upload First Document
        </button>
      </div>
    `;
    return;
  }

  p.documents.forEach(doc => {
    const card = document.createElement("div");
    card.className = "glass-card rounded-xl p-5 border border-slate-800 hover:border-blue-500/40 transition flex flex-col justify-between";

    const iconName = doc.doc_type.includes("Lab") ? "flask-conical" : (doc.doc_type.includes("Prescription") ? "pill" : "file-text");

    card.innerHTML = `
      <div>
        <div class="flex items-center justify-between mb-3">
          <span class="text-xs font-bold px-2 py-0.5 rounded bg-blue-950/60 text-blue-300 border border-blue-800/40">
            ${doc.doc_type}
          </span>
          <span class="text-xs font-mono text-slate-400">${formatDate(doc.date)}</span>
        </div>

        <h4 class="font-bold text-sm text-slate-100 mb-1">${doc.title}</h4>
        <p class="text-xs text-slate-400 font-mono mb-3">${doc.file_name}</p>
        
        <div class="text-xs text-slate-400 mb-4 space-y-1">
          <div><strong class="text-slate-300">Author:</strong> ${doc.author}</div>
          <div><strong class="text-slate-300">Facility:</strong> ${doc.facility}</div>
        </div>
      </div>

      <button onclick="openFullDocumentModal('${doc.id}', null)" class="w-full py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold flex items-center justify-center gap-1.5 border border-slate-700 transition">
        <i data-lucide="eye" class="w-3.5 h-3.5 text-cyan-400"></i>
        <span>[View Original Report]</span>
      </button>
    `;

    grid.appendChild(card);
  });
}

/* ==========================================================================
   KILLER FEATURE: "✨ What changed?"
   ========================================================================== */
async function openWhatChangedModal() {
  const modal = document.getElementById("modal-what-changed");
  const content = document.getElementById("what-changed-content");
  modal.classList.remove("hidden");

  content.innerHTML = `
    <div class="text-center py-8">
      <div class="w-5 h-5 rounded-full border-2 border-amber-400 border-t-transparent animate-spin mx-auto mb-2"></div>
      <p class="text-slate-400">Analyzing cross-document evolutions & changes...</p>
    </div>
  `;

  try {
    const res = await fetch(`/api/patients/${appState.activePatientId}/what-changed`);
    const data = await res.json();

    let html = `
      <div class="space-y-5">
        
        <!-- 1. Blood Tests Section -->
        <div>
          <h4 class="text-xs font-black text-cyan-400 uppercase tracking-wider mb-2 flex items-center gap-1.5">
            <i data-lucide="activity" class="w-4 h-4"></i> Blood Tests & Repeated Biomarkers
          </h4>
          <div class="space-y-2">
            ${data.blood_tests.map(t => `
              <div class="p-3 rounded-xl bg-slate-900/90 border border-slate-800 flex items-center justify-between gap-3">
                <div>
                  <strong class="text-slate-100 block text-xs">${t.summary}</strong>
                  <span class="text-[11px] text-slate-400">${t.interpretation} &bull; Tested ${t.times_tested} times</span>
                </div>
                <button onclick="openProvenanceFromCitation('${escapeHtml(JSON.stringify(t.provenance))}')" class="px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-cyan-400 text-xs font-mono font-semibold flex-shrink-0 transition">
                  ${t.delta} &rarr;
                </button>
              </div>
            `).join("")}
          </div>
        </div>

        <!-- 2. Medications Section -->
        <div>
          <h4 class="text-xs font-black text-emerald-400 uppercase tracking-wider mb-2 flex items-center gap-1.5">
            <i data-lucide="pill" class="w-4 h-4"></i> Medications Timeline
          </h4>
          <div class="space-y-2">
            ${data.medications.map(m => `
              <div class="p-3 rounded-xl bg-slate-900/90 border border-slate-800 flex items-center justify-between gap-3">
                <div>
                  <strong class="text-slate-100 block text-xs">${m.name} (${m.dosage})</strong>
                  <span class="text-[11px] text-slate-400">First documented: <strong>${m.first_seen}</strong> &bull; Last documented mention: <strong>${m.last_seen}</strong></span>
                </div>
                <button onclick="openProvenanceFromCitation('${escapeHtml(JSON.stringify(m.provenance))}')" class="px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-emerald-400 text-xs font-mono font-semibold flex-shrink-0 transition">
                  Source &rarr;
                </button>
              </div>
            `).join("")}
          </div>
        </div>

        <!-- 3. Missing Information & Alerts -->
        <div>
          <h4 class="text-xs font-black text-rose-400 uppercase tracking-wider mb-2 flex items-center gap-1.5">
            <i data-lucide="alert-triangle" class="w-4 h-4"></i> Missing Information & Discrepancies
          </h4>
          <div class="space-y-2">
            ${data.missing_information.length > 0 ? data.missing_information.map(mi => `
              <div class="p-3 rounded-xl bg-rose-950/20 border border-rose-900/50">
                <div class="flex items-center gap-1.5 text-rose-300 font-bold mb-1">
                  <i data-lucide="alert-circle" class="w-3.5 h-3.5"></i>
                  <span>⚠ ${mi.title}</span>
                </div>
                <p class="text-slate-300 text-[11px] leading-relaxed">${mi.description}</p>
                <div class="text-rose-400/90 text-[11px] mt-1 font-medium">Resolution: ${mi.recommendation}</div>
              </div>
            `).join("") : `<p class="text-slate-400 text-xs italic">No critical missing information detected.</p>`}
          </div>
        </div>

        <!-- 4. Repeated Testing Frequency -->
        <div>
          <h4 class="text-xs font-black text-purple-400 uppercase tracking-wider mb-2 flex items-center gap-1.5">
            <i data-lucide="repeat" class="w-4 h-4"></i> Repeated Testing Frequency
          </h4>
          <div class="p-3 rounded-xl bg-slate-900/90 border border-slate-800 space-y-1">
            ${data.repeated_tests.map(r => `
              <div class="text-slate-300 text-xs">&bull; ${r.frequency_summary}</div>
            `).join("")}
          </div>
        </div>

      </div>
    `;

    content.innerHTML = html;
    if (window.lucide) lucide.createIcons();
  } catch (err) {
    content.innerHTML = `<p class="text-rose-400 text-xs">Failed to load changes summary.</p>`;
  }
}

function closeWhatChangedModal() {
  document.getElementById("modal-what-changed").classList.add("hidden");
}

/* ==========================================================================
   SOURCE PROVENANCE & ORIGINAL REPORT VIEWER
   ========================================================================== */
function openProvenance(prov, title, category) {
  appState.selectedProvenance = prov;
  const drawer = document.getElementById("provenance-drawer");
  const overlay = document.getElementById("provenance-overlay");

  document.getElementById("prov-title").textContent = title;
  document.getElementById("prov-category").textContent = category;
  document.getElementById("prov-doc-name").textContent = prov.document_name;
  document.getElementById("prov-date").textContent = formatDate(prov.date);
  document.getElementById("prov-page").textContent = `Page ${prov.page_number}`;
  document.getElementById("prov-quote").textContent = `"${prov.verbatim_quote}"`;
  
  const scorePercent = Math.round(prov.confidence_score * 100);
  document.getElementById("prov-score").textContent = `${scorePercent}%`;
  document.getElementById("prov-meter-fill").style.width = `${scorePercent}%`;
  document.getElementById("prov-certainty-badge").textContent = `${prov.certainty_level} Certainty`;

  const viewDocBtn = document.getElementById("prov-view-doc-btn");
  viewDocBtn.onclick = () => openFullDocumentModal(prov.document_id, prov.verbatim_quote);

  overlay.classList.remove("hidden");
  drawer.classList.remove("translate-x-full");

  if (window.lucide) lucide.createIcons();
}

function closeProvenance() {
  const drawer = document.getElementById("provenance-drawer");
  const overlay = document.getElementById("provenance-overlay");
  drawer.classList.add("translate-x-full");
  setTimeout(() => overlay.classList.add("hidden"), 300);
}

async function openFullDocumentModal(docId, quoteToHighlight) {
  try {
    const res = await fetch(`/api/patients/${appState.activePatientId}/documents/${docId}`);
    if (!res.ok) throw new Error("Document not found");
    const doc = await res.json();

    document.getElementById("doc-modal-title").textContent = doc.title;
    document.getElementById("doc-modal-meta").textContent = `${doc.facility} &bull; Date: ${doc.date} &bull; Author: ${doc.author}`;
    
    let bodyHtml = escapeHtml(doc.raw_text);
    if (quoteToHighlight) {
      const cleanQuote = quoteToHighlight.replace(/^["']|["']$/g, "").trim();
      if (cleanQuote.length > 5) {
        const regex = new RegExp(`(${cleanQuote.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi');
        bodyHtml = bodyHtml.replace(regex, `<mark class="bg-amber-400/40 text-amber-200 px-1 py-0.5 rounded border border-amber-500/50 font-bold">$1</mark>`);
      }
    }

    let imagePreviewHtml = "";
    const isImageFile = doc.is_image || (doc.file_url && doc.file_url.match(/\.(jpe?g|png|webp|bmp|gif)$/i)) || (doc.file_name && doc.file_name.match(/\.(jpe?g|png|webp|bmp|gif)$/i));
    if (isImageFile && doc.file_url) {
      imagePreviewHtml = `
        <div class="mb-4 p-3 bg-slate-900/90 rounded-xl border border-slate-800 text-center">
          <span class="text-[11px] text-cyan-400 block mb-2 font-mono font-semibold">📷 Original Uploaded Image (${escapeHtml(doc.file_name)}):</span>
          <img src="${doc.file_url}" alt="${escapeHtml(doc.title)}" class="max-h-80 mx-auto rounded-lg border border-slate-700 shadow-xl object-contain" onerror="this.parentElement.style.display='none'">
        </div>
      `;
    }

    document.getElementById("doc-modal-body").innerHTML = `
      ${imagePreviewHtml}
      <div class="p-3.5 bg-slate-950/80 rounded-xl border border-slate-800">
        <span class="text-[11px] font-bold text-cyan-400 uppercase tracking-wider block mb-1.5">Extracted Clinical Content:</span>
        <pre class="whitespace-pre-wrap font-mono text-xs leading-relaxed text-slate-200">${bodyHtml}</pre>
      </div>
    `;
    document.getElementById("doc-modal").classList.remove("hidden");
  } catch (err) {
    console.error("Failed to load document preview:", err);
  }
}

function closeDocumentModal() {
  document.getElementById("doc-modal").classList.add("hidden");
}

function openProvenanceFromCitation(jsonStr) {
  try {
    const prov = JSON.parse(jsonStr);
    closeWhatChangedModal();
    openProvenance(prov, "Original Source Record", "Laboratory");
  } catch (e) {
    console.error("Citation error:", e);
  }
}

/* ==========================================================================
   NEW PATIENT MODAL & CREATION
   ========================================================================== */
function openNewPatientModal() {
  const m = document.getElementById("modal-new-patient");
  if (m) m.classList.remove("hidden");
  if (window.lucide) lucide.createIcons();
}

function closeNewPatientModal() {
  const m = document.getElementById("modal-new-patient");
  if (m) m.classList.add("hidden");
}

function fillNewPatientPreset(type) {
  if (type === "miller") {
    document.getElementById("np-name").value = "David Miller";
    document.getElementById("np-age").value = "52";
    document.getElementById("np-gender").value = "Male";
    document.getElementById("np-blood").value = "A+";
    document.getElementById("np-mrn").value = "DM-91402";
    document.getElementById("np-conditions").value = "Hypertension, Hyperlipidemia";
    document.getElementById("np-allergies").value = "Penicillin (severe hives)";
    document.getElementById("np-summary").value = "52-year-old male tracking longitudinal cardiovascular response and medication tolerance.";
  } else if (type === "clear") {
    document.getElementById("np-name").value = "";
    document.getElementById("np-age").value = "35";
    document.getElementById("np-gender").value = "Male";
    document.getElementById("np-blood").value = "O+";
    document.getElementById("np-mrn").value = "";
    document.getElementById("np-conditions").value = "";
    document.getElementById("np-allergies").value = "";
    document.getElementById("np-summary").value = "";
  }
}

async function handleCreatePatient(e) {
  e.preventDefault();
  const name = document.getElementById("np-name").value.trim();
  const age = parseInt(document.getElementById("np-age").value, 10) || 35;
  const gender = document.getElementById("np-gender").value;
  const blood = document.getElementById("np-blood").value;
  const mrn = document.getElementById("np-mrn").value.trim();
  const condStr = document.getElementById("np-conditions").value.trim();
  const conditions = condStr ? condStr.split(",").map(s => s.trim()).filter(Boolean) : ["General Health"];
  const allgStr = document.getElementById("np-allergies").value.trim();
  const allergies = allgStr ? allgStr.split(",").map(s => s.trim()).filter(Boolean) : ["No Known Drug Allergies"];
  const summary = document.getElementById("np-summary").value.trim();

  const payload = {
    name,
    age,
    gender,
    blood_type: blood,
    mrn: mrn || undefined,
    chronic_conditions: conditions,
    allergies,
    summary: summary || undefined
  };

  try {
    const res = await fetch("/api/patients", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw new Error("Failed to register patient");
    const data = await res.json();
    const newPatient = data.patient;

    // Refresh patients list
    const listRes = await fetch("/api/patients");
    const listData = await listRes.json();
    appState.patients = listData.patients || [];
    populatePatientSelector();

    // Select the new patient
    appState.activePatientId = newPatient.id;
    const sel = document.getElementById("patient-select");
    if (sel) sel.value = newPatient.id;

    closeNewPatientModal();
    await loadPatient(newPatient.id);
    switchTab("dashboard");
  } catch (err) {
    alert("Error creating patient: " + err.message);
  }
}

function loadSampleDocText(type) {
  const ta = document.getElementById("text-input");
  if (!ta) return;

  if (type === "cbc_jan") {
    ta.value = `DIAGNOSTIC PATHOLOGY LABORATORY REPORT
Date: 2026-01-15
Facility: Metro Health Diagnostic Center
Encounter: Comprehensive Blood Count (CBC)
Specimen: Whole Blood Venipuncture

RESULTS:
Hemoglobin: 11.2 g/dL [Low] (Reference: 12.0 - 17.5 g/dL)
WBC: 6,800 /uL [Normal] (Reference: 4,000 - 11,000 /uL)
Platelets: 240,000 /uL [Normal]
Ferritin: 10.5 ng/mL [Low] (Reference: 15.0 - 200.0 ng/mL)

CLINICAL IMPRESSION:
Microcytic hypochromic indices consistent with early iron deficiency anemia. Clinical correlation and dietary/supplemental iron recommended.`;
  } else if (type === "rx_iron") {
    ta.value = `OUTPATIENT CLINICAL ENCOUNTER & PRESCRIPTION
Date: 2026-01-20
Facility: Metro Health Clinic
Provider: Dr. Robert Vance, MD
Department: Internal Medicine

ASSESSMENT & PLAN:
Patient presents with progressive fatigue. Review of lab report dated Jan 15 reveals Hemoglobin 11.2 g/dL and low ferritin.

ORDERS / PRESCRIPTION:
Rx Initiate Ferrous Ascorbate 100mg once daily with orange juice for 90 days.
Follow-up repeated CBC in 8 to 12 weeks to monitor response.`;
  } else if (type === "cbc_march") {
    ta.value = `DIAGNOSTIC PATHOLOGY LABORATORY REPORT
Date: 2026-03-25
Facility: Metro Health Diagnostic Center
Encounter: Follow-up Blood Count
Specimen: Venous Blood

RESULTS:
Hemoglobin: 13.1 g/dL [Normal] (Reference: 12.0 - 17.5 g/dL)
WBC: 7,100 /uL [Normal]
Ferritin: 24.0 ng/mL [Normal] (Reference: 15.0 - 200.0 ng/mL)

INTERPRETATION:
Marked hematologic recovery following oral iron therapy. Hemoglobin normalized from baseline 11.2 g/dL to 13.1 g/dL.`;
  } else if (type === "allergy_clash") {
    ta.value = `URGENT CARE CLINIC ENCOUNTER
Date: 2026-02-10
Facility: Downtown Urgent Care
Provider: Dr. Lisa Ray, DO
Reason for Visit: Acute Bacterial Sinusitis

ORDERS:
Prescribed Amoxicillin 500mg three times daily for 7 days.`;
  } else if (type === "skin_report") {
    ta.value = `CLINICAL DERMATOLOGY ENCOUNTER & PRESCRIPTION
Date: 2026-09-18
Facility: Metro Dermatology Associates
Provider: Dr. Elena Rostova, MD (Dermatology)
Diagnosis: Inflammatory Dermatitis & Cutaneous Folliculitis

EXAMINATION & CLINICAL ASSESSMENT:
Erythematous papular skin eruptions observed. Pruritic cutaneous presentation.

ORDERS / PRESCRIPTION:
Rx Initiate Doxycycline 100mg once daily with large glass of water for 30 days.
Rx Apply Clindamycin 1% topical gel thin layer once daily in the morning.
Rx Apply Hydrocortisone 1% cream thin layer twice daily as needed for pruritus.

CARE INSTRUCTIONS:
Avoid excessive sun exposure. Re-evaluate response in 4 weeks.`;
  }
}

/* ==========================================================================
   UPLOAD MODAL
   ========================================================================== */
function openUploadModal() {
  document.getElementById("modal-upload").classList.remove("hidden");
  if (window.lucide) lucide.createIcons();
}
function closeUploadModal() {
  document.getElementById("modal-upload").classList.add("hidden");
}

/* ==========================================================================
   3-MINUTE HACKATHON PITCH SIMULATOR
   ========================================================================== */
async function runPitchDemo() {
  // Step 1: Switch to Rahul Sharma
  appState.activePatientId = "p0";
  document.getElementById("patient-select").value = "p0";
  await loadPatient("p0");

  // Step 2: Open Upload animation briefly
  openUploadModal();
  const animBox = document.getElementById("upload-anim-box");
  const animText = document.getElementById("upload-anim-text");
  animBox.classList.remove("hidden");

  animText.textContent = "Step 1: Uploading 4 scattered documents (CBCs & Prescriptions)...";
  await sleep(1500);

  animText.textContent = "Step 2: AI extracting structured clinical entities & dates...";
  await sleep(1500);

  animText.textContent = "Step 3: Connecting events & building longitudinal timeline...";
  await sleep(1500);

  closeUploadModal();
  animBox.classList.add("hidden");

  // Step 3: Switch to Timeline
  switchTab("timeline");
  await sleep(1000);

  // Step 4: Automatically trigger "What changed?"
  openWhatChangedModal();
  await sleep(2500);

  // Step 5: Open Source Provenance
  closeWhatChangedModal();
  const juneEvent = appState.currentPatient.timeline.find(e => e.title.includes("13.7"));
  if (juneEvent) {
    openProvenance(juneEvent.provenance, juneEvent.title, juneEvent.category);
  }

  // Step 6: Show closing pitch toast
  const toast = document.getElementById("pitch-toast");
  toast.classList.remove("hidden");
  setTimeout(() => toast.classList.add("hidden"), 8000);
}

/* ==========================================================================
   HELPERS & EVENT LISTENERS
   ========================================================================== */
function setupEventListeners() {
  const sel = document.getElementById("patient-select");
  if (sel) {
    sel.addEventListener("change", (e) => {
      if (e.target.value === "__new__") {
        openNewPatientModal();
        e.target.value = appState.activePatientId;
      } else {
        loadPatient(e.target.value);
      }
    });
  }

  const uploadForm = document.getElementById("upload-form");
  if (uploadForm) {
    uploadForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const textVal = document.getElementById("text-input").value.trim();
      const fileInput = document.getElementById("file-input");

      const formData = new FormData();
      if (fileInput.files.length > 0) {
        formData.append("file", fileInput.files[0]);
      } else if (textVal) {
        formData.append("raw_text", textVal);
        formData.append("doc_title", "Manual Upload Note");
      } else {
        alert("Please drop a file or paste medical text.");
        return;
      }

      const animBox = document.getElementById("upload-anim-box");
      const animText = document.getElementById("upload-anim-text");
      animBox.classList.remove("hidden");
      animText.textContent = "Extracting records and rebuilding timeline...";

      try {
        await fetch(`/api/patients/${appState.activePatientId}/upload`, {
          method: "POST",
          body: formData
        });
        animBox.classList.add("hidden");
        closeUploadModal();
        document.getElementById("text-input").value = "";
        fileInput.value = "";
        const dropTitle = document.querySelector("#drop-zone p.font-bold");
        if (dropTitle) dropTitle.textContent = "Drop medical files here or click to browse";
        await loadPatient(appState.activePatientId);
        switchTab("timeline");
      } catch (err) {
        animBox.classList.add("hidden");
        alert("Upload error: " + err.message);
      }
    });
  }

  // Drop zone click
  const dropZone = document.getElementById("drop-zone");
  const fileInput = document.getElementById("file-input");
  if (dropZone && fileInput) {
    dropZone.onclick = () => fileInput.click();
    fileInput.onchange = () => {
      if (fileInput.files.length > 0) {
        dropZone.querySelector("p.font-bold").textContent = `Selected: ${fileInput.files[0].name}`;
      }
    };
  }
}

function getCategoryDot(category) {
  const dots = {
    "Laboratory": '<span class="w-3 h-3 rounded-full bg-blue-500 shadow shadow-blue-500/50 flex-shrink-0"></span>',
    "Prescription": '<span class="w-3 h-3 rounded-full bg-emerald-500 shadow shadow-emerald-500/50 flex-shrink-0"></span>',
    "Consultation": '<span class="w-3 h-3 rounded-full bg-purple-500 shadow shadow-purple-500/50 flex-shrink-0"></span>',
    "Imaging": '<span class="w-3 h-3 rounded-full bg-amber-500 shadow shadow-amber-500/50 flex-shrink-0"></span>',
    "Hospitalization": '<span class="w-3 h-3 rounded-full bg-rose-500 shadow shadow-rose-500/50 flex-shrink-0"></span>'
  };
  return dots[category] || dots["Consultation"];
}

function formatDate(dateStr) {
  if (!dateStr) return "";
  try {
    const parts = dateStr.split("-");
    if (parts.length === 3) {
      const d = new Date(parts[0], parts[1] - 1, parts[2]);
      return d.toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" });
    }
  } catch (e) {}
  return dateStr;
}

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

function escapeHtml(str) {
  if (!str) return "";
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}
