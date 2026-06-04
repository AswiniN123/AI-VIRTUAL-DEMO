let recognition = null;
const MIC_BUTTON_LABEL = `
  <svg viewBox="0 0 24 24" aria-hidden="true">
    <path d="M12 15a3 3 0 0 0 3-3V6a3 3 0 1 0-6 0v6a3 3 0 0 0 3 3Zm5-3a1 1 0 1 1 2 0 7 7 0 0 1-6 6.93V21h3a1 1 0 1 1 0 2H8a1 1 0 1 1 0-2h3v-2.07A7 7 0 0 1 5 12a1 1 0 0 1 2 0 5 5 0 0 0 10 0Z"/>
  </svg>
`;

function toggleVoice() {
  if (!('SpeechRecognition' in window) && !('webkitSpeechRecognition' in window)) {
    alert("Please use Google Chrome for voice input!");
    return;
  }

  if (!recognition) {
    recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.continuous     = false;
    recognition.interimResults = false;
    recognition.lang           = "en-US";

    recognition.onstart = () => {
      if (typeof stopSpeaking === "function") stopSpeaking();
      document.getElementById("micBtn").innerHTML = MIC_BUTTON_LABEL;
      document.getElementById("micBtn").title = "Listening...";
      document.getElementById("micBtn").classList.add("listening");
      if (typeof setStatus === "function") setStatus("listening");
      if (window.talkingAvatar && typeof window.talkingAvatar.startMicVisualization === "function") {
        window.talkingAvatar.startMicVisualization();
      }
    };

    recognition.onresult = (e) => {
      document.getElementById("userInput").value = e.results[0][0].transcript;
      document.getElementById("micBtn").innerHTML = MIC_BUTTON_LABEL;
      document.getElementById("micBtn").title = "Voice input";
      document.getElementById("micBtn").classList.remove("listening");
      if (window.talkingAvatar && typeof window.talkingAvatar.stopMicVisualization === "function") {
        window.talkingAvatar.stopMicVisualization();
      }
      sendMessage();
    };

    recognition.onerror = (e) => {
      document.getElementById("micBtn").innerHTML = MIC_BUTTON_LABEL;
      document.getElementById("micBtn").title = "Voice input";
      document.getElementById("micBtn").classList.remove("listening");
      if (window.talkingAvatar && typeof window.talkingAvatar.stopMicVisualization === "function") {
        window.talkingAvatar.stopMicVisualization();
      }
      if (e.error === "not-allowed") {
        alert("Microphone blocked!\n1. Click lock icon in Chrome\n2. Set Microphone to Allow\n3. Refresh page");
      } else if (e.error === "no-speech") {
        alert("No speech detected. Please try again.");
      }
    };

    recognition.onend = () => {
      document.getElementById("micBtn").innerHTML = MIC_BUTTON_LABEL;
      document.getElementById("micBtn").title = "Voice input";
      document.getElementById("micBtn").classList.remove("listening");
      if (window.talkingAvatar && typeof window.talkingAvatar.stopMicVisualization === "function") {
        window.talkingAvatar.stopMicVisualization();
      }
    };
  }

  try {
    recognition.start();
  } catch(e) {
    recognition = null;
  }
}
