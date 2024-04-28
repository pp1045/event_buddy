// Show the message
document.getElementsByClassName("info-message").classList.remove("hidden");

// Schedule the message to be removed after a certain time (e.g., 3 seconds)
setTimeout(function () {
  document.getElementsByClassName("info-message").remove();
}, 30000); // 3000 milliseconds = 3 seconds
