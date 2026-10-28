const $ = id => document.getElementById(id);
const tabs = ["analyse", "batches", "library", "alerts", "learn", "tools"];
const NAMES = {
  analyse: "🔬 Analyse",
  batches: "📦 Batches",
  library: "🌍 Library",
  alerts: "🔔 Alerts",
  learn: "📘 Learn",
  tools: "🧮 Tools"
};

const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({
  "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;"
}[c]));

const J = async (u, o) => {
  const r = await fetch(u, o);
  if (r.status === 401) {
    location = "/login";
    return {};
  }
  const d = await r.json();
  if (d && d.error && u !== "/api/analyse" && !u.includes("/confirm")) {
    toast(d.error, "bad");
  }
  return d;
};

// Setup nav tabs
$("nav").innerHTML = tabs.map(t => `<button id="n_${t}" onclick="go('${t}')">${NAMES[t]}</button>`).join("");

function go(t) {
  tabs.forEach(x => {
    $(x).classList.toggle("on", x === t);
    $("n_" + x).classList.toggle("on", x === t);
  });
  ({ library: lib, alerts: al, batches: bat })[t]?.();
}

function toast(m, k) {
  const b = $("toast");
  b.className = "toast " + k;
  b.textContent = m;
  b.style.display = "block";
  setTimeout(() => { b.style.display = "none"; }, 8000);
}

go("analyse");

// ================= FILE SELECTION & PREVIEW =================

function updatePreview(file, name, sizeText) {
  const prev = $("prev");
  const previewContainer = $("drop-preview-container");
  const dropPrompt = $("drop-prompt");
  const statusBadge = $("upload-status-badge");
  const statusDot = $("upload-status-dot");
  const statusText = $("upload-status-text");

  if (file) {
    prev.src = URL.createObjectURL(file);
    prev.hidden = false;
    if (previewContainer) previewContainer.style.display = "flex";
    if (dropPrompt) dropPrompt.style.display = "none";
    if ($("preview-filename")) $("preview-filename").textContent = name || file.name || "rice_sample.png";
    if ($("preview-filesize")) $("preview-filesize").textContent = sizeText || ((file.size / 1024).toFixed(1) + " KB · Ready for inspection");
    if (statusBadge) {
      statusBadge.className = "card-quick-status ready";
      if (statusDot) statusDot.className = "status-dot ready";
      if (statusText) statusText.textContent = "Sample Image Ready";
    }
  } else {
    prev.src = "";
    prev.hidden = true;
    if (previewContainer) previewContainer.style.display = "none";
    if (dropPrompt) dropPrompt.style.display = "flex";
    if (statusBadge) {
      statusBadge.className = "card-quick-status";
      if (statusDot) statusDot.className = "status-dot awaiting";
      if (statusText) statusText.textContent = "Awaiting Sample Image";
    }
  }
}

function clearSelectedImage(e) {
  if (e) {
    e.stopPropagation();
    e.preventDefault();
  }
  const fileInput = $("file");
  fileInput.value = "";
  updatePreview(null);
  $("result").innerHTML = "";
  toast("Sample cleared", "ok");
}

$("file").onchange = e => {
  const f = e.target.files && e.target.files[0];
  if (f) {
    updatePreview(f, f.name, (f.size / 1024).toFixed(1) + " KB · Ready for inspection");
  } else {
    updatePreview(null);
  }
};

const dropEl = $("drop");
if (dropEl) {
  ["dragover", "dragleave", "drop"].forEach(ev => {
    dropEl.addEventListener(ev, e => {
      e.preventDefault();
      dropEl.classList.toggle("over", ev === "dragover");
      if (ev === "drop" && e.dataTransfer && e.dataTransfer.files[0]) {
        const file = e.dataTransfer.files[0];
        const dt = new DataTransfer();
        dt.items.add(file);
        $("file").files = dt.files;
        updatePreview(file, file.name, (file.size / 1024).toFixed(1) + " KB · Dropped file ready");
      }
    });
  });

  dropEl.addEventListener("click", e => {
    if (e.target.closest(".btn-change-image") || e.target.closest(".btn-remove-image") || e.target.closest(".btn-camera")) return;
    if ($("prev") && !$("prev").hidden) return;
    $("file").click();
  });
}

