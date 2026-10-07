#!/usr/bin/env python3
"""Build index.html (single-page site) from the chapter sources in chapters/.

Run:  python build.py
Every chapter file is embedded COMPLETELY and UNCHANGED inside index.html (in an inert
<template>) and rendered inside its own isolated frame, so each chapter keeps its own
scripts, styles, ids and routing without interfering with the others.
"""
import io, os, re, html, json

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "chapters")
OUT = os.path.join(ROOT, "index.html")

CHAPTERS = [
    ("chapter0.html", "Introduction", "AC Systems & Reactive Components",
     "Prerequisites for everything that follows: function graphs and calculus refreshers, single-, two- and three-phase voltages, Y and Δ relations, and the behaviour of resistors, inductors and capacitors — including why sudden switching produces current and voltage spikes."),
    ("chapter1.html", "Chapter 1", "Introduction to Machinery Principles",
     "Rotation and power, Ampère's law from a single wire to a toroid, Faraday's law and self-inductance, force on a wire, the moving conductor, the linear DC machine, AC power, and a full treatment of magnetic circuits."),
    ("chapter2.html", "Chapter 2", "Transformers",
     "Ideal and real transformers, the equivalent circuit built from the primary side with winding-to-circuit correspondence, voltage regulation and efficiency with live phasor diagrams, taps, autotransformers, three-phase banks, ratings and instrument transformers."),
    ("chapter3.html", "Chapter 3", "AC Machinery Fundamentals",
     "The rotating magnetic field from single-, two- and three-phase windings with animated 2-pole winding diagrams, MMF and flux distribution, induced voltage and torque, insulation, power flow and losses."),
    ("chapter4.html", "Chapter 4", "Synchronous Machines",
     "Generators and motors: phasor diagrams, power-angle curves, terminal characteristics, open- and short-circuit tests, droop and capability curves, V-curves, power-factor correction and starting."),
    ("chapter5.html", "Chapter 5", "Induction Motors",
     "Slip, the equivalent circuit, power flow, the torque–speed characteristic from the Thévenin model, NEMA designs, starting and parameter tests."),
    ("chapter6.html", "Chapter 6", "DC Machines",
     "The parts of a DC machine and how they work together, commutation, E_A = Kφω and τ = KφI_A, armature reaction, motor torque–speed curves, speed control, and generator characteristics and voltage build-up."),
    ("chapter7.html", "Chapter 7", "Single-Phase & Special Motors",
     "Universal motors, the double-revolving-field theory, starting methods, reluctance, hysteresis, brushless DC and stepper motors."),
]

SEC_RE = re.compile(r"section\('([^']+)','((?:[^'\\]|\\.)*)','((?:[^'\\]|\\.)*)'")

# Injected into every chapter: (a) chapterN.html links scroll the parent to that chapter,
# (b) the parent can ask the chapter to open one of its sections (table of contents).
BRIDGE = """<script>
document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[href]');if(!a)return;var m=(a.getAttribute('href')||'').match(/^chapter(\\d)\\.html$/);if(m){e.preventDefault();try{parent.postMessage({emfGo:+m[1]},'*');}catch(_){}}},true);
window.addEventListener('message',function(e){var d=e.data||{};if(d.emfSection&&typeof render==='function'){try{render(d.emfSection);}catch(_){}}});
</script>
"""

def load():
    out = []
    for i, (fn, num, title, blurb) in enumerate(CHAPTERS):
        s = io.open(os.path.join(SRC, fn), encoding="utf-8").read()
        assert "</template" not in s, fn
        secs = [(sid, html.unescape(lab.replace("\\'", "'"))) for sid, _grp, lab in SEC_RE.findall(s)]
        body = re.sub(r"^\s*<!doctype html>\s*", "", s, flags=re.I).replace("<head>", "<head>\n" + BRIDGE, 1)
        out.append(dict(i=i, fn=fn, num=num, title=title, blurb=blurb, secs=secs, body=body))
    return out

