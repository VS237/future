const themeBtn = document.getElementById('theme-switch');
    const html = document.documentElement;

    // Load saved theme
    const savedTheme = localStorage.getItem('theme') || 'dark';
    html.setAttribute('data-theme', savedTheme);
    updateIcon(savedTheme);

    themeBtn.addEventListener('click', () => {
        const currentTheme = html.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        html.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateIcon(newTheme);
    });

    function updateIcon(theme) {
        const icon = themeBtn.querySelector('i');
        icon.className = theme === 'dark' ? 'fa-solid fa-sun' : 'fa-solid fa-moon';
    }

    function openModal(title, htmlContent) {
    document.getElementById('modal-title').innerText = title;
    document.getElementById('modal-body').innerHTML = htmlContent;
    document.getElementById('detail-modal').style.display = 'flex';
}

function closeModal() {
    document.getElementById('detail-modal').style.display = 'none';
}

function viewCustomer(name, user, email, phone, city, address) {
    const content = `
        <div class="detail-item"><span class="detail-label">Full Name</span><span class="detail-value">${name}</span></div>
        <div class="detail-item"><span class="detail-label">Username</span><span class="detail-value" style="color:var(--accent)">${user}</span></div>
        <div class="detail-item"><span class="detail-label">Email</span><span class="detail-value">${email}</span></div>
        <div class="detail-item"><span class="detail-label">Phone</span><span class="detail-value">${phone}</span></div>
        <div class="detail-item"><span class="detail-label">Location</span><span class="detail-value">${city}</span></div>
        <div class="detail-item"><span class="detail-label">Full Address</span><span class="detail-value">${address}</span></div>
    `;
    openModal('Customer Profile', content);
}

function viewMessage(sender, subject, message, backupEmail) {
    const content = `
        <div class="detail-item"><span class="detail-label">From</span><span class="detail-value">${sender} (${backupEmail})</span></div>
        <div class="detail-item"><span class="detail-label">Subject Vector</span><span class="detail-value" style="color:var(--accent)">${subject}</span></div>
        <div class="detail-item"><span class="detail-label">Full Data Stream</span><span class="detail-value">${message}</span></div>
    `;
    openModal('Message Intel', content);
}