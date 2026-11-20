// اگر آپ کے routers میں prefix مختلف ہو (مثلاً /patients یا /patient) تو یہاں ایڈجسٹ کریں
const API_BASE = "http://127.0.0.1:8000";

const ENDPOINTS = {
    patients: "/patients/",
    departments: "/departments/",
    doctors: "/doctors/",
    appointments: "/appointments/",
    pharmacy: "/pharmacies/",
    laboratory: "/laboratories/",
    billing: "/billings/"
};
// Navigation Switcher
function showSection(sectionId, element) {
    document.querySelectorAll('.content-section').forEach(sec => sec.classList.remove('active'));
    document.querySelectorAll('.nav-links li').forEach(li => li.classList.remove('active'));
    
    document.getElementById(sectionId).classList.add('active');
    element.classList.add('active');
    document.getElementById('page-title').innerText = element.innerText.trim();
}

// Toast Notification
function showToast(message) {
    const toast = document.getElementById('toast');
    toast.innerText = message;
    toast.classList.add('show');
    setTimeout(() => toast.classList.remove('show'), 3000);
}

// Generic GET Helper
async function fetchData(endpoint) {
    try {
        const res = await fetch(`${API_BASE}${endpoint}`);
        if (!res.ok) throw new Error("Failed to fetch");
        updateServerStatus(true);
        return await res.json();
    } catch (err) {
        updateServerStatus(false);
        return [];
    }
}

