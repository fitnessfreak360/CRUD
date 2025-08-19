# Expense Tracker Django Project Documentation

## Overview
This is a Django-based Expense Tracker web application. It allows users to register, log in, add, edit, delete, and filter their expenses. Guests can also add expenses, edit/delete them, and later associate them with their account upon registration. The UI is modern, responsive, and built with Bootstrap 5.

---

## Features
- **User Authentication:** Register, login, logout using Django's built-in auth system.
- **Guest Mode:** Unauthenticated users (guests) can add, edit, and delete expenses stored in their session.
- **Expense Ownership:** Each expense is associated with a user or a guest session. Users only see their own expenses.
- **Expense CRUD:** Add, edit, delete expenses. Guests can edit/delete their session expenses.
- **Expense Filtering:** Filter expenses by date, month, year, and category. Only the current user's or guest's expenses are shown.
- **Expense Transfer:** When a guest registers, their session expenses are transferred to their new account.
- **Modern UI:** Bootstrap 5 styling, responsive layout, and clean navigation.

---

## Implementation Details

### 1. Project Setup
- Created a Django project and app (`expenses`).
- Installed dependencies: Django, django-widget-tweaks, Bootstrap via CDN.
- Configured virtual environment and database (SQLite).

### 2. Models
- `Expense` model: Fields for title, amount, date, category, description, and a nullable `user` ForeignKey.
- Guest expenses are stored in the session as dictionaries.

### 3. Forms
- `ExpenseForm`: Django ModelForm with custom validation for all fields.

### 4. Views
- **Authentication:**
  - `register`: Handles user registration and transfers guest session expenses to the new user.
  - Login/logout handled by Django's built-in views.
- **Expense CRUD:**
  - `expense_list`: Shows only the current user's expenses or guest session expenses.
  - `add_expense`: Adds expense for user or guest (stores in session).
  - `edit_expense`/`delete_expense`: For authenticated users, edits/deletes database expenses.
  - `edit_guest_expense`/`delete_guest_expense`: For guests, edits/deletes session expenses by index.
- **Filtering:**
  - `expense_filter`: Filters only the current user's or guest's expenses by date/month/year/category.

### 5. Templates
- **Base Layout:**
  - Responsive Bootstrap layout.
  - Navigation: Login, Register, Logout, Welcome message.
  - "Expense Tracker" heading is a clickable homepage link.
- **Expense List:**
  - Shows expenses as cards.
  - Edit/Delete buttons for both user and guest expenses (guests use index-based links).
- **Add/Edit/Delete:**
  - Unified forms for both user and guest actions.
- **Registration/Login:**
  - Custom registration template.
  - Login/logout templates styled with Bootstrap.
- **Filter Page:**
  - Allows filtering expenses by date, month, year, and category.
  - Displays total expenses, category-wise totals, and a dynamic input field for filter values.

### 6. Session Management
- Guest expenses are stored in `request.session['guest_expenses']` as a list of dicts.
- On registration, these are transferred to the new user's account and removed from the session.

### 7. URL Routing
- Main URLs in `ExpenseTracker/urls.py` include app URLs.
- App URLs in `expenses/urls.py` include:
  - CRUD routes for user expenses.
  - Index-based routes for guest expense edit/delete.
  - Registration route.

### 8. Security & Redirects
- `LOGIN_REDIRECT_URL` and `LOGOUT_REDIRECT_URL` set to homepage.
- Only authenticated users can access their own expenses.
- Guests cannot see other users' expenses.

### 9. Error Handling
- NoReverseMatch errors fixed by conditional template logic.
- 404 after login fixed by setting `LOGIN_REDIRECT_URL`.
- Filtering logic fixed to only show current user's/guest's expenses.

---

## How It Works (User Flow)
1. **Guest User:**
   - Can add, edit, delete expenses (stored in session).
   - Can register; session expenses are transferred to their new account.
2. **Registered User:**
   - Can add, edit, delete expenses (stored in database, linked to their account).
   - Can filter and view only their own expenses.
3. **Navigation:**
   - "Expense Tracker" logo is a homepage link.
   - Login/Register/Logout buttons shown as appropriate.

---

## Customization & Extensibility
- Easily add new fields to the `Expense` model.
- Add more filtering options or analytics in the views/templates.
- Enhance UI with more Bootstrap components or custom styles.

---

## File Structure
- `ExpenseTracker/`: Project settings and main URLs.
- `expenses/`: App code (models, forms, views, templates, migrations).
- `templates/expenses/`: Main UI templates.
- `templates/registration/`: Auth templates.

---

## Maintenance Notes
- All session logic is handled in views; no guest data is stored in the database until registration.
- All user-specific data is protected and isolated.
- UI is fully responsive and modern.

---

## Credits
- Built with Django, Bootstrap 5, and django-widget-tweaks.
- Custom logic for guest session management and expense transfer.

---

## Expense Filter Page Documentation

This section explains the structure, logic, and behavior of the `expense_filter.html` template in the Expense Tracker Django project.

### Purpose
The filter page allows users to view expenses filtered by date, month, year, and category. It displays total expenses, category-wise totals, and provides a dynamic input field for filter values.

### Template Structure
- **Extends:** `expenses/base.html` for consistent layout and navigation.
- **Form:**
  - **Filter Type:** Dropdown (`date`, `month`, `year`).
  - **Category:** Dropdown, dynamically populated from all available categories (default and user-created).
  - **Filter Value:** Input field, type changes based on filter type selection.
  - **Buttons:** Submit (Filter), Home (navigate to expense list).

