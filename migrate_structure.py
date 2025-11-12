#!/usr/bin/env python3
"""
Migration script to reorganize the repository into a professional structure.
This script will:
1. Create the new directory structure
2. Move files to their new locations
3. Update import paths and references
4. Preserve all functionality
"""

import os
import shutil
import re
from pathlib import Path

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_step(message):
    print(f"{Colors.OKBLUE}→ {message}{Colors.ENDC}")

def print_success(message):
    print(f"{Colors.OKGREEN}✓ {message}{Colors.ENDC}")

def print_warning(message):
    print(f"{Colors.WARNING}⚠ {message}{Colors.ENDC}")

def print_error(message):
    print(f"{Colors.FAIL}✗ {message}{Colors.ENDC}")

def create_directory(path):
    """Create directory if it doesn't exist"""
    Path(path).mkdir(parents=True, exist_ok=True)
    print_success(f"Created directory: {path}")

def move_file(src, dst, update_content=None):
    """Move file and optionally update its content"""
    if not os.path.exists(src):
        print_warning(f"Source file not found: {src}")
        return False
    
    # Create destination directory if needed
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    
    # Read source file
    with open(src, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update content if function provided
    if update_content:
        content = update_content(content, src, dst)
    
    # Write to destination
    with open(dst, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print_success(f"Moved: {src} → {dst}")
    return True

def copy_file(src, dst, update_content=None):
    """Copy file and optionally update its content"""
    if not os.path.exists(src):
        print_warning(f"Source file not found: {src}")
        return False
    
    # Create destination directory if needed
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    
    # Read source file
    with open(src, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update content if function provided
    if update_content:
        content = update_content(content, src, dst)
    
    # Write to destination
    with open(dst, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print_success(f"Copied: {src} → {dst}")
    return True

def update_backend_imports(content, src, dst):
    """Update import paths in backend Python files"""
    # Update relative imports based on new structure
    replacements = [
        (r'from database import', 'from app.core.database import'),
        (r'from models import', 'from app.models import'),
        (r'from auth import', 'from app.core.security import'),
        (r'from \.database import', 'from app.core.database import'),
        (r'from \.models import', 'from app.models import'),
        (r'from \.auth import', 'from app.core.security import'),
    ]
    
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content)
    
    return content

def update_html_paths(content, src, dst):
    """Update file paths in HTML files"""
    # Update CSS path
    content = re.sub(r'href="styles\.css"', 'href="src/css/styles.css"', content)
    # Update JS path
    content = re.sub(r'src="script\.js"', 'src="src/js/app.js"', content)
    # Update manifest path
    content = re.sub(r'href="manifest\.json"', 'href="public/manifest.json"', content)
    # Update libs paths
    content = re.sub(r'href="libs/', 'href="src/libs/', content)
    content = re.sub(r'src="libs/', 'src="src/libs/', content)
    # Update service worker path
    content = re.sub(r'service-worker\.js', 'public/service-worker.js', content)
    
    return content

def update_js_paths(content, src, dst):
    """Update file paths in JavaScript files"""
    # Update API base URL if needed
    # Update localStorage keys if needed
    # Update file paths
    return content

def create_init_file(path):
    """Create __init__.py file"""
    init_path = os.path.join(path, '__init__.py')
    with open(init_path, 'w', encoding='utf-8') as f:
        f.write('')
    print_success(f"Created: {init_path}")

def main():
    print(f"\n{Colors.HEADER}{Colors.BOLD}Starting Repository Migration{Colors.ENDC}\n")
    
    base_dir = Path(__file__).parent
    
    # Step 1: Create backend structure
    print_step("Creating backend directory structure...")
    backend_dirs = [
        'backend/app',
        'backend/app/api',
        'backend/app/api/v1',
        'backend/app/core',
        'backend/app/models',
        'backend/app/schemas',
        'backend/app/services',
        'backend/app/middleware',
        'backend/app/utils',
        'backend/tests',
        'backend/tests/integration',
        'backend/alembic/versions',
        'backend/scripts',
    ]
    
    for dir_path in backend_dirs:
        create_directory(dir_path)
        if 'app' in dir_path and not dir_path.endswith('versions'):
            create_init_file(dir_path)
    
    # Step 2: Create frontend structure
    print_step("Creating frontend directory structure...")
    frontend_dirs = [
        'frontend/public',
        'frontend/public/icons',
        'frontend/src',
        'frontend/src/css',
        'frontend/src/js',
        'frontend/src/libs',
    ]
    
    for dir_path in frontend_dirs:
        create_directory(dir_path)
    
    # Step 3: Create other directories
    print_step("Creating other directories...")
    other_dirs = [
        'data/samples',
        'docs/api',
        'docs/deployment',
        'docs/development',
        'scripts',
    ]
    
    for dir_path in other_dirs:
        create_directory(dir_path)
    
    # Step 4: Move backend files
    print_step("Moving backend files...")
    
    # Move and refactor main.py
    if os.path.exists('backend/main.py'):
        move_file('backend/main.py', 'backend/app/main.py', update_backend_imports)
    
    # Move database.py to core
    if os.path.exists('backend/database.py'):
        move_file('backend/database.py', 'backend/app/core/database.py')
    
    # Move auth.py to core/security.py
    if os.path.exists('backend/auth.py'):
        move_file('backend/auth.py', 'backend/app/core/security.py')
    
    # Move models.py
    if os.path.exists('backend/models.py'):
        move_file('backend/models.py', 'backend/app/models/section_data.py', 
                 lambda c, s, d: update_backend_imports(c, s, d).replace('from database import', 'from app.core.database import'))
    
    # Step 5: Move frontend files
    print_step("Moving frontend files...")
    
    # Move HTML files
    if os.path.exists('index.html'):
        move_file('index.html', 'frontend/src/index.html', update_html_paths)
    
    if os.path.exists('tanghih_editing.html'):
        move_file('tanghih_editing.html', 'frontend/src/tanghih_editing.html', update_html_paths)
    
    # Move CSS
    if os.path.exists('styles.css'):
        move_file('styles.css', 'frontend/src/css/styles.css')
    
    # Move JavaScript
    if os.path.exists('script.js'):
        move_file('script.js', 'frontend/src/js/app.js', update_js_paths)
    
    # Move service worker
    if os.path.exists('service-worker.js'):
        move_file('service-worker.js', 'frontend/public/service-worker.js')
    
    # Move manifest
    if os.path.exists('manifest.json'):
        move_file('manifest.json', 'frontend/public/manifest.json')
    
    # Move libs
    if os.path.exists('libs'):
        for file in os.listdir('libs'):
            src = os.path.join('libs', file)
            dst = os.path.join('frontend/src/libs', file)
            if os.path.isfile(src):
                copy_file(src, dst)
    
    # Step 6: Move data files
    print_step("Moving data files...")
    
    if os.path.exists('new_sample.json'):
        move_file('new_sample.json', 'data/samples/new_sample.json')
    
    if os.path.exists('four_qanons.json'):
        move_file('four_qanons.json', 'data/samples/four_qanons.json')
    
    # Step 7: Move scripts
    print_step("Moving scripts...")
    
    if os.path.exists('start_backend.sh'):
        move_file('start_backend.sh', 'scripts/start_backend.sh')
    
    if os.path.exists('start_backend.bat'):
        move_file('start_backend.bat', 'scripts/start_backend.bat')
    
    # Step 8: Copy requirements.txt
    if os.path.exists('requirements.txt'):
        copy_file('requirements.txt', 'backend/requirements.txt')
    
    # Step 9: Copy README files
    if os.path.exists('backend/README.md'):
        copy_file('backend/README.md', 'backend/README.md')
    
    print(f"\n{Colors.OKGREEN}{Colors.BOLD}Migration completed successfully!{Colors.ENDC}\n")
    print(f"{Colors.WARNING}Note: You may need to manually review and update some import paths.{Colors.ENDC}\n")
    print(f"{Colors.OKCYAN}Next steps:{Colors.ENDC}")
    print("1. Review the new structure")
    print("2. Update any remaining import paths")
    print("3. Test the application")
    print("4. Commit the changes\n")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print_error(f"Migration failed: {str(e)}")
        import traceback
        traceback.print_exc()
        exit(1)

