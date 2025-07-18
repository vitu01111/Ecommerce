document.addEventListener('DOMContentLoaded', function() {
    // --- Sidebar Toggle Functionality ---
    const sidebar = document.querySelector('.sidebar');
    const sidebarToggleBtn = document.getElementById('sidebar-toggle');

    // Check for mobile and set initial collapsed state
    if (window.innerWidth <= 768) {
        sidebar.classList.add('collapsed');
    }

    sidebarToggleBtn.addEventListener('click', function() {
        sidebar.classList.toggle('collapsed');
        // On small screens, 'collapsed' means 'default small', 'expanded' means 'full size'
        // This toggle helps manage the state correctly for mobile view
        if (window.innerWidth <= 768) {
            sidebar.classList.toggle('expanded');
        }
    });

    // --- Menu Item Active State ---
    const menuItems = document.querySelectorAll('.sidebar-menu .menu-item:not(.has-submenu) a');

    menuItems.forEach(item => {
        item.addEventListener('click', function(event) {
            // Remove 'active' from all other direct menu items
            document.querySelectorAll('.sidebar-menu .menu-item').forEach(li => {
                li.classList.remove('active');
            });
            // Add 'active' to the clicked parent menu item
            this.closest('.menu-item').classList.add('active');

            // Close any open submenus when a non-submenu item is clicked
            document.querySelectorAll('.menu-item.has-submenu.open').forEach(openItem => {
                openItem.classList.remove('open');
                openItem.querySelector('.submenu').style.maxHeight = null;
            });
        });
    });

    // --- Submenu Toggle Functionality ---
    const submenuToggles = document.querySelectorAll('.menu-item.has-submenu > a');

    submenuToggles.forEach(toggle => {
        toggle.addEventListener('click', function(event) {
            event.preventDefault(); // Prevent default link behavior
            const parentMenuItem = this.closest('.menu-item');
            const submenu = parentMenuItem.querySelector('.submenu');

            // Close other open submenus
            document.querySelectorAll('.menu-item.has-submenu.open').forEach(openItem => {
                if (openItem !== parentMenuItem) { // Don't close self
                    openItem.classList.remove('open');
                    openItem.querySelector('.submenu').style.maxHeight = null;
                }
            });

            // Toggle current submenu
            parentMenuItem.classList.toggle('open');
            if (parentMenuItem.classList.contains('open')) {
                // Set max-height to scrollHeight for smooth transition
                submenu.style.maxHeight = submenu.scrollHeight + 'px';
            } else {
                submenu.style.maxHeight = null; // Collapse
            }

            // Set the parent of the clicked submenu as active
            // Remove active from all other main menu items
            document.querySelectorAll('.sidebar-menu .menu-item').forEach(li => {
                if (li !== parentMenuItem) {
                    li.classList.remove('active');
                }
            });
            // Add active to the clicked submenu parent
            parentMenuItem.classList.add('active');
        });
    });

    // --- Submenu Item Click (make parent active too, close submenu) ---
    const submenuLinks = document.querySelectorAll('.submenu a');
    submenuLinks.forEach(link => {
        link.addEventListener('click', function() {
            // Remove 'active' from all menu items first
            document.querySelectorAll('.sidebar-menu .menu-item').forEach(li => {
                li.classList.remove('active');
            });

            // Add 'active' to the parent .has-submenu item
            const parentHasSubmenu = this.closest('.menu-item.has-submenu');
            if (parentHasSubmenu) {
                parentHasSubmenu.classList.add('active');
            }

            // Optionally, close the submenu after an item is clicked
            const openSubmenu = this.closest('.submenu.open');
            if (openSubmenu) {
                openSubmenu.style.maxHeight = null;
                openSubmenu.closest('.menu-item.has-submenu').classList.remove('open');
            }
        });
    });
});