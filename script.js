document.addEventListener('DOMContentLoaded', function() {
    const databaseSelect = document.getElementById('database-select');
    const startTimeInput = document.getElementById('startTime');
    const endTimeInput = document.getElementById('endTime');
    const recordsInput = document.getElementById('records');
    const recordsButton = document.querySelector('button[id="show-data-button"]');
    const submitButton = document.querySelector('button[id="download"]');
    const refreshButton = document.getElementById('refresh');

    function hideAllTables() {
        document.getElementById('5-Mins').style.display = 'none';
        document.getElementById('30-Mins').style.display = 'none';
        document.getElementById('60-Mins').style.display = 'none';
        document.getElementById('1-Day').style.display = 'none';
    }

    hideAllTables();
    function showError(message) {
        const errorDiv = document.getElementById('error-message');
        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
    }

    recordsButton.addEventListener('click', function(event) {
        event.preventDefault();
        hideAllTables();
        errorDiv = document.getElementById('error-message');
        errorDiv.style.display = 'none';
        const selectedValue = databaseSelect.value;
        records = recordsInput.value;
        TableName = getTableName(selectedValue);
        console.log(`TableName: ${TableName}, Records: ${records}`);

        if (TableName && records) {
            fetchDataForTable(TableName, records);
            document.getElementById(`${selectedValue}`).style.display = 'block';
        } else {
            showError('Please select a valid option and specify the number of records.');
        }
    });

    function getTableName(selectedValue) {
        const tableMapping = {
        '5-Mins': 'Apollo_5MINS_interval',
        '30-Mins': 'Apollo_30MINS_interval',
        '60-Mins': 'Apollo_60MINS_interval',
        '1-Day': 'Apollo_1DAY_interval'
        }
        return tableMapping[selectedValue];
    }

    function fetchDataForTable(TableName, records) {
        const url = `http://localhost:5000/get-data?TableName=${TableName}&Records=${records}`;
        fetch(url)
            .then(response => {
                if (!response.ok) throw new Error(`Server returned ${response.status}: ${response.statusText}`);
                return response.json();
            })
            .then(data => {
                populateTable(data, TableName);
            })
            .catch(error => {
                console.error('Error fetching data:', error);
                showError(error.message);
            });
    }

    function formatTime(dateTimeStr) {
        // Create a date object from the dateTimeStr
        const date = new Date(dateTimeStr);
        // Manually construct the date string
        const year = date.getUTCFullYear().toString().slice(-2); // Get the last two digits of the year
        const month = (date.getUTCMonth() + 1).toString().padStart(2, '0'); // Get the month and pad with leading 0 if necessary
        const day = date.getUTCDate().toString().padStart(2, '0'); // Get the day and pad with leading 0 if necessary
        const hours = date.getUTCHours().toString().padStart(2, '0'); // Get the hour and pad with leading 0 if necessary
        const minutes = date.getUTCMinutes().toString().padStart(2, '0'); // Get the minutes and pad with leading 0 if necessary

        // Combine the parts into a YY-MM-DD HH:MM format
        return `${year}/${month}/${day} ${hours}:${minutes}`;
    }

    function populateTable(dataObject, tableName) {
        console.log('Received data for table:', tableName, dataObject); // Check the raw data received

        // Make sure dataObject has the structure we expect
        if (dataObject && Array.isArray(dataObject.columns) && Array.isArray(dataObject.data)) {
            const selectedValue = databaseSelect.value;
            const tableId = `${selectedValue}-table`;
            const table = document.getElementById(tableId);

            if (!table) {
                console.error('Table not found for:', tableId);
                showError(`Table not found for: ${tableId}`); // Use showError to display error on the page
                return;
            }


            table.innerHTML = ''; // Clear existing table data

            // Create a header row using the column names from dataObject.columns
            const header = table.createTHead();
            const headerRow = header.insertRow();
            dataObject.columns.forEach(colName => {
                const headerCell = document.createElement("th");
                headerCell.textContent = colName.replace(/_/g, ' ');
                headerRow.appendChild(headerCell);
            });

            // Create a row for each object in the data array from dataObject.data
            const tbody = document.createElement('tbody');
            dataObject.data.forEach(item => {
                const row = tbody.insertRow();
                dataObject.columns.forEach(colName => {
                    const cell = row.insertCell();
                    const value = item[colName];
                    // Format the 'Time' field, if present, using the formatTime function
                    cell.textContent = (colName.toLowerCase() === 'time' && value) ? formatTime(value) : value;
                });
            });
            table.appendChild(tbody);
        } else {
            console.error('Data object is not valid or is empty', dataObject);
            showError('Data object is not valid or is empty'); // Display error on the page
        }
    }

    function triggerDownload(url, filename) {
        fetch(url)
            .then(response => {
                if (!response.ok) throw new Error(`Error: ${response.statusText}`);
                return response.blob();
            })
            .then(blob => {
                const downloadUrl = URL.createObjectURL(blob);
                const link = document.createElement("a");
                link.href = downloadUrl;
                link.download = filename;
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            })
            .catch(error => console.error('Error downloading data:', error));
    }

    submitButton.addEventListener('click', function(event) {
        event.preventDefault();
        const startTime = startTimeInput.value;
        const endTime = endTimeInput.value;
        const selectedValue = databaseSelect.value;
        const tableName = getTableName(selectedValue);
        const filename = `${selectedValue.replace(/\s+/g, '_').toLowerCase()}_data.csv`;
        const downloadUrl = `http://localhost:5000/download-data?TableName=${tableName}&StartTime=${startTime}&EndTime=${endTime}`;

        triggerDownload(downloadUrl, filename);
    });
})