const output = document.getElementById('output');
const synth = window.speechSynthesis;
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = new SpeechRecognition();

recognition.onstart = () => {
  speak("Hi, I am Boomer. How can I help you?");
};

recognition.onresult = (event) => {
  const transcript = event.results[0][0].transcript.toLowerCase();
  output.textContent = "You said: " + transcript;
  respondToUser(transcript);
};

function startListening() {
  recognition.start();
}

function speak(text) {
  const utter = new SpeechSynthesisUtterance(text);
  synth.speak(utter);
}

function respondToUser(command) {
  if (command.includes("hello")) {
    speak("Hello, nice talking to you. How was your day?");
  } else if (command.includes("time")) {
    const now = new Date();
    const time = now.toLocaleTimeString();
    speak("The current time is " + time);
  } else if (command.includes("open youtube")) {
    speak("Opening YouTube");
    window.open("https://www.youtube.com", "_blank");
  } else {
    speak("Sorry, I did not get that. Please try again.");
  }
}
