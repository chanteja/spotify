<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Feel Beats</title>
    <link rel="stylesheet" href="styles.css"> <!-- Link to your CSS file -->
    <script src="script.js" defer></script> <!-- Link to your JavaScript file -->
</head>
<body>
    <div class="container">
        <h1>FEEL BEATS...</h1>
        
        <div class="manual-search">
            <label for="manual-query">Or enter a manual search query:</label>
            <input type="text" id="manual-query" placeholder="Enter your query here">
        </div>

        <div class="selection">
            <label for="mood">Select Mood:</label>
            <select id="mood">
                <option value="happy">Happy</option>
                <option value="sad">Sad</option>
                <option value="relaxed">Relaxed</option>
                <option value="energetic">Energetic</option>
                <option value="romantic">Romantic</option>
                <option value="anxious">Anxious</option>
                <option value="angry">Angry</option>
                <option value="motivated">Motivated</option>
                <option value="calm">Calm</option>
                <option value="nostalgic">Nostalgic</option>
                <option value="dance">Dance</option>
            </select>

            <label for="language">Select Language:</label>
            <select id="language">
                <option value="English">English</option>
                <option value="Hindi">Hindi</option>
                <option value="Telugu">Telugu</option>
                <option value="Tamil">Tamil</option>
                <option value="Malayalam">Malayalam</option>
            </select>

            <label for="platform">Select Platform:</label>
            <select id="platform">
                <option value="YouTube">YouTube</option>
                <option value="Spotify">Spotify</option>
            </select>
        </div>

        <button id="submit">Submit</button>
        <button id="voice-command">Use Voice Command</button>
        <button id="stop-voice">Stop Voice Recognition</button>

        <div id="results"></div>
    </div>

    <script>
        // JavaScript code to handle user interactions and API calls
        document.getElementById('submit').addEventListener('click', function() {
            const mood = document.getElementById('mood').value;
            const language = document.getElementById('language').value;
            const platform = document.getElementById('platform').value;
            const manualQuery = document.getElementById('manual-query').value;

            // Here you would typically make an API call to your backend
            console.log(`Mood: ${mood}, Language: ${language}, Platform: ${platform}, Manual Query: ${manualQuery}`);
        });

        document.getElementById('voice-command').addEventListener('click', function() {
            // Implement voice command functionality
            console.log("Voice command activated");
        });

        document.getElementById('stop-voice').addEventListener('click', function() {
            // Implement stop voice recognition functionality
            console.log("Voice recognition stopped");
        });
    </script>
</body>
</html>
