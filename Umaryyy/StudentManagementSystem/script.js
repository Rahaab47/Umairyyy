/**
 * Advanced JavaScript for Student Management System
 * Enhanced interactivity, animations, and data handling
 */

class StudentManager {
    constructor() {
        this.students = [
            { id: 1001, name: 'Alice Johnson', age: 18, grade: 89.5, attendance: 95.2, email: 'alice@example.com', status: 'excellent' },
            { id: 1002, name: 'Bob Smith', age: 19, grade: 76.3, attendance: 88.7, email: 'bob@example.com', status: 'good' },
            { id: 1003, name: 'Carol Davis', age: 17, grade: 42.8, attendance: 75.3, email: 'carol@example.com', status: 'at-risk' },
            { id: 1004, name: 'David Wilson', age: 20, grade: 94.1, attendance: 98.5, email: 'david@example.com', status: 'excellent' },
            { id: 1005, name: 'Eva Brown', age: 18, grade: 67.9, attendance: 82.1, email: 'eva@example.com', status: 'good' }
        ];
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.renderStats();
        this.renderStudents();
        this.animateElements();
    }

    setupEventListeners() {
        // Form submission
        document.getElementById('studentForm')?.addEventListener('submit', (e) => this.handleFormSubmit(e));
        
        // Action buttons
        document.querySelectorAll('.action-btn.edit').forEach(btn => {
            btn.addEventListener('click', (e) => this.handleEdit(e));
        });
        
        document.querySelectorAll('.action-btn.delete').forEach(btn => {
            btn.addEventListener('click', (e) => this.handleDelete(e));
        });
        
        // Export button
        document.querySelector('.btn-primary[title="Download Report"]')?.addEventListener('click', () => this.exportData());
        
        // Search functionality
        const searchInput = document.getElementById('searchInput');
        if (searchInput) {
            searchInput.addEventListener('input', (e) => this.searchStudents(e.target.value));
        }
    }

    handleFormSubmit(e) {
        e.preventDefault();
        
        const formData = new FormData(e.target);
        const studentData = {
            id: parseInt(formData.get('studentId')),
            name: formData.get('name'),
            age: parseInt(formData.get('age')),
            grade: parseFloat(formData.get('grade')),
            attendance: parseFloat(formData.get('attendance')),
            email: formData.get('email') || '',
            status: this.calculateStatus(parseFloat(formData.get('grade')), parseFloat(formData.get('attendance')))
        };

        // Validate data
        if (!studentData.id || !studentData.name || isNaN(studentData.age) || 
            isNaN(studentData.grade) || isNaN(studentData.attendance)) {
            this.showNotification('Please fill in all required fields with valid data.', 'error');
            return;
        }

        if (studentData.grade < 0 || studentData.grade > 100) {
            this.showNotification('Grade must be between 0 and 100.', 'error');
            return;
        }

        if (studentData.attendance < 0 || studentData.attendance > 100) {
            this.showNotification('Attendance must be between 0 and 100%.', 'error');
            return;
        }

        // Add student
        this.students.push(studentData);
        this.renderStudents();
        this.renderStats();
        
        // Reset form
        e.target.reset();
        this.showNotification(`Student "${studentData.name}" added successfully!`, 'success');
    }

    handleEdit(e) {
        const row = e.target.closest('tr');
        const id = parseInt(row.cells[0].textContent);
        const student = this.students.find(s => s.id === id);
        
        if (student) {
            // In a real app, this would open an edit modal
            this.showNotification(`Editing student: ${student.name}`, 'info');
        }
    }

    handleDelete(e) {
        const row = e.target.closest('tr');
        const id = parseInt(row.cells[0].textContent);
        
        if (confirm(`Are you sure you want to delete student ID ${id}?`)) {
            this.students = this.students.filter(s => s.id !== id);
            this.renderStudents();
            this.renderStats();
            this.showNotification('Student deleted successfully.', 'success');
        }
    }

    calculateStatus(grade, attendance) {
        if (grade >= 85 && attendance >= 90) return 'excellent';
        if (grade >= 70 && attendance >= 80) return 'good';
        if (grade >= 50 && attendance >= 70) return 'average';
        return 'at-risk';
    }

    renderStats() {
        const totalStudents = this.students.length;
        const avgGrade = this.students.reduce((sum, s) => sum + s.grade, 0) / totalStudents;
        const avgAttendance = this.students.reduce((sum, s) => sum + s.attendance, 0) / totalStudents;
        const failingStudents = this.students.filter(s => s.grade < 50).length;
        const topPerformer = this.students.reduce((max, s) => s.grade > max.grade ? s : max);

        // Update stats cards
        document.querySelector('.card:nth-child(1) .stat-value')?.textContent = totalStudents;
        document.querySelector('.card:nth-child(2) .stat-value')?.textContent = avgGrade.toFixed(1);
        document.querySelector('.card:nth-child(3) .stat-value')?.textContent = `${avgAttendance.toFixed(1)}%`;
        document.querySelector('.card:nth-child(4) .stat-value')?.textContent = '24';

        // Update reports cards
        document.querySelector('.card:nth-child(5) .stat-value')?.textContent = failingStudents;
        document.querySelector('.card:nth-child(6) .stat-value')?.textContent = topPerformer.name;
        document.querySelector('.card:nth-child(6) .stat-label')?.textContent = `Grade: ${topPerformer.grade} | Attendance: ${topPerformer.attendance}%`;
        
        // Update low attendance card
        const lowAttendance = this.students.filter(s => s.attendance < 80).length;
        document.querySelector('.card:nth-child(7) .stat-value')?.textContent = lowAttendance;
    }