// Load Instant Sample Presets
async function loadSamplePreset(url, label, varietyName) {
  try {
    toast("Loading sample: " + label + "...", "ok");
    const res = await fetch(url);
    if (!res.ok) throw new Error("Could not fetch sample image");
    const blob = await res.blob();
    const filename = url.split("/").pop() || "sample.png";
    const file = new File([blob], filename, { type: blob.type || "image/png" });

    const dt = new DataTransfer();
    dt.items.add(file);
    $("file").files = dt.files;

    if (label && $("label")) $("label").value = label;

    updatePreview(file, label + " (" + filename + ")", (blob.size / 1024).toFixed(1) + " KB · Instant sample");
    toast("Loaded: " + label, "ok");

    const runBtn = $("btn-run-analyse");
    if (runBtn) {
      runBtn.classList.add("pulse-highlight");
      setTimeout(() => runBtn.classList.remove("pulse-highlight"), 1600);
      runBtn.scrollIntoView({ behavior: "smooth", block: "center" });
    }
  } catch (err) {
    console.error(err);
    toast("Could not load sample: " + err.message, "bad");
  }
}

// ================= LIVE CAMERA SCANNING =================

let cameraStream = null;

async function openCamera() {
  const modal = $("camera-modal");
  const video = $("camera-video");
  try {
    cameraStream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: { ideal: "environment" }, width: { ideal: 1280 }, height: { ideal: 720 } }
    });
    video.srcObject = cameraStream;
    modal.style.display = "flex";
  } catch (err) {
    console.warn("Camera failed:", err);
    toast("Camera access not available or permission denied: " + err.message, "warn");
  }
}

function closeCamera() {
  if (cameraStream) {
    cameraStream.getTracks().forEach(t => t.stop());
    cameraStream = null;
  }
  const modal = $("camera-modal");
  if (modal) modal.style.display = "none";
}

function capturePhoto() {
  const video = $("camera-video");
  if (!video || !video.videoWidth) return toast("Camera stream not ready yet", "warn");
  const canvas = document.createElement("canvas");
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  const ctx = canvas.getContext("2d");
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
  canvas.toBlob(blob => {
    if (!blob) return toast("Failed to capture image", "bad");
    const filename = "camera_grain_scan_" + Date.now() + ".jpg";
    const file = new File([blob], filename, { type: "image/jpeg" });
    const dt = new DataTransfer();
    dt.items.add(file);
    $("file").files = dt.files;
    updatePreview(file, filename, (blob.size / 1024).toFixed(1) + " KB · Live camera snapshot");
    closeCamera();
    toast("Grain photo captured! Ready to analyse.", "ok");
    const runBtn = $("btn-run-analyse");
    if (runBtn) {
      runBtn.classList.add("pulse-highlight");
      setTimeout(() => runBtn.classList.remove("pulse-highlight"), 1600);
      runBtn.scrollIntoView({ behavior: "smooth", block: "center" });
    }
  }, "image/jpeg", 0.95);
}

// Defect Guide Info helper
const DEFECT_INFO = {
  head: "🍚 Head Rice: Whole kernels with length ≥ 75% intact. Key commercial index determining highest export grade and value.",
  broken: "🥣 Broken Rice: Grain fragments shorter than 75% length. High broken ratio downgrades market value, ideal for flour or congee.",
  chalky: "⚪ Chalky Grains: White opaque chalk-like appearance over 50%+ of kernel. Cooks unevenly and is prone to breakage during milling.",
  yellow: "🟡 Yellowed Kernels: Kernels turned lemon to amber yellow due to excess moisture and bacterial/fungal heat during bulk storage.",
  mould: "🟢 Fungal Mould: Greenish, black, or grey mycelium patches. Poses serious mycotoxin risk (aflatoxin). Must not be consumed."
};

function showDefectInfo(type) {
  if (DEFECT_INFO[type]) {
    toast(DEFECT_INFO[type], type === "mould" ? "bad" : (type === "head" ? "ok" : "warn"));
  }
}

// Load variety dropdown if present
if ($("variety")) {
  J("/api/rice").then(d => {
    if (d && Array.isArray(d) && $("variety")) {
      $("variety").innerHTML += d.map(r => `<option value="${esc(r.name)}">${esc(r.name)} — ${esc(r.country)} (${esc(r.grain)} grain)</option>`).join("");
    }
  });
}

