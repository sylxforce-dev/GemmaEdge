(function () {

    // ⚡ REQUIREMENT: API must be a full endpoint URI, not the root path
    const API = window.API_BASE || "http://localhost:8000/status";

    function waitForElement(id, cb) {
        const check = () => {
            const el = document.getElementById(id);
            if (el) return cb(el);
            setTimeout(check, 100);
        };
        check();
    }

    async function tick(display) {
        try {
            const r = await fetch(API, {
                method: "GET",
                headers: {
                    "Accept": "application/json"
                }
            });

            const text = await r.text();

            // 💀 SAFE JSON PARSE
            let d;
            try {
                d = JSON.parse(text);
            } catch (e) {
                display.innerHTML = `
                    <div style="color:red; font-weight:bold;">
                        JSON PARSE FAIL<br>
                        <pre>${text}</pre>
                    </div>
                `;
                return;
            }



// telemetry.js — High-Visibility Edition
// telemetry.js — Full "Electric Lime" Edition
display.innerHTML = `
    <div style="display:flex; gap:25px; font-family:monospace; font-size: 14px; align-items: center; text-shadow: 2px 2px 3px #000;">
        <div style="display:flex; flex-direction:column;">
            <span style="color:#39FF14; font-weight:bold; text-shadow: 0 0 8px rgba(57,255,20,0.6);">VRAM ${d.vram_used.toFixed(2)} GB</span>
        </div>
        <div style="display:flex; flex-direction:column;">
            <span style="color:#39FF14; font-weight:bold; text-shadow: 0 0 10px rgba(57,255,20,0.8);">GPU LOAD ${d.gpu_load}%</span>
        </div>
        <div style="display:flex; flex-direction:column;">
            <span style="color:#FFCC00; font-weight:bold; text-shadow: 0 0 5px rgba(255,204,0,0.4);">TEMP ${d.gpu_temp}°C</span>
        </div>
        <div style="display:flex; flex-direction:column;">
            <span style="color:#00FFFF; font-weight:bold; text-shadow: 0 0 8px rgba(0,255,255,0.4);">CPU ${d.cpu_load.toFixed(1)}%</span>
        </div>
        <div style="display:flex; flex-direction:column;">
            <span style="color:#ffffff; font-weight:bold;">RAM ${d.ram_used.toFixed(2)} GB</span>
        </div>
        <div style="margin-left:auto; padding: 4px 12px; background: rgba(26, 26, 26, 0.9); border-radius: 4px; border: 1px solid #444;">
            <span style="color:#f0c040; font-weight:bold; letter-spacing: 1px;">${d.active_module || "IDLE"}</span>
        </div>
    </div>
`;


        } catch (e) {
            console.error("FETCH FAILED:", e);
            display.innerHTML = `
                <div style="color:red; font-weight:bold; font-size: 10px;">
                    API OFFLINE / CONNECTION LOST
                </div>
            `;
        }
    }

    waitForElement("telemetry-display", (display) => {
        tick(display);
        setInterval(() => tick(display), 1000); // 1s värskendus
    });

})();