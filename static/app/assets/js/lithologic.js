document.addEventListener('DOMContentLoaded', function () {
    const wellHeightInput = document.getElementById('well-height');
    const addIntervalButton = document.getElementById('add-interval');
    const lithologyInputs = document.getElementById('lithology-inputs');
    const deleteRowButton = document.getElementsByClassName('btn btn-outline-danger deleteRow');
    const wellSvg = document.getElementById('well-svg');

    let intervalCount = 1;

    function addInterval() {
        const newRow = document.createElement('div');
        newRow.className = 'lithology-row input-group mb-3';
        newRow.innerHTML = `

            <label for="depth-start-${intervalCount}" class="input-group-text">Dan (m):</label>
            <input type="number" class="form-control" id="depth-start-${intervalCount}" name="depth-start" min="0" max="100" value="0" onkeyup=enforceMinMax(this) />
            <label class="input-group-text" for="depth-end-${intervalCount}">Gacha (m):</label>
            <input type="number" class="form-control" id="depth-end-${intervalCount}" name="depth-end" min="0" max="100" value="0" onkeyup=enforceMinMax(this) />
            <label class="input-group-text" for="pattern-${intervalCount}">Element:</label>
            <select class="form-control" id="pattern-${intervalCount}" name="pattern">
                <option value="sandstone">Sandstone</option>
                <option value="shale">Shale</option>
            </select>
            <button class="btn btn-outline-danger deleteRow" type="button" onclick="removeLithologyRow(this)"><i class="bi bi-trash"></i></button>
        `;
        lithologyInputs.appendChild(newRow);
        intervalCount++;
    }

    function drawWell() {
        const wellHeight = parseInt(wellHeightInput.value);
        wellSvg.setAttribute('height', wellHeight*4);

        // Clear the existing SVG elements
        wellSvg.innerHTML = '';

        const intervals = document.querySelectorAll('.lithology-row');
        intervals.forEach(row => {
            const depthStart = parseInt(row.querySelector('input[name="depth-start"]').value);
            const depthEnd = parseInt(row.querySelector('input[name="depth-end"]').value);
            const pattern = row.querySelector('select[name="pattern"]').value;
            const pattern_name = row.querySelector('select[name="pattern"]').options[row.querySelector('select[name="pattern"]').selectedIndex].text;

            const rectHeight = ((depthEnd - depthStart) / wellHeight) * wellSvg.clientHeight;

            // Create the SVG pattern
            const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
            rect.setAttribute('x', 0);
            rect.setAttribute('y', (depthStart / wellHeight) * wellSvg.clientHeight);
            rect.setAttribute('width', 100);
            rect.setAttribute('height', rectHeight);
            rect.setAttribute('fill', `url(#${pattern})`);
            wellSvg.appendChild(rect);

            const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
            line.setAttribute('x1', 0);
            line.setAttribute('y1', rectHeight + (depthStart / wellHeight) * wellSvg.clientHeight);
            line.setAttribute('x2', wellSvg.clientWidth - 60);
            line.setAttribute('y2', rectHeight + (depthStart / wellHeight) * wellSvg.clientHeight) ;
            line.setAttribute('stroke', 'black');
            line.setAttribute('stroke-width', 1);
            wellSvg.appendChild(line);

            const text_val = document.createElementNS('http://www.w3.org/2000/svg', 'text');
            text_val.setAttribute('x', 200);
            text_val.setAttribute('y', rectHeight + (depthStart / wellHeight) * wellSvg.clientHeight + 5);
            text_val.setAttribute('text-anchor', 'middle');
            text_val.textContent = depthEnd; // Replace with dynamic name if needed
            wellSvg.appendChild(text_val);

            // Add the well name at the bottom
            const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
            text.setAttribute('x', 150);
            text.setAttribute('y', rectHeight + (depthStart / wellHeight) * wellSvg.clientHeight - 5);
            text.setAttribute('text-anchor', 'middle');
            text.textContent = pattern_name; // Replace with dynamic name if needed
            wellSvg.appendChild(text);
        });
    }

    wellHeightInput.addEventListener('input', drawWell);
    lithologyInputs.addEventListener('input', drawWell);
    Array.from(deleteRowButton).forEach(button => {
        button.addEventListener('click', drawWell);
    });
    addIntervalButton.addEventListener('click', addInterval);

    drawWell();  // Initial draw

    document.getElementById('download-png').addEventListener('click', function () {
        const wellSvg = document.getElementById('well-svg');
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
    
        // Serialize the SVG to a string
        const serializer = new XMLSerializer();
        const svgString = serializer.serializeToString(wellSvg);
    
        // Create a blob from the SVG string
        const svgBlob = new Blob([svgString], { type: 'image/svg+xml;charset=utf-8' });
        const url = URL.createObjectURL(svgBlob);
    
        // Create an image element to render the SVG blob
        const img = new Image();
        img.onload = function () {
            // Set the canvas size to match the SVG's dimensions
            canvas.width = wellSvg.clientWidth;
            canvas.height = wellSvg.clientHeight;
    
            // Draw the SVG onto the canvas
            ctx.drawImage(img, 0, 0);
    
            // Convert the canvas to a PNG and trigger the download
            const pngUrl = canvas.toDataURL('image/png');
            const downloadLink = document.createElement('a');
            downloadLink.href = pngUrl;
            downloadLink.download = 'well-lithology.png';
    
            // Append the link, trigger click, and remove it
            document.body.appendChild(downloadLink);
            downloadLink.click();
            document.body.removeChild(downloadLink);
    
            // Revoke the object URL
            URL.revokeObjectURL(url);
        };
    
        // Set the image source to the SVG blob URL
        img.src = url;
    });
    
    

});
