const getEl = (id) => document.getElementById(id);

let usageChartInstance = null;
let riskChartInstance = null;

async function predict() {
    const btn = document.querySelector('button[type="submit"]');
    const originalText = btn.innerHTML;
    const payload = {
        tenure: parseInt(getEl('tenure').value) || 0,
        MonthlyCharges: parseFloat(getEl('monthlyCharges').value) || 0,
        TotalCharges: parseFloat(getEl('totalCharges').value) || 0,
        SeniorCitizen: parseInt(getEl('seniorCitizen').value) || 0,
        Contract: getEl('contract').value,
        gender: getEl('gender').value,
        Partner: "No",
        Dependents: "No",
        PhoneService: "Yes",
        MultipleLines: "No",
        InternetService: "Fiber optic",
        OnlineSecurity: "No",
        OnlineBackup: "No",
        DeviceProtection: "No",
        TechSupport: "No",
        StreamingTV: "No",
        StreamingMovies: "No",
        PaperlessBilling: "Yes",
        PaymentMethod: "Electronic check"
    };

    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';
    btn.disabled = true;

    try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 5000); // 5s timeout

        const response = await fetch("https://customer-churn-prediction-j59a.onrender.com/predict",{
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
            signal: controller.signal
        });
        clearTimeout(timeoutId);

        if (!response.ok) throw new Error("API Request Failed");

        const data = await response.json();

        renderResults(data);
        renderCharts(payload, data.probability);

        const now = new Date();
        document.getElementById('lastUpdated').innerText = now.toLocaleTimeString();

    } catch (error) {
        console.error(error);
        alert("Error connecting to prediction server. Please ensure the Flask backend is running on port 5000.");
    } finally {
        btn.innerHTML = originalText;
        btn.disabled = false;
    }
}

function renderResults(data) {
    getEl('probValue').innerText = data.probability + "%";
    const riskCard = getEl('cardRisk');
    const probCard = getEl('cardProb');
    riskCard.className = 'kpi-card';
    probCard.className = 'kpi-card';

    getEl('riskValue').innerText = data.risk;

    if (data.risk === "Critical" || data.risk === "High") {
        riskCard.classList.add('risk-high');
        probCard.classList.add('risk-high');
    } else if (data.risk === "Medium") {
        riskCard.classList.add('risk-medium');
        probCard.classList.add('risk-medium');
    } else {
        riskCard.classList.add('risk-low');
        probCard.classList.add('risk-low');
    }
    const reasonText = Array.isArray(data.reasons) && data.reasons.length > 0
        ? data.reasons[0]
        : "Normal usage pattern";

    getEl('reasonValue').innerText = reasonText;
    getEl('suggestionValue').innerText = data.suggestion || "N/A";
    getEl('tipValue').innerText = data.tip || "N/A";
}


function renderCharts(inputs, probability) {

    const ctxUsage = getEl('usageChart').getContext('2d');
    const metricData = [
        inputs.tenure,
        inputs.MonthlyCharges,
        inputs.TotalCharges / 20 
    ];

    if (usageChartInstance) {
        usageChartInstance.data.datasets[0].data = metricData;
        usageChartInstance.update();
    } else {
        usageChartInstance = new Chart(ctxUsage, {
            type: 'bar',
            data: {
                labels: ['Tenure (Mos)', 'Monthly ($)', 'Total ($/20)'],
                datasets: [{
                    label: 'Current Customer',
                    data: metricData,
                    backgroundColor: ['#d04a02', '#5d4037', '#ff9800'],
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: { y: { beginAtZero: true } }
            }
        });
    }

    const ctxRisk = getEl('riskChart').getContext('2d');
    const riskData = [probability, 100 - probability];

    if (riskChartInstance) {
        riskChartInstance.data.datasets[0].data = riskData;
        riskChartInstance.update();
    } else {
        riskChartInstance = new Chart(ctxRisk, {
            type: 'doughnut',
            data: {
                labels: ['Churn Risk %', 'Retention Chance %'],
                datasets: [{
                    data: riskData,
                    backgroundColor: ['#d32f2f', '#28a745'],
                    borderWidth: 0,
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '70%',
                plugins: {
                    legend: { position: 'bottom' }
                }
            }
        });
    }
}

window.predict = predict;
window.switchMode = switchMode;
window.uploadBulk = uploadBulk;

document.addEventListener('DOMContentLoaded', () => {
    setTimeout(predict, 500);
});


function switchMode(mode) {
    const singleForm = getEl('predictionForm');
    const bulkForm = getEl('bulkForm');
    const btnSingle = getEl('btnSingle');
    const btnBulk = getEl('btnBulk');

    const singleResults = document.querySelector('.kpi-row');
    const chartResults = document.querySelector('.charts-row');
    const bulkResults = getEl('bulkResults');
    const sectionHeader = document.querySelector('.section-header');

    if (mode === 'bulk') {
        singleForm.style.display = 'none';
        bulkForm.style.display = 'block';

        btnSingle.className = 'btn btn-outline';
        btnBulk.className = 'btn';

        
        singleResults.style.display = 'none';
        chartResults.style.display = 'none';
        sectionHeader.style.display = 'none';

        bulkResults.style.display = 'block';

    } else {
        singleForm.style.display = 'block';
        bulkForm.style.display = 'none';

        btnSingle.className = 'btn';
        btnBulk.className = 'btn btn-outline';

        singleResults.style.display = 'grid';
        chartResults.style.display = 'grid';
        sectionHeader.style.display = 'flex';

        bulkResults.style.display = 'none';
    }
}

async function uploadBulk() {
    const fileInput = getEl('csvFile');
    const file = fileInput.files[0];
    if (!file) {
        alert("Please select a CSV file first.");
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    const btn = document.querySelector('#bulkForm button');
    const originalText = btn.innerHTML;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
    btn.disabled = true;

    try {
        const response = await fetch("https://customer-churn-prediction-j59a.onrender.com/upload", {
            method: "POST",
            body: formData
        });

        if (!response.ok) throw new Error("Upload Failed");

        const sortedData = await response.json();
        renderBulkTable(sortedData);

    } catch (error) {
        console.error(error);
        alert("Error processing file. Ensure it is a valid CSV.");
    } finally {
        btn.innerHTML = originalText;
        btn.disabled = false;
    }
}

function renderBulkTable(data) {
    const tbody = getEl('rankingTableBody');
    tbody.innerHTML = '';

    data.forEach((row, index) => {
        const isCritical = row.risk === 'Critical' || row.risk === 'High';
        const color = isCritical ? 'red' : (row.risk === 'Medium' ? 'orange' : 'green');
        const badge = `<span style="color: ${color}; font-weight: bold;">${row.risk}</span>`;

        const tr = document.createElement('tr');
        tr.style.borderBottom = '1px solid #eee';

        tr.innerHTML = `
            <td style="padding: 12px; font-weight: bold;">#${index + 1}</td>
            <td style="padding: 12px;">${row.customer_id}</td>
            <td style="padding: 12px;">${row.probability}%</td>
            <td style="padding: 12px;">${badge}</td>
            <td style="padding: 12px; color: #666;">${row.reasons[0] || '-'}</td>
        `;
        tbody.appendChild(tr);
    });
}