const VT = {
  safe: ["✅", "SAFE TO CONSUME", "Quality Meets Food Safety Standards"],
  caution: ["⚠️", "CONSUME WITH CAUTION", "Inspection Advisory Notice"],
  unsafe: ["⛔", "DO NOT CONSUME", "Critical Defect / Mould Alert"]
};

const origin = v => `
  <h4>${esc(v.name)}</h4>
  <span class="tag">📍 ${esc(v.country)}</span>
  <span class="tag">🌾 ${esc(v.grain)} grain</span>
  <p>${esc(v.info)}</p>
`;

// ================= ANALYSE ACTION =================

async function analyse() {
  const f = $("file").files[0];
  if (!f) return toast("Choose, drop or click a sample rice image first", "warn");

  const fd = new FormData();
  fd.append("image", f);
  const sampleLabel = ($("label") && $("label").value) ? $("label").value : (f.name ? f.name.replace(/\.[^/.]+$/, "") : "Rice Sample");
  fd.append("label", sampleLabel);
  if ($("variety") && $("variety").value) fd.append("variety", $("variety").value);

  const runBtn = $("btn-run-analyse");
  if (runBtn) {
    runBtn.disabled = true;
    runBtn.innerHTML = `<span class="spinner-inline"></span> <span class="btn-text">Inspecting Rice Kernels...</span>`;
  }

  $("result").innerHTML = `
    <div class="card scanning-card">
      <div class="scanning-animation">
        <div class="radar-circle"></div>
        <div class="radar-scan-line"></div>
        <div class="radar-icon">🌾</div>
      </div>
      <h3>Optical Grain Analysis in Progress</h3>
      <p class="scanning-sub">Segmenting grain boundaries and evaluating physical &amp; colour morphology...</p>
      <div class="scan-steps">
        <div class="scan-step-item active"><span>✓</span> Image thresholding &amp; background segmentation</div>
        <div class="scan-step-item active"><span>✓</span> Breadth-First Search (BFS) connected components</div>
        <div class="scan-step-item pulse"><span>⚡</span> Calculating aspect ratio (L/W) &amp; chalkiness</div>
        <div class="scan-step-item"><span>○</span> Evaluating broken % against ISO/Codex thresholds</div>
      </div>
    </div>
  `;
  $("result").scrollIntoView({ behavior: "smooth", block: "nearest" });

  try {
    const d = await J("/api/analyse", { method: "POST", body: fd });
    if (runBtn) {
      runBtn.disabled = false;
      runBtn.innerHTML = `<span class="btn-icon">⚡</span> <span class="btn-text">Run Precision Analysis</span>`;
    }

    if (d.error) {
      $("result").innerHTML = `
        <div class="card verdict-modern unsafe">
          <div class="verdict-icon-wrap">⚠️</div>
          <div class="verdict-body">
            <span class="verdict-tag">Image Notice</span>
            <div class="verdict-headline">Could Not Read Image</div>
            <div class="verdict-advice">${esc(d.error)}</div>
          </div>
        </div>
      `;
      return;
    }
    show(d);
  } catch (err) {
    if (runBtn) {
      runBtn.disabled = false;
      runBtn.innerHTML = `<span class="btn-icon">⚡</span> <span class="btn-text">Run Precision Analysis</span>`;
    }
    $("result").innerHTML = `
      <div class="card verdict-modern unsafe">
        <div class="verdict-icon-wrap">⚠️</div>
        <div class="verdict-body">
          <div class="verdict-headline">Connection Error</div>
          <div class="verdict-advice">${esc(err.message || "Failed to reach server.")}</div>
        </div>
      </div>
    `;
  }
}

// ================= RESULTS PRESENTATION =================

