// ─── PAGE TRANSITION SYSTEM ────────────────────────────────
// Spinner-ring overlay: dark backdrop + thin gradient circle spinner
// (matches the 2nd animation in the reference grid).

(function () {
  'use strict';

  // ── Grab elements from native DOM ────────────────────────
  const overlay = document.getElementById('page-overlay');
  const spinner = document.getElementById('page-spinner');
  const bar = document.getElementById('nav-bar');

  // If elements aren't present in HTML, bail out to avoid errors
  if (!overlay || !spinner || !bar) return;

  function showSpinner() {
    spinner.style.opacity = '1';
  }
  function hideSpinner() {
    spinner.style.opacity = '0';
  }

  function startBar() {
    bar.style.opacity = '1';
    bar.style.width = '70%';
  }
  function finishBar() {
    bar.style.width = '100%';
    setTimeout(() => { bar.style.opacity = '0'; bar.style.width = '0%'; }, 350);
  }

  // ── Fade overlay + spinner out after page paints ─────────
  window.addEventListener('pageshow', function () {
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        overlay.style.opacity = '0';
        hideSpinner();
        finishBar();
      });
    });
  });

  // ── Intercept link clicks ────────────────────────────────
  document.addEventListener('click', function (e) {
    const link = e.target.closest('a[href]');
    if (!link) return;

    const href = link.getAttribute('href');

    // Skip: anchors, external, new-tab, download, special-protocols
    if (
      !href ||
      href.startsWith('#') ||
      href.startsWith('mailto:') ||
      href.startsWith('tel:') ||
      href.startsWith('javascript:') ||
      link.target === '_blank' ||
      link.hasAttribute('download') ||
      link.hostname !== window.location.hostname
    ) return;

    e.preventDefault();

    startBar();
    showSpinner();

    // Fade overlay in, then navigate
    overlay.style.transition = 'opacity 0.2s ease';
    overlay.style.opacity = '1';

    setTimeout(() => {
      window.location.href = href;
    }, 450);
  });

  // ── Form submit: show bar ────────────────────────────────
  document.addEventListener('submit', function (e) {
    // If another script (like AJAX chat) already prevented default, don't show loader
    if (e.defaultPrevented) return;

    const form = e.target;
    if (form.method && form.method.toLowerCase() !== 'dialog') {
      startBar();
      showSpinner();
      overlay.style.transition = 'opacity 0.2s ease';
      overlay.style.opacity = '1';
    }
  });

})();

// ─── Sidebar card hover animations (existing) ────────────
document.addEventListener('DOMContentLoaded', function () {
  // Stagger-animate cards on initial page load
  const cards = document.querySelectorAll('.dash-card, .glass-card, .stat-card, .feature-card, .stagger-element');
  cards.forEach((card, i) => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(18px)';
    card.style.transition = 'none';
    setTimeout(() => {
      card.style.transition = 'opacity 0.45s ease, transform 0.45s ease';
      card.style.opacity = '1';
      card.style.transform = 'translateY(0)';
    }, 60 + i * 55);
  });

  // Ripple effect on primary buttons
  document.querySelectorAll('.btn-primary-custom').forEach(btn => {
    btn.addEventListener('click', function (e) {
      const ripple = document.createElement('span');
      const rect = btn.getBoundingClientRect();
      const size = Math.max(rect.width, rect.height);
      ripple.style.cssText = `
        position: absolute;
        border-radius: 50%;
        width: ${size}px; height: ${size}px;
        left: ${e.clientX - rect.left - size / 2}px;
        top: ${e.clientY - rect.top - size / 2}px;
        background: rgba(255,255,255,0.25);
        transform: scale(0);
        animation: ripple-out 0.5s ease forwards;
        pointer-events: none;
      `;
      btn.style.overflow = 'hidden';
      btn.style.position = 'relative';
      btn.appendChild(ripple);
      setTimeout(() => ripple.remove(), 500);
    });
  });
});