CSS = """
:root{--navy:#0b2a5b;--blue:#1d4ed8;--blue2:#2563eb;--sky:#e8f0fe;--sky2:#f4f7fd;--ink:#172033;--muted:#5b6b85;--line:#dbe3f0;--white:#fff}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:var(--white);color:var(--ink);font:16px/1.65 "Segoe UI",system-ui,-apple-system,Arial,sans-serif}
h1,h2,h3{font-family:Georgia,"Times New Roman",serif;color:var(--navy);margin:0 0 .4em;line-height:1.2}
a{color:var(--blue)}
.wrap{max-width:1180px;margin:0 auto;padding:0 20px}
/* fixed navigation */
.nav{position:fixed;top:0;left:0;right:0;z-index:50;background:rgba(255,255,255,.96);backdrop-filter:blur(8px);border-bottom:1px solid var(--line);box-shadow:0 2px 12px rgba(11,42,91,.06)}
.nav .wrap{display:flex;align-items:center;gap:14px;height:64px}
.brand{display:flex;align-items:center;gap:10px;text-decoration:none;color:var(--navy);font-family:Georgia,serif;font-weight:700;font-size:18px;white-space:nowrap;min-width:0}
.brand>span{overflow:hidden;text-overflow:ellipsis}
@media(max-width:700px){.brand{font-size:15px}.brand small{display:none}.brand .mark{width:30px;height:30px;font-size:16px}}
.brand .mark{width:34px;height:34px;border-radius:9px;background:linear-gradient(135deg,var(--navy),var(--blue2));color:#fff;display:grid;place-items:center;font-size:18px}
.brand small{display:block;font:12px/1.2 "Segoe UI",system-ui,sans-serif;color:var(--muted);font-weight:400}
.links{display:flex;gap:4px;margin-left:auto;list-style:none;padding:0;margin-top:0;margin-bottom:0}
.links a{display:block;padding:8px 11px;border-radius:8px;color:var(--ink);text-decoration:none;font-size:14px;font-weight:600;white-space:nowrap}
.links a:hover{background:var(--sky)}.links a.on{background:var(--blue);color:#fff}
.burger{display:none;margin-left:auto;background:none;border:1px solid var(--line);border-radius:8px;width:42px;height:38px;cursor:pointer;color:var(--navy);font-size:20px}
@media(max-width:1000px){.burger{display:block}.links{display:none;position:absolute;left:0;right:0;top:64px;background:#fff;border-bottom:1px solid var(--line);flex-direction:column;padding:8px 16px 14px;box-shadow:0 12px 24px rgba(11,42,91,.08)}.links.open{display:flex}.links a{padding:11px 12px;font-size:15px}}
/* landing */
.hero{padding:124px 0 56px;background:linear-gradient(180deg,var(--sky2) 0%,#fff 100%);border-bottom:1px solid var(--line)}
.hero .kicker{color:var(--blue);font-weight:700;letter-spacing:.08em;text-transform:uppercase;font-size:12px}
.hero h1{font-size:clamp(32px,4.6vw,52px);margin:8px 0 10px}
.hero p.lead{font-size:18px;color:var(--muted);max-width:820px;margin:0 0 22px}
.hero .meta{display:flex;flex-wrap:wrap;gap:10px 22px;color:var(--muted);font-size:14px;margin-bottom:26px}
.btn{display:inline-block;background:var(--blue);color:#fff;text-decoration:none;padding:12px 20px;border-radius:10px;font-weight:600;border:1px solid var(--blue)}
.btn.ghost{background:#fff;color:var(--blue)}
.btn+.btn{margin-left:10px}
/* chapter cards */
.section-head{display:flex;align-items:baseline;gap:14px;margin:48px 0 18px}.section-head h2{font-size:28px}.section-head p{color:var(--muted);margin:0}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(270px,1fr));gap:18px}
.cardc{background:#fff;border:1px solid var(--line);border-radius:14px;padding:20px 20px 18px;display:flex;flex-direction:column;gap:8px;box-shadow:0 1px 2px rgba(11,42,91,.04);transition:transform .15s,box-shadow .15s}
.cardc:hover{transform:translateY(-2px);box-shadow:0 10px 24px rgba(11,42,91,.10)}
.cardc .num{font-size:12px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--blue)}
.cardc h3{font-size:20px;margin:0}.cardc p{margin:0;color:var(--muted);font-size:14.5px;flex:1}
.cardc .foot{display:flex;justify-content:space-between;align-items:center;font-size:13px;color:var(--muted);margin-top:6px}
.cardc .foot a{font-weight:600;text-decoration:none}
/* table of contents */
.toc{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px 28px}
.toc details{border:1px solid var(--line);border-radius:12px;padding:0;background:#fff;overflow:hidden}
.toc summary{cursor:pointer;padding:12px 16px;font-weight:700;color:var(--navy);background:var(--sky2);list-style:none;display:flex;justify-content:space-between}
.toc summary::after{content:"+";color:var(--blue);font-weight:700}.toc details[open] summary::after{content:"–"}
.toc ol{margin:0;padding:10px 16px 12px 34px;font-size:14px}.toc li{padding:3px 0}.toc li a{text-decoration:none;color:var(--ink)}.toc li a:hover{color:var(--blue);text-decoration:underline}
/* chapter sections */
.chapter{scroll-margin-top:76px;padding:48px 0 12px;border-top:1px solid var(--line)}
.chapter .head{display:flex;flex-wrap:wrap;align-items:flex-end;gap:12px 20px;margin-bottom:14px}
.chapter .head .num{color:var(--blue);font-weight:700;letter-spacing:.08em;text-transform:uppercase;font-size:12px;display:block}
.chapter .head h2{font-size:30px;margin:0}
.chapter .head .tools{margin-left:auto;display:flex;gap:8px;flex-wrap:wrap}
.chapter .head .tools a,.chapter .head .tools button{font:600 13px "Segoe UI",system-ui,sans-serif;color:var(--blue);background:#fff;border:1px solid var(--line);border-radius:8px;padding:7px 11px;text-decoration:none;cursor:pointer}
.chapter .desc{color:var(--muted);max-width:900px;margin:0 0 16px}
.lab{position:relative;border:1px solid var(--line);border-radius:14px;overflow:hidden;background:#0f1220;height:min(900px,88vh);min-height:560px;box-shadow:0 12px 32px rgba(11,42,91,.12)}
.lab iframe{position:absolute;inset:0;width:100%;height:100%;border:0;background:#0f1220}
.lab .ph{position:absolute;inset:0;display:grid;place-items:center;color:#9aa3c4;font-size:15px}
@media(max-width:700px){.lab{height:80vh;min-height:480px}.hero{padding-top:100px}}
/* footer + back to top */
footer{margin-top:56px;padding:28px 0 40px;border-top:1px solid var(--line);color:var(--muted);font-size:14px}
#top{position:fixed;right:18px;bottom:18px;z-index:40;width:46px;height:46px;border-radius:50%;border:0;background:var(--blue);color:#fff;font-size:20px;cursor:pointer;box-shadow:0 8px 20px rgba(29,78,216,.35);opacity:0;pointer-events:none;transition:opacity .2s}
#top.show{opacity:1;pointer-events:auto}
"""

