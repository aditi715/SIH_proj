const sendBtn = document.getElementById("sendBtn");
const userInput = document.getElementById("userInput");
const messages = document.getElementById("messages");
const langSelect = document.getElementById("language");
const voiceBtn = document.getElementById("voiceBtn");

// Add message to chat
function addMessage(text, who="bot") {
  const div = document.createElement("div");
  div.className = who;
  div.innerText = text;
  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight;
}

// Send message
async function sendMessage() {
  const text = userInput.value.trim();
  if (!text) return;

  addMessage(text, "user");
  userInput.value = "";

  const res = await fetch("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: text, lang: langSelect.value })
  });

  const data = await res.json();
  addMessage(data.reply, "bot");
}

sendBtn.addEventListener("click", sendMessage);

// Voice recognition
voiceBtn.addEventListener("click", () => {
  const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
  recognition.lang = langSelect.value === "mr" ? "mr-IN" :
                     langSelect.value === "hi" ? "hi-IN" :
                     langSelect.value === "ta" ? "ta-IN" : "en-US";

  recognition.start();

  recognition.onresult = (event) => {
    userInput.value = event.results[0][0].transcript;
  };
});

// Chart rendering
async function loadChart() {
  const res = await fetch("/api/data");
  const data = await res.json();

  const ctx = document.getElementById("chart").getContext("2d");
  new Chart(ctx, {
    type: "bar",
    data: {
      labels: data.years,
      datasets: [
        { label: "Recharge", data: data.recharge, backgroundColor: "teal" },
        { label: "Extraction", data: data.extraction, backgroundColor: "orange" }
      ]
    }
  });
}

loadChart();