// ─── SLIDING NAV PILL ───────────────────────────────────────
// Creates a magic pill that flows between sidebar nav items,
// even across full page loads (via sessionStorage for position memory).
(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    const menu = document.getElementById('menu');
    if (!menu) return;

    const links = Array.from(menu.querySelectorAll('.nav-link'));
    if (!links.length) return;

    // Find active link index
    const activeIdx = links.findIndex(l => l.classList.contains('active'));
    if (activeIdx === -1) return;

    // ── Create the pill element ──────────────────────────────
    const pill = document.createElement('div');
    pill.id = 'nav-pill';
    pill.style.cssText = `
      position: absolute;
      left: 6px; right: 6px;
      border-radius: 8px;
      background: linear-gradient(135deg, rgba(124,58,237,.22), rgba(79,70,229,.16));
      border: 1px solid rgba(124,58,237,.32);
      pointer-events: none;
      z-index: 0;
      transition: top 0.45s cubic-bezier(0.16, 1, 0.3, 1),
                  height 0.45s cubic-bezier(0.16, 1, 0.3, 1),
                  opacity 0.3s ease;
    `;

    // Position needs the menu to be relative
    menu.style.position = 'relative';
    menu.insertBefore(pill, menu.firstChild);

    // Make links stack above the pill
    links.forEach(l => { l.style.position = 'relative'; l.style.zIndex = '1'; });

    function getPillGeometry(link) {
      const menuRect = menu.getBoundingClientRect();
      const linkRect = link.getBoundingClientRect();
      return {
        top: linkRect.top - menuRect.top,
        height: linkRect.height,
      };
    }

    function setPill(link, instant) {
      const { top, height } = getPillGeometry(link);
      if (instant) {
        pill.style.transition = 'none';
      } else {
        pill.style.transition = `
          top 0.45s cubic-bezier(0.16, 1, 0.3, 1),
          height 0.45s cubic-bezier(0.16, 1, 0.3, 1),
          opacity 0.3s ease
        `;
      }
      pill.style.top    = top + 'px';
      pill.style.height = height + 'px';
      pill.style.opacity = '1';
    }

    // ── Animate from previous tab if stored ─────────────────
    const prevIdx = parseInt(sessionStorage.getItem('navPillIdx') ?? '-1');

    if (prevIdx !== -1 && prevIdx !== activeIdx && links[prevIdx]) {
      // Instantly place pill at old position
      setPill(links[prevIdx], true);

      // Force reflow so browser registers the starting position
      void pill.offsetHeight;

      // Then animate to new position
      requestAnimationFrame(() => {
        setPill(links[activeIdx], false);
      });
    } else {
      // No history — just softly fade in at current position
      pill.style.opacity = '0';
      setPill(links[activeIdx], true);
      void pill.offsetHeight;
      pill.style.transition = 'opacity 0.35s ease';
      requestAnimationFrame(() => { pill.style.opacity = '1'; });
    }

    // ── Store clicked index before navigation ────────────────
    links.forEach((link, idx) => {
      link.addEventListener('click', () => {
        sessionStorage.setItem('navPillIdx', String(idx));
      });
    });

    // ── Handle window resize ─────────────────────────────────
    window.addEventListener('resize', () => {
      setPill(links[activeIdx], true);
    });
  });
})();

