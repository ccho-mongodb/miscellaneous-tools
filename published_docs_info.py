import os, sys, re, csv, toml

# Returns the path and title
# Note: only looks for titles that are surrounded by "=" lines
def get_path_and_title(file_path):
    with open(file_path) as fp:
        contents = fp.read()

    match = re.search(r'^=+.*\n(.*)\n=+$', contents, re.MULTILINE | re.DOTALL)
    title = match.group(1).strip() if match else '[ No Title ]'

    path_segments = file_path.split('/')
    path_name = ''
    if (len(path_segments) > 2):
        segments = path_segments[2:len(path_segments)-1]
        segments.append(title)
        path_name = " > ".join(segments)
    else:
        path_name = title

    return path_name

# Returns all lines that have sharedinclude or include directives
def get_include_lines(file_path):
    include_lines = []
    with open(file_path) as fp:
        for i, line in enumerate(fp):
            if 'include::' in line:
                include_lines.append("%s:%d" % (line.rstrip('\r\n'), i))

    return include_lines

# Returns all landing pages and their titles
# Note: not designed to pick up "index.txt"
def get_landing_pages(toml_file):
    landing_page_dict = {} # { path: title }
    toml_data = toml.load(toml_file)

    landing_pages = toml_data["toc_landing_pages"]
    print(landing_pages)

    #TODO: incorporate this data into output csv


# Collects all the file data for the output csv
def get_txt_files(directory):
  file_paths = []

  for root, dirs, files in os.walk(directory):
      for file in files:
          if file.endswith('.txt'):
              file_path = os.path.join(root, file)

              include_lines = get_include_lines(file_path)
              include_lines_formatted = '\n'.join(include_lines) if (len(include_lines) > 0) else ''
              first_title = get_path_and_title(file_path)

              file_paths.append((os.path.relpath(file_path, directory), first_title, include_lines_formatted))

  return file_paths

def main():
    # Path from which to search for publishable rst files
    base_path = sys.argv[1] if len(sys.argv) > 1 else '.'

    txt_files = get_txt_files(base_path)
    output_file = 'out.csv'

    with open(output_file, 'w', newline='') as f:
      writer = csv.writer(f)
      writer.writerow(['file_path', 'path_and_title', 'include_lines'])

      for path in txt_files:
        writer.writerow(path)

    print("Success! Wrote csv to: %s" % output_file)

if __name__ == '__main__':
    main()
