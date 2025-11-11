document.addEventListener('DOMContentLoaded', () => {
    // Element selections
    const jsonFileInput = document.getElementById('jsonFile');
    const jsonFileOverlayInput = document.getElementById('jsonFileOverlay');
    const hadithSelector = document.getElementById('hadithSelector');
    const hadithDisplay = document.getElementById('hadithDisplay');
    const newPropContentInput = document.getElementById('newPropContent');
    const darkModeToggle = document.getElementById('darkModeToggle');
    const darkModeIcon = document.getElementById('darkModeIcon');
    const backToTopBtn = document.getElementById('backToTopBtn');
    const guideBtn = document.getElementById('guideBtn');
    const guideModal = document.getElementById('guideModal');
    const closeGuideModal = document.getElementById('closeGuideModal');
    const fileUploadOverlay = document.getElementById('fileUploadOverlay');
    const mainContainer = document.getElementById('mainContainer');
    const hadithSelectorContainer = document.getElementById('hadithSelectorContainer');
    const progressBarContainer = document.getElementById('progressBarContainer');
    const navButtonsTop = document.getElementById('navButtonsTop');

    let sections = [];
    let currentHadithIndex = -1;

    // --- Event Listeners ---
    jsonFileInput.addEventListener('change', handleFileUpload);
    jsonFileOverlayInput.addEventListener('change', handleFileUpload);
    hadithSelector.addEventListener('change', displayHadith);
    darkModeToggle.addEventListener('click', toggleDarkMode);
    guideBtn.addEventListener('click', () => guideModal.style.display = 'flex');
    closeGuideModal.addEventListener('click', () => guideModal.style.display = 'none');
    window.addEventListener('scroll', handleScroll);
    backToTopBtn.addEventListener('click', scrollToTop);

    // --- Functions ---

    function handleFileUpload(event) {
        const file = event.target.files[0];
        if (file && file.type === "application/json") {
            const reader = new FileReader();
            reader.onload = (e) => {
                try {
                    sections = JSON.parse(e.target.result);
                    if (!Array.isArray(sections)) throw new Error("JSON is not an array.");
                    populateHadithSelector();
                    fileUploadOverlay.classList.add('hidden');
                    mainContainer.classList.remove('disabled-ui');
                    hadithSelectorContainer.style.display = 'flex';
                    progressBarContainer.style.display = 'block';
                    navButtonsTop.style.display = 'flex';
                    showToast('موفقیت', 'فایل با موفقیت بارگذاری شد.', 'success');
                } catch (error) {
                    showToast('خطا', `فایل JSON نامعتبر است: ${error.message}`, 'error');
                }
            };
            reader.readAsText(file);
        }
    }

    function populateHadithSelector() {
        hadithSelector.innerHTML = '';
        sections.forEach((section, index) => {
            const option = document.createElement('option');
            option.value = index;
            // For new format, use section IDs
            const section1Id = section.section_1_id || `بخش ۱`;
            const section2Id = section.section_2_id || `بخش ۲`;
            option.textContent = `مقایسه ${section1Id} و ${section2Id}`;
            hadithSelector.appendChild(option);
        });
        currentHadithIndex = 0;
        displayHadith();
    }

    function displayHadith() {
        currentHadithIndex = parseInt(hadithSelector.value);
        if (currentHadithIndex >= 0 && currentHadithIndex < sections.length) {
            const section = sections[currentHadithIndex];
            hadithDisplay.innerHTML = `
                <div class="section-content">
                    <h3>بخش اول</h3>
                    <p>${section.section_1_content || '(محتوای بخش اول موجود نیست)'}</p>
                    <h3>قوانین بخش اول</h3>
                    <p>${section.section_1_rules || '(قوانین بخش اول موجود نیست)'}</p>
                    <h3>بخش دوم</h3>
                    <p>${section.section_2_content || '(محتوای بخش دوم موجود نیست)'}</p>
                    <h3>قوانین بخش دوم</h3>
                    <p>${section.section_2_rules || '(قوانین بخش دوم موجود نیست)'}</p>
                    <h3>تحلیل رابطه</h3>
                    <p>${section.reason || section.explanation || '(تحلیل رابطه موجود نیست)'}</p>
                </div>
            `;
            updateHadithCounter();
            updateProgressBar();
        }
    }

    function renderPropositions() { /* ... implementation needed ... */ }
    function renderRelations() { /* ... implementation needed ... */ }
    function renderGraph() { /* ... implementation needed ... */ }

    window.addProposition = function() {
        const content = newPropContentInput.value.trim();
        if (!content) {
            showToast('هشدار', 'لطفاً محتوای گزاره را وارد کنید.', 'warning');
            return;
        }
        // Propositions not supported in the new structure
        newPropContentInput.value = '';
        showToast('هشدار', 'افزودن گزاره در ساختار جدید پشتیبانی نمی‌شود.', 'warning');
    }

    window.navigateHadith = function(direction) {
        let newIndex = currentHadithIndex + direction;
        if (newIndex >= 0 && newIndex < sections.length) {
            currentHadithIndex = newIndex;
            hadithSelector.value = currentHadithIndex;
            displayHadith();
        }
    }

    function updateHadithCounter() {
        const counter = document.getElementById('hadithCounter');
        if (counter) {
            counter.textContent = `(${currentHadithIndex + 1} از ${sections.length})`;
        }
    }

    function updateProgressBar() {
        const progressBar = document.getElementById('progressBar');
        if (progressBar) {
            const progress = sections.length > 0 ? ((currentHadithIndex + 1) / sections.length) * 100 : 0;
            progressBar.style.width = `${progress}%`;
        }
    }

    function toggleDarkMode() {
        document.body.classList.toggle('dark-mode');
        const isDarkMode = document.body.classList.contains('dark-mode');
        darkModeIcon.textContent = isDarkMode ? '☀️' : '🌙';
        localStorage.setItem('darkMode', isDarkMode);
        // Re-render graph for dark mode
        renderGraph();
    }

    // Check for saved dark mode preference
    if (localStorage.getItem('darkMode') === 'true') {
        toggleDarkMode();
    }

    function handleScroll() {
        if (window.scrollY > 300) {
            backToTopBtn.style.display = 'block';
        } else {
            backToTopBtn.style.display = 'none';
        }
    }

    function scrollToTop() {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    window.showToast = function(title, message, type = 'info') {
        const container = document.getElementById('toastContainer') || createToastContainer();
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;

        const icons = { success: '✅', error: '❌', warning: '⚠️', info: 'ℹ️' };

        toast.innerHTML = `
            <div class="toast-icon">${icons[type]}</div>
            <div class="toast-content">
                <div class="toast-title">${title}</div>
                <div class="toast-message">${message}</div>
            </div>
        `;

        container.appendChild(toast);
        setTimeout(() => toast.classList.add('show'), 100); // Animate in

        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300); // Remove from DOM after animation
        }, 5000);
    }

    function createToastContainer() {
        const container = document.createElement('div');
        container.id = 'toastContainer';
        document.body.appendChild(container);
        return container;
    }

    // Initial state setup
    mainContainer.classList.add('disabled-ui');
    hadithSelectorContainer.style.display = 'none';
    progressBarContainer.style.display = 'none';
    navButtonsTop.style.display = 'none';
});