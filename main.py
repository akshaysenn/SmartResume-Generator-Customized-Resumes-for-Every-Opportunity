import json
import sys
from datetime import datetime

def convert_json_to_html_resume(json_file_path, html_file_path=None):
    """
    Convert a JSON file containing resume data into an HTML resume.

    Args:
        json_file_path (str): Path to the JSON file
        html_file_path (str, optional): Path to output the HTML file. 
                                       If None, uses the JSON filename with .html extension.
    """
    try:
        # Read JSON file
        with open(json_file_path, 'r', encoding='utf-8') as file:
            resume_data = json.load(file)

        # Set default HTML output path if not provided
        if html_file_path is None:
            html_file_path = json_file_path.rsplit('.', 1)[0] + '.html'

        # Generate HTML content
        html_content = generate_html_resume(resume_data)

        # Write HTML to file
        with open(html_file_path, 'w', encoding='utf-8') as file:
            file.write(html_content)

        print(f"Successfully converted {json_file_path} to {html_file_path}")
        return True

    except FileNotFoundError:
        print(f"Error: Could not find file {json_file_path}")
        return False
    except json.JSONDecodeError:
        print(f"Error: {json_file_path} is not a valid JSON file")
        return False
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def generate_html_resume(resume_data):
    """Generate HTML content from resume data based on the custom format provided"""

    # Start with HTML template
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{resume_data.get('name', 'Resume')} - Resume</title>
    <style>
        body {{
            font-family: 'Helvetica', 'Arial', sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
            border-bottom: 2px solid #444;
            padding-bottom: 10px;
        }}
        .header h1 {{
            margin-bottom: 5px;
            color: #2c3e50;
        }}
        .contact-info {{
            margin-bottom: 15px;
            font-size: 0.9em;
        }}
        .section {{
            margin-bottom: 25px;
        }}
        .section-title {{
            border-bottom: 1px solid #ddd;
            padding-bottom: 5px;
            color: #2c3e50;
        }}
        .job, .education, .project, .skill-category, .hobby {{
            margin-bottom: 20px;
        }}
        .job-header, .edu-header, .project-header {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 5px;
        }}
        .organization, .institution, .project-name {{
            font-weight: bold;
        }}
        .role, .degree {{
            font-style: italic;
        }}
        .date {{
            color: #666;
        }}
        .description {{
            margin-top: 5px;
        }}
        .details {{
            margin-top: 10px;
            padding-left: 20px;
        }}
        .details li {{
            margin-bottom: 5px;
        }}
        .skills-list {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }}
        .skill {{
            background-color: #f0f0f0;
            padding: 5px 10px;
            border-radius: 3px;
            font-size: 0.9em;
        }}
        .technologies {{
            margin-top: 5px;
            display: flex;
            flex-wrap: wrap;
            gap: 5px;
        }}
        .technology {{
            background-color: #e8f4fc;
            color: #0066cc;
            padding: 3px 8px;
            border-radius: 3px;
            font-size: 0.85em;
        }}
        @media print {{
            body {{
                padding: 0;
            }}
            .page-break {{
                page-break-before: always;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
"""

    # Add name and contact information
    html += f"        <h1>{resume_data.get('name', '')}</h1>\n"

    html += '        <div class="contact-info">\n'
    if resume_data.get('email'):
        html += f"            <span>{resume_data.get('email')}</span> | \n"
    if resume_data.get('linkedin'):
        html += f"            <span><a href='https://{resume_data.get('linkedin')}'>{resume_data.get('linkedin')}</a></span> | \n"
    if resume_data.get('github'):
        html += f"            <span><a href='https://{resume_data.get('github')}'>{resume_data.get('github')}</a></span>"
    if resume_data.get('website'):
        html += f" | <span><a href='{resume_data.get('website')}'>{resume_data.get('website')}</a></span>"

    html += '\n        </div>\n'

    # Last updated info
    if resume_data.get('lastUpdated'):
        html += f"        <div><small>Last Updated: {resume_data.get('lastUpdated')}</small></div>\n"

    html += '    </div>\n'  # Close header

    # Add education section
    if resume_data.get('education'):
        html += """    <div class="section">
        <h2 class="section-title">Education</h2>
"""
        for edu in resume_data.get('education', []):
            html += f"""        <div class="education">
            <div class="edu-header">
                <span class="institution">{edu.get('institution', '')}</span>
                <span class="date">{edu.get('date', '')}</span>
            </div>
            <div class="degree">{edu.get('degree', '')}</div>
"""
            if edu.get('gpa'):
                html += f"""            <div class="description">
                <p>GPA: {edu.get('gpa', '')}</p>
            </div>
"""
            html += '        </div>\n'

        # Add high school information if available
        if resume_data.get('highSchool'):
            hs = resume_data.get('highSchool')
            html += f"""        <div class="education">
            <div class="edu-header">
                <span class="institution">{hs.get('name', '')}</span>
                <span class="date">{hs.get('date', '')}</span>
            </div>
            <div class="degree">{hs.get('note', '')}</div>
"""
            if hs.get('gpa'):
                html += f"""            <div class="description">
                <p>GPA: {hs.get('gpa', '')}</p>
            </div>
"""
            html += '        </div>\n'

        html += '    </div>\n'  # Close education section

    # Add coursework section
    if resume_data.get('coursework'):
        html += """    <div class="section">
        <h2 class="section-title">Coursework</h2>
"""
        if resume_data.get('coursework', {}).get('courses'):
            html += '        <div class="skill-category">\n'
            html += '            <div class="skills-list">\n'
            for course in resume_data.get('coursework', {}).get('courses', []):
                html += f'                <span class="skill">{course}</span>\n'
            html += '            </div>\n'
            html += '        </div>\n'

        # Add awards if available
        if resume_data.get('coursework', {}).get('awards'):
            html += '        <h3>Awards</h3>\n'
            html += '        <ul class="details">\n'
            for award in resume_data.get('coursework', {}).get('awards', []):
                html += f'            <li>{award}</li>\n'
            html += '        </ul>\n'

        html += '    </div>\n'  # Close coursework section

    # Add skills section
    if resume_data.get('skills'):
        html += """    <div class="section">
        <h2 class="section-title">Skills</h2>
"""
        for skill_category in resume_data.get('skills', []):
            html += f"""        <div class="skill-category">
            <h3>{skill_category.get('category', '')}</h3>
            <div class="skills-list">
"""
            for item in skill_category.get('items', []):
                html += f'                <span class="skill">{item}</span>\n'
            html += '            </div>\n'
            html += '        </div>\n'
        html += '    </div>\n'  # Close skills section

    # Add experience section
    if resume_data.get('experience'):
        html += """    <div class="section">
        <h2 class="section-title">Experience</h2>
"""
        for job in resume_data.get('experience', []):
            html += f"""        <div class="job">
            <div class="job-header">
                <span class="organization">{job.get('organization', '')}</span>
                <span class="date">{job.get('date', '')}</span>
            </div>
            <div class="role">{job.get('role', '')}</div>
"""
            if job.get('details'):
                html += '            <ul class="details">\n'
                for detail in job.get('details', []):
                    html += f'                <li>{detail}</li>\n'
                html += '            </ul>\n'
            html += '        </div>\n'
        html += '    </div>\n'  # Close experience section

    # Add projects section
    if resume_data.get('projects'):
        html += """    <div class="section">
        <h2 class="section-title">Projects</h2>
"""
        for project in resume_data.get('projects', []):
            html += f"""        <div class="project">
            <div class="project-header">
                <span class="project-name">{project.get('name', '')}</span>
                <span class="date">{project.get('date', '')}</span>
            </div>
"""
            if project.get('technologies'):
                html += '            <div class="technologies">\n'
                for tech in project.get('technologies', []):
                    html += f'                <span class="technology">{tech}</span>\n'
                html += '            </div>\n'

            if project.get('details'):
                html += '            <ul class="details">\n'
                for detail in project.get('details', []):
                    html += f'                <li>{detail}</li>\n'
                html += '            </ul>\n'
            html += '        </div>\n'
        html += '    </div>\n'  # Close projects section

    # Add hobbies section if available
    if resume_data.get('hobbies'):
        html += """    <div class="section">
        <h2 class="section-title">Interests & Activities</h2>
"""
        for hobby in resume_data.get('hobbies', []):
            html += f"""        <div class="hobby">
            <div class="hobby-header">
                <span class="hobby-name"><strong>{hobby.get('name', '')}</strong></span>
                {f"<span class='date'>{hobby.get('date', '')}</span>" if hobby.get('date') else ''}
            </div>
"""
            if hobby.get('details'):
                html += '            <ul class="details">\n'
                for detail in hobby.get('details', []):
                    html += f'                <li>{detail}</li>\n'
                html += '            </ul>\n'
            html += '        </div>\n'
        html += '    </div>\n'  # Close hobbies section

    # Add footer with generation date
    current_date = datetime.now().strftime("%B %d, %Y")
    html += f"""    <div class="footer">
        <p><small>Generated on {current_date}</small></p>
    </div>
"""

    # Close HTML document
    html += """</body>
</html>"""

    return html

if __name__ == "__main__":
    # Check if file path is provided as command line argument
    if len(sys.argv) < 2:
        # Default to use tailored_resume.json if no argument is provided
        json_file_path = "tailored_resume.json"
        html_file_path = None
        print(f"No arguments provided, using default file: {json_file_path}")
    else:
        json_file_path = sys.argv[1]
        html_file_path = sys.argv[2] if len(sys.argv) > 2 else None

    convert_json_to_html_resume(json_file_path, html_file_path)