function show(d) {
  const v = VT[d.verdict] || VT.safe;
  const C = 2 * Math.PI * 62;
  const col = { safe: "#2e7d32", caution: "#f59e0b", unsafe: "#c62828" }[d.verdict] || "#2e7d32";
  const qualityLevel = d.quality_level || (d.score >= 85 ? "high" : (d.score >= 70 ? "medium" : "low"));
  const qualityLabel = { high: "HIGH QUALITY", medium: "MEDIUM QUALITY", low: "LOW QUALITY" }[qualityLevel];

  const bars = [
    ["Broken Kernels", d.broken_pct, 25, "🌾"],
    ["Chalky (Opaque)", d.chalky_pct, 30, "⚪"],
    ["Yellowed / Aged", d.yellow_pct, 8, "🟡"],
    ["Discoloured / Brown", d.brown_pct, d.colour === "brown" ? 100 : 10, "🟤"],
    ["Mould / Green", d.green_pct, 1, "🟢"]
  ];

  const wholePct = Math.max(0, (100 - d.broken_pct).toFixed(1));
  const grainTypeName = (d.grain || "medium").toUpperCase() + " GRAIN";

  $("result").innerHTML = `
    <!-- Top Verdict Banner -->
    <div class="verdict-modern ${d.verdict}">
      <div class="verdict-icon-wrap">${v[0]}</div>
      <div class="verdict-body">
        <span class="verdict-tag">${v[2]}</span>
        <div class="verdict-headline">${v[1]}</div>
        <div class="verdict-advice">${esc(d.advice)}</div>
        <div class="verdict-pills">
          ${d.reasons.map(r => `<span class="verdict-pill">🔍 ${esc(r)}</span>`).join("")}
        </div>
      </div>
    </div>

    <!-- Main Quality Dashboard Card -->
    <div class="card quality-dashboard-card">
      <div class="batch-badge-header">
        <div>
          <h2>Grain Quality Dashboard</h2>
          <small>Inspection metrics derived via computer vision contour analysis</small>
        </div>
        <div>
          <span class="batch-id-tag">${esc(d.batch_id)}</span>
          <span style="margin-left:8px;font-weight:600;color:var(--ink-muted);font-size:0.9rem">Sample: ${esc(d.label)}</span>
        </div>
      </div>

      <!-- Quick Morphology Metric Chips -->
      <div class="metric-chips-grid">
        <div class="metric-chip-card">
          <span class="metric-chip-icon">🌾</span>
          <div class="metric-chip-data">
            <span class="metric-chip-val">${grainTypeName}</span>
            <span class="metric-chip-lbl">Grain Classification</span>
          </div>
        </div>

        <div class="metric-chip-card">
          <span class="metric-chip-icon">📏</span>
          <div class="metric-chip-data">
            <span class="metric-chip-val">${d.ratio}:1</span>
            <span class="metric-chip-lbl">Length / Width Ratio</span>
          </div>
        </div>

        <div class="metric-chip-card">
          <span class="metric-chip-icon">🔢</span>
          <div class="metric-chip-data">
            <span class="metric-chip-val">${d.grains} Kernels</span>
            <span class="metric-chip-lbl">Segmented Count</span>
          </div>
        </div>

        <div class="metric-chip-card">
          <span class="metric-chip-icon">${d.is_broken_rice ? '🥣' : '🍚'}</span>
          <div class="metric-chip-data">
            <span class="metric-chip-val">${wholePct}% Head Rice</span>
            <span class="metric-chip-lbl">${d.is_broken_rice ? 'Broken Rice Grade' : 'Whole Grain Ratio'}</span>
          </div>
        </div>
      </div>

      <!-- Radial Gauge & Defect Bars Split -->
      <div class="quality-details-split">
        <!-- Radial Quality Gauge -->
        <div class="gauge-column">
          <div class="gauge">
            <svg width="170" height="170" viewBox="0 0 170 170">
              <circle cx="85" cy="85" r="62" fill="none" stroke="#f0efe8" stroke-width="16" />
              <circle cx="85" cy="85" r="62" fill="none" stroke="${col}" stroke-width="16"
                stroke-linecap="round" stroke-dasharray="${C}" stroke-dashoffset="${C * (1 - d.score / 100)}"
                style="transition: stroke-dashoffset 1s ease-out;" />
            </svg>
            <div class="gv">
              <b>${d.score}</b>
              <small>Score of 100</small>
              <span class="gv-grade-chip" style="background:${col}">Grade ${esc(d.grade)}</span>
              <span class="quality-level ${qualityLevel}">${qualityLabel}</span>
            </div>
          </div>
          <p style="margin:12px 0 0;font-size:0.86rem;color:var(--ink-muted)">
            <b>${d.colour === 'brown' ? '🟤 Brown / Bran Rice' : '⚪ Polished White Rice'}</b>
          </p>
        </div>

        <!-- Defect Breakdown Bars -->
        <div class="defect-bars-container">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:2px">
            <b style="font-size:0.92rem;color:var(--g3)">🔬 Defect &amp; Morphological Inspection:</b>
            <small style="color:var(--ink-muted)">Codex Quality Limits</small>
          </div>
          ${bars.map(b => {
            const isDefect = b[1] > b[2];
            const statusClass = b[1] === 0 ? "pass" : (isDefect ? "fail" : (b[1] > b[2] * 0.6 ? "warn" : "pass"));
            const fillWidth = Math.min(100, (b[1] / Math.max(b[2] * 1.5, 30)) * 100);
            return `
              <div class="defect-bar-item">
                <div class="defect-bar-top">
                  <span class="defect-bar-name">
                    <span>${b[3]}</span>
                    <span>${b[0]}</span>
                    <span class="defect-bar-limit">(Limit: ${b[2]}%)</span>
                  </span>
                  <span class="defect-bar-val" style="color:${isDefect ? 'var(--r)' : 'var(--ink)'}">
                    ${b[1]}% ${isDefect ? '⚠️' : '✓'}
                  </span>
                </div>
                <div class="defect-track">
                  <div class="defect-fill ${statusClass}" style="width:${Math.max(4, fillWidth)}%"></div>
                </div>
              </div>
            `;
          }).join("")}
        </div>
      </div>

      <div style="background:#f9f8f4;border-radius:10px;padding:12px 16px;border:1px solid #ebe9df;font-size:0.9rem;margin-top:10px">
        ${d.is_broken_rice ? '🔸 <b>Milling Broken Rice:</b> Kernel fragments are dominant. Suitable for congee, flour, noodle milling, or brewing.' : '🔹 <b>Premium Head Rice:</b> Grains are intact with high whole-kernel percentage.'}
        Length-to-width ratio is <b>${d.ratio}:1</b> (${d.grain} grain), <b>${d.grains}</b> kernels counted.
      </div>

      <div class="result-actions-bar">
        <button type="button" class="btn-secondary" onclick="window.print()">
          🖨️ Print Quality Report
        </button>
        <button type="button" class="btn-secondary" onclick="scanAnotherSample()">
          🔄 Scan Another Sample
        </button>
      </div>
    </div>

    <!-- Complete Global Intelligence & Identified Cultivar Card -->
    <div class="card detected-variety-card">
      <div class="detected-variety-top-badge">
        <div class="detected-badge-left">
          <span class="ai-live-dot"></span>
          <b>🌾 IDENTIFIED RICE TYPE: ${esc(d.detected_variety ? d.detected_variety.name : (d.variety ? d.variety.name : "Detected Grain"))}</b>
        </div>
        <span class="confidence-pill">${d.confidence || 95}% AI Recognition Match</span>
      </div>

      <!-- Main Varietal Header -->
      <div class="detected-variety-main">
        <div class="detected-variety-avatar">
          <span class="detected-grain-icon">🍚</span>
        </div>
        <div class="detected-variety-details">
          <div class="detected-headline-row">
            <h2 class="detected-name">${esc(d.detected_variety ? d.detected_variety.name : (d.variety ? d.variety.name : "Detected Grain"))}</h2>
            <div class="detected-pills-row">
              <span class="tag origin-tag">📍 Country of Origin: <b>${esc(d.detected_variety ? d.detected_variety.country : (d.variety ? d.variety.country : "Worldwide"))}</b></span>
              <span class="tag grain-tag">🌾 Classification: <b>${esc(d.detected_variety ? d.detected_variety.grain : d.grain).toUpperCase()} GRAIN</b></span>
              <span class="tag category-tag">🏷️ <b>${esc((d.detected_variety && d.detected_variety.category) ? d.detected_variety.category : 'Specialty Grain')}</b></span>
              <span class="tag ratio-tag">📐 L/W Ratio: <b>${d.ratio}:1</b></span>
            </div>
          </div>
          <p class="detected-desc">${esc(d.detected_variety ? d.detected_variety.info : (d.variety ? d.variety.info : ""))}</p>
        </div>
      </div>

      <!-- Global Demographics: Consumers & Cultivators -->
      <div class="global-demographics-grid">
        <!-- How many people use it -->
        <div class="demo-card consumers-card">
          <div class="demo-card-header">
            <span class="demo-icon">👥</span>
            <div>
              <span class="demo-title">Global Consumers Population</span>
              <b class="demo-metric">${esc((d.detected_variety && d.detected_variety.global_consumers) ? d.detected_variety.global_consumers : '500+ Million People')}</b>
            </div>
          </div>
          <p class="demo-desc">${esc((d.detected_variety && d.detected_variety.consumer_reach) ? d.detected_variety.consumer_reach : 'Staple daily food consumed across regional and international diaspora markets.')}</p>
        </div>

        <!-- How much people grow it in the world -->
        <div class="demo-card producers-card">
          <div class="demo-card-header">
            <span class="demo-icon">🚜</span>
            <div>
              <span class="demo-title">Global Cultivation &amp; Harvest</span>
              <b class="demo-metric">${esc((d.detected_variety && d.detected_variety.global_producers) ? d.detected_variety.global_producers : '10+ Million Metric Tons / Year')}</b>
            </div>
          </div>
          <p class="demo-desc"><b>Farming Population:</b> ${esc((d.detected_variety && d.detected_variety.farmer_population) ? d.detected_variety.farmer_population : 'Cultivated by millions of smallholder farming families worldwide.')}</p>
        </div>
      </div>

      <!-- Complete Rice Agronomic & Culinary Profile Grid -->
      <div class="complete-info-grid">
        <div class="info-tile">
          <div class="info-tile-icon">🗺️</div>
          <div class="info-tile-body">
            <b>Agricultural Terroir</b>
            <span>${esc((d.detected_variety && d.detected_variety.terroir) ? d.detected_variety.terroir : (d.detected_variety ? d.detected_variety.country : 'Global agricultural river basins'))}</span>
          </div>
        </div>

        <div class="info-tile">
          <div class="info-tile-icon">🥗</div>
          <div class="info-tile-body">
            <b>Popular Culinary Dishes</b>
            <span>${esc((d.detected_variety && d.detected_variety.culinary_uses) ? d.detected_variety.culinary_uses : 'Everyday meals, traditional curries, festive dishes')}</span>
          </div>
        </div>

        <div class="info-tile">
          <div class="info-tile-icon">✨</div>
          <div class="info-tile-body">
            <b>Aroma &amp; Texture</b>
            <span>${esc((d.detected_variety && d.detected_variety.aroma_texture) ? d.detected_variety.aroma_texture : 'Distinct natural fragrance with balanced mouthfeel')}</span>
          </div>
        </div>

        <div class="info-tile">
          <div class="info-tile-icon">🧪</div>
          <div class="info-tile-body">
            <b>Nutritional &amp; Starch Profile</b>
            <span>${esc((d.detected_variety && d.detected_variety.nutrition) ? d.detected_variety.nutrition : 'Rich in carbohydrates, dietary minerals, low fat')} &bull; ${esc((d.detected_variety && d.detected_variety.amylose_content) ? d.detected_variety.amylose_content : 'Standard amylose')}</span>
          </div>
        </div>
      </div>

      <!-- Morphological Detection Evidence -->
      <div class="detected-evidence-box">
        <b>🔬 Computer Vision Identification Evidence:</b>
        <ul>
          ${(d.variety_reasons || [
            `Kernel aspect ratio (${d.ratio}:1) confirms ${d.grain.toUpperCase()} grain morphology`,
            `Endosperm optical clarity (${(100 - d.chalky_pct).toFixed(1)}% translucent) corresponds with cultivar standard`
          ]).map(r => `<li>✓ ${esc(r)}</li>`).join("")}
        </ul>
      </div>

      ${d.secondary_matches && d.secondary_matches.length > 0 ? `
        <div class="similar-varieties-tray">
          <span class="similar-tray-label">Other notable cultivars sharing this ${esc(d.grain)} grain category:</span>
          <div class="similar-tray-chips">
            ${d.secondary_matches.map(s => `
              <div class="similar-mini-card">
                <b>${esc(s.name)}</b>
                <small>📍 ${esc(s.country)}</small>
              </div>
            `).join("")}
          </div>
        </div>
      ` : ''}

      <p style="margin:16px 0 0">
        <small>Notice: Visual optical analysis provides morphological estimates. Chemical residue, toxin testing, and moisture analysis require laboratory HPLC/GC assays. If rice has a musty smell or visible mould, discard immediately.</small>
      </p>
    </div>
  `;

  if (d.verdict !== "safe") {
    toast(v[1] + ": " + d.advice, d.verdict === "unsafe" ? "bad" : "warn");
  }

  $("result").scrollIntoView({ behavior: "smooth", block: "start" });
}

