(() => {
  const stations = [['p8', 'P8'], ['p2', 'P2']].map(([id, name]) => {
    const radio = document.getElementById(`${id}-radio`);
    return {
      name, radio, source: radio.getAttribute('src'),
      button: document.getElementById(`${id}-button`),
      status: document.getElementById(`${id}-status`),
      attempt: 0,
    };
  });
  const timeInDenmark = new Intl.DateTimeFormat('en-GB', {
    timeZone: 'Europe/Copenhagen', hour: '2-digit', minute: '2-digit', hourCycle: 'h23',
  });
  let selected = null;
  let suspended = false;

  function scheduledResume() {
    const parts = timeInDenmark.formatToParts(new Date());
    const hour = Number(parts.find(part => part.type === 'hour').value);
    const minute = Number(parts.find(part => part.type === 'minute').value);
    const resumeHour = minute >= 58 ? (hour + 1) % 24 : hour;
    const resumeMinute = resumeHour === 12 ? 15 : 5;
    return minute >= 58 || minute < resumeMinute
      ? (resumeHour === 12 ? '12:15' : ':05')
      : null;
  }

  function render() {
    for (const station of stations) {
      const active = station === selected;
      station.button.textContent = active ? `❚❚ Pause ${station.name}` : `▶ Play ${station.name}`;
      station.button.setAttribute('aria-pressed', String(active));
      if (active && suspended) {
        station.status.textContent = `Paused — resumes at ${scheduledResume()} (Danish time). Press pause to cancel.`;
      }
    }
  }

  function stop(station) {
    // Disconnect rather than retaining buffered audio or downloading while paused.
    station.attempt += 1;
    station.radio.pause();
    station.radio.removeAttribute('src');
    station.radio.load();
    station.status.textContent = '';
  }

  function showError(station) {
    if (selected !== station || suspended) return;
    selected = null;
    suspended = false;
    stop(station);
    station.status.textContent = 'Unable to play automatically. Press play to try again.';
    render();
  }

  async function start(station) {
    const attempt = ++station.attempt;
    station.status.textContent = 'Connecting…';
    station.radio.src = station.source;
    station.radio.load();
    try {
      await station.radio.play();
    } catch (error) {
      if (station.attempt === attempt) showError(station);
    }
  }

  function checkSchedule() {
    if (!selected) return;
    if (scheduledResume()) {
      if (!suspended) {
        suspended = true;
        stop(selected);
      }
    } else if (suspended) {
      suspended = false;
      start(selected);
    }
    render();
  }

  for (const station of stations) {
    station.button.addEventListener('click', () => {
      const previous = selected;
      selected = null;
      suspended = false;
      if (previous) stop(previous);
      if (previous !== station) {
        selected = station;
        suspended = Boolean(scheduledResume());
        if (!suspended) start(station);
      }
      render();
    });
    station.radio.addEventListener('playing', () => {
      // Recheck the clock when playback begins, including after buffering.
      checkSchedule();
      if (selected === station && !suspended) station.status.textContent = '';
    });
    station.radio.addEventListener('waiting', () => {
      if (selected === station && !suspended) station.status.textContent = 'Connecting…';
    });
    station.radio.addEventListener('error', () => showError(station));
    // Native controls remain available without JavaScript; scheduling needs JavaScript.
    station.radio.hidden = true;
    station.button.hidden = false;
  }

  render();
  setInterval(checkSchedule, 1000);
  document.addEventListener('visibilitychange', checkSchedule);
  window.addEventListener('pageshow', checkSchedule);
  window.addEventListener('pagehide', () => {
    const previous = selected;
    selected = null;
    suspended = false;
    if (previous) stop(previous);
    render();
  });
})();
