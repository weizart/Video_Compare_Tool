console.log("Injecting JavaScript...");
document.addEventListener("DOMContentLoaded", function() {
    const syncButton = document.getElementById("sync-play-button");
    if (syncButton) {
        console.log("Sync button found. Adding onclick event...");
        syncButton.onclick = function () {
            console.log("Sync button clicked!");
            const videos = document.querySelectorAll("video");
            console.log("Found videos:", videos);
            videos.forEach((video) => {
                video.currentTime = 0; // 重置到开始
                console.log("Reset video time and attempting to play...");
                const tryPlay = () => {
                    const playPromise = video.play();
                    if (playPromise !== undefined) {
                        playPromise
                            .then(() => {
                                console.log("Video is playing");
                            })
                            .catch((error) => {
                                console.log("Playback was prevented. Trying again...");
                                requestAnimationFrame(tryPlay);
                            });
                    }
                };
                tryPlay();
            });
        };
    } else {
        console.log("Sync button not found. JavaScript did not load correctly.");
    }
});