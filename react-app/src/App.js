import { useState, useEffect, useRef } from "react";

const API_BASE = "http://localhost:8000";

const css = `
  @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Serif+Display&display=swap');
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  :root {
    --bg:#f4f6fb; --white:#ffffff; --border:#e2e8f4; --border2:#cbd5e8;
    --accent:#2563eb; --accent2:#0ea5e9; --green:#16a34a; --orange:#ea580c; --danger:#dc2626;
    --text:#0f172a; --muted:#64748b; --light:#f8fafc;
    --fh:'DM Serif Display',serif; --fm:'DM Sans',sans-serif;
    --shadow:0 1px 3px rgba(0,0,0,.08),0 4px 16px rgba(0,0,0,.04);
    --shadow-lg:0 4px 24px rgba(0,0,0,.10);
  }
  html{scroll-behavior:smooth;}
  body{background:var(--bg);color:var(--text);font-family:var(--fm);min-height:100vh;}

  /* HEADER */
  .header{background:var(--white);border-bottom:1px solid var(--border);padding:0 40px;display:flex;align-items:center;justify-content:space-between;height:64px;position:sticky;top:0;z-index:100;box-shadow:0 1px 8px rgba(0,0,0,.06);}
  .header-left{display:flex;align-items:center;gap:12px;}
  .logo{width:38px;height:38px;border-radius:10px;background:linear-gradient(135deg,var(--accent),var(--accent2));display:flex;align-items:center;justify-content:center;color:white;font-weight:700;font-size:14px;box-shadow:0 2px 8px rgba(37,99,235,.3);}
  .h-title{font-family:var(--fh);font-size:20px;} .h-title span{color:var(--accent);}
  .h-sub{font-size:11px;color:var(--muted);margin-top:1px;}
  .h-badge{font-size:11px;padding:4px 12px;border-radius:20px;background:#eff6ff;color:var(--accent);border:1px solid #bfdbfe;font-weight:500;}

  /* STATUS */
  .status-bar{background:var(--white);border-bottom:1px solid var(--border);padding:10px 40px;display:flex;gap:24px;align-items:center;font-size:12px;flex-wrap:wrap;}
  .s-item{display:flex;align-items:center;gap:7px;}
  .dot{width:7px;height:7px;border-radius:50%;flex-shrink:0;}
  .dot-on{background:var(--green);box-shadow:0 0 5px rgba(22,163,74,.4);animation:blink 2s infinite;}
  .dot-off{background:var(--danger);} .dot-check{background:#cbd5e1;}
  @keyframes blink{0%,100%{opacity:1}50%{opacity:.4}}
  .s-lbl{color:var(--muted);} .s-val{font-weight:600;}
  .rbtn{margin-left:auto;background:none;border:1px solid var(--border2);color:var(--muted);font-family:var(--fm);font-size:11px;padding:5px 12px;border-radius:6px;cursor:pointer;transition:all .2s;}
  .rbtn:hover{border-color:var(--accent);color:var(--accent);}

  /* LAYOUT */
  .wrap{max-width:1400px;margin:0 auto;padding:32px 40px 80px;}

  /* TABS */
  .tabs{display:flex;gap:2px;margin-bottom:28px;background:var(--white);border:1px solid var(--border);border-radius:10px;padding:4px;width:fit-content;box-shadow:var(--shadow);}
  .tab{padding:9px 22px;border-radius:7px;border:none;background:transparent;color:var(--muted);font-family:var(--fm);font-size:13px;font-weight:500;cursor:pointer;transition:all .18s;}
  .tab-active{background:var(--accent);color:white;font-weight:600;}
  .tab:hover:not(.tab-active){color:var(--text);background:var(--bg);}

  /* CARDS */
  .card{background:var(--white);border:1px solid var(--border);border-radius:14px;box-shadow:var(--shadow);}
  .card-head{padding:16px 22px;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:10px;}
  .card-icon{width:32px;height:32px;border-radius:8px;background:#eff6ff;display:flex;align-items:center;justify-content:center;font-size:15px;flex-shrink:0;}
  .card-title{font-weight:600;font-size:14px;} .card-sub{font-size:12px;color:var(--muted);margin-top:1px;}
  .card-body{padding:22px;}

  /* PREDICT */
  .predict-grid{display:grid;grid-template-columns:1fr 360px;gap:20px;align-items:start;}
  @media(max-width:960px){.predict-grid{grid-template-columns:1fr;}}
  .sec{font-size:11px;font-weight:600;letter-spacing:1px;text-transform:uppercase;color:var(--accent);margin:20px 0 12px;display:flex;align-items:center;gap:8px;}
  .sec:first-child{margin-top:0;}
  .sec::after{content:'';flex:1;height:1px;background:var(--border);}
  .fg2{display:grid;grid-template-columns:1fr 1fr;gap:10px;}
  .fg3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;}
  .field{display:flex;flex-direction:column;gap:5px;}
  .field label{font-size:11px;font-weight:500;color:var(--muted);}
  .field input,.field select{background:var(--light);border:1px solid var(--border);border-radius:8px;color:var(--text);font-family:var(--fm);font-size:13px;padding:9px 12px;outline:none;width:100%;transition:border-color .18s,box-shadow .18s;}
  .field input:focus,.field select:focus{border-color:var(--accent);box-shadow:0 0 0 3px rgba(37,99,235,.1);background:white;}
  .btn{width:100%;margin-top:20px;padding:14px;background:linear-gradient(135deg,var(--accent),var(--accent2));color:white;border:none;border-radius:10px;font-family:var(--fm);font-size:14px;font-weight:600;cursor:pointer;transition:all .2s;box-shadow:0 4px 12px rgba(37,99,235,.3);}
  .btn:hover:not(:disabled){transform:translateY(-1px);box-shadow:0 6px 20px rgba(37,99,235,.4);}
  .btn:disabled{opacity:.5;cursor:not-allowed;transform:none;box-shadow:none;}
  .btn-load{background:var(--bg);color:var(--accent);border:2px solid var(--accent);box-shadow:none;}
  .r-stack{display:flex;flex-direction:column;gap:16px;}
  .r-card{background:var(--white);border:1px solid var(--border);border-radius:14px;overflow:hidden;box-shadow:var(--shadow);transition:border-color .3s,box-shadow .3s;}
  .r-card-on{border-color:var(--accent);box-shadow:0 0 0 3px rgba(37,99,235,.08);}
  .r-head{padding:12px 18px;border-bottom:1px solid var(--border);background:var(--light);display:flex;align-items:center;justify-content:space-between;}
  .r-title{font-size:11px;font-weight:600;color:var(--muted);letter-spacing:.5px;text-transform:uppercase;}
  .r-body{padding:20px;}
  .big{font-family:var(--fh);font-size:52px;color:var(--accent);line-height:1;}
  .big-u{font-size:18px;color:var(--muted);font-weight:400;margin-left:3px;font-family:var(--fm);}
  .big-s{font-size:11px;color:var(--muted);margin-top:6px;}
  .cbadge{display:inline-flex;align-items:center;gap:6px;padding:6px 14px;border-radius:20px;font-size:13px;font-weight:600;}
  .cb-developed{background:#f0fdf4;color:var(--green);border:1px solid #bbf7d0;}
  .cb-developing{background:#fff7ed;color:var(--orange);border:1px solid #fed7aa;}
  .cb-emerging{background:#eff6ff;color:var(--accent);border:1px solid #bfdbfe;}
  .proba-list{margin-top:14px;display:flex;flex-direction:column;gap:10px;}
  .proba-row{display:flex;justify-content:space-between;font-size:12px;margin-bottom:4px;}
  .pname{color:var(--muted);font-weight:500;}
  .bar-bg{height:6px;background:var(--border);border-radius:3px;overflow:hidden;}
  .bar{height:100%;border-radius:3px;transition:width 1s cubic-bezier(.16,1,.3,1);}
  .bar-developed{background:var(--green);} .bar-developing{background:var(--orange);} .bar-emerging{background:var(--accent);}
  .empty{padding:36px 20px;text-align:center;color:var(--muted);}
  .empty-i{font-size:32px;margin-bottom:10px;opacity:.3;} .empty-t{font-size:13px;line-height:1.8;}
  .loader{display:flex;gap:6px;align-items:center;justify-content:center;padding:24px;}
  .ld{width:7px;height:7px;border-radius:50%;background:var(--accent);animation:ld .8s infinite;}
  .ld:nth-child(2){animation-delay:.15s} .ld:nth-child(3){animation-delay:.3s}
  @keyframes ld{0%,80%,100%{transform:scale(.5);opacity:.2}40%{transform:scale(1);opacity:1}}
  .err{background:#fef2f2;border:1px solid #fecaca;border-radius:8px;padding:12px 16px;color:var(--danger);font-size:12px;margin-top:12px;display:flex;gap:8px;}
  .note{font-size:11px;color:var(--muted);margin-top:16px;padding:10px 14px;background:#eff6ff;border-left:3px solid var(--accent);border-radius:0 6px 6px 0;line-height:1.7;}

  /* HISTORY */
  .stats-row{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:20px;}
  @media(max-width:800px){.stats-row{grid-template-columns:1fr 1fr;}}
  .stat-card{background:var(--white);border:1px solid var(--border);border-radius:12px;padding:18px;box-shadow:var(--shadow);}
  .stat-label{font-size:11px;color:var(--muted);font-weight:500;margin-bottom:8px;}
  .stat-val{font-family:var(--fh);font-size:30px;color:var(--text);line-height:1;}
  .stat-val span{font-size:14px;font-family:var(--fm);color:var(--muted);font-weight:400;}
  .history-charts{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:20px;}
  @media(max-width:900px){.history-charts{grid-template-columns:1fr;}}

  /* MAP */
  .map-wrap{position:relative;overflow:hidden;border-radius:0 0 14px 14px;}
  .map-img{width:100%;height:240px;object-fit:cover;display:block;filter:saturate(0.7) brightness(1.05);}
  .map-overlay{position:absolute;inset:0;background:linear-gradient(180deg,rgba(37,99,235,.04) 0%,rgba(37,99,235,.12) 100%);pointer-events:none;}
  .map-pins{position:absolute;inset:0;}
  .map-pin{position:absolute;transform:translate(-50%,-100%);display:flex;flex-direction:column;align-items:center;cursor:pointer;animation:pinDrop .4s ease;}
  @keyframes pinDrop{from{transform:translate(-50%,-120%);opacity:0}to{transform:translate(-50%,-100%);opacity:1}}
  .pin-dot{width:11px;height:11px;border-radius:50%;border:2px solid white;box-shadow:0 2px 6px rgba(0,0,0,.3);}
  .pin-label{background:white;border-radius:5px;padding:2px 6px;font-size:10px;font-weight:600;white-space:nowrap;box-shadow:0 2px 8px rgba(0,0,0,.15);margin-bottom:3px;color:var(--text);}
  .pin-developed{background:var(--green);} .pin-developing{background:var(--orange);} .pin-emerging{background:var(--accent);}
  .map-legend{position:absolute;bottom:10px;left:10px;background:rgba(255,255,255,.92);border-radius:8px;padding:7px 12px;display:flex;gap:12px;font-size:11px;backdrop-filter:blur(4px);box-shadow:var(--shadow);}
  .leg-item{display:flex;align-items:center;gap:5px;font-weight:500;}
  .leg-dot{width:8px;height:8px;border-radius:50%;}
  .map-tooltip{position:absolute;top:8px;right:8px;background:white;border-radius:10px;padding:12px 16px;box-shadow:var(--shadow-lg);font-size:12px;min-width:160px;border:1px solid var(--border);z-index:10;}

  /* DETAIL MODAL */
  .modal-overlay{position:fixed;inset:0;background:rgba(0,0,0,.4);z-index:200;display:flex;align-items:center;justify-content:center;padding:20px;backdrop-filter:blur(2px);}
  .modal{background:var(--white);border-radius:16px;max-width:800px;width:100%;max-height:85vh;overflow:auto;box-shadow:var(--shadow-lg);}
  .modal-head{padding:20px 24px;border-bottom:1px solid var(--border);display:flex;align-items:center;justify-content:space-between;position:sticky;top:0;background:var(--white);z-index:1;}
  .modal-title{font-family:var(--fh);font-size:20px;}
  .modal-close{background:none;border:none;font-size:20px;cursor:pointer;color:var(--muted);width:32px;height:32px;border-radius:6px;display:flex;align-items:center;justify-content:center;}
  .modal-close:hover{background:var(--bg);}
  .modal-body{padding:24px;}
  .params-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:20px;}
  @media(max-width:600px){.params-grid{grid-template-columns:1fr 1fr;}}
  .param-item{background:var(--light);border:1px solid var(--border);border-radius:8px;padding:10px 12px;}
  .param-label{font-size:10px;color:var(--muted);font-weight:500;text-transform:uppercase;letter-spacing:.5px;margin-bottom:4px;}
  .param-val{font-size:14px;font-weight:600;color:var(--text);}
  .param-cat{background:#eff6ff;border-color:#bfdbfe;}
  .param-cat .param-val{color:var(--accent);}

  /* TABLE */
  .hist-table-wrap{overflow:auto;border-radius:0 0 14px 14px;}
  table{width:100%;border-collapse:collapse;font-size:13px;}
  thead th{background:var(--light);padding:11px 16px;text-align:left;font-size:11px;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:.5px;border-bottom:1px solid var(--border);position:sticky;top:0;white-space:nowrap;}
  tbody td{padding:11px 16px;border-bottom:1px solid var(--border);}
  tbody tr:last-child td{border-bottom:none;}
  tbody tr:hover td{background:#f8faff;cursor:pointer;}
  .td-le{color:var(--accent);font-weight:700;font-size:15px;}
  .td-time{color:var(--muted);font-size:11px;}
  .clear-btn{background:none;border:1px solid #fecaca;color:var(--danger);font-family:var(--fm);font-size:12px;padding:6px 14px;border-radius:7px;cursor:pointer;transition:all .2s;}
  .clear-btn:hover{background:#fef2f2;}
  .view-btn{background:none;border:1px solid var(--border2);color:var(--muted);font-family:var(--fm);font-size:11px;padding:4px 10px;border-radius:6px;cursor:pointer;transition:all .2s;}
  .view-btn:hover{border-color:var(--accent);color:var(--accent);}

  /* BATCH */
  .upload-zone{border:2px dashed var(--border2);border-radius:12px;padding:48px 28px;text-align:center;cursor:pointer;position:relative;transition:all .2s;background:var(--light);}
  .upload-zone:hover,.upload-drag{border-color:var(--accent);background:#eff6ff;}
  .upload-zone input{position:absolute;inset:0;opacity:0;cursor:pointer;width:100%;height:100%;}
  .up-i{font-size:36px;margin-bottom:12px;} .up-t{font-size:13px;color:var(--muted);line-height:1.8;} .up-f{color:var(--accent);font-weight:600;margin-top:8px;}
  .tbl-wrap{border:1px solid var(--border);border-radius:10px;overflow:auto;max-height:400px;}
  .ca{color:var(--accent);font-weight:700;} .cg{color:var(--green);font-weight:600;} .co{color:var(--orange);font-weight:600;}
  .dlbtn{background:none;border:1px solid var(--accent);color:var(--accent);font-family:var(--fm);font-size:12px;padding:7px 16px;border-radius:7px;cursor:pointer;font-weight:500;transition:all .2s;}
  .dlbtn:hover{background:#eff6ff;}
  ::-webkit-scrollbar{width:5px;height:5px;}
  ::-webkit-scrollbar-track{background:var(--bg);}
  ::-webkit-scrollbar-thumb{background:var(--border2);border-radius:3px;}
`;