// Generic POST Helper
async function postData(endpoint, payload, onSuccess) {
    try {
        const res = await fetch(`${API_BASE}${endpoint}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        if (!res.ok) throw new Error("Error saving data");
        showToast("Record added successfully!");
        onSuccess();
        loadAllData();
    } catch (err) {
        showToast("Error: Check server connection or input IDs.");
    }
}

function updateServerStatus(isOnline) {
    const dot = document.getElementById('status-dot');
    const text = document.getElementById('status-text');
    if (isOnline) {
        dot.className = "dot online";
        text.innerText = "FastAPI Connected";
    } else {
        dot.className = "dot offline";
        text.innerText = "API Offline";
    }
}

// Load & Render All Tables
async function loadAllData() {
    // 1. Patients
    const patients = await fetchData(ENDPOINTS.patients);
    document.getElementById('count-patients').innerText = patients.length;
    document.getElementById('patients-table').innerHTML = patients.map(p => `
        <tr>
            <td>#${p.id}</td>
            <td><strong>${p.name}</strong></td>
            <td>${p.age}</td>
            <td>${p.gender}</td>
            <td>${p.phone}</td>
            <td>${p.address || '-'}</td>
        </tr>
    `).join('');

    // 2. Departments
    const departments = await fetchData(ENDPOINTS.departments);
    document.getElementById('departments-table').innerHTML = departments.map(d => `
        <tr><td>#${d.id}</td><td><strong>${d.name}</strong></td></tr>
    `).join('');

    // 3. Doctors
    const doctors = await fetchData(ENDPOINTS.doctors);
    document.getElementById('count-doctors').innerText = doctors.length;
    document.getElementById('doctors-table').innerHTML = doctors.map(doc => `
        <tr>
            <td>#${doc.id}</td>
            <td><strong>${doc.name}</strong></td>
            <td>Dept #${doc.department_id}</td>
            <td>${doc.specialization}</td>
            <td>${doc.phone}</td>
        </tr>
    `).join('');

    // 4. Appointments
    const appointments = await fetchData(ENDPOINTS.appointments);
    document.getElementById('count-appointments').innerText = appointments.length;
    document.getElementById('appointments-table').innerHTML = appointments.map(a => `
        <tr>
            <td>#${a.id}</td>
            <td>Patient #${a.patient_id}</td>
            <td>Doctor #${a.doctor_id}</td>
            <td>${a.date_time}</td>
        </tr>
    `).join('');

    // 5. Pharmacy
    const pharmacy = await fetchData(ENDPOINTS.pharmacy);
    document.getElementById('pharmacy-table').innerHTML = pharmacy.map(ph => `
        <tr>
            <td>#${ph.id}</td>
            <td>Patient #${ph.patient_id}</td>
            <td><strong>${ph.medicine_name}</strong></td>
            <td>${ph.quantity}</td>
            <td>Rs. ${ph.price}</td>
        </tr>
    `).join('');

    // 6. Laboratory
    const labs = await fetchData(ENDPOINTS.laboratory);
    document.getElementById('laboratory-table').innerHTML = labs.map(l => `
        <tr>
            <td>#${l.id}</td>
            <td>Patient #${l.patient_id}</td>
            <td><strong>${l.test_name}</strong></td>
            <td>${l.result || 'Pending'}</td>
            <td>Rs. ${l.price}</td>
        </tr>
    `).join('');

    // 7. Billing
    const bills = await fetchData(ENDPOINTS.billing);
    document.getElementById('count-billing').innerText = bills.length;
    document.getElementById('billing-table').innerHTML = bills.map(b => `
        <tr>
            <td>#${b.id}</td>
            <td>Patient #${b.patient_id}</td>
            <td>${b.appointment_id ? 'Appt #' + b.appointment_id : '-'}</td>
            <td><strong>Rs. ${b.amount}</strong></td>
            <td><span class="badge ${b.status.toLowerCase()}">${b.status}</span></td>
        </tr>
    `).join('');
}

// Form Submissions
document.getElementById('patient-form').addEventListener('submit', e => {
    e.preventDefault();
    postData(ENDPOINTS.patients, {
        name: document.getElementById('p-name').value,
        age: parseInt(document.getElementById('p-age').value),
        phone: document.getElementById('p-phone').value,
        gender: document.getElementById('p-gender').value,
        address: document.getElementById('p-address').value || null
    }, () => e.target.reset());
});

document.getElementById('department-form').addEventListener('submit', e => {
    e.preventDefault();
    postData(ENDPOINTS.departments, {
        name: document.getElementById('dept-name').value
    }, () => e.target.reset());
});

document.getElementById('doctor-form').addEventListener('submit', e => {
    e.preventDefault();
    postData(ENDPOINTS.doctors, {
        name: document.getElementById('doc-name').value,
        department_id: parseInt(document.getElementById('doc-dept-id').value),
        phone: document.getElementById('doc-phone').value,
        specialization: document.getElementById('doc-spec').value
    }, () => e.target.reset());
});

document.getElementById('appointment-form').addEventListener('submit', e => {
    e.preventDefault();
    postData(ENDPOINTS.appointments, {
        patient_id: parseInt(document.getElementById('app-patient-id').value),
        doctor_id: parseInt(document.getElementById('app-doctor-id').value),
        date_time: document.getElementById('app-datetime').value
    }, () => e.target.reset());
});

document.getElementById('pharmacy-form').addEventListener('submit', e => {
    e.preventDefault();
    postData(ENDPOINTS.pharmacy, {
        patient_id: parseInt(document.getElementById('phar-patient-id').value),
        medicine_name: document.getElementById('phar-med').value,
        quantity: parseInt(document.getElementById('phar-qty').value),
        price: parseInt(document.getElementById('phar-price').value)
    }, () => e.target.reset());
});

document.getElementById('lab-form').addEventListener('submit', e => {
    e.preventDefault();
    postData(ENDPOINTS.laboratory, {
        patient_id: parseInt(document.getElementById('lab-patient-id').value),
        test_name: document.getElementById('lab-test').value,
        result: document.getElementById('lab-result').value || null,
        price: parseInt(document.getElementById('lab-price').value)
    }, () => e.target.reset());
});

document.getElementById('billing-form').addEventListener('submit', e => {
    e.preventDefault();
    const appId = document.getElementById('bill-app-id').value;
    postData(ENDPOINTS.billing, {
        patient_id: parseInt(document.getElementById('bill-patient-id').value),
        appointment_id: appId ? parseInt(appId) : null,
        amount: parseInt(document.getElementById('bill-amount').value),
        status: document.getElementById('bill-status').value
    }, () => e.target.reset());
});

// Initialize on Load
window.addEventListener('DOMContentLoaded', loadAllData);