// ─── TELEGRAM-STYLE DARK / LIGHT MODE TOGGLE (ORIGIN-BASED) ──
// On click: captures button position → switches data-theme on <html>
// → animates a smooth circular ripple originating from the clicked icon.
(function () {
  'use strict';

  // Inject the refined ripple animation stylesheet
  const vt = document.createElement('style');
  vt.textContent = `
    /* Disable default box-shadows/blends that cause jank during transition */
    ::view-transition-old(root),
    ::view-transition-new(root) {
      animation: none;
      mix-blend-mode: normal;
    }

    /* The new theme reveals via a smooth circular ripple from the icon */
    ::view-transition-new(root) {
      z-index: 9999;
      clip-path: circle(0px at var(--theme-x, 50%) var(--theme-y, 50%));
      animation: theme-ripple 0.95s cubic-bezier(0.645, 0.045, 0.355, 1) forwards;
      will-change: clip-path;
    }

    ::view-transition-old(root) {
      z-index: 1;
    }

    @keyframes theme-ripple {
      from { clip-path: circle(0px at var(--theme-x, 50%) var(--theme-y, 50%)); }
      to   { clip-path: circle(var(--theme-r, 100%) at var(--theme-x, 50%) var(--theme-y, 50%)); }
    }

    /* Optimization: Temporarily disable heavy effects during transition to maintain 60fps */
    .theme-transitioning, 
    .theme-transitioning * {
      backdrop-filter: none !important;
      transition: none !important;
    }
  `;
  document.head.appendChild(vt);

  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
  }

  async function toggleTheme(btn) {
    const current  = document.documentElement.getAttribute('data-theme') || 'dark';
    const next     = current === 'dark' ? 'light' : 'dark';

    // Get exact center of the button for the ripple origin
    const rect = btn.getBoundingClientRect();
    const x    = Math.round(rect.left + rect.width  / 2);
    const y    = Math.round(rect.top  + rect.height / 2);
    
    // Calculate distance to the furthest corner of the screen
    const endRadius = Math.hypot(
        Math.max(x, window.innerWidth - x),
        Math.max(y, window.innerHeight - y)
    );

    // Set CSS vars used by the @keyframes above
    document.documentElement.style.setProperty('--theme-x', `${x}px`);
    document.documentElement.style.setProperty('--theme-y', `${y}px`);
    document.documentElement.style.setProperty('--theme-r', `${Math.ceil(endRadius)}px`);
    document.documentElement.style.setProperty('--theme-r-num', Math.ceil(endRadius));

    // Native View Transitions API (Chrome 111+, Firefox 126+)
    if (document.startViewTransition) {
      document.documentElement.classList.add('theme-transitioning');
      
      const transition = document.startViewTransition(() => {
        applyTheme(next);
      });

      try {
        await transition.finished;
      } finally {
        document.documentElement.classList.remove('theme-transitioning');
      }
    } else {
      applyTheme(next);
    }
  }

  document.addEventListener('DOMContentLoaded', function () {
    const btns = document.querySelectorAll('#theme-toggle, .auth-theme-toggle, .nav-theme-toggle');
    btns.forEach(btn => {
      btn.addEventListener('click', () => toggleTheme(btn));
    });
  });
})();
// ─── PREMIUM SCROLL REVEAL & PARALLAX ENGINE (V2.0) ─────────
(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    // ── 1. Reveal Elements with Intersection Observer ──
    const revealObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('revealed');
          
          // If this is a group, stagger its direct children
          if (entry.target.classList.contains('reveal-group')) {
            const children = entry.target.children;
            Array.from(children).forEach((child, i) => {
              child.style.setProperty('--reveal-delay', `${(i + 1) * 0.12}s`);
              child.classList.add('revealed');
            });
          }
        } else {
          // Re-triggering magic: remove class when out of view
          entry.target.classList.remove('revealed');
          if (entry.target.classList.contains('reveal-group')) {
            Array.from(entry.target.children).forEach(child => {
              child.classList.remove('revealed');
            });
          }
        }
      });
    }, {
      threshold: 0.1, // Reduced slightly for better sensitivity
      rootMargin: '10px 0px -40px 0px'
    });

    // Observe all [data-reveal] elements
    const elements = document.querySelectorAll('[data-reveal]');
    elements.forEach(el => revealObserver.observe(el));

    // ── 2. Ultimate Smooth Parallax ──
    let lastScrollY = window.scrollY;
    let ticking = false;

    function upgradeParallax() {
      const parallaxElements = document.querySelectorAll('.parallax-bg');
      if (!parallaxElements.length) return;

      parallaxElements.forEach(el => {
        const speed = 0.25;
        // Move image upwards while scrolling down (negative translateY)
        const offset = lastScrollY * -speed;
        el.style.setProperty('--scrolled-px', `${offset}px`);
      });

      ticking = false;
    }

    window.addEventListener('scroll', () => {
      lastScrollY = window.scrollY;
      if (!ticking) {
        requestAnimationFrame(upgradeParallax);
        ticking = true;
      }
    }, { passive: true });
    
    // Initial call
    upgradeParallax();
  });
})();

// Original code below
// ─── RESPONSIVE SIDEBAR TOGGLE ─────────────────────────────
(function () {
  'use strict';
// ... rest of the file

  document.addEventListener('DOMContentLoaded', function () {
    const toggle = document.getElementById('sidebarToggle');
    const closeBtn = document.getElementById('sidebarClose');
    const sidebar = document.getElementById('sidebarMenu');
    const overlay = document.getElementById('sidebarOverlay');
    const body = document.body;

    if (!sidebar || !overlay) return;

    function openSidebar() {
      sidebar.classList.add('open');
      overlay.classList.add('active');
      body.style.overflow = 'hidden'; // Prevent background scroll
    }

    function closeSidebar() {
      sidebar.classList.remove('open');
      overlay.classList.remove('active');
      body.style.overflow = '';
    }

    if (toggle) toggle.addEventListener('click', (e) => {
      e.stopPropagation();
      openSidebar();
    });

    if (closeBtn) closeBtn.addEventListener('click', closeSidebar);

    overlay.addEventListener('click', closeSidebar);

    // Close on link click (for mobile SPA feel)
    const links = sidebar.querySelectorAll('.nav-link');
    links.forEach(link => {
      link.addEventListener('click', () => {
        if (window.innerWidth <= 992) closeSidebar();
      });
    });

    // Handle ESC key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && sidebar.classList.contains('open')) {
        closeSidebar();
      }
    });

    // Reset state on window resize
    window.addEventListener('resize', () => {
      if (window.innerWidth > 992) {
        closeSidebar();
      }
    });
  });
})();
