import json
import ping3
import argparse
import webbrowser
from rich import print
from rich.prompt import Prompt

# add a new server
def add_server(server_name, server_ip):
    servers[server_name] = server_ip
    save_servers()

# remove a server
def remove_server(server_name):
    if server_name in servers:
        del servers[server_name]
        save_servers()

# list
def list_servers():
    for server_name, server_ip in servers.items():
        print(f"{server_name}: {server_ip}")

# save server data to JSON
def save_servers():
    with open("servers.json", "w") as server_file:
        json.dump(servers, server_file)

def open_html_report():
    webbrowser.open("report.html")

# server checks and save the results
def perform_checks():
    server_statuses = {}
    for server_name, server_ip in servers.items():
        response_time = ping3.ping(server_ip)
        if response_time is not None:
            server_statuses[server_name] = f"Online (Response Time: {response_time} ms)"
        else:
            server_statuses[server_name] = "Offline"

    # Update log.json
    existing_data = {}
    try:
        with open("logs.json", "r") as log_file:
            existing_data = json.load(log_file)
    except FileNotFoundError:
        pass

    existing_data.update(server_statuses)

    with open("logs.json", "w") as log_file:
        json.dump(existing_data, log_file)

    # Append to log.txt
    with open("log.txt", "a") as log_file_txt:
        log_file_txt.write(json.dumps(server_statuses) + '\n')

    # Generate the HTML report
    generate_report(server_statuses)

# Function to generate an HTML report
def generate_report(server_statuses):
    report_content = f"<!DOCTYPE html>\n<html>\n<head>\n<title>Server Status Report</title>\n"
    report_content += """
    <script>
        function refreshPage() {
            setTimeout(function () {
                location.reload();
            }, 60000); // Reload the page every 60 seconds (1 minute)
        }
        refreshPage();
    </script>
    """
    report_content += "</head>\n<body>\n<h1>Server Status Report</h1>\n<table>\n<tr>\n<th>Server</th>\n<th>Status</th>\n</tr>"

    for server, status in server_statuses.items():
        report_content += f"<tr>\n<td>{server}</td>\n<td>{status}</td>\n</tr>"

    report_content += "</table>\n</body>\n</html>"

    with open("report.html", "w") as report_file:
        report_file.write(report_content)


# Main menu
def main_menu():
    while True:
        print("[bold]Main Menu:[/bold]")
        menu_choice = Prompt.ask("1. Add a server\n2. Remove a server\n3. List all servers\n4. Perform checks\n5. Open HTML Report\n6. Exit", choices=["1", "2", "3", "4", "5", "6"])

        if menu_choice == "1":
            server_name = Prompt.ask("Enter server name: ")
            server_ip = Prompt.ask("Enter server IP: ")
            add_server(server_name, server_ip)
            print(f"Added server: [bold]{server_name}[/bold] with IP: [bold]{server_ip}[/bold]")

        elif menu_choice == "2":
            server_name = Prompt.ask("Enter server name to remove: ")
            remove_server(server_name)
            print(f"Removed server: [bold]{server_name}[/bold]")

        elif menu_choice == "3":
            list_servers()

        elif menu_choice == "4":
            perform_checks()
            print("Checks performed. Report generated as 'report.html'.")

        elif menu_choice == "5":
            open_html_report()  

        elif menu_choice == "6":
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    with open("servers.json", "r") as server_file:
        servers = json.load(server_file)
    main_menu()
