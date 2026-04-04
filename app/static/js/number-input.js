/**
 * NumberInput — Vanilla JS animated number input
 * Enhanced with Click-to-Edit manual entry support.
 */

(function () {
  'use strict';

  function rollDigits(displayEl, oldVal, newVal) {
    if (oldVal === newVal) return;
    
    const going_up = newVal > oldVal;
    const diff = Math.abs(newVal - oldVal);
    const steps = Math.min(diff, 8);
    const lockedH = 48; 
    
    displayEl.style.height  = lockedH + 'px';
    displayEl.style.overflow = 'hidden';

    const strip = document.createElement('div');
    strip.className = 'ni-strip';
    strip.style.cssText = `
      display: flex;
      flex-direction: column;
      will-change: transform;
      transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    `;

    const nums = [];
    for (let i = 0; i <= steps; i++) {
        const t = i / steps;
        const n = going_up ? oldVal + (newVal - oldVal) * t : oldVal - (oldVal - newVal) * t;
        nums.push(Math.round(n));
    }

    displayEl.textContent = '';
    nums.forEach((n) => {
      const span = document.createElement('span');
      span.textContent = String(n);
      span.style.cssText = `display: flex; align-items: center; justify-content: center; height: ${lockedH}px; flex-shrink: 0;`;
      strip.appendChild(span);
    });

    displayEl.appendChild(strip);
    strip.offsetHeight; // Force reflow
    strip.style.transform = `translateY(-${steps * lockedH}px)`;

    strip.addEventListener('transitionend', () => {
      displayEl.textContent = String(newVal);
      displayEl.style.height = '';
      displayEl.style.overflow = '';
    }, { once: true });
  }

  function buildWidget(input) {
    const min = parseInt(input.min) || 1900;
    const max = parseInt(input.max) || 2100;
    const noControls = input.hasAttribute('data-no-controls');
    let value = parseInt(input.value) || parseInt(input.min) || new Date().getFullYear();

    value = Math.min(Math.max(value, min), max);
    input.value = value;
    input.type = 'hidden';

    const wrapper = document.createElement('div');
    wrapper.className = 'ni-wrapper' + (noControls ? ' ni-no-controls' : '');
    wrapper.setAttribute('role', 'group');

    const display = document.createElement('div');
    display.className = 'ni-display';
    display.textContent = String(value);

    function setValue(newVal, skipAnimation = false) {
      newVal = Math.min(Math.max(newVal, min), max);
      if (newVal === value) {
        display.textContent = String(value); // Reset text in case of invalid manual entry
        return;
      }

      const oldVal = value;
      value = newVal;
      input.value = value;

      if (skipAnimation) {
        display.textContent = String(newVal);
      } else {
        rollDigits(display, oldVal, newVal);
      }
      
      if (!noControls) updateButtons();
      
      input.dispatchEvent(new Event('input', { bubbles: true }));
      input.dispatchEvent(new Event('change', { bubbles: true }));
    }

    // ── Manual Edit Logic ────────────────────────────────────
    if (!noControls) {
      display.style.cursor = 'text';
      display.addEventListener('click', () => {
        if (display.querySelector('.ni-edit-input')) return;

        const editInput = document.createElement('input');
        editInput.type = 'number';
        editInput.className = 'ni-edit-input';
        editInput.value = value;
        editInput.min = min;
        editInput.max = max;

        display.textContent = '';
        display.appendChild(editInput);
        editInput.focus();
        editInput.select();

        const commit = () => {
          const newVal = parseInt(editInput.value);
          display.removeChild(editInput);
          if (!isNaN(newVal)) {
            setValue(newVal);
          } else {
            display.textContent = String(value);
          }
        };

        editInput.addEventListener('keydown', (e) => {
          if (e.key === 'Enter') { e.preventDefault(); commit(); }
          if (e.key === 'Escape') { e.preventDefault(); display.textContent = String(value); }
        });

        editInput.addEventListener('blur', commit);
      });
    }

    let btnMinus, btnPlus;
    function updateButtons() {
      if (!btnMinus || !btnPlus) return;
      btnMinus.disabled = value <= min;
      btnPlus.disabled  = value >= max;
      btnMinus.classList.toggle('ni-btn-disabled', value <= min);
      btnPlus.classList.toggle('ni-btn-disabled', value >= max);
    }

    if (!noControls) {
      btnMinus = document.createElement('button');
      btnMinus.type = 'button';
      btnMinus.className = 'ni-btn ni-btn-minus';
      btnMinus.innerHTML = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round"><line x1="5" y1="12" x2="19" y2="12"/></svg>`;
      
      btnPlus = document.createElement('button');
      btnPlus.type = 'button';
      btnPlus.className = 'ni-btn ni-btn-plus';
      btnPlus.innerHTML = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>`;

      wrapper.appendChild(btnMinus);
      wrapper.appendChild(display);
      wrapper.appendChild(btnPlus);

      btnMinus.addEventListener('pointerdown', (e) => { e.preventDefault(); setValue(value - 1); wrapper.focus(); });
      btnPlus.addEventListener('pointerdown',  (e) => { e.preventDefault(); setValue(value + 1); wrapper.focus(); });

      let repeatTimer = null;
      const startRepeat = (dir) => { stopRepeat(); repeatTimer = setTimeout(() => { repeatTimer = setInterval(() => setValue(value + dir), 80); }, 400); };
      const stopRepeat = () => { clearTimeout(repeatTimer); clearInterval(repeatTimer); repeatTimer = null; };
      btnMinus.addEventListener('pointerdown', () => startRepeat(-1));
      btnPlus.addEventListener('pointerdown',  () => startRepeat(+1));
      document.addEventListener('pointerup', stopRepeat);

      wrapper.tabIndex = 0;
      wrapper.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowUp'   || e.key === 'ArrowRight') { e.preventDefault(); setValue(value + 1); }
        if (e.key === 'ArrowDown' || e.key === 'ArrowLeft')  { e.preventDefault(); setValue(value - 1); }
      });
      
      updateButtons();
    } else {
      wrapper.appendChild(display);
    }

    input.addEventListener('valueUpdate', () => {
      const newVal = parseInt(input.value);
      if (!isNaN(newVal)) setValue(newVal);
    });

    input.parentNode.insertBefore(wrapper, input.nextSibling);
  }

  function init() {
    document.querySelectorAll('input[data-number-input]').forEach(input => {
      if (!input.nextElementSibling || !input.nextElementSibling.classList.contains('ni-wrapper')) {
        buildWidget(input);
      }
    });
  }

  window.initNumberInputs = init;
  if (document.readyState === 'loading') { document.addEventListener('DOMContentLoaded', init); } else { init(); }
})();