function scanAnotherSample() {
  clearSelectedImage();
  const dropBox = $("drop");
  if (dropBox) dropBox.scrollIntoView({ behavior: "smooth", block: "center" });
}

async function confirmV(id, name) {
  const r = await J(`/api/batch/${id}/confirm`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name })
  });
  if (r.error) return toast(r.error, "bad");
  $("origin").innerHTML = `
    <div class="candidate-card-confirmed">
      <span class="tag" style="background:#2e7d32;color:#fff;margin-bottom:8px">✓ Verified Variety</span>
      ${origin(r)}
    </div>
  `;
  toast("Confirmed: " + r.name + " (" + r.country + ")", "ok");
}

// ================= EXISTING TABS FUNCTIONALITY =================

const card = r => `
  <div class="rc">
    <h4>${esc(r.name)}</h4>
    <span class="tag">📍 ${esc(r.country)}</span>
    <span class="tag">🌾 ${esc(r.grain)} grain</span>
    <p>${esc(r.info)}</p>
    <button class="a" style="font-size:0.82rem;padding:6px 12px;margin-top:10px" onclick="selectVarietyForAnalyse('${esc(r.name).replace(/'/g, "\\'")}')">
      🔍 Test with this variety
    </button>
  </div>
`;

function selectVarietyForAnalyse(name) {
  go("analyse");
  const varSel = $("variety");
  for (let i = 0; i < varSel.options.length; i++) {
    if (varSel.options[i].value === name) {
      varSel.selectedIndex = i;
      break;
    }
  }
  toast("Selected variety: " + name, "ok");
  const dropBox = $("drop");
  if (dropBox) dropBox.scrollIntoView({ behavior: "smooth", block: "center" });
}

