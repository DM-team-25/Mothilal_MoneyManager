def display_message(message):
    print("\n" + message + "\n")

def print_table(data, headers):
    if not data:
        print("No data to display.")
        return

    col_widths = {}
    for header in headers:
        max_width = len(header)
        for row in data:
            max_width = max(max_width, len(str(row.get(header, ''))))
        col_widths[header] = max_width

    header_row = " | ".join(header.ljust(col_widths[header]) for header in headers)
    print(header_row)
    print("-" * len(header_row))

    for row in data:
        row_str = " | ".join(str(row.get(header, '')).ljust(col_widths[header]) for header in headers)
        print(row_str)

def paginate_list(items, page_size=5):
    """Generator to paginate list into chunks of page_size."""
    for i in range(0, len(items), page_size):
        yield items[i:i+page_size]
