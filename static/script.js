<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Excavator Parts Finder</title>
</head>
<body>
    <h1>Find Excavator Parts</h1>
    <select id="makeDropdown">
        <option value="">Select Make</option>
    </select>
    <select id="modelDropdown">
        <option value="">Select Model</option>
    </select>
    <select id="versionDropdown">
        <option value="">Select Version</option>
    </select>
    <select id="categoryDropdown">
        <option value="">Select Category</option>
    </select>
    <button id="searchButton">Search Parts</button>
    <ul id="partsList"></ul>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const makeDropdown = document.getElementById('makeDropdown');
            const modelDropdown = document.getElementById('modelDropdown');
            const versionDropdown = document.getElementById('versionDropdown');
            const categoryDropdown = document.getElementById('categoryDropdown');
            const partsList = document.getElementById('partsList');
            const searchButton = document.getElementById('searchButton');

            // Fetch dropdown data from the server
            function fetchDropdownData() {
                fetch('/api/dropdowns')
                    .then(response => response.json())
                    .then(data => {
                        populateDropdown(makeDropdown, data.makes);
                        populateDropdown(modelDropdown, data.models);
                        populateDropdown(versionDropdown, data.versions);
                        populateDropdown(categoryDropdown, data.categories);
                    })
                    .catch(error => console.error('Error fetching dropdown data:', error));
            }

            // Populate dropdown options
            function populateDropdown(dropdown, options) {
                dropdown.innerHTML = '<option value="">Select</option>'; // Clear existing options and add default option
                options.forEach(option => {
                    const opt = document.createElement('option');
                    opt.value = option.name;
                    opt.textContent = option.name;
                    dropdown.appendChild(opt);
                });
            }

            // Fetch parts based on the selected dropdown options
            searchButton.addEventListener('click', function() {
                const make = makeDropdown.value;
                const model = modelDropdown.value;
                const version = versionDropdown.value;
                const category = categoryDropdown.value;

                fetch(`/api/parts?make=${encodeURIComponent(make)}&model=${encodeURIComponent(model)}&version=${encodeURIComponent(version)}&category=${encodeURIComponent(category)}`)
                    .then(response => response.json())
                    .then(parts => {
                        displayParts(parts);
                    })
                    .catch(error => console.error('Error fetching parts:', error));
            });

            // Display parts in the list
            function displayParts(parts) {
                partsList.innerHTML = ''; // Clear existing parts
                parts.forEach(part => {
                    const li = document.createElement('li');
                    li.textContent = `Part: ${part['Part']}, Part Number: ${part['Part Number']}`;
                    partsList.appendChild(li);
                });
            }

            // Initialize the app by fetching dropdown data
            fetchDropdownData();
        });
    </script>
</body>
</html>
