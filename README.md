# Dossier - Modern Resume Builder

![Dossier Screenshot](Dossier-screenshot.png) 

Dossier is a powerful, Django-based resume builder that helps users create professional resumes with ease. It offers PDF extraction, an intuitive editor, and beautifully designed templates.

🔗 **Live Demo**: Check out the website [here](https://dossier-jq2q.onrender.com)

## Features

- **Upload & Parse Resumes**: Upload a PDF and have the content extracted cleanly using `pdfplumber`.
- **AI Enhancement**: Resume content is optionally enhanced with recruiter-optimized phrasing using a connected LLM (e.g., Gemini API).
- **Editable Forms**: All resume sections (education, work experience, skills, etc.) are editable in dynamic, user-friendly forms.
- **PDF Generation**: Generate and download beautiful PDFs using `WeasyPrint`—no more messy layouts or formatting issues.
- **Modern UI**: Designed with Tailwind CSS (v4 CLI), the interface is responsive, minimalist, and easy to navigate.


## Technologies
- **Django v5.1.6**  (monolithic structure)
- **Tailwind CSS v4 (CLI, no config file)**
- **pdfplumber** – Resume parsing
- **WeasyPrint** – PDF rendering
- **Gemini API (optional)** – Resume optimization
- **JavaScript** – Frontend interactivity

## Getting Started

### Prerequisites

- Python 3.9+
- PostgreSQL
- Node.js (for Tailwind)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/mune001/Dossier

2. Set up a virtual environment:
    python -m venv .venv
    ### Linux/macOS
    source .venv/bin/activate 
    ### Windows
    .venv\Scripts\activate     

3. Install dependencies:
    pip install -r requirements.txt

4. Set up environment variables:
    ### Edit .env with your settings
    cd dossier
    cp .env.example .env

5. Run migrations:
    python manage.py migrate

6. Create a superuser:
    python manage.py createsuperuser

7. Node dependencies
    ### Ensure you have node installed
    node -v
    ### Install minify 
    npm i minify -g
    ### Tailwind CSS build (in watch mode for dev)
    npm install -D tailwindcss@3
    npx tailwindcss init
    ### Configure tailwind.config.js if new template folders are added
    npx tailwindcss -i ../static/css/input.css -o ./static/src/tailwind.css --watch
    npx tailwindcss -i ../static/css/tailwind.css -o ./static/src/tailwind-min.css --minify
    npx tailwindcss -i ../static/css/styles.css -o ./static/src/styles-min.css --minify



8. Run the development server
    python manage.py runserver

## License
This project is licensed under the MIT License.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.
