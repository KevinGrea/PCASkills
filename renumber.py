# Renumber headings and paragraphs in a markdown file.
# Very specific to PCADriverSkillsMinimumStandards.md structure.
# Headings start at H2 and paragraphs to be numbered start after an empty line
# and either with "##" or "**".
# No AST parsing, just line-by-line processing, so brittle but quick.

filename = "PCADriverSkillsMinimumStandards.md"
heading_level = 0
counts = []
max_level = 4
for i in range(max_level):
    counts.append(0)
prior_line_empty = True
out_lines = []
with open(filename, "r", encoding="utf-8") as f_in:
    in_lines = f_in.readlines()
    for line in in_lines:
        if prior_line_empty and line.startswith(("##","**")):
            prior_line_empty = False

            # Heading or paragraph to number.
            level = 0

            if line[0] == "#":
                # Heading
                heading_level = 0
                while line[heading_level] == "#":
                    heading_level += 1
                heading_level -= 2  # Adjust for zero indexing and starting at H2
                assert(0 <= heading_level <= 3)
                level = heading_level
            else:
                # Paragraph
                level = heading_level + 1  # Treat as one level deeper than current heading
            
            counts[level] += 1
            for i in range(level+1, max_level):
                counts[i] = 1
            number_str = ".".join(str(counts[i]) for i in range(level+1)) + ". "

            prefix_count = 0
            while prefix_count < len(line) and line[prefix_count] in ["#","*"]:
                prefix_count += 1

            text_start = prefix_count
            while text_start < len(line) and line[text_start] in " 0123456789.":
                text_start += 1

            out_lines.append(line[:prefix_count] + number_str + line[text_start:])
        else:
            prior_line_empty = line.strip() == ""
            out_lines.append(line)

with open(filename, "w", encoding="utf-8") as f_out:
    f_out.write("".join(out_lines))
