function processFiles() {
    const obsFile = document.getElementById("obsFile").files[0];
    const csvFile = document.getElementById("csvFile").files[0];

    if (!obsFile || !csvFile) {
        alert("Upload both files");
        return;
    }

    const r1 = new FileReader();
    const r2 = new FileReader();

    r1.onload = function(e1) {
        r2.onload = function(e2) {

            let obs = JSON.parse(e1.target.result);
            let csv = e2.target.result;

            let lots = csv.split("\n").slice(1).map(r => r.split(","));
            let lotList = [];

            let lotIndex = 0;
            let optionIndex = 1;

            let grouped = {};

            lots.forEach(r => {
                let lot = r[lotIndex];
                if (!lot) return;
                if (!grouped[lot]) grouped[lot] = [];
                grouped[lot].push(r);
            });

            Object.keys(grouped).forEach(lot => {
                let group = grouped[lot];
                if (group.length === 1) {
                    lotList.push(lot);
                } else {
                    let letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
                    group.forEach((_, i) => {
                        lotList.push(lot + "-" + letters[i]);
                    });
                }
            });

            let i = 0;

            obs.scene_order.forEach(s => {
                if (/^[0-9]+(-[A-Z])? (Transition|Video)$/.test(s.name)) {
                    if (i < lotList.length) {
                        let base = lotList[i];
                        if (s.name.includes("Transition")) {
                            s.name = base + " Transition";
                        } else {
                            s.name = base + " Video";
                            i++;
                        }
                    } else {
                        let num = String(i+1).padStart(3,"0");
                        if (s.name.includes("Transition")) {
                            s.name = "UNUSED " + num + " Transition";
                        } else {
                            s.name = "UNUSED " + num + " Video";
                            i++;
                        }
                    }
                }
            });

            let blob = new Blob([JSON.stringify(obs,null,2)], {type:"application/json"});
            let url = URL.createObjectURL(blob);

            let link = document.getElementById("downloadLink");
            link.href = url;
            link.download = "updated_scene.json";
            link.style.display = "block";
            link.innerText = "Download Updated OBS File";
        };
        r2.readAsText(csvFile);
    };
    r1.readAsText(obsFile);
}