const COORDS = {
  "France":{x:48,y:33},"Allemagne":{x:50,y:30},"Japon":{x:80,y:32},
  "Etats-Unis":{x:20,y:35},"USA":{x:20,y:35},"Tunisie":{x:50,y:40},
  "Maroc":{x:46,y:40},"Bresil":{x:30,y:60},"Chine":{x:74,y:36},
  "Inde":{x:67,y:44},"Nigeria":{x:50,y:52},"Pakistan":{x:64,y:40},
  "Arabie-Saoudite":{x:58,y:42},"Argentine":{x:28,y:72},
  "Afrique-du-Sud":{x:52,y:68},"Ethiopie":{x:55,y:50},
  "Espagne":{x:46,y:34},"Italie":{x:50,y:35},"Canada":{x:22,y:25},
  "Russie":{x:65,y:25},"Mexique":{x:20,y:42},"Egypte":{x:53,y:40},
  "Allemagne":{x:50,y:30},"Royaume-Uni":{x:46,y:29},"Australie":{x:80,y:65},
};

function getCoords(country) {
  if (COORDS[country]) return COORDS[country];
  const key = Object.keys(COORDS).find(k =>
    country.toLowerCase().includes(k.toLowerCase()) || k.toLowerCase().includes(country.toLowerCase())
  );
  return key ? COORDS[key] : null;
}

