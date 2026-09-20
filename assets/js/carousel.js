(function () {
  var AUTOPLAY_MS = 6000;
  var SWIPE_MIN_PX = 40;
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

  var SVG_NS = 'http://www.w3.org/2000/svg';
  var ICON_PATHS = {
    prev: 'M15 5l-7 7 7 7',
    next: 'M9 5l7 7-7 7',
    pause: 'M8 5v14M16 5v14',
    play: 'M8 5l11 7-11 7z'
  };

  function icon(name) {
    var el = document.createElementNS(SVG_NS, 'svg');
    el.setAttribute('viewBox', '0 0 24 24');
    el.setAttribute('aria-hidden', 'true');
    el.setAttribute('focusable', 'false');
    var path = document.createElementNS(SVG_NS, 'path');
    path.setAttribute('d', ICON_PATHS[name]);
    el.appendChild(path);
    return el;
  }

  function button(className, label, iconName) {
    var b = document.createElement('button');
    b.type = 'button';
    b.className = className;
    b.setAttribute('aria-label', label);
    if (iconName) b.appendChild(icon(iconName));
    return b;
  }

  function init(root) {
    var slidesEl = root.querySelector('.carousel-slides');
    var slides = Array.prototype.slice.call(root.querySelectorAll('.carousel-slide'));
    if (!slidesEl || slides.length < 2) return;

    var index = 0;
    var timer = null;
    var canAutoplay = root.hasAttribute('data-autoplay') && !reduceMotion.matches;
    var stopped = false;
    var shownPlaying = null;
    var hovering = false;
    var focused = false;
    var visible = true;

    var controls = document.createElement('div');
    controls.className = 'carousel-controls';
    var prev = button('carousel-btn', 'Previous slide', 'prev');
    var next = button('carousel-btn', 'Next slide', 'next');
    var dotsEl = document.createElement('div');
    dotsEl.className = 'carousel-dots';
    var count = document.createElement('span');
    count.className = 'carousel-count';
    var toggle = canAutoplay ? button('carousel-btn', '', 'pause') : null;

    var dots = slides.map(function (slide, n) {
      var title = slide.querySelector('.carousel-title');
      var dot = button('carousel-dot', 'Show slide ' + (n + 1) + (title ? ': ' + title.textContent : ''));
      dot.addEventListener('click', function () { userGo(n); });
      dotsEl.appendChild(dot);
      return dot;
    });

    controls.appendChild(prev);
    controls.appendChild(dotsEl);
    controls.appendChild(next);
    controls.appendChild(count);
    if (toggle) controls.appendChild(toggle);
    slidesEl.after(controls);

    function show(n) {
      index = (n + slides.length) % slides.length;
      slides.forEach(function (slide, i) {
        slide.classList.toggle('is-active', i === index);
        if (i === index) dots[i].setAttribute('aria-current', 'true');
        else dots[i].removeAttribute('aria-current');
      });
      count.textContent = (index + 1) + ' / ' + slides.length;
    }

    function running() {
      return canAutoplay && !stopped && !hovering && !focused && visible && !document.hidden;
    }

    function sync() {
      var run = running();
      if (run && !timer) {
        timer = setInterval(function () { show(index + 1); }, AUTOPLAY_MS);
      } else if (!run && timer) {
        clearInterval(timer);
        timer = null;
      }
      var playing = canAutoplay && !stopped;
      slidesEl.setAttribute('aria-live', playing ? 'off' : 'polite');
      // Only touch the button when the state changes: replacing its icon on
      // focus (mousedown) would swallow the click that follows.
      if (toggle && playing !== shownPlaying) {
        shownPlaying = playing;
        toggle.setAttribute('aria-label', playing ? 'Pause automatic slide show' : 'Start automatic slide show');
        toggle.replaceChildren(icon(playing ? 'pause' : 'play'));
      }
    }

    function userGo(n) {
      stopped = true;
      show(n);
      sync();
    }

    prev.addEventListener('click', function () { userGo(index - 1); });
    next.addEventListener('click', function () { userGo(index + 1); });
    if (toggle) {
      toggle.addEventListener('click', function () {
        stopped = !stopped;
        sync();
      });
    }

    root.addEventListener('keydown', function (e) {
      if (e.altKey || e.ctrlKey || e.metaKey || e.shiftKey) return;
      if (e.key === 'ArrowLeft') { e.preventDefault(); userGo(index - 1); }
      else if (e.key === 'ArrowRight') { e.preventDefault(); userGo(index + 1); }
    });

    var startX = 0;
    var startY = 0;
    var tracking = false;
    slidesEl.addEventListener('pointerdown', function (e) {
      if (e.pointerType === 'mouse') return;
      tracking = true;
      startX = e.clientX;
      startY = e.clientY;
    });
    slidesEl.addEventListener('pointerup', function (e) {
      if (!tracking) return;
      tracking = false;
      var dx = e.clientX - startX;
      var dy = e.clientY - startY;
      if (Math.abs(dx) >= SWIPE_MIN_PX && Math.abs(dx) > Math.abs(dy) * 1.5) {
        userGo(index + (dx < 0 ? 1 : -1));
      }
    });
    slidesEl.addEventListener('pointercancel', function () { tracking = false; });

    root.addEventListener('mouseenter', function () { hovering = true; sync(); });
    root.addEventListener('mouseleave', function () { hovering = false; sync(); });
    root.addEventListener('focusin', function () { focused = true; sync(); });
    root.addEventListener('focusout', function (e) {
      if (!root.contains(e.relatedTarget)) { focused = false; sync(); }
    });
    document.addEventListener('visibilitychange', sync);
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (entries) {
        visible = entries[entries.length - 1].isIntersecting;
        sync();
      }, { threshold: 0.3 }).observe(root);
    }

    root.classList.add('is-enhanced');
    show(0);
    sync();
  }

  Array.prototype.forEach.call(document.querySelectorAll('.carousel'), init);
})();