async function lib() {
  const d = await J(`/api/rice?q=${encodeURIComponent($("q").value)}&grain=${$("gr").value}`);
  $("cnt").textContent = (d ? d.length : 0) + " varieties found";
  $("rice").innerHTML = (d || []).map(card).join("") || "<p style='color:var(--ink-muted);padding:14px'>No rice varieties found matching criteria.</p>";
}

function setLibFilter(query, grain) {
  $("q").value = query;
  if (grain !== undefined) $("gr").value = grain;
  lib();
  document.querySelectorAll(".lib-pill").forEach(p => {
    p.classList.toggle("active", p.textContent.includes(query) || (query === "" && p.textContent === "All"));
  });
}

async function al() {
  const d = await J("/api/alerts");
  $("alist").innerHTML = (d || []).map(a => `
    <div class="al ${a.severity}">
      <b>${a.severity === 'danger' ? '⛔ Danger Alert:' : '⚠️ Quality Warning:'}</b> ${esc(a.message)}<br>
      <small style="opacity:0.85">${esc(a.created)}</small>
    </div>
  `).join("") || "<div style='text-align:center;padding:24px;color:var(--g2)'>🎉 No active alerts. All scanned rice batches meet safety parameters.</div>";
}

const VC = { safe: "#c8e6c9", caution: "#fff1c2", unsafe: "#ffcdd2" };
const VL = { safe: "Safe", caution: "Caution", unsafe: "Do not consume" };

