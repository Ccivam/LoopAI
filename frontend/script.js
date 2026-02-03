let mediaRecorder;
let audioChunks = [];
let recording = false;

const button = document.getElementById("micButton");
const label = document.getElementById("label");
const player = document.getElementById("player");

button.onclick = async () => {
  if (!recording) {
    // Start recording
    recording = true;
    label.innerText = "Listening...";
    audioChunks = [];

    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);

    mediaRecorder.ondataavailable = e => {
      audioChunks.push(e.data);
    };

    mediaRecorder.onstop = async () => {
      recording = false;

      // Reset label immediately
      label.innerText = "Start Conversation";

      // If user didn’t speak anything
      if (!audioChunks.length || audioChunks[0].size === 0) {
        player.src = "/frontend/silence_response.wav"; // optional
        player.play();
        return;
      }

      // Send audio to backend
      const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
      const formData = new FormData();
      formData.append("audio", audioBlob, "input.wav");

      try {
        const response = await fetch("/voice", {
          method: "POST",
          body: formData
        });

        if (!response.ok) {
          console.error("Backend error", response.statusText);
          return;
        }

        const audioResponse = await response.blob();
        const audioURL = URL.createObjectURL(audioResponse);

        player.src = audioURL;
        player.play();
      } catch (err) {
        console.error("Error sending audio:", err);
      }
    };

    mediaRecorder.start();

  } else {
    // Stop recording immediately on double click
    mediaRecorder.stop();
     label.innerText = "Start Conversation";
  }
};
