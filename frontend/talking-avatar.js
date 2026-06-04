import { TalkingHead } from "talkinghead";

let head = null;
let loginHead = null;
let micStream = null;
let micContext = null;
let micAnalyser = null;
let audioUnlocked = false;
let teachingMotionTimers = [];

const MAIN_VIEW = {
  cameraDistance: -0.6,
  cameraY: 0.06
};

const TEACHING_GESTURES = [
  { name: "handup", duration: 1.2, mirror: false },
  { name: "index", duration: 1.1, mirror: true },
  { name: "handup", duration: 1.0, mirror: true }
];

const TEACHING_POSES = ["straight", "side"];

function setLoading(message, isError) {
  const node = document.getElementById("avatar-loading");
  if (!node) return;
  node.textContent = message;
  node.style.color = isError ? "#ff9d9d" : "#9aa4ff";
}

function hideLoading() {
  const node = document.getElementById("avatar-loading");
  if (node) node.style.display = "none";
}

function safeCall(fn) {
  try {
    return fn();
  } catch (error) {
    console.error("Talking avatar action failed:", error);
    return null;
  }
}

function buildWordTimeline(text) {
  const parts = (text || "")
    .replace(/\[TOPIC:.*?\]/gi, "")
    .trim()
    .split(/\s+/)
    .filter(Boolean);

  const words = [];
  const wtimes = [];
  const wdurations = [];
  let currentTime = 120;

  parts.forEach(function(word) {
    const cleaned = word.replace(/[^\w'-]/g, "");
    if (!cleaned) {
      currentTime += 60;
      return;
    }

    const vowelCount = (cleaned.match(/[aeiouy]+/gi) || []).length;
    const duration = Math.min(
      580,
      Math.max(170, 110 + cleaned.length * 22 + Math.max(1, vowelCount) * 55)
    );
    const trailingPause = /[,.!?]$/.test(word) ? 160 : 45;

    words.push(cleaned);
    wtimes.push(currentTime);
    wdurations.push(duration);
    currentTime += duration + trailingPause;
  });

  return {
    words,
    wtimes,
    wdurations,
    totalDuration: currentTime + 200
  };
}

function createSilentAudioBuffer(durationMs) {
  if (!head || !head.audioCtx) return null;
  const rate = head.audioCtx.sampleRate || 22050;
  const sampleCount = Math.max(1, Math.ceil((durationMs / 1000) * rate));
  const buffer = head.audioCtx.createBuffer(1, sampleCount, rate);
  const channel = buffer.getChannelData(0);
  channel.fill(0);
  return buffer;
}

async function unlockAvatarAudio() {
  if (!head || audioUnlocked) return true;
  try {
    if (head.audioCtx && head.audioCtx.state !== "running") {
      await head.audioCtx.resume();
    }
    audioUnlocked = true;
    return true;
  } catch (error) {
    console.error("Avatar audio unlock failed:", error);
    return false;
  }
}

async function startMicVisualization() {
  if (!head || micStream) return;

  const AudioContextClass = window.AudioContext || window.webkitAudioContext;
  if (!AudioContextClass || !navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
    return;
  }

  try {
    micStream = await navigator.mediaDevices.getUserMedia({ audio: true });
    micContext = new AudioContextClass();
    const source = micContext.createMediaStreamSource(micStream);
    micAnalyser = micContext.createAnalyser();
    source.connect(micAnalyser);

    head.startListening(micAnalyser, {}, function(state) {
      if (state === "start") {
        safeCall(function() {
          head.setMood("happy");
        });
      } else if (state === "stop" || state === "maxsilence") {
        safeCall(function() {
          head.setMood("neutral");
        });
      }
    });
  } catch (error) {
    console.error("Microphone visualization failed:", error);
    stopMicVisualization();
  }
}

function stopMicVisualization() {
  if (head) {
    safeCall(function() {
      head.stopListening();
      head.setMood("neutral");
    });
  }

  if (micStream) {
    micStream.getTracks().forEach(function(track) {
      track.stop();
    });
  }
  if (micContext) {
    micContext.close().catch(function() {});
  }

  micStream = null;
  micContext = null;
  micAnalyser = null;
}

function buildTeachingPlan(text, totalDuration) {
  const cleaned = (text || "").replace(/\[TOPIC:.*?\]/gi, "").trim();
  const clauses = cleaned
    .split(/(?<=[.!?])\s+|(?<=,)\s+/)
    .map(function(part) { return part.trim(); })
    .filter(Boolean);

  if (!clauses.length) {
    return [{ at: 300, pose: "straight", gesture: null, duration: 0, mirror: false }];
  }

  const spacing = Math.max(2400, Math.floor(totalDuration / Math.max(clauses.length, 1)));

  return clauses.map(function(clause, index) {
    const lower = clause.toLowerCase();
    let gesture = null;
    let pose = index % 2 === 0 ? "straight" : "side";

    if (lower.includes("important") || lower.includes("remember") || lower.includes("notice")) {
      gesture = { name: "index", duration: 1.4, mirror: true };
      pose = "side";
    } else if (
      lower.includes("first") ||
      lower.includes("second") ||
      lower.includes("third") ||
      lower.includes("next") ||
      lower.includes("step") ||
      lower.includes("for example") ||
      lower.includes("example")
    ) {
      gesture = { name: "handup", duration: 1.2, mirror: false };
      pose = "straight";
    } else if (
      lower.includes("this means") ||
      lower.includes("we can say") ||
      lower.includes("in other words") ||
      lower.includes("look at") ||
      lower.includes("let us")
    ) {
      gesture = { name: "handup", duration: 1.0, mirror: true };
      pose = "side";
    } else if (index > 0 && index % 4 === 0) {
      gesture = TEACHING_GESTURES[index % TEACHING_GESTURES.length];
      pose = "straight";
    }

    return {
      at: 300 + index * spacing,
      pose: pose,
      gesture: gesture ? gesture.name : null,
      duration: gesture ? gesture.duration : 0,
      mirror: gesture ? gesture.mirror : false
    };
  });
}

function clearTeachingMotionLoop() {
  teachingMotionTimers.forEach(function(timerId) {
    clearTimeout(timerId);
  });
  teachingMotionTimers = [];
}

function applyTeachingMotionStep(step) {
  if (!head || !step) return;

  safeCall(function() {
    head.setMood("happy");
    head.playPose(step.pose, null, 4.2);
    if (step.gesture) {
      head.playGesture(step.gesture, step.duration, step.mirror);
    }
  });
}

function startTeachingMotionLoop(text, totalDuration) {
  if (!head) return;

  clearTeachingMotionLoop();

  const plan = buildTeachingPlan(text, totalDuration);
  plan.forEach(function(step) {
    const timerId = setTimeout(function() {
      applyTeachingMotionStep(step);
    }, step.at);
    teachingMotionTimers.push(timerId);
  });
}

function stopTeachingMotionLoop() {
  clearTeachingMotionLoop();
  safeCall(function() {
    if (!head) return;
    head.stopGesture();
    head.stopPose();
    head.setMood("neutral");
    head.setView("full", MAIN_VIEW);
    head.playPose("straight", null, 2.4);
  });
}

async function initTalkingAvatar() {
  const mountNode = document.getElementById("avatar-stage");
  const loginMountNode = document.getElementById("login-avatar-stage");
  if (!mountNode && !loginMountNode) return;

  try {
    const avatarConfig = {
      url: "/TalkingHead/avatars/avaturn.glb",
      body: "F",
      avatarMood: "neutral",
      lipsyncLang: "en",
      baseline: {
        headRotateX: -0.05,
        eyeBlinkLeft: 0.15,
        eyeBlinkRight: 0.15
      }
    };

    if (mountNode) {
      setLoading("Loading 3D avatar...");
      head = new TalkingHead(mountNode, {
        cameraView: "full",
        cameraRotateEnable: false,
        cameraPanEnable: false,
        cameraZoomEnable: false,
        cameraDistance: MAIN_VIEW.cameraDistance,
        cameraY: MAIN_VIEW.cameraY,
        lightAmbientIntensity: 2.2,
        lightDirectIntensity: 18,
        lightSpotIntensity: 0,
        lipsyncModules: ["en"]
      });

      await head.showAvatar(
        avatarConfig,
        function(ev) {
          if (!ev.lengthComputable) return;
          const percent = Math.min(100, Math.round((ev.loaded / ev.total) * 100));
          setLoading("Loading 3D avatar... " + percent + "%");
        }
      );

      hideLoading();
      safeCall(function() {
        head.setView("full", MAIN_VIEW);
        head.playPose("straight", null, 2.5);
      });
    }

    if (loginMountNode) {
      const loginLoading = document.getElementById("login-avatar-loading");
      loginHead = new TalkingHead(loginMountNode, {
        cameraView: "upper",
        cameraRotateEnable: false,
        cameraPanEnable: false,
        cameraZoomEnable: false,
        lightAmbientIntensity: 2.2,
        lightDirectIntensity: 18,
        lightSpotIntensity: 0,
        lipsyncModules: ["en"]
      });

      await loginHead.showAvatar(
        avatarConfig,
        function(ev) {
          if (!loginLoading || !ev.lengthComputable) return;
          const percent = Math.min(100, Math.round((ev.loaded / ev.total) * 100));
          loginLoading.textContent = "Loading 3D avatar... " + percent + "%";
        }
      );

      if (loginLoading) loginLoading.style.display = "none";
      safeCall(function() {
        loginHead.setView("upper", { cameraDistance: -0.5, cameraY: 0.18 });
      });
    }

    window.talkingAvatar = {
      async unlockAudio() {
        return unlockAvatarAudio();
      },
      async speak(text) {
        return false;
      },
      async animateText(text) {
        if (!head || !text) return false;

        await unlockAvatarAudio();

        const timeline = buildWordTimeline(text);
        if (!timeline.words.length) return false;

        safeCall(function() {
          head.stopSpeaking();
          head.setMood("happy");
          head.setView("full", MAIN_VIEW);
          startTeachingMotionLoop(text, timeline.totalDuration);
          const silentAudio = createSilentAudioBuffer(timeline.totalDuration);
          if (!silentAudio) return;
          head.speakAudio(
            {
              audio: silentAudio,
              words: timeline.words,
              wtimes: timeline.wtimes,
              wdurations: timeline.wdurations
            },
            {
              lipsyncLang: "en"
            }
          );
        });

        return true;
      },
      startTeachingMotion() {
        startTeachingMotionLoop("", 3000);
      },
      stopTeachingMotion() {
        stopTeachingMotionLoop();
      },
      setMood(mood) {
        safeCall(function() {
          if (!head) return;
          head.setMood(mood);
        });
      },
      lookAtUser() {
        safeCall(function() {
          if (!head) return;
          head.speakTo = null;
        });
      },
      playGesture(name) {
        safeCall(function() {
          if (!head || !name) return;
          head.playGesture(name, 1.5);
        });
      },
      interrupt() {
        stopMicVisualization();
        stopTeachingMotionLoop();
        safeCall(function() {
          if (!head) return;
          head.stopSpeaking();
          if (head.streamInterrupt) head.streamInterrupt();
          head.setMood("neutral");
        });
      },
      startMicVisualization() {
        startMicVisualization();
      },
      stopMicVisualization() {
        stopMicVisualization();
      }
    };
  } catch (error) {
    console.error("TalkingHead failed to initialize:", error);
    setLoading("3D avatar unavailable", true);
  }
}

document.addEventListener("DOMContentLoaded", function() {
  initTalkingAvatar();
});

document.addEventListener("visibilitychange", function() {
  [head, loginHead].forEach(function(instance) {
    if (!instance) return;
    if (document.visibilityState === "visible") {
      instance.start();
    } else {
      instance.stop();
    }
  });
});

window.addEventListener("beforeunload", function() {
  stopMicVisualization();
  stopTeachingMotionLoop();
});