const PCOLOR = { Developed:"#16a34a", Developing:"#ea580c", Emerging:"#2563eb" };

function bclass(level) {
  if (!level) return "emerging";
  const l = level.toLowerCase();
  if (l==="developed") return "developed";
  if (l==="developing") return "developing";
  return "emerging";
}

// ── UI HELPERS ───────────────────────────────────────────────────────────────
function Loader() { return <div className="loader"><div className="ld"/><div className="ld"/><div className="ld"/></div>; }
function Empty({text}) { return <div className="empty"><div className="empty-i">🌍</div><div className="empty-t">{text}</div></div>; }
function NF({label,val,onChange,step="any"}) { return <div className="field"><label>{label}</label><input type="number" value={val} step={step} onChange={e=>onChange(parseFloat(e.target.value)||0)}/></div>; }
function SF({label,val,onChange,opts}) { return <div className="field"><label>{label}</label><select value={val} onChange={e=>onChange(e.target.value)}>{opts.map(o=><option key={o}>{o}</option>)}</select></div>; }

// ── STATUS BAR ───────────────────────────────────────────────────────────────
function StatusBar({health,onRefresh}) {
  const ok=health?.status==="ok", le=health?.life_expectancy_model_loaded, dl=health?.development_level_model_loaded;
  const dc=b=>health?(b?"dot-on":"dot-off"):"dot-check";
  const vc=b=>health?(b?"var(--green)":"var(--danger)"):"var(--muted)";
  return (
    <div className="status-bar">
      <div className="s-item"><div className={`dot ${dc(ok)}`}/><span className="s-lbl">API</span><span className="s-val" style={{color:vc(ok)}}>{health?(ok?"ONLINE":"DEGRADED"):"Checking..."}</span></div>
      <div className="s-item"><div className={`dot ${dc(le)}`}/><span className="s-lbl">Life Exp. Model</span><span className="s-val" style={{color:vc(le)}}>{health?(le?"Loaded":"Missing"):"—"}</span></div>
      <div className="s-item"><div className={`dot ${dc(dl)}`}/><span className="s-lbl">Dev. Level Model</span><span className="s-val" style={{color:vc(dl)}}>{health?(dl?"Loaded":"Missing"):"—"}</span></div>
      <button className="rbtn" onClick={onRefresh}>↺ Refresh</button>
    </div>
  );
}