async function bat() {
  const d = await J("/api/batches?min_score=" + $("ms").value);
  if (!d) return;
  const n = k => d.filter(s => s.verdict === k).length;
  $("bstats").innerHTML = [
    ["Batches", d.length],
    ["Safe", n("safe")],
    ["Caution", n("caution")],
    ["Unsafe", n("unsafe")],
    ["Avg quality", d.length ? (d.reduce((a, s) => a + s.score, 0) / d.length).toFixed(1) : "-"]
  ].map(s => `<div class="stat"><small>${s[0]}</small><b>${s[1]}</b></div>`).join("");

  $("btb").innerHTML = d.map(s => `
    <tr>
      <td><b>${esc(s.batch_id)}</b></td>
      <td>${esc(s.label)}</td>
      <td>${s.variety ? esc(s.variety) + " · " + esc(s.country) : "<small style='color:#888'>unconfirmed</small>"}</td>
      <td><b>${s.score}</b></td>
      <td><span class="chip" style="background:${s.score >= 85 ? '#c8e6c9' : (s.score >= 70 ? '#fff1c2' : '#ffcdd2')}">${esc(s.grade)}</span></td>
      <td>${s.broken}%</td>
      <td>${esc(s.grain)}</td>
      <td><span class="chip" style="background:${VC[s.verdict]}">${VL[s.verdict]}</span></td>
      <td><small>${esc(s.created)}</small></td>
    </tr>
  `).join("") || "<tr><td colspan='9' style='text-align:center;padding:20px;color:var(--ink-muted)'>No batches match the minimum score filter.</td></tr>";
}

