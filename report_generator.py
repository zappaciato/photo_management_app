import os
import config


def generate_report_html(audio_files_count, other_files_count, video_files_count, updated_files_count, edited_files_count, output_html="file_report.html"):
    """Generates an HTML report of file counts."""
    total_processed = audio_files_count + other_files_count + video_files_count + updated_files_count + edited_files_count

    html_content = f"""
<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>File Processing Report</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #f8f9fa;
                color: #343a40;
                margin: 0;
                padding: 20px;
                display: flex;
                flex-direction: column;
                min-height: 100vh;
            }}

            h1, h2, h3 {{
                color: #007bff;
                text-align: center;
                margin-bottom: 20px;
            }}

            h3 {{
                color:#6c757d;
                font-size: 1.1rem;
            }}

            .report-container {{
                width: 80%;
                max-width: 800px;
                margin: 20px auto;
                background-color: white;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                border-radius: 10px;
                padding: 20px;
                flex-grow: 1;
                display: flex;
                flex-direction: column;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
                border-radius: 8px;
                overflow: hidden;
            }}

            th, td {{
                border: 1px solid #dee2e6;
                padding: 12px 15px;
                text-align: left;
            }}

            th {{
                background-color: #007bff;
                color: white;
                font-weight: 600;
            }}

            tr:nth-child(even) {{
                background-color: #f2f2f2;
            }}

            tr:hover {{
                background-color: #e6f7ff;
            }}

            p {{
                line-height: 1.6;
                margin-bottom: 15px;
                padding: 15px;
                background-color: #e8f5e9;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
                border: 1px solid #c8e6c9;
            }}
        </style>
    </head>
    <body>
        <h1>File Processing Report</h1>
        <h3>by Krzysztof Flakiewicz is coding 2025</h3>
        <div class="report-container">
            <h2>Total Files Processed</h2>
            <p>Total: {total_processed}</p>

            <h2>File Type Counts</h2>
            <table>
                <thead>
                    <tr><th>File Type</th><th>Count</th></tr>
                </thead>
                <tbody>
                    <tr><td>Updated Images</td><td>{updated_files_count}</td></tr>
                    <tr><td>Audio</td><td>{audio_files_count}</td></tr>
                    <tr><td>Video</td><td>{video_files_count}</td></tr>
                    <tr><td>Edited</td><td>{edited_files_count}</td></tr>
                    <tr><td>Other types of documents</td><td>{other_files_count}</td></tr>
                </tbody>
            </table>

            <h2>Edited Files (Metadata Issues)</h2>
            <p>Files/ Images with metadata issues or any other problem extracting those date: {edited_files_count}</p>

            <h2>Mapped Files (Geo-Tagged)</h2>
            <p>Files mapped with geolocation data on the generated html map: {updated_files_count}</p>
        </div>
    </body>
    </html>
    """
    full_output_path = os.path.join(config.OUTPUT_PATH, output_html) #combine the folder and file name.

    with open(full_output_path, "w") as f:
        f.write(html_content)

    print(f"Report generated: {output_html}")