// ── LINE CHART ────────────────────────────────────────────────────────────────
function LineChart({history}) {
  const ref = useRef(null);
  useEffect(() => {
    if (!ref.current || history.length===0) return;
    const canvas=ref.current, ctx=canvas.getContext("2d");
    const dpr=window.devicePixelRatio||1;
    const W=canvas.offsetWidth, H=220;
    canvas.width=W*dpr; canvas.height=H*dpr; ctx.scale(dpr,dpr);
    const pad={t:28,r:20,b:48,l:50};
    const cw=W-pad.l-pad.r, ch=H-pad.t-pad.b;
    ctx.clearRect(0,0,W,H);
    const vals=history.map(h=>h.life_expectancy);
    const minV=Math.max(0,Math.min(...vals)-5), maxV=Math.min(100,Math.max(...vals)+5);
    // Grid
    ctx.strokeStyle="#e2e8f4"; ctx.lineWidth=1;
    for(let i=0;i<=4;i++){
      const y=pad.t+(ch/4)*i;
      ctx.beginPath();ctx.moveTo(pad.l,y);ctx.lineTo(pad.l+cw,y);ctx.stroke();
      ctx.fillStyle="#94a3b8";ctx.font="11px DM Sans";ctx.textAlign="right";
      ctx.fillText((maxV-((maxV-minV)/4)*i).toFixed(0),pad.l-6,y+4);
    }
    if(history.length<2){
      const x=pad.l+cw/2,y=pad.t+ch-((vals[0]-minV)/(maxV-minV))*ch;
      ctx.beginPath();ctx.arc(x,y,5,0,Math.PI*2);ctx.fillStyle="#2563eb";ctx.fill();
      return;
    }
    const pts=history.map((h,i)=>({
      x:pad.l+(i/(history.length-1))*cw,
      y:pad.t+ch-((h.life_expectancy-minV)/(maxV-minV))*ch
    }));
    // Gradient fill
    const grad=ctx.createLinearGradient(0,pad.t,0,pad.t+ch);
    grad.addColorStop(0,"rgba(37,99,235,.18)");grad.addColorStop(1,"rgba(37,99,235,0)");
    ctx.beginPath();ctx.moveTo(pts[0].x,pts[0].y);
    for(let i=1;i<pts.length;i++){const cx=(pts[i-1].x+pts[i].x)/2;ctx.bezierCurveTo(cx,pts[i-1].y,cx,pts[i].y,pts[i].x,pts[i].y);}
    ctx.lineTo(pts[pts.length-1].x,pad.t+ch);ctx.lineTo(pts[0].x,pad.t+ch);ctx.closePath();
    ctx.fillStyle=grad;ctx.fill();
    // Line
    ctx.beginPath();ctx.moveTo(pts[0].x,pts[0].y);
    for(let i=1;i<pts.length;i++){const cx=(pts[i-1].x+pts[i].x)/2;ctx.bezierCurveTo(cx,pts[i-1].y,cx,pts[i].y,pts[i].x,pts[i].y);}
    ctx.strokeStyle="#2563eb";ctx.lineWidth=2.5;ctx.stroke();
    // Dots + labels
    pts.forEach((p,i)=>{
      ctx.beginPath();ctx.arc(p.x,p.y,5,0,Math.PI*2);ctx.fillStyle="white";ctx.fill();ctx.strokeStyle="#2563eb";ctx.lineWidth=2;ctx.stroke();
      ctx.fillStyle="#0f172a";ctx.font="bold 10px DM Sans";ctx.textAlign="center";
      ctx.fillText(history[i].life_expectancy,p.x,p.y-10);
      ctx.fillStyle="#94a3b8";ctx.font="10px DM Sans";
      ctx.fillText(history[i].country.substring(0,7),p.x,pad.t+ch+18);
    });
  },[history]);
  return <canvas ref={ref} style={{width:"100%",height:"220px"}}/>;
}

// ── BAR CHART ─────────────────────────────────────────────────────────────────
function BarChart({history}) {
  const counts={Developed:0,Developing:0,Emerging:0};
  history.forEach(h=>{if(counts[h.dev_level]!==undefined)counts[h.dev_level]++;});
  const total=history.length||1;
  return (
    <div style={{display:"flex",flexDirection:"column",gap:16,padding:"4px 0"}}>
      {[
        {label:"Developed", val:counts.Developed, color:"#16a34a",bg:"#f0fdf4"},
        {label:"Developing",val:counts.Developing,color:"#ea580c",bg:"#fff7ed"},
        {label:"Emerging",  val:counts.Emerging,  color:"#2563eb",bg:"#eff6ff"},
      ].map(b=>(
        <div key={b.label}>
          <div style={{display:"flex",justifyContent:"space-between",fontSize:12,marginBottom:7}}>
            <span style={{fontWeight:600,color:b.color}}>{b.label}</span>
            <span style={{color:"var(--muted)"}}>{b.val} pays · {((b.val/total)*100).toFixed(0)}%</span>
          </div>
          <div style={{height:12,background:b.bg,borderRadius:6,overflow:"hidden",border:`1px solid ${b.color}30`}}>
            <div style={{height:"100%",width:`${(b.val/total)*100}%`,background:b.color,borderRadius:6,transition:"width 1s cubic-bezier(.16,1,.3,1)"}}/>
          </div>
        </div>
      ))}
    </div>
  );
}

