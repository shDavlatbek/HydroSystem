document.addEventListener('DOMContentLoaded', function () {
    const wellHeightInput = document.getElementById('well-height');
    const addIntervalButton = document.getElementById('add-interval');
    const lithologyInputs = document.getElementById('lithology-inputs');
    let deleteRowButton = document.querySelectorAll('.deleteRow');
    const wellSvg = document.getElementById('well-svg');

    let intervalCount = 1;

    function addInterval() {
        const newRow = document.createElement('div');
        newRow.className = 'lithology-row input-group mb-3';
        newRow.innerHTML = `

            <label for="depth-start-${intervalCount}" class="input-group-text">Dan (m):</label>
            <input type="number" class="form-control" id="depth-start-${intervalCount}" name="depth-start" min="0" max="100" value="0" />
            <label class="input-group-text" for="depth-end-${intervalCount}">Gacha (m):</label>
            <input type="number" class="form-control" id="depth-end-${intervalCount}" name="depth-end" min="0" max="100" value="0" />
            <label class="input-group-text" for="pattern-${intervalCount}">Element:</label>
            <select class="form-control" id="pattern-${intervalCount}" name="pattern">
                <option value="sandstone">Sandstone</option>
                <option value="shale">Shale</option>
            </select>
            <button class="btn btn-outline-danger deleteRow" type="button"><i class="bi bi-trash"></i></button>
        `;
        lithologyInputs.appendChild(newRow);
        deleteRowButton = document.querySelectorAll('.deleteRow')
        intervalCount++;
    }

    function removeLithologyRow(button) {
        // Find the parent element with class 'lithology-row' and remove it
        const row = button.closest('.lithology-row');
        if (row) {
            // row.remove();
            lithologyInputs.removeChild(row)
        }
    }

    function enforceMinMax(el) {
        if (el.value != "") {
          if (parseInt(el.value) < parseInt(el.min)) {
            el.value = el.min;
          }
          if (parseInt(el.value) > parseInt(el.max)) {
            el.value = el.max;
          }
        }
      }

    function drawWell() {
        const wellHeight = parseInt(wellHeightInput.value);
        wellSvg.setAttribute('height', wellHeight*5);

        // Clear the existing SVG elements
        wellSvg.innerHTML = `
        
        <rect x="0" y="0" width="100" height="500" fill="none" stroke="black" stroke-width="1"></rect>
        <g font-size="10" fill="black">
            <!-- Labels and lines for scale -->
            <!-- Scale from 0 to 100 in steps of 10 -->
            <line x1="0" y1="0" x2="-20" y2="0" stroke="black" stroke-width="1"></line>
            <text x="-25" y="4" text-anchor="middle">0</text>

            <line x1="0" y1="50" x2="-20" y2="50" stroke="black" stroke-width="1"></line>
            <text x="-27" y="54" text-anchor="middle">10</text>

            <line x1="0" y1="100" x2="-20" y2="100" stroke="black" stroke-width="1"></line>
            <text x="-27" y="104" text-anchor="middle">20</text>

            <line x1="0" y1="150" x2="-20" y2="150" stroke="black" stroke-width="1"></line>
            <text x="-27" y="154" text-anchor="middle">30</text>

            <line x1="0" y1="200" x2="-20" y2="200" stroke="black" stroke-width="1"></line>
            <text x="-27" y="204" text-anchor="middle">40</text>

            <line x1="0" y1="250" x2="-20" y2="250" stroke="black" stroke-width="1"></line>
            <text x="-27" y="254" text-anchor="middle">50</text>

            <line x1="0" y1="300" x2="-20" y2="300" stroke="black" stroke-width="1"></line>
            <text x="-27" y="304" text-anchor="middle">60</text>

            <line x1="0" y1="350" x2="-20" y2="350" stroke="black" stroke-width="1"></line>
            <text x="-27" y="354" text-anchor="middle">70</text>

            <line x1="0" y1="400" x2="-20" y2="400" stroke="black" stroke-width="1"></line>
            <text x="-27" y="404" text-anchor="middle">80</text>

            <line x1="0" y1="450" x2="-20" y2="450" stroke="black" stroke-width="1"></line>
            <text x="-27" y="454" text-anchor="middle">90</text>

            <line x1="0" y1="500" x2="-20" y2="500" stroke="black" stroke-width="1"></line>
            <text x="-30" y="504" text-anchor="middle">100</text>

        </g>
        `;
                  
        


        const intervals = document.querySelectorAll('.lithology-row');
        intervals.forEach(row => {
            
            const depthStart = parseInt(row.querySelector('input[name="depth-start"]').value);
            const depthEnd = parseInt(row.querySelector('input[name="depth-end"]').value);
            const pattern = row.querySelector('select[name="pattern"]').value;
            const pattern_name = row.querySelector('select[name="pattern"]').options[row.querySelector('select[name="pattern"]').selectedIndex].text;

            const rectHeight = ((depthEnd - depthStart) / wellHeight) * wellSvg.clientHeight;

            // Create the SVG pattern
            const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
            const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
            const text_val = document.createElementNS('http://www.w3.org/2000/svg', 'text');
            const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
           
                if (isNaN(depthStart) || isNaN(wellHeight) || isNaN(rectHeight)) {
                    
                } else {
                    rect.setAttribute('x', 0);
                    rect.setAttribute('y', (depthStart / wellHeight) * wellSvg.clientHeight);
                    rect.setAttribute('width', 100);
                    rect.setAttribute('height', rectHeight);
                    rect.setAttribute('fill', `url(#${pattern})`);
                    wellSvg.appendChild(rect);
                
                    line.setAttribute('x1', 0);
                    line.setAttribute('y1', rectHeight + (depthStart / wellHeight) * wellSvg.clientHeight);
                    line.setAttribute('x2', wellSvg.clientWidth - 60);
                    line.setAttribute('y2', rectHeight + (depthStart / wellHeight) * wellSvg.clientHeight);
                    line.setAttribute('stroke', 'black');
                    line.setAttribute('stroke-width', 1);
                    wellSvg.appendChild(line);
                
                    text_val.setAttribute('x', 210);
                    text_val.setAttribute('y', rectHeight + (depthStart / wellHeight) * wellSvg.clientHeight + 5);
                    text_val.setAttribute('text-anchor', 'middle');
                    text_val.textContent = depthEnd; // Replace with dynamic name if needed
                    wellSvg.appendChild(text_val);
                
                    // Add the well name at the bottom
                    text.setAttribute('x', 150);
                    text.setAttribute('y', rectHeight + (depthStart / wellHeight) * wellSvg.clientHeight - 5);
                    text.setAttribute('text-anchor', 'middle');
                    text.textContent = pattern_name; // Replace with dynamic name if needed
                    wellSvg.appendChild(text);
                }
            
                
            
            
        });
    }

    wellHeightInput.addEventListener('input', drawWell);
    lithologyInputs.addEventListener('input', e => {
        drawWell();
        console.log(e);
        
        enforceMinMax(e);
    });
    deleteRowButton.forEach(el => el.addEventListener('click', event => {
        drawWell();
        removeLithologyRow(el);
    }));
    addIntervalButton.addEventListener('click', event => {
        addInterval();
        deleteRowButton.forEach(el => el.addEventListener('click', event => {
            drawWell();
            removeLithologyRow(el);
        }));
    });

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
