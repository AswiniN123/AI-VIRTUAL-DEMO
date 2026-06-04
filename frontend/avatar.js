// frontend/avatar.js

let bounceInterval = null;

// ── Safe element getter ─────────────────────────────────
function getAvatarEl(id) {
  return document.getElementById(id);
}

function getAvatarImg() {
  return getAvatarEl("avatar-img");
}

function notifyTalkingAvatar(eventName, payload) {
  if (window.talkingAvatar && typeof window.talkingAvatar[eventName] === "function") {
    window.talkingAvatar[eventName](payload);
  }
}

function buildSpeechText(text) {
  if (!text) return "";

  let spoken = text.replace(/\[TOPIC:.*?\]/gi, "").trim();
  spoken = spoken.replace(/```[\s\S]*?```/g, " Let me explain that code separately. ");
  spoken = spoken.replace(/`([^`]+)`/g, "$1");
  spoken = spoken.replace(/\*\*(.*?)\*\*/g, "$1");
  spoken = spoken.replace(/\*(.*?)\*/g, "$1");
  spoken = spoken.replace(/^#{1,6}\s+/gm, "");
  spoken = spoken.replace(/^\d+\.\s+/gm, "");
  spoken = spoken.replace(/^[-*]\s+/gm, "");
  spoken = spoken.replace(/\n+/g, " ");
  spoken = spoken.replace(/\s+/g, " ").trim();

  spoken = spoken.replace(/for example/gi, ". For example,");
  spoken = spoken.replace(/in simple words/gi, "In simple words,");
  spoken = spoken.replace(/that means/gi, ". That means");

  return spoken;
}

// ── Update status badge ────────────────────────────────
function setStatus(status) {
  const badge = getAvatarEl("status-badge");
  const dot   = getAvatarEl("status-dot");
  const text  = getAvatarEl("status-text");
  const bar   = getAvatarEl("avatar-status-bar");
  const inlineStatus = getAvatarEl("avatar-status-inline");

  const statusMap = {
    "ready": {
      label:  "Ready to Teach",
      color:  "#2ecc71",
      bg:     "#0d2e1a",
      border: "#1d6a3a"
    },
    "thinking": {
      label:  "Thinking...",
      color:  "#f39c12",
      bg:     "#2e1a00",
      border: "#8a5500"
    },
    "explaining": {
      label:  "Explaining",
      color:  "#7b8cff",
      bg:     "#13132a",
      border: "#3b4cca"
    },
    "listening": {
      label:  "Listening",
      color:  "#1abc9c",
      bg:     "#0d2e2a",
      border: "#1a6a60"
    },
    "error": {
      label:  "Error",
      color:  "#e74c3c",
      bg:     "#2a1010",
      border: "#662222"
    }
  };

  const s = statusMap[status] || statusMap["ready"];

  // Only update if elements exist
  if (dot)   dot.style.background    = s.color;
  if (text)  text.textContent        = s.label;
  if (inlineStatus) {
    inlineStatus.textContent = s.label;
    inlineStatus.style.color = s.color;
  }
  if (badge) {
    badge.style.background  = s.bg;
    badge.style.borderColor = s.border;
    badge.style.color       = s.color;
  }
  if (bar) {
    bar.textContent  = s.label;
    bar.style.color  = s.color;
  }
}

// ── Ring pulse ─────────────────────────────────────────
function startRingPulse(color) {
  const ring = getAvatarEl("avatar-ring");
  if (!ring) return;
  ring.style.borderColor = color;
  ring.style.boxShadow   = "0 0 18px 6px " + color + "55";
  ring.style.transition  = "all 0.3s ease";
}

function stopRingPulse() {
  const ring = getAvatarEl("avatar-ring");
  if (!ring) return;
  ring.style.borderColor = "#3b4cca";
  ring.style.boxShadow   = "0 0 8px 2px rgba(59,76,202,0.3)";
}

// ── Sound wave ─────────────────────────────────────────
function showSoundWave(show) {
  const wave = getAvatarEl("sound-wave");
  if (wave) wave.style.opacity = show ? "1" : "0";
}

// ── Bounce animation ───────────────────────────────────
function startTalking() {
  const img = getAvatarImg();
  if (img) {
    let frame = 0;
    const frames = [
      "scale(1.0)",
      "scale(1.03) translateY(-3px)",
      "scale(1.0)",
      "scale(1.02) translateY(2px)",
    ];

    img.style.transition = "transform 0.15s ease";
    bounceInterval = setInterval(function() {
      img.style.transform = frames[frame % frames.length];
      frame++;
    }, 200);
  }

  setStatus("explaining");
  startRingPulse("#7b8cff");
  showSoundWave(true);
  notifyTalkingAvatar("setMood", "happy");
  notifyTalkingAvatar("lookAtUser");
  notifyTalkingAvatar("startTeachingMotion");
}

function stopTalking() {
  const img = getAvatarImg();
  clearInterval(bounceInterval);
  bounceInterval = null;
  if (img) {
    img.style.transform  = "scale(1.0) translateY(0px)";
    img.style.transition = "transform 0.3s ease";
  }

  setStatus("ready");
  stopRingPulse();
  showSoundWave(false);
  notifyTalkingAvatar("stopTeachingMotion");
  notifyTalkingAvatar("setMood", "neutral");
}

// ── Speak text ─────────────────────────────────────────
function speakText(text) {
  if (!text) return;
  const cleanText = buildSpeechText(text);
  if (window.talkingAvatar && typeof window.talkingAvatar.animateText === "function") {
    window.talkingAvatar.animateText(cleanText).catch(function(error) {
      console.error("Talking avatar animation failed:", error);
    });
  }
  if (window.talkingAvatar && typeof window.talkingAvatar.unlockAudio === "function") {
    window.talkingAvatar.unlockAudio().catch(function(error) {
      console.error("Talking avatar audio unlock failed:", error);
    });
  }

  if (window.talkingAvatar && typeof window.talkingAvatar.speak === "function") {
    window.talkingAvatar.speak(cleanText).then(function(usedTalkingHead) {
      if (!usedTalkingHead) {
        fallbackBrowserSpeech(cleanText);
      }
    }).catch(function(error) {
      console.error("Talking avatar speech failed:", error);
      fallbackBrowserSpeech(cleanText);
    });
    return;
  }

  fallbackBrowserSpeech(cleanText);
}

function fallbackBrowserSpeech(cleanText) {
  window.speechSynthesis.cancel();
  notifyTalkingAvatar("animateText", cleanText);

  const utterance = new SpeechSynthesisUtterance(cleanText);
  utterance.lang  = "en-US";
  utterance.rate  = 0.92;
  utterance.pitch = 1.1;

  const voices = window.speechSynthesis.getVoices();
  const femaleVoice = voices.find(function(v) {
    return v.name.includes("Female")   ||
           v.name.includes("Samantha") ||
           v.name.includes("Karen")    ||
           v.name.includes("Jenny")    ||
           v.name.includes("Zira")     ||
           v.name.includes("Susan")    ||
           v.name.includes("Victoria") ||
           v.name.includes("Google UK English Female");
  });
  if (femaleVoice) utterance.voice = femaleVoice;

  utterance.onstart = function() {
    startTalking();
  };
  utterance.onend = function() {
    stopTalking();
  };
  utterance.onerror = function() {
    stopTalking();
  };

  setTimeout(function() {
    window.speechSynthesis.speak(utterance);
  }, 100);
}

function stopSpeaking() {
  window.speechSynthesis.cancel();
  stopTalking();
  notifyTalkingAvatar("interrupt");
}

// ── Init safely after DOM is ready ────────────────────
window.addEventListener("DOMContentLoaded", function() {
  setTimeout(function() {
    setStatus("ready");
  }, 1000);
});

window.speechSynthesis.onvoiceschanged = function() {
  window.speechSynthesis.getVoices();
};