// ── WORLD MAP ─────────────────────────────────────────────────────────────────
function WorldMap({history}) {
  const [tooltip,setTooltip]=useState(null);
  return (
    <div className="card">
      <div className="card-head">
        <div className="card-icon">🗺️</div>
        <div><div className="card-title">Carte des prédictions</div><div className="card-sub">{history.length} pays analysés</div></div>
      </div>
      <div className="map-wrap">
        <img className="map-img"
          src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/World_map_-_low_resolution.svg/1280px-World_map_-_low_resolution.svg.png"
          alt="World Map"
          onError={e=>{e.target.src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/Blue_Marble_2002.png/1280px-Blue_Marble_2002.png";}}
        />
        <div className="map-overlay"/>
        <div className="map-pins">
          {history.map((h,i)=>{
            const c=getCoords(h.country);
            if(!c) return null;
            return (
              <div key={i} className="map-pin" style={{left:`${c.x}%`,top:`${c.y}%`}}
                onMouseEnter={()=>setTooltip(h)} onMouseLeave={()=>setTooltip(null)}>
                <div className="pin-label">{h.country}</div>
                <div className={`pin-dot pin-${bclass(h.dev_level)}`}/>
              </div>
            );
          })}
        </div>
        {tooltip&&(
          <div className="map-tooltip">
            <div style={{fontWeight:700,marginBottom:6}}>{tooltip.country}</div>
            <div style={{color:"var(--accent)",fontWeight:700,fontSize:20,marginBottom:6}}>{tooltip.life_expectancy}<span style={{fontSize:12,color:"var(--muted)",fontWeight:400}}> ans</span></div>
            <span className={`cbadge cb-${bclass(tooltip.dev_level)}`} style={{fontSize:11,padding:"3px 10px"}}>● {tooltip.dev_level}</span>
          </div>
        )}
        <div className="map-legend">
          {[["#16a34a","Developed"],["#ea580c","Developing"],["#2563eb","Emerging"]].map(([c,l])=>(
            <div className="leg-item" key={l}><div className="leg-dot" style={{background:c}}/><span style={{color:"var(--text)"}}>{l}</span></div>
          ))}
        </div>
      </div>
    </div>
  );
}

// ── DETAIL MODAL ──────────────────────────────────────────────────────────────
function DetailModal({entry, onClose}) {
  if (!entry) return null;
  const p = entry.params;
  const numParams = [
    {label:"World Rank",val:p.Rank},{label:"Population",val:p.Population.toLocaleString()},
    {label:"GDP Rank",val:p.GDP_Rank},{label:"GDP (millions $)",val:p.GDP_USD_millions.toLocaleString()},
    {label:"GDP (billions $)",val:p.GDP_USD_billions},{label:"GDP per Capita",val:p.GDP_per_Capita.toLocaleString()},
    {label:"Life Exp. Male",val:`${p.Life_Expectancy_Male} ans`},{label:"Life Exp. Female",val:`${p.Life_Expectancy_Female} ans`},
    {label:"Gender Gap",val:`${p.Life_Expectancy_Gender_Gap} ans`},{label:"Life Exp. Overall",val:`${p.Life_Expectancy} ans`},
    {label:"Log(Population)",val:p.Log_Population},{label:"Log(GDP)",val:p.Log_GDP},
    {label:"Log(GDP/Capita)",val:p.Log_GDP_per_Capita},{label:"Wealth Score",val:p.Wealth_Score},
  ];
  const catParams = [
    {label:"Population Category",val:p.Population_Category},
    {label:"GDP Category",val:p.GDP_Category},
    {label:"Development Level",val:p.Development_Level},
  ];
  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={e=>e.stopPropagation()}>
        <div className="modal-head">
          <div>
            <div className="modal-title">🌍 {entry.country}</div>
            <div style={{fontSize:12,color:"var(--muted)",marginTop:4}}>{entry.date} à {entry.time}</div>
          </div>
          <button className="modal-close" onClick={onClose}>✕</button>
        </div>
        <div className="modal-body">
          {/* Result summary */}
          <div style={{display:"flex",gap:16,marginBottom:24,flexWrap:"wrap"}}>
            <div style={{background:"#eff6ff",border:"1px solid #bfdbfe",borderRadius:12,padding:"16px 24px",flex:1,minWidth:140}}>
              <div style={{fontSize:11,color:"var(--muted)",fontWeight:500,marginBottom:4}}>LIFE EXPECTANCY PRÉDITE</div>
              <div style={{fontFamily:"var(--fh)",fontSize:38,color:"var(--accent)",lineHeight:1}}>{entry.life_expectancy}<span style={{fontSize:16,fontFamily:"var(--fm)",color:"var(--muted)",fontWeight:400}}> ans</span></div>
            </div>
            <div style={{background:bclass(entry.dev_level)==="developed"?"#f0fdf4":bclass(entry.dev_level)==="developing"?"#fff7ed":"#eff6ff",border:`1px solid ${bclass(entry.dev_level)==="developed"?"#bbf7d0":bclass(entry.dev_level)==="developing"?"#fed7aa":"#bfdbfe"}`,borderRadius:12,padding:"16px 24px",flex:1,minWidth:140}}>
              <div style={{fontSize:11,color:"var(--muted)",fontWeight:500,marginBottom:8}}>DEVELOPMENT LEVEL</div>
              <span className={`cbadge cb-${bclass(entry.dev_level)}`} style={{fontSize:15}}>● {entry.dev_level}</span>
              {entry.probas&&<div style={{marginTop:8,fontSize:12,color:"var(--muted)"}}>Confiance : <strong style={{color:PCOLOR[entry.dev_level]||"var(--accent)"}}>{(Math.max(...Object.values(entry.probas))*100).toFixed(1)}%</strong></div>}
            </div>
          </div>

          {/* Probabilities */}
          {entry.probas&&(
            <div style={{marginBottom:24}}>
              <div style={{fontSize:12,fontWeight:600,color:"var(--muted)",textTransform:"uppercase",letterSpacing:1,marginBottom:12}}>Probabilités par classe</div>
              <div style={{display:"flex",flexDirection:"column",gap:10}}>
                {Object.entries(entry.probas).map(([c,prob])=>(
                  <div key={c}>
                    <div style={{display:"flex",justifyContent:"space-between",fontSize:12,marginBottom:4}}>
                      <span style={{fontWeight:600,color:PCOLOR[c]||"var(--accent)"}}>{c}</span>
                      <span style={{fontWeight:700,color:PCOLOR[c]||"var(--accent)"}}>{(prob*100).toFixed(1)}%</span>
                    </div>
                    <div className="bar-bg"><div className={`bar bar-${bclass(c)}`} style={{width:`${prob*100}%`}}/></div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Numerical params */}
          <div style={{fontSize:12,fontWeight:600,color:"var(--muted)",textTransform:"uppercase",letterSpacing:1,marginBottom:12}}>Paramètres numériques saisis</div>
          <div className="params-grid" style={{marginBottom:20}}>
            {numParams.map(({label,val})=>(
              <div className="param-item" key={label}>
                <div className="param-label">{label}</div>
                <div className="param-val">{val}</div>
              </div>
            ))}
          </div>

          {/* Categorical params */}
          <div style={{fontSize:12,fontWeight:600,color:"var(--muted)",textTransform:"uppercase",letterSpacing:1,marginBottom:12}}>Paramètres catégoriels saisis</div>
          <div className="params-grid">
            {catParams.map(({label,val})=>(
              <div className="param-item param-cat" key={label}>
                <div className="param-label">{label}</div>
                <div className="param-val">{val}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

// ── PREDICT TAB ───────────────────────────────────────────────────────────────
const DEFAULT={
  Rank:50,Population:50000000,GDP_Rank:40,GDP_USD_millions:500000,
  GDP_USD_billions:500,Life_Expectancy_Male:72,Life_Expectancy_Female:76,
  GDP_per_Capita:10000,Log_Population:17.7,Log_GDP:13.1,Log_GDP_per_Capita:9.2,
  Life_Expectancy_Gender_Gap:4,Wealth_Score:0.0003,Life_Expectancy:74,
  Population_Category:"Very Large",GDP_Category:"High",Development_Level:"Emerging",
};

function PredictTab({onResult}) {
  const [country,setCountry]=useState("");
  const [form,setForm]=useState(DEFAULT);
  const [result,setResult]=useState(null);
  const [loading,setLoading]=useState(false);
  const [error,setError]=useState(null);
  const set=k=>v=>setForm(f=>({...f,[k]:v}));

  const submit=async()=>{
    setLoading(true);setError(null);setResult(null);
    try{
      const res=await fetch(`${API_BASE}/predict`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(form)});
      if(!res.ok){const d=await res.json();throw new Error(d.detail||`HTTP ${res.status}`);}
      const data=await res.json();
      setResult(data);
      onResult({
        country:country||"Pays inconnu",
        life_expectancy:data.life_expectancy_prediction,
        dev_level:data.development_level_prediction,
        probas:data.development_level_probabilities,
        params:{...form},
        time:new Date().toLocaleTimeString("fr-FR"),
        date:new Date().toLocaleDateString("fr-FR"),
      });
    }catch(e){setError(e.message);}
    finally{setLoading(false);}
  };

  const cls=result?bclass(result.development_level_prediction):"";
  const probas=result?.development_level_probabilities||{};

  return (
    <div className="predict-grid">
      <div className="card">
        <div className="card-head">
          <div className="card-icon">🌍</div>
          <div><div className="card-title">Paramètres du pays</div><div className="card-sub">Données socio-économiques</div></div>
        </div>
        <div className="card-body">
          <div style={{marginBottom:16}}>
            <div className="field">
              <label>Nom du pays</label>
              <input type="text" placeholder="Ex: Tunisie, France, Brésil..." value={country} onChange={e=>setCountry(e.target.value)} style={{fontSize:15,fontWeight:600}}/>
            </div>
          </div>
          <div className="sec">Démographique &amp; Économique</div>
          <div className="fg2">
            <NF label="World Rank" val={form.Rank} onChange={set("Rank")}/>
            <NF label="Population" val={form.Population} onChange={set("Population")}/>
            <NF label="GDP Rank" val={form.GDP_Rank} onChange={set("GDP_Rank")}/>
            <NF label="GDP (millions $)" val={form.GDP_USD_millions} onChange={set("GDP_USD_millions")}/>
            <NF label="GDP (billions $)" val={form.GDP_USD_billions} onChange={set("GDP_USD_billions")}/>
            <NF label="GDP per Capita" val={form.GDP_per_Capita} onChange={set("GDP_per_Capita")}/>
          </div>
          <div className="sec">Espérance de vie</div>
          <div className="fg2">
            <NF label="Life Exp. Male" val={form.Life_Expectancy_Male} onChange={set("Life_Expectancy_Male")} step="0.1"/>
            <NF label="Life Exp. Female" val={form.Life_Expectancy_Female} onChange={set("Life_Expectancy_Female")} step="0.1"/>
            <NF label="Gender Gap (ans)" val={form.Life_Expectancy_Gender_Gap} onChange={set("Life_Expectancy_Gender_Gap")} step="0.1"/>
            <NF label="Life Exp. Overall" val={form.Life_Expectancy} onChange={set("Life_Expectancy")} step="0.1"/>
          </div>
          <div className="sec">Features dérivées</div>
          <div className="fg2">
            <NF label="Log(Population)" val={form.Log_Population} onChange={set("Log_Population")} step="0.01"/>
            <NF label="Log(GDP)" val={form.Log_GDP} onChange={set("Log_GDP")} step="0.01"/>
            <NF label="Log(GDP/Capita)" val={form.Log_GDP_per_Capita} onChange={set("Log_GDP_per_Capita")} step="0.01"/>
            <NF label="Wealth Score" val={form.Wealth_Score} onChange={set("Wealth_Score")} step="0.0001"/>
          </div>
          <div className="sec">Catégories</div>
          <div className="fg3">
            <SF label="Population Category" val={form.Population_Category} onChange={set("Population_Category")} opts={["Large","Medium","Small","Very Large"]}/>
            <SF label="GDP Category" val={form.GDP_Category} onChange={set("GDP_Category")} opts={["High","Low","Medium","Very High"]}/>
            <SF label="Development Level" val={form.Development_Level} onChange={set("Development_Level")} opts={["Developed","Developing","Emerging"]}/>
          </div>
          <button className={`btn ${loading?"btn-load":""}`} onClick={submit} disabled={loading}>
            {loading?"Calcul en cours...":"▶ Lancer la prédiction"}
          </button>
          {error&&<div className="err"><span>⚠</span><span>{error}</span></div>}
          <div className="note">💡 Log(x) = ln(x) — Ex: ln(50 000 000) ≈ 17.73</div>
        </div>
      </div>

      <div className="r-stack">
        <div className={`r-card ${result?"r-card-on":""}`}>
          <div className="r-head"><span className="r-title">Life Expectancy</span>{result&&<span style={{fontSize:10,color:"var(--accent)",fontWeight:600}}>RÉGRESSION</span>}</div>
          <div className="r-body">
            {loading&&<Loader/>}
            {!loading&&!result&&<Empty text="Remplissez le formulaire et lancez la prédiction"/>}
            {!loading&&result&&<><div className="big">{result.life_expectancy_prediction}<span className="big-u">ans</span></div><div className="big-s">{country||"Pays"} · Espérance de vie prédite</div></>}
          </div>
        </div>
        <div className={`r-card ${result?"r-card-on":""}`}>
          <div className="r-head"><span className="r-title">Development Level</span>{result&&<span style={{fontSize:10,color:"var(--accent)",fontWeight:600}}>CLASSIFICATION</span>}</div>
          <div className="r-body">
            {loading&&<Loader/>}
            {!loading&&!result&&<Empty text="En attente"/>}
            {!loading&&result&&<>
              <span className={`cbadge cb-${cls}`}>● {result.development_level_prediction}</span>
              <div className="proba-list">
                {Object.entries(probas).map(([c,p])=>(
                  <div key={c}>
                    <div className="proba-row"><span className="pname">{c}</span><span style={{fontWeight:700,color:PCOLOR[c]||"var(--accent)"}}>{(p*100).toFixed(1)}%</span></div>
                    <div className="bar-bg"><div className={`bar bar-${bclass(c)}`} style={{width:`${p*100}%`}}/></div>
                  </div>
                ))}
              </div>
            </>}
          </div>
        </div>
      </div>
    </div>
  );
}

// ── HISTORY TAB ───────────────────────────────────────────────────────────────
function HistoryTab({history,onClear}) {
  const [selected,setSelected]=useState(null);

  if(history.length===0) return (
    <div className="card" style={{textAlign:"center",padding:60}}>
      <div style={{fontSize:48,marginBottom:16}}>📊</div>
      <div style={{fontSize:16,fontWeight:600,marginBottom:8}}>Aucune prédiction encore</div>
      <div style={{color:"var(--muted)",fontSize:13}}>Allez sur <strong>Prédiction</strong>, entrez le nom du pays et lancez la prédiction.</div>
    </div>
  );

  const avgLE=(history.reduce((a,h)=>a+h.life_expectancy,0)/history.length).toFixed(1);
  const maxLE=Math.max(...history.map(h=>h.life_expectancy));
  const devCount=history.filter(h=>h.dev_level==="Developed").length;

  return (
    <div>
      {selected&&<DetailModal entry={selected} onClose={()=>setSelected(null)}/>}

      {/* Stats */}
      <div className="stats-row">
        <div className="stat-card"><div className="stat-label">Pays testés</div><div className="stat-val">{history.length}<span> pays</span></div></div>
        <div className="stat-card"><div className="stat-label">Life Exp. moyenne</div><div className="stat-val">{avgLE}<span> ans</span></div></div>
        <div className="stat-card"><div className="stat-label">Life Exp. max</div><div className="stat-val">{maxLE}<span> ans</span></div></div>
        <div className="stat-card"><div className="stat-label">Pays Developed</div><div className="stat-val">{devCount}<span>/{history.length}</span></div></div>
      </div>

      {/* Map + Bar chart */}
      <div className="history-charts">
        <WorldMap history={history}/>
        <div className="card">
          <div className="card-head"><div className="card-icon">📊</div><div><div className="card-title">Distribution — Development Level</div><div className="card-sub">{history.length} prédictions</div></div></div>
          <div className="card-body"><BarChart history={history}/></div>
        </div>
      </div>

      {/* Line chart */}
      <div className="card" style={{marginBottom:20}}>
        <div className="card-head"><div className="card-icon">📈</div><div><div className="card-title">Courbe — Life Expectancy</div><div className="card-sub">Évolution par prédiction</div></div></div>
        <div className="card-body"><LineChart history={history}/></div>
      </div>

      {/* History table */}
      <div className="card">
        <div className="card-head">
          <div className="card-icon">📋</div>
          <div style={{flex:1}}><div className="card-title">Historique complet</div><div className="card-sub">Cliquez sur une ligne pour voir tous les paramètres</div></div>
          <button className="clear-btn" onClick={onClear}>🗑 Effacer tout</button>
        </div>
        <div className="hist-table-wrap">
          <table>
            <thead>
              <tr>
                <th>#</th><th>Pays</th><th>Life Expectancy</th><th>Development Level</th>
                <th>Confiance</th><th>Population</th><th>GDP (Md$)</th>
                <th>GDP/Capita</th><th>Date</th><th>Heure</th><th></th>
              </tr>
            </thead>
            <tbody>
              {[...history].reverse().map((h,i)=>(
                <tr key={i} onClick={()=>setSelected(h)} title="Cliquez pour voir tous les paramètres">
                  <td style={{color:"var(--muted)",fontSize:12}}>{history.length-i}</td>
                  <td style={{fontWeight:600}}>{h.country}</td>
                  <td className="td-le">{h.life_expectancy} ans</td>
                  <td><span className={`cbadge cb-${bclass(h.dev_level)}`} style={{fontSize:12,padding:"3px 10px"}}>● {h.dev_level}</span></td>
                  <td style={{fontSize:12,color:PCOLOR[h.dev_level]||"var(--accent)",fontWeight:600}}>
                    {h.probas?`${(Math.max(...Object.values(h.probas))*100).toFixed(1)}%`:"—"}
                  </td>
                  <td style={{fontSize:12,color:"var(--muted)"}}>{h.params?.Population?.toLocaleString()||"—"}</td>
                  <td style={{fontSize:12,color:"var(--muted)"}}>{h.params?.GDP_USD_billions||"—"}</td>
                  <td style={{fontSize:12,color:"var(--muted)"}}>{h.params?.GDP_per_Capita?.toLocaleString()||"—"}</td>
                  <td className="td-time">{h.date}</td>
                  <td className="td-time">{h.time}</td>
                  <td><button className="view-btn" onClick={e=>{e.stopPropagation();setSelected(h);}}>👁 Détails</button></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

// ── BATCH TAB ─────────────────────────────────────────────────────────────────
function BatchTab() {
  const [file,setFile]=useState(null),[drag,setDrag]=useState(false);
  const [loading,setLoading]=useState(false),[results,setResults]=useState(null),[error,setError]=useState(null);
  const handleFile=f=>{if(!f)return;if(!f.name.endsWith(".csv")){setError("CSV requis.");return;}setFile(f);setError(null);setResults(null);};
  const submit=async()=>{
    setLoading(true);setError(null);
    const fd=new FormData();fd.append("file",file);
    try{const res=await fetch(`${API_BASE}/predict_batch`,{method:"POST",body:fd});if(!res.ok){const d=await res.json();throw new Error(d.detail||`HTTP ${res.status}`);}setResults(await res.json());}
    catch(e){setError(e.message);}finally{setLoading(false);}
  };
  const cols=results?.length?["Country","Life_Expectancy_Prediction","Development_Level_Prediction","Dev_Prob_Developed","Dev_Prob_Developing","Dev_Prob_Emerging"].filter(c=>c in results[0]):[];
  const download=()=>{const ks=Object.keys(results[0]);const csv=[ks.join(","),...results.map(r=>ks.map(k=>JSON.stringify(r[k]??'')).join(","))].join("\n");const a=document.createElement("a");a.href="data:text/csv;charset=utf-8,"+encodeURIComponent(csv);a.download="predictions.csv";a.click();};
  return (
    <div>
      <div className="card">
        <div className="card-head"><div className="card-icon">📂</div><div><div className="card-title">Prédiction en lot — CSV</div><div className="card-sub">Uploadez un CSV avec plusieurs pays</div></div></div>
        <div className="card-body">
          <div className={`upload-zone ${drag?"upload-drag":""}`} onDragOver={e=>{e.preventDefault();setDrag(true);}} onDragLeave={()=>setDrag(false)} onDrop={e=>{e.preventDefault();setDrag(false);handleFile(e.dataTransfer.files[0]);}}>
            <input type="file" accept=".csv" onChange={e=>handleFile(e.target.files[0])}/>
            <div className="up-i">📄</div>
            <div className="up-t">Glissez votre CSV ici ou cliquez</div>
            {file&&<div className="up-f">✅ {file.name}</div>}
          </div>
          {error&&<div className="err"><span>⚠</span><span>{error}</span></div>}
          <button className={`btn ${loading?"btn-load":""}`} onClick={submit} disabled={!file||loading}>{loading?"Traitement...":"▶ Lancer le batch"}</button>
          <div className="note">📋 Colonnes : Rank, Population, GDP_Rank, GDP_USD_millions, GDP_USD_billions, Life_Expectancy, Life_Expectancy_Male, Life_Expectancy_Female, GDP_per_Capita, Log_Population, Log_GDP, Log_GDP_per_Capita, Life_Expectancy_Gender_Gap, Wealth_Score, Population_Category, GDP_Category, Development_Level</div>
        </div>
      </div>
      {results&&<>
        <div style={{display:"flex",alignItems:"center",justifyContent:"space-between",margin:"24px 0 12px"}}>
          <div style={{fontWeight:600,fontSize:14}}>Résultats — <span style={{color:"var(--accent)"}}>{results.length} pays</span></div>
          <button className="dlbtn" onClick={download}>⬇ Télécharger CSV</button>
        </div>
        <div className="tbl-wrap">
          <table>
            <thead><tr>{cols.map(c=><th key={c}>{c.replace(/_/g," ")}</th>)}</tr></thead>
            <tbody>{results.map((r,i)=><tr key={i}>{cols.map(c=>{let cl="";if(c==="Life_Expectancy_Prediction")cl="ca";else if(c==="Development_Level_Prediction")cl=r[c]==="Developed"?"cg":r[c]==="Developing"?"co":"ca";return<td key={c} className={cl}>{r[c]??"—"}</td>;})}
            </tr>)}</tbody>
          </table>
        </div>
      </>}
    </div>
  );
}

// ── APP ───────────────────────────────────────────────────────────────────────
export default function App() {
  const [tab,setTab]=useState("predict");
  const [health,setHealth]=useState(null);
  const [history,setHistory]=useState([]);

  const checkHealth=async()=>{
    setHealth(null);
    try{const r=await fetch(`${API_BASE}/health`);setHealth(await r.json());}
    catch{setHealth({status:"error",life_expectancy_model_loaded:false,development_level_model_loaded:false});}
  };

  useEffect(()=>{checkHealth();},[]);

  const TABS=[
    {id:"predict",label:"🌍 Prédiction"},
    {id:"history",label:`📊 Historique${history.length>0?` (${history.length})`:""}` },
    {id:"batch",  label:"📂 Batch CSV"},
  ];

  return (
    <>
      <style>{css}</style>
      <div className="header">
        <div className="header-left">
          <div className="logo">ML</div>
          <div><div className="h-title">World <span>Prediction</span> API</div><div className="h-sub">Wikipedia Socio-Economic Pipeline</div></div>
        </div>
        <div className="h-badge">v1.0.0 · FastAPI</div>
      </div>
      <StatusBar health={health} onRefresh={checkHealth}/>
      <div className="wrap">
        <div className="tabs">
          {TABS.map(t=><button key={t.id} className={`tab ${tab===t.id?"tab-active":""}`} onClick={()=>setTab(t.id)}>{t.label}</button>)}
        </div>
        {tab==="predict"&&<PredictTab onResult={h=>setHistory(prev=>[...prev,h])}/>}
        {tab==="history"&&<HistoryTab history={history} onClear={()=>setHistory([])}/>}
        {tab==="batch"  &&<BatchTab/>}
      </div>
    </>
  );
}