JS = """
(function(){
  var N=%(n)d,frames={},pending={},sections=[].slice.call(document.querySelectorAll('section.chapter'));
  function mount(i){if(frames[i])return frames[i];var box=document.getElementById('lab'+i),f=document.createElement('iframe');f.title=box.dataset.title;f.loading='eager';
    f.addEventListener('load',function(){var ph=box.querySelector('.ph');if(ph)ph.remove();if(pending[i]){try{f.contentWindow.postMessage({emfSection:pending[i]},'*');}catch(_){ }delete pending[i];}});
    f.srcdoc=document.getElementById('tpl'+i).innerHTML;box.appendChild(f);frames[i]=f;return f;}
  function openSection(i,sid){var f=mount(i);if(sid){pending[i]=sid;try{f.contentWindow.postMessage({emfSection:sid},'*');}catch(_){ }}}
  // lazy-load each chapter frame as it approaches the viewport
  if('IntersectionObserver' in window){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){mount(+e.target.dataset.i);io.unobserve(e.target);}});},{rootMargin:'600px 0px'});
    sections.forEach(function(s){io.observe(s);});}else{sections.forEach(function(s){mount(+s.dataset.i);});}
  // table-of-contents deep links: data-ch + data-sec
  document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[data-ch]');if(!a)return;var i=+a.dataset.ch,sid=a.dataset.sec;openSection(i,sid);
    var links=document.getElementById('links');if(links)links.classList.remove('open');});
  // chapter → chapter links coming from inside a frame
  window.addEventListener('message',function(e){var d=e.data||{};if(typeof d.emfGo==='number'){var s=document.getElementById('chapter'+d.emfGo);if(s){mount(d.emfGo);s.scrollIntoView({behavior:'smooth'});}}});
  // mobile navigation
  var burger=document.getElementById('burger'),links=document.getElementById('links');
  burger.onclick=function(){links.classList.toggle('open');};
  links.addEventListener('click',function(e){if(e.target.tagName==='A')links.classList.remove('open');});
  // active link + back-to-top
  var navLinks=[].slice.call(links.querySelectorAll('a[href^="#chapter"]')),top=document.getElementById('top');
  function onScroll(){var y=window.scrollY;top.classList.toggle('show',y>600);var cur=null;sections.forEach(function(s){if(s.getBoundingClientRect().top<=90)cur=s.id;});navLinks.forEach(function(a){a.classList.toggle('on',a.getAttribute('href')==='#'+cur);});}
  window.addEventListener('scroll',onScroll,{passive:true});onScroll();
  top.onclick=function(){window.scrollTo({top:0,behavior:'smooth'});};
  // "reload chapter" tool
  document.querySelectorAll('button[data-reload]').forEach(function(b){b.onclick=function(){var i=+b.dataset.reload;if(frames[i]){frames[i].remove();delete frames[i];}mount(i);};});
  // deep link: index.html#chapter2 (section) — frame is mounted by the observer once scrolled into view
  if(location.hash){var t=document.querySelector(location.hash);if(t&&t.classList.contains('chapter'))mount(+t.dataset.i);}
})();
"""