### Dynamic Input Field
- Uses JavaScript to change the input type and placeholder based on the selected filter type:
  - `date`: Shows a date picker.
  - `month`: Shows a month picker.
  - `year`: Shows a number input (1900-2100).
  - Default: Text input for custom formats.
- On page load and when filter type changes, the input field updates accordingly.

### Expense Display Logic
- If expenses are found:
  - **Total Expense:** Shows filtered total or all-time total if no filter applied.
  - **Expense List:** Each expense displays date, category, title, and amount.
  - **Category-wise Total:** Shows total amount spent per category for the filtered results.
- If no expenses match the filter:
  - Shows an info alert: "No expenses found for this filter."

### Template Variables
- `expenses`: List of filtered expenses (queryset for users, list for guests).
- `total`: Total amount for filtered expenses.
- `all_time_total`: Total amount for all expenses (if no filter).
- `categories`: List of all categories (default and user-created).
- `category_totals`: Dictionary of totals per category.
- `filter_type`, `filter_value`, `category`: Current filter selections.

### Category Dropdown
- Populated from the `categories` variable, which is aggregated in the view to include all possible categories.
- "All Categories" option allows filtering across all categories.

### Integration with Views
- The view (`expense_filter`) prepares all variables and aggregates categories, totals, and filtered expenses.
- Handles both authenticated users (database query) and guests (session data).

### Accessibility & UX
- Uses Bootstrap 5 for responsive layout and styling.
- Input field adapts to filter type for better user experience.
- Error and info messages are clearly displayed.

### Example Usage
1. Select filter type (e.g., Month).
2. Select category (or leave as "All Categories").
3. Enter filter value (e.g., `2025-08`).
4. Click Filter to view results.

### Maintenance Notes
- Ensure the view always passes all relevant categories to the template.
- If new filter types are added, update the JavaScript and form accordingly.
- For custom categories, verify that category assignment in views/forms uses cleaned data.

---
For further details, see the Django view logic in `expenses/views.py` and form logic in `expenses/forms.py`.

# End of Expense Filter Page Documentation

# Expense Tracker Website: Code Flow & Feature Connections

## 1. Project Structure
- **ExpenseTracker/**: Django project settings and URLs.
- **expenses/**: Main app containing models, forms, views, templates.
- **templates/expenses/**: HTML templates for all pages.

## 2. Models
- **Expense (expenses/models.py):**
  - Fields: user (FK), title, amount, date, category, description.
  - CATEGORY_CHOICES: Default categories (Food, Transport, etc.).
  - Custom categories are supported via form logic.

## 3. Forms
- **ExpenseForm (expenses/forms.py):**
  - Standard fields + `new_category` for custom category input.
  - Validation ensures correct category assignment (default or custom).

## 4. Views (expenses/views.py)
- **add_expense:**
  - Handles both authenticated users and guests.
  - Uses `ExpenseForm` to validate and save data.
  - For users: saves to DB; for guests: saves to session.
  - Custom category logic: always uses cleaned data for category.
- **edit_expense / edit_guest_expense:**
  - Allows editing expenses for users (DB) and guests (session).
  - Ensures category is updated correctly.
- **delete_expense / delete_guest_expense:**
  - Deletes expense from DB or session.
- **expense_list:**
  - Displays all expenses for user or guest.
  - Shows total expense.
- **expense_filter:**
  - Filters expenses by date, month, year, and category.
  - Aggregates all categories (default + user-created) for dropdown.
  - Calculates total and category-wise totals.
  - Handles both DB (user) and session (guest) logic.
- **register:**
  - Handles user registration.
  - Clears guest session data on registration (no transfer).

## 5. Templates
- **add_expense.html / edit_expense.html:**
  - Render form fields, including custom category input.
  - Show validation errors.
- **expense_list.html:**
  - Displays all expenses, total, and edit/delete options.
- **expense_filter.html:**
  - Filter form with dynamic input type (JS logic).
  - Shows filtered expenses, total, and category-wise totals.

## 6. Guest vs. User Flow
- **Guest:**
  - Expenses stored in session (`guest_expenses`).
  - Can add, edit, delete, and filter expenses.
  - On registration, session is cleared (no transfer).
- **User:**
  - Expenses stored in DB, linked to user.
  - Can add, edit, delete, and filter expenses.
  - Custom categories are saved as plain text in DB.

## 7. Category Management
- **Default categories:** Defined in model.
- **Custom categories:** Entered via form, saved as plain text.
- **Dropdowns:** Always show all categories used by user/guest.

## 8. Filtering & Analytics
- **Filter by:** Date, month, year, category.
- **Totals:** Overall and per category.
- **Dynamic input:** JS changes input type based on filter selection.

## 9. Error Handling & Validation
- **Form validation:** Ensures required fields, correct category, amount > 0, etc.
- **Template feedback:** Shows errors and info messages.

## 10. UI/UX
- **Bootstrap 5:** Responsive design, cards, forms, buttons.
- **Navigation:** Links to add, filter, home, edit, delete.
- **Dynamic JS:** Improves filter form usability.

## 11. How Features Connect
- **Models** define data structure.
- **Forms** handle input and validation.
- **Views** orchestrate logic for CRUD, filtering, and session management.
- **Templates** render UI and display data.
- **Session vs. DB:** Views check authentication to decide where to store/retrieve expenses.
- **Category aggregation:** Views always collect all categories for dropdowns and analytics.
- **Filtering:** Views and templates work together to provide dynamic, user-friendly filtering.

---
For further details, see individual code files and the documentation section above.

# End of Expense Tracker Website Flow