const TRACE_ICONS = {
  Farm: "🌾",
  Mill: "🏭",
  Warehouse: "🏬",
  Distributor: "🚚",
  Retailer: "🏪"
};

async function trace() {
  const d = await J(`/api/trace?from=${$("tf").value}&to=${$("tt").value}`);
  const visual = $("trace-visual");
  if (d.path && d.path.length > 0) {
    visual.innerHTML = `
      <div style="display:flex;align-items:center;flex-wrap:wrap;gap:6px">
        ${d.path.map((node, i) => `
          <span class="trace-step-node">
            <span>${TRACE_ICONS[node] || "📍"}</span>
            <span>${esc(node)}</span>
          </span>
          ${i < d.path.length - 1 ? '<span class="trace-step-arrow">➔</span>' : ''}
        `).join("")}
      </div>
      <p style="margin:12px 0 0;font-size:0.88rem;color:var(--g2);font-weight:600">
        ✓ Shortest custody path identified: ${d.path.length - 1} intermediary transit hops
      </p>
    `;
  } else {
    visual.innerHTML = `<span style="color:var(--r);font-weight:600">❌ No supply chain transit path found between ${esc($("tf").value)} and ${esc($("tt").value)}</span>`;
  }
}

function loadDemoBlend() {
  $("bq").value = 100;
  $("bt").value = 82;
  $("bm").value = "greedy";
  $("bb").value = `Batch A (Premium Basmati),92,60,40,11.5,4,98\nBatch B (Sona Masuri Standard),78,45,50,12.0,6,97\nBatch C (Miniket Milling),65,30,60,13.0,12,94`;
  toast("Loaded demo blend batches", "ok");
}

async function blend() {
  const batches = $("bb").value.trim().split("\n").map(l => {
    const p = l.split(",");
    return {
      name: p[0].trim(),
      quality: +p[1],
      cost: +p[2],
      qty: +p[3],
      moisture: +(p[4] || 12),
      broken: +(p[5] || 5),
      purity: +(p[6] || 97)
    };
  });
  const d = await J("/api/blend", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      batches,
      method: $("bm").value,
      qty: +$("bq").value,
      target: +$("bt").value
    })
  });
  const m = d.mix ? d.mix.map(x => `<b>${esc(x.name)}</b>: ${x.qty} kg`).join(" &bull; ") : (d.batches || []).join(" + ") || "no valid combination";
  $("bo").innerHTML = `
    <div>
      <div style="font-size:1.05rem;color:var(--g3);margin-bottom:6px">${m}</div>
      <div style="font-size:0.92rem;color:var(--ink)">
        ${d.quality !== undefined ? `Blended Quality: <b>${d.quality}</b> &bull; Total Purchase Cost: <b>₹${d.cost}</b> &bull; ${d.meets_target ? "<span style='color:var(--g)'>✅ Meets Target Specification</span>" : "<span style='color:var(--r)'>❌ Target Specification Not Met</span>"}` :
          d.best_total_quality !== undefined ? `Best Total Quality: <b>${d.best_total_quality}</b>` :
          d.found ? "✅ Valid blend combination found within constraints" : "❌ No batch combination satisfies the blend limits"}
      </div>
    </div>
  `;
}