    renderStudents() {
        const tbody = document.querySelector('tbody');
        if (!tbody) return;

        tbody.innerHTML = this.students.map(student => `
            <tr>
                <td>${student.id}</td>
                <td>${student.name}</td>
                <td>${student.age}</td>
                <td>${student.grade.toFixed(1)}</td>
                <td>${student.attendance.toFixed(1)}%</td>
                <td><span class="status-badge status-${student.status}">${this.getStatusLabel(student.status)}</span></td>
                <td>
                    <button class="action-btn edit" title="Edit"><i class="fas fa-edit"></i></button>
                    <button class="action-btn delete" title="Delete"><i class="fas fa-trash"></i></button>
                </td>
            </tr>
        `).join('');
    }

    getStatusLabel(status) {
        switch (status) {
            case 'excellent': return 'Excellent';
            case 'good': return 'Good';
            case 'average': return 'Average';
            case 'at-risk': return 'At Risk';
            default: return 'Unknown';
        }
    }

    searchStudents(query) {
        if (!query.trim()) {
            this.renderStudents();
            return;
        }

        const filtered = this.students.filter(student =>
            student.name.toLowerCase().includes(query.toLowerCase()) ||
            student.id.toString().includes(query)
        );

        const tbody = document.querySelector('tbody');
        if (tbody) {
            tbody.innerHTML = filtered.map(student => `
                <tr>
                    <td>${student.id}</td>
                    <td>${student.name}</td>
                    <td>${student.age}</td>
                    <td>${student.grade.toFixed(1)}</td>
                    <td>${student.attendance.toFixed(1)}%</td>
                    <td><span class="status-badge status-${student.status}">${this.getStatusLabel(student.status)}</span></td>
                    <td>
                        <button class="action-btn edit" title="Edit"><i class="fas fa-edit"></i></button>
                        <button class="action-btn delete" title="Delete"><i class="fas fa-trash"></i></button>
                    </td>
                </tr>
            `).join('');
        }
    }

    exportData() {
        // In a real app, this would generate and download a CSV file
        this.showNotification('Exporting data to CSV...', 'info');
        
        // Simulate export process
        setTimeout(() => {
            this.showNotification('Data exported successfully!', 'success');
        }, 1500);
    }

    showNotification(message, type) {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <i class="fas fa-${this.getIconForType(type)}"></i>
                <span>${message}</span>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        // Auto-remove after 3 seconds
        setTimeout(() => {
            notification.classList.add('fade-out');
            setTimeout(() => {
                notification.remove();
            }, 300);
        }, 3000);
    }

    getIconForType(type) {
        switch (type) {
            case 'success': return 'check-circle';
            case 'error': return 'times-circle';
            case 'info': return 'info-circle';
            default: return 'info-circle';
        }
    }

    animateElements() {
        // Add staggered animation to cards
        const cards = document.querySelectorAll('.card');
        cards.forEach((card, index) => {
            setTimeout(() => {
                card.classList.add('animate');
                card.classList.add('appear');
            }, 200 * index);
        });

        // Add animation to table rows
        const rows = document.querySelectorAll('tbody tr');
        rows.forEach((row, index) => {
            setTimeout(() => {
                row.style.opacity = '1';
                row.style.transform = 'translateX(0)';
            }, 300 + 100 * index);
        });
    }
}

// Initialize the student manager when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new StudentManager();

    // Add search input if it doesn't exist
    const headerContent = document.querySelector('.header-content');
    if (headerContent) {
        const searchDiv = document.createElement('div');
        searchDiv.innerHTML = `
            <div style="position: relative;">
                <input type="text" id="searchInput" placeholder="Search students..." 
                       style="padding: 12px 20px 12px 40px; border-radius: 50px; border: 2px solid rgba(0,0,0,0.1); 
                              font-size: 0.9rem; width: 250px; background: white;">
                <i class="fas fa-search" style="position: absolute; left: 15px; top: 50%; transform: translateY(-50%); color: #95a5a6;"></i>
            </div>
        `;
        headerContent.insertBefore(searchDiv, headerContent.children[1]);
    }

    // Add smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                window.scrollTo({
                    top: target.offsetTop - 80,
                    behavior: 'smooth'
                });
            }
        });
    });
});

// Notification styles
const styleSheet = document.createElement('style');
styleSheet.textContent = `
.notification {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 1000;
    padding: 16px 24px;
    border-radius: 12px;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
    transform: translateX(120%);
    transition: transform 0.4s ease, opacity 0.3s ease;
    display: flex;
    align-items: center;
    gap: 12px;
    font-weight: 500;
}

.notification.appear {
    transform: translateX(0);
}

.notification.fade-out {
    opacity: 0;
    transform: translateX(120%);
}

.notification-success {
    background: linear-gradient(135deg, #27ae60, #219653);
    color: white;
}

.notification-error {
    background: linear-gradient(135deg, #e74c3c, #c0392b);
    color: white;
}

.notification-info {
    background: linear-gradient(135deg, #3498db, #2980b9);
    color: white;
}

.notification-content {
    display: flex;
    align-items: center;
    gap: 10px;
}

.notification i {
    font-size: 1.2rem;
}
`;
document.head.appendChild(styleSheet);