import os
import config


def generate_report_html(audio_files_count, other_files_count, video_files_count, updated_files_count, edited_files_count, output_html="file_report.html"):
    """Generates an HTML report of file counts."""
    total_processed = audio_files_count + other_files_count + video_files_count + updated_files_count + edited_files_count

    html_content = f"""
<!DOCTYPE html>
    <html>
    <head>
        <title>File Processing Report</title>
        <style>
            body {{ font-family: 'Arial', sans-serif; background-color: #f4f4f4; color: #333; margin: 20px; }}
            h1, h2 {{ color: #007bff; text-align: center; margin-bottom: 20px; }}
            table {{ border-collapse: collapse; width: 80%; margin: 20px auto; background-color: white; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); border-radius: 8px; overflow: hidden; }}
            th, td {{ border: 1px solid #ddd; padding: 12px 15px; text-align: left; }}
            th {{ background-color: #007bff; color: white; font-weight: bold; }}
            tr:nth-child(even) {{ background-color: #f9f9f9; }}
            tr:hover {{ background-color: #e0f7fa; }}
            p {{ line-height: 1.6; margin-bottom: 15px; padding: 10px; background-color: #e8f5e9; border-radius: 5px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05); }}
        </style>
    </head>
    <body>
        <h1>File Processing Report</h1>
        <h2>Total Files Processed</h2>
        <p>Total: {total_processed}</p>
        <h2>File Type Counts</h2>
        <table>
            <tr><th>File Type</th><th>Count</th></tr>
            <tr><td>Updated Images</td><td>{updated_files_count}</td></tr>
            <tr><td>Audio</td><td>{audio_files_count}</td></tr>
            <tr><td>Video</td><td>{video_files_count}</td></tr>
            <tr><td>Edited</td><td>{edited_files_count}</td></tr>
            <tr><td>Other types of documents</td><td>{other_files_count}</td></tr>
        </table>
        <h2>Edited Files (Metadata Issues)</h2>
        <p>Files with metadata issues or any other problem extracting those date: {edited_files_count}</p>
        <p>Those files are images.</p>
        <h2>Mapped Files (Geo-Tagged)</h2>
        <p>Files mapped with geolocation data on the generated html map: {updated_files_count}</p>
    </body>
    </html>
    """
    full_output_path = os.path.join(config.OUTPUT_PATH, output_html) #combine the folder and file name.

    with open(full_output_path, "w") as f:
        f.write(html_content)

    print(f"Report generated: {output_html}")