def build():
    ch = load()
    e = html.escape
    nav = "".join(f'<li><a href="#chapter{c["i"]}">{e(c["num"] if c["i"] else "Intro")}</a></li>' for c in ch)
    cards = "".join(f'''
      <article class="cardc">
        <span class="num">{e(c["num"])}</span>
        <h3>{e(c["title"])}</h3>
        <p>{e(c["blurb"])}</p>
        <div class="foot"><span>{len(c["secs"])} interactive sections</span><a href="#chapter{c["i"]}" data-ch="{c["i"]}">Open →</a></div>
      </article>''' for c in ch)
    toc = "".join(f'''
      <details{" open" if c["i"]==0 else ""}>
        <summary>{e(c["num"])} · {e(c["title"])}</summary>
        <ol>{"".join(f'<li><a href="#chapter{c["i"]}" data-ch="{c["i"]}" data-sec="{e(sid)}">{e(lab)}</a></li>' for sid,lab in c["secs"])}</ol>
      </details>''' for c in ch)
    secs = "".join(f'''
  <section class="chapter" id="chapter{c["i"]}" data-i="{c["i"]}">
    <div class="wrap">
      <div class="head">
        <div><span class="num">{e(c["num"])}</span><h2>{e(c["title"])}</h2></div>
        <div class="tools"><a href="chapters/{c["fn"]}" target="_blank" rel="noopener">Open full screen ↗</a><button type="button" data-reload="{c["i"]}">Reset chapter</button></div>
      </div>
      <p class="desc">{e(c["blurb"])}</p>
      <div class="lab" id="lab{c["i"]}" data-title="{e(c["num"] + " — " + c["title"])}"><div class="ph">Loading {e(c["num"].lower() if c["i"] else "the introduction")}…</div></div>
    </div>
  </section>''' for c in ch)
    templates = "".join(f'<template id="tpl{c["i"]}">\n{c["body"]}\n</template>\n' for c in ch)
    total = sum(len(c["secs"]) for c in ch)
    page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Electric Machinery Fundamentals — Interactive Course</title>
<meta name="description" content="An interactive, single-page course on Electric Machinery Fundamentals (Chapman, 4th ed.): transformers, AC and DC machines, with live simulations, phasor diagrams and derivations.">
<meta name="theme-color" content="#0b2a5b">
<style>{CSS}</style>
</head>
<body>
<header class="nav">
  <div class="wrap">
    <a class="brand" href="#home"><span class="mark">⚡</span><span>Electric Machinery Fundamentals<small>Interactive course · Chapman, 4th ed.</small></span></a>
    <button class="burger" id="burger" aria-label="Menu" aria-controls="links">☰</button>
    <ul class="links" id="links"><li><a href="#contents">Contents</a></li>{nav}</ul>
  </div>
</header>

<section class="hero" id="home">
  <div class="wrap">
    <div class="kicker">University of Engineering &amp; Technology · Electrical Machines</div>
    <h1>Electric Machinery Fundamentals</h1>
    <p class="lead">An interactive companion to Chapman's <em>Electric Machinery Fundamentals</em> (4th ed.): eight chapters of live simulations, animated phasor diagrams, step-by-step derivations and worked examples — every equation you can derive, every number you can change.</p>
    <div class="meta"><span>📚 {len(ch)} chapters · {total} interactive sections</span><span>👨‍🏫 Dr. Muhammad Salim Butt</span><span>✉ <a href="mailto:salimbutt@uet.edu.pk">salimbutt@uet.edu.pk</a></span><span>⚙ Runs entirely in the browser — no installation</span></div>
    <a class="btn" href="#chapter0" data-ch="0">Start with the Introduction</a><a class="btn ghost" href="#contents">Table of contents</a>
  </div>
</section>

<main>
  <div class="wrap">
    <div class="section-head"><h2>Chapters</h2><p>Each chapter is a complete interactive lab. Open it below or in its own full-screen window.</p></div>
    <div class="cards">{cards}
    </div>
    <div class="section-head" id="contents" style="scroll-margin-top:76px"><h2>Table of contents</h2><p>Click any topic to jump straight to it.</p></div>
    <div class="toc">{toc}
    </div>
  </div>
{secs}
</main>

<footer><div class="wrap">© Dr. Muhammad Salim Butt · University of Engineering &amp; Technology · Built as a teaching aid for <em>Electric Machinery Fundamentals</em> (S. J. Chapman). Each chapter also opens stand-alone from the <code>chapters/</code> folder.</div></footer>
<button id="top" aria-label="Back to top">↑</button>

{templates}
<script>{JS % {"n": len(ch)}}</script>
</body>
</html>
'''
    io.open(OUT, "w", encoding="utf-8", newline="").write(page)
    print(f"index.html written: {len(page.encode('utf-8'))/1024:.0f} KB, {len(ch)} chapters, {total} sections")

if __name__ == "__main__":
    build()
