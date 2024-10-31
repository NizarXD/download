document.getElementById("downloadForm").addEventListener("submit", function(event) {
    event.preventDefault();
    const videoURL = document.getElementById("videoURL").value;
    document.getElementById("statusMessage").textContent = `Mencoba mengunduh video dari ${videoURL}`;
    // Tambahkan proses download di sini
});
